# SutraZen project context

## Project
- GitHub repository: https://github.com/Sutra-Zen/sutra-zen.github.io
- GitHub Pages entry point: https://sutra-zen.github.io/
- Related Buddhist learning map: https://sutrazen.netlify.app/map.html
- Primary language: Traditional Chinese (Taiwan)

## Current outer ocean and overview return (2026-11-22)

Latest game follow-up: [outer ocean / overview handoff](play/game-ocean-overview/README.md). Original 1600×900 geography and all anchors remain unchanged, with an outer-sea display frame and camera-safe dock inset. Overview fits the enlarged frame and offers a visible return arrow restoring the previous camera; old camera/session and reading progress remain compatible. Twelve QA evidence directories are excluded from Pages only. Exact publication status is recorded by the new PR's merge-SHA Pages/live checks; physical Safari remains untested.

## Current full-window map and bottom overlay (2026-11-22)

Latest follow-up to PR61: [full-window/dock handoff](play/game-fullscreen-dock/README.md), branch `feat/game-fullscreen-dock` from `ab311d9a2e030cf7e608e3bd9bc83a006445532e`. This supersedes the earlier separated top HUD/bottom navigation layout. Map fills the entire usable viewport; all common controls share a translucent single bottom row with local horizontal scrolling/arrows at narrow widths. Title is centered; an actual miniature castle is half clipped by the west world boundary at the harbor. A reproduced single-touch capture hand-off cancellation on labels is fixed in camera.js. Store/eligibility/reader content and the world source graph stay unchanged. Eleven QA directories are excluded from Pages, whose source remains main:/. Actual validation/screenshots: [evidence](previews/game-fullscreen-dock/README.md). Exact merge/Pages/live status belongs to the new PR release record; real Safari is untested.

## Current game immersion and shared progression (2026-11-22)

Latest game implementation: [immersion handoff](play/game-immersion/README.md), branch `feat/game-immersion-sequential`, from published PR60 merge `7e39f04a383ab98d3b747365ea3e513ad7140a0e`. This supersedes older free-selection / arbitrary-bookmark / player review-all descriptions below; those sections retain historical design and test evidence. The original fourteen public book URLs remain free.

`/game/` uses the author's unchanged 2752×1536 cat-cover JPEG, HTML title/buttons, then an immersive map/city/shelf shell. `play/worldmap-v4/index.html` is the source for `scripts/build-game-entry.py`; root-relative module imports replace the old `<base>` approach. Shared `route/eligibility.js` governs every game entry and completion write: first unfinished only, completed-book review only, historical non-sequential completions retained. Future bookmarks remain stored without unlocking or changing the mainline. Shelf reviews return to the shelf without rewards. Completion feedback goes back to the map and focuses the next station before opening a book.

All world layers share one 1600×900 camera transform with drag/pinch, visible controls, readable labels and session camera persistence. The harbor city marker and fixed city tab share the same page. Full「念-守門人」labels and canonical city correspondences remain. Settings hold backups and secondary site/source navigation; developer art inspection is isolated from game storage. The new shell is never injected into public readers.

615 protected original files are byte-identical to the baseline. `_config.yml` now excludes ten game QA directories only; legacy Pages main:/, homepage, SEO, Google verification and original content remain. Five-size UI tests, native first-book completion/review, storage/eligibility/history models and camera gestures pass; real iPhone/iPad Safari remains untested. See [actual evidence](previews/game-immersion/README.md). Publication follows existing author authorization and a new PR; exact merge-SHA Pages/live evidence is recorded in that PR, not inferred from this implementation status. Notion is unavailable; [pending note](play/game-immersion/PENDING_NOTION.md) is provided.

## Public game entry release (2026-11-22)

The author explicitly authorized this round's publication at `https://sutra-zen.github.io/game/`, superseding the earlier game-preview-only restrictions. `release/game-first-playable` starts from reviewed prototype `a2b3225`, which already contains current main `b9a0dad2`; [release PR60](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/60) targets main while retaining the prototype review history. The PR's delivery record must confirm the actual merge SHA, Pages result and live checks before the public URL is claimed available.

