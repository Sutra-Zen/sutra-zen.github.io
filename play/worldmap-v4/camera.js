// One camera transforms the whole existing world: art, labels, fog and hit areas.
// No document-wide gesture suppression, reader changes, or progress writes.
const memoryCameras = new Map();
const finite = value => Number.isFinite(value);
const clamp = (value, low, high) => Math.max(low, Math.min(high, value));

export function constrainCamera(state, viewport, world, maxScale = 2.5) {
  const fitScale = Math.min(viewport.width / world.width, viewport.height / world.height);
  const scale = clamp(state.scale, fitScale, Math.max(fitScale, maxScale));
  const halfWidth = viewport.width / (2 * scale), halfHeight = viewport.height / (2 * scale);
  return {
    x: halfWidth >= world.width / 2 ? world.width / 2 : clamp(state.x, halfWidth, world.width - halfWidth),
    y: halfHeight >= world.height / 2 ? world.height / 2 : clamp(state.y, halfHeight, world.height - halfHeight),
    scale,
  };
}

export function createMapCamera(viewport, worldElement, options = {}) {
  const world = {width: options.width || 1600, height: options.height || 900};
  const initial = options.initialCenter || {x: world.width / 2, y: world.height / 2};
  const initialScale = options.initialScale || .95, maxScale = options.maxScale || 2.5;
  const key = options.storageKey || 'sutrazen.play.camera.v1';
  const saved = readSaved();
  let state = saved || {x: initial.x, y: initial.y, scale: initialScale};
  let size = {width: 0, height: 0}, destroyed = false, saveTimer = null;
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
      return parsed.version === 1 && finite(parsed.x) && finite(parsed.y) &&
        finite(parsed.scale) && parsed.scale > 0 && parsed.scale <= 20 ?
        {x: parsed.x, y: parsed.y, scale: parsed.scale} : null;
    } catch (_) { return null; }
  }
  function persist() {
    clearTimeout(saveTimer); saveTimer = null;
    if (destroyed || !size.width || !size.height) return;
    const value = JSON.stringify({version: 1, ...state});
    memoryCameras.set(key, value);
    try { globalThis.sessionStorage?.setItem(key, value); } catch (_) { /* No progress data is touched. */ }
  }
  function schedulePersist() { clearTimeout(saveTimer); saveTimer = setTimeout(persist, 100); }
  function fitScale() { return size.width && size.height ? Math.min(size.width / world.width, size.height / world.height) : 0; }
  function focusScale() { return Math.min(maxScale, Math.max(initialScale, fitScale() * 1.4)); }
  function getState() {
    const fit = fitScale(), overview = state.scale < .65 || (fit > 0 && state.scale <= fit * 1.08);
    return {...state, fitScale: fit, overview, restored: Boolean(saved),
      viewport: {...size}, world: {...world}, defaultFocusScale: focusScale(),
      offsetX: size.width / 2 - state.x * state.scale,
      offsetY: size.height / 2 - state.y * state.scale};
  }
  function apply(reason = 'change') {
    if (destroyed || !size.width || !size.height) return getState();
    state = constrainCamera(state, size, world, maxScale);
    const snapshot = getState();
    worldElement.style.transform = `translate(${snapshot.offsetX}px, ${snapshot.offsetY}px) scale(${state.scale})`;
    worldElement.style.setProperty('--wm-camera-scale', String(state.scale));
    worldElement.style.setProperty('--wm-marker-scale', String(Math.max(1, 1 / state.scale)));
    worldElement.classList.toggle('wm-is-overview', snapshot.overview);
    viewport.dataset.cameraX = state.x.toFixed(4);
    viewport.dataset.cameraY = state.y.toFixed(4);
    viewport.dataset.cameraScale = state.scale.toFixed(6);
    viewport.dataset.cameraOverview = String(snapshot.overview);
    schedulePersist();
    options.onChange?.(snapshot, reason);
    return snapshot;
  }
  function refresh() {
    const width = viewport.clientWidth, height = viewport.clientHeight;
    if (!width || !height) return getState();
    const firstVisible = !size.width || !size.height;
    size = {width, height};
    if (firstVisible && !saved) state.scale = focusScale();
    return apply('resize');
  }
  function viewportToWorld(point) {
    return {x: state.x + (point.x - size.width / 2) / state.scale,
      y: state.y + (point.y - size.height / 2) / state.scale};
  }
  function worldToViewport(point) {
    return {x: size.width / 2 + (point.x - state.x) * state.scale,
      y: size.height / 2 + (point.y - state.y) * state.scale};
  }
  function localPoint(event) {
    const rect = viewport.getBoundingClientRect();
    return {x: event.clientX - rect.left, y: event.clientY - rect.top};
  }
  function zoomBy(factor, point = {x: size.width / 2, y: size.height / 2}) {
    if (!finite(factor) || factor <= 0 || !size.width || !size.height) return getState();
    const anchor = viewportToWorld(point);
    const scale = clamp(state.scale * factor, fitScale(), Math.max(fitScale(), maxScale));
    state = {x: anchor.x + (size.width / 2 - point.x) / scale,
      y: anchor.y + (size.height / 2 - point.y) / scale, scale};
    return apply('zoom');
  }
  function focus(point, scale = focusScale()) {
    if (!point || !finite(point.x) || !finite(point.y)) return getState();
    state = {x: point.x, y: point.y, scale: finite(scale) && scale > 0 ? scale : focusScale()};
    const result = apply('focus'); persist(); return result;
  }
  function fit() {
    state = {x: world.width / 2, y: world.height / 2, scale: fitScale() || initialScale};
    const result = apply('fit'); persist(); return result;
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
      const scale = clamp(gesture.scale * Math.hypot(a.x-b.x,a.y-b.y) / gesture.distance,
        fitScale(), Math.max(fitScale(), maxScale));
      state = {x: gesture.anchor.x + (size.width / 2 - middle.x) / scale,
        y: gesture.anchor.y + (size.height / 2 - middle.y) / scale, scale};
      blockGestureClick(); event.preventDefault(); apply('pinch');
    } else {
      const point = pointers.values().next().value;
      const dx = point.x - gesture.start.x, dy = point.y - gesture.start.y;
      if (!gesture.moved && Math.hypot(dx,dy) <= 6) return;
      gesture.moved = true; capture(event.pointerId); blockGestureClick();
      state = {x: gesture.camera.x - dx / gesture.camera.scale,
        y: gesture.camera.y - dy / gesture.camera.scale, scale: gesture.camera.scale};
      event.preventDefault(); apply('drag');
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
  return {focus,fit,zoomBy,getState,refresh,viewportToWorld,worldToViewport,
    wasGesture:()=>suppressClick && performance.now()<suppressUntil,
    destroy(){persist();destroyed=true;clearTimeout(saveTimer);resize?.disconnect();cancelAll();listeners.forEach(remove=>remove());
      worldElement.style.transform=original.transform;worldElement.style.transformOrigin=original.transformOrigin;
      viewport.style.touchAction=original.touchAction;viewport.style.userSelect=original.userSelect;}};
}
