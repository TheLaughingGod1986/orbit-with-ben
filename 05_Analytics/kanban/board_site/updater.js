// Code and live data have different refresh paths. Keep open phone tabs on the current code too.
(function () {
  const current=document.querySelector('meta[name="studio-version"]')?.content;
  if(!current) return;
  let busy=false,pending=null;
  function editing(){
    if(window.__studioPendingWrites) return true;
    if([...document.querySelectorAll('#youbar input,#youbar textarea')].some(x=>x.value.trim())) return true;
    try { if(typeof drafts!=="undefined" && Object.values(drafts).some(rows=>rows.length)) return true; } catch(e) {}
    return false;
  }
  function notice(message){
    let el=document.getElementById('page-update');
    if(!el){el=document.createElement('div');el.id='page-update';el.setAttribute('role','status');el.style.cssText='position:fixed;bottom:16px;left:16px;right:16px;z-index:100;padding:12px 16px;background:var(--panel,#fff);color:var(--ink,#222);border:1px solid #aaa;border-radius:10px;box-shadow:0 2px 12px #0002;font-size:14px';document.body.appendChild(el);}
    el.textContent=message;
  }
  function apply(){
    if(!pending || navigator.onLine===false) return false;
    if(editing()){notice('Page update ready. Finish or cancel your comment to apply it.');return false;}
    // Preserve the board code in local storage, the route and any existing URL options.
    // A versioned navigation also bypasses an old document in the phone's cache.
    let attempted=null;try{attempted=sessionStorage.getItem('studio-update-attempt');}catch(e){}
    if(attempted===pending){notice('Page update ready. Reload this page to apply it.');return false;}
    try{sessionStorage.setItem('studio-update-attempt',pending);}catch(e){}
    const url=new URL(location.href);url.searchParams.set('__studio_v',pending);
    location.replace(url.href);return true;
  }
  window.__studioCheckVersion=async()=>{
    if(busy) return false;
    busy=true;
    try{
      const r=await fetch('/version.json',{cache:'no-store'});
      if(!r.ok) return false;
      const data=await r.json();
      if(!/^[a-f0-9]{16}$/.test(data.version||'')) return false;
      if(data.version===current){pending=null;document.getElementById('page-update')?.remove();try{sessionStorage.removeItem('studio-update-attempt');}catch(e){}return false;}
      pending=data.version;return apply();
    }catch(e){return false;}finally{busy=false;}
  };
  window.__studioCheckVersion();
  setInterval(()=>{if(!document.hidden)window.__studioCheckVersion();},60000);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)window.__studioCheckVersion();});
  document.addEventListener('input',()=>{if(pending)setTimeout(apply,0);});
  document.addEventListener('click',()=>{if(pending)setTimeout(apply,0);});
  addEventListener('online',()=>window.__studioCheckVersion());
})();