`game/index.html` mounts the existing worldmap shell using an explicit base URL; `scripts/build-game-entry.py` keeps the intentional title/base/brand/badge differences reproducible. Runtime, book data, images, saved book IDs and storage keys remain shared. The opt-in reader bridge accepts only the existing worldmap return, the new `game` return, or the default collection shelf. City, shelf and source return links lead to `/game/`; standalone original books retain their interface. The public trial is deliberately noindex, with the existing fifteen-page SEO/Google files preserved.

Sea-map labels are 「安那般那與止觀竹林」 and 「六念燈塔」. The city audience scene places the crowned moustached/goateed lord forward by the plaza, with black-white/calico messengers and an open cream scroll. Editable labels read 「地水火風四大廣場」「止・觀使者」「如實消息・涅槃」; the message leader uses the scroll's image-relative center. Scroll and facial hair are story artwork, not additions to the canonical allegory.

`_config.yml` preserves legacy main:/ Pages publishing and only excludes nine game QA evidence directories from its artifact; all Git history, older preview URLs, original documents, book images and source PDFs remain. The source-size estimate falls from about957MB to775MB before this round's small assets. See `docs/play/game-release/` for the runtime asset manifest and limitations, and `docs/previews/play-game-release/` on GitHub for actual checks/screenshots. Real iPhone/iPad Safari remains untested unless a later record says otherwise.

## Current status and deployment (verified 2026-11-19)

The owner renamed `rooneyflower-star/sutrazen-map` to `Sutra-Zen/sutra-zen.github.io`; GitHub repository ID 1441581789 and commit history are unchanged. Baseline main `2ec341a6ffa1a4f0108183da980e9af85c55bd31` includes all fourteen released books and the latest Anapana scripture/comic-focus corrections. Older dated preview restrictions below describe historical work; use the newest HANDOFF entry and the current user's authorization.

GitHub Pages API confirms `build_type: legacy`, source `main` at `/`, `cname: null`, HTTPS enforced, and https://sutra-zen.github.io/ as the production entry. GitHub manages the `dynamic/pages/pages-build-deployment` workflow; there is no tracked custom Actions release workflow or application build requirement. Preserve this branch-source method. Implement from latest main on a branch, open a PR against main, merge only when authorized, verify the exact merge SHA's successful Pages build, and test the current domain. A pushed commit or a successful local test alone does not prove live availability.

Website files use relative paths and work from `/`; do not prepend the old project path. The cloud mount `/workspace/sutrazen-map` is intentionally retained to avoid breaking existing local paths. `origin` now points to `https://github.com/Sutra-Zen/sutra-zen.github.io.git`. Local testing: from the repository root run `python3 -m http.server 8765 --bind 127.0.0.1`, then open `http://127.0.0.1:8765/`. For an existing check script with its own port, use that port or set `SUTRAZEN_TEST_URL` to the served repository root URL.

Original author-supplied handoff documents, manifests, screenshots and historical report hashes are archival inputs; old names within them are retained. Maintained guide/test instructions and pending release notes use the new URLs. Each release still needs a fixed-merge-SHA ZIP backup and Notion update or an explicit pending note if tools are unavailable.

## Repository structure (verified 2026-11-19)

