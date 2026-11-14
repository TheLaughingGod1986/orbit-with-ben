// Channel Tracker, self-updating host (Ben, 10 Oct: "can this be a web app too"). The page is
// 05_Analytics/dashboard/template.html, unchanged apart from build.py's patches; instead of data built into the page it
// reads tracker.json from the orbit-with-ben `board-data` branch at runtime. That file is main's
// 05_Analytics/dashboard/data.json, put there by the Mac mini's scripts/board_publish.py right after the 06:40 snapshot
// (and on its 5-minute run), so the page never needs a redeploy for new data.
//
// Order: the copy this phone saved last time (instant), then the live file; if the live file differs, it's saved and the
// page reloads once. With no saved copy and no network, the copy built into this deploy is shown. The line under the
// snapshot date always says which one you're looking at. Re-checked on return to the app and every minute.
(function () {
  const REPO = "TheLaughingGod1986/orbit-with-ben";
  // raw.githubusercontent caches a branch URL for up to 5 min and ignores query strings, so ask the GitHub API which
  // commit board-data is on and read that commit's file (it never goes stale). If the API says no, use the branch URL.
  const REF = `https://api.github.com/repos/${REPO}/git/ref/heads/board-data`;
  const AT = (sha) => `https://raw.githubusercontent.com/${REPO}/${sha}/tracker.json`;
  const BRANCH = `https://raw.githubusercontent.com/${REPO}/board-data/tracker.json`;
  const KEY = "tracker.data.v1";
  // The site's own server first (api/data.js, J2532): it reads with the server's token, so this page works when the
  // data's repo is private. A 401 from it means "sign in" and stops the read; GitHub's public addresses above are only
  // the fallback when that server cannot be reached.
  const SIGN_IN = "This page is private. Open your board link on this device to sign in, then come back to this page.";
  let signIn = false;
  async function own(query, cache) {
    let key = ""; try { key = localStorage.getItem("studio-board-key") || ""; } catch (e) { /* private window */ }
    const r = await fetch("/api/data?" + query, { cache, credentials: "same-origin", headers: key ? { "x-board-key": key } : {} });
    if (r.status === 401) throw Object.assign(new Error("sign in"), { signIn: true });
    return r;
  }
  const elsewhere = (p, old) => p.then(r => r.ok ? r : old()).catch(e => { if (e && e.signIn) throw e; return old(); });
  const el = document.getElementById("livestamp");
  const store = { get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }, set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} } };
  const parse = (t) => { try { const j = JSON.parse(t); return j && Array.isArray(j.channels) ? j : null; } catch (e) { return null; } };
  const hhmm = () => new Date().toLocaleTimeString("en-GB", { timeZone: "Europe/London", hour: "2-digit", minute: "2-digit" });
  const say = (s) => { if (el) el.textContent = s; };
  let shown = null;

  function start(text) {
    shown = text;
    window.__trackerStart(parse(text));
  }
  async function latest() {
    let sha = "";
    signIn = false;
    try {
      const g = await elsewhere(own("f=ref", "no-cache"),
        () => fetch("/api/ref", { cache: "no-cache" }).then(r => r.ok ? r : fetch(REF, { cache: "no-cache" })).catch(() => fetch(REF, { cache: "no-cache" })));
      if (g.ok) sha = ((await g.json()).object || {}).sha || "";
    } catch (e) { if (e && e.signIn) { signIn = true; return null; } }
    try {
      const r = await elsewhere(own("f=tracker", "no-cache"),
        () => fetch(sha ? AT(sha) : BRANCH + "?t=" + Date.now(), { cache: sha ? "force-cache" : "no-store" }));
      if (!r.ok) return null;
      const t = await r.text();
      return parse(t) ? t : null;
    } catch (e) { if (e && e.signIn) signIn = true; return null; }
  }
  const withTimeout = (p, ms) => Promise.race([p, new Promise((res) => setTimeout(() => res(null), ms))]);

  async function check(first) {
    const t = await (first && !shown ? withTimeout(latest(), 8000) : latest());
    if (t) {
      store.set(t);
      if (shown === null) start(t);
      else if (t !== shown) { location.reload(); return; }
      say(`Latest saved snapshot fetched ${hhmm()} · source refreshes after the 06:40 collection each morning`);
      return;
    }
    if (shown === null) {
      const baked = document.getElementById("tracker-data").textContent;
      start(parse(baked) ? baked : '{"channels":[]}');
      say(signIn ? SIGN_IN : `Couldn't reach the live data (${hhmm()}); showing the copy built into this page. It tries again when you come back to it.`);
    } else {
      say(signIn ? SIGN_IN + " Showing the copy saved on this phone." : `Couldn't reach the live data (${hhmm()}); showing the copy saved on this phone.`);
    }
  }

  const refresh=document.getElementById("tracker-refresh");
  if(refresh) refresh.onclick=async()=>{if(window.__studioCheckVersion && await window.__studioCheckVersion()) return; say("Checking the latest snapshot…");check(false);};
  const saved = store.get();
  if (saved && parse(saved)) { start(saved); say("Saved copy · checking for a newer snapshot…"); }
  else say("Loading the latest snapshot…");
  check(true);
  setInterval(() => { if (!document.hidden) check(false); }, 60 * 1000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) check(false); });
})();
