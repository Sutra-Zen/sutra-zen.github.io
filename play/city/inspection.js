// Deliberately independent of player store, metadata, shell and reader bridge.
// This route may inspect artwork; it has no reading or completion operation.
import {CITY_SPOTS} from '../visual-v2/data.js?v=summary-merge-1';
import {T} from './text.js?v=summary-merge-1';
const asset=path=>new URL(`../visual-v2/assets/${path}`,import.meta.url).href;
const positions={town:[8,8],eye:[50,7],ear:[88,24],nose:[87,69],tongue:[48,88],body:[13,69],mind:[12,24],guardian:[31,74],messengers:[78,58],plaza:[39,46],lord:[60,32],message:[64.6918,60],road:[65,94],dock:[14,94]};
const titles={guardian:'念-守門人',plaza:'地水火風四大廣場',messengers:'止・觀使者',message:'如實消息・涅槃'};
document.querySelector('#inspection-title').textContent=T.inspection;document.querySelector('#inspection-copy').textContent=T.inspectionCopy;
const button=document.querySelector('#inspection-labels');button.textContent=T.allLabels;
document.querySelector('#inspection-scene').innerHTML=`<div class="inspection-frame"><img class="inspection-art" src="${asset('city-scroll-audience-concept.png')}" width="1671" height="941" alt="六門城池、廣場北緣的鬍子城主與右前方持開卷的止觀使者"><svg class="inspection-hair" viewBox="0 0 1671 941" aria-hidden="true"><image href="${asset('city-lord-facial-hair-layer.png')}" x="778" y="350" width="128" height="85.333333333333"/></svg><img src="${asset('city-dharma-dock-concept.png')}" alt="法輪碼頭構圖層" style="position:absolute;left:2%;top:67%;width:25%;height:auto"><div class="inspection-labels">${[...CITY_SPOTS,{id:'dock',title:'法輪碼頭'}].map(s=>`<span class="inspection-label" style="--x:${positions[s.id][0]}%;--y:${positions[s.id][1]}%">${titles[s.id]||s.title}</span>`).join('')}</div></div>`;
button.onclick=()=>{const target=document.querySelector('.inspection-labels');target.hidden=!target.hidden;button.setAttribute('aria-pressed',String(!target.hidden));};
