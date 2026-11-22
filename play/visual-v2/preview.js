// Read-only historical artwork gallery. All imports are data/rendering only.
// No player store, metadata, shell, reader bridge or completion event is imported.
import {networkMarkup,nodePanel,point} from './network.js';
import {MAP_STYLES} from './art-directions.js';
import {INSTANCES} from './network-data.js';
const host=document.querySelector('#scene-host'),controls=document.querySelector('#scene-controls'),footer=document.querySelector('#scene-footer'),dialog=document.querySelector('#inspect-dialog'),content=document.querySelector('#inspect-content');
const params=new URLSearchParams(location.search),inspectionURL=new URL('../city/inspection.html',import.meta.url).href;
const text={network:'歷史互通海圖・畫風比較',map:'早期群島構圖',networkCopy:'比較三種畫風與原心智圖關係；這裡不讀取、寫入或清除遊戲存檔。歷史航線不是目前的遊戲解鎖順序。',mapCopy:'保留早期水彩構圖供檢視，不模擬閱讀完成，也不提供遊戲關卡入口。',inspectCity:'城池構圖檢視（唯讀）',siteShelf:'原網站書架（離開檢視）',leaveGame:'前往遊戲（離開檢視）'};
let style=Object.hasOwn(MAP_STYLES,params.get('style'))?params.get('style'):'terrain';
let view=params.get('view')==='map'?'map':'network',selected=null,route=true,allLinks=true,overview=innerWidth>800,cameraNode='four-truths';
let returnFocus=null;
function centerNetwork(id){const i=INSTANCES.find(i=>i.nodeId===id),sc=host.querySelector('.network-scroll'),world=host.querySelector('.network-world');if(!i||!sc||!world)return;const p=point(i,style);sc.scrollTo({left:p.x*world.clientWidth/100-sc.clientWidth/2,top:p.y*world.clientHeight/100-sc.clientHeight/2});}
function openNode(id){selected=id;cameraNode=id;render();const panel=nodePanel(id);content.innerHTML=`<p class="eyebrow">唯讀美術與關係檢視</p><h2 id="inspect-title">${panel.title}</h2>${panel.html}`;returnFocus=`[data-node="${id}"]`;if(!dialog.open)dialog.showModal();}
function render(){
 document.querySelector('#screen-title').textContent=text[view];document.querySelector('#scene-description').textContent=text[view+'Copy'];
 document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
 controls.innerHTML=view==='network'?`<div class="map-style-picker" role="group" aria-label="比較地圖畫風"><span>比較畫風</span>${Object.entries(MAP_STYLES).map(([key,art])=>`<button data-map-style="${key}" aria-pressed="${key===style}">${art.label}</button>`).join('')}</div><div class="network-controls"><button data-net-toggle="route" aria-pressed="${route}">歷史構圖航線</button><button data-net-toggle="links" aria-pressed="${allLinks}">全部互通連線</button><button data-net-locate="four-truths">定位四聖諦</button><button data-net-locate="four-mindfulness">看念的互通</button><button data-net-locate="roots-powers-overview">定位左上總說</button><button data-net-clear>清除選取</button><button data-net-overview>${overview?'放大探索':'只看全景'}</button></div>`:'';
 host.innerHTML=view==='network'?networkMarkup({selected,route,allLinks,style}):'<div class="scene-scroll"><div class="artboard map-board"><img class="scene-art" src="assets/archipelago-concept.png" alt="早期水彩群島、中央城池與法輪構圖；唯讀美術參考"></div></div>';
 host.classList.toggle('is-overview',overview||view==='map');
 footer.innerHTML=`<p>此檢視不取得角色、不解鎖書籍，也不改變已讀本數。</p><a href="${inspectionURL}">${text.inspectCity} ↗</a><a href="../../index.html#books">${text.siteShelf} ↗</a>`;
 if(view==='network'&&!overview)requestAnimationFrame(()=>centerNetwork(cameraNode));
}
function handleClick(event){const b=event.target.closest('button');if(!b)return;
 if(b.classList.contains('close-dialog')){dialog.close();return;}
 if(b.dataset.view==='city'||b.dataset.view==='celebrate'){location.assign(inspectionURL);return;}
 if(b.dataset.mapStyle){style=b.dataset.mapStyle;render();}
 if(b.dataset.view==='network'||b.dataset.view==='map'){view=b.dataset.view;render();}
 if(b.dataset.netLocate){cameraNode=b.dataset.netLocate;selected=cameraNode;overview=false;render();}
 if(b.hasAttribute('data-net-clear')){selected=null;render();}
 if(b.dataset.netToggle){if(b.dataset.netToggle==='route')route=!route;if(b.dataset.netToggle==='links')allLinks=!allLinks;render();}
 if(b.hasAttribute('data-net-overview')){overview=!overview;render();}
 if(b.dataset.node||b.dataset.relatedNode)openNode(b.dataset.node||b.dataset.relatedNode);
}
if(['city','celebrate'].includes(params.get('view'))){location.replace(inspectionURL);}else{
 document.addEventListener('click',handleClick);dialog.addEventListener('close',()=>{const target=returnFocus&&host.querySelector(returnFocus);target?.focus({preventScroll:true});});render();
}
