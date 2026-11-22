// One camera transforms the whole existing world: art, labels, fog and hit areas.
// No document-wide gesture suppression, reader changes, or progress writes.
const memoryCameras = new Map();
const finite = value => Number.isFinite(value);
const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
const edges = value => Object.fromEntries(['top', 'right', 'bottom', 'left'].map(side =>
  [side, finite(value?.[side]) ? Math.max(0, value[side]) : 0]));
const validView = value => value && finite(value.x) && finite(value.y) &&
  finite(value.scale) && value.scale > 0 && value.scale <= 20;

function layoutFor(viewport, world, settings = {}) {
  const insets = edges(settings.safeInsets);
  // Leave one usable CSS pixel even when an overlay is temporarily larger than
  // a very short viewport. Insets never change the original world coordinates.
  const horizontal = Math.min(1, Math.max(0, viewport.width - 1) / Math.max(1, insets.left + insets.right));
  const vertical = Math.min(1, Math.max(0, viewport.height - 1) / Math.max(1, insets.top + insets.bottom));
  insets.left *= horizontal; insets.right *= horizontal;
  insets.top *= vertical; insets.bottom *= vertical;
  const visible = {left: insets.left, top: insets.top,
    width: Math.max(1, viewport.width - insets.left - insets.right),
    height: Math.max(1, viewport.height - insets.top - insets.bottom)};
  visible.right = visible.left + visible.width; visible.bottom = visible.top + visible.height;
  visible.centerX = visible.left + visible.width / 2; visible.centerY = visible.top + visible.height / 2;
  const bounds = {left: 0, top: 0, right: world.width, bottom: world.height,
    width: world.width, height: world.height};
  return {visible, bounds, insets,
    fitScale: Math.min(visible.width / bounds.width, visible.height / bounds.height),
    coverScale: Math.max(visible.width / bounds.width, visible.height / bounds.height)};
}

export function constrainCamera(state, viewport, world, maxScale = 2.5, settings = {}) {
  const {visible, bounds, fitScale, coverScale} = layoutFor(viewport, world, settings);
  // Only an explicit full-image overview may letterbox. Exploration always
  // covers the usable viewport and stops at the original illustration frame.
  const minimum = settings.overviewExplicit ? fitScale : coverScale;
  const scale = clamp(state.scale, minimum, Math.max(coverScale, maxScale));
  const halfWidth = visible.width / (2 * scale), halfHeight = visible.height / (2 * scale);
  return {
    x: halfWidth >= bounds.width / 2 ? (bounds.left + bounds.right) / 2 :
      clamp(state.x, bounds.left + halfWidth, bounds.right - halfWidth),
    y: halfHeight >= bounds.height / 2 ? (bounds.top + bounds.bottom) / 2 :
      clamp(state.y, bounds.top + halfHeight, bounds.bottom - halfHeight),
    scale,
  };
}

