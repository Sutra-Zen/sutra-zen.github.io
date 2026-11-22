import {initializeGameShell,GAME_URLS} from '../game-shell.js';
import {store} from '../collection/store.js';
import {routeMetadata} from '../route/metadata.js';
import {routeStatus,routeBooks} from '../route/selectors.js';
import {canStartGameBook,canReviewGameBook} from '../route/eligibility.js';
import {CITY_COPY,TACTICS_SPOTS,renderTacticsCity,citySpotStatus,renderCityRolePreview} from '../visual-v2/city-tactics.js';
import {T} from './text.js';
const cityText=CITY_COPY['zh-Hant'],main=document.querySelector('#city-main'),dialog=document.querySelector('#city-dialog'),content=document.querySelector('#city-dialog-content');
const catalogURL=new URL('../collection/catalog.js',import.meta.url),books=new Map(routeBooks.map(b=>[b.id,b]));
const related={eye:'six-senses',ear:'six-senses',nose:'six-senses',tongue:'six-senses',body:'six-senses',mind:'six-senses',town:'five-aggregates',plaza:'five-aggregates',lord:'five-aggregates',guardian:'mindfulness',messengers:'anapana',message:'six-senses',road:'eightfold-path',dock:'four-truths'};
let labels=true,explore=false,lastTrigger=null;
// Old author-preview parameters never alter a player's city or completed state.
const address=new URL(location.href);if(address.searchParams.has('review')){address.searchParams.delete('review');history.replaceState(null,'',address);}
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function actualRoute(){const s=store.get();return routeStatus(s.completed,s.positions,routeMetadata.get());}
function primaryBook(route){return books.get(route.nextBookId)||null;}
function fitScene(){
 const host=document.querySelector('#city-scene-host'),board=host?.querySelector('.city-tactics-board');if(!host||!board)return;
 const availableWidth=host.clientWidth,availableHeight=host.clientHeight,ratio=1671/941;
 const width=explore?Math.max(availableWidth,availableHeight*ratio,1000):Math.min(availableWidth,availableHeight*ratio);
 board.style.width=`${Math.max(1,width)}px`;
}
function render(){
 const old=main.querySelector('.tactics-scroll'),scroll=old?{left:old.scrollLeft,top:old.scrollTop}:null;
 const route=actualRoute(),primary=primaryBook(route),saved=store.get(),at=primary?saved.positions[primary.id]:null;
 const canResume=primary&&Number.isInteger(at)&&at>0&&at<primary.totalSteps;
 const nextReward=primary?route.city.rewards.find(r=>r.bookId===primary.id):null;
 main.innerHTML=`<h1 class="city-visually-hidden">${T.scene}</h1><div class="city-tools"><button id="city-label-toggle" aria-pressed="${labels}">${T.labels}</button><button id="city-overview-toggle" aria-pressed="${!explore}">${explore?T.overview:T.enlarge}</button><button id="city-meaning-index">${T.meanings}</button></div>
 <section id="city-scene-host" class="${explore?'city-explore':'city-overview'}" aria-label="${T.scene}">${renderTacticsCity({showSpots:labels,showLabels:labels,labelLayout:matchMedia('(max-width:1000px), (max-height:500px)').matches?'compact':'wide'})}</section>
 <div class="city-primary"><div class="city-next-copy"><span id="city-continuation-info">${primary?escape(T.nextHint(primary.title)):T.completedHint}</span>${nextReward?`<span class="city-build-hint">${escape(T.nextCity(nextReward.title))}</span>`:''}${store.issue?`<span id="city-storage-notice" role="status">${T.issue}</span>`:''}</div>${canResume?`<button id="city-continue" class="primary" data-city-primary-book="${primary.id}" data-city-resume-at="${at}">${T.continue(escape(primary.title),at)}</button>`:`<a id="city-back-map" class="primary" href="${GAME_URLS.map}">${primary?T.backMap:T.allComplete}</a>`}</div>`;
 fitScene();if(explore&&scroll)main.querySelector('.tactics-scroll').scrollTo(scroll);
}
function read(id,{review=false}={}){
 const b=books.get(id),saved=store.get();if(!b)return;
 const allowed=review?canReviewGameBook(id,saved.completed):canStartGameBook(id,saved.completed);
 if(!allowed){location.assign(GAME_URLS.map);return;}
 const u=new URL(b.reader,catalogURL),at=saved.positions[id];u.searchParams.set('collection','1');u.searchParams.set('collectionReturn','game');
 if(review){u.searchParams.set('collectionReview','1');u.searchParams.set('collectionPage',String(Number.isInteger(at)&&at>=0&&at<b.totalSteps-1?at:0));}
 else if(Number.isInteger(at)&&at>=0&&at<b.totalSteps)u.searchParams.set('collectionPage',String(at));
 location.assign(u.href);
}
function inspect(id){
 const spot=TACTICS_SPOTS.find(s=>s.id===id);if(!spot)return;
 const state=citySpotStatus(id),book=books.get(related[id]),reviewable=canReviewGameBook(book.id,store.get().completed);
 content.innerHTML=`<p class="eyebrow">SN 35.245</p><h2 id="city-dialog-title">${spot.title}</h2><p class="status-label">${state.statusText}</p>${renderCityRolePreview(id)}<p>${spot.copy}</p>${state.missingTitles.length?`<p class="city-missing">${cityText.missingPrefix}：${state.missingTitles.map(escape).join('、')}。${cityText.waiting}</p>`:''}<div class="city-dialog-actions">${reviewable?`<button class="primary" data-city-reread="${book.id}">${T.completedReview(escape(book.title))}</button>`:`<p class="city-future-copy">${T.futureReview}</p><a class="primary" data-city-current href="${GAME_URLS.map}">${T.backMap}</a>`}<a class="city-source-link" href="${new URL('../sources.html',import.meta.url).href}">${T.sources}</a></div><p class="source-note">${T.sourceNote}</p>`;
 if(!dialog.open)dialog.showModal();
}
function index(){content.innerHTML=`<h2 id="city-dialog-title">${T.meanings}</h2><div class="city-meaning-list">${TACTICS_SPOTS.map(s=>`<button data-city-meaning="${s.id}">${s.title}</button>`).join('')}</div><a href="${new URL('../sources.html',import.meta.url).href}">${T.sources}</a>`;dialog.showModal();}
document.addEventListener('click',event=>{
 const b=event.target.closest('button');if(!b)return;
 if(b.id==='city-continue'){const p=primaryBook(actualRoute());if(p)read(p.id);}
 if(b.id==='city-label-toggle'){labels=!labels;render();}
 if(b.id==='city-overview-toggle'){explore=!explore;render();}
 if(b.id==='city-meaning-index'){lastTrigger=b;index();}
 if(b.dataset.spot||b.dataset.cityMeaning){if(!dialog.open)lastTrigger=b;inspect(b.dataset.spot||b.dataset.cityMeaning);}
 if(b.dataset.cityReread)read(b.dataset.cityReread,{review:true});
 if(b.hasAttribute('data-city-close'))dialog.close();
});
dialog.addEventListener('close',()=>{if(lastTrigger?.isConnected)lastTrigger.focus();});
window.addEventListener('sutrazen:collection-progress',render);window.addEventListener('sutrazen:route-metadata',render);
window.addEventListener('resize',fitScene);new ResizeObserver(fitScene).observe(main);
matchMedia('(max-width:1000px), (max-height:500px)').addEventListener('change',render);
render();initializeGameShell({active:'city'});
