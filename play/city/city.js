import {initializeGameShell,GAME_URLS} from '../game-shell.js?v=outro-order-1';
import {store} from '../collection/store.js';
import {routeMetadata} from '../route/metadata.js';
import {routeStatus,routeBooks} from '../route/selectors.js';
import {canStartGameBook,canReviewGameBook} from '../route/eligibility.js';
import {CITY_COPY,TACTICS_SPOTS} from '../visual-v2/city-tactics.js?v=20261122-city-rewards';
import {CITY_REWARD_COPY,REWARD_TYPE_LABELS,renderRewardSourcePreview} from '../visual-v2/city-rewards.js?v=20261122-city-rewards';
import {cityStore,CITY_LAYOUT_EVENT} from './modules/store.js';
import {MODULE_UI as U} from './modules/text.js';
import {initializeModularCity,renderSprite} from './modules/scene.js';
import {initializeCityThoughts} from './thoughts.js';
import {T} from './text.js?v=outro-order-1';

const main=document.querySelector('#city-main'),dialog=document.querySelector('#city-dialog'),content=document.querySelector('#city-dialog-content');
const catalogURL=new URL('../collection/catalog.js',import.meta.url),books=new Map(routeBooks.map(book=>[book.id,book]));
const related={eye:'six-senses',ear:'six-senses',nose:'six-senses',tongue:'six-senses',body:'six-senses',mind:'six-senses',town:'five-aggregates',plaza:'five-aggregates',lord:'five-aggregates',guardian:'mindfulness',messengers:'anapana',message:'anapana',road:'eightfold-path',dock:'four-truths'};
const spotModules={eye:'six_gates',ear:'six_gates',nose:'six_gates',tongue:'six_gates',body:'six_gates',mind:'six_gates',guardian:'mindfulness_guard',messengers:'calm_insight_messengers',message:'calm_insight_messengers',road:'noble_path',dock:'truth_dock'};
const escape=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
let labels=true,explore=true,lastTrigger=null,scene=null,thoughts=null,restoreDialogFocus=true;
const address=new URL(location.href);if(address.searchParams.has('review')){address.searchParams.delete('review');history.replaceState(null,'',address);}
document.body.classList.add('modular-city');
const actualRoute=()=>{const saved=store.get();return routeStatus(saved.completed,saved.positions,routeMetadata.get());};
const layout=()=>({...cityStore.get(store.get().completed),labels});
const moduleFor=id=>layout().modules.find(module=>module.id===id);
main.innerHTML=`<h1 class="city-visually-hidden">${T.scene}</h1><div class="city-tools"><button id="city-label-toggle" aria-pressed="true">${T.labels}</button><button id="city-overview-toggle" aria-pressed="false">${T.overview}</button><button id="city-meaning-index">${T.meanings}</button><button id="city-thought-open">${T.thoughts}</button></div><section id="city-scene-host" aria-label="${T.scene}"></section><div class="city-primary"><div class="city-next-copy"><span id="city-continuation-info"></span><span id="city-placement-count"></span><span id="city-storage-notice" role="status" hidden></span></div><span id="city-primary-action"></span></div>`;
const shell=initializeGameShell({active:'city'});
function updateChrome(){
 const route=actualRoute(),city=layout(),book=books.get(route.nextBookId),at=book?store.get().positions[book.id]:null;
 const resume=book&&Number.isInteger(at)&&at>0&&at<book.totalSteps;
 document.querySelector('#city-continuation-info').textContent=book?T.nextHint(book.title):T.completedHint;
 document.querySelector('#city-placement-count').textContent=U.placedCount(city.placedIds.length);
 document.querySelector('#city-primary-action').innerHTML=resume?`<button id="city-continue" class="primary" data-city-primary-book="${book.id}">${T.continue(escape(book.title),at)}</button>`:`<a id="city-back-map" class="primary" href="${GAME_URLS.map}">${book?T.backMap:T.allComplete}</a>`;
 const issue=document.querySelector('#city-storage-notice');issue.hidden=!city.issue&&!store.issue;issue.textContent=city.issue==='corrupt'?U.corruptStorage:city.persistence==='session'?U.sessionIssue:city.issue?U.storageIssue:T.issue;
 document.querySelector('#city-label-toggle').setAttribute('aria-pressed',String(labels));
 document.querySelector('#city-overview-toggle').textContent=explore?T.overview:T.enlarge;
 document.querySelector('#city-overview-toggle').setAttribute('aria-pressed',String(!explore));
 document.querySelector('#city-thought-open').disabled=!city.baseVisible;
 shell.setProgress(store.get().completed.length,14);
}
function render(){updateChrome();scene?.render();}
function open(html){if(!dialog.open)lastTrigger=document.activeElement;thoughts?.close();content.innerHTML=html;if(!dialog.open)dialog.showModal();dialog.scrollTop=0;}
function sourceLinks(book,sourceURL){
 const reviewed=canReviewGameBook(book.id,store.get().completed);
 return `<div class="city-dialog-actions">${reviewed?`<button class="primary" data-city-reread="${book.id}">${T.completedReview(escape(book.title))}</button>`:`<p class="city-future-copy">${T.futureReview}</p><a class="primary" href="${GAME_URLS.map}">${T.backMap}</a>`}${sourceURL?`<a class="city-source-link" href="${sourceURL}">${T.sources}</a>`:''}</div>`;
}
function inspectSpot(id){
 const spot=TACTICS_SPOTS.find(item=>item.id===id);if(!spot)return;
 const city=layout(),visible=['plaza','lord'].includes(id)?city.baseVisible:id==='town'?city.placedIds.includes('city_body'):city.placedIds.includes(spotModules[id]);
 const book=books.get(related[id]),sourceURL=new URL('../sources.html',import.meta.url).href;
 open(`<p class="eyebrow">${T.canonicalSource}</p><h2 id="city-dialog-title">${escape(spot.title)}</h2><p class="status-label">${visible?T.sceneVisible:T.sceneWaiting}</p><p>${spot.copy}</p>${sourceLinks(book,sourceURL)}<p class="source-note">${T.sourceNote}</p>`);
}
function inspectModule(id){
 const module=moduleFor(id);if(!module)return;
 const book=books.get(module.bookId),reviewable=canReviewGameBook(book.id,store.get().completed);
 const status=module.placed?U.placed:module.unlocked?module.canPlace?U.available:U.needsPlacement:U.locked;
 const sourceURL=module.type==='canonical'?new URL('../sources.html',import.meta.url).href:reviewable?new URL(book.guide+'#sources',catalogURL).href:null;
 const art=module.revealed===false?'':renderSprite(module.slots[0]?.assetKey,{className:'city-module-preview',label:module.title});
 const missing=module.unlocked&&!module.canPlace&&!module.placed&&module.missingModuleIds.length?`<p>${U.missingModules(module.missingModuleIds.map(key=>moduleFor(key)?.title||U.unknownModule))}</p>`:'';
 open(`<p class="eyebrow">${REWARD_TYPE_LABELS[module.type]}</p><h2 id="city-dialog-title">${escape(module.title)}</h2><p class="status-label">${status}</p>${art}<p>${module.description}</p>${missing}${module.revealed===false?'':`<p>${CITY_REWARD_COPY[id]||''}</p>`}${module.canPlace?`<button class="primary" data-city-select-module="${module.id}">${U.place}</button>`:''}${module.unlocked&&reviewable?renderRewardSourcePreview(id):''}${module.revealed===false?`<a class="primary" href="${GAME_URLS.map}">${T.backMap}</a>`:sourceLinks(book,sourceURL)}<p class="source-note">${module.type==='canonical'?T.sourceNote:T.extendedNote}</p>`);
}
function meanings(){
 const city=layout();
 open(`<h2 id="city-dialog-title">${T.meanings}</h2><h3>${T.canonicalHeading}</h3><div class="city-meaning-list">${TACTICS_SPOTS.filter(spot=>spot.id!=='dock').map(spot=>`<button data-city-meaning="${spot.id}">${escape(spot.title)}</button>`).join('')}</div><p class="source-note">${T.sourceNote}</p><h3>${T.rewardHeading}</h3><div class="city-reward-index">${city.modules.map(module=>`<button data-city-module-detail="${module.id}"><span>${escape(module.title)}</span><small>${module.placed?U.placed:module.unlocked?U.unlocked:U.locked}</small></button>`).join('')}</div><a href="${new URL('../sources.html',import.meta.url).href}">${T.sources}</a>`);
}
function read(id){
 const saved=store.get(),book=books.get(id);if(!book)return;
 const review=canReviewGameBook(id,saved.completed);if(!review&&!canStartGameBook(id,saved.completed)){location.assign(GAME_URLS.map);return;}
 const url=new URL(book.reader,catalogURL),at=saved.positions[id];url.searchParams.set('collection','1');url.searchParams.set('collectionReturn','game');url.searchParams.set('collectionStory','outro-order-1');
 if(review){url.searchParams.set('collectionReview','1');url.searchParams.set('collectionPage',String(Number.isInteger(at)&&at>=0&&at<book.totalSteps-1?at:0));}
 else if(Number.isInteger(at)&&at>=0&&at<book.totalSteps)url.searchParams.set('collectionPage',String(at));location.assign(url.href);
}
thoughts=initializeCityThoughts({host:main,getState:layout,onSeen:id=>cityStore.markThoughtSeen(id),onClose:()=>document.querySelector('#city-thought-open').focus({preventScroll:true})});
function afterPlaced(result){
 if(!result?.ok)return;render();const placed=result.placedNow||[];
 requestAnimationFrame(()=>{
  const state=layout();if(!state.baseVisible)return;
  if(placed.includes('mindfulness_guard')&&!state.thoughtSeenIds.includes('mindfulness-guardian-introduction'))thoughts.show('guardian');
  else if(placed.includes('calm_insight_messengers')&&!state.thoughtSeenIds.includes('calm-insight-messengers-arrival'))thoughts.show('messengers');
  else if(placed.includes('six_gates')&&!state.placedIds.includes('mindfulness_guard')&&!state.thoughtSeenIds.includes('six-gates-unwatched'))thoughts.show('mara');
 });
}
scene=initializeModularCity({host:document.querySelector('#city-scene-host'),getState:layout,onPlace:id=>{
 const result=id==='all'?cityStore.placeAll(store.get().completed):cityStore.place(id,store.get().completed);afterPlaced(result);return result;
},onThought:id=>thoughts.show(id),onInspect:id=>moduleFor(id)?inspectModule(id):inspectSpot(id),onChange:change=>{if(change.type==='camera'){const next=!change.camera.overview;if(explore!==next){explore=next;updateChrome();}}}});
main.addEventListener('click',event=>{
 const button=event.target.closest('button');if(!button)return;
 if(button.id==='city-label-toggle'){labels=!labels;render();}
 if(button.id==='city-overview-toggle'){if(explore)scene.fit();else scene.focus('four-elements-base');explore=!scene.getState().camera.overview;updateChrome();}
 if(button.id==='city-meaning-index'){lastTrigger=button;meanings();}
 if(button.id==='city-thought-open')thoughts.show(layout().placedIds.includes('six_gates')?'mara':'lord');
});
dialog.addEventListener('click',event=>{
 const button=event.target.closest('button');if(!button)return;
 if(button.hasAttribute('data-city-close'))dialog.close();
 if(button.dataset.cityMeaning)inspectSpot(button.dataset.cityMeaning);
 if(button.dataset.cityModuleDetail)inspectModule(button.dataset.cityModuleDetail);
 if(button.dataset.citySelectModule){restoreDialogFocus=false;dialog.close();scene.selectModule(button.dataset.citySelectModule);}
 if(button.dataset.cityReread)read(button.dataset.cityReread);
});
main.addEventListener('click',event=>{if(event.target.closest('#city-continue')){const book=books.get(actualRoute().nextBookId);if(book)read(book.id);}});
dialog.addEventListener('close',()=>{if(restoreDialogFocus&&!thoughts.isOpen&&lastTrigger?.isConnected)lastTrigger.focus({preventScroll:true});restoreDialogFocus=true;});
for(const event of ['sutrazen:collection-progress',CITY_LAYOUT_EVENT])window.addEventListener(event,render);
window.addEventListener('sutrazen:journey-state',()=>{thoughts.close();dialog.close();scene.selectModule(null);scene.focus('four-elements-base');render();});
window.addEventListener('pageshow',render);render();
requestAnimationFrame(()=>{const state=layout();if(state.baseVisible&&!state.thoughtSeenIds.includes('city-lord-introduction'))thoughts.show('lord');});
window.SutraZenModularCity={getState:()=>layout(),getCamera:()=>scene.getState(),closeThought:()=>thoughts.close()};
