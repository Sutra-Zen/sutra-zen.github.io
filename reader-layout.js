// Older readers retain their content/renderers; reserve the same image-free bands.
(() => {
  const page = document.querySelector('.page');
  const scene = page?.querySelector('.scene');
  const caption = document.querySelector('#caption');
  const scripture = page?.querySelector('.scripture');
  const frame = document.querySelector('#art-frame');
  const art = document.querySelector('#art');
  if (!page || !scene || !caption || !scripture || !frame || !art) return;
  const plainScenesOnly = document.currentScript?.dataset.mode === 'plain-scenes';
  let pending = false;
  function layout() {
    pending = false;
    const enabled = !plainScenesOnly || !page.classList.contains('overlay-scene');
    page.classList.toggle('reader-standard-layout', enabled);
    const bands = enabled && matchMedia('(orientation:landscape)').matches && !frame.hidden &&
      !page.classList.contains('text-scene') && !page.classList.contains('afterword-scene') &&
      art.naturalWidth > 0 && art.naturalHeight > 0;
    page.classList.toggle('reader-bands', bands);
    if (art.naturalWidth && art.naturalHeight)
      scene.style.setProperty('--reader-art-ratio', String(art.naturalWidth / art.naturalHeight));
    if (!bands) return;
    const top = caption.hidden ? 0 : caption.getBoundingClientRect().height;
    const bottom = scripture.hidden ? 0 : scripture.getBoundingClientRect().height;
    scene.style.setProperty('--reader-caption-space', top + 'px');
    scene.style.setProperty('--reader-image-space', Math.max(1, scene.clientHeight - top - bottom) + 'px');
  }
  function schedule() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(layout);
  }
  const resize = new ResizeObserver(schedule);
  for (const element of [scene, caption, scripture]) resize.observe(element);
  new MutationObserver(schedule).observe(page, {childList:true, subtree:true, attributes:true,
    attributeFilter:['class','hidden','src']});
  art.addEventListener('load', schedule);
  window.addEventListener('resize', schedule);
  document.fonts.ready.then(schedule);
  schedule();
})();
