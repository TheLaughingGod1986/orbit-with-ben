// Studio Kanban, live layer for the self-updating host (Ben, 14 Oct: "make it more dynamic"). Runs after the page's own
// script and leans on shim.js (window.__boardPoll, window.__boardRefresh, the "board:poll" / "board:data" events):
//   - the source line says when the data last changed and counts down to the next check, with a Refresh button;
//   - pull down at the top of the page to check now (the Home Screen app has no browser pull-to-refresh);
//   - when a read brings changes, a short note says which jobs moved (started, done, blocked, a step) and their cards
//     flash once, so a change is visible without comparing numbers.
// Data never needs a redeploy; this file is part of the page, so a change here does (board_site/build.py).
(function () {
  if (typeof renderSource !== "function" || !window.__boardPoll) return;
  const css = document.createElement("style");
  css.textContent = `
#srctxt .nchk{font-variant-numeric:tabular-nums}
#refresh.spin{opacity:.6}
.ptr{position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 6px);transform:translate(-50%,-60px);visibility:hidden;transition:transform .15s,visibility .15s;z-index:20;
  background:var(--panel);border:1px solid var(--line);border-radius:99px;padding:4px 12px;font-size:13px;color:var(--ink-2);box-shadow:var(--shadow)}
.ptr.on{transform:translate(-50%,0);visibility:visible}
.toast{position:fixed;left:50%;bottom:calc(env(safe-area-inset-bottom,0px) + 14px);transform:translate(-50%,calc(100% + 40px));visibility:hidden;transition:transform .25s,visibility .25s;z-index:20;
  max-width:min(560px,calc(100vw - 24px));background:var(--ink);color:var(--bg);border-radius:12px;padding:9px 14px;font-size:13px;line-height:1.45;
  box-shadow:0 4px 18px rgba(0,0,0,.25);cursor:pointer}
.toast.on{transform:translate(-50%,0);visibility:visible}
.toast b{font-weight:600}.toast .r{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media (prefers-reduced-motion:reduce){.ptr,.toast{transition:none}}`;
  document.head.appendChild(css);
  const $ = id => document.getElementById(id);
  const poll = window.__boardPoll;
  const secs = ms => { const s = Math.max(0, Math.round(ms / 1000)); return s < 60 ? `${s} s` : `${Math.round(s / 60)} min`; };

  // ---- Source line: last change, next check, Refresh ----
  function srcLine() {
    const t = $("srctxt"), dot = $("dot"); if (!t) return;
    const bd = window.__boardData || {}, at = ts(bd.dataChangedAt || bd.publishedAt);
    const when = isNaN(at) ? "" : `Data changed ${esc(clock(at))} · <span data-ago="${at}">${esc(ago(at))}</span> · `;
    const next = poll.busy ? "checking…" : `next check in <span class="nchk">${secs(poll.next - Date.now())}</span>`;
    const html = poll.ok ? when + next : `${when}<b class="soon">can't reach the data</b> · retrying, ${next}`;
    if (t.dataset.h !== html) { t.dataset.h = html; t.innerHTML = html; }
    if (dot) dot.className = "dot " + (poll.ok ? "live" : "warn");
  }
  const orig = renderSource;
  renderSource = function () { orig(); const t = $("srctxt"); if (t) delete t.dataset.h; srcLine(); };   // page render() calls this

  const btn = $("refresh");
  async function refresh() {
    if (!btn || btn.disabled) return;
    const before = (window.__boardData || {}).publishedAt;
    btn.disabled = true; btn.classList.add("spin"); btn.textContent = "Checking…";
    try {
      if (window.__studioCheckVersion && await window.__studioCheckVersion()) return;
      await window.__boardRefresh();
    } catch (e) {}
    btn.textContent = !poll.ok ? "Offline" : (window.__boardData || {}).publishedAt !== before ? "Data refreshed" : "Data checked";
    setTimeout(() => { btn.disabled = false; btn.classList.remove("spin"); btn.textContent = "↻ Refresh"; }, 1800);
  }
  if (btn) { btn.hidden = false; btn.textContent = "↻ Refresh"; btn.onclick = refresh; }

  setInterval(() => {
    const n = document.querySelector("#srctxt .nchk");
    if (n && !poll.busy) n.textContent = secs(poll.next - Date.now()); else srcLine();
  }, 1000);
  document.addEventListener("board:poll", srcLine);

  // ---- Pull to refresh (touch, at the very top) ----
  const ptr = document.createElement("div"); ptr.className = "ptr"; ptr.textContent = "Pull to check now"; document.body.appendChild(ptr);
  let y0 = null, pulled = 0;
  addEventListener("touchstart", e => { y0 = scrollY <= 0 && e.touches.length === 1 ? e.touches[0].clientY : null; pulled = 0; }, { passive: true });
  addEventListener("touchmove", e => {
    if (y0 === null) return;
    pulled = e.touches[0].clientY - y0;
    if (pulled > 30) { ptr.classList.add("on"); ptr.textContent = pulled > 80 ? "Release to check now" : "Pull to check now"; }
    else ptr.classList.remove("on");
  }, { passive: true });
  addEventListener("touchend", () => {
    if (y0 !== null && pulled > 80) { ptr.textContent = "Checking…"; refresh().finally(() => setTimeout(() => ptr.classList.remove("on"), 600)); }
    else ptr.classList.remove("on");
    y0 = null; pulled = 0;
  }, { passive: true });

  // ---- What changed: a short note, and the cards that moved flash once ----
  const WHAT = { claimed: "started", done: "done", blocked: "parked or blocked", open: "back in the queue", added: "added to the queue",
    removed: "taken off the queue", cancelled: "cancelled" };
  const toast = document.createElement("div"); toast.className = "toast"; toast.setAttribute("role", "status"); document.body.appendChild(toast);
  let hide = null;
  toast.onclick = () => toast.classList.remove("on");
  const filmKey = j => { const h = /^HOS\s+(\d{3})\b/.exec(j.title); if (h) return "HOS:" + h[1];
    const n = j.film || ((/^(?:OWB\s+)?(\d{3})\b/.exec(j.title) || [])[1]); return n ? "OWB:" + n : ""; };
  const flash = el => { if (!el) return; el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash"); };
  document.addEventListener("board:data", e => {
    const { first, diff } = e.detail || {};
    if (first || !diff || !diff.length) return;
    const who = d => d.what === "claimed" && d.by ? ` (${esc(WORKER[d.by] || d.by)})` : "";
    const rows = diff.slice(0, 3).map(d => `<div class="r">${d.what === "step" ? `Step ${d.step} of ${d.of} done` : (WHAT[d.what] || esc(d.what)).replace(/^./, c => c.toUpperCase())}${who(d)}: <b>${esc(plainTitle({ title: d.title }, 48))}</b></div>`);
    toast.innerHTML = `<div style="opacity:.7;font-size:12px">Just now</div>${rows.join("")}${diff.length > 3 ? `<div>and ${diff.length - 3} more</div>` : ""}`;
    toast.classList.add("on"); clearTimeout(hide); hide = setTimeout(() => toast.classList.remove("on"), 9000);
    for (const d of diff) {
      document.querySelectorAll(".jc .jid").forEach(s => { if (s.textContent === d.id) flash(s.closest(".jc")); });
      const k = filmKey(d); if (k) document.querySelectorAll(`.tf[data-key="${k}"]`).forEach(flash);
    }
    if (diff.some(d => ["claimed", "done", "step"].includes(d.what))) flash($("nowbar"));
    if (diff.some(d => d.what === "done")) flash($("daystats"));
  });
  srcLine();
})();
