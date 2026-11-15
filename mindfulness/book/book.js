const $ = selector => document.querySelector(selector);
const pages = BOOK.scenes;
const storageKey = 'sutrazen-mindfulness-page';
let current = 0;
let zoom = 1;
const assetUrl = path => '../../docs/mindfulness/' + path;

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function artwork(frame, scene, zoomed = false) {
  frame.replaceChildren();
  frame.style.setProperty('--ratio', scene.dimensions[0] / scene.dimensions[1]);
  const image = element('img');
  if (!zoomed) image.id = 'art';
  image.src = assetUrl(scene.image);
  image.alt = scene.alt;
  image.width = scene.dimensions[0]; image.height = scene.dimensions[1]; image.draggable = false;
  frame.append(image);
  const labels = element('div', 'art-overlays');
  for (const overlay of scene.artOverlay) {
    const label = element('div', 'art-label', overlay.text);
    label.style.left = overlay.x + '%'; label.style.top = overlay.y + '%';
    label.style.width = overlay.width + '%'; label.style.fontSize = overlay.fontSizeCqw + 'cqw';
    label.style.textAlign = overlay.align; label.dataset.color = overlay.color;
    labels.append(label);
  }
  frame.append(labels);
  if (scene.summaryRows.length) {
    const summary = element('div', 'summary-overlay');
    summary.style.setProperty('--scrim', scene.scrimOpacity);
    for (const [i, text] of scene.summaryRows.entries()) {
      const row = element('p', 'summary-row', text);
      row.style.top = (25 + 12 * i) + '%'; summary.append(row);
    }
    frame.append(summary);
    if (zoomed) summary.classList.add('zoom-summary');
  }
}

function quoteCard(group) {
  const card = element('article', 'scripture-card');
  card.dataset.quoteId = group.quoteId;
  card.dataset.afterParagraph = group.afterParagraph;
  const relation = group.relation === '原片下方引文對應' ? '對照經文' : group.relation;
  card.append(element('p', 'quote-relation', relation));
  card.append(element('h3', '', group.source));
  for (const mapping of group.mappings) {
    card.append(element('p', 'quote-mapping', '口白第' + mapping.paragraphs.join('、') + '段 · ' + mapping.focus));
  }
  card.append(element('blockquote', '', group.text));
  const link = element('a', '', '經文與來源影格');
  link.href = '../#' + group.quoteId; card.append(link);
  return card;
}

function showPage(index) {
  const scene = pages[index];
  if (!scene) return;
  current = index;
  try { sessionStorage.setItem(storageKey, String(index)); } catch {}
  // Keep chapter-entry URLs current so returning from a source preserves reading position.
  const readingUrl = new URL(location.href);
  readingUrl.searchParams.set('scene', scene.id);
  history.replaceState(null, '', readingUrl);
  $('.page').dataset.scene = scene.id;
  $('.page').classList.toggle('summary-scene', Boolean(scene.summaryRows.length));
  $('#page-title').textContent = scene.title;
  artwork($('#art-frame'), scene);
  const content = $('#reading-content'); content.replaceChildren();
  for (const [i, paragraph] of scene.paragraphs.entries()) {
    const p = element('p', 'narration-paragraph', paragraph.text);
    p.id = paragraph.id; p.dataset.paragraph = i + 1; content.append(p);
    for (const group of scene.quotes.filter(q => q.afterParagraph === i + 1)) content.append(quoteCard(group));
  }
  if (scene.id === 'S01') {
    const link = element('a', 'paper-link', '閱讀研究論文 PDF');
    link.href = assetUrl('references/A_Wandering_Mind_Is_an_Unhappy_Mind.pdf');
    link.target = '_blank'; link.rel = 'noopener noreferrer'; content.append(link);
  }
  $('#summary-cards').replaceChildren(...scene.summaryRows.map(text => element('p', 'summary-card', text)));
  const labelReading = $('#label-reading');
  labelReading.hidden = !scene.artOverlay.length;
  labelReading.open = false;
  labelReading.querySelector('div').replaceChildren(...scene.artOverlay.map(o => element('p', '', o.text)));
  $('#previous').disabled = index === 0;
  $('#next').disabled = index === pages.length - 1;
  $('#page-select').value = scene.id;
  $('#position-text').textContent = `${index + 1} / ${pages.length} 頁`;
  $('.reading-text').scrollTop = 0;
  $('.scene').scrollTop = 0;
  $('.reader').scrollTop = 0;
  if (window.scrollY) window.scrollTo(0, 0);
  const next = pages[index + 1];
  if (next && next.image !== scene.image) new Image().src = assetUrl(next.image);
  requestAnimationFrame(summaryLayout);
}

