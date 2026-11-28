// The module is inert unless this reader was explicitly opened from collection.
// It never reads, writes or completes the three-book v1 journey.
const collectionParams = new URLSearchParams(location.search);
if (collectionParams.get('collection') === '1' && collectionParams.has('journey')) {
  // A mixed old-mode URL must not bypass collection policy or run two bridges.
  const clean = new URL(location.href); clean.searchParams.delete('journey');
  location.replace(clean.href);
} else if (collectionParams.get('collection') === '1') {
  initializeCollection().catch(async () => {
    const { COLLECTION_TEXT: text } = await import('./catalog.js?v=summary-merge-1');
    const notice = document.createElement('p');
    notice.textContent = text.integrationUnavailable;
    notice.setAttribute('role', 'status');
    document.querySelector('.reader')?.prepend(notice);
  });
}

async function initializeCollection() {
  const [{ store }, { CATALOG, COLLECTION_TEXT: text }, policy, {issueFirstCompletionReceipt}, pagination] = await Promise.all([
    import('./store.js?v=summary-merge-1'), import('./catalog.js?v=summary-merge-1'), import('../route/eligibility.js?v=summary-merge-1'), import('../story/completion-receipt.js?v=summary-merge-1').catch(() => ({issueFirstCompletionReceipt: () => false})), import('./migrations.js?v=summary-merge-1'),
  ]);
  const parts = location.pathname.split('/').filter(Boolean);
  const bookId = parts[parts.indexOf('book') - 1];
  const book = CATALOG.find(book => book.id === bookId);
  if (!book || typeof window.showPage !== 'function') return;
  let redirecting = false;
  const gameURL = new URL('../../game/?v=summary-merge-1', import.meta.url);
  const denyEntry = () => {
    if (redirecting) return;
    redirecting = true;
    const destination = new URL(gameURL);
    destination.searchParams.set('notice', 'locked'); destination.hash = 'map';
    location.replace(destination.href);
  };
  const eligible = () => policy.canReadGameBook(bookId, store.get().completed);
  if (!eligible()) { denyEntry(); return; }
  const reviewing = policy.canReviewGameBook(bookId, store.get().completed);
  const next = document.getElementById('next');
  const position = document.getElementById('position-text');
  if (!next || !position) return;
  const readPosition = () => {
    // Seven Factors counts every cue, not merely its illustration scenes.
    const match = position.textContent.match(/(\d+)\s*\/\s*(\d+)/);
    return match ? { index: Number(match[1]) - 1, total: Number(match[2]) } : null;
  };
  let paginationBlocked = false;
  const verifyPagination = at => {
    if (bookId !== pagination.EIGHTFOLD_BOOK_ID || at?.total === pagination.EIGHTFOLD_CURRENT_STEPS) return true;
    if (paginationBlocked) return false;
    paginationBlocked = true;
    // Never write new-coordinate bookmarks from an old cached 111-page reader.
    // Keep the incoming page/version together through one bounded HTML refresh.
    if (collectionParams.get('readerRefresh') !== 'summary-merge-1') {
      const updated = new URL(location.href); updated.searchParams.set('readerRefresh', 'summary-merge-1');
      location.replace(updated.href); return false;
    }
    document.body.dataset.collectionReaderState = 'version-mismatch';
    const notice = document.createElement('div'); notice.className = 'collection-reader-pagination-error'; notice.setAttribute('role', 'alert');
    const copy = document.createElement('p'); copy.textContent = text.paginationUnavailable;
    const retry = document.createElement('button'); retry.type = 'button'; retry.textContent = text.reloadReader; retry.style.minHeight = '44px';
    retry.addEventListener('click', () => location.reload());
    const back = document.createElement('a'); const destination = new URL(gameURL); destination.hash = 'map';
    back.href = destination.href; back.textContent = text.returnJourney;
    notice.append(copy, retry, document.createTextNode(' '), back);
    document.querySelector('.reader')?.prepend(notice);
    return false;
  };
  if (!verifyPagination(readPosition())) return;
  const stylesheet = document.createElement('link');
  stylesheet.rel = 'stylesheet'; stylesheet.href = new URL('./reader.css?v=stable-art-1', import.meta.url).href;
  document.head.append(stylesheet);
  document.body.classList.add('collection-reading');
  document.body.dataset.collectionBook = bookId;
  document.body.dataset.collectionMode = reviewing ? 'review' : 'mainline';
  // Return hints never grant access. All game readers now share the same shell.
  const returnURL = new URL(gameURL); returnURL.hash = reviewing ? 'shelf' : 'map';
  const returnLabel = reviewing ? text.returnShelf : (await import('../worldmap-v4/text.js?v=summary-merge-1')).T.returnJourney;
  // Reuse the top-left slot; another landscape toolbar would cover narration.
  const returnLink = document.querySelector('.top > a') || document.createElement('a');
  returnLink.classList.add('collection-reader-return');
  returnLink.href = returnURL.href; returnLink.textContent = returnLabel;
  returnLink.setAttribute('aria-label', returnLabel);
  if (!returnLink.isConnected) document.querySelector('.top')?.prepend(returnLink);
  let lastSaved = -1;
  let finishing = false;
  const update = () => {
    if (!eligible()) { denyEntry(); return; }
    const at = readPosition(); if (!at || !verifyPagination(at)) return;
    document.body.dataset.collectionIndex = String(at.index);
    document.body.dataset.collectionTotal = String(at.total);
    if (at.index !== lastSaved && !finishing) {
      if (!store.savePosition(bookId, at.index)) { denyEntry(); return; }
      lastSaved = at.index;
    }
    const last = at.index === at.total - 1;
    next.classList.toggle('collection-reader-finish', last);
    if (last) {
      next.disabled = false; next.textContent = text.completeBook;
      next.setAttribute('aria-label', text.completeBook);
    }
  };
  const originalShow = window.showPage;
  window.showPage = function (...args) { if (!eligible()) { denyEntry(); return; } originalShow(...args); update(); };
  // Capture at document level before original reader/restart button listeners.
  document.addEventListener('click', event => {
    if (!event.target.closest?.('#next')) return;
    const at = readPosition();
    if (!verifyPagination(at)) { event.preventDefault(); event.stopImmediatePropagation(); return; }
    if (!at || at.index !== at.total - 1) return;
    event.preventDefault(); event.stopImmediatePropagation();
    if (finishing) return;
    if (!eligible()) { denyEntry(); return; }
    finishing = true;
    if (!store.savePosition(bookId, at.index)) { finishing = false; denyEntry(); return; }
    if (reviewing || policy.canReviewGameBook(bookId, store.get().completed)) {
      const shelf = new URL(gameURL); shelf.hash = 'shelf';
      location.assign(shelf.href); // No completion marker, write or reward replay.
    } else if (policy.canCompleteGameBook(bookId, store.get().completed) && store.complete(bookId)) {
      if (bookId === 'four-truths') issueFirstCompletionReceipt();
      const next = new URL(gameURL); next.searchParams.set('completed', bookId); next.hash = 'map';
      location.assign(next.href);
    } else { finishing = false; denyEntry(); }
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
  window.addEventListener('sutrazen:collection-progress', () => { warn(); if (!eligible()) denyEntry(); }); warn();
  const query = new URLSearchParams(location.search);
  const savedPosition = store.get().positions[bookId];
  let requested;
  if (query.has('collectionPage')) {
    requested = Number(query.get('collectionPage'));
    if (bookId === pagination.EIGHTFOLD_BOOK_ID) {
      if (!query.has('collectionPageVersion')) requested = pagination.migrateEightfoldIndex(requested);
      else if (query.get('collectionPageVersion') !== String(pagination.CURRENT_POSITIONS_REVISION)) requested = NaN;
    }
  } else requested = reviewing && savedPosition === readPosition().total - 1 ? 0 : savedPosition;
  const at = readPosition();
  const target = Number.isInteger(requested) && requested >= 0 && requested < at.total ? requested : 0;
  if (query.has('collectionPage')) {
    query.delete('collectionPage');
    if (bookId === pagination.EIGHTFOLD_BOOK_ID) query.set('collectionPageVersion', String(pagination.CURRENT_POSITIONS_REVISION));
    const url = new URL(location.href); url.search = query.toString();
    history.replaceState(history.state, '', url);
  }
  if (bookId === 'seven-factors' && typeof readingSteps !== 'undefined') {
    const step = readingSteps[target]; window.showPage(step.page, step.cue);
  } else window.showPage(target);
  Object.defineProperty(window, 'SutraZenCollectionBridge', {
    configurable: true, get: () => ({ bookId, ...readPosition(), mode: reviewing ? 'review' : 'mainline' }),
  });
  window.addEventListener('pagehide', () => {
    if (finishing) return;
    const at = readPosition(); if (at && verifyPagination(at)) store.savePosition(bookId, at.index);
  });
}
