import { CATALOG } from '../collection/catalog.js';
import { store } from '../collection/store.js';
import { T } from '../collection/shelf-text.js';
const moduleURL=new URL('../collection/catalog.js',import.meta.url);
const books=document.querySelector('#collection-books'),count=document.querySelector('#collection-count'),bar=document.querySelector('#collection-progress'),feedback=document.querySelector('#collection-feedback'),notice=document.querySelector('#collection-notice'),dialog=document.querySelector('#collection-dialog'),dialogContent=document.querySelector('#collection-dialog-content');
const urlFor=value=>new URL(value,moduleURL).href;
const wheel='<svg viewBox="0 0 80 80" aria-hidden="true"><circle cx="40" cy="40" r="28"/><circle cx="40" cy="40" r="10"/>'+Array.from({length:8},(_,i)=>`<path d="M40 12V30" transform="rotate(${i*45} 40 40)"/>`).join('')+'</svg>';
let completedId=new URLSearchParams(location.search).get('completed');
if(completedId)history.replaceState(null,'',location.pathname);
function showNotice(text){notice.textContent=text;notice.hidden=!text;}
function render(){
 const s=store.get(),n=s.completed.length;count.textContent=T.collectedCount(n);bar.value=n;bar.textContent=T.countFraction(n);
 books.innerHTML=CATALOG.map(b=>{const done=s.completed.includes(b.id),at=s.positions[b.id],resuming=Number.isInteger(at)&&(!done||at<b.totalSteps-1);return `<article class="collection-book ${done?'is-earned':'is-unearned'}" data-book-card="${b.id}" data-earned="${done}"><button class="collection-book-button" data-collection-read="${b.id}" aria-label="${T.readAria({resuming,done,title:b.title})}"><span class="collection-book-art">${done?`<img class="earned-cover" src="${urlFor(b.cover)}" alt="${T.coverAlt(b.title)}">`:`<span class="unearned-icon">${b.unreadIcon?`<img src="${urlFor(b.unreadIcon)}" alt="">`:wheel}</span><img class="achievement-lock" src="assets/shelf-lock.svg" alt="${T.unearnedAlt}">`}<span class="collection-book-number" aria-hidden="true">${String(b.number).padStart(2,'0')} <span>／14</span></span><span class="collection-book-title">${b.title}</span></span><span class="collection-book-status">${T.bookStatus({resuming,done,at})}</span></button></article>`;}).join('');
 const justRead=CATALOG.find(b=>b.id===completedId&&s.completed.includes(b.id));
 if(n===14){feedback.hidden=false;feedback.dataset.complete='all';feedback.innerHTML=`<p class="eyebrow">${T.allEyebrow}</p><h2>${T.allHeading}</h2><p>${T.allCopy}</p><a class="primary" href="./">${T.backToMap}</a>`;}
 else if(justRead){feedback.hidden=false;feedback.dataset.complete=justRead.id;feedback.innerHTML=`<p class="eyebrow">${T.earnedEyebrow}</p><h2>${T.earnedHeading(justRead.title)}</h2><p>${T.earnedCopy(n)}</p><button class="primary" data-collection-next>${T.collectNext}</button>`;}
 else{feedback.hidden=true;feedback.replaceChildren();}
 if(store.issue)showNotice(store.issue==='corrupt'?T.corruptNotice:T.unavailableNotice);
}
function read(id){const b=CATALOG.find(b=>b.id===id);if(!b)return;const s=store.get(),u=new URL(b.reader,moduleURL);u.searchParams.set('collection','1');if(Number.isInteger(s.positions[id])&&(!s.completed.includes(id)||s.positions[id]<b.totalSteps-1))u.searchParams.set('collectionPage',s.positions[id]);else if(s.completed.includes(id))u.searchParams.set('collectionPage','0');location.assign(u);}
function confirm(title,text,action,label){dialogContent.innerHTML=`<h2 id="collection-dialog-title">${title}</h2><p>${text}</p><div class="dialog-actions"><button id="collection-cancel">${T.cancel}</button><button id="collection-confirm" class="primary">${label}</button></div>`;dialog.showModal();document.querySelector('#collection-cancel').onclick=()=>dialog.close();document.querySelector('#collection-confirm').onclick=()=>{dialog.close();action();};}
document.addEventListener('click',e=>{
 const el=e.target.closest('button');if(!el)return;
 if(el.dataset.collectionRead)read(el.dataset.collectionRead);
 if(el.hasAttribute('data-collection-next')){const next=CATALOG.find(b=>!store.get().completed.includes(b.id));if(next)read(next.id);}
 if(el.hasAttribute('data-collection-reset'))confirm(T.resetTitle,T.resetCopy,()=>{completedId=null;store.reset();showNotice('');render();},T.resetConfirm);
 if(el.hasAttribute('data-collection-backup')){const url=URL.createObjectURL(new Blob([store.exportBackup()],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='sutrazen-book-collection-v1.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
});
document.querySelector('#collection-import').addEventListener('change',async e=>{const f=e.target.files[0];if(!f)return;if(f.size>100000){showNotice(T.oversizedBackup);return;}let text;try{text=await f.text();}catch{showNotice(T.unreadableBackup);return;}e.target.value='';confirm(T.restoreTitle,T.restoreCopy,()=>{completedId=null;if(store.restoreBackup(text)){render();showNotice(store.issue?T.restoreUnavailable:T.restoreSuccess);}else showNotice(T.restoreInvalid);},T.restoreConfirm);});
window.addEventListener('sutrazen:collection-progress',()=>render());window.addEventListener('pageshow',()=>render());
render();
