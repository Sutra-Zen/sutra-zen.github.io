import {store} from './collection/store.js';
import {GAME_UI as T} from './game-ui-text.js?v=simple-ui-1';
import {initializePrologue} from './prologue/prologue.js?v=character-pronouns-1';
import {authorReviewEnabled,resetAuthorJourney} from './title-review.js?v=character-pronouns-1';
// Only the author's specified attachment is accepted; no substitute illustration.
export const TITLE_ART_FILENAME='CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg';
export function initializeTitleScreen({onEnterMap,shell,opening,enabled=/^\/game(?:\/|$)/.test(location.pathname)}={}){
 const host=document.querySelector('#game-title-screen'),content=document.querySelector('#game-content');if(!host||!content)throw Error('Missing title/game content hosts.');
 const href=new URL('./title-screen.css?v=character-pronouns-1',import.meta.url).href;if(![...document.querySelectorAll('link[rel="stylesheet"]')].some(n=>n.href===href)){const link=document.createElement('link');link.rel='stylesheet';link.href=href;document.head.append(link);}
 host.querySelector('[data-title-brand]').textContent=T.brand;host.querySelector('[data-title-heading]').textContent=T.title;host.querySelector('[data-title-subtitle]').textContent=T.subtitle;host.querySelector('[data-title-tagline]').textContent=T.tagline;host.querySelector('[data-title-settings]').textContent=T.settings;
 let entered=false,prologue=null;
 const start=host.querySelector('[data-title-start]');
 function refresh(){const s=store.get();start.textContent=s.completed.length||Object.keys(s.positions).length?T.continue:T.start;}
 function enterMap({updateHash=true}={}){if(prologue?.isPlaying)return;if(updateHash&&enabled){const url=new URL(location.href);url.searchParams.delete('screen');url.hash='map';history.replaceState(null,'',url.href);}host.hidden=true;content.hidden=false;shell?.setVisible(true);if(!entered){entered=true;onEnterMap?.();}}
 function startJourney({resume=false}={}){
  if(prologue?.isPlaying||opening?.isPlaying)return;
  if(enabled&&opening?.canPlay()){
   const url=new URL(location.href);url.searchParams.delete('screen');url.hash='opening';history.replaceState(null,'',url.href);
   if(opening.start({resume,onComplete:()=>enterMap()}))return;
  }
  enterMap();
 }
 start.addEventListener('click',()=>startJourney());host.querySelector('[data-title-settings]').addEventListener('click',event=>shell?.openSettings(event));
 const query=new URLSearchParams(location.search),menuRequested=enabled&&query.get('screen')==='title';
 const hash=location.hash.slice(1).split('?')[0],skip=!enabled||(!menuRequested&&(['map','city','shelf'].includes(hash)||query.has('completed')));refresh();window.addEventListener('sutrazen:collection-progress',refresh);
 if(skip){enterMap({updateHash:false});return {enterMap,isEntered:()=>entered};}
 content.hidden=true;host.hidden=false;shell?.setVisible(false);
 prologue=initializePrologue({host,onComplete:()=>{refresh();start.focus({preventScroll:true});}});
 opening?.prepare();
 if(authorReviewEnabled()){
  const button=document.createElement('button');button.type='button';button.className='game-title-author-reset';button.dataset.titleAuthorReset='';button.textContent=T.authorReset;
  const status=document.createElement('p');status.className='game-title-reset-status';status.dataset.titleResetStatus='';status.setAttribute('role','status');status.hidden=true;
  const reviewRow=document.createElement('div');reviewRow.className='game-title-review-row';
  const settings=host.querySelector('[data-title-settings]');settings.replaceWith(reviewRow);reviewRow.append(settings,button);
  host.querySelector('.game-title-paper').insertBefore(status,host.querySelector('[data-title-brand]'));
  button.addEventListener('click',()=>{
   if(!window.confirm(T.authorResetConfirm))return;
   opening?.cancel();const result=resetAuthorJourney();refresh();status.textContent=result.persistent?T.authorResetDone:T.authorResetTemporary;status.hidden=false;
   prologue.start();
  });
 }
 const image=host.querySelector('[data-title-art]'),notice=host.querySelector('[data-title-art-notice]');
 function unavailable(){host.classList.add('is-art-pending');notice.textContent=T.titleArtUnavailable;notice.hidden=false;}
 if(host.dataset.titleArtReady==='true'){image.addEventListener('load',()=>{host.classList.remove('is-art-pending');host.classList.add('is-art-loaded');notice.hidden=true;},{once:true});image.addEventListener('error',unavailable,{once:true});image.src=host.dataset.titleArtSrc;}else unavailable();
 // Returning from settings opens the same menu directly; this view hint never
 // changes any save. Author reset can still start the prologue controller.
 if(hash==='opening')startJourney({resume:true});
 else if(menuRequested)start.focus({preventScroll:true});
 else prologue.start();
 return {enterMap,isEntered:()=>entered};
}
