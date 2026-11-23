import { createMapCamera } from '../../worldmap-v4/camera.js';
import { MODULES, BASE_PLINTH } from './catalog.js?v=modular-city-1';
import { MODULE_UI as T } from './text.js?v=modular-city-1';
import { CITY_MODULE_ART } from './art.js?v=modular-city-1';

const WORLD = { width: 1600, height: 900 };
const escape = value => String(value ?? '').replace(/[&<>"']/g, character =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]));
const artwork = key => CITY_MODULE_ART.sprites?.[key] || CITY_MODULE_ART[key];
const titleOf = module => module?.title || '';
const format = (key, ...args) => typeof T[key] === 'function' ? T[key](...args) : T[key] || '';
let spriteSequence = 0;
function croppedImage(art) {
  const x = art.x || 0, y = art.y || 0, width = art.w || art.width, height = art.h || art.height;
  const id = 'city-sprite-clip-' + ++spriteSequence;
  // Clipping the SVG viewport alone is insufficient with meet letterboxing:
  // a neighbouring atlas cell would otherwise paint into the unused margins.
  return `<defs><clipPath id="${id}"><rect x="${x}" y="${y}" width="${width}" height="${height}"/></clipPath></defs><g clip-path="url(#${id})"><image href="${escape(art.src || art.url)}" x="0" y="0" width="${art.atlasWidth || width}" height="${art.atlasHeight || height}"/></g>`;
}

// One transparent atlas remains intact. SVG viewBox selects a real painted
// sprite; no building, character, or image text is reconstructed by code.
export function renderSprite(assetKey, { className = '', style = '', label = '', attachments = true } = {}) {
  const art = artwork(assetKey); if (!art) return '';
  const x = art.x || 0, y = art.y || 0, width = art.w || art.width, height = art.h || art.height;
  if (!(width > 0 && height > 0)) return '';
  const attached = attachments ? (art.attachments || []).map(part => {
    const image = artwork(part.assetKey); if (!image) return '';
    return `<svg x="${x + width * part.xPct / 100}" y="${y + height * part.yPct / 100}" width="${width * part.widthPct / 100}" height="${height * part.heightPct / 100}" viewBox="${image.x || 0} ${image.y || 0} ${image.w || image.width} ${image.h || image.height}" preserveAspectRatio="xMidYMid meet">${croppedImage(image)}</svg>`;
  }).join('') : '';
  return `<svg class="${escape(className)}" style="${escape(style)}" viewBox="${x} ${y} ${width} ${height}" preserveAspectRatio="xMidYMid meet" ${label ? `role="img" aria-label="${escape(label)}"` : 'aria-hidden="true"'} focusable="false">${croppedImage(art)}${attached}</svg>`;
}

export function initializeModularCity({ host, getState, onPlace, onThought, onInspect, onChange } = {}) {
  if (!host || typeof getState !== 'function') throw new TypeError('A city host and getState are required.');
  const root = document.createElement('section'); root.className = 'mod-city';
  root.innerHTML = `<div class="mod-city__viewport" tabindex="0" aria-label="${escape(format('dragHint'))}"><div class="mod-city__world" data-city-world="1600x900"><img class="mod-city__ground" alt="" draggable="false"><div class="mod-city__art-layer"></div><div class="mod-city__npc-layer"></div><div class="mod-city__target-layer"></div></div></div><div class="mod-city__art-notice" role="status" hidden><span></span><button type="button" data-city-art-retry></button></div><aside class="mod-city__inventory" aria-label="${escape(format('inventoryTitle'))}"><button type="button" class="mod-city__inventory-toggle" data-city-inventory-toggle aria-expanded="false"><span></span><span aria-hidden="true">⌃</span></button><div class="mod-city__drawer" hidden><div class="mod-city__inventory-heading"><h2></h2><button type="button" data-city-inventory-close></button></div><p class="mod-city__selection-hint"></p><div class="mod-city__inventory-list"></div><div class="mod-city__inventory-actions"><button type="button" class="mod-city__auto-place" data-city-place-all></button><button type="button" class="mod-city__auto-place" data-city-auto-place></button><button type="button" data-city-selection-cancel></button></div><p class="mod-city__storage-note" role="status" hidden></p></div></aside><div class="mod-city__announcement" role="status" aria-live="polite"></div>`;
  host.append(root);
  const $ = selector => root.querySelector(selector), viewport = $('.mod-city__viewport');
  const world = $('.mod-city__world'), ground = $('.mod-city__ground');
  const artLayer = $('.mod-city__art-layer'), npcLayer = $('.mod-city__npc-layer'), targetLayer = $('.mod-city__target-layer');
  const drawer = $('.mod-city__drawer'), inventory = $('.mod-city__inventory');
  let destroyed = false, selected = null, drawerOpen = false, pending = false, drag = null, selectionCleared = false;
  let worldSignature = '', inventorySignature = '', state = null, artFailed = false;
  const listeners = [];
  const groundArt = CITY_MODULE_ART.ground; ground.src = groundArt.src || groundArt.url;
  ground.width = WORLD.width; ground.height = WORLD.height;
  $('.mod-city__inventory-heading h2').textContent = format('inventoryTitle');
  $('[data-city-inventory-close]').textContent = format('closeInventory');
  $('[data-city-auto-place]').textContent = format('autoPlace');
  $('[data-city-place-all]').textContent = format('placeAll');
  $('[data-city-selection-cancel]').textContent = format('cancelSelection');
  $('[data-city-art-retry]').textContent = format('retryArt');
  $('.mod-city__art-notice span').textContent = format('artFailed');
  const camera = createMapCamera(viewport, world, {
    ...WORLD, initialCenter: { x: 800, y: 450 }, initialScale: .95,
    storageKey: 'sutrazen.play.city.camera.v1',
    getInsets: () => ({ bottom: Math.max(0, inventory.getBoundingClientRect().height + 12) }),
    onChange: snapshot => onChange?.({ type: 'camera', camera: snapshot, selectedModuleId: selected }),
  });

  function listen(target, name, handler, options) {
    target.addEventListener(name, handler, options); listeners.push(() => target.removeEventListener(name, handler, options));
  }
  function announce(message) { $('.mod-city__announcement').textContent = message || ''; }
  function models(snapshot) {
    if (Array.isArray(snapshot.modules)) return snapshot.modules;
    const completed = new Set(snapshot.completed || []), placed = new Set(snapshot.placedIds || []);
    return MODULES.map(module => ({ ...module, unlocked: completed.has(module.bookId), placed: placed.has(module.id),
      missingModuleIds: (module.requires || []).filter(id => !placed.has(id)),
      canPlace: completed.has(module.bookId) && !placed.has(module.id) && (module.requires || []).every(id => placed.has(id)) }));
  }
  function readState() {
    const snapshot = getState() || {}, modules = models(snapshot);
    return { ...snapshot, modules, baseVisible: snapshot.baseVisible ?? (snapshot.completed || []).includes('four-truths'),
      labels: snapshot.labels !== false };
  }
  function moduleById(id) { return state.modules.find(module => module.id === id); }
  function placementPoint(module) {
    if (module.placementAnchor) return module.placementAnchor;
    const slot = module.slots.find(candidate => candidate.visible !== false) || module.slots[0];
    return slot ? { x: slot.x, y: slot.y } : { x: 800, y: 450 };
  }
  function artError() { artFailed = true; $('.mod-city__art-notice').hidden = false; }
  function attachArtErrors(parent) { parent.querySelectorAll('image').forEach(image => image.addEventListener('error', artError)); }
  function artNode(slot, module, { base = false, primary = false } = {}) {
    if (slot.effect) {
      const glow = document.createElement('span'); glow.className = 'mod-city__effect';
      glow.dataset.citySlot = slot.id; if (module) glow.dataset.cityModule = module.id;
      glow.dataset.cityEffect = slot.effect; glow.setAttribute('aria-hidden', 'true');
      Object.assign(glow.style, { left: slot.x + 'px', top: slot.y + 'px', width: slot.width + 'px',
        height: (slot.height || slot.width * .65) + 'px', zIndex: String(slot.z || 37) });
      return glow;
    }
    const art = artwork(slot.assetKey); if (!art) { artError(); return null; }
    const actor = slot.actorId, inspectId = slot.inspectId || (actor === 'source_plaza' ? 'plaza' : module?.id);
    const node = document.createElement(actor || inspectId ? 'button' : 'div');
    node.className = 'mod-city__placed-art' + (actor ? ' mod-city__actor mod-city__actor--' + actor : '');
    if (node.tagName === 'BUTTON') node.type = 'button';
    node.dataset.citySlot = slot.id || slot.assetKey;
    if (module) node.dataset.cityModule = module.id;
    if (actor && actor !== 'source_plaza') node.dataset.cityActor = actor;
    else if (inspectId) node.dataset.cityInspect = inspectId;
    const width = slot.width || 140, height = slot.height || width * ((art.h || art.height) / (art.w || art.width));
    Object.assign(node.style, { left: slot.x + 'px', top: slot.y + 'px', width: width + 'px', height: height + 'px',
      zIndex: String(slot.z ?? (base ? 5 : Math.round(slot.y / 10) + 10)) });
    const label = slot.label || (primary ? titleOf(module) : '');
    node.setAttribute('aria-label', label || titleOf(module) || format('inventoryTitle'));
    node.innerHTML = renderSprite(slot.assetKey, { className: 'mod-city__sprite mod-city__actor-art', attachments: slot.assetKey !== 'messengers' });
    if (label) {
      const caption = document.createElement('span'); caption.className = 'mod-city__world-label'; caption.textContent = label;
      caption.hidden = !state.labels; node.append(caption);
    }
    if (actor === 'lord') {
      node.classList.toggle('is-calm', state.placedIds?.includes('mindfulness_guard'));
      for (let i = 0; i < 2; i++) { const drop = document.createElement('span'); drop.className = 'mod-city__sweat'; drop.setAttribute('aria-hidden', 'true'); node.append(drop); }
    }
    return node;
  }
  const npcDefinitions = [
    { id: 'desire', keys: ['hindrance_desire'], near: [603, 472], far: [280, 495] },
    { id: 'anger', keys: ['hindrance_anger', 'hindrance_ill_will'], near: [993, 479], far: [1330, 460] },
    { id: 'sloth', keys: ['hindrance_sloth'], near: [611, 619], far: [360, 740] },
    { id: 'restlessness', keys: ['hindrance_restlessness'], near: [987, 622], far: [1290, 725] },
    { id: 'doubt', keys: ['hindrance_doubt'], near: [807, 663], far: [1120, 665] },
    { id: 'mara', keys: ['mara'], near: [1081, 315], far: [1360, 260], width: 110 },
  ];
  function renderWorld() {
    const signature = JSON.stringify({ base: state.baseVisible, placed: state.modules.filter(module => module.placed).map(module => [module.id, module.slots.filter(slot => slot.visible !== false).map(slot => slot.id)]),
      guard: state.placedIds?.includes('mindfulness_guard'), labels: state.labels });
    if (signature === worldSignature) return;
    worldSignature = signature; artLayer.replaceChildren(); npcLayer.replaceChildren();
    if (state.baseVisible) for (const slot of BASE_PLINTH.slots) {
      const node = artNode(slot, null, { base: true }); if (node) artLayer.append(node);
    }
    for (const module of state.modules.filter(module => module.placed)) {
      module.slots.filter(slot => slot.visible !== false).forEach((slot, index) => {
        const node = artNode(slot, module, { primary: index === 0 }); if (node) artLayer.append(node);
        if (slot.assetKey === 'messengers' && artwork('scroll')) {
          const scroll = artNode({ id: 'truthful-scroll', x: slot.x, y: slot.y + (slot.height || 170) * .05,
            width: slot.width * .8, height: (slot.height || 170) * .26, assetKey: 'scroll', z: (slot.z || 46) + 1,
            inspectId: 'message', label: format('messageLabel') }, module);
          if (scroll) artLayer.append(scroll);
        }
      });
    }
    if (state.baseVisible) for (const npc of npcDefinitions) {
      const assetKey = npc.keys.find(key => artwork(key)); if (!assetKey) continue;
      const [x, y] = state.placedIds?.includes('mindfulness_guard') ? npc.far : npc.near;
      const label = format('actorLabel', npc.id) || npc.id;
      const node = artNode({ id: 'npc-' + npc.id, x, y, width: npc.width || 84, assetKey, actorId: npc.id, label, z: 85 }, null);
      if (node) { node.classList.add('mod-city__npc'); node.dataset.cityNpc = npc.id; npcLayer.append(node); }
    }
    attachArtErrors(artLayer); attachArtErrors(npcLayer);
  }
  function renderTargets() {
    targetLayer.replaceChildren();
    const module = moduleById(selected); if (!module?.canPlace) return;
    const point = placementPoint(module), button = document.createElement('button');
    button.type = 'button'; button.className = 'mod-city__target'; button.dataset.cityPlace = module.id;
    Object.assign(button.style, { left: point.x + 'px', top: point.y + 'px' });
    button.setAttribute('aria-label', format('place') + ' ' + titleOf(module));
    button.innerHTML = '<span aria-hidden="true">＋</span><span class="mod-city__target-label"></span>';
    button.lastElementChild.textContent = titleOf(module); targetLayer.append(button);
  }
  function statusText(module) {
    if (module.placed) return format('placed');
    if (module.canPlace) return format('available');
    if (!module.unlocked) return format('locked');
    const missing = [];
    if (module.missingBookIds?.length) missing.push(format('missingBooks', module.missingBookIds.map(id => {
      const book = state.modules.find(candidate => candidate.bookId === id); return book?.bookTitle || titleOf(book) || id;
    })));
    if (module.missingModuleIds?.length) missing.push(format('missingModules', module.missingModuleIds.map(id => titleOf(moduleById(id)))));
    return missing.join('；') || format('needsPlacement');
  }
  function renderInventory() {
    const signature = JSON.stringify(state.modules.map(module => [module.id, module.unlocked, module.placed, module.canPlace, module.missingModuleIds]));
    if (signature !== inventorySignature) {
      inventorySignature = signature;
      const list = $('.mod-city__inventory-list'); list.replaceChildren();
      for (const module of state.modules) {
        const card = document.createElement('button'); card.type = 'button'; card.className = 'mod-city__inventory-card';
        card.dataset.cityInventory = module.id; card.dataset.cityModuleState = module.placed ? 'placed' : module.canPlace ? 'available' : module.unlocked ? 'waiting' : 'locked';
        card.disabled = !module.canPlace && !module.placed; card.setAttribute('aria-label', titleOf(module) + '，' + statusText(module));
        const thumbnail = module.revealed === false ? null : module.inventoryAssetKey || module.slots.find(slot => !slot.effect)?.assetKey;
        card.innerHTML = `<span class="mod-city__inventory-art">${renderSprite(thumbnail, { className: 'mod-city__sprite' })}</span><span class="mod-city__inventory-title"></span><small></small>`;
        card.querySelector('.mod-city__inventory-title').textContent = titleOf(module); card.querySelector('small').textContent = statusText(module); list.append(card);
      }
      attachArtErrors(list);
    }
    root.querySelectorAll('[data-city-inventory]').forEach(card => card.setAttribute('aria-pressed', String(card.dataset.cityInventory === selected)));
    const current = moduleById(selected), count = state.modules.filter(module => module.canPlace).length;
    $('[data-city-inventory-toggle] span').textContent = format('openInventory') + (count ? ' · ' + count : '');
    $('.mod-city__selection-hint').textContent = current?.canPlace ? format('selectedHint', titleOf(current)) : format('dragHint');
    $('[data-city-auto-place]').disabled = !current?.canPlace || pending;
    $('[data-city-place-all]').disabled = !count || pending;
    $('[data-city-selection-cancel]').hidden = !selected;
    const note = $('.mod-city__storage-note'); note.hidden = !state.issue; note.textContent = state.issue ? format('storageIssue') : '';
  }
  function render() {
    if (destroyed) return;
    state = readState();
    if (!moduleById(selected)?.canPlace) selected = selectionCleared ? null : state.modules.find(module => module.canPlace)?.id || null;
    renderWorld(); renderTargets(); renderInventory(); camera.refresh();
  }
  function setDrawer(open) {
    drawerOpen = Boolean(open); drawer.hidden = !drawerOpen;
    $('[data-city-inventory-toggle]').setAttribute('aria-expanded', String(drawerOpen));
    root.classList.toggle('is-inventory-open', drawerOpen); camera.refresh();
  }
  function select(id, { focus = true } = {}) {
    if (destroyed) return false;
    if (id === null) {
      if (drag) finishDrag({ pointerId: drag.pointerId }, true);
      selected = null; selectionCleared = true; renderTargets(); renderInventory();
      onChange?.({ type: 'selection', selectedModuleId: null }); return true;
    }
    state = readState(); const module = moduleById(id);
    if (!module?.canPlace) { if (module?.placed) onInspect?.(id); return false; }
    selected = id; selectionCleared = false; renderTargets(); renderInventory(); announce(format('selectedHint', titleOf(module)));
    if (focus) camera.focus(placementPoint(module), Math.max(camera.getState().scale, .95));
    onChange?.({ type: 'selection', selectedModuleId: selected }); return true;
  }
  async function place(id) {
    if (pending || destroyed) return false;
    state = readState(); const module = moduleById(id), all = id === 'all';
    if (all ? !state.modules.some(candidate => candidate.canPlace) : !module?.canPlace) return false;
    pending = true; root.classList.add('is-placing'); renderInventory();
    try {
      const result = await onPlace?.(id), accepted = result === true || result?.ok === true;
      if (accepted) { announce((all ? format('placeAll') : titleOf(module)) + '，' + format('placed')); render(); }
      else { render(); announce(module ? statusText(moduleById(id) || module) : format('placeFailed')); }
      return accepted;
    } catch (_) {
      render(); announce(format('placeFailed')); return false;
    } finally { pending = false; root.classList.remove('is-placing'); if (!destroyed) renderInventory(); }
  }
  function finishDrag(event, cancel = false) {
    if (!drag || drag.pointerId !== event.pointerId) return;
    const ended = drag; drag = null; ended.ghost?.remove(); root.classList.remove('is-dragging-module');
    try { if (ended.card.hasPointerCapture(event.pointerId)) ended.card.releasePointerCapture(event.pointerId); } catch (_) {}
    targetLayer.querySelector('.mod-city__target')?.classList.remove('is-drop-ready');
    if (!ended.moved || cancel) return;
    ended.card.dataset.suppressClick = 'true';
    const rect = viewport.getBoundingClientRect(), at = camera.viewportToWorld({ x: event.clientX - rect.left, y: event.clientY - rect.top });
    const module = moduleById(ended.id), target = module && placementPoint(module);
    if (module?.canPlace && target && Math.hypot(at.x - target.x, at.y - target.y) * camera.getState().scale <= 80) place(ended.id);
  }
  function pointerDown(event) {
    const card = event.target.closest('[data-city-inventory]');
    if (!card || card.disabled || event.button > 0 || pending) return;
    const module = moduleById(card.dataset.cityInventory); if (!module?.canPlace) return;
    delete card.dataset.suppressClick;
    drag = { pointerId: event.pointerId, pointerType: event.pointerType, id: module.id, card,
      startX: event.clientX, startY: event.clientY, moved: false };
  }
  function pointerMove(event) {
    if (!drag || event.pointerId !== drag.pointerId) return;
    if (!drag.moved && Math.hypot(event.clientX - drag.startX, event.clientY - drag.startY) < 8) return;
    // Horizontal swipes browse the tray. A deliberate vertical lift starts a
    // placement drag; it never disables the tray's native touch scrolling.
    if (!drag.moved && drag.pointerType !== 'mouse' && Math.abs(event.clientX - drag.startX) > Math.abs(event.clientY - drag.startY) * 1.2) return;
    if (!drag.moved) {
      drag.moved = true; select(drag.id);
      try { drag.card.setPointerCapture(event.pointerId); } catch (_) {}
      drag.ghost = document.createElement('div'); drag.ghost.className = 'mod-city__drag-ghost';
      const module = moduleById(drag.id), thumbnail = module.inventoryAssetKey || module.slots.find(slot => !slot.effect)?.assetKey;
      drag.ghost.innerHTML = renderSprite(thumbnail, { className: 'mod-city__sprite' }); root.append(drag.ghost);
      root.classList.add('is-dragging-module');
    }
    event.preventDefault();
    const rect = root.getBoundingClientRect(); Object.assign(drag.ghost.style, { left: event.clientX - rect.left + 'px', top: event.clientY - rect.top + 'px' });
    const view = viewport.getBoundingClientRect(), at = camera.viewportToWorld({ x: event.clientX - view.left, y: event.clientY - view.top });
    const target = placementPoint(moduleById(drag.id));
    targetLayer.querySelector('.mod-city__target')?.classList.toggle('is-drop-ready', Math.hypot(at.x - target.x, at.y - target.y) * camera.getState().scale <= 80);
  }
  listen(root, 'pointerdown', pointerDown, { passive: true });
  listen(window, 'pointermove', pointerMove, { passive: false });
  listen(window, 'pointerup', event => finishDrag(event));
  listen(window, 'pointercancel', event => finishDrag(event, true));
  listen(root, 'click', event => {
    const button = event.target.closest('button'); if (!button) return;
    if (button.dataset.suppressClick) {
      delete button.dataset.suppressClick;
      if (event.detail !== 0) { event.preventDefault(); event.stopPropagation(); return; }
    }
    if (button.hasAttribute('data-city-inventory-toggle')) setDrawer(!drawerOpen);
    else if (button.hasAttribute('data-city-inventory-close')) setDrawer(false);
    else if (button.hasAttribute('data-city-auto-place')) place(selected);
    else if (button.hasAttribute('data-city-place-all')) place('all');
    else if (button.hasAttribute('data-city-selection-cancel')) select(null);
    else if (button.hasAttribute('data-city-art-retry')) {
      artFailed = false; $('.mod-city__art-notice').hidden = true;
      root.querySelectorAll('image').forEach(image => { const href = image.getAttribute('href'); image.removeAttribute('href'); image.setAttribute('href', href); });
      const src = ground.src; ground.removeAttribute('src'); ground.src = src;
    }
    else if (button.dataset.cityInventory) select(button.dataset.cityInventory);
    else if (button.dataset.cityPlace) place(button.dataset.cityPlace);
    else if (button.dataset.cityActor) onThought?.(button.dataset.cityActor);
    else if (button.dataset.cityInspect) onInspect?.(button.dataset.cityInspect);
  });
  listen(ground, 'error', artError);
  const resize = new ResizeObserver(() => camera.refresh()); resize.observe(inventory);
  render();
  return { render, update: render, select, selectModule: select, autoPlace: id => place(id || selected),
    fit: () => camera.fit(), zoomBy: factor => camera.zoomBy(factor),
    focus(id) {
      if (id === BASE_PLINTH.id) return camera.focus({ x: 800, y: 440 }, .95);
      const module = moduleById(id); if (module) return camera.focus(placementPoint(module), .95);
    },
    getState: () => ({ selectedModuleId: selected, drawerOpen, pending, artFailed, camera: camera.getState() }),
    renderSprite,
    destroy() { if (destroyed) return; if (drag) finishDrag({ pointerId: drag.pointerId }, true); destroyed = true; resize.disconnect(); camera.destroy(); listeners.forEach(remove => remove()); root.remove(); },
  };
}