function summaryLayout() {
  const summary = $('#art-frame .summary-overlay');
  if (!summary) { $('#summary-cards').hidden = true; return; }
  const onImage = $('#art-frame').getBoundingClientRect().width >= 900;
  summary.hidden = !onImage;
  $('#summary-cards').hidden = onImage;
}
new ResizeObserver(summaryLayout).observe($('#art-frame'));

for (const [i, scene] of pages.entries()) $('#page-select').add(new Option(`${String(i + 1).padStart(2, '0')} · ${scene.title}`, scene.id));
$('.controls').hidden = false;
$('#previous').onclick = () => showPage(current - 1);
$('#next').onclick = () => showPage(current + 1);
$('#page-select').onchange = event => showPage(pages.findIndex(s => s.id === event.target.value));
let saved = 0;
try { saved = Number(sessionStorage.getItem(storageKey) || 0); } catch {}
const requestedScene = new URLSearchParams(location.search).get('scene');
const requestedIndex = pages.findIndex(s => s.id === requestedScene);
showPage(requestedIndex >= 0 ? requestedIndex : Number.isInteger(saved) && pages[saved] ? saved : 0);

function zoomLayout() {
  if (!$('#image-dialog').open) return;
  $('#zoom-frame').style.width = $('#zoom-scroll').clientWidth * zoom + 'px';
  $('#zoom-level').textContent = Math.round(zoom * 100) + '%';
  $('#zoom-out').disabled = zoom <= 1; $('#zoom-in').disabled = zoom >= 4;
}
$('#open-image').onclick = () => {
  zoom = 1; artwork($('#zoom-frame'), pages[current], true);
  $('#image-dialog').showModal(); zoomLayout();
  $('#zoom-scroll').scrollTo(0, 0);
};
$('#zoom-in').onclick = () => { zoom = Math.min(4, zoom + .5); zoomLayout(); };
$('#zoom-out').onclick = () => { zoom = Math.max(1, zoom - .5); zoomLayout(); };
window.addEventListener('resize', () => { zoomLayout(); summaryLayout(); });

function fullscreenLabel() {
  $('#fullscreen').textContent = document.fullscreenElement || document.body.classList.contains('fullscreen-fallback') ? '退出全螢幕' : '全螢幕';
}
$('#fullscreen').onclick = async () => {
  if (document.fullscreenElement) await document.exitFullscreen();
  else if (document.body.classList.contains('fullscreen-fallback')) document.body.classList.remove('fullscreen-fallback');
  else if (document.documentElement.requestFullscreen) {
    try { await document.documentElement.requestFullscreen(); }
    catch { document.body.classList.add('fullscreen-fallback'); }
  } else document.body.classList.add('fullscreen-fallback');
  fullscreenLabel();
};
document.addEventListener('fullscreenchange', fullscreenLabel);
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && document.body.classList.contains('fullscreen-fallback')) {
    document.body.classList.remove('fullscreen-fallback'); fullscreenLabel();
  }
  if ($('#image-dialog').open || event.target.closest('select,input,textarea,.reading-text') || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
    event.preventDefault(); showPage(current + (event.key === 'ArrowRight' ? 1 : -1));
  }
});
let touch;
$('.art-column').addEventListener('touchstart', event => {
  touch = event.touches.length === 1 && !event.target.closest('button,a') ? {x:event.touches[0].clientX,y:event.touches[0].clientY} : null;
}, {passive:true});
$('.art-column').addEventListener('touchcancel', () => { touch = null; });
$('.art-column').addEventListener('touchend', event => {
  if (!touch) return;
  const dx = event.changedTouches[0].clientX - touch.x, dy = event.changedTouches[0].clientY - touch.y;
  touch = null;
  if (!window.getSelection()?.toString() && Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.5) showPage(current + (dx < 0 ? 1 : -1));
}, {passive:true});
