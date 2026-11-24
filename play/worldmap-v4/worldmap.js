import {store} from '../collection/store.js';
import {routeStatus,routeBooks} from '../route/selectors.js';
import {canStartGameBook,canReviewGameBook,getGameBookAccess} from '../route/eligibility.js';
import {routeMetadata} from '../route/metadata.js';
import {initializeGameShell,GAME_URLS} from '../game-shell.js?v=dark-heart-1';
import {initializeTitleScreen} from '../title-screen.js?v=entry-no-frame-1';
import {createMapCamera} from './camera.js?v=original-frame-1';
import {initializeStoryDialogue} from '../story/dialogue.js?v=simple-ui-1';
import {storyStore} from '../story/store.js?v=mara-1';
import {consumeFirstCompletionReceipt} from '../story/completion-receipt.js?v=doubt-1';
import {initializeDoubtStage} from '../story/doubt-stage.js?v=mara-1';
import {STORY_UI} from '../story/data.js?v=simple-ui-1';
import {compactCompletionFeedback} from './completion-feedback.js?v=simple-ui-1';
import {WORLD,LANDMARKS,MEMBERS,NODES,EDGES,GEOGRAPHIC_ROAD,MAP_CONNECTIONS,conceptAnchor,sourceGroupAnchor,PRIMARY_BOOK_LANDMARK} from './data.js';
import {T} from './text.js?v=five-cities-1';
import {renderCityRegions} from './city-regions.js?v=five-cities-1';

