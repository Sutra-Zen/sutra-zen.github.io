import { STORY_SCENES } from './data.js?v=summary-merge-1';

// Presentation only. Never reads or writes completion, bookmarks or eligibility.
export const STORY_STORAGE_KEY = 'sutrazen.play.story.v1';
const SESSION_KEY = 'sutrazen.play.story.session.v1';
const fresh = () => ({ version: 1, seenSceneIds: [] });
function validate(raw) {
  if (!raw || raw.version !== 1 || !Array.isArray(raw.seenSceneIds) ||
      raw.seenSceneIds.some(id => !Object.hasOwn(STORY_SCENES, id)) ||
      Object.hasOwn(raw, 'completed') || Object.hasOwn(raw, 'positions')) throw Error('schema');
  return { version: 1, seenSceneIds: [...new Set(raw.seenSceneIds)] };
}
export function createStoryStore(storage, session) {
  let state = fresh(), issue = null, localRaw = null, localReadable = true;
  if (storage === undefined) { try { storage = globalThis.localStorage; } catch { storage = null; } }
  if (session === undefined) { try { session = globalThis.sessionStorage; } catch { session = null; } }
  try {
    if (!storage) throw Error('unavailable');
    localRaw = storage.getItem(STORY_STORAGE_KEY);
    if (localRaw) { try { state = validate(JSON.parse(localRaw)); } catch { issue = 'corrupt'; } }
  } catch { localReadable = false; issue = 'unavailable'; }
  // Quota errors can leave localStorage readable but stale. A same-tab fallback
  // remains valid only while its base local value has not changed externally.
  try {
    const raw = session?.getItem(SESSION_KEY), recovery = raw && JSON.parse(raw);
    if (recovery && recovery.version === 1 && (recovery.baseRaw === null || typeof recovery.baseRaw === 'string')) {
      if (!localReadable || recovery.baseRaw === localRaw) {
        state = validate(recovery.state); issue = 'unavailable';
        if (!localReadable) localRaw = recovery.baseRaw;
      } else session?.removeItem(SESSION_KEY);
    }
  } catch {}
  return {
    get: () => ({ version: 1, seenSceneIds: [...state.seenSceneIds] }),
    get issue() { return issue; },
    hasSeen: id => state.seenSceneIds.includes(id),
    markSeen(id) {
      if (!Object.hasOwn(STORY_SCENES, id)) return false;
      if (state.seenSceneIds.includes(id)) return true;
      state.seenSceneIds.push(id);
      try {
        if (!storage) throw Error('unavailable');
        const raw = JSON.stringify(state);
        storage.setItem(STORY_STORAGE_KEY, raw); localRaw = raw; issue = null;
        try { session?.removeItem(SESSION_KEY); } catch {}
      } catch {
        issue = 'unavailable';
        try { session?.setItem(SESSION_KEY, JSON.stringify({ version: 1, baseRaw: localRaw, state })); } catch {}
      }
      return true;
    },
    reset() {
      state = fresh(); issue = null;
      let localReset = false;
      try {
        if (!storage) throw Error('unavailable');
        storage.removeItem(STORY_STORAGE_KEY); localRaw = null; localReset = true;
      } catch { issue = 'unavailable'; }
      let sessionReset = true;
      try { session?.removeItem(SESSION_KEY); } catch { sessionReset = false; issue = 'unavailable'; }
      if (!localReset || !sessionReset) {
        // Replace any stale fallback with the empty state too. A successful
        // local deletion must not resurrect a same-tab 'seen' fallback.
        try { session?.setItem(SESSION_KEY, JSON.stringify({ version: 1, baseRaw: localRaw, state })); } catch {}
      }
    },
  };
}
export const storyStore = createStoryStore();
