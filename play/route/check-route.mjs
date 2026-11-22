// Targeted route/save risks; no retelling or re-walking the 1,192 reader steps.
import assert from 'node:assert/strict';
import { routeStatus, deriveCityState, routeOrder, routeBooks, recommendNextBook, sceneAvailability, canonicalCorrespondences } from './selectors.js';
import { createRouteMetadataStore, ROUTE_METADATA_KEY } from './metadata.js';

const expected = [
  'four-truths','five-aggregates','six-senses','twelve-links','eightfold-path',
  'four-purities-six-recollections','mindfulness','right-effort','anapana','iddhipada',
  'four-jhanas','five-roots-powers','seven-factors','four-fruits-ten-fetters',
];
const final = 'four-fruits-ten-fetters';
const normative = {
  city_experience: ['five-aggregates','six-senses'],
  city_conditions: ['five-aggregates','six-senses','twelve-links'],
  city_allegory: ['five-aggregates','six-senses','eightfold-path','mindfulness','anapana'],
  faculties_network: ['five-aggregates','five-roots-powers','four-purities-six-recollections','right-effort','mindfulness','four-jhanas','four-truths','twelve-links'],
  final_chapter_reveal: expected.filter(id => id !== final),
  ending_release: expected,
  garden_irrigation: ['eightfold-path','right-effort'],
};
const checks = [];
function check(name, body) { body(); checks.push(name); }
check('r3 order uses permanent IDs; catalog shelf order is independent', () => {
  assert.deepEqual([...routeOrder], expected);
  assert.deepEqual(routeBooks.map(book => book.id), expected);
  assert.equal(new Set(routeOrder).size, 14);
});
check('no completion is inferred from all bookmarks or animation metadata', () => {
  const positions = Object.fromEntries(routeBooks.map(book => [book.id, book.totalSteps - 1]));
  const s = routeStatus([], positions, { playedAnimationIds: Object.keys(normative) });
  assert.equal(s.count, 0); assert.equal(s.total, 14); assert.equal(s.nextBookId, 'four-truths');
  assert.equal(s.endingAvailable, false); assert(s.city.rewards.every(reward => !reward.earned));
  assert(s.books.every(book => book.canRead));
});
check('opening / knowing / completing final reveals name but does not fill previous books', () => {
  assert.equal(routeStatus([]).finalChapterRevealed, false);
  assert.equal(routeStatus([]).books.at(-1).mainlineTitle, '尚未揭曉的旅程');
  for (const state of [routeStatus([], { [final]:0 }), routeStatus([], {}, { knownBookIds:[final] }), routeStatus([], {}, { openedBookIds:[final] })]) {
    assert.equal(state.finalChapterRevealed, true); assert.equal(state.count, 0); assert.equal(state.endingAvailable, false);
  }
  const early = routeStatus([final]); assert.equal(early.count, 1); assert.equal(early.finalChapterRevealed, true);
  assert.equal(early.endingAvailable, false); assert.equal(early.nextBookId, 'four-truths');
  const thirteen = routeStatus(expected.slice(0,13)); assert.equal(thirteen.finalChapterRevealed, true);
  assert.equal(thirteen.nextBookId, final); assert.equal(thirteen.endingAvailable, false);
  const all = routeStatus([final, ...expected.slice(0,13)]);
  assert.equal(all.endingAvailable, true); assert.equal(all.nextBookId, null);
  assert.equal(all.ending.countsAsBook, false); assert.equal(all.ending.implemented, false);
});
check('arbitrary order / repeated completions produce identical rewards without mutating inputs', () => {
  const complete = ['anapana','mindfulness','six-senses','five-aggregates','eightfold-path'];
  const input = Object.freeze([...complete, 'anapana', 'unknown-book']);
  const positions = Object.freeze({ 'mindfulness':4 });
  const metadata = Object.freeze({ knownBookIds:Object.freeze([final]) });
  const a = routeStatus(input, positions, metadata), b = routeStatus([...complete].reverse(), positions, metadata);
  assert.deepEqual(a, b); assert.deepEqual([...input], [...complete,'anapana','unknown-book']);
  assert.equal(a.count, 5); assert.equal(a.combinations.city_allegory.available, true);
});
check('guardian and gates acquired early are previews until actual city sources are completed', () => {
  const guardian = ids => deriveCityState(ids).rewards.find(reward => reward.id === 'mindfulness_guard');
  assert.equal(guardian(['mindfulness']).earned, true); assert.equal(guardian(['mindfulness']).preview, true);
  assert.equal(guardian(['mindfulness','five-aggregates']).available, false);
  assert.equal(guardian(['mindfulness','five-aggregates','six-senses']).available, true);
  const gates = deriveCityState(['six-senses']); assert.equal(gates.features.six_gates, false);
  assert.equal(gates.rewards.find(reward => reward.id === 'six_gates').preview, true);
  assert.equal(deriveCityState(['anapana']).features.calm_insight_messengers, false);
});
check('first three states derive from IDs, including out-of-order reads', () => {
  assert.deepEqual([[],['four-truths'],['four-truths','five-aggregates'],['four-truths','five-aggregates','six-senses']].map(ids => deriveCityState(ids).stage), [0,1,2,3]);
  assert.equal(deriveCityState(['five-aggregates']).stage, 2);
  assert.equal(deriveCityState(['six-senses','five-aggregates']).stage, 3);
  assert.equal(deriveCityState(['four-truths']).features.four_elements_plaza, false);
  assert.equal(canonicalCorrespondences.truthful_message, '涅槃');
  assert.equal(canonicalCorrespondences.four_elements_plaza, '地、水、火、風四大');
  assert.equal(canonicalCorrespondences.city_lord, '識');
});
check('garden is independent; irrigation is extra two-book feedback and never a gate', () => {
  const path = routeStatus(['eightfold-path']); assert.equal(path.world.pathActive, true); assert.equal(path.world.gardenActive, false); assert.equal(path.world.irrigationActive, false);
  const garden = routeStatus(['right-effort']); assert.equal(garden.world.gardenActive, true); assert.equal(garden.world.pathActive, false); assert.equal(garden.world.irrigationActive, false);
  const both = routeStatus(['right-effort','eightfold-path']); assert.equal(both.world.irrigationActive, true);
  assert(both.books.every(book => book.canRead));
  for (const id of ['path_station','path_road','path_bridge_wisdom','path_bridge_concentration','path_bridge_effort_ethics','path_bridge_mindfulness','path_stream','wholesome_lake']) assert.equal(path.landmarks[id].active, true);
  assert.equal(path.landmarks.effort_garden.active, false);
});
check('faculties book does not manufacture source-book completion or five filled zones', () => {
  const only = routeStatus(['five-roots-powers']); assert.equal(only.count, 1);
  assert(Object.values(only.city.facultiesZones).every(zone => !zone.linked));
  const faith = deriveCityState(['five-roots-powers','four-purities-six-recollections']);
  assert.equal(faith.facultiesZones.faith.linked, true); assert.equal(faith.facultiesZones.wisdom.linked, false);
  assert.equal(deriveCityState(['five-roots-powers','four-truths']).facultiesZones.wisdom.conditionsLinked, false);
  assert.equal(deriveCityState(['five-roots-powers','four-truths','twelve-links']).facultiesZones.wisdom.conditionsLinked, true);
});
check('recommendation selects first supported unread stable ID', () => {
  assert.equal(recommendNextBook(['six-senses','four-truths']), 'five-aggregates');
  assert.equal(recommendNextBook(expected.slice(0,3), expected.slice(0,3)), null);
  assert.equal(recommendNextBook(expected), null);
});
check('metadata touches only its own key, never duplicates completed records or rewrites old saves', () => {
  const old = new Map([
    ['sutrazen.play.collection.v1', JSON.stringify({version:1,completed:[final,'anapana'],positions:{anapana:7},activeBook:final})],
    ['sutrazen.play.v1', JSON.stringify({version:1,completed:['four-truths'],positions:{'four-truths':6}})],
    ['unrecognized.numeric.legacy', '{"finishedLevels":[1,2]}'],
  ]);
  const before = [...old]; const fake = { getItem:key => old.get(key) ?? null, setItem:(key,value) => old.set(key,value), removeItem:key => old.delete(key) };
  const metadata = createRouteMetadataStore(fake);
  assert(metadata.markOpened(final)); assert(metadata.markAnimation('city_allegory'));
  assert.equal(metadata.markKnown('fake'), false);
  assert.deepEqual([...old].filter(([key]) => key !== ROUTE_METADATA_KEY), before);
  const raw = JSON.parse(old.get(ROUTE_METADATA_KEY)); assert.equal(Object.hasOwn(raw,'completed'), false); assert.equal(Object.hasOwn(raw,'positions'), false);
  assert.equal(routeStatus([], {}, metadata.get()).finalChapterRevealed, true);
  metadata.reset(); assert.deepEqual([...old], before);
  const blocked = createRouteMetadataStore({getItem(){throw Error('blocked')},setItem(){throw Error('blocked')},removeItem(){throw Error('blocked')}});
  blocked.markOpened(final); assert.equal(blocked.issue,'unavailable'); assert.equal(routeStatus([], {}, blocked.get()).count,0);
  old.set(ROUTE_METADATA_KEY,'{"version":1,"completed":["four-truths"]}'); assert.equal(createRouteMetadataStore(fake).issue,'corrupt');
});
let subsets = 0;
check('all 16384 completion subsets match normative combination conditions without order shortcuts', () => {
  for (let mask = 0; mask < 2 ** expected.length; mask++) {
    const selected = expected.filter((id, bit) => mask & (1 << bit)), have = new Set(selected);
    const scenes = sceneAvailability(selected);
    for (const [id, required] of Object.entries(normative)) {
      assert.equal(scenes[id].available, required.every(book => have.has(book)), `${id} at ${mask}`);
    }
    subsets++;
  }
});
console.log(JSON.stringify({version:'2026-11-22-r3 + map-v4', checks, subsets, result:'passed', scope:'Pure route/reward/metadata risks; original readers and 1192-step content are unchanged and not rerun here.'}, null, 2));
