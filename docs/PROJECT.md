# SutraZen project context

## Project
- GitHub repository: https://github.com/rooneyflower-star/sutrazen-map
- GitHub Pages entry point: https://rooneyflower-star.github.io/sutrazen-map/
- Related Buddhist learning map: https://sutrazen.netlify.app/map.html
- Primary language: Traditional Chinese (Taiwan)

## Repository structure (verified 2026-11-14)
- index.html — top-level site entry
- shelf.css — shared shelf styling
- five-aggregates/ — five aggregates picture book, including book/ and storyboard.csv
- four-truths/ — Four Noble Truths picture book, including assets/ and book/
- six-senses/ — six senses picture book, including book/ and cover.webp
- twelve-links/ — twelve-link picture book, guide, static Wheel of Life, 77-page data, storyboard and original extracted assets
- eightfold-path/ — Eightfold Path / Ten Wholesome Actions implementation: 111-page reader (110 original subtitle pages plus an editorial afterword) and guide; original 13-scene handoff and 11 illustrations in docs/eightfold-path/
- README.md

The twelve-link reader is implemented in twelve-links/ and preserves 77 pages: 18 narrative scenes plus an afterword. The author approved publication on 2026-11-14. Verify the corresponding GitHub Pages deployment before claiming live availability.

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
