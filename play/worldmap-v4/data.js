import {NODES,EDGES,GROUPS} from '../visual-v2/network-data.js?v=summary-merge-1';
export {NODES,EDGES,GROUPS};
export const WORLD=Object.freeze({width:1600,height:900});
export const COLUMNS=Object.freeze({faith:432,mindfulness:672,effort:912,concentration:1152,wisdom:1392});
const l=(id,bookId,conceptId,x,y,options={})=>Object.freeze({id,bookId,conceptId,x,y,...options});
export const LANDMARKS=Object.freeze([
 l('harbor',null,'road-overview',128,423,{type:'harbor',alwaysClear:true}),
 l('awakening_overview','seven-factors','awakening-overview',168,108,{type:'scroll',overview:true}),
 l('faculties_overview','five-roots-powers','roots-powers-overview',168,243,{type:'scroll',overview:true}),
 ...[['mindfulness-awakening','mindfulness'],['effort-awakening','effort'],['concentration-awakening-group','concentration'],['discrimination-awakening','wisdom']].map(([id,family])=>l(id,'seven-factors',id,COLUMNS[family],108,{type:'island',family,row:'awakening'})),
 ...[['faith-root-power','faith'],['mindfulness-root-power','mindfulness'],['effort-root-power','effort'],['concentration-root-power','concentration'],['wisdom-root-power','wisdom']].map(([id,family])=>l(id,'five-roots-powers',id,COLUMNS[family],243,{type:'island',family,row:'faculties'})),
 l('recollection_lighthouse','four-purities-six-recollections','six-recollections',432,405,{family:'faith'}),
 l('confidence_lagoon','four-purities-six-recollections','four-purities',432,540,{family:'faith'}),
 l('mindfulness_pavilion','mindfulness','four-mindfulness',672,423,{family:'mindfulness'}),
 l('inversion_grove','mindfulness','four-inversions',672,585,{family:'mindfulness'}),
 l('effort_garden','right-effort','right-effort',912,486,{family:'effort'}),
 l('wholesome_lake','eightfold-path','ten-wholesome',912,630,{family:'effort'}),
 l('breathing_grove','anapana','anapana',1152,405,{family:'concentration'}),
 l('endeavor_boathouse','iddhipada','iddhipada',1152,531,{family:'concentration'}),
 l('jhana_water_garden','four-jhanas','four-jhanas',1152,630,{family:'concentration'}),
 l('aggregates_lake','five-aggregates','five-aggregates',1312,414,{family:'wisdom'}),
 l('senses_lake','six-senses','six-senses',1496,414,{family:'wisdom'}),
 l('dependent_origination_court','twelve-links','twelve-links',1376,504,{family:'wisdom'}),
 l('fruition_valley','four-fruits-ten-fetters','four-fruits',1512,585,{family:'wisdom'}),
 l('truth_wheel_ruin','four-truths','four-truths',1312,630,{family:'wisdom'}),
 l('path_station','eightfold-path','eightfold-overview',1480,693,{type:'station',family:'wisdom',alwaysAccessible:true}),
 l('path_road','eightfold-path','eightfold-overview',368,760,{type:'scroll',alwaysClear:true}),
 l('path_bridge_mindfulness','eightfold-path','right-mindfulness',672,810,{type:'bridge',family:'mindfulness'}),
 l('path_bridge_effort_ethics','eightfold-path','eightfold-action-group',912,810,{type:'bridge',family:'effort'}),
 l('path_bridge_concentration','eightfold-path','right-concentration',1152,810,{type:'bridge',family:'concentration'}),
 l('path_bridge_wisdom','eightfold-path','right-view-intention',1392,810,{type:'bridge',family:'wisdom'}),
]);
// Secondary scenic elements share a book and have no added source relation.
export const SECONDARY=Object.freeze([
 l('sense_landings','six-senses','six-senses',1520,450,{label:false}),
 l('calm_insight_streams','anapana','anapana',1168,441,{label:false}),
 l('path_stream','eightfold-path','ten-wholesome',1008,585,{label:false}),
]);
export const LANDSCAPE_GROUPS=Object.freeze(Object.entries(COLUMNS).map(([family,x])=>({id:`${family}-landscape`,family,x,y:540})));
export const MEMBERS=Object.freeze([
 ...['joy','tranquility','concentration','equanimity'].map(key=>({id:`concentration-awakening-group--${key}`,key,sourceParentId:'concentration-awakening-group',provenance:'member-of-source-aggregate'})),
 ...['effort','speech','action','livelihood'].map(key=>({id:`eightfold-action-group--${key}`,key,sourceParentId:'eightfold-action-group',provenance:'member-of-source-aggregate'})),
 ...['view','intention'].map(key=>({id:`right-view-intention--${key}`,key,sourceParentId:'right-view-intention',provenance:'member-of-source-aggregate'})),
 ...['faith','mindfulness','effort','concentration','wisdom'].flatMap(family=>['root','power'].map(key=>({id:`${family}-root-power--${key}`,key,sourceParentId:`${family}-root-power`,provenance:'member-of-source-aggregate'}))),
]);
export const GEOGRAPHIC_ROAD='M1480 693C1580 700 1536 770 1440 810L672 810C475 830 185 825 128 770S45 630 80 540L128 423';
// Author-requested geographic access, separate from the original 46 relations.
// Four Jhanas reaches the harbor through the existing Iddhipada group.
export const MAP_CONNECTIONS=Object.freeze([
 Object.freeze({id:'harbor-concentration-access',kind:'author-geographic-access',relation:false,
  landmarkIds:Object.freeze(['jhana_water_garden','endeavor_boathouse','harbor']),
  d:'M1152 630L1152 531C950 520 500 504 200 504Q128 504 128 423'})
]);
export function conceptAnchor(id){
 const found=LANDMARKS.find(l=>l.conceptId===id);if(found)return {x:found.x,y:found.y};
 if(id==='related-overview')return {x:240,y:540};
 return null;
}
export function sourceGroupAnchor(id){
 const g=GROUPS.find(g=>g.id===id);return g?{x:COLUMNS[g.family],y:540}:null;
}
export const PRIMARY_BOOK_LANDMARK=Object.freeze({
 'four-truths':'truth_wheel_ruin','five-aggregates':'aggregates_lake','six-senses':'senses_lake','twelve-links':'dependent_origination_court','eightfold-path':'path_station','four-purities-six-recollections':'confidence_lagoon','mindfulness':'mindfulness_pavilion','right-effort':'effort_garden','anapana':'breathing_grove','iddhipada':'endeavor_boathouse','four-jhanas':'jhana_water_garden','five-roots-powers':'faculties_overview','seven-factors':'awakening_overview','four-fruits-ten-fetters':'fruition_valley'
});
