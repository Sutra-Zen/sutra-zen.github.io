# Route, eligibility and rewards (2026-11-22 immersion / strict-sequential-v1)

The current player journey uses the author's fixed fourteen-book route and one shared sequential eligibility policy. This supersedes the historical free-reading game prototype. Original public readers without `collection=1` remain freely readable; their narration, scripture, illustrations and URLs are unchanged.

## Authoritative input

```js
import { store } from '../collection/store.js';
import { routeStatus, deriveCityState } from '../route/selectors.js';
import { routeMetadata } from '../route/metadata.js';
const save = store.get();
const state = routeStatus(save.completed, save.positions, routeMetadata.get());
const city = deriveCityState(save.completed, save.positions, routeMetadata.get());
```

`save.completed` from `sutrazen.play.collection.v1` is the sole book-completion set. The selectors and `eligibility.js` are pure and never save, sort in place, migrate, reset or fill another book's completion. The old three-book `sutrazen.play.v1` remains separate. Existing out-of-order completed IDs stay valid; incomplete future bookmarks and `activeBook` values are retained but cannot grant access or redirect the mainline.

Only the first unfinished route book may start. Completed books may be reviewed, and the shelf offers only these reviews. Every player entry and any old collection entry must use the shared policy; a return URL such as `collectionReturn=game` is navigation context, never authorization. The visual gallery and city inspection routes import only data/renderers and do not read or write player storage.

## Public API

- `routeOrder`: fourteen permanent book IDs; Twelve Links is fourth, Seven Factors thirteenth, Four Fruits/Ten Fetters fourteenth. Independent from the existing homepage/catalog shelf order.
- `routeBooks`: catalog metadata in that recommendation order, including existing `totalSteps`, titles and relative reader URLs. URLs keep the catalog module's original base; use `new URL(book.reader, new URL('../collection/catalog.js', import.meta.url))` when consuming them elsewhere.
- `currentGameBookId(completed)`: first unfinished ID in the full fixed route, or `null`; this is the mainline target and ignores review bookmarks.
- `canStartGameBook`, `canReviewGameBook`, `canReadGameBook`, `canCompleteGameBook`: shared helpers in `eligibility.js`. Starting/completing applies only to the current unfinished book; reviewing applies only to completed IDs. `getGameBookAccess(id, completed, positions)` returns `available`, `reading`, `completed` or `locked`, plus eligibility and a valid `resumePosition`. A preserved future bookmark stays locked and returns no resumable position until eligible.
- `recommendNextBook(completed, supportedBookIds = routeOrder)`: pure first-supported-unread recommendation, or `null`. A restricted supported subset is not a permission check; entry and completion must still use the eligibility helpers.
- `routeStatus(completed, positions = {}, metadata = {})`: derived count/14, `nextBookId`, books with shared access fields, landmark state, world state, city state and combination conditions. `eligibilityPolicy` is `strict-sequential-v1`. `books[].mainlineTitle` conceals the final title until the reveal condition; locked bookmarks never set `inProgress`. The original public catalog remains unchanged outside the game.
- `sceneAvailability(completed)`: keyed objects with `available`, `requiredBookIds` and `missingBookIds` for the six r3 combinations and map-v4's `garden_irrigation`.
- `deriveCityState(...)`: `stage` 0–3 and named `stageId`, `features`, fourteen rewards, source-dependent `facultiesZones`, `sceneFlags` and ending-condition metadata. The first-three stage is based on actual IDs, not the number of completed books. Out-of-order completed rewards remain `earned`, can stay in `preview`, and become `available` for placement once their actual prerequisites are complete, without re-reading.
- `rewardDefinitions`, `combinationScenes`, `canonicalCorrespondences`, `landmarkBooks`, `endingDefinition`: author-aligned definitions from `data.js`.

Reward `type` is `canonical`, `extended` or `mixed`; `canonicalElements` and `extendedElements` identify the boundary. The town square remains the four elements, the lord represents consciousness, and the truthful message remains nirvana. The waterwheel/dock/garden/harbor/reading chronology is teaching and artwork extension. Neither reading nor scene availability indicates attainments.

## Completion, placement and geography

A book's own completion activates all world landmarks that belong to that book. City rewards may additionally need a city body or gates for placement. Historical out-of-order Mindfulness completion still grants a guardian preview; Five Aggregates + Six Senses later places it automatically without manufacturing prerequisites. New game completions must follow the shared sequential policy.

The real store rechecks eligibility before saving positions or completing a new book. It also requires the final real reader bookmark before explicit `store.complete(id)` can add a completion. Repeated completion of an already completed ID returns success without a write, event or reward. A review bookmark may change, but it does not replace the mainline `activeBook`. Opening, returning, refreshing, reaching the last page or viewing an animation never completes a book.

`world.gardenActive` depends only on Right Effort. Eightfold Path activates its station, road, four bridge groups, stream and Ten Wholesome Actions lake. Irrigation is extra feedback requiring both books, not a prerequisite for either reading or the flower field. The five faculties' zones only link to sources actually completed; the full network additionally uses the author's explicit combination set.

The road's visual west/east bridge order never replaces `routeOrder` or the original concept relations. Map geography, recommendation and doctrinal relations are separate.

## Known title and optional presentation metadata

The final title is revealed only when the first thirteen IDs are completed or that final book already has a historical completed ID. A future bookmark, step zero or known/opened metadata does not reveal or unlock it. Existing out-of-order completions remain valid for review without filling preceding IDs or releasing the ending early.

`metadata.js` exports `routeMetadata` and testable `createRouteMetadataStore(storage)`. Its independent key `sutrazen.play.route-metadata.v1` stores only:

- `knownBookIds`
- `openedBookIds`
- `playedAnimationIds`

Methods: `get()`, `get issue`, `markKnown(id)`, `markOpened(id)`, `markAnimation(sceneOrRewardId)`, `reset()`. It emits `sutrazen:route-metadata`, never collection-completion events. A malformed metadata record containing completed IDs or reader positions is rejected. Optional metadata storage failure does not affect existing reading/collection records.

Call `markOpened(id)` only after the real game entry passes eligibility. Metadata remains optional presentation history, not a gate or completion record. Do not call `store.complete` from a route view, title discovery, preview or animation skip. Playing/skipping/replaying an animation never changes earned rewards.

Primary saves retain the existing collection namespace. If permanent storage fails, the store may use `sutrazen.play.collection.session.v1` for same-tab navigation recovery, with the original canonical snapshot as its base marker. It never merges stale recovered completions with a newly replaced canonical save. If both storages fail, only the current document's memory is available and the UI reports that limitation. No code clears the entire site's storage.

## Ending boundary

`endingAvailable` means the fourteen-ID condition is met. `ending.implemented` remains **false**: this module provides the agreed future endpoint and author-supplied SA262 quotation, not a new fully written or illustrated story. The ending is not a fifteenth book and does not add a completion count. The quote is labelled SA262, not SN35.245.

## Targeted verification

Run `node play/route/check-route.mjs`, `node play/route/check-eligibility.mjs` and `node play/route/check-eligibility-recovery.mjs`. These check source/route order, canonical boundaries, the 16,384 completion subsets, legacy out-of-order placement, sequential entry and completion, future-bookmark retention without permission, review/mainline separation, final reveal, idempotence, namespace isolation and failed-storage recovery. Browser tests separately verify real reader entry/last-step actions and presentation. These pure checks do not re-run the unchanged 1,192-step content or claim physical Safari/artwork verification.
