// Match the other readers: caption above the complete artwork, scripture below.
const $ = selector => document.querySelector(selector);
const pages = BOOK.pages;
const storageKey = 'sutrazen-iddhipada-page';
const sceneStarts = new Map(BOOK.scenes.map(scene => [scene.id, scene.start]));

let current = 0;
let measuredScene = null;
function paragraph(text) {
  const p = document.createElement('p'); p.textContent = text; return p;
}
function overlays(container, plan) {
  container.replaceChildren(...(plan?.artOverlay || []).map(o => {
    const label = document.createElement('div');
    label.className = 'art-overlay'; label.textContent = o.text; label.dataset.color = o.color;
    if (o.mobileMode === 'outside_image_when_width_below_600px') label.dataset.smallHint = 'true';
    for (const [key, value] of Object.entries({
      '--overlay-x': o.x + '%', '--overlay-y': o.y + '%', '--overlay-width': o.width + '%',
      '--overlay-font': o.fontSizeCqw + 'cqw', '--label-color': o.color, '--label-align': o.textAlign || 'center', '--label-line-height': '1.15',
    })) label.style.setProperty(key, value);
    return label;
  }));
}
function scriptureText(item) {
  return item.quotes.map(q => q.source + '\n' + (q.sourceType === 'pali_with_editorial_chinese_paraphrase' ? q.translationNote + '\n\n巴利原文：\n' + q.originalText : q.originalText + '\n\n' + q.translationNote)).join('\n\n');
}
function renderScripture(item) {
  const verse = $('#verse'); verse.replaceChildren();
  for (const quote of item.quotes) {
    const card = document.createElement('article'); card.className = 'scripture-card'; card.dataset.quoteId = quote.quoteId; card.dataset.sourceType = quote.sourceType;
    const source = document.createElement('h3'); source.textContent = quote.source; card.append(source);
    if (quote.sourceType === 'pali_with_editorial_chinese_paraphrase') {
      const chinese = paragraph(quote.translationNote); chinese.className = 'chinese-paraphrase';
      const label = paragraph('巴利原文'); label.className = 'original-label';
      const original = document.createElement('blockquote'); original.className = 'pali-original'; original.lang = 'pi'; original.textContent = quote.originalText;
      card.append(chinese, label, original);
    } else {
      const body = document.createElement('blockquote'); body.className = 'source-quotation'; body.textContent = quote.originalText;
      card.append(body);
      if (quote.translationNote) {
        const note = paragraph(quote.translationNote); note.className = 'source-note'; card.append(note);
      }
    }
    verse.append(card);
  }
}
function renderSummary(item) {
  const summary = $('#summary-text'); summary.replaceChildren();
  for (const entry of item.textSummary || []) {
    const section = document.createElement('section'); const heading = document.createElement('h3'); heading.textContent = entry.title; section.append(heading);
    for (const text of entry.paragraphs) section.append(paragraph(text));
    if (entry.rows.length) {
      const table = document.createElement('table'); const caption = document.createElement('caption'); caption.textContent = '內容對照'; table.append(caption);
      for (const [title, steps] of entry.rows) {
        const row = document.createElement('tr'), name = document.createElement('th'), content = document.createElement('td');
        name.scope = 'row'; name.textContent = title; content.textContent = steps; row.append(name, content); table.append(row);
      }
      section.append(table);
    }
    summary.append(section);
  }
  if (item.editorialNote) {
    const footer = document.createElement('section'); const heading = document.createElement('h3'); heading.textContent = '閱讀說明'; footer.append(heading, ...item.editorialNote.map(paragraph)); summary.append(footer);
  }
}

