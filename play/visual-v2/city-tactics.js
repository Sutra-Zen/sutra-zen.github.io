import { CITY_SPOTS } from './data.js';
import { CATALOG } from '../collection/catalog.js';
import { store } from '../collection/store.js';
import { deriveCityState, routeOrder } from '../route/selectors.js';

// Image-relative display positions; actual artwork anchors remain separate.
const POSITION = {
 eye:[50,13],ear:[79,31],nose:[77.5,65],tongue:[50,81.5],body:[23,65],mind:[21,31],
 guardian:[34,67],messengers:[72,49],plaza:[45,48],lord:[61,27],message:[78,64],road:[57,94],town:[8,8]
};
const ART_ANCHOR={guardian:[29,63],messengers:[67.5,55.5],plaza:[50,51],lord:[50.2693,32.6],message:[64.6918,49.4155],road:[50,94]};
const SPOT_FEATURE={eye:'six_gates',ear:'six_gates',nose:'six_gates',tongue:'six_gates',body:'six_gates',mind:'six_gates',guardian:'mindfulness_guard',messengers:'calm_insight_messengers',plaza:'four_elements_plaza',lord:'city_lord',message:'truthful_message',road:'noble_path',town:'city_body',dock:'truth_dock'};
const SPOT_REWARD={...SPOT_FEATURE,plaza:'city_body',lord:'city_body',town:'city_body',message:'calm_insight_messengers'};
const SPOT_TITLES={guardian:'念-守門人',plaza:'地水火風四大廣場',messengers:'止・觀使者',message:'如實消息・涅槃'};
const SPOT_COPY={message:'使者傳達的如實話語譬喻涅槃。卷軸是本場景表現傳達消息的道具。'};
export const TACTICS_SPOTS=[...CITY_SPOTS.map(s=>({...s,title:SPOT_TITLES[s.id]||s.title,copy:SPOT_COPY[s.id]||s.copy,x:POSITION[s.id][0],y:POSITION[s.id][1],...(ART_ANCHOR[s.id]?{artAnchor:{x:ART_ANCHOR[s.id][0],y:ART_ANCHOR[s.id][1]}}:{})})),{id:'dock',title:'法輪碼頭',x:18,y:90,copy:'法輪碼頭是四聖諦讀本的遊戲延伸，不取代中央的四大廣場；SN35.245的如實消息仍對應涅槃。'}];
const asset=path=>new URL(path,import.meta.url).href;
export const TACTICS_ART={assetPath:'assets/city-scroll-audience-concept.png',path:asset('assets/city-scroll-audience-concept.png'),width:1671,height:941,status:'generated-concept-pending-author-review',gates:6};
export const CITY_LORD_HAIR={assetPath:'assets/city-lord-facial-hair-layer.png',path:asset('assets/city-lord-facial-hair-layer.png'),width:1536,height:1024,placement:{x:778,y:350,w:128,h:128*1024/1536}};
export function renderCityFacialHairImage(){const p=CITY_LORD_HAIR.placement;return `<image data-lord-facial-hair href="${CITY_LORD_HAIR.path}" x="${p.x}" y="${p.y}" width="${p.w}" height="${p.h}"/>`;}
export function renderCitySVGImages(){return `<image href="${TACTICS_ART.path}" x="0" y="0" width="${TACTICS_ART.width}" height="${TACTICS_ART.height}"/>${renderCityFacialHairImage()}`;}
const titles=new Map(CATALOG.map(b=>[b.id,b.title]));
const TEXT={
 scroll:'俯視六門城池，可上下左右平移查看；沒有棋格或戰鬥操作。',
 alt:'水彩俯視六門貓城概念圖，橘虎斑小貓城主戴小皇冠、八字鬍、下巴短鬍子與披肩，念守門貓和黑白、三花雙使分開扮演城喻角色。',
 travellerAlt:'金黃交領長袍的小橘貓旅人握槳坐在木船上，與皇冠鬍子城主、念守門人分開。',
 traveller:'旅人回到城池',readingOnly:'城景是閱讀回饋，不判定證果、斷結或取得禪定。',
 real:'使用實際閱讀進度',review:'審稿預覽，不寫入進度',initial:'初始',first:'讀完四聖諦',second:'再讀完五陰',third:'再讀完六處',all:'完整配置預覽',
 earned:'已取得',placed:'已安置',preview:'已取得・先預覽',unearned:'尚未取得',waiting:'完成所需讀本後自動安置，不需重讀已完成的書。',
 previews:'已取得，等待城景齊備',noWrites:'預覽切換不會新增、刪除或清空任何閱讀完成紀錄。',
 realIntro:'此畫面依已完成讀本顯示；未齊備的角色或城門保留在預覽中。',
 missing:'尚需完成',sourceTypes:{canonical:'SN城喻',mixed:'原喻＋場景延伸',extended:'場景延伸'},
 statuses:['城影仍在薄霧中。','四聖諦已讀完，法輪碼頭點亮。','五陰已讀完，城體、四大廣場與城主登場。','五陰與六處齊備，六道城門顯現。']
};
export const CITY_COPY={
 'zh-Hant':{...TEXT,progress:(count,total)=>`閱讀進度 ${count}／${total} 本`,pageTitle:'六門城池',pageIntro:'讀過的故事，讓城景慢慢清楚。點選標牌，對照城喻與相關繪本。',trial:'試玩版',backMap:'回到海圖',continue:'繼續閱讀',start:'開始閱讀四聖諦',next:'接著閱讀',revisit:'重讀四聖諦',continuePrefix:'接續',pageSuffix:'頁',labelsToggle:'城內標牌',zoom:'放大平移',overview:'看完整城池',sourceIndex:'城中對應與原經',reviewOptions:'審稿預覽選項',readingOnly:TEXT.readingOnly,close:'關閉',relatedBook:'相關繪本',reread:'重新閱讀',scripture:'查看城喻原經',missingPrefix:'尚需完成',sourceNote:'場景依SN35.245六門城喻改編；方位、衣裝與建設是教學美術。',unavailableStorage:'此瀏覽器暫時無法保存紀錄，仍可閱讀。',labels:{eye:{wide:'眼門',compact:'眼門'},ear:{wide:'耳門',compact:'耳門'},nose:{wide:'鼻門',compact:'鼻門'},tongue:{wide:'舌門',compact:'舌門'},body:{wide:'身門',compact:'身門'},mind:{wide:'意門',compact:'意門'},guardian:{wide:'念-守門人',compact:'念-守門人'},plaza:{wide:'地水火風四大廣場',compact:'地水火風\n四大廣場'},lord:{wide:'識・城主',compact:'識'},messengers:{wide:'止・觀使者',compact:'止・觀使者'},message:{wide:'如實消息・涅槃',compact:'如實消息・涅槃'},road:{wide:'八正道',compact:'八正道'},town:{wide:'城池',compact:'城池'},dock:{wide:'法輪碼頭',compact:'法輪碼頭'}}},
 'zh-Hans':null,en:null,ja:null
};
const WIDE_LABELS={town:[8,8],eye:[50,7],ear:[88,24],nose:[87,69],tongue:[48,88],body:[13,69],mind:[12,24],guardian:[31,74],messengers:[78,58],plaza:[39,46],lord:[60,32],message:[64.6918,60],road:[65,94],dock:[14,94]};
const COMPACT_LABELS={town:[9,14],eye:[50,14],lord:[82,14],mind:[10,38],plaza:[35,38],ear:[91,38],body:[10,64],guardian:[42,64],messengers:[66,38],nose:[91,64],dock:[14,88],tongue:[40,88],road:[65,88],message:[69,62]};
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
export const CITY_REWARD_CROPS={lord:[750,280,165,190],guardian:[425,535,120,125],messengers:[1025,378,190,155],gates:[735,35,195,150]};
const ROLE_CROP=Object.fromEntries(Object.entries(CITY_REWARD_CROPS).map(([id,[x,y,w,h]])=>[id,{x,y,w,h,label:({lord:'戴皇冠、八字鬍與下巴短鬍子的城主概念圖',guardian:'持燈的念守門貓概念',messengers:'黑白與三花貓扮演的止觀雙使概念',gates:'六門之一的門樓預覽'})[id]}]));
function cropArt(role){const c=ROLE_CROP[role];return `<figure class="tactics-character-preview"><svg viewBox="${c.x} ${c.y} ${c.w} ${c.h}" role="img" aria-label="${c.label}">${renderCitySVGImages()}</svg><figcaption>概念圖局部預覽，非獨立去背角色稿</figcaption></figure>`;}
export function renderCityRolePreview(id,reviewStage=null){const status=citySpotStatus(id,reviewStage);return ROLE_CROP[id]&&(status.earned||status.review)?cropArt(id):'';}
function rewardArt(reward){const role={mindfulness_guard:'guardian',calm_insight_messengers:'messengers',six_gates:'gates'}[reward.id];if(role)return cropArt(role);const b=CATALOG.find(b=>b.id===reward.bookId);return b?`<img class="tactics-reward-cover" src="${new URL(b.cover,new URL('../collection/catalog.js',import.meta.url)).href}" alt="${escape(b.title)}既有繪本縮圖；獎勵場景素材仍待補齊">`:'';}
function previewRewards(s){
 const pending=s.rewards.filter(r=>r.preview);
 return pending.length?`<section class="tactics-pending-rewards" aria-label="已取得的場景預覽"><h3>${TEXT.previews}</h3><div>${pending.map(r=>`<article data-preview-reward="${r.id}">${rewardArt(r)}<strong>${escape(r.title)}</strong><span>${TEXT.preview} · ${TEXT.sourceTypes[r.type]}</span><p>${TEXT.missing}：${r.missingBookIds.map(id=>escape(titles.get(id)||id)).join('、')}。${TEXT.waiting}</p></article>`).join('')}</div></section>`:'';
}
export function renderTacticsCity({cityState=null,reviewStage=null,celebrate=false,showSpots=true,showLabels=false,labelLayout='wide'}={}){
 const s=cityState||getCitySnapshot(reviewStage),f=s.features,gates=TACTICS_SPOTS.slice(0,6),labelPositions=labelLayout==='compact'?COMPACT_LABELS:WIDE_LABELS;
 const visibleSpots=TACTICS_SPOTS.filter(p=>showLabels||s.review||f[SPOT_FEATURE[p.id]]);
 const leaderLines=showSpots&&showLabels?`<svg class="tactics-label-lines" viewBox="0 0 ${TACTICS_ART.width} ${TACTICS_ART.height}" aria-hidden="true">${visibleSpots.map(p=>{const a=p.artAnchor||{x:p.x,y:p.y},b=labelPositions[p.id];return `<path data-label-for="${p.id}" d="M${a.x*TACTICS_ART.width/100} ${a.y*TACTICS_ART.height/100}L${b[0]*TACTICS_ART.width/100} ${b[1]*TACTICS_ART.height/100}"/>`;}).join('')}</svg>`:'';
 return `<div class="tactics-state-caption ${s.review?'is-review':''}" data-city-state-source="${s.review?'review':'collection'}"><strong>${s.review?TEXT.review:TEXT.real}</strong><span>${TEXT.statuses[s.stage]}</span><p>${s.review?TEXT.noWrites:TEXT.realIntro}</p></div><div class="scene-scroll tactics-scroll ${celebrate?'celebration-scroll':''}" tabindex="0" aria-label="${TEXT.scroll}"><div class="artboard city-tactics-board stage-${s.stage} ${celebrate?'is-celebration':''} ${f.city_body?'has-city-body':'without-city-body'} ${f.six_gates?'has-six-gates':''} ${f.truth_dock?'has-truth-dock':''}" data-board="city" data-city-view="top-down" data-city-stage="${s.stage}" data-city-review="${s.review}" data-city-body="${f.city_body}" data-city-guardian="${f.mindfulness_guard}" data-city-messengers="${f.calm_insight_messengers}" data-city-labels="${showLabels}" style="--city-aspect:${TACTICS_ART.width}/${TACTICS_ART.height}">
 <div class="tactics-painted-layer"><img class="scene-art tactics-art" src="${TACTICS_ART.path}" alt="${TEXT.alt}" width="${TACTICS_ART.width}" height="${TACTICS_ART.height}"><svg class="tactics-lord-hair" viewBox="0 0 ${TACTICS_ART.width} ${TACTICS_ART.height}" aria-hidden="true">${renderCityFacialHairImage()}</svg>

 ${gates.map(g=>featureVeil('gate-'+g.id,g.x,g.y,13,16,f.six_gates)).join('')}
 ${featureVeil('guardian',ART_ANCHOR.guardian[0],ART_ANCHOR.guardian[1],11,20,f.mindfulness_guard)}
 ${featureVeil('messengers',ART_ANCHOR.messengers[0],ART_ANCHOR.messengers[1],13,18,f.calm_insight_messengers)}</div>
 <div class="tactics-truth-dock ${f.truth_dock?'is-earned':''}" data-feature="truth_dock" data-available="${f.truth_dock}" aria-label="法輪碼頭，${f.truth_dock?TEXT.earned:TEXT.unearned}"><img src="${asset('assets/city-dharma-dock-concept.png')}" alt="透明水彩木碼頭與八輻法輪，四聖諦閱讀完成後點亮"></div>
 <svg class="tactics-road-light ${f.noble_path?'is-active':''}" viewBox="0 0 ${TACTICS_ART.width} ${TACTICS_ART.height}" aria-hidden="true"><path d="M836 930L836 805L836 650L836 480"/></svg>
 <div class="tactics-plaza-light ${f.four_elements_plaza?'is-active':''}" style="--x:50%;--y:51%" aria-hidden="true"></div>
 ${gates.map(g=>`<span class="tactics-gate-light ${f.six_gates?'is-active':''}" data-gate-light="${g.id}" style="--x:${g.x}%;--y:${g.y}%" aria-hidden="true"></span>`).join('')}
 ${leaderLines}${!celebrate&&showSpots?visibleSpots.map(p=>{const xy=showLabels?labelPositions[p.id]:[p.x,p.y];return `<button class="city-spot tactics-spot ${showLabels?'tactics-label':''} ${gates.some(g=>g.id===p.id)?'tactics-gate-hotspot':''} ${f[SPOT_FEATURE[p.id]]?'is-available':'is-future'}" data-spot="${p.id}" ${showLabels?`data-city-label="${p.id}"`: ''} data-feature-available="${Boolean(f[SPOT_FEATURE[p.id]])}" style="--x:${xy[0]}%;--y:${xy[1]}%" aria-label="查看${p.title}">${showLabels?`<span class="tactics-label-text">${CITY_COPY['zh-Hant'].labels[p.id][labelLayout==='compact'?'compact':'wide']}</span>`:`<span aria-hidden="true">＋</span><span class="spot-name">${p.title}</span>`}</button>`;}).join(''):''}
 ${celebrate&&s.completedBookIds.length?'<div class="tactics-fireflies" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>':''}
 </div></div>${previewRewards(s)}${celebrate?`<div class="tactics-traveler-note"><img src="${asset('assets/kitten-rowboat-concept.png')}" alt="${TEXT.travellerAlt}"><p><strong>${TEXT.traveller}</strong><span>${TEXT.readingOnly}</span></p></div>`:''}`;
}
