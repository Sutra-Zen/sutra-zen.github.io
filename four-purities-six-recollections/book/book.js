// Navigation and layout follow the current Twelve Links reader.
const pages = BOOK.pages;
const $ = selector => document.querySelector(selector);
const page = $('.page'), title = $('#page-title'), art = $('#art'), artFrame = $('#art-frame');
const verse = $('#verse'), sourceLink = $('#source-link'), select = $('#page-select');
const previous = $('#previous'), next = $('#next'), verseDialog = $('#verse-dialog');
const storageKey = 'sutrazen-four-purities-six-recollections-page';
const sceneStarts = new Map(BOOK.scenes.map(scene => [scene.id, scene.start]));
const artworkDescriptions = {
 S01:'小貓隨法行、兔子隨信行，兩條溪流合入須陀洹與涅槃的主流；原圖四處標示完整保留。',
 S02:'船上小貓與兔子，四張木牌分別寫親近善友、聽聞正法、內正思惟、法次法向。',
 S03:'左邊轉輪王坐在雲上寶座、下方漩渦；右邊衣著樸素的兔子在金色光罩中讀書。',
 S04:'遠方佛像放射光芒，湖面小船載著小貓與兔子。',
 S05:'書本發出光芒，小貓望遠方、兔子手捧清水，乘船航行。',
 S06:'小貓與兔子乘船航行，金色光罩圍繞著小船。',
 S07:'小貓與兔子安坐船中，光罩與右上鹿、象和田地完整可見。',
 S08:'小船航行在波浪中，六張原圖木牌：念佛、念法、念僧、念戒、念施、念天。',
 END:'沿用六念完整原圖，覆蓋六成五暗幕，顯示兩行收尾語。',
};
let current = 0;

function showPage(index) {
  const item = pages[index];
  if (!item) return;
  current = index;
  try { sessionStorage.setItem(storageKey, String(index)); } catch {}
  title.textContent = item.title;
  $('#narration').replaceChildren(...item.lines.map(text => {
    const paragraph = document.createElement('p');
    paragraph.textContent = text;
    return paragraph;
  }));
  applySceneLayout(item);
  page.classList.toggle('afterword-scene', Boolean(item.afterword));
  page.classList.toggle('end-scene', Boolean(item.end));
  $('#caption').hidden = Boolean(item.end);
  $('#caption-sizer').hidden = Boolean(item.end || item.afterword);
  $('#closing-shade').hidden = !item.end;
  artFrame.hidden = !item.image;
  if (item.image) {
    if (art.getAttribute('src') !== item.image) art.src = item.image;
    art.alt = artworkDescriptions[item.scene];
    artFrame.style.setProperty('--art-ratio', item.dimensions.join(' / '));
    artFrame.style.setProperty('--art-ratio-number', String(item.dimensions[0] / item.dimensions[1]));
  }
  verse.textContent = [item.verseLabel, item.verse].filter(Boolean).join('\n');
  $('.scripture').hidden = !item.verseLabel;
  $('.verse-body').scrollTop = 0;
  sourceLink.hidden = !item.source;
  if (item.source) sourceLink.setAttribute('href', item.source);
  else sourceLink.removeAttribute('href');
  $('#open-verse').hidden = !item.image || !item.verseLabel;
  previous.disabled = index === 0;
  next.disabled = index === pages.length - 1;
  select.value = String(item.scene);
  $('#position-text').textContent = `${index + 1} / ${pages.length} 頁`;
  // A long text chapter must start at its top on both orientations.
  $('.scene').scrollTop = 0;
  if (window.scrollY) window.scrollTo(0, 0);
  const upcoming = pages.slice(index + 1).find(p => p.image && p.image !== item.image);
  if (upcoming) new Image().src = upcoming.image;
  layoutArtwork();
}

