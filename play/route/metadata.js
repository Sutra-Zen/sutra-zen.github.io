import { routeOrder, rewardDefinitions, combinationScenes } from './data.js?v=summary-merge-1';

// Optional presentation-only metadata. Completion lives exclusively in the
// existing collection store; no completed IDs or reader positions are copied here.
export const ROUTE_METADATA_KEY = 'sutrazen.play.route-metadata.v1';
const fresh = () => ({ version: 1, knownBookIds: [], openedBookIds: [], playedAnimationIds: [] });
const animations = new Set([...rewardDefinitions.map(reward => reward.id), ...combinationScenes.map(scene => scene.id)]);
const clone = value => JSON.parse(JSON.stringify(value));
function validate(raw) {
  if (!raw || raw.version !== 1 || Object.hasOwn(raw, 'completed') || Object.hasOwn(raw, 'completedBookIds') || Object.hasOwn(raw, 'positions')) throw new Error('schema');
  const result = fresh();
  for (const field of ['knownBookIds', 'openedBookIds']) {
    if (!Array.isArray(raw[field]) || raw[field].some(id => !routeOrder.includes(id))) throw new Error('book');
    result[field] = [...new Set(raw[field])];
  }
  if (!Array.isArray(raw.playedAnimationIds) || raw.playedAnimationIds.some(id => !animations.has(id))) throw new Error('animation');
  result.playedAnimationIds = [...new Set(raw.playedAnimationIds)];
  return result;
}
export function createRouteMetadataStore(storage) {
  let state = fresh(), issue = null;
  if (storage === undefined) {
    try { storage = globalThis.localStorage; } catch { storage = null; }
  }
  try {
    if (!storage) throw new Error('unavailable');
    const raw = storage.getItem(ROUTE_METADATA_KEY);
    if (raw) { try { state = validate(JSON.parse(raw)); } catch { issue = 'corrupt'; } }
  } catch { issue = 'unavailable'; }
  const announce = () => {
    if (typeof globalThis.dispatchEvent === 'function' && typeof CustomEvent !== 'undefined') {
      globalThis.dispatchEvent(new CustomEvent('sutrazen:route-metadata', { detail: { issue } }));
    }
  };
  const persist = () => {
    try {
      if (!storage) throw new Error('unavailable');
      storage.setItem(ROUTE_METADATA_KEY, JSON.stringify(state));
    } catch { issue = 'unavailable'; }
    announce();
  };
  return {
    get: () => clone(state),
    get issue() { return issue; },
    markKnown(id) {
      if (!routeOrder.includes(id)) return false;
      if (!state.knownBookIds.includes(id)) state.knownBookIds.push(id);
      persist(); return true;
    },
    markOpened(id) {
      if (!routeOrder.includes(id)) return false;
      if (!state.openedBookIds.includes(id)) state.openedBookIds.push(id);
      if (!state.knownBookIds.includes(id)) state.knownBookIds.push(id);
      persist(); return true;
    },
    markAnimation(id) {
      if (!animations.has(id)) return false;
      if (!state.playedAnimationIds.includes(id)) state.playedAnimationIds.push(id);
      persist(); return true;
    },
    reset() {
      state = fresh(); issue = null;
      try {
        if (!storage) throw new Error('unavailable');
        storage.removeItem(ROUTE_METADATA_KEY);
      } catch { issue = 'unavailable'; }
      announce();
    },
  };
}
export const routeMetadata = createRouteMetadataStore();