- `index.html` — 修道地圖、十四本書架及影片入口；`shelf.css` — 書架樣式。
- `four-truths/` — 01 四聖諦。
- `five-aggregates/` — 02 五陰。
- `six-senses/` — 03 六處。
- `twelve-links/` — 04 十二因緣。
- `eightfold-path/` — 05 八正道與十善業道。
- `four-fruits-ten-fetters/` — 06 四向四果與十結。
- `four-purities-six-recollections/` — 07 四不壞淨與六念。
- `mindfulness/` — 08 四念處與四顛倒。
- `right-effort/` — 09 四正勤。
- `anapana/` — 10 安那般那與止觀。
- `iddhipada/` — 11 四如意足。
- `four-jhanas/` — 12 四禪。
- `five-roots-powers/` — 13 五根五力。
- `seven-factors/` — 14 七覺支。
- 各目錄 `index.html` 是導讀，`book/` 是既有閱讀器；圖片、來源與分鏡依各書原有慣例保留。
- 根目錄 `reader-controls.css`、`reader-restart.js`、`picture-panel-focus.js/css` 為共用操作。
- `docs/` — 交接、原稿與驗證；`scripts/` — 各書建置及檢查；`downloads/` — 既有離線包。

The twelve-link reader is implemented in twelve-links/ and preserves 77 pages: 18 narrative scenes plus an afterword. The author approved publication on 2026-11-14. Verify the corresponding GitHub Pages deployment before claiming live availability.

## Independent city preview (2026-11-22, not published)

`/play/city/` now owns the complete six-gate city scene. Opted-in preview headers share `play/navigation.js/css`: sea map, original mind map, castle icon + city, shelf. The city keeps a primary continue-reading action, a sea-map return, image-relative editable labels, feature explanations and original-book rereading. `?review=all` shows an explicitly marked full-art review without changing saved progress; default entry reads the real collection. Old `visual-v2/?view=city` entries redirect here and retain a valid review parameter. The small harbor-city illustration remains future artwork, not an additional map button in this round.

The new crowned lord concept adds an eight-shaped moustache while retaining the chin beard; black-white and calico messengers remain separate. Native art is1672×941, not4K or fully separated animation layers. Completion dialogs show only a compact reward feature with “continue next book” primary and “see city” secondary; they no longer embed the full city. The misleading harbor/eightfold-station diagonal follows the coastal road. A separate geographic-only path connects Four Jhanas → Iddhipada → harbor, without changing the original46 source relations or route progression. Details, limitations and screenshots: `docs/play/city-entry/` and `docs/previews/play-city-entry/`.

## World landscape map-v4 and route-r3 (2026-11-22, not published)

The current draft adds `/play/worldmap-v4/`: a shared1600×900 two-row/five-column landscape, fog without map locks, editable labels, original relation overlays and route-r3 recommendations. All fourteen existing readers remain supported; collection completion IDs are the sole source for map/shelf/city rewards. The optional `collectionReturn=worldmap-v4` integration returns only this new entry to real city feedback; default collection and standalone readers retain their behavior. New cat city art has the crowned short-bearded orange lord, black-white/calico messengers and an independent wooden Dharma dock. See `docs/play/worldmap-v4/README.md` and `docs/previews/play-worldmap-v4/`. The3840×2160 exports are browser renders, while the native illustration remains1672×941; full native4K/layered art and the complete ending remain pending. DraftPR59 is still against the prototype branch, with no main merge/deployment authorized; latest main remains `b9a0dad2`.

## Art-direction comparison preview (2026-11-21, not published)

The existing `preview/journey-visual-v2` draft now includes original-watercolor / terrain / fantasy-world map comparisons, a new no-grid top-down six-gate city and bound-book collection covers. Only proposal visuals change; source graph, collection/journey storage, fourteen reader files and production site are unchanged from `dedc066`. See `docs/play/visual-v2/ART-DIRECTIONS.md` and `docs/previews/play-art-directions/`. Main remains `b9a0dad2`; no merge or publication is authorized.

## Collection and continent preview (2026-11-21, not published)

`preview/journey-visual-v2` now includes a connected bottom continent with topic mountains and a shelf for collecting fourteen books. An independent `sutrazen.play.collection.v1` store and opt-in reader module support explicit end-of-book completion across all fourteen originals; each book HTML only adds the module, preserving standalone behavior. The first-three-book journey remains separate. See `docs/play/collection/README.md` and newest HANDOFF for actual1192-step verification, art limitations and local entry routes. PR59 is a draft against the prototype branch, with no main merge or public deployment authorized.

