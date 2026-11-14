"""Read historical upload results and their same-revision package tags; no writes to services."""
import datetime
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).parent
ROOTS = {'owb': pathlib.Path('/Users/benjaminoats/YouTube/orbit-with-ben'),
         'hos': pathlib.Path('/Users/benjaminoats/YouTube/History Of Science')}

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True,
                                   stderr=subprocess.DEVNULL, timeout=30)

def main():
    comparison = json.loads((HERE / 'current_comparison.json').read_text())
    output = {'checkedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'channels': {}}
    for channel, root in ROOTS.items():
        missing = {r['id'] for r in comparison[channel]['rows'] if not r['baselineTags']}
        history = git(root, 'log', '--all', '--format=%H', '--name-only', '--',
                      '02_Video-Projects/**/PACKAGE_UPLOAD_RESULT*.json')
        revision = None
        pairs = []
        for line in history.splitlines():
            if len(line) == 40 and all(c in '0123456789abcdef' for c in line):
                revision = line
            elif revision and line.endswith('.json'):
                pairs.append((revision, line))
        found = {}
        scanned = 0
        mars = []
        for revision, path in dict.fromkeys(pairs):
            try:
                data = json.loads(git(root, 'show', revision + ':' + path))
            except (subprocess.CalledProcessError, ValueError):
                continue
            scanned += 1
            vid = data.get('upload', {}).get('platformPostId')
            if vid == 'uhZSRcvngvE':
                # Record field names only; no tokens or unfiltered logs enter evidence.
                mars.append({'revision': revision, 'path': path, 'fields': sorted(data),
                             'uploadFields': sorted(data.get('upload', {}))})
            if vid not in missing:
                continue
            manifest_path = str(pathlib.PurePosixPath(path).parent / 'PACKAGE_MANIFEST.json')
            try:
                manifest = json.loads(git(root, 'show', revision + ':' + manifest_path))
                tags = manifest.get('tags', [])
                if not tags and manifest.get('tagsFile'):
                    import re
                    tag_path = str(pathlib.PurePosixPath(path).parent / manifest['tagsFile'])
                    tags = [x.strip() for x in re.split('[,\n]', git(root, 'show', revision + ':' + tag_path)) if x.strip()]
            except (subprocess.CalledProcessError, ValueError):
                continue
            if not isinstance(tags, list) or not tags or not all(isinstance(t, str) for t in tags):
                continue
            candidate = {'revision': revision, 'resultPath': path, 'manifestPath': manifest_path, 'tags': tags}
            candidates = found.setdefault(vid, [])
            if not any(c['tags'] == tags for c in candidates):
                candidates.append(candidate)
        output['channels'][channel] = {'resultVersionsScanned': scanned, 'recovered': found,
                                       'unavailableIds': sorted(missing - found.keys()), 'marsResultFields': mars}
        print(channel, 'versions', scanned, 'recovered', len(found), 'unavailable', len(missing - found.keys()), flush=True)
    (HERE / 'historical_upload_result_recovery.json').write_text(json.dumps(output, indent=2) + '\n')

if __name__ == '__main__':
    main()
