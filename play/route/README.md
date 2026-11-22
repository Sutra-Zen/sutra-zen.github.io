# Route and reward selectors (2026-11-22-r3 / map-v4)

These modules implement the author's actual document versions, despite the older `v2` / `v1` attachment filenames. They do not change public book order, narrations, scripture, readers, completion events, or the existing collection/v1 stores.

## Authoritative input

```js
import { store } from '../collection/store.js';
import { routeStatus, deriveCityState } from '../route/selectors.js';
import { routeMetadata } from '../route/metadata.js';
const save = store.get();
const state = routeStatus(save.completed, save.positions, routeMetadata.get());
const city = deriveCityState(save.completed, save.positions, routeMetadata.get());
```

`save.completed` from `sutrazen.play.collection.v1` is the sole book-completion set. The selectors are pure and never save, sort in place, migrate, reset or fill another book's completion. The old three-book `sutrazen.play.v1` remains untouched. Unknown numeric legacy progress is not guessed or cleared. All fourteen supported books have `canRead: true`; the mainline reveal is presentation only, not a reading gate.

## Public API

- `routeOrder`: fourteen permanent book IDs; Twelve Links is fourth, Seven Factors thirteenth, Four Fruits/Ten Fetters fourteenth. Independent from the existing homepage/catalog shelf order.
- `routeBooks`: catalog metadata in that recommendation order, including existing `totalSteps`, titles and relative reader URLs. URLs keep the catalog module's original base; use `new URL(book.reader, new URL('../collection/catalog.js', import.meta.url))` when consuming them elsewhere.
- `recommendNextBook(completed, supportedBookIds = routeOrder)`: first supported unread ID, or `null`. It does not require the preceding books to be read before free access.
- `routeStatus(completed, positions = {}, metadata = {})`: derived count/14, `nextBookId`, books, landmark state, world state, city state and combination conditions. `books[].mainlineTitle` hides the last title only when appropriate; the real catalog title remains available for free reading and original public pages.
- `sceneAvailability(completed)`: keyed objects with `available`, `requiredBookIds` and `missingBookIds` for the six r3 combinations and map-v4's `garden_irrigation`.
- `deriveCityState(...)`: `stage` 0–3 and named `stageId`, `features`, fourteen rewards, source-dependent `facultiesZones`, `sceneFlags` and ending-condition metadata. The first-three stage is based on actual IDs, not the number of completed books. Out-of-order completed rewards remain `earned`, can stay in `preview`, and become `available` for placement once their actual prerequisites are complete, without re-reading.
- `rewardDefinitions`, `combinationScenes`, `canonicalCorrespondences`, `landmarkBooks`, `endingDefinition`: author-aligned definitions from `data.js`.

Reward `type` is `canonical`, `extended` or `mixed`; `canonicalElements` and `extendedElements` identify the boundary. The town square remains the four elements, the lord represents consciousness, and the truthful message remains nirvana. The waterwheel/dock/garden/harbor/reading chronology is teaching and artwork extension. Neither reading nor scene availability indicates attainments.

## Completion, placement and geography

A book's own completion activates all world landmarks that belong to that book. City rewards may additionally need a city body or gates for placement. Thus freely completing Mindfulness grants a guardian preview; Five Aggregates + Six Senses later places it automatically. It does not manufacture either prerequisite book.

`world.gardenActive` depends only on Right Effort. Eightfold Path activates its station, road, four bridge groups, stream and Ten Wholesome Actions lake. Irrigation is extra feedback requiring both books, not a prerequisite for either reading or the flower field. The five faculties' zones only link to sources actually completed; the full network additionally uses the author's explicit combination set.

The road's visual west/east bridge order never replaces `routeOrder` or the original concept relations. Map geography, recommendation and doctrinal relations are separate.

## Known title and optional presentation metadata

The final title is revealed when the first thirteen IDs are completed **or** the final book is already completed, has an existing valid position (including step zero), or has explicitly known/opened metadata. Old identifiable collection records therefore remain recognized. Reaching the final book early does not release the ending or mark previous books complete.

`metadata.js` exports `routeMetadata` and testable `createRouteMetadataStore(storage)`. Its independent key `sutrazen.play.route-metadata.v1` stores only:

- `knownBookIds`
- `openedBookIds`
- `playedAnimationIds`

Methods: `get()`, `get issue`, `markKnown(id)`, `markOpened(id)`, `markAnimation(sceneOrRewardId)`, `reset()`. It emits `sutrazen:route-metadata`, never collection-completion events. A malformed metadata record containing completed IDs or reader positions is rejected. Optional metadata storage failure does not affect existing reading/collection records.

Call `markOpened(id)` when actually opening a known free-reading entry if needed. Do not call `store.complete` from a route view, from title discovery, or from an animation skip. Playing/skipping/replaying an animation never changes earned rewards.

## Ending boundary

`endingAvailable` means the fourteen-ID condition is met. `ending.implemented` remains **false**: this module provides the agreed future endpoint and author-supplied SA262 quotation, not a new fully written or illustrated story. The ending is not a fifteenth book and does not add a completion count. The quote is labelled SA262, not SN35.245.

## Targeted verification

Run `node play/route/check-route.mjs`. It checks document order, canonical boundaries, all 16,384 completion subsets against the explicit combination requirements, out-of-order acquisition and placement, guardian preview, independent garden/irrigation, faculty-source links, final reveal versus ending, recommendation, duplicate/unknown IDs, and metadata isolation against old identifiable and unrecognized save records. It does not re-run the unchanged 1,192-step reader content or claim browser/artwork verification.