## Picture-book journey prototype (2026-11-21, not published)

Branch `feat/picture-book-journey-v1` adds an isolated `/play/` prototype for the first three original books, opt-in reader progress and a six-gate SN35.245 castle sketch. It does not replace the map, promote itself from the homepage or change Pages. No merge/deployment is authorized for this task. Run a local root HTTP server and open `/play/`; see `docs/play/README.md` for implementation boundaries, source verification, provisional character art, save schema and validation. The proposed production URL is not evidence of public availability.

## Visual and reading experience
- Picture-book visual language: gentle hand-drawn children's illustration, recurring kitten character where appropriate, 16:9 artwork.
- Prefer concise, accurate Traditional Chinese on illustrations; narration and textual content should be faithful to cited Buddhist texts.
- Navigation and layout should remain consistent across books, particularly portrait/landscape arrangements and touch controls on iPad.
- Before making a shared component, compare the actual behavior of existing books. Existing books may not yet use one common implementation.

## Collaboration model
1. ChatGPT and the author finalize research, storyboard, narration, artwork, and functional requirements.
2. Approved decisions are summarized in docs/HANDOFF.md.
3. Codex reads AGENTS.md, docs/PROJECT.md, docs/HANDOFF.md and the real codebase.
4. Codex implements a limited change and tests it, reporting what is verified versus pending.
5. The author reviews on iPad; only then proceed with any explicitly approved production publication.

## Important distinction
This repository does not necessarily contain every asset or HTML draft discussed in ChatGPT. If a required draft is absent, ask the author to supply it; do not fabricate missing content.

## Twelve-link release approval (2026-11-14)
The author reviewed two preview revisions and explicitly requested publication. The approved implementation includes native guide/book pages, original artwork, corrected scripture navigation and keyboard behavior, refined birth/name-and-form endpoints and the Four Noble Truths-style YouTube preview. See docs/HANDOFF.md for test coverage and remaining limitations.

## Eightfold Path release approval (2026-11-14)
Implemented on `feat/eightfold-path-preview` from main `0236fca`, incorporating handoff `e121f3c`. Shelf #05 and the existing 八正道 map dialog link to the guide/reader in this branch. The four released books and shared guide styles remain unchanged. The author explicitly authorized direct publication of this version on 2026-11-14. PR #11 targets main; verify its merge commit and corresponding Pages deployment before claiming live availability. See docs/eightfold-path/verification.md for source checks, pairing choices and separate editorial suggestions.

## Image overlays and panel focus release approval (2026-11-14)
Branch `fix/picture-book-overlays` starts from published main `51d6572`. Eightfold Path uses independent image-space topic overlays stored in each storyboard scene's `presentation`. Six Senses adds focus to its six quad scenes; Five Aggregates uses the actual three-panel illustration. The author explicitly authorized direct publication of this correction via PR #12; verify the merge commit and Pages deployment before claiming live availability. See the newest HANDOFF and `docs/previews/picture-book-overlays/README.md`.

## Reader labels and open scripture (2026-11-14)
`fix/reader-labels-and-scripture` starts from main `f01ffa8`. Six Senses eighteen-realm labels align to measured image-window columns; Eightfold Path removes the mistaken ten-evil prefix from 心不定 and the redundant 正業 heading in the wholesome quad. SA771 keeps the verified transcription with a four-line whitespace-only display variant. The 13 original scenes/110 subtitles remain, with a separate afterword at page111 saying interpretation follows the original scriptures. Scripture sections in all five guides show their existing text directly. Publication follows the author's instruction to inspect this ongoing book work on the live site; confirm the new PR merge and Pages run.

## Shared reader touch controls
All five readers load root `reader-controls.css`; future readers must include it too. Navigation buttons use `touch-action: manipulation` in both orientations, preserving pinch zoom and scrolling. AGENTS.md records this as a production requirement.

## Book 06 preview (2026-11-14)

