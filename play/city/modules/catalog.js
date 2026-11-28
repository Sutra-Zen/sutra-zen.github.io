import {CATALOG} from '../../collection/catalog.js?v=summary-merge-1';
import {routeOrder,rewardDefinitions} from '../../route/data.js?v=summary-merge-1';
import {MODULE_COPY,MODULE_SLOT_LABELS} from './text.js?v=summary-merge-1';

// Fixed world-space slots. x/y are image centres, widths/heights are world
// pixels; only module IDs are saved, never these coordinates or translated text.
export const WORLD = Object.freeze({width:1600,height:900,centre:Object.freeze({x:800,y:440})});
const slot=(id,x,y,width,assetKey,z=20,extra={})=>Object.freeze({id,x,y,width,assetKey,z,...extra,
  ...(MODULE_SLOT_LABELS[id]?{label:MODULE_SLOT_LABELS[id]}:{}),
  ...(extra.requires?{requires:Object.freeze([...extra.requires])}:{}),
});
export const BASE_PLINTH = Object.freeze({
  id:'four-elements-base',requiredBookId:'four-truths',free:true,
  slots:Object.freeze([
    slot('four-elements-garden',800,440,600,'base_garden',11,{height:390,actorId:'source_plaza'}),
    slot('city-lord',800,415,122,'city_lord',45,{height:150,actorId:'lord'}),
  ]),
});

const placements={
  truth_dock:{requires:[],slots:[slot('truth-dock',180,680,300,'truth_dock',20,{height:190})]},
  city_body:{requires:[],slots:[
    slot('city-outline',800,440,1040,'city_outline',10,{height:690}),
    slot('aggregates-corner',1045,490,240,'aggregates_corner',22,{height:170}),
  ]},
  six_gates:{requires:['city_body'],slots:[
    slot('gate-n',800,170,220,'gate_n',30,{height:180}),
    slot('gate-ne',1150,300,220,'gate_ne',31,{height:180}),
    slot('gate-se',1150,610,220,'gate_se',34,{height:180}),
    slot('gate-s',800,730,220,'gate_s',35,{height:180}),
    slot('gate-sw',450,610,220,'gate_sw',33,{height:180}),
    slot('gate-nw',450,300,220,'gate_nw',32,{height:180}),
  ]},
  conditions_wheel:{requires:['city_body'],slots:[slot('conditions-wheel',1280,430,220,'conditions_wheel',21,{height:250})]},
  noble_path:{requires:['city_body'],slots:[slot('noble-path',800,660,560,'noble_path',12,{height:235})]},
  confidence_harbor:{requires:[],slots:[slot('confidence-harbor',250,490,290,'confidence_harbor',19,{height:210})]},
  mindfulness_guard:{requires:['city_body','six_gates'],slots:[slot('mindfulness-guardian',515,570,120,'mindfulness_guard',46,{height:155,actorId:'guardian'})]},
  effort_garden:{requires:['city_body'],slots:[slot('effort-garden',1110,735,320,'effort_garden',23,{height:180})]},
  calm_insight_messengers:{requires:['city_body'],slots:[slot('calm-insight-messengers',930,510,205,'messengers',46,{height:170,actorId:'messengers'})]},
  endeavor_boat:{requires:[],slots:[slot('endeavor-boat',245,790,210,'endeavor_boat',28,{height:150})]},
  jhana_garden:{requires:['city_body'],slots:[slot('jhana-garden',1030,220,360,'jhana_garden',18,{height:205})]},
  faculties_links:{requires:['city_body'],slots:[
    slot('faculties-decoration',800,440,210,'faculties_links',24,{height:145}),
    slot('faculty-faith',250,490,210,'faculty_glow',37,{effect:'faith',requires:['confidence_harbor']}),
    slot('faculty-effort',1110,735,220,'faculty_glow',37,{effect:'effort',requires:['effort_garden']}),
    slot('faculty-mindfulness',515,570,155,'faculty_glow',47,{effect:'mindfulness',requires:['mindfulness_guard']}),
    slot('faculty-concentration',1030,220,260,'faculty_glow',37,{effect:'concentration',requires:['jhana_garden']}),
    slot('faculty-wisdom',180,680,205,'faculty_glow',37,{effect:'wisdom',requires:['truth_dock']}),
    slot('faculty-conditions-link',1280,430,180,'faculty_glow',37,{effect:'conditions',requires:['truth_dock','conditions_wheel']}),
  ]},
  awakening_companions:{requires:['city_body'],inventoryAssetKey:'awakening_companions',slots:[
    slot('awakening-mindfulness',515,570,155,'mindfulness_glow',48,{effect:'mindfulness',requires:['mindfulness_guard']}),
    slot('awakening-owl',620,250,108,'companion_owl',43,{height:120,actorId:'awakening-owl'}),
    slot('awakening-rabbit',620,655,108,'companion_rabbit',43,{height:120,actorId:'awakening-rabbit'}),
    slot('awakening-bird',795,245,98,'companion_bird',44,{height:100,actorId:'awakening-bird'}),
    slot('awakening-turtle',1000,400,108,'companion_turtle',43,{height:110,actorId:'awakening-turtle'}),
    slot('awakening-lotus',1000,600,108,'companion_lotus',43,{height:110,actorId:'awakening-lotus'}),
    slot('awakening-deer',800,630,108,'companion_deer',43,{height:120,actorId:'awakening-deer'}),
  ]},
  fruition_guide:{requires:[],slots:[slot('fruition-guide',1360,205,265,'fruition_guide',24,{height:200})]},
};

const bookTitles=new Map(CATALOG.map(book=>[book.id,book.title]));
const rewardByBook=new Map(rewardDefinitions.map(reward=>[reward.bookId,reward]));
export const MODULES=Object.freeze(routeOrder.map((bookId,index)=>{
  const reward=rewardByBook.get(bookId),p=placements[reward.id],copy=MODULE_COPY[reward.id];
  return Object.freeze({id:reward.id,bookId,bookTitle:bookTitles.get(bookId),order:index+1,title:copy.title,description:copy.description,
    type:reward.type,requiredBookIds:Object.freeze([...reward.requiredBookIds]),
    requires:Object.freeze([...p.requires]),slots:Object.freeze([...p.slots]),
    placementAnchor:Object.freeze({x:p.slots[0].x,y:p.slots[0].y}),
    inventoryAssetKey:p.inventoryAssetKey||p.slots[0].assetKey,
  });
}));
export const MODULE_IDS=Object.freeze(MODULES.map(module=>module.id));
export const MODULE_BY_ID=Object.freeze(Object.fromEntries(MODULES.map(module=>[module.id,module])));
export const THOUGHT_IDS=Object.freeze([
  'city-lord-introduction','mindfulness-guardian-introduction','calm-insight-messengers-arrival',
  'doubt-at-city','mara-at-city','six-gates-unwatched','desire-at-city','anger-at-city',
  'sloth-at-city','restlessness-at-city',
  'awakening-owl-at-city','awakening-rabbit-at-city','awakening-bird-at-city',
  'awakening-turtle-at-city','awakening-lotus-at-city','awakening-deer-at-city',
]);
