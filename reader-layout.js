// Shared framing only: book renderers retain every cue, quote and image overlay.
(() => {
  const page = document.querySelector('.page');
  const scene = page?.querySelector('.scene');
  const caption = document.querySelector('#caption');
  const scripture = page?.querySelector('.scripture');
  const frame = document.querySelector('#art-frame');
  const art = document.querySelector('#art');
  if (!page || !scene || !caption || !scripture || !frame || !art) return;
  const legacyPlain = document.currentScript?.dataset.mode === 'plain-scenes';
  const landscape = matchMedia('(orientation:landscape)');
  // All normal source illustrations fit this ratio (maximum is1681/935).
  // The unusually wide related-video document still fits its complete width.
  const referenceRatio = 1.8;
  const defaultRatio = Number(document.currentScript?.dataset.artRatio) || referenceRatio;
  const verseBody = scripture.querySelector('.verse-body');
  const top = document.querySelector('.top');
  const position = document.querySelector('.position');
  const links = document.querySelector('.reading-links');
  const openVerse = document.querySelector('#open-verse');
  const previous = document.querySelector('#previous'), next = document.querySelector('#next');
  const outside = document.querySelector('#outside-labels');
  const summary = document.querySelector('#summary-text');
  const summaryParent = summary?.parentElement;
  const summaryNext = summary?.nextSibling;
  const summaryBand = summary ? document.createElement('div') : null;
  if (summaryBand) {
    summaryBand.id = 'reader-summary-caption';summaryBand.className = 'story band';
    summaryBand.hidden = true;summaryBand.tabIndex = 0;
    summaryBand.setAttribute('role', 'region');
    summaryBand.setAttribute('aria-label', '本頁總結，可捲動閱讀');
    scene.prepend(summaryBand);
  }
  const artSummary = document.querySelector('#art-summary');
  const artSummaryParent = artSummary?.parentElement, artSummaryNext = artSummary?.nextSibling;
  const focusAttrs = ['tabindex', 'role', 'aria-label'];
  const originalFocus = element => Object.fromEntries(focusAttrs.map(name => [name, element.getAttribute(name)]));
  const captionFocus = originalFocus(caption), sceneFocus = originalFocus(scene);
  const restoreFocus = (element, attributes) => {
    for (const [name, value] of Object.entries(attributes))
      if (value === null) element.removeAttribute(name); else element.setAttribute(name, value);
  };
  if (outside && caption.querySelector('#narration')) caption.append(outside);
  document.body.classList.add('reader-unified-controls');
  let pending = false, lastText = '', lastPictureRatio = null;
  const toggle = (name, enabled) => {
    if (page.classList.contains(name) !== enabled) page.classList.toggle(name, enabled);
  };
  const set = (name, value) => {
    if (scene.style.getPropertyValue(name) !== value) scene.style.setProperty(name, value);
  };
  const shown = element => element && !element.hidden && element.getClientRects().length &&
    getComputedStyle(element).visibility !== 'hidden';
  function inset(element, side, rect) {
    if (!shown(element)) return 12;
    const box = element.getBoundingClientRect();
    if (box.bottom < rect.top || box.top > rect.bottom) return 12;
    return Math.max(12, side === 'left' ? box.right - rect.left + 10 : rect.right - box.left + 10);
  }
  function verticalSpace(elements, side, rect) {
    return Math.max(0, ...elements.filter(shown).map(element => {
      const box = element.getBoundingClientRect();
      return (side === 'top' ? box.bottom - rect.top : rect.bottom - box.top) + 8;
    }));
  }
  function ratio() {
    if (art.complete && art.naturalWidth && art.naturalHeight) return art.naturalWidth / art.naturalHeight;
    const known = Number(frame.style.getPropertyValue('--art-ratio-number'));
    if (known > 0) return known;
    const native = getComputedStyle(frame).getPropertyValue('--art-ratio').trim().split('/').map(Number);
    return native[0] > 0 ? native[0] / (native[1] || 1) : defaultRatio;
  }
  function layout() {
    pending = false;
    const legacy = !legacyPlain || !page.classList.contains('overlay-scene');
    const illustrated = !frame.hidden && Boolean(art.getAttribute('src')) &&
      !page.matches('.text-scene,.afterword-scene,.heart-scene,.text-summary-scene');
    const heart = page.classList.contains('heart-scene');
    const ending = !heart && !illustrated &&
      page.matches('.text-scene,.afterword-scene,.text-summary-scene');
    toggle('reader-standard-layout', legacy);
    toggle('reader-bands', legacy && landscape.matches && illustrated);
    toggle('reader-stable-artwork', illustrated);
    toggle('reader-framed-heart', heart);
    toggle('reader-framed-ending', ending);
    if (artSummary) {
      const belowImage = illustrated && page.classList.contains('summary-scene') &&
        !landscape.matches && innerWidth < 680;
      if (belowImage && artSummary.parentElement === frame) frame.after(artSummary);
      else if (!belowImage && artSummary.parentElement !== artSummaryParent)
        artSummaryParent.insertBefore(artSummary,
          artSummaryNext?.parentElement === artSummaryParent ? artSummaryNext : null);
    }
    if (ending) {
      scene.tabIndex = 0;scene.setAttribute('role', 'region');
      scene.setAttribute('aria-label', '本頁文字，可捲動閱讀');
    } else restoreFocus(scene, sceneFocus);
    const naturalRatio = ratio();
    // An ultra-wide document uses the common canvas with contained letterboxing;
    // the following text page can therefore retain that same picture frame.
    const frameRatio = heart ? (lastPictureRatio || defaultRatio) :
      naturalRatio > referenceRatio + .01 ? referenceRatio : naturalRatio;
    if (illustrated) lastPictureRatio = frameRatio;
    set('--reader-art-ratio', String(frameRatio));
    if (!illustrated && !heart && !ending) return;
    // Narrow illustrated summaries keep their extra copy in the scrollable
    // narration band. Text-only closings retain the original full content host.
    if (summary && caption.querySelector('#narration')) {
      const inCaption = illustrated && landscape.matches && !summary.hidden;
      if (inCaption && summary.parentElement !== summaryBand) summaryBand.append(summary);
      else if (!inCaption && summary.parentElement === summaryBand)
        summaryParent.insertBefore(summary, summaryNext?.parentElement === summaryParent ? summaryNext : null);
      summaryBand.hidden = !inCaption;
    }
    const rect = scene.getBoundingClientRect();
    let target;
    if (landscape.matches) {
      // These bands depend on the viewport/font, never this page's line count.
      const base = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
      const capLine = Math.min(base * 1.25, Math.max(base, innerHeight * .035)) * 1.4;
      const verseLine = Math.min(base * 1.125, Math.max(base * .94, innerHeight * .033)) * 1.4;
      const capSpace = Math.max(64, capLine * 2 + 16, verticalSpace([top, position], 'top', rect));
      const verseSpace = Math.max(60, verseLine * 2 + 10, verticalSpace([links, openVerse], 'bottom', rect));
      const area = Math.max(1, scene.clientHeight - capSpace - verseSpace);
      set('--reader-caption-space', capSpace + 'px');
      set('--reader-scripture-space', verseSpace + 'px');
      set('--reader-image-space', area + 'px');
      set('--reader-caption-left', inset(top, 'left', rect) + 'px');
      set('--reader-caption-right', inset(position, 'right', rect) + 'px');
      set('--reader-verse-left', inset(links, 'left', rect) + 'px');
      set('--reader-verse-right', inset(openVerse, 'right', rect) + 'px');
      set('--reader-ending-left', Math.max(inset(top, 'left', rect), inset(previous, 'left', rect)) + 'px');
      set('--reader-ending-right', Math.max(inset(position, 'right', rect), inset(next, 'right', rect)) + 'px');
      target = Math.min(area, Math.max(1, scene.clientWidth - 112) / referenceRatio);
    } else {
      // Portrait remains a scrolling document; long captions never lose text.
      target = scene.clientWidth / referenceRatio;
    }
    const widthAvailable = Math.max(1, scene.clientWidth - (landscape.matches ? 112 : 0));
    const height = Math.min(target, widthAvailable / frameRatio);
    set('--reader-target-art-height', target + 'px');
    set('--reader-art-height', height + 'px');
    page.dataset.readerArtKind = naturalRatio > referenceRatio + .01 ? 'wide-document' : 'illustration';
    const text = caption.textContent + '\n' + (summaryBand?.textContent || '') + '\n' + scripture.textContent;
    if (text !== lastText) {
      caption.scrollTop = 0;
      if (summaryBand) summaryBand.scrollTop = 0;
      if (verseBody) verseBody.scrollTop = 0;
      lastText = text;
    }
    const scrollable = landscape.matches && !ending && !page.classList.contains('baked-scene');
    if (scrollable) {
      caption.tabIndex = 0;
      caption.setAttribute('role', 'region');
      caption.setAttribute('aria-label', '本頁口白，可捲動閱讀');
      if (verseBody && !heart) {
        verseBody.tabIndex = 0;
        verseBody.setAttribute('role', 'region');
        verseBody.setAttribute('aria-label', '本頁經文，可捲動閱讀');
      }
    } else restoreFocus(caption, captionFocus);
  }
  function schedule() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(layout);
  }
  const resize = new ResizeObserver(schedule);
  for (const element of [scene, caption, scripture, summaryBand, top, position, links, openVerse, previous, next])
    if (element) resize.observe(element);
  new MutationObserver(schedule).observe(page, {childList:true, subtree:true, characterData:true,
    attributes:true, attributeFilter:['class','hidden','src']});
  if (top) new MutationObserver(schedule).observe(top, {childList:true, subtree:true, characterData:true});
  art.addEventListener('load', schedule);
  window.addEventListener('resize', schedule);
  window.addEventListener('pageshow', schedule);
  document.fonts.ready.then(schedule);
  schedule();
})();
