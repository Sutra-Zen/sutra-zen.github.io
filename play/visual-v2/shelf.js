import {initializeGameShell,GAME_URLS} from '../game-shell.js?v=dark-heart-1';
import {store} from '../collection/store.js';
import {routeStatus} from '../route/selectors.js';
import {canReviewGameBook} from '../route/eligibility.js';
import {T} from './shelf-copy.js';
const moduleURL=new URL('../collection/catalog.js',import.meta.url);
const books=document.querySelector('#collection-books'),count=document.querySelector('#collection-count'),bar=document.querySelector('#collection-progress'),empty=document.querySelector('#collection-empty'),notice=document.querySelector('#collection-notice');
const urlFor=value=>new URL(value,moduleURL).href;
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const address=new URL(location.href);if(address.searchParams.has('completed')){address.searchParams.delete('completed');history.replaceState(null,'',address);}
document.querySelector('.collection-heading h1').textContent=T.title;
document.querySelector('.collection-case').setAttribute('aria-label',T.caseLabel);
document.querySelector('#collection-all-read').textContent=T.allRead;
function render(){
 const saved=store.get(),route=routeStatus(saved.completed,saved.positions),n=route.count;count.textContent=T.count(n);bar.value=n;bar.textContent=T.fraction(n);
 empty.hidden=n>0;empty.innerHTML=n?'':`<h2>${T.emptyTitle}</h2><p>${T.emptyCopy}</p><a class="primary" href="${GAME_URLS.map}">${T.first}</a>`;
 books.innerHTML=route.books.map((b,index)=>{
  const done=canReviewGameBook(b.id,saved.completed),title=b.revealed?b.title:T.unknown;
  const art=`<span class="collection-book-art">${done?`<img class="earned-cover" src="${urlFor(b.cover)}" alt="${T.cover(escape(title))}">`:'<span class="unearned-icon" aria-hidden="true">?</span>'}<span class="collection-book-number" aria-hidden="true">${String(index+1).padStart(2,'0')} <span>／14</span></span><span class="collection-book-title">${escape(title)}</span></span><span class="collection-book-status">${done?T.reviewed:T.locked}</span>`;
  return `<article class="collection-book ${done?'is-earned':'is-unearned'}" data-book-card="${b.id}" data-earned="${done}">${done?`<button class="collection-book-button" data-collection-read="${b.id}" aria-label="${T.review(escape(title))}">${art}</button>`:`<div class="collection-book-placeholder" aria-label="${escape(title)}，${T.locked}">${art}</div>`}</article>`;
 }).join('');
 notice.textContent=store.issue?(store.issue==='corrupt'?T.corrupt:T.notice):'';notice.hidden=!store.issue;
 document.querySelector('#collection-all-read').hidden=n!==14;
}
function read(id){
 const saved=store.get();if(!canReviewGameBook(id,saved.completed)){location.assign(GAME_URLS.map);return;}
 const b=routeStatus(saved.completed,saved.positions).books.find(b=>b.id===id);if(!b)return;
 const u=new URL(b.reader,moduleURL),at=saved.positions[id];u.searchParams.set('collection','1');u.searchParams.set('collectionReview','1');u.searchParams.set('collectionReturn','game');u.searchParams.set('collectionStory','dark-heart-1');u.searchParams.set('collectionPage',String(Number.isInteger(at)&&at>=0&&at<b.totalSteps-1?at:0));location.assign(u.href);
}
document.addEventListener('click',e=>{const button=e.target.closest('[data-collection-read]');if(button)read(button.dataset.collectionRead);});
window.addEventListener('sutrazen:collection-progress',render);window.addEventListener('pageshow',render);
render();initializeGameShell({active:'shelf'});
