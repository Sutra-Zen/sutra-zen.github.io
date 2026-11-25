import {store} from '../collection/store.js';
import {storyStore} from '../story/store.js?v=dialogue-two-1';
import {STORY_SCENES} from '../story/data.js?v=dialogue-two-1';
import {OPENING_VERSION as V,TRAIN_ART,TRAIN_SCENE_IDS,TRAIN_UI as T,TRAIN_TIMING as C} from './data.js?v=dialogue-two-1';

// Story presentation only: finishing/skipping never opens or completes a book.
export function canPlayTrainOpening(saved=store.get()){
 // Before the first completed book, every new title launch plays the train.
 // Bookmarks and presentation flags do not count as completing a book.
 return saved.completed.length===0;
}
const clamp=(n,min,max)=>Math.max(min,Math.min(max,n));
export function initializeTrainOpening({host=document.body}={}){
 const href=new URL('./opening.css?v='+V,import.meta.url).href;
 if(![...document.querySelectorAll('link[rel="stylesheet"]')].some(n=>n.href===href)){
  const link=document.createElement('link');link.rel='stylesheet';link.href=href;document.head.append(link);
 }
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 let overlay=null,image=null,viewport=null,copy=null,primary=null,notice=null,retry=null;
 let replay=false,finishing=false,onComplete=null,previousFocus=null,locked=[],listeners=[];
 let transitionTimer=0,guardTimer=0,guard=null,warmedArt=null,animation=null,duration=0,resizeFrame=0,milestoneFrame=0,observer=null;
 let staticMode=false,presentationStarted=false,firstPending=false;
 const listen=(target,type,handler,options)=>{target.addEventListener(type,handler,options);listeners.push(()=>target.removeEventListener(type,handler,options));};
 const progress=()=>animation&&duration?clamp(Number(animation.currentTime||0)/duration,0,1):0;
 function stopAnimation(){if(animation){animation.onfinish=null;animation.cancel();animation=null;}cancelAnimationFrame(milestoneFrame);milestoneFrame=0;}
 function clearGuard(){if(guard)document.removeEventListener('click',guard,true);guard=null;clearTimeout(guardTimer);}
 function guardFollowthrough(){
  clearGuard();guard=event=>{event.preventDefault();event.stopImmediatePropagation();};
  document.addEventListener('click',guard,true);guardTimer=setTimeout(clearGuard,C.followthroughMs);
 }
 function lockUnderlay(){
  locked=[...document.querySelectorAll('#game-title-screen,#game-content,.game-dock')].map(node=>({node,inert:node.getAttribute('inert'),aria:node.getAttribute('aria-hidden')}));
  for(const {node} of locked){node.setAttribute('inert','');node.setAttribute('aria-hidden','true');}
 }
 function restoreUnderlay(){
  for(const {node,inert,aria} of locked){
   if(inert===null)node.removeAttribute('inert');else node.setAttribute('inert',inert);
   if(aria===null)node.removeAttribute('aria-hidden');else node.setAttribute('aria-hidden',aria);
  }
  locked=[];
 }
 function showNotice(){
  const failed=overlay?.dataset.trainArtState==='unavailable';
  notice.textContent=[failed?T.imageUnavailable:overlay?.dataset.trainArtState==='loading'?T.imageLoading:'',storyStore.issue?T.storageUnavailable:''].filter(Boolean).join(' ');
  notice.hidden=!notice.textContent;retry.hidden=!failed||!TRAIN_ART.ready;
 }
 function markFirstPassed(){
  if(!firstPending||!overlay||finishing)return;
  const first=copy.querySelector('[data-scene="train-desires"]');
  if(first&&first.getBoundingClientRect().bottom>viewport.getBoundingClientRect().top)return;
  firstPending=false;overlay.dataset.trainStep='1';overlay.dataset.scene=TRAIN_SCENE_IDS[1];
  if(!replay)storyStore.markSeen(TRAIN_SCENE_IDS[0]);showNotice();
 }
 function watchMilestone(){markFirstPassed();if(firstPending&&overlay&&!finishing&&!staticMode)milestoneFrame=requestAnimationFrame(watchMilestone);}
 function layoutCrawl(){
  resizeFrame=0;if(!overlay||finishing||staticMode||!presentationStarted)return;
  const fraction=progress(),thisOverlay=overlay;stopAnimation();
  const from=viewport.clientHeight+C.edgeGapPx,to=-copy.offsetHeight-C.edgeGapPx;
  duration=clamp((from-to)/C.pixelsPerSecond*1000,C.minDurationMs,C.maxDurationMs);
  animation=copy.animate([{transform:`translateY(${from}px)`},{transform:`translateY(${to}px)`}],{duration,easing:'linear',fill:'both'});
  animation.currentTime=fraction*duration;animation.onfinish=()=>{if(overlay===thisOverlay)complete(false);};
  if(document.hidden)animation.pause();if(firstPending)milestoneFrame=requestAnimationFrame(watchMilestone);
 }
 function scheduleLayout(){if(!resizeFrame&&overlay&&!finishing&&!staticMode&&presentationStarted)resizeFrame=requestAnimationFrame(layoutCrawl);}
 function staticReading(fraction=0){
  if(!overlay||finishing)return;stopAnimation();staticMode=true;overlay.dataset.trainMode='static';overlay.classList.add('is-static');
  viewport.tabIndex=0;viewport.setAttribute('aria-label',T.readingHint);
  if(fraction)requestAnimationFrame(()=>{if(viewport)viewport.scrollTop=fraction*Math.max(0,viewport.scrollHeight-viewport.clientHeight);});
 }
 function beginPresentation(){if(presentationStarted||!overlay)return;presentationStarted=true;if(staticMode)staticReading();else scheduleLayout();}
 function loadArt(){
  if(!overlay)return;
  if(!TRAIN_ART.ready){image.hidden=true;overlay.dataset.trainArtState='unavailable';showNotice();beginPresentation();return;}
  overlay.dataset.trainArtState='loading';image.hidden=true;showNotice();image.src=TRAIN_ART.url;
 }
 function removeOverlay(){
  clearTimeout(transitionTimer);transitionTimer=0;stopAnimation();cancelAnimationFrame(resizeFrame);resizeFrame=0;
  observer?.disconnect();observer=null;for(const remove of listeners)remove();listeners=[];restoreUnderlay();overlay?.remove();
  overlay=null;image=null;viewport=null;copy=null;primary=null;notice=null;retry=null;finishing=false;
 }
 function complete(skipped){
  if(!overlay||finishing)return;finishing=true;stopAnimation();overlay.dataset.trainState='departing';overlay.classList.add('is-departing');
  if(!replay)for(const id of TRAIN_SCENE_IDS)storyStore.markSeen(id);
  const callback=onComplete,reviewing=replay;onComplete=null;
  const done=()=>{removeOverlay();guardFollowthrough();if(callback)callback({replay:reviewing,skipped});else if(previousFocus?.isConnected)previousFocus.focus({preventScroll:true});};
  if(reduced.matches||skipped)done();else transitionTimer=setTimeout(done,650);
 }
 function eat(event){event.preventDefault();event.stopImmediatePropagation();}
 function start({replay:reviewing=false,resume=false,onComplete:callback}={}){
  if(overlay||(!reviewing&&!canPlayTrainOpening()))return false;
  clearGuard();replay=reviewing;onComplete=callback;finishing=false;presentationStarted=false;
  const firstStep=resume&&!reviewing&&storyStore.hasSeen(TRAIN_SCENE_IDS[0])&&!storyStore.hasSeen(TRAIN_SCENE_IDS[1])?1:0;firstPending=firstStep===0;
  staticMode=reduced.matches||typeof Element.prototype.animate!=='function';previousFocus=document.activeElement;
  overlay=document.createElement('section');overlay.className='train-opening';overlay.dataset.trainOpening='';overlay.dataset.trainState='playing';overlay.dataset.replay=String(reviewing);overlay.dataset.trainMode=staticMode?'static':'crawl';overlay.dataset.trainStep=String(firstStep);overlay.dataset.scene=TRAIN_SCENE_IDS[firstStep];
  overlay.setAttribute('role','dialog');overlay.setAttribute('aria-modal','true');overlay.setAttribute('aria-label',T.label);
  image=document.createElement('img');image.className='train-opening__art';image.alt=T.imageAlt;image.decoding='async';image.draggable=false;
  const shade=document.createElement('div');shade.className='train-opening__shade';shade.setAttribute('aria-hidden','true');
  const light=document.createElement('div');light.className='train-opening__light';light.setAttribute('aria-hidden','true');
  viewport=document.createElement('div');viewport.className='train-opening__viewport';viewport.dataset.trainViewport='';
  copy=document.createElement('div');copy.className='train-opening__copy';copy.dataset.trainCopy='';copy.setAttribute('aria-live','off');
  for(const id of TRAIN_SCENE_IDS.slice(firstStep)){const p=document.createElement('p');p.dataset.scene=id;p.textContent=STORY_SCENES[id].text;copy.append(p);}viewport.append(copy);
  const footer=document.createElement('div');footer.className='train-opening__footer';
  notice=document.createElement('p');notice.className='train-opening__notice';notice.setAttribute('role','status');notice.hidden=true;
  retry=document.createElement('button');retry.type='button';retry.className='train-opening__retry';retry.textContent=T.retry;retry.hidden=true;
  primary=document.createElement('button');primary.type='button';primary.className='train-opening__hint';primary.dataset.trainSkip='';primary.textContent=T.continue;footer.append(notice,retry,primary);
  const thisOverlay=overlay,thisImage=image;
  listen(image,'load',()=>{if(overlay!==thisOverlay)return;overlay.dataset.trainArtState='loaded';thisImage.hidden=false;showNotice();beginPresentation();});
  listen(image,'error',()=>{if(overlay!==thisOverlay)return;overlay.dataset.trainArtState='unavailable';thisImage.hidden=true;showNotice();beginPresentation();});
  listen(overlay,'click',event=>{
   if(event.target.closest('.train-opening__retry')){eat(event);loadArt();return;}
   const explicit=Boolean(event.target.closest('[data-train-skip]'));
   if(staticMode&&!explicit)return;if(!explicit&&window.getSelection?.()?.toString())return;eat(event);complete(true);
  });
  listen(overlay,'keydown',event=>{
   if(event.key==='Escape'||(event.target.closest('[data-train-skip]')&&['Enter',' ','Spacebar'].includes(event.key))){eat(event);if(!event.repeat)complete(true);return;}
   if(event.key==='Tab'){
    const focusable=[...(staticMode?[viewport]:[]),retry,primary].filter(n=>!n.hidden&&n.getClientRects().length);
    const at=focusable.indexOf(document.activeElement);
    if(event.shiftKey&&at<=0){eat(event);focusable.at(-1)?.focus();}
    else if(!event.shiftKey&&(at<0||at===focusable.length-1)){eat(event);focusable[0]?.focus();}
   }
  });
  listen(viewport,'scroll',markFirstPassed);listen(window,'resize',scheduleLayout);
  listen(document,'visibilitychange',()=>{if(!animation||finishing)return;if(document.hidden)animation.pause();else animation.play();});
  listen(reduced,'change',event=>{if(event.matches)staticReading(progress());});
  overlay.append(image,shade,viewport,footer,light);host.append(overlay);
  if(typeof ResizeObserver==='function'){observer=new ResizeObserver(scheduleLayout);observer.observe(viewport);observer.observe(copy);}
  lockUnderlay();loadArt();primary.focus({preventScroll:true});return true;
 }
 return {start,canPlay:canPlayTrainOpening,prepare(){if(TRAIN_ART.ready&&canPlayTrainOpening()&&!warmedArt){warmedArt=new Image();warmedArt.src=TRAIN_ART.url;}},cancel(){onComplete=null;removeOverlay();clearGuard();},get isPlaying(){return Boolean(overlay);}};
}
