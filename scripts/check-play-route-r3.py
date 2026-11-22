#!/usr/bin/env python3
"""Check r3 route/reward derivation without changing a player's saved progress.

This is a model/storage-boundary check, not a substitute for reader/UI tests.
It imports the real browser ES modules from a disposable local HTTP server.
"""
import functools
import hashlib
import http.server
import json
from pathlib import Path
import subprocess
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/previews/play-worldmap-v4/route-model-validation.json"
BASELINE = "4f4e1fd"
PROTECTED = [f"play/collection/{name}" for name in (
    "catalog.js", "store.js", "reader-bridge.js", "reader.css",
)]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        if self.path == "/__route_model_test__":
            body = b"<!doctype html><meta charset=utf-8><title>Isolated route model QA</title>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()


MODEL_CHECK = r"""async () => {
  const data = await import('/play/route/data.js');
  const selectors = await import('/play/route/selectors.js');
  const metadataModule = await import('/play/route/metadata.js');
  const { CATALOG } = await import('/play/collection/catalog.js');
  let assertionCount = 0;
  const scenarios = [];
  const assert = (condition, message) => {
    assertionCount++;
    if (!condition) throw new Error(message);
  };
  const equal = (actual, expected, label) => assert(JSON.stringify(actual) === JSON.stringify(expected),
    `${label}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  const scenario = (id, fn) => { const before = assertionCount; fn(); scenarios.push({id, assertions: assertionCount - before, result: 'passed'}); };
  const order = ['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path',
    'four-purities-six-recollections','mindfulness','right-effort','anapana','iddhipada',
    'four-jhanas','five-roots-powers','seven-factors','four-fruits-ten-fetters'];
  const final = order[13];
  const status = selectors.routeStatus;
  const reward = (s, id) => s.city.rewards.find(item => item.id === id);
  const book = (s, id) => s.books.find(item => item.id === id);
  const cityRequired = ['five-aggregates','six-senses','eightfold-path','mindfulness','anapana'];
  const pathLandmarks = ['path_station','path_road','path_bridge_wisdom','path_bridge_concentration',
    'path_bridge_effort_ethics','path_bridge_mindfulness','path_stream','wholesome_lake'];
  scenario('stable IDs, new recommendation order, original catalog order unchanged', () => {
    equal(data.routeOrder, order, 'routeOrder');
    equal(selectors.routeBooks.map(item=>item.id), order, 'derived route books');
    equal(selectors.routeBooks.map(item=>item.order), order.map((_,i)=>i+1), 'order labels');
    equal(new Set(order).size, 14, 'unique books');
    equal(CATALOG.length, 14, 'original catalog length');
    equal(CATALOG[5].id, final, 'original public book06 identity');
    equal(data.FIRST_THIRTEEN, order.slice(0,13), 'final reveal prerequisite IDs');
    equal(data.FINAL_BOOK_ID, final, 'stable final ID');
    equal(data.ROUTE_VERSION, '2026-11-22-r3', 'handoff route version');
    equal(data.MAP_VERSION, '2026-11-22-map-v4', 'handoff map version');
    equal(status([]).total, 14, 'fixed denominator');
    equal(status([]).books.every(item=>item.canRead), true, 'recommendation is not a reader lock');
  });
  scenario('first missing supported book, not numeric chapter completion', () => {
    equal(selectors.recommendNextBook([]), order[0], 'new player');
    equal(selectors.recommendNextBook(order.slice(0,3)), 'twelve-links', 'after first three');
    equal(selectors.recommendNextBook([order[0], order[2]], new Set(order.slice(0,3))), order[1], 'missing middle supported');
    equal(selectors.recommendNextBook(order.slice(0,3), order.slice(0,3)), null, 'prototype support exhausted');
    equal(selectors.recommendNextBook([final]), order[0], 'early final completion');
    equal(selectors.recommendNextBook([], ['seven-factors','twelve-links']), 'twelve-links', 'supported list does not reorder route');
    equal(selectors.recommendNextBook([], []), null, 'nothing supported');
    equal(status([1,2,3,'unknown']).count, 0, 'do not guess numeric legacy completion');
  });
  scenario('one book activates many landmarks but counts once', () => {
    const s = status(['eightfold-path','eightfold-path']);
    equal(s.count, 1, 'unique book completion');
    equal(s.completedBookIds, ['eightfold-path'], 'book not landmark IDs');
    for (const id of pathLandmarks) {
      equal(data.landmarkBooks[id], 'eightfold-path', `${id} ownership`);
      equal(s.landmarks[id].active, true, `${id} activated`);
    }
    equal(s.landmarks.effort_garden.active, false, 'no borrowed effort completion');
    equal(status(['six-senses']).landmarks.sense_landings.active, true, 'multiple senses entries');
    equal(status(['six-senses']).count, 1, 'multiple senses entries still one');
    const c = status(['anapana']);
    equal(c.landmarks.breathing_grove.active, true, 'breathing grove');
    equal(c.landmarks.calm_insight_streams.active, true, 'same book streams');
    equal(c.landmarks.endeavor_boathouse.active, false, 'independent iddhipada');
    equal(c.landmarks.jhana_water_garden.active, false, 'independent jhanas');
  });
  scenario('eightfold path and right effort independently unlock world rewards', () => {
    for (const [done, path, garden, irrigation] of [
      [[],false,false,false], [['eightfold-path'],true,false,false],
      [['right-effort'],false,true,false], [['right-effort','eightfold-path'],true,true,true],
    ]) {
      const s = status(done);
      equal(s.world.pathBaseVisible, true, 'base path stays visible');
      equal(s.world.harborAccessible, true, 'harbor remains usable');
      equal(s.world.pathActive, path, 'path activation');
      equal(s.world.wholesomeLakeActive, path, 'wholesome lake owner');
      equal(s.world.gardenActive, garden, 'independent garden');
      equal(s.world.irrigationActive, irrigation, 'cross-book irrigation');
      equal(s.count, done.length, 'irrigation is not another book');
    }
    equal(status(['right-effort']).landmarks.effort_garden.active, true, 'early free garden');
    equal(reward(status(['right-effort']), 'effort_garden').preview, true, 'city garden waits for body');
    equal(reward(status(['right-effort','five-aggregates']), 'effort_garden').available, true, 'city placement later');
  });
  scenario('earned preview is separate from later city placement', () => {
    for (const [id, rewardId, required] of [
      ['mindfulness','mindfulness_guard',['five-aggregates','six-senses']],
      ['six-senses','six_gates',['five-aggregates']],
      ['anapana','calm_insight_messengers',['five-aggregates']],
    ]) {
      const early = status([id]);
      equal(early.completedBookIds, [id], `${id}: no invented completions`);
      equal(reward(early,rewardId).earned, true, `${id}: earned immediately`);
      equal(reward(early,rewardId).preview, true, `${id}: preview before placement`);
      equal(reward(early,rewardId).available, false, `${id}: not yet placed`);
      const later = status([id,...required]);
      equal(reward(later,rewardId).earned, true, `${id}: reward remains owned`);
      equal(reward(later,rewardId).preview, false, `${id}: no reread required`);
      equal(reward(later,rewardId).available, true, `${id}: automatically placed`);
      equal(later.count, required.length+1, `${id}: only actual books counted`);
    }
    equal(status([]).city.stage, 0, 'initial city');
    equal(status(['four-truths']).city.stage, 1, 'dock and silhouette');
    equal(status(['four-truths','five-aggregates']).city.stage, 2, 'body, plaza, lord');
    equal(status(order.slice(0,3)).city.stage, 3, 'six gates');
    equal(status(['five-aggregates']).city.features.city_lord, true, 'lord derives from body');
    equal(status(['five-aggregates']).city.features.four_elements_plaza, true, 'four elements plaza');
  });
  scenario('complete city allegory depends on five exact books, not ordinal nine', () => {
    equal(status(cityRequired).combinations.city_allegory.available, true, 'five free-read prerequisites suffice');
    equal(status(cityRequired.slice().reverse()).city.features.truthful_message, true, 'reverse order same outcome');
    equal(status(order.slice(0,9)).combinations.city_allegory.available, true, 'natural mainline ninth');
    const otherNine = order.filter(id=>id!=='anapana').slice(0,9);
    equal(otherNine.length, 9, 'negative fixture has nine completions');
    equal(status(otherNine).combinations.city_allegory.available, false, 'nine arbitrary books insufficient');
    for (const missing of cityRequired) equal(status(cityRequired.filter(id=>id!==missing)).combinations.city_allegory.available, false, `missing ${missing}`);
    equal(status(['five-aggregates','six-senses']).combinations.city_experience.available, true, 'experience combination');
    equal(status(['five-aggregates','six-senses']).combinations.city_conditions.available, false, 'conditions needs twelve links');
    equal(status(['twelve-links','five-aggregates','six-senses']).combinations.city_conditions.available, true, 'conditions in arbitrary order');
  });
  scenario('faculties source areas never complete missing books', () => {
    const sourceIds = {faith:'four-purities-six-recollections',effort:'right-effort',mindfulness:'mindfulness',concentration:'four-jhanas',wisdom:'four-truths'};
    const early = status(['five-roots-powers']);
    equal(early.count, 1, 'faculties only one completion');
    for (const [zone,source] of Object.entries(sourceIds)) {
      equal(early.city.facultiesZones[zone].sourceCompleted, false, `${zone} not fabricated`);
      equal(early.city.facultiesZones[zone].linked, false, `${zone} waits for source`);
      equal(early.city.facultiesZones[zone].preview, true, `${zone} preview`);
      const linked = status(['five-roots-powers',source]);
      equal(linked.city.facultiesZones[zone].linked, true, `${zone} own source links`);
      equal(linked.city.facultiesZones[zone].available, false, `${zone} city placement needs body`);
      const placed = status(['five-roots-powers',source,'five-aggregates',...(zone==='mindfulness'?['six-senses']:[])]);
      equal(placed.city.facultiesZones[zone].available, true, `${zone} placed when complete`);
      equal(data.facultiesSources[zone].bookId, source, `${zone} reference definition`);
    }
    equal(status(['five-roots-powers','four-truths']).city.facultiesZones.wisdom.conditionsLinked, false, 'wisdom core is truths');
    equal(status(['five-roots-powers','four-truths','twelve-links']).city.facultiesZones.wisdom.conditionsLinked, true, 'twelve links adds conditions review');
    equal(status(['five-roots-powers','twelve-links']).city.facultiesZones.wisdom.linked, false, 'twelve links does not replace truths');
    const network = data.combinationScenes.find(item=>item.id==='faculties_network').requiredBookIds;
    equal(status(network).combinations.faculties_network.available, true, 'all specified sources');
    for (const source of network) equal(status(network.filter(id=>id!==source)).combinations.faculties_network.available, false, `network missing ${source}`);
  });
  scenario('hidden final title, known-book exceptions, reveal and ending are distinct', () => {
    let s = status([]);
    equal(s.finalChapterRevealed, false, 'initial mystery');
    equal(book(s,final).mainlineTitle, '尚未揭曉的旅程', 'hidden mainline label');
    equal(book(s,final).canRead, true, 'free/public book stays readable');
    equal(s.landmarks.fruition_valley.visible, false, 'only mainline landmark concealed');
    s = status(order.slice(0,13));
    equal(s.finalChapterRevealed, true, 'first thirteen reveal');
    equal(s.nextBookId, final, 'recommend final next');
    equal(s.endingAvailable, false, 'reveal is not ending');
    s = status([final]);
    equal(s.finalChapterRevealed, true, 'early completed title stays known');
    equal(s.count, 1, 'early final counts exactly one');
    equal(reward(s,'fruition_guide').earned, true, 'early final reward');
    equal(s.endingAvailable, false, 'final alone is not ending');
    const missing = 'four-truths';
    s = status(order.filter(id=>id!==missing));
    equal(s.count, 13, 'thirteen arbitrary subset');
    equal(s.finalChapterRevealed, true, 'known final is not rehidden');
    equal(s.combinations.final_chapter_reveal.available, false, 'specific first thirteen not satisfied');
    equal(s.endingAvailable, false, 'missing one book blocks ending');
    equal(s.nextBookId, missing, 'backfill first missing');
    s = status(order.slice().reverse());
    equal(s.count, 14, 'arbitrary order all fourteen');
    equal(s.endingAvailable, true, 'all fourteen ending eligibility');
    equal(s.ending.available, true, 'ending data eligibility');
    equal(s.nextBookId, null, 'no reread required');
    equal(s.ending.countsAsBook, false, 'ending not fifteenth book');
    equal(s.total, 14, 'ending keeps denominator');
    equal(s.ending.implemented, false, 'ending script is explicitly not implemented');
    equal(s.ending.quoteSource, '《雜阿含經》第262經', 'ending reference distinct from city SN');
    equal(status([], {[final]:0}).finalChapterRevealed, true, 'existing bookmark zero proves known title');
    equal(status([], {[final]:0}).count, 0, 'bookmark is not completion');
    for (const field of ['knownBookIds','openedBookIds','visitedBookIds','discoveredBookIds']) {
      equal(status([],{}, {[field]:[final]}).finalChapterRevealed, true, `${field} known exception`);
      equal(status([],{}, {[field]:new Set([final])}).count, 0, `${field} does not complete`);
    }
    for (const invalid of [-1,'0',null,0.5]) equal(status([], {[final]:invalid}).finalChapterRevealed, false, 'invalid final bookmark not trusted');
    equal(status([],Object.create({[final]:0})).finalChapterRevealed, false, 'inherited final bookmark ignored');
  });
  scenario('order independence, deduplication and input objects are immutable', () => {
    const completed = Object.freeze(['mindfulness','four-truths','mindfulness','unknown']);
    const positions = Object.freeze({mindfulness:6,[final]:0});
    const metadata = Object.freeze({knownBookIds:Object.freeze([final]),playedAnimationIds:Object.freeze(['city_body'])});
    const before = JSON.stringify({completed,positions,metadata});
    const a = status(completed,positions,metadata);
    const b = status(new Set(['four-truths','mindfulness']),positions,metadata);
    equal(a,b,'array/Set and input order produce same derivation');
    equal(JSON.stringify({completed,positions,metadata}),before,'inputs not rewritten');
    equal(a.completedBookIds,['four-truths','mindfulness'],'stable output order');
    equal(a.count,2,'unknown IDs and duplicates excluded');
    equal(book(a,'mindfulness').position,6,'existing position preserved');
    equal(book(a,'mindfulness').inProgress,true,'completed reread can resume');
    equal(book(status(['mindfulness'],{mindfulness:110}),'mindfulness').inProgress,false,'finished position is not reread in progress');
  });
  scenario('city canonical correspondences remain separate from creative rewards', () => {
    const expected = {city_body:'四大所成、會變壞的色身',four_elements_plaza:'地、水、火、風四大',six_gates:'眼、耳、鼻、舌、身、意六內處',mindfulness_guard:'念',city_lord:'識',calm_insight_messengers:'止、觀',truthful_message:'涅槃',noble_path:'八正道'};
    equal(data.canonicalCorrespondences,expected,'SN six-gate city map');
    equal(data.rewardDefinitions.length,14,'one own-book reward per book');
    equal(new Set(data.rewardDefinitions.map(item=>item.bookId)).size,14,'no duplicate own-book reward');
    equal(data.rewardDefinitions.every(item=>['canonical','mixed','extended'].includes(item.type)),true,'creative provenance type retained');
    equal(reward(status([]),'confidence_harbor').feedbackLabel,'場景開放','avoid claiming faith attainment');
    equal(reward(status([]),'jhana_garden').feedbackLabel,'讀本完成','avoid claiming jhana attainment');
    equal(reward(status([]),'fruition_guide').feedbackLabel,'導覽開放','avoid claiming fruits attained');
  });
  scenario('all 16384 completion subsets: counts, recommendation, rewards and endings', () => {
    const allMask = (1<<14)-1;
    const requirements = {
      truth_dock:['four-truths'],city_body:['five-aggregates'],six_gates:['five-aggregates','six-senses'],
      conditions_wheel:['five-aggregates','twelve-links'],noble_path:['five-aggregates','eightfold-path'],
      confidence_harbor:['four-purities-six-recollections'],mindfulness_guard:['five-aggregates','six-senses','mindfulness'],
      effort_garden:['five-aggregates','right-effort'],calm_insight_messengers:['five-aggregates','anapana'],
      endeavor_boat:['iddhipada'],jhana_garden:['five-aggregates','four-jhanas'],
      faculties_links:['five-aggregates','five-roots-powers'],awakening_companions:['five-aggregates','seven-factors'],fruition_guide:[final],
    };
    for (let mask=0;mask<=allMask;mask++) {
      const done=order.filter((_,i)=>mask&(1<<i)), set=new Set(done);
      const s=status(done.slice().reverse());
      const prefix=`subset ${mask}`;
      equal(s.count,done.length,`${prefix} count`);
      equal(s.completedBookIds,done,`${prefix} stable completed IDs`);
      equal(s.nextBookId,order.find(id=>!set.has(id))||null,`${prefix} recommendation`);
      equal(s.endingAvailable,mask===allMask,`${prefix} ending`);
      equal(s.finalChapterRevealed,set.has(final)||order.slice(0,13).every(id=>set.has(id)),`${prefix} final known`);
      equal(s.world.pathActive,set.has('eightfold-path'),`${prefix} path owner`);
      equal(s.world.gardenActive,set.has('right-effort'),`${prefix} garden owner`);
      equal(s.world.irrigationActive,set.has('eightfold-path')&&set.has('right-effort'),`${prefix} irrigation`);
      equal(s.combinations.city_allegory.available,cityRequired.every(id=>set.has(id)),`${prefix} city five-book set`);
      for (const r of s.city.rewards) {
        equal(r.earned,set.has(r.bookId),`${prefix} ${r.id} earned`);
        equal(r.available,requirements[r.id].every(id=>set.has(id)),`${prefix} ${r.id} placement`);
        equal(r.preview,r.earned&&!r.available,`${prefix} ${r.id} preview`);
      }
      for (const [id,owner] of Object.entries(data.landmarkBooks)) equal(s.landmarks[id].active,set.has(owner),`${prefix} ${id} landmark`);
    }
  });
  const makeStorage = (initial={}) => {
    const map=new Map(Object.entries(initial)),calls=[];
    return {map,calls,getItem(key){calls.push(['get',key]);return map.get(key)??null;},
      setItem(key,value){calls.push(['set',key]);map.set(key,String(value));},
      removeItem(key){calls.push(['remove',key]);map.delete(key);},
      clear(){throw new Error('No test/product action may clear all storage');}};
  };
  scenario('presentation metadata cannot overwrite authoritative collection records', () => {
    const key=metadataModule.ROUTE_METADATA_KEY;
    const legacy='{"version":1,"positions":{"four-fruits-ten-fetters":0,"mindfulness":17},"completed":["mindfulness"],"activeBook":"mindfulness"}';
    const fake=makeStorage({'sutrazen.play.collection.v1':legacy,'sutrazen.play.v1':'old journey bytes','unrelated':'retain me'});
    const store=metadataModule.createRouteMetadataStore(fake);
    equal(fake.calls,[['get',key]],'construction reads metadata only');
    equal(store.markOpened(final),true,'known final opening');
    equal(store.markKnown(final),true,'duplicate known allowed');
    equal(store.markAnimation('city_body'),true,'animation record');
    equal(store.markAnimation('city_body'),true,'replayed/skipped animation dedup');
    equal(store.markAnimation('city_allegory'),true,'combination animation');
    const value=store.get();
    equal(value.knownBookIds,[final],'known IDs dedup');
    equal(value.openedBookIds,[final],'opened IDs separate');
    equal(value.playedAnimationIds,['city_body','city_allegory'],'animation IDs dedup');
    equal(Object.keys(value).sort(),['version','knownBookIds','openedBookIds','playedAnimationIds'].sort(),'metadata stores no completion/positions');
    equal(fake.map.get('sutrazen.play.collection.v1'),legacy,'authoritative collection bytes preserved');
    equal(fake.map.get('sutrazen.play.v1'),'old journey bytes','old journey untouched');
    equal(fake.map.get('unrelated'),'retain me','unrelated key untouched');
    const eventWrites=fake.calls.filter(([action])=>action==='set').length;
    equal(store.markOpened('bogus'),false,'invalid opened ID rejected');
    equal(store.markKnown(14),false,'numeric old ID not guessed');
    equal(store.markAnimation('bogus'),false,'invalid animation rejected');
    equal(fake.calls.filter(([action])=>action==='set').length,eventWrites,'invalid marks do not write');
    const clone=store.get();clone.knownBookIds.push('four-truths');
    equal(store.get().knownBookIds,[final],'metadata getter isolates state');
    store.reset();
    equal(fake.map.has(key),false,'reset removes only metadata');
    equal(fake.map.get('sutrazen.play.collection.v1'),legacy,'metadata reset preserves collection');
    equal(fake.calls.filter(([action])=>['set','remove'].includes(action)).every(([,k])=>k===key),true,'all mutations scoped to metadata key');
  });
  scenario('invalid old metadata preserved on load and unavailable storage remains usable', () => {
    const key=metadataModule.ROUTE_METADATA_KEY;
    const valid={version:1,knownBookIds:[final,final],openedBookIds:[final],playedAnimationIds:['city_body','city_body']};
    const okay=metadataModule.createRouteMetadataStore(makeStorage({[key]:JSON.stringify(valid)}));
    equal(okay.issue,null,'valid optional metadata');
    equal(okay.get().knownBookIds,[final],'valid duplicates normalize in memory');
    for (const raw of ['{broken',JSON.stringify({...valid,positions:{[final]:0}}),JSON.stringify({...valid,completed:[final]}),JSON.stringify({...valid,completedBookIds:[final]}),JSON.stringify({...valid,knownBookIds:[99]}),JSON.stringify({...valid,playedAnimationIds:['unrecognized']})]) {
      const fake=makeStorage({[key]:raw,'sutrazen.play.collection.v1':'legacy invalid source bytes'});
      const model=metadataModule.createRouteMetadataStore(fake);
      equal(model.issue,'corrupt','invalid metadata flagged');
      equal(fake.map.get(key),raw,'invalid metadata raw preserved on read');
      equal(fake.map.get('sutrazen.play.collection.v1'),'legacy invalid source bytes','unconfirmed legacy raw preserved');
      equal(fake.calls.every(([action])=>action==='get'),true,'invalid load never clears or writes');
    }
    for (const storage of [null,{getItem(){throw new Error('blocked');},setItem(){throw new Error('blocked');},removeItem(){throw new Error('blocked');}}]) {
      const model=metadataModule.createRouteMetadataStore(storage);
      equal(model.issue,'unavailable','storage unavailable reported');
      equal(model.markOpened(final),true,'memory metadata remains usable');
      equal(model.get().openedBookIds,[final],'memory state retained');
      equal(model.issue,'unavailable','writing still reports unavailable');
    }
  });
  return {result:'passed',assertionCount,scenarioCount:scenarios.length,exhaustiveCompletionSubsets:16384,scenarios,
    ending:{eligibilityVerified:true,implemented:data.endingDefinition.implemented,claim:'Eligibility data only; no complete epilogue is claimed.'}};
}"""


