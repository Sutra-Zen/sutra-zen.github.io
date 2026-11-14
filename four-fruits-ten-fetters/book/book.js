// Navigation and layout follow the current Twelve Links reader.
const pages = BOOK.pages;
const $ = selector => document.querySelector(selector);
const page = $('.page'), title = $('#page-title'), art = $('#art'), artFrame = $('#art-frame');
const verse = $('#verse'), sourceLink = $('#source-link'), select = $('#page-select');
const previous = $('#previous'), next = $('#next'), verseDialog = $('#verse-dialog');
const storageKey = 'sutrazen-four-fruits-ten-fetters-page';
const sceneStarts = new Map(BOOK.scenes.map(scene => [scene.id, scene.start]));
const artworkDescriptions = {
  S01: '小貓想像飛天超人與雲上城堡，思索彼岸的意義。',
  S02: '小貓安坐於鎖鏈之間。左側：身見、戒取、疑、貪欲、瞋恚；右側：色愛、無色愛、慢、掉舉、無明。',
  S03: '四隻小貓分別穿白袍持羽、戴王冠持劍、背錢袋和持工具，表示不同社會出身。',
  S04: '四隻穿著相同衣服的小貓走在金光下的同一條階梯上。',
  S05: '小狗繞著木柱奔跑，柱上直排五受陰，皮帶上寫貪愛。',
  S06: '智慧之劍斬斷皮帶，小狗離開木柱，象徵初果斷三結。',
  S07: '欲望雲將彩色染料注入水鍋，底下烈火使水沸騰。',
  S08: '撤去底火的水鍋，水面轉為清澈平靜。',
  S09: '木門的門閂斷裂，左側貪、右側瞋二字完整可見，門縫透出光芒。',
  S10: '閃電截斷棕櫚樹的樹冠，保留樹幹、斷裂處與墜落的樹冠。',
  S11: '繁忙辦公室中，小貓安坐在光罩內，周圍人們仍為各種事情煩心。',
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
  artFrame.hidden = !item.image;
  if (item.image) {
    if (art.getAttribute('src') !== item.image) art.src = item.image;
    art.alt = artworkDescriptions[item.scene];
    artFrame.style.setProperty('--art-ratio', item.dimensions.join(' / '));
    artFrame.style.setProperty('--art-ratio-number', String(item.dimensions[0] / item.dimensions[1]));
  }
  verse.textContent = item.verse ? item.verseLabel + '\n' + item.verse : '';
  $('.scripture').hidden = !item.verse;
  $('.verse-body').scrollTop = 0;
  sourceLink.hidden = !item.source;
  if (item.source) sourceLink.setAttribute('href', item.source);
  else sourceLink.removeAttribute('href');
  $('#open-verse').hidden = !item.image || !item.verse;
  previous.disabled = index === 0;
  const lastPage = index === pages.length - 1;
  next.disabled = false;
  next.setAttribute('aria-label', lastPage ? '回到第一頁' : '下一頁');
  next.innerHTML = lastPage ? '<span class="portrait-label">回到第一頁 </span><span aria-hidden="true">↺</span>' : '<span class="portrait-label">下一頁 </span><span aria-hidden="true">→</span>';
  next.classList.toggle('restart', lastPage);
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
  // artOverlay is intentionally empty in every author-approved scene.
  $('#art-overlays').replaceChildren();
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
  select.add(new Option(scene.id === 'afterword' ? scene.title : `${scene.id.slice(1)} · ${scene.title}`, scene.id));
}
$('.controls').hidden = false;
$('#hint').hidden = false;
let saved = 0;
try { saved = Number(sessionStorage.getItem(storageKey) || 0); } catch {}
showPage(Number.isInteger(saved) && pages[saved] ? saved : 0);

previous.onclick = () => showPage(current - 1);
next.onclick = () => showPage(current === pages.length - 1 ? 0 : current + 1);
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
