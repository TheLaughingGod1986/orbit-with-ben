(function () {
  // AI & credits page (Ben, 28 Oct 2026): which agents are up or out of credit, who is acting Chief, what credit is
  // left on each plan and where it went, so we can pick agents and plans on evidence. Reads the same board.json as
  // the video board (board.models from the relay, board.credits from scripts/ai_spend.py); no secrets, no writes.
  const DATA_REF = "https://api.github.com/repos/TheLaughingGod1986/orbit-with-ben/git/ref/heads/board-data";
  const DATA_AT = sha => `https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/${sha}/board.json`;
  const DATA = "https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/board-data/board.json";
  const STALE_H = 30;   // a pool read daily is stale after a missed day
  const LOW = 0.1;      // under 10% left reads red
  const POOLS = {
    elevenlabs: ["ElevenLabs", "voice credits"],
    flow: ["Google Flow", "picture credits (AI Ultra)"],
    vertex: ["Google Cloud / Vertex", "£ of Cloud credit"],
    cursor: ["Cursor", "% of Cursor models left (Grok Bot runs here)"],
    codex: ["Codex", "% of the weekly limit left (one ChatGPT Pro account: Mac mini + MacBook)"],
  };
  let board = null, lastSha = "";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  }
  function ago(iso, now) {
    const t = Date.parse(iso || "");
    if (!t) return "never";
    const m = Math.max(0, (now - t) / 60000);
    if (m < 60) return `${Math.round(m)} min ago`;
    if (m < 48 * 60) return `${Math.round(m / 60)} h ago`;
    return `${Math.round(m / 1440)} days ago`;
  }
  function num(n, unit) {
    if (n == null || isNaN(n)) return "—";
    if (unit === "GBP") return "£" + Number(n).toFixed(2);
    if (unit === "%") return Math.round(n) + "%";
    return Math.round(n).toLocaleString("en-GB");
  }
  const clip = (s, n) => s.length <= n ? s : s.slice(0, s.lastIndexOf(" ", n) > n / 2 ? s.lastIndexOf(" ", n) : n) + "…";
  const dot = s => `<span class="dot ${esc(s)}" aria-label="${esc(s)}"></span>`;

  // The pool's size: its own reading, else the plan's monthly allowance (Flow: the current AI Ultra tier).
  function poolTotal(id, pool, credits) {
    const t = (pool.latest || {}).total;
    if (t) return t;
    if (pool.unit === "%") return 100;
    const tier = ((credits.tiers || {})[id] || []).find(x => x.current);
    return tier ? tier.allow : null;
  }

  // Credit used per day over the last 14 days of readings, counted only since the last refill (a rise).
  function burnPerDay(series, now) {
    const pts = (series || []).filter(p => p[1] != null && now - Date.parse(p[0]) <= 14 * 864e5);
    let start = 0;
    for (let i = 1; i < pts.length; i++) if (pts[i][1] > pts[i - 1][1]) start = i;
    const run = pts.slice(start);
    if (run.length < 2) return null;
    const days = (Date.parse(run[run.length - 1][0]) - Date.parse(run[0][0])) / 864e5;
    const used = run[0][1] - run[run.length - 1][1];
    return days >= 1 && used > 0 ? used / days : null;
  }

  function poolState(id, pool, credits, now) {
    const lt = pool.latest || {};
    const total = poolTotal(id, pool, credits);
    const share = total && lt.left != null ? lt.left / total : null;
    const ageH = (now - Date.parse(lt.at || "")) / 36e5;
    let status = "green", why = "";
    if (!lt.at || isNaN(ageH)) { status = "amber"; why = "no reading yet"; }
    else if (share != null && share < LOW) { status = "red"; why = "almost out"; }
    else if (ageH > STALE_H) { status = "amber"; why = `no reading for ${ago(lt.at, now).replace(" ago", "")}`; }
    const burn = burnPerDay(pool.series, now);
    const daysLeft = burn && lt.left != null ? lt.left / burn : null;
    return { status, why, total, share, burn, daysLeft, left: lt.left, at: lt.at, note: lt.note || "" };
  }

  function chiefHtml(models, now) {
    const c = models.chief || {};
    const chain = (models.chiefChain || []).map((r, i) =>
      `<li class="${r.agent === c.agent ? "on" : ""}">${dot(r.up ? "green" : "red")}<b>${i + 1}. ${esc(r.name || r.agent)}</b>` +
      `<span class="why">${esc(r.why || "")}</span></li>`).join("");
    return `<section class="card chief"><h2>Acting Chief</h2>
      <div class="big">${dot(c.agent ? "green" : "red")}${esc(c.name || "nobody")}${c.acting ? ' <span class="tag">covering</span>' : ""}</div>
      <p class="muted">Chief since ${esc(ago(c.since, now))}. The Chief is the first agent in this order that is up.</p>
      <ol class="chain">${chain}</ol></section>`;
  }

  function modelsHtml(models, now) {
    const rows = (models.models || []).map(m => `<li>${dot(m.status)}<b>${esc(m.name)}</b>` +
      `<span class="why">${esc(m.why || "")}${m.until ? " · back " + esc(new Date(m.until).toUTCString().slice(0, 22)) : ""}</span></li>`).join("");
    const stale = models.fresh === false ? `<p class="warn">The relay hasn't checked in since ${esc(ago(models.checkedAt, now))}: these may be out of date.</p>` : "";
    return `<section class="card"><h2>Agents & models</h2>${stale}<ul class="rows">${rows}</ul>
      <p class="muted">Green: working. Amber: unknown or waiting. Red: out of credit or failing; jobs go to the next agent in line. Checked ${esc(ago(models.checkedAt, now))}.</p></section>`;
  }

  function poolsHtml(credits, now) {
    const pools = credits.pools || {};
    const ids = Object.keys(POOLS).filter(id => pools[id]).concat(Object.keys(pools).filter(id => !POOLS[id] && id !== "claude"));
    const rows = ids.map(id => {
      const p = pools[id], s = poolState(id, p, credits, now), [name, what] = POOLS[id] || [id, p.unit];
      const bar = s.share != null ? `<div class="bar"><i class="${s.status}" style="width:${Math.max(2, Math.min(100, s.share * 100)).toFixed(0)}%"></i></div>` : "";
      const of = s.total && p.unit !== "%" ? ` of ${num(s.total, p.unit)}` : "";
      const pace = s.daysLeft >= 1 ? ` · at this pace about ${Math.round(s.daysLeft)} days left` : "";
      return `<li class="pool">${dot(s.status)}<div><b>${esc(name)}</b> <span class="muted">${esc(what)}</span>
        <div class="figure">${num(s.left, p.unit)} left${of}${s.why ? ` · <span class="${s.status}t">${esc(s.why)}</span>` : ""}</div>${bar}
        <div class="muted small">Read ${esc(ago(s.at, now))}${pace}${s.note ? " · " + esc(clip(s.note, 160)) : ""}</div></div></li>`;
    }).join("");
    return `<section class="card"><h2>Credit left</h2><ul class="rows">${rows || '<li class="muted">No readings yet.</li>'}</ul>
      <p class="muted">The Mac mini reads these every morning (scripts/ai_spend_daily.py), and the MacBook updates the shared Codex reading after its runs. Claude and Gemini don't publish a meter: their status above comes from what their runs report.</p></section>`;
  }

  function plansHtml(credits) {
    const plans = credits.plans || [];
    const total = plans.reduce((a, p) => a + (Number(p.gbp) || 0), 0);
    const rows = plans.map(p => `<tr><td>${esc(p.name)}</td><td class="r">£${esc(p.gbp)}</td><td class="muted">${esc(p.covers || "")}</td></tr>`).join("");
    const target = credits.target && credits.target.label ? `<p class="muted">Target: ${esc(credits.target.label)}, about £${esc(credits.target.gbp)} a month.</p>` : "";
    return `<section class="card"><h2>Plans</h2><table><tbody>${rows}</tbody>
      <tfoot><tr><td>Total a month</td><td class="r"><b>£${total}</b></td><td class="muted">incl. VAT, from list prices</td></tr></tfoot></table>${target}</section>`;
  }

  function usageHtml(credits) {
    const work = credits.miniWork || {}, by = work.byAgent || {};
    const hrs = Object.entries(by).filter(([, m]) => m >= 30).sort((a, b) => b[1] - a[1]);
    const max = Math.max(1, ...hrs.map(([, m]) => m));
    const agents = hrs.map(([a, m]) => `<li><b>${esc(a === "chief" ? "Grok" : a[0].toUpperCase() + a.slice(1))}</b>
      <div class="bar"><i class="green" style="width:${(m / max * 100).toFixed(0)}%"></i></div><span>${Math.round(m / 60)} h</span></li>`).join("");
    const films = Object.entries(credits.byFilm || {}).filter(([f]) => f !== "(none)").map(([f, d]) => {
      const bits = Object.entries(d).filter(([, v]) => v).map(([p, v]) => `${num(v, ((credits.pools || {})[p] || {}).unit)} ${esc((POOLS[p] || [p])[0])}`);
      return [f, d.elevenlabs || 0, d.flow || 0, bits.join(" · ")];
    }).sort((a, b) => (b[1] + b[2]) - (a[1] + a[2])).slice(0, 10)
      .map(([f, , , bits]) => `<tr><td>${esc(f.replace(":", " "))}</td><td>${bits}</td></tr>`).join("");
    return `<section class="card"><h2>Where it went</h2>
      <h3>Mac mini work time by agent, since ${esc(work.since || "")}</h3><ul class="hbars">${agents}</ul>
      <h3>Credit by film (top 10)</h3><table><tbody>${films}</tbody></table></section>`;
  }

  function renderAI(b, now) {
    if (!b || !b.models || !b.credits) return '<p class="muted">No data yet. The Mac mini publishes it on the next board update.</p>';
    return chiefHtml(b.models, now) + modelsHtml(b.models, now) + poolsHtml(b.credits, now) + plansHtml(b.credits) + usageHtml(b.credits);
  }

  function render() {
    document.getElementById("ai").innerHTML = renderAI(board, Date.now());
    const at = (board && (board.models || {}).checkedAt) || (board || {}).publishedAt;
    document.getElementById("asof").textContent = at ? `Updated ${ago(at, Date.now())} · checks every minute` : "Loading…";
  }

  async function poll() {
    try {
      let url = DATA + "?t=" + Date.now(), sha = "";
      try {
        const g = await fetch(DATA_REF, { cache: "no-cache" });
        if (g.ok) {
          sha = ((await g.json()).object || {}).sha || "";
          if (sha && sha === lastSha && board) return render();
          if (sha) url = DATA_AT(sha);
        }
      } catch (e) {}
      const r = await fetch(url, { cache: sha ? "force-cache" : "no-store" });
      if (!r.ok) return;
      board = await r.json();
      if (sha) lastSha = sha;
      render();
    } catch (e) {
      document.getElementById("asof").textContent = "Could not load the data";
    }
  }

  // AI_APP_TEST_HOOK
  poll();
  setInterval(poll, 60 * 1000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) poll(); });
})();
