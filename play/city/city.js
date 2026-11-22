import {renderGameNavigation,NAV_ITEMS} from '../navigation.js';
import {store} from '../collection/store.js';
import {routeMetadata} from '../route/metadata.js';
import {routeStatus,routeBooks} from '../route/selectors.js';
import {CITY_COPY,TACTICS_SPOTS,renderTacticsCity,getCitySnapshot,cityReviewControls,citySpotStatus,renderCityRolePreview} from '../visual-v2/city-tactics.js';
const T=CITY_COPY['zh-Hant'],main=document.querySelector('#city-main'),dialog=document.querySelector('#city-dialog'),content=document.querySelector('#city-dialog-content');
const catalogURL=new URL('../collection/catalog.js',import.meta.url),books=new Map(routeBooks.map(b=>[b.id,b]));
const mapURL=NAV_ITEMS.find(n=>n.id==='map').href;
const related={eye:'six-senses',ear:'six-senses',nose:'six-senses',tongue:'six-senses',body:'six-senses',mind:'six-senses',town:'five-aggregates',plaza:'five-aggregates',lord:'five-aggregates',guardian:'mindfulness',messengers:'anapana',message:'six-senses',road:'eightfold-path',dock:'four-truths'};
const params=new URLSearchParams(location.search),requestedReview=params.get('review');
let labels=true,explore=false,reviewStage=requestedReview==='all'?'all':/^[0-3]$/.test(requestedReview||'')?Number(requestedReview):null;
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
document.querySelector('header').insertAdjacentHTML('beforeend',renderGameNavigation({active:'city'}));
function actualRoute(){const saved=store.get();return routeStatus(saved.completed,saved.positions,routeMetadata.get());}
function primaryBook(route){
 const saved=store.get(),active=books.get(saved.activeBook),at=active?saved.positions[active.id]:null;
 if(active&&Number.isInteger(at)&&at>=0&&at<active.totalSteps&&(!saved.completed.includes(active.id)||at<active.totalSteps-1))return {...active,resumeAt:at};
 const next=books.get(route.nextBookId);return next?{...next,resumeAt:null}:{...books.get('four-truths'),resumeAt:null,revisit:true};
}
function render(){
 const old=main.querySelector('.tactics-scroll'),scroll=old?{left:old.scrollLeft,top:old.scrollTop}:null;
 const route=actualRoute(),primary=primaryBook(route),compact=matchMedia('(max-width:600px)').matches;
 const primaryText=primary.resumeAt!==null?T.continue:primary.revisit?T.revisit:primary.id==='four-truths'&&route.count===0?T.start:`${T.next}《${primary.title}》`;
 main.innerHTML=`<section class="city-heading"><div><p class="eyebrow">SutraZen · ${T.trial}</p><h1>${T.pageTitle}</h1><p>${T.pageIntro}</p></div><div class="city-primary"><span id="city-progress">${T.progress(route.count,route.total)}</span><button id="city-continue" class="primary" data-city-primary-book="${primary.id}" data-city-resume-at="${primary.resumeAt===null?'':primary.resumeAt}">${primaryText}</button><span id="city-continuation-info">${primary.resumeAt!==null?`${T.continuePrefix}《${primary.title}》・${primary.resumeAt+1} ${T.pageSuffix}`:`《${primary.title}》`}</span></div></section>
 ${store.issue?`<p id="city-storage-notice" class="city-notice" role="status">${T.unavailableStorage}</p>`:''}
 <div class="city-tools"><a id="city-back-map" href="${mapURL}">← ${T.backMap}</a><button id="city-label-toggle" aria-pressed="${labels}">${T.labelsToggle}</button><button id="city-overview-toggle" aria-pressed="${!explore}">${explore?T.overview:T.zoom}</button></div>
 <section id="city-scene-host" class="${explore?'city-explore':'city-overview'}" aria-label="${T.pageTitle}">${renderTacticsCity({reviewStage,showSpots:labels,showLabels:labels,labelLayout:compact?'compact':'wide'})}</section>
 <p class="city-reading-note">${T.readingOnly}</p>
 <details id="city-source-index"><summary>${T.sourceIndex}</summary><div class="city-meaning-list">${TACTICS_SPOTS.map(s=>`<button data-city-meaning="${s.id}">${s.title}</button>`).join('')}</div><a href="${new URL('../sources.html',import.meta.url).href}">${T.scripture} ↗</a></details>
 <details id="city-review-options" ${reviewStage!==null?'open':''}><summary>${T.reviewOptions}</summary><p>${T.noWrites}</p>${cityReviewControls(reviewStage)}</details>`;
 if(explore&&scroll)main.querySelector('.tactics-scroll').scrollTo(scroll);
}
function read(id,{restart=false}={}){
 const b=books.get(id);if(!b)return;
 routeMetadata.markOpened(id);const saved=store.get(),u=new URL(b.reader,catalogURL),at=saved.positions[id];
 u.searchParams.set('collection','1');u.searchParams.set('collectionReturn','worldmap-v4');
 if(restart)u.searchParams.set('collectionPage','0');
 else if(Number.isInteger(at)&&at>=0&&at<b.totalSteps&&(!saved.completed.includes(id)||at<b.totalSteps-1))u.searchParams.set('collectionPage',String(at));
 else if(saved.completed.includes(id))u.searchParams.set('collectionPage','0');
 location.assign(u.href);
}
function inspect(id){
 const spot=TACTICS_SPOTS.find(s=>s.id===id);if(!spot)return;
 const state=citySpotStatus(id,reviewStage),book=books.get(related[id]);
 content.innerHTML=`<p class="eyebrow">SN 35.245</p><h2 id="city-dialog-title">${spot.title}</h2><p class="status-label">${state.statusText}</p>${renderCityRolePreview(id,reviewStage)}<p>${spot.copy}</p>${state.missingTitles.length?`<p class="city-missing">${T.missingPrefix}：${state.missingTitles.map(escape).join('、')}。${T.waiting}</p>`:''}<div class="city-dialog-actions"><button class="primary" data-city-reread="${book.id}">${T.reread}《${book.title}》</button><a href="${new URL(book.guide,catalogURL).href}">${T.relatedBook}</a><a href="${new URL('../sources.html',import.meta.url).href}">${T.scripture}</a></div><p class="source-note">${T.sourceNote}</p>`;
 if(!dialog.open)dialog.showModal();
}
document.addEventListener('click',event=>{
 const b=event.target.closest('button');if(!b)return;
 if(b.id==='city-continue')read(primaryBook(actualRoute()).id);
 if(b.id==='city-label-toggle'){labels=!labels;render();}
 if(b.id==='city-overview-toggle'){explore=!explore;render();}
 if(b.dataset.spot||b.dataset.cityMeaning)inspect(b.dataset.spot||b.dataset.cityMeaning);
 if(b.dataset.cityReread)read(b.dataset.cityReread,{restart:true});
 if(b.hasAttribute('data-city-close'))dialog.close();
 if(b.hasAttribute('data-city-review')){reviewStage=b.dataset.cityReview==='real'?null:b.dataset.cityReview==='all'?'all':Number(b.dataset.cityReview);render();}
});
window.addEventListener('sutrazen:collection-progress',()=>{reviewStage=null;render();});
window.addEventListener('sutrazen:route-metadata',render);
let resizeTimer;window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(render,80);});
render();
