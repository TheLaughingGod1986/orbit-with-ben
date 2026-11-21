// Present urgent alerts on every Studio page, including AI and the tracker.
(() => {
  async function refresh() {
    try {
      let key = ''; try { key = localStorage.getItem('studio-board-key') || ''; } catch (_) {}
      const response = await fetch('/api/data?f=board', {cache: 'no-cache', credentials: 'same-origin',
        headers: key ? {'x-board-key': key} : {}});
      if (!response.ok) return;
      const board = await response.json();
      let banner = document.getElementById('urgent-studio-alerts');
      if (!banner) {
        banner = document.createElement('aside');
        banner.id = 'urgent-studio-alerts';
        banner.setAttribute('role', 'alert');
        banner.style.cssText = 'background:#8b1425;color:#fff;padding:14px 20px;border-bottom:2px solid #ff8591;font:600 16px/1.5 system-ui;position:relative;z-index:1000';
        document.body.prepend(banner);
      }
      banner.replaceChildren();
      const alerts = board.urgentAlerts || [];
      banner.hidden = !alerts.length;
      for (const alert of alerts) {
        const row = document.createElement('div');
        const link = document.createElement('a');
        const url = new URL(alert.url, location.origin);
        if (url.origin !== location.origin) continue;
        link.href = url.href;
        link.style.color = '#fff';
        link.textContent = alert.message + ' Open watch card ›';
        row.append(link); banner.append(row);
      }
    } catch (_) { /* Retain the last known warning during a failed read. */ }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', refresh);
  else refresh();
  setInterval(refresh, 60000);
})();
