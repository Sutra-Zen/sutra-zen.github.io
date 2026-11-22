// Behavioral policy risks, using the real persistence module and legacy fixtures.
import assert from 'node:assert/strict';
import { CATALOG } from '../collection/catalog.js';
import { routeOrder } from './data.js';
import { routeStatus } from './selectors.js';
import { currentGameBookId, canStartGameBook, canReviewGameBook, canReadGameBook, canCompleteGameBook } from './eligibility.js';
const data = new Map(), writes = [];
globalThis.localStorage = {
  getItem: key => data.get(key) ?? null,
  setItem: (key, value) => { data.set(key, value); writes.push(key); },
  removeItem: key => { data.delete(key); writes.push(key); },
};
globalThis.window = new EventTarget();
const KEY = 'sutrazen.play.collection.v1';
const oldSave = {version:1,completed:['four-jhanas','four-truths'],positions:{'four-jhanas':28,'six-senses':73,'five-aggregates':2},activeBook:'six-senses'};
const raw = JSON.stringify(oldSave, null, 1);
data.set(KEY, raw); data.set('sutrazen.play.v1', 'preserve-original-journey'); data.set('unrelated-setting', 'keep');
const {store} = await import('../collection/store.js');
const counts = new Map(CATALOG.map(book => [book.id, book.totalSteps]));
const checks = [];
const test = (name, body) => { body(); checks.push(name); };
const seed = (completed = [], positions = {}, activeBook = routeOrder[0]) => {
  assert(store.restoreBackup(JSON.stringify({version:1,completed,positions,activeBook})));
};
test('existing out-of-order history, future bookmark and activeBook load unchanged, no initial writes', () => {
  assert.deepEqual(store.get(),oldSave); assert.equal(data.get(KEY),raw); assert.equal(writes.length,0);
  const s = routeStatus(store.get().completed,store.get().positions);
  assert.equal(s.nextBookId,'five-aggregates'); assert.equal(s.books.find(b=>b.id==='six-senses').canRead,false);
  assert.equal(s.books.find(b=>b.id==='four-jhanas').canReview,true);
});
test('only earliest unfinished starts/completes across all14 prefix states; bookmarks do not grant entry', () => {
  for (let prefix=0;prefix<=14;prefix++) {
    const completed=routeOrder.slice(0,prefix), positions=Object.fromEntries(routeOrder.map(id=>[id,counts.get(id)-1]));
    seed(completed,positions,'four-jhanas'); const before=data.get(KEY);
    assert.equal(currentGameBookId(completed),routeOrder[prefix]||null);
    for (const id of routeOrder) {
      assert.equal(canStartGameBook(id,completed),id===routeOrder[prefix]);
      assert.equal(canReviewGameBook(id,completed),completed.includes(id));
      assert.equal(canReadGameBook(id,completed),completed.includes(id)||id===routeOrder[prefix]);
      assert.equal(canCompleteGameBook(id,completed),id===routeOrder[prefix]);
      if (!canReadGameBook(id,completed)) {assert.equal(store.savePosition(id,0),false);assert.equal(store.complete(id),false);}
    }
    assert.equal(data.get(KEY),before);
  }
});
test('halfway/arrival never complete; formal last bookmark plus explicit eligible complete counts once', () => {
  seed();assert.equal(store.complete('four-truths'),false);assert(store.savePosition('four-truths',3));assert.equal(store.complete('four-truths'),false);
  assert(store.savePosition('four-truths',28));assert.deepEqual(store.get().completed,[]);
  assert(store.complete('four-truths'));assert.deepEqual(store.get().completed,['four-truths']);assert.equal(store.get().activeBook,'five-aggregates');
  const before=data.get(KEY), writeCount=writes.length;let events=0;const count=()=>events++;window.addEventListener('sutrazen:collection-progress',count);
  assert(store.complete('four-truths'));assert.equal(data.get(KEY),before);assert.equal(writes.length,writeCount);assert.equal(events,0);window.removeEventListener('sutrazen:collection-progress',count);
});
test('review retains completion and current mainline active target; only review bookmark changes', () => {
  seed(['four-truths'],{'four-truths':28,'five-aggregates':4,'four-jhanas':56},'five-aggregates');
  assert(store.savePosition('four-truths',5));assert.equal(store.get().activeBook,'five-aggregates');assert.equal(currentGameBookId(store.get().completed),'five-aggregates');assert.equal(store.get().positions['four-jhanas'],56);
  assert.equal(store.savePosition('four-jhanas',0),false);assert.deepEqual(store.get().completed,['four-truths']);
});
test('entry eligibility is rechecked after reset/restore while a reader is open', () => {
  seed(['four-truths'],{'five-aggregates':53},'five-aggregates');assert(canCompleteGameBook('five-aggregates',store.get().completed));
  seed([],{'five-aggregates':53},'five-aggregates');const before=data.get(KEY);assert.equal(store.complete('five-aggregates'),false);assert.equal(store.savePosition('five-aggregates',53),false);assert.equal(data.get(KEY),before);
});
test('final title is not revealed by an old future bookmark/open metadata; historical completion remains', () => {
  assert.equal(routeStatus([],{'four-fruits-ten-fetters':0},{knownBookIds:['four-fruits-ten-fetters']}).finalChapterRevealed,false);
  assert.equal(routeStatus(routeOrder.slice(0,13)).finalChapterRevealed,true);
  const history=routeStatus(['four-fruits-ten-fetters']);assert.equal(history.finalChapterRevealed,true);assert(history.books.at(-1).canReview);assert.equal(history.nextBookId,'four-truths');assert.equal(history.endingAvailable,false);
});
test('arbitrary legal legacy completion order is preserved on restore; no fabricated prerequisite completion', () => {
  seed(['seven-factors','four-fruits-ten-fetters','four-truths'],{'four-jhanas':9},'four-jhanas');
  assert.deepEqual(store.get().completed,['seven-factors','four-fruits-ten-fetters','four-truths']);assert.equal(currentGameBookId(store.get().completed),'five-aggregates');
  assert.equal(store.complete('four-jhanas'),false);assert.equal(store.get().positions['four-jhanas'],9);
  const before=data.get(KEY);assert.equal(store.restoreBackup('{broken'),false);assert.equal(data.get(KEY),before);
});
test('only existing collection key written; oldjourney/unrelated unchanged', () => {
  assert(writes.every(key=>key===KEY));assert.equal(data.get('sutrazen.play.v1'),'preserve-original-journey');assert.equal(data.get('unrelated-setting'),'keep');
});
console.log(JSON.stringify({policy:'strict-sequential-v1',result:'passed',checks,scope:'Real store and pure eligibility; no reader or camera rewrite.'},null,2));
