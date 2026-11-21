import { CITY_SPOTS } from './data.js';

// Coordinates are image-relative percentages; keep the original doctrinal copy.
// Calibrated to city-tactics-concept.png (1536×1024); not canonical geography.
const POSITION = {
 eye:[50,12], ear:[80,30], nose:[78.5,61.5], tongue:[50,77],
 body:[21.5,61], mind:[20.5,30], guardian:[30.8,62], messengers:[67.5,47.5],
 plaza:[50,47], lord:[50,25], message:[72.5,57.5], road:[50,93], town:[50,4.8]
};
// Person markers sit beside their figures so the buttons do not cover faces.
const ART_ANCHOR = {guardian:[27.3,59.5],messengers:[65.5,52.5]};
export const TACTICS_SPOTS = CITY_SPOTS.map(s=>({...s,x:POSITION[s.id][0],y:POSITION[s.id][1],...(ART_ANCHOR[s.id]?{artAnchor:{x:ART_ANCHOR[s.id][0],y:ART_ANCHOR[s.id][1]}}:{})}));
export const TACTICS_ART = {
 path:'assets/city-tactics-concept.png', width:1536, height:1024,
 status:'generated-concept-pending-author-review', gates:6
};
const TEXT = {
 scroll:'俯視六門城池，可上下左右平移查看；圖上沒有棋格或戰鬥操作。',
 alt:'水彩俯視城池概念圖，六座城門圍繞中央四大廣場，城內道路與人物供點選對讀。',
 travellerAlt:'金黃色長袍的小橘貓旅人握著木槳坐在小船上，不兼任城喻的守門者。',
 traveller:'旅人回到城池', readingOnly:'初始與亮燈為閱讀回饋示範，不表示證果或斷結。'
};
export function renderTacticsCity({stage=0,celebrate=false,showSpots=true}={}) {
 const level=Math.max(0,Math.min(3,Math.trunc(Number(stage)||0)));
 const gates=TACTICS_SPOTS.slice(0,6);
 return `<div class="scene-scroll tactics-scroll ${celebrate?'celebration-scroll':''}" tabindex="0" aria-label="${TEXT.scroll}"><div class="artboard city-tactics-board stage-${level} ${celebrate?'is-celebration':''}" data-board="city" data-city-view="top-down" data-city-stage="${level}">
 <img class="scene-art tactics-art" src="${TACTICS_ART.path}" alt="${TEXT.alt}" width="${TACTICS_ART.width}" height="${TACTICS_ART.height}">
 <div class="tactics-pale" aria-hidden="true"></div>
 <svg class="tactics-road-light" viewBox="0 0 1536 1024" aria-hidden="true"><path d="M768 1010L768 842L768 630L768 482"/></svg>
 <div class="tactics-plaza-light" style="--x:50%;--y:47%" aria-hidden="true"></div>
 ${gates.map((s,i)=>`<span class="tactics-gate-light" data-gate-light="${s.id}" style="--x:${s.x}%;--y:${s.y}%" aria-hidden="true"></span>`).join('')}
 ${!celebrate&&showSpots?TACTICS_SPOTS.map(s=>`<button class="city-spot tactics-spot ${gates.some(g=>g.id===s.id)?'tactics-gate-hotspot':''}" data-spot="${s.id}" style="--x:${s.x}%;--y:${s.y}%" aria-label="查看${s.title}"><span aria-hidden="true">＋</span><span class="spot-name">${s.title}</span></button>`).join(''):''}
 ${celebrate?'<div class="tactics-fireflies" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>':''}
 </div></div>${celebrate?`<div class="tactics-traveler-note"><img src="assets/kitten-rowboat-concept.png" alt="${TEXT.travellerAlt}"><p><strong>${TEXT.traveller}</strong><span>${TEXT.readingOnly}</span></p></div>`:''}`;
}