let measuredScene = null;
function applySceneLayout(item) {
  const plan = BOOK.scenes.find(scene => scene.id === item.scene);
  page.dataset.scene = item.scene;
  page.dataset.captionColor = plan.topSubtitleLayout.color;
  const overlays = plan.artOverlay.filter(o => item.atSec >= o.startSec && item.atSec < o.endSec);
  $('#art-overlays').replaceChildren(...overlays.map(o => {
    const el = document.createElement('div');
    el.className = 'art-overlay';
    el.textContent = o.text;
    el.style.setProperty('--overlay-x', o.xPct + '%');
    el.style.setProperty('--overlay-y', o.yPct + '%');
    el.style.setProperty('--overlay-width', o.maxWidthPct + '%');
    el.style.setProperty('--overlay-font', o.fontSizePctOfImageWidth + 'cqw');
    return el;
  }));
  if (measuredScene !== item.scene) {
    measuredScene = item.scene;
    $('#caption-sizer').replaceChildren(...pages.filter(p => p.scene === item.scene).map(p => {
      const wrapper = document.createElement('div');
      wrapper.append(...p.lines.map(text => {const paragraph = document.createElement('p'); paragraph.textContent = text; return paragraph;}));
      return wrapper;
    }));
  }
}
function layoutArtwork() {
  const scene = $('.scene');
  const captionHeight = $('#caption-sizer').getBoundingClientRect().height;
  const scriptureHeight = $('.scripture').hidden ? 0 : $('.scripture').getBoundingClientRect().height;
  scene.style.setProperty('--caption-space', captionHeight + 'px');
  scene.style.setProperty('--scripture-space', scriptureHeight + 'px');
  scene.style.setProperty('--image-space-height', Math.max(1, scene.clientHeight - captionHeight - scriptureHeight) + 'px');
}
const layoutObserver = new ResizeObserver(layoutArtwork);
layoutObserver.observe($('#caption-sizer'));
layoutObserver.observe($('.scripture'));
window.addEventListener('resize', layoutArtwork);
document.fonts.ready.then(layoutArtwork);

for (const scene of BOOK.scenes) {
  select.add(new Option(['afterword', 'END'].includes(scene.id) ? scene.title : `${scene.id.slice(1)} · ${scene.title}`, scene.id));
}
$('.controls').hidden = false;
$('#hint').hidden = false;
let saved = 0;
try { saved = Number(sessionStorage.getItem(storageKey) || 0); } catch {}
showPage(Number.isInteger(saved) && pages[saved] ? saved : 0);

previous.onclick = () => showPage(current - 1);
next.onclick = () => showPage(current + 1);
select.onchange = () => showPage(sceneStarts.get(select.value));
$('#open-verse').onclick = () => {
  $('#dialog-verse').textContent = verse.textContent;
  $('#dialog-source').hidden = sourceLink.hidden;
  if (!sourceLink.hidden) $('#dialog-source').setAttribute('href', sourceLink.getAttribute('href'));
  verseDialog.showModal();
  $('.verse-scroll').scrollTop = 0;
};
const readingText = 'select,input,textarea,.verse-body,.verse-scroll';
document.addEventListener('keydown', event => {
  if (verseDialog.open || event.target.closest(readingText) ||
      event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
    event.preventDefault();
    showPage(current + (event.key === 'ArrowRight' ? 1 : -1));
  }
});
let touchStart;
page.addEventListener('touchstart', event => {
  // Selecting text and scrolling scripture must never turn the page.
  if (event.touches.length !== 1 || event.target.closest('a,' + readingText)) {
    touchStart = null; return;
  }
  touchStart = { x: event.touches[0].clientX, y: event.touches[0].clientY };
}, { passive: true });
page.addEventListener('touchcancel', () => { touchStart = null; });
page.addEventListener('touchend', event => {
  if (!touchStart) return;
  const dx = event.changedTouches[0].clientX - touchStart.x;
  const dy = event.changedTouches[0].clientY - touchStart.y;
  touchStart = null;
  if (window.getSelection()?.toString()) return;
  if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.5) {
    showPage(current + (dx < 0 ? 1 : -1));
  }
}, { passive: true });
matchMedia('(orientation:portrait)').addEventListener('change', event => {
  if (event.matches && verseDialog.open) verseDialog.close();
});
