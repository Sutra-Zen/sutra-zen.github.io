// The module is inert unless this reader was explicitly opened from collection.
// It never reads, writes or completes the three-book v1 journey.
if (new URLSearchParams(location.search).get('collection') === '1') {
  initializeCollection().catch(async () => {
    const { COLLECTION_TEXT: text } = await import('./catalog.js');
    const notice = document.createElement('p');
    notice.textContent = text.integrationUnavailable;
    notice.setAttribute('role', 'status');
    document.querySelector('.reader')?.prepend(notice);
  });
}

async function initializeCollection() {
  const [{ store }, { CATALOG, COLLECTION_TEXT: text }] = await Promise.all([
    import('./store.js'), import('./catalog.js'),
  ]);
  const parts = location.pathname.split('/').filter(Boolean);
  const bookId = parts[parts.indexOf('book') - 1];
  if (!CATALOG.some(book => book.id === bookId) || typeof window.showPage !== 'function') return;
  // Avoid running two optional integrations if an edited URL contains both modes.
  // Normal collection links contain only collection=1.
  if (new URLSearchParams(location.search).has('journey')) return;
  const next = document.getElementById('next');
  const position = document.getElementById('position-text');
  if (!next || !position) return;
  const stylesheet = document.createElement('link');
  stylesheet.rel = 'stylesheet'; stylesheet.href = new URL('./reader.css', import.meta.url).href;
  document.head.append(stylesheet);
  document.body.classList.add('collection-reading');
  document.body.dataset.collectionBook = bookId;
  const requestedReturn = new URLSearchParams(location.search).get('collectionReturn');
  const worldmapReturn = requestedReturn === 'worldmap-v4';
  const gameReturn = requestedReturn === 'game';
  const shelfURL = new URL(gameReturn ? '../../game/' : worldmapReturn ? '../worldmap-v4/' : '../visual-v2/shelf.html', import.meta.url);
  const returnLabel = worldmapReturn || gameReturn ? (await import('../worldmap-v4/text.js')).T.returnJourney : text.returnShelf;
  // Reuse the top-left slot; another landscape toolbar would cover narration.
  const returnLink = document.querySelector('.top > a') || document.createElement('a');
  returnLink.classList.add('collection-reader-return');
  returnLink.href = shelfURL.href; returnLink.textContent = returnLabel;
  returnLink.setAttribute('aria-label', returnLabel);
  if (!returnLink.isConnected) document.querySelector('.top')?.prepend(returnLink);
  const readPosition = () => {
    // The first fraction is the real reading-step count, including all cues in
    // Seven Factors (not merely its 12 illustration scenes).
    const match = position.textContent.match(/(\d+)\s*\/\s*(\d+)/);
    return match ? { index: Number(match[1]) - 1, total: Number(match[2]) } : null;
  };
  let lastSaved = -1;
  let finishing = false;
  const update = () => {
    const at = readPosition(); if (!at) return;
    document.body.dataset.collectionIndex = String(at.index);
    document.body.dataset.collectionTotal = String(at.total);
    if (at.index !== lastSaved && !finishing) {
      store.savePosition(bookId, at.index); lastSaved = at.index;
    }
    const last = at.index === at.total - 1;
    next.classList.toggle('collection-reader-finish', last);
    if (last) {
      next.disabled = false; next.textContent = text.completeBook;
      next.setAttribute('aria-label', text.completeBook);
    }
  };
  const originalShow = window.showPage;
  window.showPage = function (...args) { originalShow(...args); update(); };
  // Capture at document level before original reader/restart button listeners.
  document.addEventListener('click', event => {
    if (!event.target.closest?.('#next')) return;
    const at = readPosition(); if (!at || at.index !== at.total - 1) return;
    event.preventDefault(); event.stopImmediatePropagation();
    if (finishing) return;
    finishing = true;
    store.savePosition(bookId, at.index);
    if (store.complete(bookId)) {
      shelfURL.searchParams.set('completed', bookId); location.assign(shelfURL.href);
    } else finishing = false;
  }, true);
  new MutationObserver(update).observe(position, { childList: true, subtree: true, characterData: true });
  let warned = null;
  const warn = () => {
    if (!store.issue || warned === store.issue) return;
    warned = store.issue;
    const dialog = document.createElement('dialog'); dialog.className = 'collection-reader-storage';
    const heading = document.createElement('h2'); heading.textContent = text.storageTitle;
    const copy = document.createElement('p'); copy.textContent = store.issue === 'corrupt' ? text.storageCorrupt : text.storageUnavailable;
    const close = document.createElement('button'); close.type = 'button'; close.textContent = text.keepReading;
    close.addEventListener('click', () => { dialog.close(); dialog.remove(); });
    dialog.append(heading, copy, close); document.body.append(dialog); dialog.showModal();
  };
  window.addEventListener('sutrazen:collection-progress', warn); warn();
  const query = new URLSearchParams(location.search);
  const requested = query.has('collectionPage') ? Number(query.get('collectionPage')) : store.get().positions[bookId];
  const at = readPosition();
  const target = Number.isInteger(requested) && requested >= 0 && requested < at.total ? requested : 0;
  if (query.has('collectionPage')) {
    query.delete('collectionPage'); const url = new URL(location.href); url.search = query.toString();
    history.replaceState(history.state, '', url);
  }
  if (bookId === 'seven-factors' && typeof readingSteps !== 'undefined') {
    const step = readingSteps[target]; window.showPage(step.page, step.cue);
  } else window.showPage(target);
  Object.defineProperty(window, 'SutraZenCollectionBridge', {
    configurable: true, get: () => ({ bookId, ...readPosition() }),
  });
  window.addEventListener('pagehide', () => {
    if (finishing) return;
    const at = readPosition(); if (at) store.savePosition(bookId, at.index);
  });
}