`feat/four-fruits-ten-fetters-preview` starts from main `bc29ec6`. It adds `four-fruits-ten-fetters/` and `four-fruits-ten-fetters/book/`, importing only the handoff folder from `content/four-fruits-ten-fetters-handoff` at `d82957317cd6733553c97149ebb49d1bd7bd7bad`; original images come from the author's uploaded ZIP and match all manifest hashes. The preview has 11 scenes / 74 subtitle pages, 15 scripture cue states and no image-space overlays. Shelf #06 and the existing 四向四果 map dialog are connected in this branch. All five published books, common CSS and Pages settings remain unchanged. This book is **for review only**: do not merge or publish without the author's next instruction. See the latest HANDOFF and `docs/previews/four-fruits-ten-fetters/README.md` for preview access and device-test limits.

## Book 07 release (2026-11-15)

`four-purities-six-recollections/` adds the seventh guide and reader from main `31ebc8679723ab9908f771436bc0563cc4b04270`, based on the author's ZIP. Eight original illustrations, 93 subtitle pages, a same-image closing page, and an editorial afterword make 95 pages. Six chapter labels and the two-line ending use the handoff's actual-image percentage coordinates; all original assets and six existing books remain unchanged. Uses shared guide styles, reader controls and last-page restart. The author explicitly authorized direct publication in this task. Verify the actual merge commit and successful Pages run before claiming it is live.

## Author corrections (2026-11-15)

Book 07 image assignments were confirmed reversed by the author: S06 uses IMG_0400.jpeg (sangha, deer/elephant/field), S07 uses IMG_0401.jpeg (white protective hull). Runtime assignments are recorded separately from the original handoff. All seven books' final sentence now ends「走入經藏的起點」, without「溫柔」. Book 07's requested explanatory paragraph was removed; scripture cards and original story content remain.

## Book 08: 四念處與四顛倒 (2026-11-15)

`mindfulness/` and `mindfulness/book/` implement the author's complete four-package v3 handoff in `docs/mindfulness/`: 25 scenes, 92 actual narration paragraphs, 18 scripture records and 27 paragraph mappings. Shelf #08 and the existing 四念處／四顛倒 map dialogs are connected; eight books are now readable and six remain locked. All seven existing books, shared styles/scripts and Pages configuration remain unchanged from main `24983232d11bc9e775641bf444bcbe59055fe1ad`.

The initial 25-page whole-scene reader was replaced at the author's request with the established book 06/07 caption-above / full-image / scripture-below layout. The complete 92 narration paragraphs are paginated into 109 caption pages, followed by the existing summary and a new scripture-basis afterword (111 pages total). Menu, page counter, scripture dialog, portrait/landscape controls and restart follow book 07. Image overlays keep the original top-left percentages, including when enlarging an image. Source cards now use the same icons, Chinese scripture/translation and annotation/Pali buttons, edition/translator/provider labels and directly visible excerpts as existing books. Seven official source files were read and hash-verified; original video transcriptions remain unchanged and differences are recorded separately. Four polished body/feeling/mind/dhamma summaries are integrated into the guide. Full assets, PDF and reference frames remain. Publication authorization from package04 persists; verify merge SHA, Pages success and public files before claiming the correction is live.

The MA98 source card now groups 11 source-verified excerpts under body, feeling, mind and dhamma, including six elements, corpse contemplation, the detailed feeling categories, inner/outer contemplation and five hindrances. MA98/MA102 annotation links use the author's exact deep anchors. The public source-frame card was removed at the author's request; frames remain in the repository and are described in the pending Notion note. The reader and other books are unchanged.

## Book 09: 四正勤 (2026-11-15)