function showPage(index) {
  const item = pages[index]; if (!item) return;
  current = index;
  try { sessionStorage.setItem(storageKey, String(index)); } catch {}
  const url = new URL(location.href);
  url.searchParams.set('scene', item.scene); url.searchParams.set('page', String(index + 1));
  history.replaceState(null, '', url);
  const plan = BOOK.scenes.find(s => s.id === item.scene);
  const page = $('.page'); page.dataset.scene = item.scene; page.dataset.paragraph = item.paragraphId || ''; page.dataset.startSeconds = item.startSeconds ?? ''; page.dataset.endSeconds = item.endSeconds ?? '';
  page.classList.toggle('afterword-scene', Boolean(item.afterword));
  page.classList.toggle('text-summary-scene', Boolean(item.textSummary));
  $('#page-title').textContent = item.title;
  $('#narration').replaceChildren(...item.lines.map(paragraph));
  $('#caption').hidden = Boolean(item.textSummary);
  $('#caption-sizer').hidden = Boolean(item.afterword || item.summary);
  if (measuredScene !== item.scene) {
    measuredScene = item.scene;
    $('#caption-sizer').replaceChildren(...pages.filter(p => p.scene === item.scene).map(p => {
      const wrapper = document.createElement('div'); wrapper.append(...p.lines.map(paragraph)); return wrapper;
    }));
  }
  $('#art-frame').hidden = !item.image;
  if (item.image) {
    if ($('#art').getAttribute('src') !== item.image) $('#art').src = item.image;
    $('#art').alt = plan.alt;
    $('#art-frame').style.setProperty('--art-ratio', item.dimensions.join(' / '));
    $('#art-frame').style.setProperty('--art-ratio-number', String(item.dimensions[0] / item.dimensions[1]));
  }
  overlays($('#art-overlays'), plan);
  $('#summary-overlay').replaceChildren(...(plan?.summaryRows || []).map((text, i) => {
    const row = paragraph(text); row.className = 'summary-row'; row.style.top = (25 + 12 * i) + '%'; return row;
  }));
  $('#summary-text').replaceChildren(...(plan?.summaryRows || []).map(paragraph));
  renderScripture(item);
  renderSummary(item);
  $('.scripture').hidden = !item.quotes.length && !item.sourceNote && !item.context;
  $('.verse-body').scrollTop = 0;
  $('#source-link').hidden = !item.quotes.length;
  if (item.quotes.length) $('#source-link').href = '../index.html#' + item.quotes[0].quoteId;
  else $('#source-link').removeAttribute('href');
  $('#open-verse').hidden = !item.quotes.length;
  $('#previous').disabled = index === 0; $('#next').disabled = index === pages.length - 1;
  $('#page-select').value = item.scene;
  $('#position-text').textContent = `${index + 1} / ${pages.length} 頁`;
  $('.scene').scrollTop = 0;
  if (window.scrollY) window.scrollTo(0, 0);
  const next = pages.slice(index + 1).find(p => p.image && p.image !== item.image);
  if (next) new Image().src = next.image;
  layoutArtwork();
}
function layoutArtwork() {
  const scene = $('.scene');
  const caption = $('#caption-sizer').getBoundingClientRect().height;
  const scripture = $('.scripture').hidden ? 0 : $('.scripture').getBoundingClientRect().height;
  scene.style.setProperty('--caption-space', caption + 'px');
  scene.style.setProperty('--scripture-space', scripture + 'px');
  scene.style.setProperty('--image-space-height', Math.max(1, scene.clientHeight - caption - scripture) + 'px');
  $('#closing-shade').hidden = true; $('#summary-text').hidden = !pages[current].textSummary;
  const narrow = $('#art-frame').getBoundingClientRect().width < 600;
  $('#art-frame').classList.toggle('small-art', narrow);
  const hints = BOOK.scenes.find(s => s.id === pages[current].scene).artOverlay.filter(o => o.mobileMode === 'outside_image_when_width_below_600px');
  $('#outside-labels').hidden = !narrow || !hints.length || !pages[current].image;
  $('#outside-labels').textContent = hints.length ? '由左到右：' + hints.map(o => o.text).join('／') : '';
  $('.page').classList.toggle('has-outside-labels', !$('#outside-labels').hidden);
  scene.style.setProperty('--hint-space', $('#outside-labels').getBoundingClientRect().height + 'px');
}
const observer = new ResizeObserver(layoutArtwork);
observer.observe($('#caption-sizer')); observer.observe($('.scripture')); observer.observe($('#art-frame'));
observer.observe($('#outside-labels'));
window.addEventListener('resize', layoutArtwork); document.fonts.ready.then(layoutArtwork);
for (const scene of BOOK.scenes) $('#page-select').add(new Option(`${scene.id.slice(1)} · ${scene.title}`, scene.id));

