// A presentation-only reading geography on the existing 1600 × 900 painting.
// The five districts share their coast and divider curves exactly. They do not
// define book eligibility, scripture relations, fog, or new travel connections.
const point = (x, y) => Object.freeze({x, y});
const curve = (from, segments) => Object.freeze({
 from: Object.freeze(from),
 segments: Object.freeze(segments.map(segment => Object.freeze(segment))),
});
const start = c => 'M' + c.from.join(' ');
const commands = c => c.segments.map(s => 'C' + s.join(' ')).join(' ');
function reverse(c) {
 const ends = [c.from, ...c.segments.map(s => s.slice(4))];
 return curve(ends.at(-1), c.segments.map((s, i) => [
  s[2], s[3], s[0], s[1], ...ends[i],
 ]).reverse());
}
const join = curves => start(curves[0]) + ' ' + curves.map(commands).join(' ') + ' Z';

// North shore: tree crowns and the low mountain ridge, not the offshore islands.
const north = [
 curve([278,354], [
  [288,342,301,350,314,337], [330,326,345,337,360,328],
  [377,318,395,334,412,327], [432,316,452,332,472,326],
  [493,319,514,340,535,344], [540,346,546,347,550,350],
 ]),
 curve([550,350], [
  [569,341,587,352,606,342], [625,331,644,341,662,331],
  [679,325,692,334,705,327], [724,315,741,328,756,320],
  [771,312,784,322,790,333],
 ]),
 curve([790,333], [
  [808,321,828,329,844,321], [858,315,876,327,890,316],
  [903,306,913,318,926,310], [936,301,945,316,957,312],
  [967,305,976,300,984,309], [997,301,1008,291,1024,308],
 ]),
 curve([1024,308], [
  [1040,321,1050,328,1067,332], [1076,328,1079,322,1086,329],
  [1095,339,1103,343,1117,340], [1131,334,1143,345,1156,341],
  [1173,335,1189,351,1203,343], [1217,337,1234,343,1244,350],
 ]),
 curve([1244,350], [
  [1261,338,1276,347,1292,342], [1308,335,1323,344,1341,336],
  [1358,329,1378,344,1394,340], [1411,331,1427,349,1445,342],
  [1468,333,1485,351,1505,351], [1525,345,1542,361,1556,363],
  [1564,361,1570,369,1572,375],
 ]),
];
// South shore stops above the Eightfold Path's separate road peninsula.
const south = [
 curve([310,650], [
  [335,663,357,651,378,662], [401,677,428,668,451,676],
  [482,684,507,665,531,674], [541,679,548,673,555,671],
 ]),
 curve([555,671], [
  [575,682,593,669,611,680], [634,695,656,677,679,688],
  [701,700,720,681,741,690], [758,696,778,680,790,683],
 ]),
 curve([790,683], [
  [811,691,832,679,852,687], [875,697,893,681,912,688],
  [938,698,957,677,978,685], [990,691,1000,681,1008,682],
 ]),
 curve([1008,682], [
  [1029,689,1042,676,1058,685], [1079,696,1100,679,1117,686],
  [1143,698,1166,679,1187,690], [1204,698,1222,681,1243,687],
 ]),
 curve([1243,687], [
  [1262,698,1284,690,1305,699], [1323,707,1341,695,1359,698],
  [1381,707,1404,694,1426,699], [1454,708,1471,689,1489,696],
  [1507,706,1524,692,1539,693],
 ]),
];
const west = curve([278,354], [
 [265,366,256,384,250,402], [236,420,249,443,244,460],
 [234,478,248,492,242,509], [225,523,236,545,226,559],
 [225,578,252,587,251,603], [257,626,284,636,310,650],
]);
const east = curve([1572,375], [
 [1585,388,1579,405,1591,422], [1598,441,1584,462,1590,481],
 [1598,504,1586,520,1594,542], [1598,562,1587,578,1592,597],
 [1598,616,1581,631,1589,650], [1595,667,1577,679,1574,687],
 [1562,696,1551,695,1539,693],
]);
// Interior borders follow woodland breaks, pond banks and the garden waterfall.
// Each begins on the north shore and ends on the south shore: no open provinces.
const dividers = [
 curve([550,350], [
  [562,382,539,412,550,445], [560,471,582,490,567,525],
  [550,557,552,583,565,610], [576,634,553,652,555,671],
 ]),
 curve([790,333], [
  [781,369,799,399,786,426], [775,450,790,478,783,507],
  [775,545,793,566,779,593], [771,623,789,653,790,683],
 ]),
 curve([1024,308], [
  [1032,353,1023,393,1018,432], [1015,471,1045,477,1030,510],
  [1018,539,1021,560,1002,582], [988,614,1013,641,1008,682],
 ]),
 curve([1244,350], [
  [1232,385,1231,418,1216,447], [1208,476,1210,499,1223,524],
  [1238,550,1220,571,1233,594], [1246,617,1230,646,1243,687],
 ]),
];