`right-effort/` and `right-effort/book/` add the ninth guide and reader from the author's two ZIPs, verified against all 33 manifest entries. Eleven scenes contain 80 full narration paragraphs plus the original closing text card, producing 81 pages. The existing book 08 controls, scripture dialog, source-card UI, image enlargement and restart are reused. The author's latest correction restores the standard caption-above / complete-artwork / scripture-below arrangement in both orientations, superseding the old handoff's below-image narration instruction. Shelf09 and the existing 四正勤 map dialog are connected, with the original video RqWhPhhP8eY. Source names, actual-image overlays and scene-specific scripture switches follow the intact handoff. Original eight books and shared files remain unchanged. The author explicitly authorized publication; verify merge SHA, Pages success, public files and a fixed-SHA full ZIP at delivery. Source differences remain separate from the original narration/quotes.

At the author's follow-up request, S03's four-panel and S07's six-panel comics use the existing shared picture-panel-focus.js/css. Paragraph-to-panel mapping and measured image-space boundaries live in right-effort/book/panel-focus-data.js. Noncurrent panels receive the same 76% dimming as older books; overview/closing paragraphs show the entire image. Enlarged images and orientation changes retain the focus. Original artwork, all 81 pages and S10's separate 60% summary shade remain unchanged.

## Book 10 review implementation — 2026-11-16

`feat/anapana-review` starts from latest main `0034db754a478bbce76c79b0dbe7479822dfee76`. `anapana/` adds the guide and `anapana/book/` the existing caption-above / complete-artwork / scripture-below reader. The two complementary author ZIPs are intact under `docs/anapana/`: 11 original illustrations, 12 scenes, 118 unchanged narration paragraphs, 41 video-transcribed quotes and 12 image-relative overlays. There are 119 reader pages including the selectable S12 summary. Shelf10 and the existing 安那般那與止觀 map node are connected only in the review branch; all nine previous books, shared assets and Pages settings remain unchanged. S10 switches its three small labels outside the image below an actual displayed width of600px; enlargement retains image/label alignment. Guide source cards distinguish Āgama/MN118 from later commentarial material. See the newest HANDOFF, `docs/anapana/REVIEW_TODO.md` and `docs/previews/anapana/README.md`.

**Publication authorized 2026-11-16:** after receiving the review implementation, the author explicitly requested direct publication. This supersedes the earlier review-only restriction. Publish via PR #28, verify the actual merge SHA and Pages build/public files, and provide a fixed-SHA full ZIP. See the newest HANDOFF and final PR verification; do not infer deployment from the earlier preview checks.

## Book 11: 四如意足 — review only (2026-11-16)

`feat/iddhipada-review` starts from main `140f62221726485916f3992d8ea6f5782e7507b5`. `iddhipada/` and `iddhipada/book/` implement the author's two complete ZIPs, intact under `docs/iddhipada/`: 9 scenes, 81 timed narration paragraphs, 11 scripture cards, 13 image-relative overlays and 9 formal images. One editorial afterword makes82 reader pages. Uses the current Anapana reader and source-card design, shared touch controls/restart, full-image enlargement and scene navigation. Shelf11 and the existing 四如意足 map dialog are connected in this review branch only; all ten previous books/shared files/Pages settings remain unchanged. No merge or public deployment is authorized. Preview/PDF/screenshots: `docs/previews/iddhipada/README.md`; source and timing review: `docs/iddhipada/REVIEW_TODO.md`.

**Publication authorized 2026-11-16:** the author subsequently requested「直接發布吧」. This supersedes the preceding book11 review-only restriction. Publish the reviewed implementation through PR #34, remove public noindex/preview markers and retain all original content. Verify the actual merge SHA, matching successful Pages build, public files and a fixed-merge-SHA full ZIP; final evidence belongs in PR #34.

## Book 11 source copy cleanup (2026-11-17)

Following publication via PR #34 (main97dc5fb), the author's correction replaces S08's public video-transcribed quote with the verified SN51.11 Zhuang translation and removes its editorial explanation. Three displayed paraphrases no longer refer to internal Q03 IDs. Original handoff files stay intact; reader-edits.json drives both runtime data and the review PDF. Narration, page counts, mappings and artwork remain unchanged. See the newest HANDOFF for release verification and the pending Notion note.

## Book12: 四禪 — review implementation (2026-11-18)

