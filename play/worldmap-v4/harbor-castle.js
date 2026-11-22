import {TACTICS_ART,renderCitySVGImages} from '../visual-v2/city-tactics.js';

// These are display coordinates in the existing 1600×900 world, not a new
// scripture/route node. The miniature uses the same castle and facial-hair art
// as the full city. Only its left half lies beyond the world's x=0 boundary.
const artWidth=360,artHeight=artWidth*TACTICS_ART.height/TACTICS_ART.width;
export const HARBOR_CASTLE_GEOMETRY=Object.freeze({
  worldWidth:1600,worldHeight:900,
  art:Object.freeze({x:-180,y:232,width:artWidth,height:artHeight}),
  visible:Object.freeze({x:0,y:232,width:180,height:artHeight}),
  entrance:Object.freeze({x:99,y:232+artHeight*.65}),
  harbor:Object.freeze({x:128,y:423}),
  label:Object.freeze({x:143,y:318}),
});
export const HARBOR_CASTLE_CSS=new URL('./harbor-castle.css',import.meta.url).href;
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

export function renderHarborCastle({label='城池',ariaLabel='進入六門城池',idPrefix='wm-harbor-castle'}={}){
  const g=HARBOR_CASTLE_GEOMETRY,id=String(idPrefix).replace(/[^a-zA-Z0-9_-]/g,''),entranceY=g.entrance.y-g.art.y;
  // Runtime SVG clipping retains the authored PNG bytes. This irregular edge
  // avoids placing a rectangular screenshot on the sea; x=0 is a hard world
  // boundary, while the right shore is the existing artwork's coast.
  return `<div class="wm-harbor-castle" data-harbor-castle data-world-x="0" data-world-y="${g.art.y}" data-castle-art-source="${TACTICS_ART.assetPath}" style="--harbor-castle-top:${g.art.y}px;--harbor-castle-width:${g.art.width}px;--harbor-castle-height:${g.art.height}px;--harbor-castle-label-x:${g.label.x}px;--harbor-castle-label-y:${g.label.y-g.art.y}px">
    <span class="wm-harbor-castle__window" aria-hidden="true"><svg class="wm-harbor-castle__art" viewBox="0 0 ${TACTICS_ART.width} ${TACTICS_ART.height}" width="${g.art.width}" height="${g.art.height}" focusable="false"><defs><clipPath id="${id}-coast"><path d="M180 120Q450 -5 835 0Q1250 0 1500 170Q1650 380 1600 640Q1450 910 900 935Q350 950 140 760Q10 520 90 300Z"/></clipPath></defs><g clip-path="url(#${id}-coast)">${renderCitySVGImages()}</g></svg></span>
    <svg class="wm-harbor-castle__approach" viewBox="0 0 220 230" aria-hidden="true"><path class="wm-harbor-castle__road-edge" d="M99 ${entranceY}Q109 154 116 173T128 191"/><path class="wm-harbor-castle__road" d="M99 ${entranceY}Q109 154 116 173T128 191"/></svg>
    <button type="button" class="wm-harbor-castle__entry" data-wm-city-entry aria-label="${escape(ariaLabel)}"><span class="wm-harbor-castle__label">${escape(label)}<span aria-hidden="true"> ›</span></span></button>
  </div>`;
}
