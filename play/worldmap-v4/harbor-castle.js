import {gameIcon} from '../navigation.js';

// A compact UI badge beside the existing harbor, not another pasted island.
// The full illustrated city opens only after selecting this entry.
export const HARBOR_CASTLE_GEOMETRY=Object.freeze({
 worldWidth:1600,worldHeight:900,label:Object.freeze({x:240,y:345}),
 harbor:Object.freeze({x:128,y:423}),
});
export const HARBOR_CASTLE_CSS=new URL('./harbor-castle.css',import.meta.url).href;
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function renderHarborCastle({label='城池',ariaLabel='進入六門城池'}={}){
 const p=HARBOR_CASTLE_GEOMETRY.label;
 return `<div class="wm-harbor-castle" data-harbor-castle data-world-x="${p.x}" data-world-y="${p.y}" style="--harbor-entry-x:${p.x}px;--harbor-entry-y:${p.y}px"><button type="button" class="wm-harbor-castle__entry" data-wm-city-entry aria-label="${escape(ariaLabel)}">${gameIcon('city')}<span>${escape(label)} ›</span></button></div>`;
}
