import {exportJourneyBackup,restoreJourneyBackup,resetJourney} from './journey-save.js?v=mandatory-dialogue-1';
import {cityStore} from './city/modules/store.js?v=auto-city-1';
import {store} from './collection/store.js';
import {CATALOG_IDS} from './collection/catalog.js';
import {GAME_UI as T} from './game-ui-text.js?v=simple-ui-1';
import {renderGameNavigation,GAME_URLS} from './navigation.js?v=mandatory-dialogue-1';
export {GAME_URLS};
const settingsIcon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z"/><path d="m9 3-1 3-3 1-2 3 2 2-1 3 2 3h3l2 3 3-1 2-2 3-1 2-3-2-2 1-3-2-3h-3l-2-3-3 1Z"/></svg>';
function loadStyle(name){const href=new URL(name,import.meta.url).href;if(![...document.querySelectorAll('link[rel="stylesheet"]')].some(n=>n.href===href)){const link=document.createElement('link');link.rel='stylesheet';link.href=href;document.head.append(link);}}
export function initializeGameShell({active='map',onMap}={}){
 if(document.body.classList.contains('collection-reading')||/\/book\//.test(location.pathname))throw Error('The game shell is not a reader toolbar.');
 if(document.querySelector('#game-shell-hud'))return window.SutraZenGameShell;
 loadStyle('./navigation.css');loadStyle('./game-shell.css');loadStyle('./game-theme.css?v=cyan-1');
 const themeURL=new URL('./game-theme.css?v=cyan-1',import.meta.url).href;const themeLink=[...document.querySelectorAll('link[rel="stylesheet"]')].find(link=>link.href===themeURL);if(themeLink)document.head.append(themeLink);
 document.body.classList.add('game-shell',`game-shell--${active}`);
 const hud=document.createElement('header');hud.id='game-shell-hud';hud.className='game-hud';hud.innerHTML=`<span class="game-hud__progress" data-game-progress aria-live="polite"></span><button class="game-hud__settings" data-game-settings>${settingsIcon}<span>${T.settings}</span></button>`;
 const navHost=document.createElement('div');navHost.innerHTML=renderGameNavigation({active});const nav=navHost.firstElementChild;
 const settingsButton=hud.querySelector('[data-game-settings]');
 const dock=document.createElement('footer');dock.className='game-dock';dock.setAttribute('aria-label',T.dockLabel);
 const row=document.createElement('div');row.className='game-dock__scroll';row.setAttribute('aria-label',T.dockLabel);
 const previous=document.createElement('button'),next=document.createElement('button');
 for(const [button,direction,label] of [[previous,-1,T.dockPrevious],[next,1,T.dockNext]]){button.className='game-dock__arrow';button.dataset.dockScroll=String(direction);button.setAttribute('aria-label',label);button.innerHTML=direction<0?'‹':'›';button.hidden=true;button.addEventListener('click',()=>row.scrollBy({left:direction*Math.max(200,row.clientWidth*.75),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'}));}
 row.append(nav,hud,settingsButton);dock.append(previous,row,next);
 function updateOverflow(){const before=row.scrollLeft>3,after=row.scrollWidth-row.clientWidth-row.scrollLeft>3;previous.hidden=!before;next.hidden=!after;dock.classList.toggle('has-overflow',before||after);dock.dataset.canScrollLeft=String(before);dock.dataset.canScrollRight=String(after);row.dataset.scrollable=String(before||after);}
 row.addEventListener('scroll',updateOverflow,{passive:true});
 row.addEventListener('focusin',event=>{const target=event.target;if(!(target instanceof HTMLElement))return;const a=target.getBoundingClientRect(),b=row.getBoundingClientRect();if(a.left<b.left||a.right>b.right)target.scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'});});
 const dockObserver=new ResizeObserver(()=>{updateOverflow();document.body.style.setProperty('--game-dock-height',dock.getBoundingClientRect().height+'px');});dockObserver.observe(dock);dockObserver.observe(row);
 const notice=document.createElement('p');notice.className='game-shell-notice';notice.id='game-shell-storage-notice';notice.setAttribute('role','status');notice.hidden=true;
 const dialog=document.createElement('dialog');dialog.className='game-settings';dialog.id='game-settings';dialog.setAttribute('aria-labelledby','game-settings-title');dialog.innerHTML=`<button class="game-settings__close" data-game-settings-close aria-label="${T.close}">×</button><h2 id="game-settings-title">${T.settingsTitle}</h2><p>${T.localSave}</p><p data-game-settings-status class="game-settings__status" role="status" hidden></p><div class="game-settings__actions"><a data-game-title href="${GAME_URLS.title}">${T.backToTitle}</a></div><section><h3>${T.saveTools}</h3><div class="game-settings__actions"><button data-game-backup>${T.backup}</button><label class="game-settings__file">${T.restore}<input data-game-import type="file" accept="application/json,.json"></label></div><div class="game-settings__actions"><button class="game-settings__danger" data-game-reset>${T.reset}</button></div></section><section><h3>${T.moreLinks}</h3><div class="game-settings__actions"><a href="${GAME_URLS.mindmap}">${T.originalMap}</a><a href="${GAME_URLS.site}">${T.originalSite}</a><a href="${GAME_URLS.sources}">${T.sources}</a></div></section><section data-game-display-section><h3>${T.displayTools}</h3><div class="game-settings__actions"><button data-game-fullscreen>${T.fullscreen}</button></div><p>${T.fullscreenNote}</p></section>`;
 document.body.append(dock,notice,dialog);let opener=null,visible=true;
 const issueText=()=>store.issue==='corrupt'?T.storageCorrupt:store.issue?T.storageUnavailable:cityStore.issue==='corrupt'?T.cityStorageCorrupt:cityStore.issue?T.cityStorageUnavailable:'';
 const showStatus=text=>{const n=dialog.querySelector('[data-game-settings-status]');n.textContent=text;n.hidden=!text;};
 function refresh(){hud.querySelector('[data-game-progress]').textContent=T.progress(store.get().completed.length,CATALOG_IDS.length);const text=issueText();notice.textContent=text;notice.hidden=!visible||!text;}
 function openSettings(event){opener=event?.currentTarget||document.activeElement;showStatus(issueText());dialog.querySelector('[data-game-fullscreen]').textContent=document.fullscreenElement?T.exitFullscreen:T.fullscreen;if(!dialog.open)dialog.showModal();}
 settingsButton.addEventListener('click',openSettings);dialog.querySelector('[data-game-settings-close]').addEventListener('click',()=>dialog.close());dialog.addEventListener('close',()=>{
  const storyAction=document.querySelector('.story-dialogue:not([hidden]) .story-dialogue__next');
  if(storyAction?.getClientRects().length)storyAction.focus({preventScroll:true});
  else if(opener?.isConnected)opener.focus({preventScroll:true});
 });
 dialog.querySelector('[data-game-backup]').addEventListener('click',()=>{const url=URL.createObjectURL(new Blob([exportJourneyBackup()],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='sutrazen-journey-v2.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
 dialog.querySelector('[data-game-import]').addEventListener('change',async event=>{const input=event.currentTarget,file=input.files?.[0];if(!file)return;try{const result=restoreJourneyBackup(await file.text());showStatus(result.ok?(result.persistent?T.restored:T.restoredTemporary):T.invalidBackup);}catch{showStatus(T.restoreFailed);}finally{input.value='';refresh();}});
 dialog.querySelector('[data-game-reset]').addEventListener('click',()=>{
  if(!window.confirm(T.resetConfirm))return;
  const result=resetJourney();showStatus(result.persistent?T.resetDone:T.authorResetTemporary);refresh();
  // Keep temporary in-memory recovery if this device could not save the reset.
  if(result.persistent)location.assign(GAME_URLS.title);
 });
 const fullButton=dialog.querySelector('[data-game-fullscreen]');if(!document.fullscreenEnabled||!document.documentElement.requestFullscreen)dialog.querySelector('[data-game-display-section]').hidden=true;
 fullButton.addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();fullButton.textContent=document.fullscreenElement?T.exitFullscreen:T.fullscreen;}catch{showStatus(T.fullscreenUnavailable);}});
 nav.addEventListener('click',event=>{if(event.target.closest('[data-game-nav="map"]')&&typeof onMap==='function'){event.preventDefault();onMap();}});for(const event of ['sutrazen:collection-progress','sutrazen:city-layout','sutrazen:journey-state'])window.addEventListener(event,refresh);
 const api={openSettings,mountMapControls({primary,tools,menu}){if(primary)row.insertBefore(primary,hud);for(const control of [tools,menu])if(control)row.insertBefore(control,settingsButton);requestAnimationFrame(updateOverflow);},setVisible(value){visible=Boolean(value);dock.hidden=!visible;refresh();if(visible)requestAnimationFrame(updateOverflow);},setProgress(value,total=CATALOG_IDS.length){if(typeof value==='number'||typeof value==='string')hud.querySelector('[data-game-progress]').textContent=typeof value==='number'?T.progress(value,total):value;else refresh();},destroy(){for(const event of ['sutrazen:collection-progress','sutrazen:city-layout','sutrazen:journey-state'])window.removeEventListener(event,refresh);dockObserver.disconnect();dock.remove();notice.remove();dialog.remove();document.body.style.removeProperty('--game-dock-height');document.body.classList.remove('game-shell',`game-shell--${active}`);delete window.SutraZenGameShell;}};
 window.SutraZenGameShell=api;refresh();return api;
}