`feat/four-jhanas-review` starts from mainc4e6670. `four-jhanas/` and `four-jhanas/book/` add the guide and existing Anapana caption/art/scripture UI. The intact handoff in docs/four-jhanas contains10 scenes,130 timed subtitle cues,8 quote cards and11 original images including credits. Two added editorial/credits pages make132 pages; the menu stays10 scenes. Shelf12 and the existing 四禪 map node are connected in this branch. Seven image-space overlays, four-column panel focus, selectable summary table, enlargement, scripture/source navigation and shared restart are retained. The corrected S08/S09 files and SHA-256 are verified. All11 existing books/shared files/Pages configuration remain unchanged. New-book publication is not authorized; do not merge or deploy without a subsequent publication request. Preview/PDF/screenshots: docs/previews/four-jhanas/README.md; source details: docs/four-jhanas/REVIEW.md.

**Publication authorized 2026-11-18:** the author explicitly requested「直接發佈吧」after delivery. This supersedes book12's earlier review-only restriction. Publish the reviewed implementation via PR #36, remove public noindex/preview markers, and verify the merge SHA, matching Pages build/public files and full fixed-SHA ZIP. The original ten scenes,130 captions,eight quote cards and previous eleven books stay unchanged. Final release evidence belongs in PR #36.

## Book12: remove credits page (2026-11-18)

At the author's request, the standalone credits screenshot page is removed from the published reader and review PDF. The130 original timed captions now lead straight to the editorial afterword:131 reader pages,10 menu scenes; PDF24 pages. Guide scripture sources and all original handoff files remain. The generator reflects the removal, and old132-page links/session positions clamp to the current final page. See newest HANDOFF and docs/previews/four-jhanas-ending for scoped verification.

## Reader corrections: 四禪 / 安那般那 (2026-11-18)

The author requested maintenance of the published readers. Four Jhanas S10 keeps its original comparison artwork and scripture, removes the duplicate HTML/dialog table and updates the PDF; S05瞋恚 moves from y29% to17% above the face. Anapana S04–S07 use the unchanged shared panel-focus helper, with16 measured column rectangles and paragraph-specific focus. Intro/closing pages stay full frame; zoom/rotation follow the same focus. Both original page counts, timed narration, scripture data and all artwork remain. See newest HANDOFF and docs/previews/reading-focus for scoped340-page-state/80-zoom validation; physical Safari remains untested.

## Book11 comic focus (2026-11-18)

At the author's request, the published Iddhipada reader adds shared76% noncurrent-panel dimming to S01's four columns and S06's2x2 deviations. S08 remains a full-frame overview because its narration discusses all four together. Focus is keyed by scene-local page offset, not the book's global paragraphNumber. Enlargement and rotation stay synchronized; the82-page data,81 timed paragraphs,11 scripture cards,13 overlays and all artwork/source text remain unchanged. Scoped115-page/40-zoom/35-noncomic checks and screenshots are in docs/previews/iddhipada-focus; physical Safari remains untested.

## Book13: 五根五力 review (2026-11-18)

`feat/five-roots-powers-review` starts from main2376c9c after the separate Anapana S08 focus release(PR40). The author's two ZIPs provide10 scenes,74 timed cues and11original PNGs; all are intact in docs/five-roots-powers. The new guide and current Anapana-style reader connect shelf13 and the existing map node in this branch only.74subtitle pages plus the original enlargeable sources image and editorial afterword make76pages. Five black overlays use the supplied top-left percentages; S03's five signs remain baked text. Five verified canonical source cards preserve the distinction from14video-transcribed Qcards. All12old books/shared files/Pages remain unchanged. New-book merge/deployment is not authorized; review PDF,380-page-state/25overlay-zoom/5credits-zoom checks and30screenshots are in docs/previews/five-roots-powers.

