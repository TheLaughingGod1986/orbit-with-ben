(function () {
  // AI & credits page (Ben, 28 Oct 2026): which agents are up or out of credit, who is acting Chief, what credit is
  // left on each plan and where it went, so we can pick agents and plans on evidence. Reads the same board.json as
  // the video board (board.models from the relay, board.credits from scripts/ai_spend.py); no secrets, no writes.
  // Data comes through the site's own server (api/data.js, J2532). It reads with the server's token, so this page
  // works when the data's repo is private, and it answers 401 to a viewer who is not signed in. GitHub's public
  // addresses below are only the fallback when that server cannot be reached; they work while the repo is public.
  const DATA_REF = "https://api.github.com/repos/TheLaughingGod1986/orbit-with-ben/git/ref/heads/board-data";
  const SIGN_IN = "This page is private. Open your board link on this device to sign in, then come back to this page.";
  // One read from api/data.js. A 401 means "sign in": it is thrown, so the caller stops instead of trying GitHub.
  async function own(query, cache) {
    let key = ""; try { key = localStorage.getItem("studio-board-key") || ""; } catch (e) { /* private window */ }
    const r = await fetch("/api/data?" + query, { cache, credentials: "same-origin", headers: key ? { "x-board-key": key } : {} });
    if (r.status === 401) throw Object.assign(new Error("sign in"), { signIn: true });
    return r;
  }
  // Our own server first; the old way only if it cannot be reached or says no for another reason.
  const elsewhere = (p, old) => p.then(r => r.ok ? r : old()).catch(e => { if (e && e.signIn) throw e; return old(); });
  const oldRef = () => fetch("/api/ref", { cache: "no-cache" }).then(r => r.ok ? r : fetch(DATA_REF, { cache: "no-cache" }))
    .catch(() => fetch(DATA_REF, { cache: "no-cache" }));
  const refFetch = () => elsewhere(own("f=ref", "no-cache"), oldRef);
  const fullBoardFetch = sha => elsewhere(own("f=board" + (sha ? "&sha=" + sha : ""), sha ? "force-cache" : "no-store"),
    () => fetch(sha ? DATA_AT(sha) : DATA + "?t=" + Date.now(), { cache: sha ? "force-cache" : "no-store" }));
  const boardFetch = sha => window.__boardUpdates ? window.__boardUpdates(sha, own, fullBoardFetch) : fullBoardFetch(sha);
  const DATA_AT = sha => `https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/${sha}/board.json`;
  const DATA = "https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/board-data/board.json";
  const STALE_H = 30;   // a pool read daily is stale after a missed day (30h, J2985)
  const LOW = 0.1;      // under 10% left reads red
  const WEEKLY = new Set(["claude", "codex", "codex-macbook", "cursor", "gemini"]);
  const MONS = { jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5, jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11 };
  const DAYS = { sun: 0, mon: 1, tue: 2, wed: 3, thu: 4, fri: 5, sat: 6 };
  const POOLS = {
    flow: ["Google Flow", "monthly picture credits (AI Ultra)"],
    elevenlabs: ["ElevenLabs", "monthly voice credits"],
    vertex: ["Google Cloud / Vertex", "monthly £ Cloud credit (AI Ultra)"],
    claude: ["Claude", "weekly limit (Claude Ultra)"],
    codex: ["Codex", "weekly limit (one ChatGPT Pro account: Mac mini + MacBook)"],
    cursor: ["Cursor & Grok", "shared weekly allowance (Grok Bot runs on Cursor's pool)"],
    gemini: ["Gemini", "weekly quota (AI Ultra)"],
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

  function londonShortDate(ms) {
    return new Date(ms).toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short", timeZone: "Europe/London" }).replace(/,/g, "");
  }
  function londonClock(ms) {
    return new Date(ms).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", hour12: false, timeZone: "Europe/London" });
  }
  function londonParts(ms) {
    const p = Object.fromEntries(new Intl.DateTimeFormat("en-GB", {
      timeZone: "Europe/London", year: "numeric", month: "2-digit", day: "2-digit", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false
    }).formatToParts(new Date(ms)).map(x => [x.type, x.value]));
    return { y: Number(p.year), m0: Number(p.month) - 1, d: Number(p.day), h: Number(p.hour) % 24, min: Number(p.minute), dow: DAYS[String(p.weekday || "").slice(0, 3).toLowerCase()] };
  }
  function londonWallToUtc(y, m0, d, h, min) {
    const guess = Date.UTC(y, m0, d, h, min);
    const p = londonParts(guess);
    return guess - (Date.UTC(p.y, p.m0, p.d, p.h, p.min) - guess);
  }
  function parseClock24(hh, mm, ampm) {
    let h = Number(hh), m = Number(mm || 0);
    const ap = String(ampm || "").toLowerCase();
    if (ap === "am" && h === 12) h = 0;
    else if (ap === "pm" && h < 12) h += 12;
    return [h, m];
  }
  function parseWeeklyReset(noteStr, refMs) {
    const s = String(noteStr || "");
    const mClause = s.match(/weekly[^;]*?resets?\s+(?:on\s+|at\s+)?([^;()]+)/i) || s.match(/\bresets?\s+(?:on\s+|at\s+)?([^;()]+)/i);
    if (!mClause) return null;
    const raw = mClause[1].trim();
    if (/^\d+%\s*used/i.test(raw)) return null;
    const refYear = new Date(refMs).getUTCFullYear();
    const dm = raw.match(/^(?:(?:mon|tue|wed|thu|fri|sat|sun)[a-z]*\s+)?(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*(?:\s+(\d{4}))?(?:\s+(\d{1,2}):(\d{2})\s*([ap]m)?\s*(UTC|GMT|Z)?)?/i);
    const md = !dm && raw.match(/^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{1,2})(?:,?\s+(\d{4}))?(?:\s+(\d{1,2}):(\d{2})\s*([ap]m)?\s*(UTC|GMT|Z)?)?/i);
    if (dm || md) {
      const match = dm || md;
      const day = Number(dm ? match[1] : match[2]), mon0 = MONS[(dm ? match[2] : match[1]).slice(0, 3).toLowerCase()];
      const year = match[3] ? Number(match[3]) : refYear;
      const [h, m] = parseClock24(match[4] || 0, match[5], match[6]);
      const build = yr => match[7] ? Date.UTC(yr, mon0, day, h, m) : londonWallToUtc(yr, mon0, day, h, m);
      let endMs = build(year);
      if (!match[3] && endMs < refMs - 60 * 864e5) endMs = build(year + 1);
      return { endMs, hasClock: match[4] != null, label: `resets ${londonShortDate(endMs)}${match[4] != null ? ', ' + londonClock(endMs) : ''}` };
    }
    const wd = raw.match(/^(mon|tue|wed|thu|fri|sat|sun)[a-z]*\s+(\d{1,2})(?::(\d{2}))?\s*([ap]m)?\s*(UTC|GMT|Z)?/i);
    if (wd) {
      const targetDow = DAYS[wd[1].slice(0, 3).toLowerCase()];
      const isUtc = Boolean(wd[5]);
      const [h, m] = parseClock24(wd[2], wd[3], wd[4]);
      const rp = isUtc ? {y: new Date(refMs).getUTCFullYear(), m0: new Date(refMs).getUTCMonth(), d: new Date(refMs).getUTCDate()} : londonParts(refMs);
      for (let off = 0; off <= 7; off++) {
        const cand = isUtc ? Date.UTC(rp.y, rp.m0, rp.d + off, h, m) : londonWallToUtc(rp.y, rp.m0, rp.d + off, h, m);
        if ((isUtc ? new Date(cand).getUTCDay() : londonParts(cand).dow) === targetDow && cand >= refMs - 1800e3) {
          return { endMs: cand, hasClock: true, label: `resets ${londonShortDate(cand)}, ${londonClock(cand)}` };
        }
      }
    }
    return null;
  }

  // The pool's size: its own reading, else the plan's monthly allowance (Flow: the current AI Ultra tier).
  function poolTotal(id, pool, credits) {
    const t = (pool.latest || {}).total;
    if (t) return t;
    if (pool.unit === "%") return 100;
    const tier = (((credits || {}).tiers || {})[id] || []).find(x => x.current);
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

  function resolvePlanMeta(id, pool, credits) {
    const cyc = ((credits || {}).cycles || {})[id] || {};
    const plans = (credits || {}).plans || [];
    const matchRe = id === "flow" || id === "gemini" || id === "vertex" ? /google/i
      : id === "cursor" ? /cursor|grok/i : id === "codex" || id === "codex-macbook" ? /chatgpt|codex/i
      : id === "claude" ? /claude/i : id === "elevenlabs" ? /elevenlabs/i : null;
    const sub = plans.find(p => Array.isArray(p.pools) && p.pools.includes(id)) || (matchRe ? plans.find(p => matchRe.test(p.name || "")) : null) || {};
    const start = cyc.start || (pool && pool.since) || sub.cycleStart || "";
    const renews = sub.billingVerified === false ? "" : cyc.renews || (pool && pool.renews) || sub.renews || "";
    const aw = (pool && pool.allowanceWindow) || (sub.allowanceWindows || {})[id] || {};
    const allowanceStartMs = aw.verified === true ? Date.parse(aw.start || "") : NaN;
    const allowanceEndMs = aw.verified === true ? Date.parse(aw.end || "") : NaN;
    const gbp = cyc.gbp != null ? cyc.gbp : sub.gbp;
    const currentGbp = cyc.currentGbp != null ? cyc.currentGbp : sub.currentGbp;
    const planName = (cyc.planName || sub.name || "").replace(/\s*\(30 TB\)|\s*\(shared plan\)|\s*\(Codex\)|\s*\(top tier\)/gi, "").trim();
    const startMs = /^\d{4}-\d{2}-\d{2}$/.test(start) ? Date.parse(start + "T00:00:00Z") : NaN;
    const endMs = /^\d{4}-\d{2}-\d{2}$/.test(renews) ? Date.parse(renews + "T00:00:00Z") : NaN;
    const renewLabel = !isNaN(endMs) ? `renews ${londonShortDate(Date.parse(renews + "T12:00:00Z"))}` : "";
    const priceBit = currentGbp && gbp && currentGbp !== gbp ? `£${currentGbp}/mo now (£${gbp} planned)` : gbp != null ? `£${gbp}/mo` : "";
    const planLine = [planName, priceBit, renewLabel || (planName ? "billing renewal date unread · rolling history" : "")].filter(Boolean).join(" · ");
    return {
      planName, gbp, currentGbp, start, renews, startMs, endMs, renewLabel, planLine, allowanceStartMs, allowanceEndMs,
      usageNote: cyc.usageNote || sub.usageNote || "",
      billingNote: cyc.billingNote || sub.billingNote || "",
      next: cyc.next || sub.next || "",
    };
  }

  function poolVerdict(id, pool, credits, pmMeta, used, total, usedShare, stale, isWeekly, now) {
    if (stale || usedShare == null) return "";
    if (id === "vertex") return "Included in Google AI Ultra (£75.18/mo Cloud credit; tier follows Flow)";
    const wkAll = (pool && pool.weeklyHistory) || [];
    if (id === "gemini") {
      if (!wkAll.length) return "Included in Google AI Ultra (tier follows Flow)";
      const hits = wkAll.filter(w => w.hitLimit).length;
      const avg = Math.round(wkAll.reduce((a, w) => a + Number(w.peakUsed || 0), 0) / wkAll.length);
      return `Included in Google AI Ultra · hit weekly limit ${hits} of ${wkAll.length} ${wkAll.length === 1 ? "week" : "weeks"} (avg ${avg}%/wk)`;
    }
    const tiers = ((credits || {}).tiers || {})[id] || [];
    const cur = tiers.find(t => t.current);
    const hasBounds = !isNaN(pmMeta.startMs) && !isNaN(pmMeta.endMs) && pmMeta.endMs > pmMeta.startMs;
    const wkSpanDays = wkAll.length && wkAll[0].firstAt ? (now - Date.parse(wkAll[0].firstAt)) / 864e5 : 0;
    const cycleDaysElapsed = hasBounds ? (now - pmMeta.startMs) / 864e5 : wkSpanDays;
    const monthPct = hasBounds ? Math.round(Math.max(0, Math.min(100, ((now - pmMeta.startMs) / (pmMeta.endMs - pmMeta.startMs)) * 100))) : null;
    if (!hasBounds && !wkAll.length) return "";
    if (cycleDaysElapsed < 7) {
      const dIn = Math.max(1, Math.floor(Math.max(0, cycleDaysElapsed)));
      if (id === "flow" && pmMeta.next) {
        const past = pool.pastCycleMaxUsed ? `; last cycle used ${Math.round(pool.pastCycleMaxUsed).toLocaleString("en-GB")}` : "";
        return `Verdict after 1 week of cycle (${dIn}d in) · Keeping Ultra (£189.99) this month (9 Nov decision${past}), then review £90 tier (10,000)`;
      }
      return `Verdict after 1 week (${dIn}d of ${monthPct == null ? "rolling history" : "billing cycle"})`;
    }
    if (isWeekly) {
      const wkIn = wkAll.filter(w => w.inCycle);
      const wks = wkIn.length ? wkIn : (wkAll.length ? wkAll : [{ peakUsed: Math.round(usedShare * 100), hitLimit: usedShare >= 1 }]);
      const hits = wks.filter(w => w.hitLimit).length;
      const avgWk = Math.round(wks.reduce((a, w) => a + Number(w.peakUsed || 0), 0) / wks.length);
      const basis = cur && (cur.quotaId || cur.name);
      const comparable = wkAll.filter(w => !w.quotaId || w.quotaId === basis);
      const uncertain = wkAll.some(w => !w.quotaId || w.quotaId !== basis || w.windowUnknown);
      const maxWk = Math.max(...comparable.map(w => Number(w.peakUsed || 0)), Math.round(usedShare * 100));
      const subHit = wkAll.some(w => w.sublimitHit) || /\bfable\s+100%\s+used\b/i.test((pool.latest || {}).note || "");
      if (hits > 0) return `Keep: hit its weekly limit ${hits} of ${wks.length} ${wks.length === 1 ? "week" : "weeks"} (avg ${avgWk}%/wk)${wks.some(w => w.partial) ? " · partial observed windows; full-week use unknown" : ""}${hasBounds ? "" : " · rolling history"}`;
      if (!cur) return "";
      if (uncertain) return `Keep: quota history unknown or plan/allowance changed; no downgrade advice (${hasBounds ? "billing cycle" : "rolling history"})`;
      if (tiers.some(t => t.verified === false)) return "Keep: tier allowances unverified; no downgrade advice";
      const cheaper = tiers.filter(t => t.gbp < cur.gbp && t.allow >= maxWk / 100 * cur.allow * 1.15 && !subHit).sort((a, b) => a.gbp - b.gbp);
      if (cheaper.length && comparable.filter(w => !w.partial).length >= 2) {
        const b = cheaper[0];
        return `Could drop to ${b.name} (£${b.gbp}): peak weekly use ${Math.round(maxWk)}% (avg ${avgWk}%/wk across ${wks.length} weeks${monthPct != null ? `, ${monthPct}% of the month gone` : ""})`;
      }
      const nextDown = tiers.filter(t => t.gbp < cur.gbp).sort((a, b) => b.gbp - a.gbp)[0];
      const why = nextDown && maxWk > nextDown.allow
        ? `used ${Math.round(maxWk)}% of weekly limit (above ${nextDown.name}'s ${nextDown.allow}%${subHit ? "; Fable hit 100%" : ""})`
        : subHit ? "Fable model hit 100% weekly limit" : `avg ${avgWk}%/wk`;
      return `Keep ${cur.name} (£${cur.gbp}): ${why}`;
    }
    if (tiers.some(t => t.verified === false)) return "Keep: tier allowances unverified; no downgrade advice";
    if (!cur || used == null || !total || !monthPct) return "";
    const projectedSafe = (monthPct > 0 ? used / (monthPct / 100) : used) * 1.15;
    const histFloor = Math.max(used, Number(pool.pastCycleMaxUsed || 0), projectedSafe);
    const cheaper = tiers.filter(t => t.gbp < cur.gbp && t.allow >= histFloor).sort((a, b) => a.gbp - b.gbp);
    const uFmt = Math.round(used).toLocaleString("en-GB"), tFmt = Math.round(total).toLocaleString("en-GB");
    if (cheaper.length) {
      const b = cheaper[0];
      return `Could drop to ${b.name} (£${b.gbp}): used ${uFmt} of its ${tFmt} allowance with ${monthPct}% of the month gone`;
    }
    const nextDown = tiers.filter(t => t.gbp < cur.gbp).sort((a, b) => b.gbp - a.gbp)[0];
    const reason = nextDown && used > nextDown.allow
      ? ` (${nextDown.name}'s ${Number(nextDown.allow).toLocaleString("en-GB")} would have run out)`
      : nextDown && Number(pool.pastCycleMaxUsed || 0) > nextDown.allow
      ? ` (last cycle used ${Math.round(pool.pastCycleMaxUsed).toLocaleString("en-GB")}, above ${nextDown.name}'s ${Number(nextDown.allow).toLocaleString("en-GB")})`
      : "";
    return `Keep ${cur.name} (£${cur.gbp}): used ${uFmt} of its ${tFmt} allowance with ${monthPct}% of the month gone${reason}`;
  }

  function poolState(id, pool, credits, now) {
    const lt = pool.latest || {}, isWeekly = WEEKLY.has(id) || pool.unit === "%";
    const pmMeta = resolvePlanMeta(id, pool, credits || {});
    let total = poolTotal(id, pool, credits), used = null;
    if (pool.unit === "GBP") {
      const startBal = pool.first && pool.first.left != null ? Number(pool.first.left) : total;
      if (startBal != null && lt.left != null) used = Math.max(0, startBal - Number(lt.left));
    } else if (total != null && lt.left != null) {
      used = Math.max(0, total - Number(lt.left));
    }
    const share = total && lt.left != null ? lt.left / total : null;
    const usedShare = total && used != null ? Math.max(0, Math.min(1, used / total)) : null;
    const atMs = Date.parse(lt.at || ""), ageH = (now - atMs) / 36e5;
    let stale = !lt.at || isNaN(ageH) || ageH > STALE_H;
    let expiredWindow = false;
    const lastDate = !isNaN(atMs) ? new Date(atMs).toLocaleDateString("en-GB", { day: "numeric", month: "short", timeZone: "Europe/London" }) : "";

    let timeShare = null, windowEnd = "Time unavailable · allowance reset/window unread";
    if (isWeekly) {
      const wr = parseWeeklyReset(lt.note, !isNaN(atMs) ? atMs : now);
      if (wr) {
        windowEnd = wr.label;
        expiredWindow = now >= wr.endMs;
        stale = stale || expiredWindow;
        timeShare = Math.max(0, Math.min(1, (now - (wr.endMs - 7 * 864e5)) / (7 * 864e5)));
      }
    } else if (!isNaN(pmMeta.allowanceStartMs) && !isNaN(pmMeta.allowanceEndMs) && pmMeta.allowanceEndMs > pmMeta.allowanceStartMs) {
      windowEnd = `allowance resets ${londonShortDate(pmMeta.allowanceEndMs)}, ${londonClock(pmMeta.allowanceEndMs)}`;
      expiredWindow = now >= pmMeta.allowanceEndMs;
      stale = stale || expiredWindow;
      timeShare = Math.max(0, Math.min(1, (now - pmMeta.allowanceStartMs) / (pmMeta.allowanceEndMs - pmMeta.allowanceStartMs)));
    } else if (!isNaN(pmMeta.startMs) && !isNaN(pmMeta.endMs) && pmMeta.endMs > pmMeta.startMs) {
      windowEnd = pmMeta.renewLabel;
      timeShare = Math.max(0, Math.min(1, (now - pmMeta.startMs) / (pmMeta.endMs - pmMeta.startMs)));
    }

    if (!isWeekly && timeShare == null && !isNaN(pmMeta.allowanceEndMs)) {
      windowEnd = `allowance resets ${londonShortDate(pmMeta.allowanceEndMs)}, ${londonClock(pmMeta.allowanceEndMs)} · start unread; Time unavailable`;
      expiredWindow = now >= pmMeta.allowanceEndMs;
      stale = stale || expiredWindow;
    }
    if (expiredWindow) { timeShare = null; windowEnd = "Previous window ended · awaiting refreshed reading"; }
    let status = "green", barTone = "green", why = "";
    if (!lt.at || isNaN(ageH)) { status = "amber"; barTone = "amber"; why = "no reading yet"; }
    else if (expiredWindow) { status = "amber"; barTone = "amber"; why = "historical · awaiting refreshed reading"; }
    else if (ageH > STALE_H) { status = "amber"; barTone = "amber"; why = `no reading for ${ago(lt.at, now).replace(" ago", "")}`; }
    else if (share != null && share <= 0) { status = "red"; barTone = "red"; why = "at limit"; }
    else if (share != null && share < LOW) { status = "red"; barTone = "red"; why = "almost out"; }
    else if (usedShare != null && timeShare != null) {
      const diff = usedShare - timeShare;
      if (diff > 0.20) { status = "red"; barTone = "red"; why = "ahead of time"; }
      else if (diff > 0.08) { status = "amber"; barTone = "amber"; why = "ahead of time"; }
      else if (diff < -0.12) { status = "green"; barTone = "blue"; why = "using little"; }
      else { status = "green"; barTone = "green"; why = "on pace"; }
    }
    const burn = stale ? null : burnPerDay(pool.series, now);
    const daysLeft = burn && lt.left != null ? lt.left / burn : null;
    const verdict = poolVerdict(id, pool, credits, pmMeta, used, total, usedShare, stale, isWeekly, now);
    return { status, barTone, why, total, used, share, usedShare, timeShare, windowEnd, planLine: pmMeta.planLine, verdict, pmMeta, stale, lastDate, burn, daysLeft, left: lt.left, at: lt.at, decision: pmMeta.next, note: lt.note || "" };
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
    const hasMeter = id => pools[id] && (id !== "claude" || (pools[id].latest || {}).left != null);
    const ids = Object.keys(POOLS).filter(hasMeter).concat(Object.keys(pools).filter(id => !POOLS[id] && hasMeter(id)));
    const rows = ids.map(id => {
      const p = pools[id], s = poolState(id, p, credits, now), [name, what] = POOLS[id] || [id, p.unit];
      const usedPct = s.usedShare != null ? `${Math.round(s.usedShare * 100)}% used` : `${num(s.left, p.unit)} avail`;
      const fig = s.stale && s.lastDate ? `${usedPct} · ${s.lastDate}` : usedPct;
      const usedDetail = p.unit === "%" ? `${Math.round((s.usedShare || 0) * 100)}% of weekly limit`
        : s.used != null && s.total ? `${num(s.used, p.unit)} of ${num(s.total, p.unit)}${p.unit === "GBP" ? ` (${num(s.left, "GBP")} total promo left)` : ""}` : `${num(s.left, p.unit)} left`;
      const usedW = s.usedShare != null ? Math.max(s.usedShare > 0 ? 2 : 0, Math.round(s.usedShare * 100)) : 0;
      const timeW = s.timeShare != null ? Math.max(s.timeShare > 0 ? 2 : 0, Math.round(s.timeShare * 100)) : 0;
      const usedBar = s.usedShare != null ? `<div class="cbar"><div class="cbar-head"><strong>Used</strong><span>${esc(usedDetail)}</span></div><div class="bar"><i class="${s.barTone}" style="width:${usedW}%"></i></div></div>` : `<div class="cbar"><div class="cbar-head"><strong>Time</strong><span>${esc(s.windowEnd)}</span></div></div>`;
      const isWeekly = WEEKLY.has(id) || p.unit === "%";
      const timeBar = s.timeShare != null ? `<div class="cbar"><div class="cbar-head"><strong>Time</strong><span>${Math.round(s.timeShare * 100)}% of ${isWeekly ? "week" : "allowance window"} · ${esc(s.windowEnd)}</span></div><div class="bar"><i class="time" style="width:${timeW}%"></i></div></div>` : `<div class="cbar"><div class="cbar-head"><strong>Time</strong><span>${esc(s.windowEnd)}</span></div></div>`;
      const whyText = s.stale && s.lastDate ? `${s.why} (last read ${s.lastDate})` : s.why;
      const pacePlan = (((credits || {}).pace || {}).plans || {})[id] || {};
      const paceLine = pacePlan.line ? `<div class="verdict">${esc(pacePlan.line)}</div>` : "";
      const pace = s.daysLeft >= 1 ? ` · at this pace about ${Math.round(s.daysLeft)} days left` : "";
      const extras = [id === "flow" ? s.pmMeta.usageNote : "", id === "cursor" ? s.pmMeta.billingNote : ""].filter(Boolean).join(" · ");
      return `<li class="pool">${dot(s.status)}<div><b>${esc(name)}</b> <span class="muted">${esc(what)}</span>
        ${s.planLine ? `<div class="muted small">${esc(s.planLine)}</div>` : ""}
        <div class="figure">${esc(fig)}${whyText ? ` · <span class="${s.barTone}t">${esc(whyText)}</span>` : ""}</div>${usedBar}${timeBar}
        ${paceLine}${s.decision ? `<div class="credit-verdict">${esc(s.decision)}</div>` : ""}${s.verdict ? `<div class="verdict">${esc(s.verdict)}</div>` : ""}
        ${extras ? `<div class="muted small">${esc(extras)}</div>` : ""}
        <div class="muted small">Read ${esc(ago(s.at, now))}${pace}${s.note ? " · " + esc(clip(s.note, 160)) : ""}</div></div></li>`;
    }).join("");
    return `<section class="card"><h2>Credit left &amp; pace</h2><ul class="rows">${rows || '<li class="muted">No readings yet.</li>'}</ul>
      <p class="muted">The Mac mini reads these every morning (scripts/ai_spend_daily.py), and the MacBook updates the shared Codex reading after its runs. Readings older than 30 hours show their date. The board advises only; changing a plan is Ben's.</p></section>`;
  }

  function plansHtml(credits) {
    const plans = credits.plans || [];
    const total = plans.reduce((a, p) => a + (Number(p.gbp) || 0), 0);
    const currentTotal = plans.reduce((a, p) => a + (Number(p.currentGbp != null ? p.currentGbp : p.gbp) || 0), 0);
    const rows = plans.map(p => {
      const ren = p.billingVerified !== false && p.renews && /^\d{4}-\d{2}-\d{2}$/.test(p.renews) ? `renews ${londonShortDate(Date.parse(p.renews + "T12:00:00Z"))}` : "renewal date unread";
      const price = p.currentGbp && p.currentGbp !== p.gbp ? `£${esc(p.currentGbp)} → £${esc(p.gbp)}` : `£${esc(p.gbp)}`;
      return `<tr><td><b>${esc(p.name)}</b><div class="muted small">${esc(ren)}</div></td><td class="r">${price}</td><td class="muted">${esc(p.covers || "")}</td></tr>`;
    }).join("");
    const target = credits.target && credits.target.label ? `<p class="muted">Target: ${esc(credits.target.label)}, about £${esc(credits.target.gbp)} a month${currentTotal !== total ? ` (current billed total £${currentTotal.toFixed(2)} where recorded; billing identity unverified)` : ""}.</p>` : "";
    return `<section class="card"><h2>Plans</h2><table><tbody>${rows}</tbody>
      <tfoot><tr><td>Planned a month</td><td class="r"><b>£${total.toFixed(2).replace(/\.00$/, "")}</b></td><td class="muted">incl. VAT, each plan on its own monthly cycle</td></tr></tfoot></table>${target}</section>`;
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

  function paceHtml(credits) {
    const pace = (credits || {}).pace || {};
    const plans = pace.plans || {};
    const rows = Object.keys(plans).map(id => {
      const plan = plans[id] || {};
      return `<li>${esc(plan.name || id)}: ${esc(plan.line || "no reading yet")}</li>`;
    }).join("");
    const caps = (pace.caps || []).map(cap => `<li>${esc(cap.line || cap.label || cap.service)}</li>`).join("");
    if (!rows && !caps) return "";
    return `<section class="card"><h2>Use-it-all pace</h2><ul class="rows">${rows}</ul>
      ${caps ? `<h3>Pay-per-use caps</h3><ul class="rows">${caps}</ul>` : ""}
      ${pace.proposal ? `<p class="muted">${esc(pace.proposal)}</p>` : ""}</section>`;
  }

  function renderAI(b, now) {
    if (!b || !b.models || !b.credits) return '<p class="muted">No data yet. The Mac mini publishes it on the next board update.</p>';
    return chiefHtml(b.models, now) + modelsHtml(b.models, now) + poolsHtml(b.credits, now) + paceHtml(b.credits) + plansHtml(b.credits) + usageHtml(b.credits);
  }

  function render() {
    document.getElementById("ai").innerHTML = renderAI(board, Date.now());
    const at = (board && (board.models || {}).checkedAt) || (board || {}).publishedAt;
    document.getElementById("asof").textContent = at ? `Updated ${ago(at, Date.now())} · checks every minute` : "Loading…";
  }

  async function poll() {
    try {
      let sha = "";
      try {
        const g = await refFetch();
        if (g.ok) {
          sha = ((await g.json()).object || {}).sha || "";
          if (sha && sha === lastSha && board) return render();
        }
      } catch (e) { if (e && e.signIn) throw e; }
      const r = await boardFetch(sha);
      if (!r.ok) return;
      board = await r.json();
      if (sha) lastSha = sha;
      render();
    } catch (e) {
      document.getElementById("asof").textContent = e && e.signIn ? SIGN_IN : "Could not load the data";
    }
  }

  // AI_APP_TEST_HOOK
  poll();
  setInterval(poll, 60 * 1000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) poll(); });
})();
