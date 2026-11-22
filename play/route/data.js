// Author handoff: 2026-11-22-r3 + 2026-11-22-map-v4.
// Recommendation order is teaching design, never a prerequisite for reading.
export const ROUTE_VERSION = '2026-11-22-r3';
export const MAP_VERSION = '2026-11-22-map-v4';
export const routeOrder = Object.freeze([
  'four-truths', 'five-aggregates', 'six-senses', 'twelve-links',
  'eightfold-path', 'four-purities-six-recollections', 'mindfulness',
  'right-effort', 'anapana', 'iddhipada', 'four-jhanas',
  'five-roots-powers', 'seven-factors', 'four-fruits-ten-fetters',
]);
export const FINAL_BOOK_ID = 'four-fruits-ten-fetters';
export const FIRST_THIRTEEN = Object.freeze(routeOrder.filter(id => id !== FINAL_BOOK_ID));
export const canonicalCorrespondences = Object.freeze({
  city_body: '四大所成、會變壞的色身',
  four_elements_plaza: '地、水、火、風四大',
  six_gates: '眼、耳、鼻、舌、身、意六內處',
  mindfulness_guard: '念',
  city_lord: '識',
  calm_insight_messengers: '止、觀',
  truthful_message: '涅槃',
  noble_path: '八正道',
});
const reward = (id, bookId, title, type, requiredBookIds, details) => Object.freeze({
  id, bookId, title, type, requiredBookIds: Object.freeze(requiredBookIds), ...details,
});
// earned: own book completed; available: city-placement requirements complete.
// World landmarks are independently activated by their own book, below.
export const rewardDefinitions = Object.freeze([
  reward('truth_dock', 'four-truths', '法輪碼頭', 'extended', ['four-truths'], { canonicalElements: [], extendedElements: ['法輪碼頭與遠處城影'] }),
  reward('city_body', 'five-aggregates', '城體、四大廣場與城主', 'mixed', ['five-aggregates'], { canonicalElements: ['city_body', 'four_elements_plaza', 'city_lord'], extendedElements: ['城中日常經驗的觀察視角'] }),
  reward('six_gates', 'six-senses', '六道城門', 'canonical', ['five-aggregates', 'six-senses'], { canonicalElements: ['six_gates'], extendedElements: ['六處的感官景物演出'] }),
  reward('conditions_wheel', 'twelve-links', '城側緣起之輪', 'extended', ['five-aggregates', 'twelve-links'], { canonicalElements: [], extendedElements: ['緣起輪庭與條件變化場景'] }),
  reward('noble_path', 'eightfold-path', '道路與善行生活場景', 'mixed', ['five-aggregates', 'eightfold-path'], { canonicalElements: ['noble_path'], extendedElements: ['八支提示及十善生活場景'] }),
  reward('confidence_harbor', 'four-purities-six-recollections', '信心港灣與六念燈景', 'extended', ['four-purities-six-recollections'], { canonicalElements: [], extendedElements: ['港灣及六念燈景'], feedbackLabel: '場景開放' }),
  reward('mindfulness_guard', 'mindfulness', '念守門人', 'mixed', ['five-aggregates', 'six-senses', 'mindfulness'], { canonicalElements: ['mindfulness_guard'], extendedElements: ['身、受、心、法四種觀察及四顛倒辨識'] }),
  reward('effort_garden', 'right-effort', '城中善巧照料花園', 'extended', ['five-aggregates', 'right-effort'], { canonicalElements: [], extendedElements: ['預防、拔草、播種與照料活動'] }),
  reward('calm_insight_messengers', 'anapana', '止觀雙使與安靜呼吸場景', 'mixed', ['five-aggregates', 'anapana'], { canonicalElements: ['calm_insight_messengers'], extendedElements: ['呼吸竹林與相伴溪流'] }),
  reward('endeavor_boat', 'iddhipada', '調心小舟', 'extended', ['iddhipada'], { canonicalElements: [], extendedElements: ['欲、勤、心、觀的小舟提示'] }),
  reward('jhana_garden', 'four-jhanas', '四禪靜水庭園', 'extended', ['five-aggregates', 'four-jhanas'], { canonicalElements: [], extendedElements: ['澡粉團、湧泉池、蓮花池與白布覆身的既有譬喻'], feedbackLabel: '讀本完成' }),
  reward('faculties_links', 'five-roots-powers', '五根五力區域呼應', 'extended', ['five-aggregates', 'five-roots-powers'], { canonicalElements: [], extendedElements: ['既有信、勤、念、定、慧區域逐一聯動'], sourceReference: '《雜阿含經》646；緣起輪回顧為教材延伸' }),
  reward('awakening_companions', 'seven-factors', '七覺支夥伴與調整用功', 'extended', ['five-aggregates', 'seven-factors'], { canonicalElements: [], extendedElements: ['念燈與六位既有夥伴；昏沉及浮動時的調整'] }),
  reward('fruition_guide', FINAL_BOOK_ID, '四向四果與十結導覽', 'extended', [FINAL_BOOK_ID], { canonicalElements: [], extendedElements: ['河岸、花與繫縛的既有繪本意象'], feedbackLabel: '導覽開放' }),
]);
const combination = (id, requiredBookIds, title) => Object.freeze({ id, title, requiredBookIds: Object.freeze(requiredBookIds) });
export const combinationScenes = Object.freeze([
  combination('city_experience', ['five-aggregates', 'six-senses'], '五陰與六處的城中經驗'),
  combination('city_conditions', ['five-aggregates', 'six-senses', 'twelve-links'], '城中經驗與條件關係'),
  combination('city_allegory', ['five-aggregates', 'six-senses', 'eightfold-path', 'mindfulness', 'anapana'], '完整六門城喻'),
  combination('faculties_network', ['five-aggregates', 'five-roots-powers', 'four-purities-six-recollections', 'right-effort', 'mindfulness', 'four-jhanas', 'four-truths', 'twelve-links'], '五根五力的五區聯動'),
  combination('final_chapter_reveal', [...FIRST_THIRTEEN], '末關主線揭曉'),
  combination('ending_release', [...routeOrder], '終章條件齊備'),
  combination('garden_irrigation', ['eightfold-path', 'right-effort'], '十善業道湖與四正勤花田灌溉'),
]);
export const facultiesSources = Object.freeze({
  faith: { bookId: 'four-purities-six-recollections', title: '信' },
  effort: { bookId: 'right-effort', title: '精進' },
  mindfulness: { bookId: 'mindfulness', title: '念' },
  concentration: { bookId: 'four-jhanas', title: '定' },
  wisdom: { bookId: 'four-truths', title: '慧' },
});
// These IDs map geographical views to the same authoritative book completion.
export const landmarkBooks = Object.freeze({
  truth_wheel_ruin: 'four-truths', aggregates_lake: 'five-aggregates',
  senses_lake: 'six-senses', sense_landings: 'six-senses',
  dependent_origination_court: 'twelve-links',
  path_station: 'eightfold-path', path_road: 'eightfold-path',
  path_bridge_wisdom: 'eightfold-path', path_bridge_concentration: 'eightfold-path',
  path_bridge_effort_ethics: 'eightfold-path', path_bridge_mindfulness: 'eightfold-path',
  path_stream: 'eightfold-path', wholesome_lake: 'eightfold-path',
  confidence_lagoon: 'four-purities-six-recollections', recollection_lighthouse: 'four-purities-six-recollections',
  mindfulness_pavilion: 'mindfulness', inversion_grove: 'mindfulness',
  effort_garden: 'right-effort', breathing_grove: 'anapana', calm_insight_streams: 'anapana',
  endeavor_boathouse: 'iddhipada', jhana_water_garden: 'four-jhanas',
  faculties_overview: 'five-roots-powers', awakening_overview: 'seven-factors', fruition_valley: FINAL_BOOK_ID,
});
export const endingDefinition = Object.freeze({
  id: 'ending_release', title: '回到城中，學會放下', implemented: false,
  countsAsBook: false, requiredBookIds: routeOrder,
  quote: '如實正觀世間集者，則不生世間無見；如實正觀世間滅，則不生世間有見。',
  quoteSource: '《雜阿含經》第262經',
  direction: '回看身心經驗與執取；放下不是消滅自己或摧毀世界，城與六門仍繼續運作。',
});