$('.controls').hidden = false; $('#hint').hidden = false;
$('#previous').onclick = () => showPage(current - 1); $('#next').onclick = () => showPage(current + 1);
$('#page-select').onchange = () => showPage(sceneStarts.get($('#page-select').value));
let saved = 0;
try {
  const stored = sessionStorage.getItem(storageKey);
  saved = stored === null ? 0 : Number(stored);
} catch {}
const requested = new URLSearchParams(location.search);
const requestedPage = Number(requested.get('page')) - 1, requestedScene = requested.get('scene');
const start = requestedScene && sceneStarts.has(requestedScene)
  ? (pages[requestedPage]?.scene === requestedScene ? requestedPage : sceneStarts.get(requestedScene))
  : (Number.isInteger(saved) && pages[saved] ? saved : 0);
showPage(start);
$('#open-verse').onclick = () => {
  const item = pages[current]; $('#dialog-verse').textContent = scriptureText(item);
  $('#dialog-source').hidden = !item.quotes.length;
  if (item.quotes.length) $('#dialog-source').href = '../index.html#' + item.quotes[0].quoteId;
  document.querySelectorAll('.additional-source').forEach(el => el.remove());
  for (const quote of item.quotes.slice(1)) {
    const link = document.createElement('a'); link.className = 'additional-source';
    link.textContent = '查看經典出處 · ' + quote.source; link.href = '../index.html#' + quote.quoteId; $('.verse-scroll').append(link);
  }
  $('#verse-dialog').showModal(); $('.verse-scroll').scrollTop = 0;
};
// Enlarge the complete image without introducing a separate persistent toolbar.
$('#art').tabIndex = 0; $('#art').setAttribute('role', 'button');
$('#art').setAttribute('aria-haspopup', 'dialog'); $('#art').title = '點選放大圖片';
let swiped = false;
function enlargeImage() {
  const item = pages[current]; if (!item.image || swiped) return;
  $('#zoom-art').src = item.image; $('#zoom-art').alt = $('#art').alt;
  const plan = BOOK.scenes.find(s => s.id === item.scene);
  overlays($('#zoom-overlays'), plan);

  $('#zoom-shade').hidden = true;
  $('#image-dialog').showModal(); $('.image-scroll').scrollTo(0, 0);
}
$('#art').onclick = enlargeImage;
$('#art').onkeydown = event => {
  if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); enlargeImage(); }
};
const readingText = 'select,input,textarea,.verse-body,.verse-scroll,#summary-text';
document.addEventListener('keydown', event => {
  if ($('#verse-dialog').open || $('#image-dialog').open || event.target.closest(readingText) ||
      event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
    event.preventDefault(); showPage(current + (event.key === 'ArrowRight' ? 1 : -1));
  }
});
let touchStart;
$('.page').addEventListener('touchstart', event => {
  swiped = false;
  touchStart = event.touches.length === 1 && !event.target.closest('a,' + readingText)
    ? {x: event.touches[0].clientX, y: event.touches[0].clientY} : null;
}, {passive:true});
$('.page').addEventListener('touchcancel', () => { touchStart = null; });
$('.page').addEventListener('touchend', event => {
  if (!touchStart) return;
  const dx = event.changedTouches[0].clientX - touchStart.x, dy = event.changedTouches[0].clientY - touchStart.y; touchStart = null;
  if (!window.getSelection()?.toString() && Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.5) {
    swiped = true; showPage(current + (dx < 0 ? 1 : -1));
  }
}, {passive:true});
matchMedia('(orientation:portrait)').addEventListener('change', event => {
  if (event.matches && $('#verse-dialog').open) $('#verse-dialog').close();
});
