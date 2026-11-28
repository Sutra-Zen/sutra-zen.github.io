import { BOOKS, store } from './progress.js?v=summary-merge-1';
import { t } from './i18n.js?v=summary-merge-1';
import { renderCity } from './city.js?v=summary-merge-1';
const app = document.querySelector('#journey-app');
const dialog = document.querySelector('#journey-dialog');
const body = document.querySelector('#dialog-body');
const notice = document.querySelector('#journey-notice');
let view = store.get().mode === 'free' ? 'free' : 'home';
let feedback = null;
let timer;
const qs = new URLSearchParams(location.search);
const complete = qs.get('completed'), freeRead = qs.get('freeRead');
if (BOOKS.some(b => b.id === complete) && store.get().completed.includes(complete)) feedback = { id: complete, free: false };
if (BOOKS.some(b => b.id === freeRead)) feedback = { id: freeRead, free: true };
if (feedback) history.replaceState(null, '', location.pathname);
const portrait = () => `<svg class="sz-traveler" viewBox="660 275 370 450" role="img" aria-label="${t.travelerAlt}"><image href="../seven-factors/assets/11.webp" x="0" y="0" width="1671" height="941"/></svg>`;
function notify(text) { notice.textContent = text; notice.hidden = !text; }
function storageNotice() { if (store.issue) notify(store.issue === 'corrupt' ? t.storageCorrupt : t.storageUnavailable); }
function primaryBook() { const s = store.get(); return BOOKS.find(b => b.id === s.replayBook) || BOOKS.find(b => b.id === s.orderedBook && store.canRead(b.id)) || BOOKS.find(b => !s.completed.includes(b.id)) || BOOKS[0]; }
function bookStatus(book, free = false) {
  const s = store.get();
  if (!free && s.completed.includes(book.id)) return 'complete';
  if (!free && !store.canRead(book.id)) return 'locked';
  return Number.isInteger(s[free ? 'freePositions' : 'positions'][book.id]) ? 'reading' : 'available';
}
function bookCard(book, index, free = false) {
  const status = bookStatus(book, free), locked = status === 'locked';
  return `<article class="sz-island sz-${status}" data-book-card="${book.id}"><div class="sz-island-top"><span class="sz-island-number">0${index + 1}</span><span class="sz-status">${locked ? '🔒 ' : status === 'complete' ? '✓ ' : ''}${t.statuses[status]}</span></div>${status === 'complete' || free ? `<img class="sz-thumb" src="${book.thumbnail}" alt="${book.title}既有插畫縮圖" loading="lazy">` : `<div class="sz-topic-symbol" aria-hidden="true">${book.symbol}</div>`}<h3>${book.title}</h3><p>${locked ? t.unlock : status === 'reading' ? t.resumeAt(book.title, (store.get()[free ? 'freePositions' : 'positions'][book.id] || 0) + 1) : status === 'complete' ? t.readAgain : t.read}</p><button class="sz-secondary" data-action="read" data-book="${book.id}" ${locked ? 'disabled' : ''}>${locked ? t.statuses.locked : status === 'reading' ? t.resume : status === 'complete' ? t.readAgain : t.read}</button></article>`;
}
function map() {
  return `<section class="sz-map" aria-labelledby="island-heading"><div class="sz-section-title"><div><p class="sz-kicker">01 → 02 → 03</p><h2 id="island-heading">${t.mapTitle}</h2></div><p>${t.mapHint}</p></div><div class="sz-sea"><div class="sz-islands">${BOOKS.map((b, i) => bookCard(b, i)).join('')}</div><button class="sz-city-marker" data-action="city"><span aria-hidden="true">♜</span><strong>${t.cityMarker}</strong><span>${t.progress(store.get().completed.length)} · ${t.city}</span></button><span class="sz-wave sz-wave-one" aria-hidden="true">∿ ∿ ∿ ∿ ∿</span><span class="sz-wave sz-wave-two" aria-hidden="true">∿ ∿ ∿</span></div></section>`;
}
function render() {
  const s = store.get(), n = s.completed.length;
  app.dataset.view = feedback ? 'feedback' : view;
  if (feedback) {
    const book = BOOKS.find(b => b.id === feedback.id);
    app.innerHTML = `<section class="sz-feedback"><p class="sz-kicker">${feedback.free ? t.free : t.progress(n)}</p><h1>${feedback.free ? t.freeDone(book.title) : n === 3 ? t.allDone : t.completed(book.title)}</h1><p class="sz-large">${feedback.free ? t.freeDoneText : t.feedback[n - 1]}</p>${renderCity(n)}<p class="sz-muted">${t.feedbackNote}</p><button class="sz-primary" data-action="continue">${feedback.free ? t.ordered : n === 3 ? t.shelf : t.continue}</button>${n === 3 && !feedback.free ? `<button class="sz-secondary" data-action="reread">${t.reread}</button>` : ''}<button class="sz-link" data-action="city">${t.blueprint}</button></section>`;
  } else if (view === 'city') {
    app.innerHTML = `<section class="sz-city-view"><button class="sz-link" data-action="home">← ${t.ordered}</button><p class="sz-kicker">${t.progress(n)} · ${t.city}</p><h1>${t.blueprint}</h1><p>${t.cityIntro}</p>${renderCity(n, { blueprint: true })}<a class="sz-secondary" href="sources.html">${t.sources}</a><button class="sz-primary" data-action="start">${n === 3 && !s.replayBook ? t.reread : t.resume}</button></section>`;
  } else if (view === 'free') {
    app.innerHTML = `<section class="sz-free"><p class="sz-kicker">${t.free}</p><h1>${t.freeTitle}</h1><p class="sz-large">${t.freeIntro}</p><button class="sz-primary" data-action="ordered">${t.ordered}</button><div class="sz-islands sz-free-islands">${BOOKS.map((b,i) => bookCard(b,i,true)).join('')}</div></section>${options()}`;
  } else {
    const b = primaryBook(), started = Object.keys(s.positions).length > 0;
    app.innerHTML = `<section class="sz-hero"><div class="sz-hero-copy"><p class="sz-kicker">${t.stage} · ${t.progress(n)}</p><h1>${n === 3 ? t.allDone : t.heading}</h1><p class="sz-large">${n === 3 ? t.allDoneText : t.intro}</p><div class="sz-main-action"><button class="sz-primary" data-action="start">${n === 3 && !s.replayBook ? t.reread : started ? t.resume : t.start}<span aria-hidden="true"> →</span></button><span>${n === 3 && !s.replayBook ? t.stage : started ? t.resumeAt(b.title, (s.positions[b.id] || 0) + 1) : t.first}</span></div><p class="sz-local">${t.savedLocal}</p></div><div class="sz-traveler-card">${portrait()}<p>${t.travelerCaption}</p></div></section>${map()}<section class="sz-city-preview"><div><p class="sz-kicker">${t.progress(n)}</p><h2>${t.city}</h2><p>${t.cityIntro}</p><button class="sz-secondary" data-action="city">${t.blueprint}</button></div>${renderCity(n)}</section><section class="sz-later"><h2>${t.later}</h2><p>${t.laterText}</p><a href="../index.html#books">${t.shelf} →</a><button class="sz-link" data-action="free">${t.free}</button></section>${options()}`;
  }
  storageNotice();
}
function options() { return `<details class="sz-options"><summary>${t.more}</summary><div class="sz-option-actions"><button class="sz-secondary" data-action="backup">${t.backup}</button><label class="sz-file-label">${t.restore}<input id="backup-file" type="file" accept="application/json,.json"></label><button class="sz-link" data-action="clear">${t.clear}</button></div><label class="sz-motion"><input type="checkbox" id="reduce-motion" ${store.get().settings.reducedMotion ? 'checked' : ''}> ${t.reduce}</label><p class="sz-muted">${t.prototypeArt}</p><a href="sources.html">${t.sources}</a></details>`; }
function focusMain() { app.focus(); window.scrollTo({ top: 0, behavior: 'instant' }); }
function navigate(book, mode, restart = false) {
  if (!store.setActive(book.id, mode)) return;
  const state = store.get();
  const index = restart ? 0 : state[mode === 'free' ? 'freePositions' : 'positions'][book.id] || 0;
  if (restart) store.savePosition(book.id, 0, mode);
  const url = new URL(book.path, import.meta.url); url.searchParams.set('journey', mode); url.searchParams.set('playPage', String(index));
  const go = () => { clearTimeout(timer); location.assign(url.href); };
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || state.settings.reducedMotion) { go(); return; }
  body.innerHTML = `<div class="sz-sailing"><p class="sz-kicker">${t.sailing}</p><h2 id="dialog-title">${book.title}</h2><div class="sz-boat" aria-hidden="true">⛵ <span>念</span></div><p>${t.sailingText(book.title)}</p><button class="sz-primary" id="skip-sailing">${t.skip}</button></div>`;
  dialog.showModal(); document.querySelector('#skip-sailing').onclick = go; timer = setTimeout(go, 1700);
}
function confirmAction(title, text, label, action) {
  body.innerHTML = `<h2 id="dialog-title">${title}</h2><p>${text}</p><div class="sz-confirm"><button class="sz-secondary" id="cancel-action">${t.cancel}</button><button class="sz-primary" id="confirm-action">${label}</button></div>`;
  dialog.showModal(); document.querySelector('#cancel-action').onclick = () => dialog.close(); document.querySelector('#confirm-action').onclick = () => { dialog.close(); action(); };
}
app.addEventListener('click', event => {
  const control = event.target.closest('[data-action]'); if (!control || control.disabled) return;
  const action = control.dataset.action;
  if (action === 'start') { const done = store.get().completed.length === 3 && !store.get().replayBook; navigate(done ? BOOKS[0] : primaryBook(), 'ordered', done); }
  if (action === 'read') { const b = BOOKS.find(b => b.id === control.dataset.book); if (b) navigate(b, view === 'free' ? 'free' : 'ordered', view !== 'free' && store.get().completed.includes(b.id)); }
  if (action === 'reread') navigate(BOOKS[0], 'ordered', true);
  if (action === 'city') { feedback = null; view = 'city'; render(); focusMain(); }
  if (action === 'home' || action === 'ordered') { feedback = null; view = 'home'; store.setActive(primaryBook().id, 'ordered'); render(); focusMain(); }
  if (action === 'free') { view = 'free'; store.setActive(store.get().activeBook, 'free'); render(); focusMain(); }
  if (action === 'continue') {
    const free = feedback?.free; feedback = null;
    if (!free && store.get().completed.length === 3) location.assign('../index.html#books');
    else if (free) { view = 'home'; store.setActive(primaryBook().id, 'ordered'); render(); focusMain(); }
    else navigate(primaryBook(), 'ordered');
  }
  if (action === 'clear') confirmAction(t.clearTitle, t.clearText, t.confirmClear, () => { store.reset(); view = 'home'; feedback = null; notify(''); render(); focusMain(); });
  if (action === 'backup') {
    const url = URL.createObjectURL(new Blob([store.exportBackup()], { type: 'application/json' })); const link = document.createElement('a'); link.href = url; link.download = 'sutrazen-journey-v1.json'; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
});
app.addEventListener('change', async event => {
  if (event.target.id === 'reduce-motion') store.setReducedMotion(event.target.checked);
  if (event.target.id !== 'backup-file') return;
  const file = event.target.files[0]; if (!file) return;
  if (file.size > 100000) { notify(t.invalid); event.target.value = ''; return; }
  let text; try { text = await file.text(); } catch { notify(t.invalid); return; }
  event.target.value = '';
  confirmAction(t.restoreTitle, t.restoreText, t.confirmRestore, () => { if (store.restoreBackup(text)) { view = store.get().mode === 'free' ? 'free' : 'home'; render(); notify(store.issue ? t.storageUnavailable : t.restored); } else notify(t.invalid); });
});
dialog.addEventListener('cancel', () => clearTimeout(timer));
window.addEventListener('pageshow', event => { if (event.persisted) { dialog.close(); clearTimeout(timer); render(); } });
window.addEventListener('storage', () => render());
render();
