import {PROLOGUE_VERSION,PROLOGUE_PARAGRAPHS,PROLOGUE_UI as T,PROLOGUE_TIMING as C} from './data.js?v=summary-merge-1';
export {PROLOGUE_VERSION};
const clamp=(n,min,max)=>Math.max(min,Math.min(max,n));
// No storage, book data, route selectors or completion records are used here.
export function initializePrologue({host,onComplete}={}){
 if(!host?.append||!host.querySelector)throw Error('A title host is required for the prologue.');
 const href=new URL(`./prologue.css?v=${PROLOGUE_VERSION}`,import.meta.url).href;
 if(![...document.querySelectorAll('link[rel="stylesheet"]')].some(link=>link.href===href)){const link=document.createElement('link');link.rel='stylesheet';link.href=href;document.head.append(link);}
 const reduced=window.matchMedia?.('(prefers-reduced-motion: reduce)');
 let phase='idle',run=0,overlay=null,viewport=null,copy=null,action=null,animation=null,duration=0,staticMode=false,resizeFrame=0,observer=null,savedPaper=null,guardTimer=0,guard=null;
 let listeners=[];
 const listen=(target,type,handler,options)=>{target.addEventListener(type,handler,options);listeners.push(()=>target.removeEventListener(type,handler,options));};
 const progress=()=>animation&&duration?clamp(Number(animation.currentTime||0)/duration,0,1):0;
 function stopAnimation(){if(animation){animation.onfinish=null;animation.cancel();animation=null;}}
 function clearGuard(){if(guard){host.removeEventListener('click',guard,true);guard=null;}clearTimeout(guardTimer);guardTimer=0;}
 function guardFollowthrough(){clearGuard();guard=event=>{event.preventDefault();event.stopImmediatePropagation();};host.addEventListener('click',guard,true);guardTimer=setTimeout(clearGuard,C.followthroughMs);}
 function restorePaper(){if(!savedPaper)return;const {paper,hidden,inert,ariaHidden}=savedPaper;paper.hidden=hidden;if(inert===null)paper.removeAttribute('inert');else paper.setAttribute('inert',inert);if(ariaHidden===null)paper.removeAttribute('aria-hidden');else paper.setAttribute('aria-hidden',ariaHidden);savedPaper=null;}
 function cleanup(){stopAnimation();cancelAnimationFrame(resizeFrame);resizeFrame=0;observer?.disconnect();observer=null;for(const remove of listeners)remove();listeners=[];overlay?.remove();overlay=null;host.classList.remove('is-prologue-active');host.removeAttribute('data-prologue-state');restorePaper();}
 function finish(reason='skip'){
  if(phase!=='playing')return false;
  phase='finished';cleanup();if(reason==='skip')guardFollowthrough();onComplete?.({reason,version:PROLOGUE_VERSION,mode:staticMode?'static':'crawl'});return true;
 }
 function staticReading(fraction=0){
  if(phase!=='playing')return;stopAnimation();staticMode=true;overlay.classList.add('is-static');overlay.dataset.prologueMode='static';host.dataset.prologueState='static';viewport.tabIndex=0;viewport.setAttribute('aria-label',T.readingHint);
  if(fraction)requestAnimationFrame(()=>{if(phase==='playing'&&viewport)viewport.scrollTop=fraction*Math.max(0,viewport.scrollHeight-viewport.clientHeight);});
 }
 function layoutCrawl(){
  resizeFrame=0;if(phase!=='playing'||staticMode||!copy)return;
  const fraction=progress(),thisRun=run;stopAnimation();const from=viewport.clientHeight+C.edgeGapPx,to=-copy.offsetHeight-C.edgeGapPx;
  duration=clamp((from-to)/C.pixelsPerSecond*1000,C.minDurationMs,C.maxDurationMs);
  animation=copy.animate([{transform:`translateY(${from}px)`},{transform:`translateY(${to}px)`}],{duration,easing:'linear',fill:'both'});animation.currentTime=fraction*duration;
  animation.onfinish=()=>{if(run===thisRun)finish('ended');};if(document.hidden)animation.pause();
 }
 function scheduleLayout(){if(!resizeFrame&&phase==='playing'&&!staticMode)resizeFrame=requestAnimationFrame(layoutCrawl);}
 function eat(event){event.preventDefault();event.stopImmediatePropagation();}
 function start(){
  if(phase==='destroyed'||phase==='playing')return false;
  clearGuard();phase='playing';run++;staticMode=Boolean(reduced?.matches)||typeof Element.prototype.animate!=='function';
  const paper=host.querySelector('.game-title-paper');if(paper){savedPaper={paper,hidden:paper.hidden,inert:paper.getAttribute('inert'),ariaHidden:paper.getAttribute('aria-hidden')};paper.hidden=true;paper.setAttribute('inert','');paper.setAttribute('aria-hidden','true');}
  host.classList.add('is-prologue-active');host.dataset.prologueState=staticMode?'static':'crawl';
  overlay=document.createElement('section');overlay.className='game-prologue';overlay.dataset.prologue='';overlay.dataset.prologueVersion=PROLOGUE_VERSION;overlay.dataset.prologueMode=staticMode?'static':'crawl';overlay.setAttribute('aria-label',T.label);overlay.tabIndex=-1;
  viewport=document.createElement('div');viewport.className='prologue-viewport';viewport.dataset.prologueViewport='';copy=document.createElement('div');copy.className='prologue-copy';copy.dataset.prologueCopy='';copy.setAttribute('aria-live','off');
  PROLOGUE_PARAGRAPHS.forEach((paragraph,index)=>{const p=document.createElement('p');p.dataset.prologueParagraph=String(index+1);paragraph.split('\n').forEach((line,lineIndex)=>{if(lineIndex)p.append(document.createElement('br'));const span=document.createElement('span');span.dataset.prologueLine=`${index+1}-${lineIndex+1}`;span.textContent=line;p.append(span);});copy.append(p);});viewport.append(copy);
  action=document.createElement('button');action.type='button';action.className='prologue-hint';action.dataset.prologueSkip='';action.textContent=T.enterMenu;overlay.append(viewport,action);host.append(overlay);
  listen(overlay,'click',event=>{const explicit=Boolean(event.target.closest('[data-prologue-skip]'));if(staticMode&&!explicit)return;if(!explicit&&window.getSelection?.()?.toString())return;eat(event);finish('skip');});
  listen(overlay,'keydown',event=>{if(event.key==='Escape'||(event.target.closest('[data-prologue-skip]')&&['Enter',' ','Spacebar'].includes(event.key))){eat(event);finish('skip');}});
  listen(window,'resize',scheduleLayout);listen(document,'visibilitychange',()=>{if(!animation||phase!=='playing')return;if(document.hidden)animation.pause();else animation.play();});
  if(reduced?.addEventListener)listen(reduced,'change',event=>{if(event.matches)staticReading(progress());});
  if(typeof ResizeObserver==='function'){observer=new ResizeObserver(scheduleLayout);observer.observe(viewport);observer.observe(copy);}
  if(staticMode)staticReading();else scheduleLayout();action.focus({preventScroll:true});return true;
 }
 return {start,finish,destroy(){if(phase==='destroyed')return;phase='destroyed';run++;cleanup();clearGuard();},get isPlaying(){return phase==='playing';}};
}
