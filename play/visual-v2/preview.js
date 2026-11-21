import { networkMarkup, nodePanel, point } from './network.js';
import { NODES, INSTANCES } from './network-data.js';
import { ISLANDS, RELATIONS, CITY_SPOTS, COPY } from './data.js';
const host=document.querySelector('#scene-host'),controls=document.querySelector('#scene-controls'),footer=document.querySelector('#scene-footer'),dialog=document.querySelector('#inspect-dialog'),content=document.querySelector('#inspect-content');
let view='network',stage=0,relations=false,showSpots=true,zoom=innerWidth>800;
let selectedNode=null,showReadingRoute=true,showNetworkLinks=true,cameraNode='four-truths';
const wheel='<svg viewBox="0 0 80 80" aria-hidden="true"><circle cx="40" cy="40" r="28"/><circle cx="40" cy="40" r="10"/>'+Array.from({length:8},(_,i)=>`<path d="M40 12V30" transform="rotate(${i*45} 40 40)"/>`).join('')+'</svg>';
const boat=(cls='')=>`<div class="traveler ${cls}" aria-label="小貓木船概念立繪，待作者確認"><img src="assets/kitten-rowboat-concept.png" alt="金黃長袍的小橘貓握著木槳坐在木船上"></div>`;
const icon=n=>n===1?wheel:`<img src="assets/shelf-${String(n).padStart(2,'0')}.svg" alt="">`;
function open(title,html){content.innerHTML=`<p class="eyebrow">繪本旅程・視覺提案</p><h2 id="inspect-title">${title}</h2>${html}`;if(!dialog.open)dialog.showModal();}
function island(i){const first=i.n<=3,locked=first&&i.n>stage+1,read=first&&i.n<=stage;
 return `<button class="island-pin ${first?'first-island':'future-island'} ${locked?'is-locked':''} ${read?'is-read':''}" data-island="${i.n}" style="--x:${i.x}%;--y:${i.y}%" aria-label="${i.title}，${first?locked?'尚未解鎖':read?'已讀示範':'可閱讀':'後續旅程，原書已可閱讀'}"><span class="pin-icon">${icon(i.n)}</span>${locked?'<span class="lock-dot" aria-hidden="true"><img src="assets/shelf-lock.svg" alt=""></span>':''}${read?'<span class="read-dot" aria-hidden="true">✓</span>':''}<span class="island-name">${i.title}</span></button>`;
}
function stageControls(){return `<span>視覺狀態示範</span><div class="stage-options" role="group" aria-label="預覽閱讀後的場景變化">${[0,1,2,3].map(n=>`<button data-stage="${n}" aria-pressed="${stage===n}">${n===0?'初始':`讀完${n}本`}</button>`).join('')}</div>`;}
function mapScene(){
 const relationPaths=RELATIONS.map(([a,b])=>{const x=ISLANDS[a-1],y=ISLANDS[b-1];return `<path d="M${x.x*15.36} ${x.y*10.24}Q768 380 ${y.x*15.36} ${y.y*10.24}"/>`;}).join('');
 return `<div class="scene-scroll" tabindex="0" aria-label="群島全景，可左右與上下捲動"><div class="artboard map-board stage-${stage}" data-board="map"><img class="scene-art" src="assets/archipelago-concept.png" alt="森林花草與溪流環繞的水彩群島，中央有城池，前景有法輪、五種相依景物和六窗小屋"><svg class="sea-routes" viewBox="0 0 1536 1024" aria-hidden="true"><path class="reading-route" d="M290 842C410 960 560 948 815 847S1250 800 1330 660"/><g class="related-routes" ${relations?'':'hidden'}>${relationPaths}</g></svg>${stage<1?'<div class="mist mist-five" aria-hidden="true"></div>':''}${stage<2?'<div class="mist mist-six" aria-hidden="true"></div>':''}${ISLANDS.map(island).join('')}<button class="town-pin" data-go="city" style="--x:48%;--y:37%">進入城池 <span>↗</span></button>${boat('map-boat')}</div></div>`;
}
function cityScene(celebrate=false){return `<div class="scene-scroll ${celebrate?'celebration-scroll':''}" tabindex="0" aria-label="六門城池水彩場景，可放大探索"><div class="artboard city-board stage-${stage} ${celebrate?'is-celebration':''}" data-board="city"><img class="scene-art" src="assets/city-concept.png" alt="六座門樓圍繞花園城池，中央廣場有地水火風的景物，石徑連向城外碼頭"><div class="city-atmosphere" aria-hidden="true"></div><img class="garden-growth" src="assets/garden-growth-concept.png" alt="" aria-hidden="true"><svg class="road-light" viewBox="0 0 1536 1024" aria-hidden="true"><path d="M775 1000C770 900 760 845 750 795S660 680 705 607"/></svg>${CITY_SPOTS.slice(0,6).map((s,i)=>`<span class="gate-light gate-light-${i}" style="--x:${s.x}%;--y:${s.y}%" aria-hidden="true"></span>`).join('')}${celebrate?boat('return-boat'):''}${!celebrate&&showSpots?CITY_SPOTS.map(s=>`<button class="city-spot" data-spot="${s.id}" style="--x:${s.x}%;--y:${s.y}%" aria-label="查看${s.title}"><span aria-hidden="true">＋</span><span class="spot-name">${s.title}</span></button>`).join(''):''}${celebrate?'<div class="fireflies" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>':''}</div></div>`;}
function render(){
 document.querySelector('#screen-title').textContent=view==='network'?'修道群島・互通海圖':view==='map'?COPY.mapTitle:view==='city'?COPY.cityTitle:COPY.celebrateTitle;
 document.querySelector('#scene-description').textContent=view==='network'?'從右下四聖諦出發，沿閱讀航線走向左上；每個小島仍保留原心智圖的互通連線，可自由點開專頁。':COPY.descriptions[view];
 document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
 controls.innerHTML=view==='network'?`<div class="network-controls"><button data-net-toggle="route" aria-pressed="${showReadingRoute}">閱讀航線</button><button data-net-toggle="links" aria-pressed="${showNetworkLinks}">全部互通連線</button><button data-net-locate="four-truths">定位四聖諦</button><button data-net-locate="four-mindfulness">看念的互通</button><button data-net-locate="roots-powers-overview">定位左上總說</button><button data-net-clear>清除選取</button><button data-toggle="zoom">${zoom?'放大探索':'只看全景'}</button></div>`:stageControls()+`<div class="explore-options">${view==='map'?`<button data-toggle="relations" aria-pressed="${relations}">心智圖關聯</button>`:view==='city'?`<button data-toggle="spots" aria-pressed="${showSpots}">${showSpots?'隱藏探索點':'顯示探索點'}</button>`:''}<button data-toggle="zoom" aria-pressed="${zoom}">${zoom?'返回探索':'只看全景'}</button></div>`;
 host.innerHTML=view==='network'?networkMarkup({selected:selectedNode,route:showReadingRoute,allLinks:showNetworkLinks}):view==='map'?mapScene():cityScene(view==='celebrate');host.classList.toggle('is-overview',zoom);
 footer.innerHTML=view==='network'?`<div class="network-footer"><img src="assets/kitten-rowboat-concept.png" alt="握著木槳、不持燈籠的小橘貓旅人"><div><strong>旅人陪你閱讀，不固定代表某一支法。</strong><p>32個主題、33個島嶼入口；八正道的兩處入口仍是同一份內容。先點小島，再前往專頁或繪本。</p><p>閱讀導覽不是修證次第；原站的每本繪本都可自由閱讀。</p></div><button class="primary" data-node="four-truths">從四聖諦開始 →</button></div>`:view==='map'?`<div><strong>第一段旅程</strong><span>四聖諦 → 五陰 → 六處</span><span>場景可左右／上下滑動，也可直接定位。</span></div><div class="locate-options" role="group" aria-label="定位閱讀島">${ISLANDS.slice(0,3).map(i=>`<button data-locate="${i.n}">定位${i.title}</button>`).join('')}</div><button class="primary" data-island="${Math.min(stage+1,3)}">${stage===3?'重訪六處島':'前往'+ISLANDS[Math.min(stage,2)].title+'島 →'}</button>`:view==='city'?`<span>場景可左右／上下滑動；法義說明由點選開啟。</span><button data-help="city">查看法義索引</button><a href="../sources.html">工程配置與原經對讀 ↗</a>`:`<div class="celebration-copy"><span class="eyebrow">${stage===3?'第一段旅程完成':'旅人回到城池'}</span><h2>${COPY.feedback[stage]}</h2><p>此為回饋演出預覽，不會改變已保存的閱讀紀錄。</p></div><button class="primary" data-continue>${stage===3?'重訪群島':'繼續旅程 →'}</button>`;
  if(view==='network'&&!zoom){requestAnimationFrame(()=>centerNetwork(cameraNode));}
  else if(view!=='network'&&innerWidth<=800){requestAnimationFrame(()=>{const sc=host.querySelector('.scene-scroll'),board=host.querySelector('.artboard');if(sc&&board)sc.scrollTo({left:board.clientWidth*(view==='map'?[.27,.63,.83,.83][stage]:.5)-sc.clientWidth/2,top:board.clientHeight*(view==='map'?.69:view==='celebrate'?.64:.52)-sc.clientHeight/2});});}
}
document.addEventListener('click',e=>{
 const b=e.target.closest('button');if(!b)return;
 if(b.dataset.view){view=b.dataset.view;zoom=view==='network'&&innerWidth>800;render();}
 if(b.dataset.netLocate){cameraNode=b.dataset.netLocate;selectedNode=cameraNode;zoom=false;render();}
 if(b.hasAttribute('data-net-clear')){selectedNode=null;render();}
 if(b.dataset.netToggle){if(b.dataset.netToggle==='route')showReadingRoute=!showReadingRoute;if(b.dataset.netToggle==='links')showNetworkLinks=!showNetworkLinks;render();}
 if(b.dataset.node||b.dataset.relatedNode){const id=b.dataset.node||b.dataset.relatedNode;selectedNode=id;cameraNode=id;render();const panel=nodePanel(id);open(panel.title,panel.html);}
 if(b.hasAttribute('data-stage')){stage=Number(b.dataset.stage);render();}
 if(b.dataset.toggle){if(b.dataset.toggle==='relations')relations=!relations;if(b.dataset.toggle==='spots')showSpots=!showSpots;if(b.dataset.toggle==='zoom')zoom=!zoom;render();}
 if(b.dataset.locate){zoom=false;render();const i=ISLANDS.find(i=>i.n===Number(b.dataset.locate));requestAnimationFrame(()=>{const sc=host.querySelector('.scene-scroll'),board=host.querySelector('.artboard');sc.scrollTo({left:board.clientWidth*i.x/100-sc.clientWidth/2,top:board.clientHeight*i.y/100-sc.clientHeight/2,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});});}
 if(b.dataset.go){view=b.dataset.go;render();}
 if(b.hasAttribute('data-island')){
 const i=ISLANDS.find(i=>i.n===Number(b.dataset.island));const locked=i.n<=3&&i.n>stage+1;
 const status=i.n>3?'後續旅程':locked?'薄霧中的下一站':i.n<=stage?'已讀狀態示範':'現在可以出發';
 open(i.title,`<span class="status-label">${status}</span><p>${i.feature||'保留原書架的小圖，作為這座島未讀時的辨識。'}</p><p>${i.relation}</p>${i.n>3?'<p>這本繪本已在原網站公開閱讀；第一版旅程只接入前三本，不表示它尚未上架。</p>':locked?'<p>正式旅程須讀完前一本才開放。本預覽可切換上方狀態，查看霧散後的樣子。</p>':'<p>閱讀操作在點選島嶼後才顯示。此輪先確認構圖，完整進度與解鎖仍沿用第一版功能原型。</p>'}<div class="dialog-actions">${i.n<=3&&!locked?`<a class="primary" href="../../${i.id}/book/">試讀原繪本 ↗</a>`:''}<a href="../../${i.id}/">${i.n>3?'前往原專頁':'主題導讀'} ↗</a></div>`);
 }
 if(b.dataset.spot){const s=CITY_SPOTS.find(s=>s.id===b.dataset.spot);open(s.title,`<p>${s.copy}</p><p class="source-note">場景依《相應部》SN 35.245 六門城喻改編。人物、門樓方位及光影是教學美術。</p><a href="../sources.html">原經與漢巴差異對讀 ↗</a>`);}
 if(b.dataset.help==='city')open('城池法義索引',`<p>也可從場景中的探索點逐一查看。</p><div class="meaning-index">${CITY_SPOTS.map(s=>`<button data-spot="${s.id}">${s.title}</button>`).join('')}</div><a href="../sources.html">保留的工程配置圖與原經 ↗</a>`);
 if(b.hasAttribute('data-continue')){view='map';render();window.scrollTo(0,0);}
 if(b.classList.contains('close-dialog'))dialog.close();
});
render();

function centerNetwork(id){const i=INSTANCES.find(i=>i.nodeId===id);if(!i)return;const sc=host.querySelector('.network-scroll'),world=host.querySelector('.network-world');if(!sc||!world)return;const p=point(i);sc.scrollTo({left:p.x*world.clientWidth/100-sc.clientWidth/2,top:p.y*world.clientHeight/100-sc.clientHeight/2});}
