// Reuse the current reader controls, with book 09 narration and scripture below the artwork.
const $ = selector => document.querySelector(selector);
const pages = BOOK.pages;
const storageKey = 'sutrazen-right-effort-page';
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
    for (const [key, value] of Object.entries({
      '--overlay-x': o.leftPct + '%', '--overlay-y': o.topPct + '%', '--overlay-width': o.widthPct + '%',
      '--overlay-font': o.fontSizeCqw + 'cqw', '--label-color': o.color === 'black' ? '#111' : '#fff', '--label-align': o.align, '--label-line-height': String(o.lineHeight),
    })) label.style.setProperty(key, value);
    return label;
  }));
}
function scriptureText(item) {
  return item.quotes.map(q => [q.relation === '原片下方引文' ? q.source : q.relation + ' · ' + q.source, q.text].join('\n')).join('\n\n');
}
function showPage(index) {
  const item = pages[index]; if (!item) return;
  current = index;
  try { sessionStorage.setItem(storageKey, String(index)); } catch {}
  const url = new URL(location.href);
  url.searchParams.set('scene', item.scene); url.searchParams.set('page', String(index + 1));
  history.replaceState(null, '', url);
  const plan = BOOK.scenes.find(s => s.id === item.scene);
  const page = $('.page'); page.dataset.scene = item.scene; page.dataset.paragraph = item.paragraphId || '';
  page.classList.toggle('afterword-scene', Boolean(item.afterword));
  page.classList.toggle('summary-scene', Boolean(item.summary));
  $('#page-title').textContent = item.title;
  $('#narration').replaceChildren(...item.lines.map(paragraph));
  $('#caption').hidden = Boolean(item.summary);
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
  const focus = PANEL_FOCUS.scenes[item.scene];
  SutraZenPanelFocus.update($('#art-frame'), $('#art'), focus, item.paragraphNumber);
  const activePanel = focus?.panels.find(panel => panel.id === focus.pages[item.paragraphNumber - 1]);
  if (activePanel) $('#art').alt += '，目前閱讀：' + activePanel.label;
  $('#summary-overlay').replaceChildren(...(plan?.summaryRows || []).map((text, i) => {
    const row = paragraph(text); row.className = 'summary-row'; row.style.top = (25 + 12 * i) + '%'; return row;
  }));
  $('#summary-text').replaceChildren(...(plan?.summaryRows || []).map(paragraph));
  $('#verse').textContent = scriptureText(item);
  $('.scripture').hidden = !item.quotes.length;
  $('.verse-body').scrollTop = 0;
  $('#source-link').hidden = !item.quotes.length;
  if (item.quotes.length) $('#source-link').href = '../#' + item.quotes[0].quoteId;
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
  const opacity = BOOK.scenes.find(s => s.id === pages[current].scene).darkOverlayOpacity;
  $('#closing-shade').hidden = !opacity; $('#closing-shade').style.opacity = String(opacity); $('#summary-text').hidden = true;
}
const observer = new ResizeObserver(layoutArtwork);
observer.observe($('#caption-sizer')); observer.observe($('.scripture')); observer.observe($('#art-frame'));
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
  if (item.quotes.length) $('#dialog-source').href = '../#' + item.quotes[0].quoteId;
  document.querySelectorAll('.additional-source').forEach(el => el.remove());
  for (const quote of item.quotes.slice(1)) {
    const link = document.createElement('a'); link.className = 'additional-source';
    link.textContent = '查看經典出處 · ' + quote.source; link.href = '../#' + quote.quoteId; $('.verse-scroll').append(link);
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
  SutraZenPanelFocus.update($('#zoom-frame'), $('#zoom-art'), PANEL_FOCUS.scenes[item.scene], item.paragraphNumber);
  $('#zoom-shade').hidden = !plan.darkOverlayOpacity; $('#zoom-shade').style.opacity = String(plan.darkOverlayOpacity);
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