**Book13 publication authorized 2026-11-18:** the author explicitly requested「可以直接發佈五根五力」. This supersedes the preceding review-only restriction. Publish the validated implementation through PR41, remove noindex/review cache markers and preserve all content, artwork and previous12books. Verify the merged SHA, matching successful Pages build/public files and fixed-SHA full ZIP, with final evidence in PR41.

## Book14: 七覺支 review (2026-11-18)

`feat/seven-factors-review` starts from main99b1a1d. Two author ZIPs provide12story images,one source screenshot and36timed narration paragraphs. The reader keeps12image pages, with within-page cue controls so narration/scripture/S11focus switch together; existing portrait-bottom/landscape-side page controls remain.14overlays use center percentages and image-height font sizes; S08/S09 stay distinct; S12baked labels are not duplicated. Five canonical source cards and a29-file offline ZIP are added only for this book. Actual main had no downloader; new guide download button uses existing source styles.180online/180downloaded-extracted-local-HTTP-with-external-origins-blocked cue states,120zoomed labels and13legacy reader regressions passed. file:// is blocked by managed Chromium and not verified; physical Safari likewise untested. New book is review-only; do not merge/deploy without new authorization. See docs/previews/seven-factors for12page PDF/37screenshots/download and docs/seven-factors/REVIEW.md.

**Book14 publication authorized 2026-11-18:** the author explicitly requested「可直接發佈」after review delivery. This overrides the preceding review-only restriction. Publish the approved12page/36cue implementation through PR43, remove noindex/review cache markers, rebuild the same-content offline ZIP, and verify matching Pages commit/public files/download plus a fixed-SHA full backup. Physical Safari/file:// restrictions remain; do not imply those have been tested.

## Seven Factors continuous reading fix (2026-11-18)

The original36cues were intact, but main navigation advanced image pages and skipped within-scene narration unless the reader used separate cue controls. Main buttons, keyboard and swipes now traverse all36cues before changing the12images; the separate cue toolbar is removed and the shared restart only triggers at cue36. Guide download/source-screenshot links are removed at the author's request; canonical source cards remain. New main-control forward/reverse/offline regression covers the complete reading path. See newest HANDOFF and docs/previews/seven-sequence/.


## All-reader map navigation and reading bands (2026-11-20)

All fourteen readers now keep the same source/map pair, with a direct root map action in both orientations, and use「本頁經文」for their scripture dialog. Shared reader-controls.css reserves the correct actual scene gutter. The original four readers and Eightfold Path plain scenes load reader-layout.js to preserve complete-image caption/art/scripture bands; text/Heart Sutra/afterword pages and original scene data remain. See the newest HANDOFF and docs/previews/reader-navigation for local and publication verification; the author explicitly authorized publication of this correction.

## Practice-map resource cards (2026-11-21)

All 32 clickable map dialogs use the approved three-card presentation: guide / picture book / video, with lavender / blue / coral backgrounds. Thirty topic/subtopic nodes link to the existing fourteen guides/readers and original videos. The two broad overview nodes direct to the existing shelf/video sections with explicit selection wording. Keep concise explanations intact and use map-topic-resources.css for future nodes. Publication was explicitly authorized by the author; verification and release evidence belong in the latest HANDOFF entry and PR.

## Website SEO and ownership file (2026-11-21-r2)

The 15 home/guide pages use the approved r2 titles, descriptions and canonical URLs from docs/seo/seo_pages.json. scripts/build-seo.py manages metadata/sitemap/robots and verifies the permanent root Google file googlee0c995331ec518ae.html (original53bytes). Four existing guide generators apply scripts/site_seo.py at the end; other guides remain hand-maintained HTML. Details and per-page list: docs/seo/README.md. Reader content, metadata, artwork, controls, map32nodes, shelf14books and PR54 source correction remain. Pages still uses main:/.

The user explicitly authorized publishing this batch and the real verification file together in their final supplement. For this SEO batch, Notion, vidIQ, Search Console account actions and search-performance tracking belong to the original ChatGPT conversation. Codex installs and verifies the public files; no Google account verification or indexing outcome is implied.
