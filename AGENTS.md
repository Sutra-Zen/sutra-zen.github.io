# SutraZen — Codex project instructions

## Current repository and release target (verified 2026-11-19)
- Repository: https://github.com/Sutra-Zen/sutra-zen.github.io (GitHub repository ID 1441581789).
- Production: https://sutra-zen.github.io/ ; serve this repository at the domain root, with no project-path prefix.
- This is the renamed original project. Continue its existing history, fourteen books, illustrations and approved fixes.
- The current cloud checkout may still be `/workspace/sutrazen-map`; that is a local mount name, not a website URL. Verify `git remote -v` and current main before working; preserve local edits.
- GitHub Pages currently uses `main` and `/` (legacy branch source), with GitHub's managed `pages-build-deployment` workflow. Keep this method. When publication is authorized, use a reviewable branch/PR into main, then verify the exact merge SHA's Pages build and live behavior.
- Use current URLs in new work. Original handoff packages and historical artifact hashes stay intact; their old project names do not override this section.

## Purpose
Maintain the SutraZen Buddhist learning website and its interactive picture books. The human author discusses Buddhist source texts, storyboards, illustrations, narration, and interaction design in ChatGPT. Codex implements approved changes in this repository.

## Start of every task
1. Read this file, docs/PROJECT.md, and docs/HANDOFF.md.
2. Inspect the actual repository before modifying code. Treat documentation as context, not proof that a feature exists.
3. Follow the user's latest task instruction. If it conflicts with the handoff, ask before overwriting approved content.
4. Prefer small, reviewable changes. Do not recreate a picture book from scratch when existing source can be updated.
5. Do not assume unpublished artwork or HTML is present in GitHub. Request the missing asset/source when needed.

## Design and content rules
- Traditional Chinese (Taiwan) is the primary UI language. Proofread all Chinese labels carefully.
- Preserve the established gentle hand-drawn children's picture-book style and consistent kitten character wherever relevant.
- Respect the original Buddhist references and distinguish scripture quotations from creative explanatory narration.
- Preserve the established 16:9 illustration style where applicable.
- Maintain usability on iPad/iPhone, including portrait and landscape layouts.
- Reuse established navigation, reading controls, and interaction patterns from existing books rather than introducing inconsistent controls.
- Every web reader must include the same reading-links pair:「閱讀原經」to its guide sources and「回修道地圖」to `../../index.html`, usable in portrait and landscape; the scripture dialog action is「本頁經文」. Reserve space for both links so they never cover scripture.
- The original first four readers and the plain scenes of Eightfold Path load root `reader-layout.js` for image-free caption/scripture bands; keep their image-relative overlays and special text/scripture pages intact.
- For new readers, use the current book 06/07 caption-above / complete-artwork / scripture-below layout and its existing scripture dialog, menu and portrait/landscape controls. Paginate long narration without dropping text; do not replace this with a whole-scene sidebar reader.
- Source sections use the shared source cards: scripture title, edition/translator, original Chinese/translated text button, annotated-guide or Pali-comparison button, provider labels and directly visible excerpts. Video screenshots are supplementary evidence, not replacements for scripture access.
- End each book with the established editorial note explaining its actual Āgama/scripture basis and that interpretation follows the original scriptures, followed by the shared restart action. Keep「走入經藏的起點」without「溫柔」.
- Do not let annotations obscure important artwork or scripture text.
- Avoid adding unnecessary signposts, labels, or UI elements.
- Practice-map dialogs use the shared `map-topic-resources.css` cards in this order:「專頁說明」「翻頁繪本」「繪本影片」(lavender / blue / coral). Preserve concise descriptions, link subtopics to their existing parent resources, and label overview links explicitly when they lead to the shelf/video sections.

## Engineering and release safeguards
- Inspect index.html, shelf.css, and the relevant book directory before changing shared navigation.
- Preserve working books and their routes; do not delete or rename existing assets without explicit approval.
- Validate HTML/CSS/JS and test interactive buttons, navigation, image loading, and mobile portrait/landscape behavior as far as the environment permits.
- If browser testing is unavailable, report that limitation explicitly. Never claim a successful visual test without performing one.
- Do not deploy or merge into the production branch unless the user explicitly requests publication. Prefer a branch/PR for review when possible.
- Report which files changed, what was tested, and the preview or published URL only when verified.
- Update docs/HANDOFF.md after completing a task, recording what changed and what remains unverified.

## Source of truth
Actual repository files and verified live behavior govern implementation status. docs/HANDOFF.md records design decisions and outstanding work, not proof of deployment.

## Buddhist source discovery
- Actively research references rather than treating an unsuccessful search or network denial as proof that a source is absent.
- For annotations to all four Chinese Āgamas, start at https://buddhaspace.org/main/modules/dokuwiki/ and follow the appropriate collection/volume/section. The site is not limited to 雜阿含; do not apply one collection's path pattern to another.
- For Pali canon references, look for a verified Traditional Chinese translation and identify the translator; present Chinese access before comparison languages where available. Preserve distinct labels for ancient Chinese texts, modern translations, Pali originals and annotations.
- If a provider is blocked, inspect its authoritative public data repository when available and clearly distinguish verified source content from an untested website URL. Do not ask the author to find material that can be researched independently.

## Reader touch controls (all current and future books)
- Every book reader must load the root `reader-controls.css` using the appropriate relative path (currently `../../reader-controls.css`).
- Keep previous/next buttons inside `.controls`; shared `touch-action: manipulation` prevents rapid taps from triggering double-tap zoom in portrait and landscape. Preserve pinch zoom and normal scrolling; do not use `user-scalable=no`, `maximum-scale=1`, or document-wide touch prevention.
- Verify computed touch-action and rapid previous/next taps at phone/iPad portrait and landscape sizes. Real Safari gesture behavior must be reported separately from Chromium simulation.

## SEO and Google verification (2026-11-21-r2)
- Fifteen public guide/homepage heads use docs/seo/seo_pages.json via scripts/site_seo.py; run `python3 -B scripts/build-seo.py --check` after guide work. Guide builders must apply the shared metadata after generating head content. Keep reader metadata separate.
- Preserve root `googlee0c995331ec518ae.html` byte-for-byte permanently; never delete, rename, template, move, or replace it during releases. Its SHA-256 is recorded in docs/seo/site-verification.json.
- Keep sitemap at the root with canonical URLs, retain existing robots rules (search and model-training policies are independent), and use only verified data in sharing/structured metadata.