export function createMapCamera(viewport, worldElement, options = {}) {
  const world = {width: options.width || 1600, height: options.height || 900};
  const initial = options.initialCenter || {x: world.width / 2, y: world.height / 2};
  const initialScale = options.initialScale || .95, maxScale = options.maxScale || 2.5;
  const key = options.storageKey || 'sutrazen.play.camera.v1';
  const saved = readSaved();
  let state = saved ? {x: saved.x, y: saved.y, scale: saved.scale} : {x: initial.x, y: initial.y, scale: initialScale};
  let returnView = saved?.returnView || null, overviewExplicit = Boolean(saved?.overviewExplicit);
  let size = {width: 0, height: 0}, destroyed = false, saveTimer = null;
  let layout = layoutFor(size, world);
  let pointers = new Map(), gesture = null, suppressClick = false, suppressUntil = 0;
  const listeners = [];
  const original = {transform: worldElement.style.transform, transformOrigin: worldElement.style.transformOrigin,
    touchAction: viewport.style.touchAction, userSelect: viewport.style.userSelect};
  worldElement.style.transformOrigin = '0 0';
  viewport.style.touchAction = 'none';
  viewport.style.userSelect = 'none';

  function readSaved() {
    let value;
    try { value = globalThis.sessionStorage?.getItem(key); } catch (_) { /* Memory still works. */ }
    if (!value) value = memoryCameras.get(key);
    if (!value) return null;
    try {
      const parsed = typeof value === 'string' ? JSON.parse(value) : value;
      if (parsed.version !== 1 || !validView(parsed)) return null;
      return {x: parsed.x, y: parsed.y, scale: parsed.scale,
        returnView: validView(parsed.returnView) ? {...parsed.returnView} : null,
        overviewExplicit: parsed.overviewExplicit === true};
    } catch (_) { return null; }
  }
  function persist() {
    clearTimeout(saveTimer); saveTimer = null;
    if (destroyed || !size.width || !size.height) return;
    const value = JSON.stringify({version: 1, ...state, overviewExplicit, returnView});
    memoryCameras.set(key, value);
    try { globalThis.sessionStorage?.setItem(key, value); } catch (_) { /* No progress data is touched. */ }
  }
  function schedulePersist() { clearTimeout(saveTimer); saveTimer = setTimeout(persist, 100); }
  function fitScale() { return size.width && size.height ? layout.fitScale : 0; }
  function coverScale() { return size.width && size.height ? layout.coverScale : 0; }
  function focusScale() { return Math.max(coverScale(), Math.min(maxScale, Math.max(initialScale, fitScale() * 1.4))); }
  function fitView() {
    return {x: (layout.bounds.left + layout.bounds.right) / 2,
      y: (layout.bounds.top + layout.bounds.bottom) / 2, scale: fitScale() || initialScale};
  }
  function getState() {
    const fit = fitScale(), overview = overviewExplicit;
    return {...state, fitScale: fit, coverScale: coverScale(), overview, restored: Boolean(saved),
      viewport: {...size}, world: {...world}, defaultFocusScale: focusScale(),
      outerBounds: {...layout.bounds}, safeInsets: {...layout.insets}, visibleViewport: {...layout.visible},
      canReturn: Boolean(returnView), overviewExplicit,
      offsetX: layout.visible.centerX - state.x * state.scale,
      offsetY: layout.visible.centerY - state.y * state.scale};
  }
  function apply(reason = 'change') {
    if (destroyed || !size.width || !size.height) return getState();
    state = constrainCamera(state, size, world, maxScale, {safeInsets: layout.insets, overviewExplicit});
    const snapshot = getState();
    worldElement.style.transform = `translate(${snapshot.offsetX}px, ${snapshot.offsetY}px) scale(${state.scale})`;
    worldElement.style.setProperty('--wm-camera-scale', String(state.scale));
    worldElement.style.setProperty('--wm-marker-scale', String(Math.max(1, 1 / state.scale)));
    worldElement.classList.toggle('wm-is-overview', snapshot.overview);
    viewport.dataset.cameraX = state.x.toFixed(4);
    viewport.dataset.cameraY = state.y.toFixed(4);
    viewport.dataset.cameraScale = state.scale.toFixed(6);
    viewport.dataset.cameraOverview = String(snapshot.overview);
    viewport.dataset.cameraCanReturn = String(snapshot.canReturn);
    viewport.dataset.cameraOverviewExplicit = String(overviewExplicit);
    schedulePersist();
    options.onChange?.(snapshot, reason);
    return snapshot;
  }
  function refresh() {
    const width = viewport.clientWidth, height = viewport.clientHeight;
    if (!width || !height) return getState();
    const firstVisible = !size.width || !size.height;
    size = {width, height};
    let safeInsets = options.safeInsets;
    try { if (typeof options.getInsets === 'function') safeInsets = options.getInsets(); }
    catch (_) { /* A missing overlay measurement must not block the map. */ }
    layout = layoutFor(size, world, {safeInsets});
    if (firstVisible && !saved) state.scale = focusScale();
    if (overviewExplicit) state = fitView();
    return apply('resize');
  }
  function viewportToWorld(point) {
    return {x: state.x + (point.x - layout.visible.centerX) / state.scale,
      y: state.y + (point.y - layout.visible.centerY) / state.scale};
  }
  function worldToViewport(point) {
    return {x: layout.visible.centerX + (point.x - state.x) * state.scale,
      y: layout.visible.centerY + (point.y - state.y) * state.scale};
  }
  function localPoint(event) {
    const rect = viewport.getBoundingClientRect();
    return {x: event.clientX - rect.left, y: event.clientY - rect.top};
  }
  function zoomBy(factor, point = {x: layout.visible.centerX, y: layout.visible.centerY}) {
    if (!finite(factor) || factor <= 0 || !size.width || !size.height) return getState();
    if (overviewExplicit && factor <= 1) return apply('zoom');
    const anchor = viewportToWorld(point);
    const scale = clamp(state.scale * factor, coverScale(), Math.max(coverScale(), maxScale));
    state = {x: anchor.x + (layout.visible.centerX - point.x) / scale,
      y: anchor.y + (layout.visible.centerY - point.y) / scale, scale};
    overviewExplicit = false;
    return apply('zoom');
  }
  function focus(point, scale = focusScale()) {
    if (!point || !finite(point.x) || !finite(point.y)) return getState();
    overviewExplicit = false; returnView = null;
    state = {x: point.x, y: point.y, scale: finite(scale) && scale > 0 ? scale : focusScale()};
    const result = apply('focus'); persist(); return result;
  }
  function fit() {
    if (!returnView) returnView = {...state};
    overviewExplicit = true; state = fitView();
    const result = apply('fit'); persist(); return result;
  }
  function returnFromOverview() {
    if (!returnView) return getState();
    state = {...returnView}; returnView = null; overviewExplicit = false;
    const result = apply('return'); persist(); return result;
  }
  function capture(id) { try { viewport.setPointerCapture(id); } catch (_) { /* Synthetic input has no capture owner. */ } }
  function release(id) { try { if (viewport.hasPointerCapture(id)) viewport.releasePointerCapture(id); } catch (_) {} }
  function blockGestureClick() { suppressClick = true; suppressUntil = performance.now() + 700; }
  function startGesture() {
    const points = [...pointers.values()];
    if (points.length > 1) {
      const [a,b] = points, middle = {x: (a.x + b.x) / 2, y: (a.y + b.y) / 2};
      gesture = {type: 'pinch', scale: state.scale, distance: Math.max(1, Math.hypot(a.x-b.x,a.y-b.y)),
        anchor: viewportToWorld(middle), moved: true};
      for (const id of pointers.keys()) capture(id);
      blockGestureClick();
    } else if (points.length) {
      gesture = {type: 'drag', start: {...points[0]}, camera: {...state}, moved: suppressClick};
    } else gesture = null;
  }
  function pointerDown(event) {
    if (event.pointerType === 'mouse' && event.button !== 0) return;
    if (!pointers.size) { suppressClick = false; suppressUntil = 0; }
    pointers.set(event.pointerId, localPoint(event));
    startGesture();
    viewport.dataset.cameraGesture = gesture.type;
    // A tap remains a native button click. Capture starts only after dragging.
  }
  function pointerMove(event) {
    if (!pointers.has(event.pointerId) || !gesture) return;
    pointers.set(event.pointerId, localPoint(event));
    if (pointers.size > 1) {
      if (gesture.type !== 'pinch') startGesture();
      const [a,b] = [...pointers.values()];
      const middle = {x: (a.x + b.x) / 2, y: (a.y + b.y) / 2};
      const distance = Math.max(1, Math.hypot(a.x-b.x,a.y-b.y));
      const desired = gesture.scale * distance / gesture.distance;
      if (overviewExplicit && desired <= fitScale()) state = fitView();
      else {
        const scale = clamp(desired, coverScale(), Math.max(coverScale(), maxScale));
        state = {x: gesture.anchor.x + (layout.visible.centerX - middle.x) / scale,
          y: gesture.anchor.y + (layout.visible.centerY - middle.y) / scale, scale};
        overviewExplicit = false;
      }
      blockGestureClick(); event.preventDefault(); apply('pinch');
      // Consume clamped movement so reversing at an edge responds immediately.
      gesture.scale = state.scale; gesture.distance = distance; gesture.anchor = viewportToWorld(middle);
    } else {
      const point = pointers.values().next().value;
      const dx = point.x - gesture.start.x, dy = point.y - gesture.start.y;
      if (!gesture.moved && Math.hypot(dx,dy) <= 6) return;
      gesture.moved = true; capture(event.pointerId); blockGestureClick();
      state = {x: gesture.camera.x - dx / gesture.camera.scale,
        y: gesture.camera.y - dy / gesture.camera.scale, scale: gesture.camera.scale};
      event.preventDefault(); apply('drag');
      gesture.start = {...point}; gesture.camera = {...state};
    }
  }
  function pointerEnd(event) {
    if (!pointers.has(event.pointerId)) return;
    if (gesture?.moved || event.type === 'pointercancel') blockGestureClick();
    pointers.delete(event.pointerId); release(event.pointerId);
    startGesture();
    viewport.dataset.cameraGesture = gesture?.type || 'none';
    persist();
  }
  function lostPointerCapture(event) {
    // Touch starts with implicit capture on the tapped label/image. When a drag
    // takes ownership, that child's capture-loss event bubbles through here;
    // it is a hand-off, not cancellation of the viewport's active gesture.
    if (event.target !== viewport || !pointers.has(event.pointerId) ||
        viewport.hasPointerCapture?.(event.pointerId)) return;
    pointerEnd({type: 'pointercancel', pointerId: event.pointerId});
  }
  function cancelAll() {
    if (pointers.size) blockGestureClick();
    for (const id of pointers.keys()) release(id);
    pointers.clear(); gesture = null; viewport.dataset.cameraGesture = 'none'; persist();
  }
  function clickCapture(event) {
    if (event.detail !== 0 && suppressClick && performance.now() < suppressUntil) {
      event.preventDefault(); event.stopImmediatePropagation(); suppressClick = false;
    }
  }
  function wheel(event) {
    if (!event.deltaY || !size.width || !size.height) return;
    event.preventDefault();
    zoomBy(Math.exp(-clamp(event.deltaY, -300, 300) * .002), localPoint(event));
  }
  function keyDown(event) {
    if (event.target.closest('input,textarea,select,[contenteditable="true"]')) return;
    const distance = event.shiftKey ? 100 : 45;
    if (['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(event.key)) {
      event.preventDefault();
      if (event.key==='ArrowLeft') state.x-=distance/state.scale;
      if (event.key==='ArrowRight') state.x+=distance/state.scale;
      if (event.key==='ArrowUp') state.y-=distance/state.scale;
      if (event.key==='ArrowDown') state.y+=distance/state.scale;
      apply('keyboard');
    } else if (['+','=','-','_','0','Home'].includes(event.key)) {
      event.preventDefault();
      if (event.key==='0'||event.key==='Home') fit();
      else zoomBy(event.key==='+'||event.key==='='?1.25:.8);
    }
  }
  function listen(target,type,handler,settings) {
    target.addEventListener(type,handler,settings); listeners.push(()=>target.removeEventListener(type,handler,settings));
  }
  listen(viewport,'pointerdown',pointerDown,{passive:true});
  listen(window,'pointermove',pointerMove,{passive:false});
  listen(window,'pointerup',pointerEnd);
  listen(window,'pointercancel',pointerEnd);
  listen(viewport,'lostpointercapture',lostPointerCapture);
  listen(viewport,'click',clickCapture,true);
  listen(viewport,'wheel',wheel,{passive:false});
  listen(viewport,'keydown',keyDown);
  listen(window,'blur',cancelAll);
  listen(window,'pagehide',persist);
  const resize = typeof ResizeObserver === 'function' ? new ResizeObserver(refresh) : null;
  resize?.observe(viewport); if (!resize) listen(window,'resize',refresh);
  refresh();
  return {focus,fit,returnFromOverview,zoomBy,getState,refresh,viewportToWorld,worldToViewport,
    wasGesture:()=>suppressClick && performance.now()<suppressUntil,
    destroy(){persist();destroyed=true;clearTimeout(saveTimer);resize?.disconnect();cancelAll();listeners.forEach(remove=>remove());
      worldElement.style.transform=original.transform;worldElement.style.transformOrigin=original.transformOrigin;
      viewport.style.touchAction=original.touchAction;viewport.style.userSelect=original.userSelect;}};
}
