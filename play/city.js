import { CITY_TEXT as T, CITY_MAPPING } from './source-data.js';
let serial = 0;
const points = [[500,176],[740,292],[740,505],[500,620],[260,505],[260,292]];
function gate([x,y],i) {
  return `<g class="sz-city__gate" transform="translate(${x} ${y})"><circle class="sz-city__halo" r="40"/><path class="sz-city__tower" d="M-25 27V-28H-18V-39H-6V-28H6V-39H18V-28H25V27Z"/><path class="sz-city__door" d="M-12 27V3A12 12 0 0 1 12 3V27"/><text class="sz-city__gate-label" x="0" y="-52">${T.gates[i]}</text><circle class="sz-city__lamp" cx="-30" cy="0" r="5"/><circle class="sz-city__lamp" cx="30" cy="0" r="5"/></g>`;
}
function messenger(x,y,label) {
 return `<g transform="translate(${x} ${y})"><circle class="sz-city__face" cy="-18" r="11"/><path class="sz-city__messenger" d="M-15 22L-11-7Q0-15 11-7L15 22Z"/><path d="M-6 23L-13 34M6 23L15 31" class="sz-city__limb"/><text class="sz-city__person-label" y="13">${label}</text></g>`;
}
export function renderCity(stage=0,{blueprint=false}={}) {
 const level=Math.max(0,Math.min(3,Math.trunc(Number(stage)||0))); const full=blueprint?3:level; const id=`sz-city-${++serial}`;
 return `<figure class="sz-city sz-city--stage-${full}${blueprint?' sz-city--blueprint':''}" data-city-stage="${level}">
 <figcaption class="sz-city__heading"><strong>${blueprint?T.title:T.stages[level]}</strong><span>${blueprint?T.prototype:T.stageNotes[level]}</span></figcaption>
 <div class="sz-city__scroll" tabindex="${blueprint?'0':'-1'}" ${blueprint?`aria-label="${T.scroll}"`:''}>
 <svg class="sz-city__drawing" viewBox="0 0 1000 780" role="img" aria-labelledby="${id}-title ${id}-desc">
 <title id="${id}-title">${T.title}：${T.stages[full]}</title><desc id="${id}-desc">${T.description}${T.progressOnly}</desc>
 <defs><radialGradient id="${id}-paper"><stop stop-color="#fffbed"/><stop offset="1" stop-color="#e9f0db"/></radialGradient><linearGradient id="${id}-river" x2="1" y2="1"><stop stop-color="#d7eeea"/><stop offset="1" stop-color="#a9d5d7"/></linearGradient></defs>
 <rect width="1000" height="780" rx="32" fill="url(#${id}-paper)"/>
 <path class="sz-city__water" d="M0 610Q140 510 170 340T320 80M1000 635Q860 580 850 400T680 55" fill="none" stroke="url(#${id}-river)" stroke-width="66"/>
 <g class="sz-city__land"><path d="M134 435Q122 214 328 113Q520 30 755 165Q924 262 863 532Q806 704 567 714Q312 737 189 588Z"/><g class="sz-city__trees"><path d="M145 246l-37 71h74Z M848 220l-37 71h74Z M182 568l-33 61h66Z M826 570l-35 67h70Z"/><path d="M140 343l-30 55h60Z M872 450l-31 58h62Z"/></g></g>
 <g class="sz-city__roads">${points.map(([x,y])=>`<path d="M500 390L${x} ${y}"/>`).join('')}<path d="M500 620Q490 710 330 750"/></g>
 <path class="sz-city__wall" d="M500 176L740 292V505L500 620L260 505V292Z"/>
 <path class="sz-city__inner-wall" d="M500 204L715 307V490L500 593L285 490V307Z"/>
 <g class="sz-city__plaza"><circle cx="500" cy="401" r="101"/><path d="M500 308V496M408 402H592"/>
 <text x="467" y="376">${T.elements[0]}</text><text x="534" y="376">${T.elements[1]}</text><text x="467" y="449">${T.elements[2]}</text><text x="534" y="449">${T.elements[3]}</text><text class="sz-city__plaza-name" x="500" y="532">${T.plaza}</text></g>
 <g class="sz-city__lord" transform="translate(500 267)"><path d="M-46 31V-18H46V31Z"/><path d="M-57-18L0-53L57-18Z"/><text y="13">識</text></g>
 ${points.map(gate).join('')}
 <g class="sz-city__people"><g transform="translate(321 308)"><circle class="sz-city__face" cy="-18" r="13"/><path class="sz-city__guardian" d="M-18 26L-13-5Q0-17 13-5L18 26Z"/><text class="sz-city__person-label" y="13">念</text></g>${messenger(602,379,'止')}${messenger(646,402,'觀')}</g>
 <g class="sz-city__labels"><text x="500" y="70">${T.body}</text><path d="M405 80L335 242"/>
 <text x="789" y="199">${T.lord}</text><path d="M742 208L553 261"/>
 <text x="115" y="390">${T.guardian}</text><path d="M190 385L308 331"/>
 <text x="832" y="380">${T.messengers}</text><path d="M752 387L663 398"/>
 <g class="sz-city__message"><rect x="585" y="556" width="236" height="47" rx="13"/><text x="703" y="587">${T.message}</text></g>
 <text x="701" y="710">${T.road}</text><path d="M598 702L483 665"/>
 </g></svg></div>
 ${blueprint?`<p class="sz-city__scroll-hint">${T.scroll}</p><dl class="sz-city__mapping">${CITY_MAPPING.map(([a,b])=>`<div><dt>${a}</dt><dd>${b}</dd></div>`).join('')}</dl>`:''}
 <p class="sz-city__caption">${T.caption}</p><p class="sz-city__disclaimer">${T.progressOnly}</p>${blueprint?`<p class="sz-city__disclaimer">${T.consciousness}</p>`:''}
 </figure>`;
}
