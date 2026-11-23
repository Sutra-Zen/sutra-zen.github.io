import { createMapCamera } from '../../worldmap-v4/camera.js';
import { MODULES, BASE_PLINTH } from './catalog.js?v=auto-city-1';
import { MODULE_UI as T } from './text.js?v=auto-city-1';
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

export function initializeModularCity({ host, getState, getInsets, onThought, onInspect, onChange } = {}) {
  if (!host || typeof getState !== 'function') throw new TypeError('A city host and getState are required.');
  const root = document.createElement('section'); root.className = 'mod-city';
  root.innerHTML = `<div class="mod-city__viewport" tabindex="0" aria-label="${escape(format('exploreHint'))}"><div class="mod-city__world" data-city-world="1600x900"><img class="mod-city__ground" alt="" draggable="false"><div class="mod-city__art-layer"></div><div class="mod-city__npc-layer"></div></div></div><div class="mod-city__art-notice" role="status" hidden><span></span><button type="button" data-city-art-retry></button></div>`;
  host.append(root);
  const $ = selector => root.querySelector(selector), viewport = $('.mod-city__viewport');
  const world = $('.mod-city__world'), ground = $('.mod-city__ground');
  const artLayer = $('.mod-city__art-layer'), npcLayer = $('.mod-city__npc-layer');
  let destroyed = false, worldSignature = '', state = null, artFailed = false;
  const listeners = [];
  const groundArt = CITY_MODULE_ART.ground; ground.src = groundArt.src || groundArt.url;
  ground.width = WORLD.width; ground.height = WORLD.height;
  $('[data-city-art-retry]').textContent = format('retryArt');
  $('.mod-city__art-notice span').textContent = format('artFailed');
  function visibleInsets() {
    if (typeof getInsets === 'function') return getInsets();
    const view = viewport.getBoundingClientRect(), dock = document.querySelector('.game-dock')?.getBoundingClientRect();
    return { bottom: dock ? Math.max(0, view.bottom - Math.max(view.top, dock.top)) : 0 };
  }
  const camera = createMapCamera(viewport, world, {
    ...WORLD, initialCenter: { x: 800, y: 440 }, initialScale: .95,
    storageKey: 'sutrazen.play.city.camera.v1', getInsets: visibleInsets,
    onChange: snapshot => onChange?.({ type: 'camera', camera: snapshot }),
  });
  function listen(target, name, handler, options) {
    target.addEventListener(name, handler, options); listeners.push(() => target.removeEventListener(name, handler, options));
  }
  function readState() {
    const snapshot = getState() || {};
    const placed = new Set(snapshot.placedIds || []);
    const modules = Array.isArray(snapshot.modules) ? snapshot.modules : MODULES.map(module => ({ ...module, placed: placed.has(module.id) }));
    return { ...snapshot, modules, baseVisible: snapshot.baseVisible ?? (snapshot.completed || []).includes('four-truths') };
  }
  function focusPoint(module) {
    if (module.placementAnchor) return module.placementAnchor;
    const slot = module.slots.find(candidate => candidate.visible !== false) || module.slots[0];
    return slot ? { x: slot.x, y: slot.y } : { x: 800, y: 440 };
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
    node.setAttribute('aria-label', label || (actor ? format('actorLabel', actor) : titleOf(module)) || format('inventoryTitle'));
    node.innerHTML = renderSprite(slot.assetKey, { className: 'mod-city__sprite mod-city__actor-art', attachments: slot.assetKey !== 'messengers' });
    if (label) {
      const caption = document.createElement('span'); caption.className = 'mod-city__world-label'; caption.textContent = label;
      node.append(caption);
    }
    return node;
  }
  const npcDefinitions = [
    { id: 'desire', keys: ['hindrance_desire'], near: [603, 472], far: [280, 495] },
    { id: 'anger', keys: ['hindrance_anger', 'hindrance_ill_will'], near: [993, 479], far: [1330, 460] },
    { id: 'sloth', keys: ['hindrance_sloth'], near: [611, 619], far: [360, 740] },
    { id: 'restlessness', keys: ['hindrance_restlessness'], near: [987, 622], far: [1290, 725] },
    { id: 'doubt', keys: ['hindrance_doubt'], near: [807, 663], far: [1120, 665] },
    { id: 'mara', keys: ['mara'], near: [500, 130], far: [250, 230], width: 110 },
  ];
  function renderWorld() {
    const signature = JSON.stringify({ base: state.baseVisible, placed: state.modules.filter(module => module.placed).map(module => [module.id, module.slots.filter(slot => slot.visible !== false).map(slot => slot.id)]),
      guard: state.placedIds?.includes('mindfulness_guard') });
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
  function render() {
    if (destroyed) return;
    state = readState(); renderWorld(); camera.refresh();
  }
  listen(root, 'click', event => {
    const button = event.target.closest('button'); if (!button) return;
    if (button.hasAttribute('data-city-art-retry')) {
      artFailed = false; $('.mod-city__art-notice').hidden = true;
      root.querySelectorAll('image').forEach(image => { const href = image.getAttribute('href'); image.removeAttribute('href'); image.setAttribute('href', href); });
      const src = ground.src; ground.removeAttribute('src'); ground.src = src;
    } else if (button.dataset.cityActor) onThought?.(button.dataset.cityActor);
    else if (button.dataset.cityInspect) onInspect?.(button.dataset.cityInspect);
  });
  listen(ground, 'error', artError);
  const dock = document.querySelector('.game-dock');
  const resize = dock && typeof ResizeObserver === 'function' ? new ResizeObserver(() => camera.refresh()) : null;
  resize?.observe(dock);
  render();
  return { render, update: render, fit: () => camera.fit(), returnFromOverview: () => camera.returnFromOverview(),
    refresh: () => camera.refresh(), zoomBy: factor => camera.zoomBy(factor),
    focus(id) {
      if (id === BASE_PLINTH.id) return camera.focus({ x: 800, y: 440 }, .95);
      const module = state.modules.find(candidate => candidate.id === id);
      if (module?.placed) return camera.focus(focusPoint(module), .95);
    },
    getState: () => ({ artFailed, camera: camera.getState() }), renderSprite,
    destroy() { if (destroyed) return; destroyed = true; resize?.disconnect(); camera.destroy(); listeners.forEach(remove => remove()); root.remove(); },
  };
}
