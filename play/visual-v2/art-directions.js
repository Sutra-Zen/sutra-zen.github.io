// Image-space display calibration only. These positions are not doctrinal links.
export const MAP_STYLES = {
 watercolor: {label:'原水彩',image:'assets/network-sea-concept.png',aspect:'18 / 13',alt:'原水彩海圖，分層小島及連續主題山陸地',points:{}},
 terrain: {label:'塔防地景',image:'assets/network-terrain-concept.png',aspect:'1672 / 941',alt:'塔防地景畫風的群島與山群，翠綠台地、瀑布與沿岸土路',points:{
  'road-overview':[9,36],
  'roots-powers-overview':[19,18],'faith-root-power':[31.5,18],'mindfulness-root-power':[44.7,18],'effort-root-power':[58,18],'concentration-root-power':[71,18],'wisdom-root-power':[85,18],
  'awakening-overview':[19,32],'mindfulness-awakening':[44.7,32],'effort-awakening':[58,32],'concentration-awakening-group':[71,32],'discrimination-awakening':[85,32],
  'eightfold-overview':[19,46],'right-mindfulness':[44.7,46],'eightfold-action-group':[58,46],'right-concentration':[71,46],'right-view-intention':[85,46],
  'four-purities':[30,65],'six-recollections':[30,76],'four-mindfulness':[43,66],'four-inversions':[44,76],
  'right-effort':[55,66],'ten-wholesome':[55,79],
  'anapana':[65.5,60],'iddhipada':[72.5,65],'four-jhanas':[68,74],
  'four-truths':[82,74],'five-aggregates':[82,55],'six-senses':[92,55],'twelve-links':[92,66],'four-fruits':[92,79],
  'eightfold-overview-four-truths-port':[80.8,86]
 }},
 world: {label:'奇幻世界',image:'assets/network-world-concept.png',aspect:'1448 / 1086',alt:'奇幻世界地圖畫風，深藍海洋、雪峰森林與有橋梁的連續山地',points:{
  'road-overview':[9,32],
  'roots-powers-overview':[19,17.5],'faith-root-power':[31.5,17.5],'mindfulness-root-power':[44.7,17.5],'effort-root-power':[58,17.5],'concentration-root-power':[71.5,17.5],'wisdom-root-power':[85.5,17.5],
  'awakening-overview':[19,29.5],'mindfulness-awakening':[44.7,29.5],'effort-awakening':[58,29.5],'concentration-awakening-group':[71.5,29.5],'discrimination-awakening':[85.5,29.5],
  'eightfold-overview':[19,42.5],'right-mindfulness':[44.7,42.5],'eightfold-action-group':[58,42.5],'right-concentration':[71.5,42.5],'right-view-intention':[85.5,42.5],
  'four-purities':[30,61],'six-recollections':[30,71],'four-mindfulness':[43,62],'four-inversions':[44,74],
  'right-effort':[55,64],'ten-wholesome':[55,79],
  'anapana':[65.5,58],'iddhipada':[74,64],'four-jhanas':[68,72],
  'four-truths':[82,72],'five-aggregates':[82,55],'six-senses':[92,55],'twelve-links':[92,66],'four-fruits':[92,79],
  'eightfold-overview-four-truths-port':[80.8,85]
 }}
};
export function terrainReturnPath(style,p,q){
 if(style==='watercolor')return `M${p.x} ${p.y}C${p.x+70} ${p.y-15} 1640 1090 1590 1058C1300 1082 1100 1050 900 1065S420 1050 220 1040C110 1030 100 920 125 835S92 650 ${q.x} ${q.y}`;
 // The painted dirt road and its approach are calibrated separately per full-frame art.
 if(style==='terrain')return `M${p.x} ${p.y}C1540 1092 1570 1014 1476 1014C1300 1040 1130 1020 990 1040S520 1035 230 1010C135 990 140 855 150 735S128 570 ${q.x} ${q.y}`;
 return `M${p.x} ${p.y}C1512 1092 1530 1001 1476 975C1260 1027 1116 949 900 975S450 1014 198 923C144 871 180 754 162 663S144 507 ${q.x} ${q.y}`;
}