def main():
    report = {
        "scope": "2026-11-22-r3 pure route/reward selectors and presentation metadata",
        "environment": "Local HTTP + desktop Chromium ES modules; no physical Safari or external source tests",
        "protectedBaseline": BASELINE,
        "protectedFiles": [],
        "javascriptErrors": [],
        "httpErrors": [],
        "limitations": [
            "No UI, artwork, source-link loading or reader-navigation assertion belongs to this model-only test.",
            "All completion-subset fixtures are isolated test inputs, not a user's saved achievements.",
            "No claim that the independent epilogue has been implemented or publicly deployed.",
        ],
    }
    for path in PROTECTED:
        baseline = subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT)
        actual = (ROOT / path).read_bytes()
        normalized = actual
        permitted = []
        if path == "play/collection/reader-bridge.js":
            # Only the explicit worldmap opt-in may change where the existing
            # collection reader returns. No reader/save/completion logic differs.
            replacements = [
                (
                    "  const worldmapReturn = new URLSearchParams(location.search).get('collectionReturn') === 'worldmap-v4';\n"
                    "  const shelfURL = new URL(worldmapReturn ? '../worldmap-v4/' : '../visual-v2/shelf.html', import.meta.url);\n"
                    "  const returnLabel = worldmapReturn ? (await import('../worldmap-v4/text.js')).T.returnJourney : text.returnShelf;\n",
                    "  const shelfURL = new URL('../visual-v2/shelf.html', import.meta.url);\n",
                ),
                (
                    "  returnLink.href = shelfURL.href; returnLink.textContent = returnLabel;\n",
                    "  returnLink.href = shelfURL.href; returnLink.textContent = text.returnShelf;\n",
                ),
                (
                    "  returnLink.setAttribute('aria-label', returnLabel);\n",
                    "  returnLink.setAttribute('aria-label', text.returnShelf);\n",
                ),
            ]
            for expected, original in replacements:
                assert normalized.count(expected.encode()) == 1, "Authorized reader return branch changed unexpectedly"
                normalized = normalized.replace(expected.encode(), original.encode(), 1)
            permitted = ["collectionReturn=worldmap-v4 opt-in return URL and translated return label only"]
        assert normalized == baseline, f"Existing collection behavior changed beyond authorized return target: {path}"
        report["protectedFiles"].append({
            "path": path,
            "sha256": hashlib.sha256(actual).hexdigest(),
            "normalizedSha256": hashlib.sha256(normalized).hexdigest(),
            "permittedChanges": permitted,
            "result": "normalized byte-identical" if permitted else "byte-identical",
        })
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
            context = browser.new_context()
            page = context.new_page()
            page.on("pageerror", lambda error: report["javascriptErrors"].append(str(error)))
            page.on("response", lambda response: report["httpErrors"].append(response.url) if response.url.startswith(base) and response.status >= 400 else None)
            page.goto(base + "/__route_model_test__")
            report["model"] = page.evaluate(MODEL_CHECK)
            # Use real localStorage only in fresh, isolated browser contexts.
            report["legacyStorageFixtures"] = []
            all_ids = [
                "four-truths", "five-aggregates", "six-senses", "twelve-links", "eightfold-path",
                "four-purities-six-recollections", "mindfulness", "right-effort", "anapana", "iddhipada",
                "four-jhanas", "five-roots-powers", "seven-factors", "four-fruits-ten-fetters",
            ]
            for kind, raw, expected_issue, expected_count in [
                ("recognizable bookmark-zero record", json.dumps({"version": 1, "positions": {"four-fruits-ten-fetters": 0, "mindfulness": 17}, "completed": ["mindfulness"], "activeBook": "mindfulness"}, separators=(",", ":")), None, 1),
                ("preexisting all-fourteen completion and bookmark record", json.dumps({"version": 1, "positions": {book_id: index for index, book_id in enumerate(all_ids)}, "completed": all_ids[::-1], "activeBook": "seven-factors"}, separators=(",", ":")), None, 14),
                ("unconfirmed malformed old record", "{unconfirmed old saved record", "corrupt", 0),
                ("unconfirmed numeric-version old record", json.dumps({"version": 0, "completed": [1, 2, 3], "position": 9}), "corrupt", 0),
            ]:
                fixture = browser.new_context()
                fixture.add_init_script("localStorage.setItem('sutrazen.play.collection.v1', " + json.dumps(raw) + "); localStorage.setItem('sutrazen.play.v1','older-three-book-record'); localStorage.setItem('unrelated-key','keep-this');")
                p = fixture.new_page()
                p.goto(base + "/__route_model_test__")
                result = p.evaluate("""async () => {
                  const keys=['sutrazen.play.collection.v1','sutrazen.play.v1','unrelated-key'];
                  const before=Object.fromEntries(keys.map(key=>[key,localStorage.getItem(key)]));
                  const {store}=await import('/play/collection/store.js');
                  const {routeStatus}=await import('/play/route/selectors.js');
                  const {routeMetadata}=await import('/play/route/metadata.js');
                  const state=store.get();
                  const initial=routeStatus(state.completed,state.positions,routeMetadata.get());
                  routeMetadata.markOpened('four-fruits-ten-fetters');
                  routeMetadata.markAnimation('city_body');
                  routeMetadata.markAnimation('city_allegory');
                  const after=Object.fromEntries(keys.map(key=>[key,localStorage.getItem(key)]));
                  const derived=routeStatus(state.completed,state.positions,routeMetadata.get());
                  return {rawUnchanged:JSON.stringify(before)===JSON.stringify(after),collectionIssue:store.issue,
                    initialCount:initial.count,afterMetadataCount:derived.count,initialFinalKnown:initial.finalChapterRevealed,initialEndingEligible:initial.endingAvailable,
                    afterMetadataFinalKnown:derived.finalChapterRevealed,positionsUnchanged:JSON.stringify(store.get().positions)===JSON.stringify(state.positions),
                    metadataFields:Object.keys(routeMetadata.get()).sort()};
                }""")
                assert result["rawUnchanged"] and result["positionsUnchanged"], "Route presentation changed existing saved records"
                assert result["collectionIssue"] == expected_issue, result
                assert result["initialCount"] == expected_count, "Recognized completion IDs were lost or invented"
                assert result["initialCount"] == result["afterMetadataCount"], "Metadata created a completion"
                assert result["initialEndingEligible"] == (expected_count == 14), "Existing all-fourteen record did not immediately qualify for ending"
                if expected_issue is None:
                    assert result["initialFinalKnown"], "Saved final bookmark at page zero was hidden"
                assert result["afterMetadataFinalKnown"], "Opened final title was rehidden"
                report["legacyStorageFixtures"].append({"kind": kind, **result})
                fixture.close()
            context.close()
            browser.close()
        assert not report["javascriptErrors"] and not report["httpErrors"], report
        report["result"] = "passed"
    finally:
        server.shutdown()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"result": report["result"], "scenarios": report["model"]["scenarioCount"], "assertions": report["model"]["assertionCount"], "completionSubsets": report["model"]["exhaustiveCompletionSubsets"], "report": str(OUTPUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