export const CITY_MAINLAND_OUTLINE = join([
 ...north, east, ...south.map(reverse).reverse(), reverse(west),
]);
const districts = [
 ['faith', '#edce8f', point(432,359)],
 ['mindfulness', '#7ed0b3', point(672,358)],
 ['effort', '#f1bd8e', point(912,352)],
 ['concentration', '#9dc9eb', point(1152,357)],
 ['wisdom', '#c8a3de', point(1392,361)],
];
export const CITY_REGIONS = Object.freeze(districts.map(([family,tint,label],i) => {
 const edges = [north[i], i === 4 ? east : dividers[i], reverse(south[i]),
  i === 0 ? reverse(west) : reverse(dividers[i-1])];
 return Object.freeze({id:family, family, tint, label, path:join(edges)});
}));
const escape = value => String(value ?? '').replace(/[&<>"']/g, char => ({
 '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;',
}[char]));
function boundary(c, id) {
 const d = start(c) + ' ' + commands(c);
 return '<g class="wm-city-boundary" data-city-divider="' + id + '">' +
  '<path class="wm-city-boundary__rim" d="' + d + '"/>' +
  '<path class="wm-city-boundary__line" d="' + d + '"/></g>';
}
export function renderCityRegions({label='',names={}}={}) {
 const fills = CITY_REGIONS.map(region =>
  '<path class="wm-city-region" data-city-region="' + region.family +
  '" style="--wm-city-color:' + region.tint + '" d="' + region.path + '"/>').join('');
 const borders = '<g class="wm-city-boundary" data-city-mainland-outline>' +
  '<path class="wm-city-boundary__rim" d="' + CITY_MAINLAND_OUTLINE + '"/>' +
  '<path class="wm-city-boundary__line" d="' + CITY_MAINLAND_OUTLINE + '"/></g>' +
  dividers.map((line,i) => boundary(line,districts[i][0] + '-' + districts[i+1][0])).join('');
 const titles = CITY_REGIONS.filter(region => names[region.family]).map(region =>
  '<span class="wm-city-region-label" data-city-name="' + region.family +
  '" data-world-x="' + region.label.x + '" data-world-y="' + region.label.y +
  '" style="--wm-city-x:' + region.label.x + 'px;--wm-city-y:' + region.label.y + 'px">' +
  escape(names[region.family]) + '</span>').join('');
 return '<div class="wm-city-regions" data-city-regions role="group"' +
  (label ? ' aria-label="' + escape(label) + '"' : '') + '>' +
  '<svg class="wm-city-regions__map" viewBox="0 0 1600 900" width="1600" height="900" aria-hidden="true">' +
  '<defs><clipPath id="wm-city-mainland-clip" clipPathUnits="userSpaceOnUse"><path d="' +
  CITY_MAINLAND_OUTLINE + '"/></clipPath></defs>' +
  '<g clip-path="url(#wm-city-mainland-clip)">' + fills + borders + '</g></svg>' +
  titles + '</div>';
}
