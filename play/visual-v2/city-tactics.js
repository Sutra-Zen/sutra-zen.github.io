import { CITY_SPOTS } from './data.js';
import { CATALOG } from '../collection/catalog.js';
import { store } from '../collection/store.js';
import { deriveCityState, routeOrder } from '../route/selectors.js';

// Image-relative display positions; actual artwork anchors remain separate.
const POSITION = {
 eye:[50,12],ear:[80,30],nose:[78.5,61.5],tongue:[50,77],body:[21.5,61],mind:[20.5,30],
 guardian:[30.8,62],messengers:[71.5,47.5],plaza:[50,47],lord:[57,30],message:[72.5,57.5],road:[50,93],town:[50,4.8]
};
const ART_ANCHOR={guardian:[27.4,59.1],messengers:[66.3,51.8]};
const SPOT_FEATURE={eye:'six_gates',ear:'six_gates',nose:'six_gates',tongue:'six_gates',body:'six_gates',mind:'six_gates',guardian:'mindfulness_guard',messengers:'calm_insight_messengers',plaza:'four_elements_plaza',lord:'city_lord',message:'truthful_message',road:'noble_path',town:'city_body',dock:'truth_dock'};
const SPOT_REWARD={...SPOT_FEATURE,plaza:'city_body',lord:'city_body',town:'city_body',message:'calm_insight_messengers'};
export const TACTICS_SPOTS=[...CITY_SPOTS.map(s=>({...s,x:POSITION[s.id][0],y:POSITION[s.id][1],...(ART_ANCHOR[s.id]?{artAnchor:{x:ART_ANCHOR[s.id][0],y:ART_ANCHOR[s.id][1]}}:{})})),{id:'dock',title:'法輪碼頭',x:18,y:90,copy:'法輪碼頭是四聖諦讀本的遊戲延伸，不取代中央的四大廣場；SN35.245的如實消息仍對應涅槃。'}];
const asset=path=>new URL(path,import.meta.url).href;
export const TACTICS_ART={assetPath:'assets/city-cats-concept.png',path:asset('assets/city-cats-concept.png'),width:1536,height:1024,status:'generated-concept-pending-author-review',gates:6};
const titles=new Map(CATALOG.map(b=>[b.id,b.title]));
const TEXT={
 scroll:'俯視六門城池，可上下左右平移查看；沒有棋格或戰鬥操作。',
 alt:'水彩俯視六門貓城概念圖，橘虎斑小貓城主戴小皇冠、短下巴鬍子與披肩，念守門貓和黑白、三花雙使分開扮演城喻角色。',
 travellerAlt:'金黃交領長袍的小橘貓旅人握槳坐在木船上，與皇冠鬍子城主、念守門人分開。',
 traveller:'旅人回到城池',readingOnly:'城景是閱讀回饋，不判定證果、斷結或取得禪定。',
 real:'使用實際閱讀進度',review:'審稿預覽，不寫入進度',initial:'初始',first:'讀完四聖諦',second:'再讀完五陰',third:'再讀完六處',all:'完整配置預覽',
 earned:'已取得',placed:'已安置',preview:'已取得・先預覽',unearned:'尚未取得',waiting:'完成所需讀本後自動安置，不需重讀已完成的書。',
 previews:'已取得，等待城景齊備',noWrites:'預覽切換不會新增、刪除或清空任何閱讀完成紀錄。',
 realIntro:'此畫面依已完成讀本顯示；未齊備的角色或城門保留在預覽中。',
 missing:'尚需完成',sourceTypes:{canonical:'SN城喻',mixed:'原喻＋場景延伸',extended:'場景延伸'},
 statuses:['城影仍在薄霧中。','四聖諦已讀完，法輪碼頭點亮。','五陰已讀完，城體、四大廣場與城主登場。','五陰與六處齊備，六道城門顯現。']
};
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function getCitySnapshot(reviewStage=null){
 const saved=store.get();
 const completed=reviewStage==='all'?routeOrder:reviewStage===null?saved.completed:routeOrder.slice(0,Math.max(0,Math.min(3,Number(reviewStage)||0)));
 return {...deriveCityState(completed,saved.positions,saved),review:reviewStage!==null,reviewStage};
}
export function cityReviewControls(reviewStage=null){
 return `<span>${reviewStage===null?TEXT.real:TEXT.review}</span><div class="stage-options city-review-options" role="group" aria-label="城景審稿與實際進度">${[[null,TEXT.real],[0,TEXT.initial],[1,TEXT.first],[2,TEXT.second],[3,TEXT.third],['all',TEXT.all]].map(([value,label])=>`<button data-city-review="${value===null?'real':value}" aria-pressed="${reviewStage===value}">${label}</button>`).join('')}</div>`;
}
export function citySpotStatus(id,reviewStage=null){
 const s=getCitySnapshot(reviewStage),reward=s.rewards.find(r=>r.id===SPOT_REWARD[id]);
 const available=Boolean(s.features[SPOT_FEATURE[id]]),earned=Boolean(reward?.earned);
 const missing=id==='message'&&!s.sceneFlags.city_allegory?['five-aggregates','six-senses','eightfold-path','mindfulness','anapana'].filter(book=>!s.completedBookIds.includes(book)):reward?.missingBookIds||[];
 return {earned,available,preview:earned&&!available,review:s.review,statusText:s.review?TEXT.review:available?TEXT.placed:earned?TEXT.preview:TEXT.unearned,missingTitles:missing.map(book=>titles.get(book)||book)};
}
export function cityFeedbackText(reviewStage=null){return TEXT.statuses[getCitySnapshot(reviewStage).stage];}
function featureVeil(name,x,y,w,h,visible){return visible?'':`<div class="tactics-feature-veil veil-${name}" data-concealed-feature="${name}" style="--x:${x}%;--y:${y}%;--w:${w}%;--h:${h}%" aria-hidden="true"><img class="tactics-veil-art" src="${TACTICS_ART.path}" alt="" style="width:${10000/w}%;height:${10000/h}%;left:${-(x-w/2)/w*100}%;top:${-(y-h/2)/h*100}%"></div>`;}
const ROLE_CROP={lord:{x:710,y:215,w:160,h:155,label:'city_lord_cat・皇冠短鬍子城主概念'},guardian:{x:370,y:535,w:120,h:140,label:'持燈的念守門貓概念'},messengers:{x:940,y:470,w:165,h:125,label:'黑白與三花貓扮演的止觀雙使概念'},gates:{x:680,y:35,w:185,h:145,label:'六門之一的門樓預覽'}};
function cropArt(role){const c=ROLE_CROP[role];return `<figure class="tactics-character-preview"><svg viewBox="${c.x} ${c.y} ${c.w} ${c.h}" role="img" aria-label="${c.label}"><image href="${TACTICS_ART.path}" x="0" y="0" width="${TACTICS_ART.width}" height="${TACTICS_ART.height}"/></svg><figcaption>概念圖局部預覽，非獨立去背角色稿</figcaption></figure>`;}
export function renderCityRolePreview(id,reviewStage=null){const status=citySpotStatus(id,reviewStage);return ROLE_CROP[id]&&(status.earned||status.review)?cropArt(id):'';}
function rewardArt(reward){const role={mindfulness_guard:'guardian',calm_insight_messengers:'messengers',six_gates:'gates'}[reward.id];if(role)return cropArt(role);const b=CATALOG.find(b=>b.id===reward.bookId);return b?`<img class="tactics-reward-cover" src="${new URL(b.cover,new URL('../collection/catalog.js',import.meta.url)).href}" alt="${escape(b.title)}既有繪本縮圖；獎勵場景素材仍待補齊">`:'';}
function previewRewards(s){
 const pending=s.rewards.filter(r=>r.preview);
 return pending.length?`<section class="tactics-pending-rewards" aria-label="已取得的場景預覽"><h3>${TEXT.previews}</h3><div>${pending.map(r=>`<article data-preview-reward="${r.id}">${rewardArt(r)}<strong>${escape(r.title)}</strong><span>${TEXT.preview} · ${TEXT.sourceTypes[r.type]}</span><p>${TEXT.missing}：${r.missingBookIds.map(id=>escape(titles.get(id)||id)).join('、')}。${TEXT.waiting}</p></article>`).join('')}</div></section>`:'';
}
export function renderTacticsCity({cityState=null,reviewStage=null,celebrate=false,showSpots=true}={}){
 const s=cityState||getCitySnapshot(reviewStage),f=s.features,gates=TACTICS_SPOTS.slice(0,6);
 return `<div class="tactics-state-caption ${s.review?'is-review':''}" data-city-state-source="${s.review?'review':'collection'}"><strong>${s.review?TEXT.review:TEXT.real}</strong><span>${TEXT.statuses[s.stage]}</span><p>${s.review?TEXT.noWrites:TEXT.realIntro}</p></div><div class="scene-scroll tactics-scroll ${celebrate?'celebration-scroll':''}" tabindex="0" aria-label="${TEXT.scroll}"><div class="artboard city-tactics-board stage-${s.stage} ${celebrate?'is-celebration':''} ${f.city_body?'has-city-body':'without-city-body'} ${f.six_gates?'has-six-gates':''} ${f.truth_dock?'has-truth-dock':''}" data-board="city" data-city-view="top-down" data-city-stage="${s.stage}" data-city-review="${s.review}" data-city-body="${f.city_body}" data-city-guardian="${f.mindfulness_guard}" data-city-messengers="${f.calm_insight_messengers}">
 <div class="tactics-painted-layer"><img class="scene-art tactics-art" src="${TACTICS_ART.path}" alt="${TEXT.alt}" width="${TACTICS_ART.width}" height="${TACTICS_ART.height}">

 ${gates.map(g=>featureVeil('gate-'+g.id,g.x,g.y,13,16,f.six_gates)).join('')}
 ${featureVeil('guardian',ART_ANCHOR.guardian[0],ART_ANCHOR.guardian[1],11,20,f.mindfulness_guard)}
 ${featureVeil('messengers',ART_ANCHOR.messengers[0],ART_ANCHOR.messengers[1],13,18,f.calm_insight_messengers)}</div>
 <div class="tactics-truth-dock ${f.truth_dock?'is-earned':''}" data-feature="truth_dock" data-available="${f.truth_dock}" aria-label="法輪碼頭，${f.truth_dock?TEXT.earned:TEXT.unearned}"><img src="${asset('assets/city-dharma-dock-concept.png')}" alt="透明水彩木碼頭與八輻法輪，四聖諦閱讀完成後點亮"></div>
 <svg class="tactics-road-light ${f.noble_path?'is-active':''}" viewBox="0 0 1536 1024" aria-hidden="true"><path d="M768 1010L768 842L768 630L768 482"/></svg>
 <div class="tactics-plaza-light ${f.four_elements_plaza?'is-active':''}" style="--x:50%;--y:47%" aria-hidden="true"></div>
 ${gates.map(g=>`<span class="tactics-gate-light ${f.six_gates?'is-active':''}" data-gate-light="${g.id}" style="--x:${g.x}%;--y:${g.y}%" aria-hidden="true"></span>`).join('')}
 ${!celebrate&&showSpots?TACTICS_SPOTS.filter(p=>s.review||f[SPOT_FEATURE[p.id]]).map(p=>`<button class="city-spot tactics-spot ${gates.some(g=>g.id===p.id)?'tactics-gate-hotspot':''} ${f[SPOT_FEATURE[p.id]]?'is-available':'is-future'}" data-spot="${p.id}" data-feature-available="${Boolean(f[SPOT_FEATURE[p.id]])}" style="--x:${p.x}%;--y:${p.y}%" aria-label="查看${p.title}"><span aria-hidden="true">＋</span><span class="spot-name">${p.title}</span></button>`).join(''):''}
 ${celebrate&&s.completedBookIds.length?'<div class="tactics-fireflies" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>':''}
 </div></div>${previewRewards(s)}${celebrate?`<div class="tactics-traveler-note"><img src="${asset('assets/kitten-rowboat-concept.png')}" alt="${TEXT.travellerAlt}"><p><strong>${TEXT.traveller}</strong><span>${TEXT.readingOnly}</span></p></div>`:''}`;
}
