/* Keep panel masks on actual object-fit:contain image pixels, including when
 * the reader's image element has letterboxing. No image pixels are modified. */
(() => {
  const states = new WeakMap();
  function update(frame, art, definition, localPage) {
    let state = states.get(frame);
    if (!state) {
      const mask = document.createElement('div');
      mask.className = 'picture-panel-focus';
      mask.setAttribute('aria-hidden', 'true');
      frame.append(mask);
      state = { mask };
      states.set(frame, state);
      state.layout = () => {
        if (state.mask.hidden || !art.naturalWidth || !art.naturalHeight) return;
        const image = art.getBoundingClientRect(), parent = frame.getBoundingClientRect();
        const scale = Math.min(image.width / art.naturalWidth, image.height / art.naturalHeight);
        const width = art.naturalWidth * scale, height = art.naturalHeight * scale;
        Object.assign(mask.style, {
          left: image.left - parent.left + (image.width - width) / 2 + 'px',
          top: image.top - parent.top + (image.height - height) / 2 + 'px',
          width: width + 'px', height: height + 'px'
        });
      };
      const observer = new ResizeObserver(state.layout);
      observer.observe(frame); observer.observe(art);
      art.addEventListener('load', state.layout);
      window.addEventListener('resize', state.layout);
    }
    const active = definition?.pages[localPage - 1];
    state.mask.hidden = !active;
    if (!active) { state.mask.replaceChildren(); return; }
    state.mask.dataset.activePanel = active;
    state.mask.replaceChildren(...definition.panels.map(panel => {
      const cell = document.createElement('span');
      cell.dataset.panel = panel.id;
      cell.classList.toggle('active', panel.id === active);
      Object.assign(cell.style, {
        left: panel.x + '%', top: panel.y + '%',
        width: panel.width + '%', height: panel.height + '%'
      });
      return cell;
    }));
    state.layout();
  }
  window.SutraZenPanelFocus = { update };
})();
