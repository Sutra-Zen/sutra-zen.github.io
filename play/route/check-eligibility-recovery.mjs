// Same-tab recovery is a transport fallback for the one collection store, not
// a route-completion merge. Simulate a fresh ES-module document per navigation.
import assert from 'node:assert/strict';
const local = new Map(), session = new Map(); let quota = false, localBlocked = false, sessionBlocked = false;
globalThis.localStorage = {
  getItem(key){if(localBlocked)throw Error('blocked');return local.get(key)??null;},
  setItem(key,value){if(localBlocked||quota)throw Error('quota');local.set(key,value);},
  removeItem(key){if(localBlocked)throw Error('blocked');local.delete(key);},
};
globalThis.sessionStorage = {
  getItem(key){if(sessionBlocked)throw Error('blocked');return session.get(key)??null;},
  setItem(key,value){if(sessionBlocked)throw Error('blocked');session.set(key,value);},
  removeItem(key){if(sessionBlocked)throw Error('blocked');session.delete(key);},
};
globalThis.window = new EventTarget();
const KEY='sutrazen.play.collection.v1', RECOVERY='sutrazen.play.collection.session.v1';
const old={version:1,completed:['four-truths'],positions:{'five-aggregates':4,'four-jhanas':73},activeBook:'five-aggregates'};
const raw=JSON.stringify(old,null,1);local.set(KEY,raw);local.set('sutrazen.play.v1','old-journey');local.set('other-site-setting','keep');
let doc=0;const load=async()=> (await import(`../collection/store.js?recovery-test=${++doc}`)).store;
const checks=[];let store=await load();assert.deepEqual(store.get(),old);assert.equal(session.size,0);
quota=true;assert(store.savePosition('five-aggregates',7));assert.equal(store.issue,'unavailable');assert.equal(local.get(KEY),raw);
store=await load();assert.equal(store.get().positions['five-aggregates'],7);assert.equal(store.issue,'unavailable');
assert.deepEqual(store.get().completed,['four-truths']);assert.equal(store.get().positions['four-jhanas'],73);
assert(store.savePosition('five-aggregates',53));assert(store.complete('five-aggregates'));
store=await load();assert.deepEqual(store.get().completed,['four-truths','five-aggregates']);assert.equal(store.get().activeBook,'six-senses');assert.equal(local.get(KEY),raw);
const recoveryBefore=session.get(RECOVERY);assert(store.complete('five-aggregates'));assert.equal(session.get(RECOVERY),recoveryBefore);
checks.push('quota leaves stale valid local bytes; same-tab module/navigation recovers bookmark and explicit completion without duplicate count');
localBlocked=true;store=await load();assert.deepEqual(store.get().completed,['four-truths','five-aggregates']);assert(store.savePosition('six-senses',3));
localBlocked=false;store=await load();assert.deepEqual(store.get().completed,['four-truths','five-aggregates']);assert.equal(store.get().positions['six-senses'],3);
checks.push('temporary local-read denial preserves the recovery base marker; later readable unchanged canonical bytes do not discard session progress');

const history={version:1,completed:['four-jhanas','four-truths','five-aggregates'],positions:{'four-jhanas':5,'six-senses':8},activeBook:'six-senses'};
assert(store.restoreBackup(JSON.stringify(history)));store=await load();assert.deepEqual(store.get(),history);assert.equal(local.get(KEY),raw);
quota=false;assert(store.savePosition('six-senses',9));assert.equal(store.issue,null);assert.equal(session.has(RECOVERY),false);assert.deepEqual(JSON.parse(local.get(KEY)).completed,history.completed);
checks.push('legal out-of-order restore survives temporary persistence; successful local write clears recovery and keeps IDs/order');
// External canonical replacement is authoritative; never combine its completions
// with a stale recovery snapshot from this tab.
quota=true;assert(store.savePosition('six-senses',10));assert(session.has(RECOVERY));
const external={version:1,completed:['seven-factors'],positions:{'four-truths':2},activeBook:'four-truths'};
const externalRaw=JSON.stringify(external);local.set(KEY,externalRaw);store=await load();assert.deepEqual(store.get(),external);assert.equal(session.has(RECOVERY),false);assert.equal(local.get(KEY),externalRaw);
checks.push('changed canonical base from external restore wins exactly, clears stale recovery and does not merge completed sets');
localBlocked=true;sessionBlocked=true;store=await load();assert.equal(store.issue,'unavailable');assert(store.savePosition('four-truths',2));assert.equal(store.get().positions['four-truths'],2);assert.equal(local.get(KEY),externalRaw);
store=await load();assert.equal(store.issue,'unavailable');assert.equal(store.get().positions['four-truths'],undefined);
checks.push('both storages blocked remains honest single-document memory only, with no cross-page preservation claim');
assert.equal(local.get('sutrazen.play.v1'),'old-journey');assert.equal(local.get('other-site-setting'),'keep');
console.log(JSON.stringify({result:'passed',checks,primaryKey:KEY,recoveryKey:RECOVERY,otherNamespaces:'unchanged'},null,2));
