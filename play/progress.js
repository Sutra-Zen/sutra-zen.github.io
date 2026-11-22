import { BOOKS, BOOK_IDS } from './books.js';
export { BOOKS };
export const STORAGE_KEY = 'sutrazen.play.v1';
const fresh = () => ({ version: 1, replayBook: null, positions: {}, freePositions: {}, completed: [], activeBook: BOOK_IDS[0], orderedBook: BOOK_IDS[0], mode: 'ordered', settings: { locale: 'zh-Hant', reducedMotion: false } });
let issue = null;
function validate(raw) {
  if (!raw || raw.version !== 1 || !['ordered', 'free'].includes(raw.mode) || !BOOK_IDS.includes(raw.activeBook) || !BOOK_IDS.includes(raw.orderedBook) || !Array.isArray(raw.completed) || raw.completed.some(id => !BOOK_IDS.includes(id))) throw new Error('schema');
  const completed = [...new Set(raw.completed)];
  if (completed.some((id, i) => id !== BOOK_IDS[i])) throw new Error('sequence');
  if (raw.replayBook != null && (!BOOK_IDS.includes(raw.replayBook) || !completed.includes(raw.replayBook))) throw new Error('replay');
  const clean = fresh();
  for (const key of ['positions', 'freePositions']) {
    if (!raw[key] || typeof raw[key] !== 'object' || Array.isArray(raw[key])) throw new Error('positions');
    for (const [id, value] of Object.entries(raw[key])) {
      if (!BOOK_IDS.includes(id) || !Number.isInteger(value) || value < 0 || value > 10000) throw new Error('position');
      clean[key][id] = value;
    }
  }
  return { ...clean, ...Object.fromEntries(['activeBook', 'orderedBook', 'mode'].map(k => [k, raw[k]])), positions: clean.positions, freePositions: clean.freePositions, completed, replayBook: raw.replayBook || null, settings: { locale: ['zh-Hant', 'zh-Hans', 'en', 'ja'].includes(raw.settings?.locale) ? raw.settings.locale : 'zh-Hant', reducedMotion: raw.settings?.reducedMotion === true } };
}
let state;
try {
  const raw = localStorage.getItem(STORAGE_KEY);
  try { state = raw ? validate(JSON.parse(raw)) : fresh(); }
  catch { state = fresh(); issue = 'corrupt'; }
} catch { state = fresh(); issue = 'unavailable'; }
const clone = value => JSON.parse(JSON.stringify(value));
function persist() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
  catch { issue = 'unavailable'; }
  window.dispatchEvent(new CustomEvent('sutrazen:play-progress', { detail: { issue } }));
}
function known(id) { return BOOK_IDS.includes(id); }
function canRead(id) { const index = BOOK_IDS.indexOf(id); return index >= 0 && (index === 0 || state.completed.includes(BOOK_IDS[index - 1])); }
export const store = {
  get: () => clone(state),
  get issue() { return issue; },
  canRead,
  setActive(id, mode = 'ordered') {
    if (!known(id) || !['ordered', 'free'].includes(mode) || (mode === 'ordered' && !canRead(id))) return false;
    state.mode = mode; state.activeBook = id;
    if (mode === 'ordered') state.orderedBook = id;
    persist(); return true;
  },
  savePosition(id, index, mode = 'ordered') {
    if (!known(id) || !Number.isInteger(index) || index < 0 || index > 10000 || !['ordered', 'free'].includes(mode) || (mode === 'ordered' && !canRead(id))) return false;
    state[mode === 'free' ? 'freePositions' : 'positions'][id] = index;
    state.activeBook = id; state.mode = mode;
    if (mode === 'ordered') { state.orderedBook = id; state.replayBook = state.completed.includes(id) ? id : null; }
    persist(); return true;
  },
  finish(id, mode = 'ordered') {
    if (mode !== 'ordered' || !canRead(id)) return false;
    if (!state.completed.includes(id)) state.completed.push(id);
    const next = BOOK_IDS.find(key => !state.completed.includes(key));
    state.replayBook = null; state.mode = 'ordered'; state.activeBook = next || id; state.orderedBook = next || id;
    persist(); return true;
  },
  reset() { state = fresh(); issue = null; try { localStorage.removeItem(STORAGE_KEY); } catch { issue = 'unavailable'; } window.dispatchEvent(new CustomEvent('sutrazen:play-progress')); },
  exportBackup: () => JSON.stringify(state, null, 2),
  restoreBackup(text) { let parsed; try { parsed = validate(JSON.parse(text)); } catch { return false; } state = parsed; issue = null; persist(); return true; },
  setReducedMotion(value) { state.settings.reducedMotion = Boolean(value); persist(); }
};
window.addEventListener('storage', event => {
  if (event.key !== STORAGE_KEY) return;
  try { state = event.newValue ? validate(JSON.parse(event.newValue)) : fresh(); window.dispatchEvent(new CustomEvent('sutrazen:play-progress')); }
  catch { issue = 'corrupt'; }
});
