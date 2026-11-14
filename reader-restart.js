// Shared last-page action; keep each reader's original navigation elsewhere.
(() => {
  const next = document.querySelector('#next');
  const position = document.querySelector('#position-text');
  if (!next || !position || typeof window.showPage !== 'function') return;
  const original = next.innerHTML;
  const isLast = () => {
    const match = position.textContent.match(/(\d+)\s*\/\s*(\d+)/);
    return Boolean(match && Number(match[1]) === Number(match[2]));
  };
  function update() {
    const last = isLast();
    document.body.classList.toggle('reader-at-end', last);
    next.classList.toggle('reader-restart', last);
    next.setAttribute('aria-label', last ? '回到第一頁' : '下一頁');
    next.innerHTML = last ? '<span class="portrait-label">回到第一頁 </span><span aria-hidden="true">↺</span>' : original;
    if (last) next.disabled = false;
  }
  next.addEventListener('click', event => {
    if (!isLast()) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    window.showPage(0);
    update();
  }, true);
  new MutationObserver(update).observe(position, { childList: true, subtree: true, characterData: true });
  update();
})();
