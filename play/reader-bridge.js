// Opt-in adapter only. Existing books, scripture and independent reading stay intact.
const query = new URLSearchParams(location.search);
const journeyMode = query.get('journey');
if (journeyMode === 'ordered' || journeyMode === 'free') {
  initializeJourney().catch(async () => {
    const { readerLabels } = await import('./reader-labels.js');
    const warning = document.createElement('p');
    warning.className = 'play-reader-warning';
    warning.setAttribute('role', 'status');
    warning.textContent = readerLabels['zh-Hant'].integrationUnavailable;
    document.querySelector('.top')?.append(warning);
  });
}

async function initializeJourney() {
  const [{ store }, { readerLabels }] = await Promise.all([
    import('./progress.js'), import('./reader-labels.js'),
  ]);
  const labels = readerLabels['zh-Hant'];
  const pathParts = location.pathname.split('/').filter(Boolean);
  const bookId = pathParts[pathParts.indexOf('book') - 1];
  if (!['four-truths', 'five-aggregates', 'six-senses'].includes(bookId)) return;
  if (typeof window.showPage !== 'function') return;
  if (journeyMode === 'ordered' && !store.canRead(bookId)) {
    location.replace(new URL('./?notice=locked', import.meta.url));
    return;
  }
  const next = document.getElementById('next');
  const position = document.getElementById('position-text');
  if (!next || !position) return;
  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = new URL('./reader-bridge.css', import.meta.url).href;
  document.head.append(css);
  document.body.classList.add('play-reading');
  document.body.dataset.playBook = bookId;
  document.body.dataset.playMode = journeyMode;
  const journeyURL = new URL('./', import.meta.url);
  // Reuse the existing top-left slot: adding a second landscape button would
  // overlap the caption. Original guide access remains in 閱讀原經 below.
  const returnLink = document.querySelector('.top > a') || document.createElement('a');
  returnLink.classList.add('play-reader-return', 'sz-journey-return');
  returnLink.href = journeyURL.href;
  returnLink.textContent = labels.returnJourney;
  returnLink.setAttribute('aria-label', labels.returnJourney);
  if (!returnLink.isConnected) document.querySelector('.top')?.prepend(returnLink);

  let warnedIssue = null;
  const announceStorageIssue = () => {
    if (!store.issue || warnedIssue === store.issue) return;
    warnedIssue = store.issue;
    const dialog = document.createElement('dialog');
    dialog.className = 'play-reader-storage';
    const heading = document.createElement('h2');
    heading.textContent = labels.storageTitle;
    const copy = document.createElement('p');
    copy.textContent = store.issue === 'corrupt' ? labels.storageCorrupt : labels.storageUnavailable;
    const close = document.createElement('button');
    close.type = 'button'; close.textContent = labels.keepReading;
    close.addEventListener('click', () => { dialog.close(); dialog.remove(); });
    dialog.append(heading, copy, close); document.body.append(dialog);
    dialog.showModal();
  };
  window.addEventListener('sutrazen:play-progress', announceStorageIssue);
  announceStorageIssue();

  const readPosition = () => {
    const match = position.textContent.match(/(\d+)\s*\/\s*(\d+)/);
    return match ? { index: Number(match[1]) - 1, total: Number(match[2]) } : null;
  };
  let lastSaved = -1;
  const update = () => {
    const at = readPosition();
    if (!at) return;
    document.body.dataset.playIndex = String(at.index);
    document.body.dataset.playTotal = String(at.total);
    if (at.index !== lastSaved) {
      store.savePosition(bookId, at.index, journeyMode);
      lastSaved = at.index;
    }
    const last = at.index === at.total - 1;
    next.classList.toggle('play-reader-finish', last);
    if (last) {
      next.disabled = false;
      next.textContent = labels.completeBook;
      next.setAttribute('aria-label', next.textContent);
    }
  };
  const originalShow = window.showPage;
  window.showPage = function (index) {
    originalShow(index);
    update();
  };
  // Document capture runs before the shared button's restart listener.
  // Merely reaching this page never records completion.
  let finishing = false;
  document.addEventListener('click', event => {
    if (!event.target.closest?.('#next')) return;
    const at = readPosition();
    if (!at || at.index !== at.total - 1) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    if (finishing) return;
    finishing = true;
    store.savePosition(bookId, at.index, journeyMode);
    if (journeyMode === 'free') {
      journeyURL.searchParams.set('freeRead', bookId);
      location.assign(journeyURL.href);
    } else {
      const finished = store.finish(bookId, journeyMode);
      if (finished) {
        journeyURL.searchParams.set('completed', bookId);
        location.assign(journeyURL.href);
      } else {
        finishing = false;
        next.textContent = labels.cannotFinish;
      }
    }
  }, true);
  new MutationObserver(update).observe(position, {
    childList: true, subtree: true, characterData: true,
  });
  store.setActive(bookId, journeyMode);
  const saved = (journeyMode === 'free' ? store.get().freePositions : store.get().positions)?.[bookId];
  const requested = query.has('playPage') ? Number(query.get('playPage')) : saved;
  const at = readPosition();
  const target = Number.isInteger(requested) && requested >= 0 && requested < at.total ? requested : 0;
  // The URL is an initial destination only; subsequent reloads use the saved position.
  if (query.has('playPage')) {
    query.delete('playPage');
    const url = new URL(location.href);
    url.search = query.toString();
    history.replaceState(history.state, '', url);
  }
  window.showPage(target);
  Object.defineProperty(window, 'SutraZenJourneyBridge', {
    configurable: true,
    get: () => ({ bookId, ...readPosition(), mode: journeyMode }),
  });
  window.addEventListener('pagehide', () => {
    if (finishing) return; // finish() has already selected the next ordered book.
    const at = readPosition();
    if (at) store.savePosition(bookId, at.index, journeyMode);
  });
}
