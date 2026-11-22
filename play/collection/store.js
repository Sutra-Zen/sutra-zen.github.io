import { CATALOG_IDS, CATALOG } from './catalog.js';
import { canReadGameBook, canReviewGameBook, canCompleteGameBook, currentGameBookId } from '../route/eligibility.js';

// Collection achievement never controls access to the public readers.
export const STORAGE_KEY = 'sutrazen.play.collection.v1';
// Recovery is a single-tab continuation only, never an additional completion set.
export const SESSION_FALLBACK_KEY = 'sutrazen.play.collection.session.v1';
const known = id => CATALOG_IDS.includes(id);
const stepCounts = new Map(CATALOG.map(book => [book.id, book.totalSteps]));
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
let state, lastLocalRaw = null;
function readRecovery() {
  try {
    const raw = sessionStorage.getItem(SESSION_FALLBACK_KEY);
    if (!raw) return null;
    const record = JSON.parse(raw);
    if (!record || record.version !== 1 || !(record.baseRaw === null || typeof record.baseRaw === 'string')) return null;
    return { baseRaw: record.baseRaw, state: validate(record.state) };
  } catch { return null; }
}
function clearRecovery() { try { sessionStorage.removeItem(SESSION_FALLBACK_KEY); } catch {} }
function saveRecovery() {
  try { sessionStorage.setItem(SESSION_FALLBACK_KEY, JSON.stringify({version:1,baseRaw:lastLocalRaw,state})); }
  catch {} // With both storage mechanisms blocked, this document remains usable.
}
let localReadable = true;
try { lastLocalRaw = localStorage.getItem(STORAGE_KEY); }
catch { localReadable = false; issue = 'unavailable'; }
const recovery = readRecovery();
if (recovery && (!localReadable || recovery.baseRaw === lastLocalRaw)) {
  // A quota failure can leave a valid but stale local value. Prefer this tab's
  // continuation only while the canonical local value still matches its base.
  state = recovery.state;
  if (!localReadable) lastLocalRaw = recovery.baseRaw;
  issue = 'unavailable';
} else {
  if (recovery) clearRecovery(); // External restore/new canonical save wins; never merge.
  try { state = lastLocalRaw ? validate(JSON.parse(lastLocalRaw)) : fresh(); }
  catch { state = fresh(); issue = 'corrupt'; }
}

function announce() {
  window.dispatchEvent(new CustomEvent('sutrazen:collection-progress', { detail: { issue } }));
}
function persist() {
  try {
    const raw = JSON.stringify(state); localStorage.setItem(STORAGE_KEY, raw);
    lastLocalRaw = raw; clearRecovery();
    if (issue === 'unavailable') issue = null;
  } catch { issue = 'unavailable'; saveRecovery(); }
  announce();
}
export const store = {
  get: () => clone(state),
  get issue() { return issue; },
  savePosition(id, index) {
    if (!known(id) || !Number.isInteger(index) || index < 0 || index >= stepCounts.get(id) || !canReadGameBook(id, state.completed)) return false;
    state.positions[id] = index;
    // Review bookmarks belong to that book, not to the mainline active target.
    if (!canReviewGameBook(id, state.completed)) state.activeBook = id;
    persist(); return true;
  },
  complete(id) {
    if (!known(id)) return false;
    if (state.completed.includes(id)) return true; // Idempotent, with no write/event/reward.
    if (!canCompleteGameBook(id, state.completed) || state.positions[id] !== stepCounts.get(id) - 1) return false;
    state.completed.push(id);
    state.activeBook = currentGameBookId(state.completed) || id;
    persist(); return true;
  },
  reset() {
    state = fresh(); issue = null;
    let recoveryRemoved = true;
    try { sessionStorage.removeItem(SESSION_FALLBACK_KEY); }
    catch { recoveryRemoved = false; issue = 'unavailable'; }
    try { localStorage.removeItem(STORAGE_KEY); lastLocalRaw = null; }
    catch { issue = 'unavailable'; saveRecovery(); }
    // Deleting the canonical value must not revive a stale session fallback
    // whose base was also null. Replace it with this empty state if possible.
    if (!recoveryRemoved) saveRecovery();
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
  try { state = event.newValue ? validate(JSON.parse(event.newValue)) : fresh(); lastLocalRaw = event.newValue; clearRecovery(); issue = null; }
  catch { issue = 'corrupt'; }
  announce();
});
