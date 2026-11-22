import {store} from './collection/store.js';
import {GAME_UI as T} from './game-ui-text.js';
// Only the author's specified attachment is accepted; no substitute illustration.
export const TITLE_ART_FILENAME='CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg';
export function initializeTitleScreen({onEnterMap,shell,enabled=/^\/game(?:\/|$)/.test(location.pathname)}={}){
 const host=document.querySelector('#game-title-screen'),content=document.querySelector('#game-content');if(!host||!content)throw Error('Missing title/game content hosts.');
 const href=new URL('./title-screen.css',import.meta.url).href;if(![...document.querySelectorAll('link[rel="stylesheet"]')].some(n=>n.href===href)){const link=document.createElement('link');link.rel='stylesheet';link.href=href;document.head.append(link);}
 host.querySelector('[data-title-brand]').textContent=T.brand;host.querySelector('[data-title-heading]').textContent=T.title;host.querySelector('[data-title-subtitle]').textContent=T.subtitle;host.querySelector('[data-title-tagline]').textContent=T.tagline;host.querySelector('[data-title-settings]').textContent=T.settings;
 let entered=false;
 function refresh(){const s=store.get();host.querySelector('[data-title-start]').textContent=s.completed.length||Object.keys(s.positions).length?T.continue:T.start;}
 function enterMap({updateHash=true}={}){if(updateHash&&enabled){const url=new URL(location.href);url.hash='map';history.replaceState(null,'',url.href);}host.hidden=true;content.hidden=false;shell?.setVisible(true);if(!entered){entered=true;onEnterMap?.();}}
 host.querySelector('[data-title-start]').addEventListener('click',()=>enterMap());host.querySelector('[data-title-settings]').addEventListener('click',event=>shell?.openSettings(event));
 const hash=location.hash.slice(1).split('?')[0],skip=!enabled||['map','city','shelf'].includes(hash)||new URLSearchParams(location.search).has('completed');refresh();window.addEventListener('sutrazen:collection-progress',refresh);
 if(skip){enterMap({updateHash:false});return {enterMap,isEntered:()=>entered};}
 content.hidden=true;host.hidden=false;shell?.setVisible(false);const image=host.querySelector('[data-title-art]'),notice=host.querySelector('[data-title-art-notice]');
 function unavailable(){host.classList.add('is-art-pending');notice.textContent=T.titleArtUnavailable;notice.hidden=false;}
 if(host.dataset.titleArtReady==='true'){image.addEventListener('load',()=>{host.classList.add('is-art-loaded');notice.hidden=true;},{once:true});image.addEventListener('error',unavailable,{once:true});image.src=host.dataset.titleArtSrc;}else unavailable();
 return {enterMap,isEntered:()=>entered};
}
