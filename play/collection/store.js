import { CATALOG_IDS } from './catalog.js';

// Collection achievement never controls access to the public readers.
export const STORAGE_KEY = 'sutrazen.play.collection.v1';
const known = id => CATALOG_IDS.includes(id);
const fresh = () => ({ version: 1, positions: {}, completed: [], activeBook: CATALOG_IDS[0] });
const clone = value => JSON.parse(JSON.stringify(value));
let issue = null;
function validate(raw) {
  if (!raw || raw.version !== 1 || !known(raw.activeBook) || !Array.isArray(raw.completed) ||
      raw.completed.some(id => !known(id)) || !raw.positions ||
      typeof raw.positions !== 'object' || Array.isArray(raw.positions)) throw new Error('schema');
  const result = fresh();
  for (const [id, index] of Object.entries(raw.positions)) {
    if (!known(id) || !Number.isInteger(index) || index < 0 || index > 10000) throw new Error('position');
    result.positions[id] = index;
  }
  result.completed = [...new Set(raw.completed)];
  result.activeBook = raw.activeBook;
  return result;
}
let state;
try {
  const raw = localStorage.getItem(STORAGE_KEY);
  try { state = raw ? validate(JSON.parse(raw)) : fresh(); }
  catch { state = fresh(); issue = 'corrupt'; }
} catch { state = fresh(); issue = 'unavailable'; }
function announce() {
  window.dispatchEvent(new CustomEvent('sutrazen:collection-progress', { detail: { issue } }));
}
function persist() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
  catch { issue = 'unavailable'; }
  announce();
}
export const store = {
  get: () => clone(state),
  get issue() { return issue; },
  savePosition(id, index) {
    if (!known(id) || !Number.isInteger(index) || index < 0 || index > 10000) return false;
    state.positions[id] = index; state.activeBook = id; persist(); return true;
  },
  complete(id) {
    if (!known(id)) return false;
    if (!state.completed.includes(id)) state.completed.push(id);
    state.activeBook = id; persist(); return true;
  },
  reset() {
    state = fresh(); issue = null;
    try { localStorage.removeItem(STORAGE_KEY); } catch { issue = 'unavailable'; }
    announce();
  },
  exportBackup: () => JSON.stringify(state, null, 2),
  restoreBackup(text) {
    let restored; try { restored = validate(JSON.parse(text)); } catch { return false; }
    state = restored; issue = null; persist(); return true;
  },
};
window.addEventListener('storage', event => {
  if (event.key !== STORAGE_KEY) return;
  try { state = event.newValue ? validate(JSON.parse(event.newValue)) : fresh(); issue = null; }
  catch { issue = 'corrupt'; }
  announce();
});
