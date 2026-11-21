import { NODES, EDGES, INSTANCES, GROUPS, READING_ROUTE, BOOK_WAYPOINTS } from './network-data.js';
import { ISLANDS } from './data.js';
export const NETWORK_SIZE={width:1800,height:1300};
const lookup=new Map(NODES.map(n=>[n.id,n]));
export const MOUNTAIN_IDS=new Set(GROUPS.flatMap(g=>g.members));
export const VISIBLE_INSTANCES=INSTANCES.filter(i=>i.nodeId!=='related-overview');
const isMountain=i=>MOUNTAIN_IDS.has(i.nodeId)&&(i.nodeId!=='eightfold-overview'||i.id.endsWith('four-truths-port'));

// Display spacing is independent of the exact source positions retained in data.js.
const DISPLAY = {
 'road-overview':[5,43], 'roots-powers-overview':[14,11], 'awakening-overview':[14,31], 'eightfold-overview':[14,51], 'related-overview':[14,81],
 'faith-root-power':[29,11], 'mindfulness-root-power':[44,11], 'effort-root-power':[59,11], 'concentration-root-power':[74,11], 'wisdom-root-power':[90,11],
 'mindfulness-awakening':[44,31], 'effort-awakening':[59,31], 'concentration-awakening-group':[74,31], 'discrimination-awakening':[90,31],
 'right-mindfulness':[44,51], 'eightfold-action-group':[59,51], 'right-concentration':[74,51], 'right-view-intention':[90,51],
 'four-purities':[29,78], 'six-recollections':[29,91], 'four-mindfulness':[44,78], 'four-inversions':[44,91], 'right-effort':[59,78], 'ten-wholesome':[59,91],
 'anapana':[68,74], 'iddhipada':[76,76.5], 'four-jhanas':[72,88], 'four-truths':[85,81], 'five-aggregates':[87,63], 'six-senses':[98,63], 'twelve-links':[98,76], 'four-fruits':[98,89]
};
export function point(instance){
 let [x,y]=DISPLAY[instance.nodeId];
 if(instance.id.endsWith('four-truths-port')){x=85;y=98;}
 return {x:6+.88*x,y:4+.88*y};
}
function coords(instance){const p=point(instance);return {x:p.x*18,y:p.y*13};}
const instances=new Map(INSTANCES.map(i=>[i.id,i]));
function nodeInstance(id){return INSTANCES.find(i=>i.nodeId===id);}
function groupAnchor(id,kind){const g=GROUPS.find(g=>g.id===id);if(!g)return null;const points=g.members.map(key=>coords(key==='eightfold-overview'?instances.get('eightfold-overview-four-truths-port'):nodeInstance(key)));return {x:points.reduce((s,p)=>s+p.x,0)/points.length,y:kind==='vertical'?Math.min(...points.map(p=>p.y))-35:points.reduce((s,p)=>s+p.y,0)/points.length};}
export function routeInstance(bookId){return bookId==='eightfold-path'?instances.get('eightfold-overview-four-truths-port'):nodeInstance(BOOK_WAYPOINTS[bookId]);}
export function connected(id){const node=lookup.get(id);if(!node)return new Set();const set=new Set([id]);if(node.family!=='overview')for(const n of NODES)if(n.family===node.family)set.add(n.id);for(const e of EDGES){if(e.from===id)set.add(e.to);if(e.to===id)set.add(e.from);}set.delete('related-overview');return set;}
export function networkMarkup({selected=null,route=true,allLinks=true}={}){
 const lit=connected(selected),routePoints=READING_ROUTE.map(id=>coords(routeInstance(id)));
 const routePath=routePoints.map((p,i)=>`${i?'L':'M'}${p.x} ${p.y}`).join(' ');
 const paths=EDGES.map(e=>{
 const a=e.kind==='return'?instances.get('eightfold-overview-four-truths-port'):instances.get(e.fromInstance)||nodeInstance(e.from),b=instances.get(e.toInstance)||nodeInstance(e.to);const p=groupAnchor(e.fromGroup,e.kind)||coords(a),q=groupAnchor(e.toGroup,e.kind)||coords(b);
 const active=lit.has(e.from)&&lit.has(e.to),cls=`network-edge edge-${e.kind} ${active?'is-highlighted':''} ${!allLinks&&!active?'is-hidden':''}`;
 let d=`M${p.x} ${p.y}L${q.x} ${q.y}`;
 if(e.kind==='overview-branch')d=`M${p.x} ${p.y}C${p.x+90} ${p.y} ${q.x-100} ${q.y} ${q.x} ${q.y}`;
 if(e.kind==='return')d=`M${p.x} ${p.y}C${p.x+70} ${p.y-15} 1640 1090 1590 1058C1300 1082 1100 1050 900 1065S420 1050 220 1040C110 1030 100 920 125 835S92 650 ${q.x} ${q.y}`;
 return `<path class="${cls}" data-edge="${e.id}" ${e.kind==='return'?'data-terrain-road="true"':''} data-from="${e.from}" data-to="${e.to}" data-from-group="${e.fromGroup||''}" data-to-group="${e.toGroup||''}" ${e.directed?'marker-end="url(#network-return-arrow)"':''} d="${d}">${e.port?`<title>四聖諦${e.port}的原圖對讀</title>`:''}</path>`;
 }).join('');
 const buttons=VISIBLE_INSTANCES.map((i,index)=>{
 const n=lookup.get(i.nodeId),p=point(i),mountain=isMountain(i),book=ISLANDS.find(b=>b.id===n.bookId),active=lit.has(n.id),focused=n.id===selected;
 return `<button class="network-island ${mountain?'network-mountain':'sea-island'} variant-${index%4} family-${n.family} ${active?'is-related':''} ${focused?'is-selected':''}" data-terrain="${mountain?'mountain':'island'}" data-node="${n.id}" data-instance="${i.id}" style="--x:${p.x}%;--y:${p.y}%" aria-label="${n.label}，點選查看互通主題與專頁" aria-pressed="${focused}"><span class="island-paint" aria-hidden="true"></span>${book?`<span class="node-book-icon" aria-hidden="true">${book.n===1?'<svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="#8b682f"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M12 3v6m0 6v6M3 12h6m6 0h6M5.6 5.6l4.2 4.2m4.4 4.4 4.2 4.2M18.4 5.6l-4.2 4.2m-4.4 4.4-4.2 4.2"/></svg>':`<img src="assets/shelf-${String(book.n).padStart(2,'0')}.svg" alt="">`}</span>`:''}<span class="network-label">${i.id.endsWith('four-truths-port')?'道・八正道山':n.label+(mountain?'山':'')}</span>${n.id==='four-truths'?'<span class="route-start">旅程起點</span>':''}${n.id==='roots-powers-overview'||n.id==='awakening-overview'?'<span class="route-end">左上對讀</span>':''}</button>`;
 }).join('');
 return `<div class="network-legend"><span><i class="gold-key"></i>閱讀導覽（可自由轉往其他島）</span><span><i class="relation-key"></i>原心智圖的對讀／群組關係</span><span><i class="active-key"></i>選取後亮起的互通主題</span></div><div class="scene-scroll network-scroll" tabindex="0" aria-label="原心智圖群島網絡，可左右上下平移"><div class="network-world" data-board="network"><img class="network-sea" src="assets/network-sea-concept.png" alt="以水彩海面與花草海岸承載原心智圖的群島網絡"><img class="continent-art" src="assets/continent-concept.png" alt="下方相關內容形成連續長條陸地，左側半島連向道路入口"><div class="continent-region-label" data-region="related">相關內容大陸</div><svg class="network-lines" viewBox="0 0 1800 1300" aria-hidden="true"><defs><marker id="network-return-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#4b8c8a"/></marker></defs>${paths}${route?`<path class="network-reading-route" d="${routePath}"/>`:''}</svg>${buttons}</div></div><p class="network-note">下排主題在同一塊大陸上成為山峰；右下「道」沿陸地小徑回到左側道路入口。閱讀航線仍只是導覽。</p>`;
}
export function nodePanel(id){
 const n=lookup.get(id),related=connected(id);related.delete(id);
 const exactNeighbours=EDGES.filter(e=>e.from===id||e.to===id).map(e=>e.from===id?e.to:e.from);
 return {title:n.label,html:`<p>這是原心智圖的「${n.key}」節點。${n.family==='mindfulness'?'念根念力、念覺支、正念與四念處可在同一縱向對讀網絡中互通。':''}</p><div class="dialog-actions"><a class="primary" data-network-guide href="${n.guide}">${n.bookId?'前往主題專頁':'前往原網站書架'} ↗</a><a data-network-reader href="${n.reader+(n.bookId?'?collection=1':'')}">${n.bookId?'閱讀並收集這本':'選擇繪本'} ↗</a></div><p><a href="shelf.html">查看十四本收集書架 ↗</a></p><h3>互通與相鄰主題</h3><div class="network-related-list">${[...related].map(key=>`<button data-related-node="${key}" data-direct="${exactNeighbours.includes(key)}">${lookup.get(key).label}</button>`).join('')}</div><p class="source-note">顯示原圖相鄰節點與同族縱向對讀；同一本的不同入口不重複計冊。此視覺提案不更動解鎖與存檔。</p>`};
}
