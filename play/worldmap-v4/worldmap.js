import {store} from '../collection/store.js';
import {routeStatus,routeBooks,routeOrder} from '../route/selectors.js';
import {routeMetadata} from '../route/metadata.js';
import {renderGameNavigation} from '../navigation.js';
import {compactCompletionFeedback} from './completion-feedback.js';
import {WORLD,COLUMNS,LANDMARKS,SECONDARY,MEMBERS,NODES,EDGES,GEOGRAPHIC_ROAD,MAP_CONNECTIONS,conceptAnchor,sourceGroupAnchor,PRIMARY_BOOK_LANDMARK} from './data.js';
import {T} from './text.js';

const $=s=>document.querySelector(s),bookById=new Map(routeBooks.map(b=>[b.id,b])),nodeById=new Map(NODES.map(n=>[n.id,n]));
const query=new URLSearchParams(location.search),catalogURL=new URL('../collection/catalog.js',import.meta.url);
let mode=query.get('mode')==='free'?'free':'route',overview=true,links='none',labels=true,selected=null;
const dialog=$('#wm-dialog'),dialogContent=$('#wm-dialog-content');
$('.proposal-header nav').outerHTML=renderGameNavigation({active:'map'});
const escape=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function status(){const s=store.get();return routeStatus(s.completed,s.positions,routeMetadata.get());}
function primaryReader(s){
 const saved=store.get(),active=bookById.get(saved.activeBook),at=active?saved.positions[active.id]:null;
 // Resume the actual current reading, including a partial re-read. Recommendation
 // order stays separate and still points at the first unfinished route book.
 if(active&&Number.isInteger(at)&&at>=0&&(!s.completedBookIds.includes(active.id)||at<active.totalSteps-1))return active;
 return bookById.get(s.nextBookId)||null;
}
function unlocked(l,s){
 if(l.alwaysClear||!l.bookId||mode==='free')return true;
 const b=s.books.find(b=>b.id===l.bookId);
 return b.completed||b.inProgress||routeOrder.indexOf(l.bookId)<=routeOrder.indexOf(s.nextBookId);
}
function name(l,s){return l.bookId==='four-fruits-ten-fetters'&&mode==='route'&&!s.finalChapterRevealed?T.unknown:T.names[l.id];}
function sourceLines(){
 const chosen=LANDMARKS.find(l=>l.id===selected);
 const paths=EDGES.map(e=>{
  const p=sourceGroupAnchor(e.fromGroup)||conceptAnchor(e.from),q=sourceGroupAnchor(e.toGroup)||conceptAnchor(e.to);
  if(!p||!q)throw Error(`Missing source anchor ${e.id}`);
  const direct=chosen&&(e.from===chosen.conceptId||e.to===chosen.conceptId);
  const hidden=links==='none'||(links==='direct'&&!direct);
  const coast=e.kind==='return'||e.id==='overview-branch-road-overview-eightfold-overview';
  const d=coast?GEOGRAPHIC_ROAD:`M${p.x} ${p.y}L${q.x} ${q.y}`;
  return `<path class="wm-relation ${direct?'is-direct':''} ${hidden?'is-hidden':''}" data-source-edge="${e.id}" data-from="${e.from}" data-to="${e.to}" ${coast?'data-display-routing="coastal-road"':''} d="${d}"/>`;
 }).join('');
 const guide=links==='all'?`<g class="wm-alignment" data-layout-guides><path data-row="awakening" d="M168 108H1392"/><path data-row="faculties" d="M168 243H1392"/>${Object.entries(COLUMNS).map(([family,x])=>`<path data-column="${family}" d="M${x} ${family==='faith'?243:108}V${family==='faith'?540:810}"/>`).join('')}</g>`:'';
 const access=MAP_CONNECTIONS.map(c=>{
  const shown=links==='all'||(links==='direct'&&c.landmarkIds.includes(chosen?.id));
  return `<path class="wm-display-connector ${shown?'':'is-hidden'}" data-display-route="${c.id}" data-route-kind="${c.kind}" data-is-source-relation="false" d="${c.d}"/>`;
 }).join('');
 return `<svg class="wm-lines" viewBox="0 0 1600 900" preserveAspectRatio="none" aria-hidden="true">${guide}${paths}${access}</svg>`;
}
function landscape(s){
 const chosen=LANDMARKS.find(l=>l.id===selected),nextLandmark=PRIMARY_BOOK_LANDMARK[s.nextBookId];
 const fog=LANDMARKS.filter(l=>!unlocked(l,s)).map(l=>`<div class="wm-fog ${l.type==='island'?'is-island-fog':''} ${l.type==='scroll'?'is-scroll-fog':''} ${l.id==='fruition_valley'?'is-final-fog':''}" data-fog-for="${l.id}" style="left:${l.x/16}%;top:${l.y/9}%" aria-hidden="true"></div>`).join('');
 const marks=LANDMARKS.map(l=>{
  const earned=s.completedBookIds.includes(l.bookId),available=unlocked(l,s),same=chosen?.bookId&&chosen.bookId===l.bookId;
  return `<button class="wm-landmark ${l.type==='scroll'?'is-scroll':''} ${l.id===selected?'is-selected':''} ${same?'is-same-book':''} ${earned?'is-earned':''} ${nextLandmark===l.id?'is-next':''}" data-wm-landmark="${l.id}" data-landmark="${l.id}" data-book="${l.bookId||''}" data-concept="${l.conceptId}" data-unlocked="${available}" data-completed="${earned}" ${l.row?`data-row="${l.row}"`:''} ${l.family?`data-column="${l.family}"`:''} style="--x:${l.x/16}%;--y:${l.y/9}%" aria-label="${escape(name(l,s))}，${earned?T.earned:available?T.available:T.unfinished}"><span class="wm-label">${escape(name(l,s))}</span></button>`;
 }).join('');
 return `<div class="wm-viewport ${overview?'is-overview':''}" tabindex="0" aria-label="完整山海世界，可放大並左右上下平移"><div class="wm-world ${labels?'':'wm-labels-hidden'}" data-world-size="1600x900" data-world-version="2026-11-22-map-v4" data-mode="${mode}"><img class="wm-background" src="assets/worldmap-master-concept.png" width="1672" height="941" alt="無字山海世界：七覺支北排、五根五力近岸排，中段為木造燈亭、湖灣、鏡影林、花田、竹林、船塢、庭園及輪庭，下方公路半島與四組橋由藍色水道分隔"><svg class="wm-geography" viewBox="0 0 1600 900" preserveAspectRatio="none" aria-hidden="true">${s.world.pathActive?`<path class="wm-road-active" data-path-active d="${GEOGRAPHIC_ROAD}"/>`:''}${s.world.irrigationActive?'<path class="wm-irrigation" data-irrigation-active d="M912 630Q958 582 912 515"/>':''}</svg>${fog}${sourceLines()}${marks}</div></div>`;
}
function render(){
 const s=status(),next=primaryReader(s);
 $('#wm-title').textContent=T.title;$('#wm-eyebrow').textContent=T.eyebrow;$('#wm-description').textContent=T.description;
 $('#wm-count').textContent=T.collection(s.count);
 $('[data-wm-next]').textContent=!next?T.allComplete:s.count||s.books.some(b=>b.inProgress)?T.continue:T.start;
 $('[data-wm-next]').setAttribute('aria-label',next?`${T.continue}《${next.title}》`:T.allComplete);
 $('[data-wm-next]').dataset.nextBook=next?.id||'';
 $('[data-wm-lines]').textContent=links==='all'?T.linesOff:links==='direct'?'查看全部互通連線':T.linesOn;
 $('[data-wm-lines]').setAttribute('aria-pressed',String(links!=='none'));
 $('[data-wm-zoom]').textContent=overview?T.zoomIn:T.zoomOut;
 $('[data-wm-labels]').setAttribute('aria-pressed',String(labels));
 document.querySelectorAll('[data-wm-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.wmMode===mode)));
 $('#wm-fog-note').textContent=T.fogNote;$('#wm-route-note').textContent=T.routeNote;
 $('#wm-details-title').textContent=T.details;$('#wm-native-note').textContent=T.nativeNote;$('#wm-figure-note').textContent=T.figureNote;
 $('#wm-detail-buttons').innerHTML=Object.entries(T.detailNames).map(([id,title])=>`<button data-wm-detail="${id}">${title}</button>`).join('');
 const was=$('.wm-viewport'),scroll=was?{left:was.scrollLeft,top:was.scrollTop}:null;
 $('#wm-host').innerHTML=landscape(s);
 if(scroll&&!overview){const sc=$('.wm-viewport');sc.scrollTo(scroll);}
 $('#wm-route-strip').innerHTML=`<details class="wm-route-details"><summary>${mode==='free'?T.free:'十四本閱讀路線'} · ${T.collection(s.count)}</summary><ol class="wm-route-list">${s.books.map(b=>`<li><button data-wm-book="${b.id}" aria-current="${b.id===s.nextBookId}"><span class="wm-order">${String(b.order).padStart(2,'0')}</span>${escape(mode==='free'?b.title:b.mainlineTitle)}${b.completed?' ✓':''}</button></li>`).join('')}</ol></details>${s.endingAvailable?`<button class="primary" data-wm-ending>${T.ending}</button>`:''}`;
 const notice=$('#wm-storage-notice');notice.hidden=!(store.issue||routeMetadata.issue);notice.className='wm-storage-notice';notice.textContent=store.issue?'此瀏覽器暫時無法保存閱讀紀錄，仍可繼續閱讀。':routeMetadata.issue?'角色與書名的顯示紀錄暫時無法保存，已讀紀錄維持原狀。':'';
}
function open(title,html,detail=false){
 dialog.classList.remove('wm-completion-dialog');
 dialog.classList.toggle('wm-detail-dialog',detail);dialogContent.innerHTML=`<h2 id="wm-dialog-title">${escape(title)}</h2>${html}`;
 if(!dialog.open)dialog.showModal();
}
function openReader(id){
 const b=bookById.get(id);if(!b)return;
 routeMetadata.markOpened(id);const s=store.get(),u=new URL(b.reader,catalogURL);
 u.searchParams.set('collection','1');u.searchParams.set('collectionReturn','worldmap-v4');
 const at=s.positions[id];
 if(Number.isInteger(at)&&(!s.completed.includes(id)||at<b.totalSteps-1))u.searchParams.set('collectionPage',at);
 else if(s.completed.includes(id))u.searchParams.set('collectionPage','0');
 location.assign(u.href);
}
function inspect(l){
 selected=l.id;links=links==='none'?'direct':links;render();const s=status();
 if(!l.bookId){
  open(T.names.harbor,`<p>從港口接續閱讀，或回城池看看已讀故事帶來的變化。</p><div class="wm-dialog-actions"><button class="primary" data-wm-next>${T.continue}</button><a data-wm-city href="../city/">${T.city}</a><a href="../visual-v2/shelf.html">${T.shelf}</a></div>`);return;
 }
 const b=s.books.find(b=>b.id===l.bookId),concealed=mode==='route'&&!b.revealed;
 const neighbours=new Set(EDGES.filter(e=>e.from===l.conceptId||e.to===l.conceptId).flatMap(e=>[e.from,e.to]));neighbours.delete(l.conceptId);
 const members=MEMBERS.filter(m=>m.sourceParentId===l.conceptId);
 const node=nodeById.get(l.conceptId),same=LANDMARKS.filter(p=>p.bookId===l.bookId&&p.id!==l.id);
 const caption=b.completed?T.earned:b.inProgress?T.reading:unlocked(l,s)?T.available:T.unfinished;
 open(concealed?T.unknown:name(l,s),`<span class="status-label">${caption}</span><p>${concealed?'前十三本完成後，主線會揭曉這段旅程。原網站與自由選讀保持開放。':`這處地景屬於《${escape(b.title)}》。${l.id==='recollection_lighthouse'?'木造燈塔與六盞步道燈，同屬四不壞淨與六念這一本。':''}`}</p>${members.length?`<ul>${members.map(m=>`<li data-concept-member="${m.id}" data-source-parent="${m.sourceParentId}">${escape((m.key==='root'||m.key==='power'?T.familyNames[node.family]:'')+T.members[m.key])}</li>`).join('')}</ul>`:''}<div class="wm-dialog-actions"><button class="primary" data-wm-read="${b.id}">${concealed?'自由選讀':b.inProgress?T.continue:b.completed?T.restart:T.read}</button>${!concealed?`<a data-wm-guide href="${new URL(b.guide,catalogURL).href}">${T.guide}</a>`:''}</div>${same.length&&!concealed?`<h3>${T.sameBook}</h3><div class="wm-related">${same.map(p=>`<button data-wm-select="${p.id}">${escape(name(p,s))}</button>`).join('')}</div>`:''}${neighbours.size&&!concealed?`<h3>${T.related}</h3><div class="wm-related">${[...neighbours].map(id=>{const p=LANDMARKS.find(l=>l.conceptId===id);return p?`<button data-wm-select="${p.id}">${escape(name(p,s))}</button>`:'';}).join('')}</div>`:''}<p class="wm-source-note">${T.routeNote}</p>${node?'<p class="wm-source-note">對讀關係沿用原心智圖；地景位置與閱讀次序是本次教學設計。</p>':''}`);
}
function locateNext(){
 const next=primaryReader(status())?.id;if(!next)return;const l=LANDMARKS.find(l=>l.id===PRIMARY_BOOK_LANDMARK[next]);
 overview=false;selected=l.id;render();requestAnimationFrame(()=>{const sc=$('.wm-viewport'),world=$('.wm-world');sc.scrollTo({left:l.x/WORLD.width*world.clientWidth-sc.clientWidth/2,top:l.y/WORLD.height*world.clientHeight-sc.clientHeight/2});});
}
function showEnding(){
 const s=status();if(!s.endingAvailable)return;
 open(T.ending,`<p>${T.endingCopy}</p><p>${T.endingDirection}</p><blockquote>${escape(s.ending.quote)}</blockquote><p><a href="https://buddhaspace.org/agama/sub/262.html" target="_blank" rel="noopener">${s.ending.quoteSource}</a></p><div class="wm-dialog-actions"><a class="primary" href="../../index.html#books">回原網站書架</a><a href="../city/">${T.city}</a></div>`);
}
function completedFeedback(id){
 const s=status(),b=bookById.get(id);if(!b||!s.completedBookIds.includes(id))return;
 const firstThree=id==='six-senses'&&['four-truths','five-aggregates','six-senses'].every(id=>s.completedBookIds.includes(id));
 const next=bookById.get(s.nextBookId);
 open(T.completeTitle(b.title),`${firstThree?`<p class="wm-success">${T.firstComplete}</p>`:''}${compactCompletionFeedback(id,s)}<p class="wm-completion-count">${T.collection(s.count)}</p><div class="wm-dialog-actions wm-completion-actions">${next?`<button class="primary" data-wm-read="${next.id}">${escape(T.nextTitle(next.title))}</button>`:`<button class="primary" data-wm-ending>${T.ending}</button>`}<a data-wm-city href="../city/">${T.seeCity}</a></div>`);
 dialog.classList.add('wm-completion-dialog');
}
document.addEventListener('click',e=>{
 const b=e.target.closest('button');if(!b)return;
 if(b.hasAttribute('data-wm-close'))dialog.close();
 if(b.hasAttribute('data-wm-lines')){links=links==='all'?'none':'all';render();}
 if(b.hasAttribute('data-wm-labels')){labels=!labels;render();}
 if(b.hasAttribute('data-wm-zoom')){overview=!overview;render();}
 if(b.hasAttribute('data-wm-locate'))locateNext();
 if(b.dataset.wmMode){mode=b.dataset.wmMode;render();}
 if(b.dataset.wmLandmark||b.dataset.wmSelect){const l=LANDMARKS.find(l=>l.id===(b.dataset.wmLandmark||b.dataset.wmSelect));if(l)inspect(l);}
 if(b.dataset.wmBook){const l=LANDMARKS.find(l=>l.id===PRIMARY_BOOK_LANDMARK[b.dataset.wmBook]);if(l)inspect(l);}
 if(b.hasAttribute('data-wm-next')){const next=primaryReader(status())?.id;if(next)openReader(next);else showEnding();}
 if(b.dataset.wmRead)openReader(b.dataset.wmRead);
 if(b.dataset.wmDetail){const id=b.dataset.wmDetail;if(Object.hasOwn(T.detailNames,id))open(T.detailNames[id],`<p>${T.detailNote}</p><img class="wm-detail-art" src="assets/detail-${id}.png" alt="${escape(T.detailNames[id])}">`,true);}
 if(b.hasAttribute('data-wm-ending'))showEnding();
});
window.addEventListener('sutrazen:collection-progress',render);
window.addEventListener('sutrazen:route-metadata',render);
window.addEventListener('pageshow',render);
render();
const completed=query.get('completed');
if(completed){history.replaceState(null,'',location.pathname);completedFeedback(completed);}
window.SutraZenWorldmap={getState:()=>({mode,links,overview,selected,status:status()}),locateNext};