const $=s=>document.querySelector(s);
const books=new Map(routeBooks.map(b=>[b.id,b]));
const nodes=new Map(NODES.map(n=>[n.id,n]));
const params=new URLSearchParams(location.search);
const gameEntry=/^\/game(?:\/|$)/.test(location.pathname);
const catalogURL=new URL('../collection/catalog.js',import.meta.url);
const asset=p=>new URL(p,import.meta.url).href;
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let camera=null,active=false,links='none',labels=true,selected=null,lastFocus=null,completed=params.get('completed');
const dialog=$('#wm-dialog'),content=$('#wm-dialog-content');
const shell=initializeGameShell({active:'map',onMap:()=>activateMap()});
shell.mountMapControls({primary:$('.wm-main-action'),tools:$('.wm-tools'),menu:$('.wm-menu-action')});
const toolsDialog=$('#wm-tools-dialog');let toolsFocus=null;
let doubtStage=null,activeStoryScene=null,activeStoryContext=null,activeStoryReplay=false;
const story=initializeStoryDialogue({
 host:$('#game-content'),
 onClose:()=>$('[data-wm-next]').focus({preventScroll:true}),
 onScene:(scene,{context=null,replay=false}={})=>{
  activeStoryScene=scene;activeStoryContext=context;activeStoryReplay=replay;
  syncDoubtStage();camera?.refresh();
  if(scene?.doubtState)camera?.focus({x:1248,y:566});
 },
 onDismiss:(scene,{replay,context})=>{
  if(context==='completion-reward'){clearCompletionNotice();return;}
  if(replay||(context!=='first-completion'&&scene?.group!=='first-completion'))return;
  if(scene?.action==='enter-aggregates-book')finishFirstOutro();
  else{
   // Explicitly skipping the preamble acknowledges it too. Reload can then
   // distinguish this tail from an old save that bypassed an unseen Mara.
   storyStore.markSeen('mara-watches');completeFirstOutro();
  }
 },
 onAction:(scene,{replay,context})=>{
  if(!replay&&context==='completion-reward'){
   clearCompletionNotice();
   if(scene.action==='completion-city')location.assign(GAME_URLS.city);
   else{locateNext();$('[data-wm-next]').focus({preventScroll:true});}
   return;
  }
  if(replay&&scene.action==='show-first-completion'){story.show('toward-aggregates-lake',{replay:true,context:'first-completion'});return;}
  if(!replay&&context==='first-completion'&&scene.action==='enter-aggregates-book'){finishFirstOutro();return;}
  if(!replay&&scene.action==='enter-first-book'&&currentBook()?.id===scene.bookId)openReader(scene.bookId,{bypassDoubt:true});
  else if(!replay&&scene.action==='enter-aggregates-book'&&currentBook()?.id===scene.bookId)openReader(scene.bookId,{bypassAggregatesIntro:true});
  else if(!replay&&scene.action==='show-first-completion')completeFirstOutro();
  else{locateNext();$('[data-wm-next]').focus({preventScroll:true});}
 }
});
$('[data-wm-story-replay]').textContent=STORY_UI.replay;
$('[data-wm-completion-replay]').textContent=STORY_UI.replayCompletion;
function syncDoubtStage(){
 const done=store.get().completed.includes('four-truths');
 const state=activeStoryScene?.doubtState||(!done&&storyStore.hasSeen('doubt-at-ruins')?'waiting':'hidden');
 doubtStage?.update({state});
}
function firstCompletionStory(hasReceipt){
 const saved=store.get(),done=saved.completed.includes('four-truths'),last=saved.positions['four-truths']===books.get('four-truths').totalSteps-1;
 if(Object.hasOwn(saved.positions,'five-aggregates')||saved.completed.includes('five-aggregates'))return false;
 const pending=storyStore.hasSeen('first-book-insight')&&!storyStore.hasSeen('doubt-recedes');
 if(!done||!last||!storyStore.hasSeen('doubt-at-ruins')||storyStore.hasSeen('doubt-recedes')||(!hasReceipt&&!pending))return false;
 const l=landmarkFor('four-truths');selected=l.id;camera?.focus({x:l.x,y:l.y});
 // Keep the cutoff pending through the lake transition, so reload resumes it
 // before the reward panel can branch to the city or the next station.
 const nextScene=!pending?'first-book-insight':!storyStore.hasSeen('mara-watches')?'doubt-recedes':storyStore.hasSeen('toward-aggregates-lake')?'toward-aggregates-lake':'mara-watches';
 story.show(nextScene,{context:'first-completion'});return true;
}
function showCompletionTransition(){
 const s=store.get(),a=getGameBookAccess('five-aggregates',s.completed,s.positions);
 if(!s.completed.includes('four-truths')||!a.canStart||Object.hasOwn(s.positions,'five-aggregates')||storyStore.hasSeen('toward-aggregates-lake'))return false;
 dialog.close();
 return story.show('toward-aggregates-lake',{context:'first-completion'});
}
function finishFirstOutro(){storyStore.markSeen('doubt-recedes');completedFeedback('four-truths');}
function completeFirstOutro(){if(!showCompletionTransition())finishFirstOutro();}
function resumeLegacyTransition(){
 // Repair the previous release's split outro, not unrelated historical saves.
 return store.get().positions['four-truths']===books.get('four-truths').totalSteps-1&&storyStore.hasSeen('mara-watches')&&storyStore.hasSeen('doubt-recedes')&&showCompletionTransition();
}
function completionStoryOpen(){return story.isOpen&&activeStoryContext==='first-completion'&&!activeStoryReplay;}
function focusCompletionStory(){$('.story-dialogue__next').focus({preventScroll:true});}
document.addEventListener('click',event=>{
 if(!completionStoryOpen()||event.target.closest('.story-dialogue'))return;
 const entry=event.target.closest('[data-game-nav],[data-wm-next],[data-wm-current],[data-wm-next-station],[data-wm-landmark],[data-wm-book],[data-wm-read],[data-wm-tools-open]');
 if(entry){event.preventDefault();event.stopImmediatePropagation();focusCompletionStory();}
},true);
toolsDialog.addEventListener('close',()=>!story.isOpen&&toolsFocus?.isConnected&&toolsFocus.focus({preventScroll:true}));
const status=()=>{const s=store.get();return routeStatus(s.completed,s.positions,routeMetadata.get());};
const currentBook=()=>books.get(status().nextBookId)||null;
function recoverMapExploration(){
 if(!camera)return;
 if(camera.getState().canReturn)camera.returnFromOverview();
 if(camera.getState().overview){const l=landmarkFor(currentBook()?.id||'four-truths');selected=l.id;camera.focus({x:l.x,y:l.y});render();}
}
function mapInsets(){
 const bottom=$('.game-dock').getBoundingClientRect().height;
 const panel=$('.story-dialogue'),top=activeStoryScene?.doubtState&&panel&&!panel.hidden?Math.max(0,panel.getBoundingClientRect().bottom+8):0;
 return {top:Math.min(top,Math.max(0,innerHeight-bottom-100)),left:0,right:0,bottom};
}
const landmarkFor=id=>LANDMARKS.find(l=>l.id===PRIMARY_BOOK_LANDMARK[id]);
const revealed=(l,s)=>l.bookId!=='four-fruits-ten-fetters'||s.finalChapterRevealed;
const name=(l,s)=>revealed(l,s)?T.names[l.id]:T.unknown;
const access=(l,s)=>getGameBookAccess(l.bookId,s.completedBookIds,store.get().positions);
function sourceLines(){
 const chosen=LANDMARKS.find(l=>l.id===selected);
 const paths=EDGES.map(e=>{
  const p=sourceGroupAnchor(e.fromGroup)||conceptAnchor(e.from),q=sourceGroupAnchor(e.toGroup)||conceptAnchor(e.to);
  const direct=chosen&&(e.from===chosen.conceptId||e.to===chosen.conceptId);
  const coast=e.kind==='return'||e.id==='overview-branch-road-overview-eightfold-overview';
  const d=coast?GEOGRAPHIC_ROAD:'M'+p.x+' '+p.y+'L'+q.x+' '+q.y;
  return '<path class="wm-relation '+(direct?'is-direct ':'')+((links==='none'||(links==='direct'&&!direct))?'is-hidden':'')+'" data-source-edge="'+e.id+'" data-from="'+e.from+'" data-to="'+e.to+'" d="'+d+'"/>';
 }).join('');
 const extra=MAP_CONNECTIONS.map(c=>'<path class="wm-display-connector '+((links==='all'||(links==='direct'&&c.landmarkIds.includes(chosen?.id)))?'':'is-hidden')+'" data-display-route="'+c.id+'" data-is-source-relation="false" d="'+c.d+'"/>').join('');
 return paths+extra;
}
function mountWorld(){
 const marks=LANDMARKS.map(l=>'<button class="wm-landmark '+(l.type==='scroll'?'is-scroll':'')+'" data-wm-landmark="'+l.id+'" data-landmark="'+l.id+'" data-book="'+(l.bookId||'')+'" data-concept="'+l.conceptId+'" style="--x:'+l.x+'px;--y:'+l.y+'px"><span class="wm-pin" aria-hidden="true"></span><span class="wm-label"></span><span class="wm-status-chip"></span></button>').join('');
 $('#wm-host').innerHTML='<div class="wm-viewport" tabindex="0" aria-label="'+T.cameraLabel+'"><div class="wm-world" data-world-size="1600x900"><img class="wm-background" src="'+asset('assets/worldmap-master-concept.png')+'" width="1600" height="900" alt="'+T.worldAlt+'">'+renderCityRegions({label:T.cityRegions,names:T.cityNames})+'<svg class="wm-geography" viewBox="0 0 1600 900" aria-hidden="true"></svg><div class="wm-fog-layer"></div><svg class="wm-lines" viewBox="0 0 1600 900" aria-hidden="true"></svg>'+marks+'<img class="wm-traveler" src="'+new URL('../visual-v2/assets/kitten-rowboat-concept.png',import.meta.url).href+'" alt="'+T.travelerAlt+'"></div><div class="wm-load-state" role="status">'+T.loadingMap+'</div></div>';
 doubtStage=initializeDoubtStage({world:$('.wm-world'),anchor:{x:1248,y:566}});
 const image=$('.wm-background'),loading=$('.wm-load-state');
 const loaded=()=>{loading.hidden=true;};
 image.addEventListener('load',loaded);
 image.addEventListener('error',()=>{loading.hidden=false;loading.innerHTML='<span>'+T.mapLoadFailed+'</span><button data-wm-retry>'+T.retry+'</button>';});
 if(image.complete&&image.naturalWidth)loaded();
}
function render(){
 const s=status(),book=books.get(s.nextBookId),saved=store.get();
 $('#wm-title').textContent=T.title;$('#wm-eyebrow').textContent=T.eyebrow;$('#wm-description').textContent=T.description;
 $('#wm-count').textContent=T.collection(s.count);shell.setProgress(s.count,14);
 const next=$('[data-wm-next]'),at=book?getGameBookAccess(book.id,s.completedBookIds,saved.positions):null;
 next.textContent=book?(at.status==='reading'?T.resumeBook(book.title,at.resumePosition+1,book.totalSteps):T.startBook(book.title)):T.viewEnding;
 next.dataset.nextBook=book?.id||'';
 $('[data-wm-lines]').textContent=links==='none'?T.linesOn:T.linesOff;
 $('[data-wm-lines]').setAttribute('aria-pressed',String(links!=='none'));
 $('[data-wm-labels]').textContent=T.labels;$('[data-wm-labels]').setAttribute('aria-pressed',String(labels));
 $('[data-wm-locate]').textContent=T.currentLevel;
 $('[data-wm-tools-open]').textContent=T.moreTools;$('#wm-tools-title').textContent=T.mapToolsTitle;
 $('#wm-host').querySelectorAll('[data-wm-landmark]').forEach(el=>{
  const l=LANDMARKS.find(l=>l.id===el.dataset.landmark),a=access(l,s),primary=PRIMARY_BOOK_LANDMARK[l.bookId]===l.id;
  const state=!l.bookId?'harbor':a.status;
  const flag=a.canStart&&primary?(a.status==='reading'?T.readingAt(a.resumePosition+1,a.totalSteps):T.newLevel):a.canReview?T.readDone:'';
  el.classList.toggle('is-earned',a.canReview);el.classList.toggle('is-locked',Boolean(l.bookId&&!a.canRead));
  el.classList.toggle('is-next',a.canStart&&primary);el.classList.toggle('is-selected',l.id===selected);
  el.dataset.levelState=state;el.dataset.unlocked=String(!l.bookId||a.canRead);el.dataset.completed=String(a.canReview);
  el.setAttribute('aria-label',name(l,s)+(flag?'，'+flag:''));el.querySelector('.wm-label').textContent=name(l,s);
  el.querySelector('.wm-status-chip').textContent=flag;
 });
 $('.wm-world').classList.toggle('wm-labels-hidden',!labels);
 const place=landmarkFor(s.nextBookId||'four-truths'),traveler=$('.wm-traveler');traveler.style.left=(place.x-110)+'px';traveler.style.top=(place.y+53)+'px';
 $('.wm-fog-layer').innerHTML=LANDMARKS.filter(l=>l.bookId&&!l.alwaysClear&&!access(l,s).canRead).map(l=>'<div class="wm-fog" data-fog-for="'+l.id+'" style="left:'+l.x+'px;top:'+l.y+'px" aria-hidden="true"></div>').join('');
 $('.wm-lines').innerHTML=sourceLines();
 $('.wm-geography').innerHTML=(s.world.pathActive?'<path class="wm-road-active" d="'+GEOGRAPHIC_ROAD+'"/>':'')+(s.world.irrigationActive?'<path class="wm-irrigation" d="M912 630Q958 582 912 515"/>':'');
 const routeKey=JSON.stringify(s.books.map(b=>[b.id,b.completed,b.canRead,b.inProgress,b.mainlineTitle]));
 if($('#wm-route-strip').dataset.signature!==routeKey){$('#wm-route-strip').dataset.signature=routeKey;$('#wm-route-strip').innerHTML='<details class="wm-route-details"><summary>'+T.routeList+'</summary><ol class="wm-route-list">'+s.books.map(b=>'<li><button data-wm-book="'+b.id+'" data-level-state="'+getGameBookAccess(b.id,s.completedBookIds,saved.positions).status+'" aria-current="'+(b.id===s.nextBookId)+'">'+String(b.order).padStart(2,'0')+' · '+escape(b.mainlineTitle)+(b.completed?' ✓':'')+'</button></li>').join('')+'</ol></details>';}
 $('[data-wm-completion-replay]').hidden=!s.completedBookIds.includes('four-truths');
 syncDoubtStage();
 const notice=$('#wm-storage-notice');notice.hidden=true;notice.textContent='';
}
function open(title,html){
 lastFocus=document.activeElement;
 content.innerHTML='<h2 id="wm-dialog-title">'+escape(title)+'</h2>'+html;
 if(!dialog.open)dialog.showModal();
}
function lockPanel(){
 open(T.lockedTitle,'<p>'+T.lockedCopy+'</p><button class="primary" data-wm-current>'+T.goCurrent+'</button>');
}
function inspect(l){
 selected=l.id;render();const s=status(),a=access(l,s);
 if(!l.bookId){open(T.names.harbor,'<p>'+T.harborCopy+'</p><div class="wm-dialog-actions"><button class="primary" data-wm-current>'+T.goCurrent+'</button><a href="'+GAME_URLS.city+'">'+T.enterCity+'</a></div>');return;}
 if(!a.canRead){lockPanel();return;}
 const b=books.get(l.bookId),members=MEMBERS.filter(m=>m.sourceParentId===l.conceptId),node=nodes.get(l.conceptId);
 const memberMarkup=members.length?'<ul>'+members.map(m=>'<li>'+escape((m.key==='root'||m.key==='power'?T.familyNames[node.family]:'')+T.members[m.key])+'</li>').join('')+'</ul>':'';
 open(name(l,s),'<p class="wm-book-caption">'+escape(b.title)+'</p>'+memberMarkup+'<div class="wm-dialog-actions"><button class="primary" data-wm-read="'+b.id+'">'+(a.canReview?T.reviewBook:a.status==='reading'?T.continue:T.startReading)+'</button><a href="'+new URL(b.guide,catalogURL).href+'">'+T.guide+'</a></div><p class="wm-source-note">'+T.routeNote+'</p>');
}
function aggregatesEntryStory(){
 const id='five-aggregates',s=store.get(),a=getGameBookAccess(id,s.completed,s.positions);
 // Narrative only: existing bookmarks/reviews resume directly, never unlock.
 if(!a.canStart||Object.hasOwn(s.positions,id)||storyStore.hasSeen('toward-aggregates-lake'))return false;
 const l=landmarkFor(id);selected=l.id;render();dialog.close();camera?.focus({x:l.x,y:l.y});
 return story.show('toward-aggregates-lake');
}
function openReader(id,{bypassDoubt=false,bypassAggregatesIntro=false}={}){
 if(completionStoryOpen()){focusCompletionStory();return;}
 const s=store.get(),b=books.get(id),a=getGameBookAccess(id,s.completed,s.positions);
 if(!b||!a.canRead){lockPanel();return;}
 if(id==='four-truths'&&a.canStart&&!bypassDoubt&&!Object.hasOwn(s.positions,id)&&!storyStore.hasSeen('doubt-at-ruins')){dialog.close();story.show('doubt-at-ruins');return;}
 if(id==='five-aggregates'&&!bypassAggregatesIntro&&aggregatesEntryStory())return;
 if(a.canStart)routeMetadata.markOpened(id);
 const u=new URL(b.reader,catalogURL);
 u.searchParams.set('collection','1');u.searchParams.set('collectionReturn','game');
 u.searchParams.set('collectionStory','dark-heart-1');
 if(a.canReview)u.searchParams.set('collectionReview','1');
 const at=a.canReview&&a.resumePosition===b.totalSteps-1?0:(a.resumePosition??0);
 u.searchParams.set('collectionPage',String(at));
 location.assign(u.href);
}
function locateNext(){
 const book=currentBook();if(!book){showEnding();return;}
 const l=landmarkFor(book.id);selected=l.id;render();camera?.focus({x:l.x,y:l.y});
}
function showEnding(){
 const s=status();if(!s.endingAvailable)return;
 open(T.ending,'<p>'+T.endingCopy+'</p><p>'+T.endingDirection+'</p><blockquote>'+escape(s.ending.quote)+'</blockquote><a href="https://buddhaspace.org/agama/sub/262.html" target="_blank" rel="noopener">'+s.ending.quoteSource+'</a><div class="wm-dialog-actions"><a href="'+GAME_URLS.shelf+'" class="primary">'+T.reviewShelf+'</a></div>');
}
function completedFeedback(id){
 const s=status(),b=books.get(id);if(!b||!s.completedBookIds.includes(id))return;
 if(id==='four-truths'&&resumeLegacyTransition())return;
 const primary=landmarkFor(id);
 dialog.close();
 // A presentation-only URL keeps an acknowledged outro's final notification
 // resumable. It never grants reading access or writes a completed book.
 const url=new URL(GAME_URLS.map);url.searchParams.set('completed',id);history.replaceState(null,'',url);
 story.showCompletion({bookId:id,title:T.completeTitle(b.title),html:'<p class="wm-world-reward">'+escape(T.mapReward(name(primary,s)))+'</p>'+compactCompletionFeedback(id,s)+'<p>'+T.collection(s.count)+'</p>',nextLabel:s.nextBookId?T.nextStation:T.viewEnding,cityLabel:T.seeCity});
}
function clearCompletionNotice(){history.replaceState(null,'',GAME_URLS.map);}
function activateMap(){
 $('#game-content').hidden=false;shell.setVisible(true);
 if(active){camera?.refresh();recoverMapExploration();return;}
 active=true;mountWorld();render();
 const book=currentBook(),l=book?landmarkFor(book.id):landmarkFor('four-truths');
 camera=createMapCamera($('.wm-viewport'),$('.wm-world'),{width:WORLD.width,height:WORLD.height,initialCenter:{x:l.x,y:l.y},getInsets:mapInsets});
 // Old full-image snapshots must not strand the player now that overview and
 // its return controls are gone. The camera persists the restored exploration.
 recoverMapExploration();
 $('.wm-viewport').addEventListener('keydown',event=>{
  if(event.target.closest('input,textarea,select,[contenteditable="true"]'))return;
  const keys=['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-','_','0','Home'];
  if(!keys.includes(event.key))return;
  if(event.ctrlKey||event.metaKey||event.altKey){event.stopImmediatePropagation();return;}
  if(event.key==='0'||event.key==='Home'){event.preventDefault();event.stopImmediatePropagation();}
 },true);
 const dockObserver=new ResizeObserver(()=>camera.refresh());dockObserver.observe($('.game-dock'));
 $('.wm-viewport').addEventListener('focusin',event=>{
  const target=event.target.closest('.wm-landmark');
  if(!target||!target.matches(':focus-visible'))return; // Pointer taps must not move their target before click.
  const clipped=()=>{const r=target.getBoundingClientRect(),view=$('.wm-viewport').getBoundingClientRect(),dock=$('.game-dock').getBoundingClientRect();return r.left<view.left+3||r.right>view.right-3||r.top<view.top+3||r.bottom>dock.top-3;};
  if(!clipped())return;
  const point=LANDMARKS.find(item=>item.id===target.dataset.wmLandmark);
  if(!point)return;
  const scale=camera.getState().scale;camera.focus(point,scale);
  if(clipped())camera.focus(point,Math.max(scale,1.5));
 });
 if(params.get('focus')==='current')locateNext();
 const receipt=consumeFirstCompletionReceipt();
 if(completed){const id=completed;completed=null;history.replaceState(null,'',GAME_URLS.map);if(id!=='four-truths'||!firstCompletionStory(receipt))completedFeedback(id);}
 else if(!firstCompletionStory(receipt))resumeLegacyTransition();
 const saved=store.get();
 if(!story.isOpen&&!params.has('completed')&&!saved.completed.length&&!Object.keys(saved.positions).length&&!storyStore.hasSeen('arrival-at-wheel')){
  story.show('arrival-at-wheel');
 }
 let taught=false;try{taught=sessionStorage.getItem('sutrazen.play.map-tip.v1')==='1';}catch{}
 if(!taught){
  const tip=document.createElement('p');tip.className='wm-once-tip';tip.textContent=T.cameraTip;$('#wm-host').append(tip);
  try{sessionStorage.setItem('sutrazen.play.map-tip.v1','1');}catch{}
  setTimeout(()=>tip.remove(),6500);
 }
}
dialog.addEventListener('close',()=>!story.isOpen&&lastFocus?.isConnected&&lastFocus.focus({preventScroll:true}));
document.addEventListener('click',e=>{
 const b=e.target.closest('button');if(!b)return;
 if(b.hasAttribute('data-wm-close'))dialog.close();
 if(b.hasAttribute('data-wm-tools-open')){toolsFocus=b;toolsDialog.showModal();}
 if(b.hasAttribute('data-wm-tools-close'))toolsDialog.close();
 if(b.hasAttribute('data-wm-next')){const book=currentBook();if(book)openReader(book.id);else showEnding();}
 if(b.hasAttribute('data-wm-current')){dialog.close();locateNext();}
 if(b.hasAttribute('data-wm-locate'))locateNext();
 if(b.hasAttribute('data-wm-zoom-in'))camera?.zoomBy(1.3);
 if(b.hasAttribute('data-wm-zoom-out'))camera?.zoomBy(1/1.3);
 if(b.hasAttribute('data-wm-lines')){links=links==='none'?'all':'none';render();}
 if(b.hasAttribute('data-wm-labels')){labels=!labels;render();}
 if(b.hasAttribute('data-wm-story-replay')){toolsDialog.close();dialog.close();story.show('arrival-at-wheel',{replay:true});}
 if(b.hasAttribute('data-wm-completion-replay')&&store.get().completed.includes('four-truths')){toolsDialog.close();dialog.close();const l=landmarkFor('four-truths');camera?.focus({x:l.x,y:l.y});story.show('first-book-insight',{replay:true});}
 if(b.dataset.wmLandmark){const l=LANDMARKS.find(l=>l.id===b.dataset.wmLandmark);if(l)inspect(l);}
 if(b.dataset.wmBook){toolsDialog.close();const l=landmarkFor(b.dataset.wmBook);if(l)inspect(l);}
 if(b.dataset.wmRead)openReader(b.dataset.wmRead);
 if(b.hasAttribute('data-wm-retry')){const img=$('.wm-background');img.src=asset('assets/worldmap-master-concept.png')+'?retry='+Date.now();}
});
for(const event of ['sutrazen:collection-progress','sutrazen:route-metadata'])window.addEventListener(event,()=>{if(active)render();});
window.addEventListener('sutrazen:journey-state',()=>{story.close();dialog.close();toolsDialog.close();completed=null;if(new URL(location.href).searchParams.has('completed'))clearCompletionNotice();if(active){render();locateNext();const saved=store.get();if(!saved.completed.length&&!Object.keys(saved.positions).length)story.show('arrival-at-wheel');}});
window.addEventListener('pageshow',()=>{if(active){render();camera?.refresh();recoverMapExploration();}});
const alias=location.hash==='#city'?'city':location.hash==='#shelf'?'shelf':null;
if(alias)location.replace(GAME_URLS[alias]);
else initializeTitleScreen({shell,enabled:gameEntry,onEnterMap:activateMap});
window.SutraZenWorldmap={getState:()=>({mode:'route',links,selected,status:status(),camera:camera?.getState()||null}),locateNext,activateMap};
