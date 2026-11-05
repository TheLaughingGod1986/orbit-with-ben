"""Canonical account occupancy for ordinary serial dispatch when capacity is enabled.

The local caller lock spans admission and process publication. Git compare/push
serializes admissions across hosts with capacity reservations. A serial admission
never expires into spare capacity: only the caller's observed exit removes it.
"""
import copy
import uuid

import capacity_reservations as reservations
import dispatch_capacity as capacity
import routing
import workflow_state as workflow


def reserve(data, *, host_id, request, observed):
    import jobs
    at = observed['at']
    hosts, leases = observed['hosts'], observed['leases']
    host = next((h for h in hosts if h.get('host') == host_id), {})
    if (capacity.host_problem(host, at) or any(
            not capacity.fresh(h, at) or h.get('registered_id') != h.get('host') for h in hosts)
            or any(not x.get('account') or x.get('recovery_required') for x in leases)
            or capacity.unattributed_claims(data, hosts, leases, at)):
        raise ValueError('serial occupancy unverified')
    occupied = list(leases)
    occupied += [dict(a, job=j['id']) for j in data.get('jobs', [])
                 if (a := reservations.active(j, at))]
    if any(not x.get("account") for x in occupied):
        raise ValueError("unattributed canonical account occupancy")
    if any(x.get('host') == host_id for x in occupied):
        raise ValueError('serial host occupied')
    laptop = host.get('role') == 'macbook'
    if laptop:
        # Use the actual ordinary queue selector, then the actual installed
        # worker/model selector. No portable CPU contract is needed for this
        # pre-existing git-only macbook/any lane.
        selected = jobs.choose_next(data, 'macbook', {'macbook', 'any'}, at)
        if not selected:
            raise ValueError('no ordinary laptop candidate')
        import macbook_worker
        worker, model = macbook_worker.pick_agent(selected,
            macbook_worker.usable(macbook_worker.installed()))
        claimant = 'macbook'
    else:
        selected = next((j for j in data.get('jobs', []) if j['id'] == request.get('job')), None)
        worker, claimant = request.get('worker'), request.get('worker')
        model = request.get('model')
        if not selected:
            raise ValueError('serial selection absent')
        # Revalidate normal eligibility (or elected-Chief review) against the
        # canonical retry snapshot. A selection changing during Git retry stops.
        if request.get('review'):
            by_id = {j['id']: j for j in data.get('jobs', [])}
            if (worker != observed['chief'] or not workflow.is_review(selected)
                    or workflow.state(selected, by_id, at) != 'review'
                    or workflow.external_hold(selected, at)
                    or workflow.dependency_problem(selected, by_id)):
                raise ValueError('Chief review selection changed')
        elif not jobs.claimable(data, selected, workflow.MINI, at, worker):
            raise ValueError('serial queue selection changed')
    report = (host.get('workers') or {}).get(worker) or {}
    account_id = report.get('account')
    account = observed['accounts'].get(account_id) or {}
    if (not worker or not model or model != routing.model_for(
            {'kind': 'chief'} if request.get('review') else selected, worker)
            or not capacity.fresh(report, at) or report.get('ready') is not True
            or not report.get('auth_evidence') or model not in report.get('verified_models', [])
            or not capacity.fresh(account, at) or account.get('ready') is not True
            or not account.get('quota_evidence') or type(account.get('limit')) is not int
            or sum(x.get('account') == account_id for x in occupied) >= account['limit']
            or workflow.capability_problem(selected, worker, at,
                {worker: report.get('capabilities') or {}})):
        raise ValueError('selected serial worker/account unavailable')
    if selected.get('repo') == 'hos' and selected.get('film'):
        raise ValueError('HOS serial admission needs supported cross-repo adapter')
    stage = reservations.stage_key(selected)
    if selected.get('film') and selected.get('stage') and (
            stage in map(tuple, observed.get('stage_claims', [])) or any(
                j['id'] != selected['id'] and reservations.active(j, at)
                and reservations.stage_key(j) == stage for j in data.get('jobs', []))):
        raise ValueError('serial stage occupied')
    value = dict(token=uuid.uuid4().hex, phase='serial', host=host_id,
        worker=worker, claimant=claimant, model=model, account=account_id,
        job=selected['id'], at=at.isoformat(), head=observed['installed_head'])
    selected['dispatch_reservation'] = value
    return copy.deepcopy(value)


def finish(receipt):
    """Call only after the bounded ordinary child positively returned.

    Exceptions/uncertain launches retain the admission for explicit recovery.
    Token comparison prevents a delayed cleanup from freeing another run.
    """
    if not receipt or not receipt.get('admission'):
        return
    import jobs
    admission = receipt['admission']
    def apply(data):
        row = next((j for j in data.get('jobs', []) if j['id'] == admission['job']), None)
        if row and row.get('dispatch_reservation') == admission:
            del row['dispatch_reservation']
        return True, None, []
    return jobs.with_git(apply, 'jobs: reconcile observed serial exit')
