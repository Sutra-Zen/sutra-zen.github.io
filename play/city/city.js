import {initializeGameShell,GAME_URLS} from '../game-shell.js?v=train-reset-1';
import {store} from '../collection/store.js';
import {routeMetadata} from '../route/metadata.js';
import {routeStatus,routeBooks} from '../route/selectors.js';
import {canStartGameBook,canReviewGameBook} from '../route/eligibility.js';
import {CANONICAL_EXPLANATIONS,MODULE_EXPLANATIONS} from './explanations.js?v=simple-ui-1';
import {cityStore,CITY_LAYOUT_EVENT} from './modules/store.js?v=auto-city-1';
import {MODULE_UI as U} from './modules/text.js?v=auto-city-1';
import {initializeModularCity} from './modules/scene.js?v=simple-ui-1';
import {initializeCityThoughts} from './thoughts.js?v=simple-ui-1';
import {T} from './text.js?v=auto-city-1';

const main=document.querySelector('#city-main'),dialog=document.querySelector('#city-dialog'),content=document.querySelector('#city-dialog-content');
const catalogURL=new URL('../collection/catalog.js',import.meta.url),books=new Map(routeBooks.map(book=>[book.id,book]));
const spotModules={eye:'six_gates',ear:'six_gates',nose:'six_gates',tongue:'six_gates',body:'six_gates',mind:'six_gates',guardian:'mindfulness_guard',messengers:'calm_insight_messengers',message:'calm_insight_messengers',road:'noble_path',dock:'truth_dock'};
const escape=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
let lastTrigger=null,scene=null,thoughts=null;
const address=new URL(location.href);if(address.searchParams.has('review')){address.searchParams.delete('review');history.replaceState(null,'',address);}
document.body.classList.add('modular-city','auto-city');
const actualRoute=()=>{const saved=store.get();return routeStatus(saved.completed,saved.positions,routeMetadata.get());};
const layout=()=>({...cityStore.get(store.get().completed),labels:true});
const moduleFor=id=>layout().modules.find(module=>module.id===id);
main.innerHTML=`<h1 class="city-visually-hidden">${T.scene}</h1><section id="city-scene-host" aria-label="${T.scene}"></section><p id="city-storage-notice" role="status" hidden></p>`;
const shell=initializeGameShell({active:'city'});
const continuation=document.createElement('div');continuation.id='city-primary-action';continuation.className='city-read-action';
shell.mountMapControls({primary:continuation});
function updateChrome(){
 const route=actualRoute(),city=layout(),book=books.get(route.nextBookId),at=book?store.get().positions[book.id]:null;
 const resume=book&&Number.isInteger(at)&&at>=0&&at<book.totalSteps;
 const markup=resume?`<button id="city-continue" class="primary" data-city-primary-book="${book.id}">${T.continue(escape(book.title),at)}</button>`:`<a id="city-back-map" class="primary" href="${GAME_URLS.map}">${book?T.currentBook(escape(book.title)):T.allComplete}</a>`;
 if(continuation.innerHTML!==markup)continuation.innerHTML=markup;
 const issue=document.querySelector('#city-storage-notice');issue.hidden=!city.issue&&!store.issue;
 issue.textContent=city.issue==='corrupt'?U.corruptStorage:city.persistence==='session'?U.sessionIssue:city.issue?U.storageIssue:T.issue;
 shell.setProgress(store.get().completed.length,14);
}
function render(){updateChrome();scene?.render();}
function open(html){
 if(!dialog.open)lastTrigger=document.activeElement;
 thoughts?.close();content.innerHTML=html;
 if(!dialog.open)dialog.showModal();dialog.scrollTop=0;
 dialog.querySelector('[data-city-close]').focus({preventScroll:true});
}
function showExplanation(explanation){
 if(!explanation)return;
 const tag=explanation.kind==='canonical'?'blockquote':'p';
 open(`<h2 id="city-dialog-title">${escape(explanation.title)}</h2><${tag} class="city-explanation" data-city-explanation="${explanation.kind}">${escape(explanation.text)}</${tag}>`);
}
function inspectSpot(id){
 const city=layout(),visible=['plaza','lord'].includes(id)?city.baseVisible:id==='town'?city.placedIds.includes('city_body'):city.placedIds.includes(spotModules[id]);
 if(!visible)return;
 showExplanation(CANONICAL_EXPLANATIONS[id]||(id==='dock'?MODULE_EXPLANATIONS.truth_dock:null));
}
function inspectModule(id){
 const module=moduleFor(id);if(!module?.placed||module.revealed===false)return;
 showExplanation(MODULE_EXPLANATIONS[id]);
}
function read(id){
 const saved=store.get(),book=books.get(id);if(!book)return;
 const review=canReviewGameBook(id,saved.completed);if(!review&&!canStartGameBook(id,saved.completed)){location.assign(GAME_URLS.map);return;}
 const url=new URL(book.reader,catalogURL),at=saved.positions[id];url.searchParams.set('collection','1');url.searchParams.set('collectionReturn','game');url.searchParams.set('collectionStory','train-reset-1');
 if(review){url.searchParams.set('collectionReview','1');url.searchParams.set('collectionPage',String(Number.isInteger(at)&&at>=0&&at<book.totalSteps-1?at:0));}
 else if(Number.isInteger(at)&&at>=0&&at<book.totalSteps)url.searchParams.set('collectionPage',String(at));location.assign(url.href);
}
thoughts=initializeCityThoughts({host:main,getState:layout,onSeen:id=>cityStore.markThoughtSeen(id),onClose:()=>document.querySelector('.mod-city__viewport')?.focus({preventScroll:true})});
scene=initializeModularCity({host:document.querySelector('#city-scene-host'),getState:layout,
 getInsets:()=>({top:8,left:8,right:8,bottom:(document.querySelector('.game-dock')?.getBoundingClientRect().height||0)+8}),
 onThought:id=>{if(dialog.open)dialog.close();thoughts.show(id);},
 onInspect:id=>moduleFor(id)?inspectModule(id):inspectSpot(id),onChange:()=>updateChrome()});
const oldCamera=scene.getState().camera;
if(oldCamera.canReturn)scene.returnFromOverview();else if(oldCamera.overview)scene.focus('four-elements-base');
main.addEventListener('keydown',event=>{
 if(!event.target.closest('.mod-city__viewport')||!['0','Home'].includes(event.key))return;
 if(event.ctrlKey||event.metaKey||event.altKey||event.shiftKey){event.stopPropagation();return;}
 event.preventDefault();event.stopImmediatePropagation();
},true);
dialog.addEventListener('click',event=>{
 const button=event.target.closest('button');if(!button)return;
 if(button.hasAttribute('data-city-close'))dialog.close();
});
continuation.addEventListener('click',event=>{if(event.target.closest('#city-continue')){const book=books.get(actualRoute().nextBookId);if(book)read(book.id);}});
dialog.addEventListener('close',()=>{if(!thoughts.isOpen&&lastTrigger?.isConnected)lastTrigger.focus({preventScroll:true});});
for(const event of ['sutrazen:collection-progress',CITY_LAYOUT_EVENT])window.addEventListener(event,render);
window.addEventListener('sutrazen:journey-state',()=>{thoughts.close();dialog.close();scene.focus('four-elements-base');render();});
window.addEventListener('pageshow',()=>{render();scene.refresh();});render();
const dockObserver=new ResizeObserver(()=>scene.refresh());dockObserver.observe(document.querySelector('.game-dock'));
window.SutraZenModularCity={getState:()=>layout(),getCamera:()=>scene.getState(),closeThought:()=>thoughts.close()};
