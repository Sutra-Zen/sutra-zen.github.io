import {store,SESSION_FALLBACK_KEY} from './collection/store.js';
import {routeMetadata} from './route/metadata.js';
import {storyStore} from './story/store.js?v=prologue-1';

// Temporary author opt-in UI, not authentication or a game unlock mechanism.
// Turn this off when the author-testing round ends; ordinary /game/ never
// creates the reset control. It grants no access to uncompleted books.
export const AUTHOR_REVIEW_ENABLED = true;
export function authorReviewEnabled(url = location.href) {
  const address = new URL(url);
  return AUTHOR_REVIEW_ENABLED && /^\/game(?:\/|$)/.test(address.pathname) && address.searchParams.get('author') === '1';
}

export function resetAuthorJourney() {
  const failures = [];
  store.reset();
  // Existing readers share the unversioned store URL. A browser may still
  // have the previous reset implementation cached; verify its recovery cleanup
  // here too without creating a second store instance or erasing fresh recovery
  // needed when the canonical removal itself failed.
  if (!store.issue) {
    try { sessionStorage.removeItem(SESSION_FALLBACK_KEY); }
    catch {
      failures.push(SESSION_FALLBACK_KEY);
      try { sessionStorage.setItem(SESSION_FALLBACK_KEY, JSON.stringify({version:1,baseRaw:null,state:store.get()})); } catch {}
    }
  }
  routeMetadata.reset();
  storyStore.reset();
  // The title has not mounted a camera yet. Only the game's exact session
  // entries are removed; original readers and other site settings survive.
  for (const key of ['sutrazen.play.camera.v1', 'sutrazen.play.map-tip.v1']) {
    try { sessionStorage.removeItem(key); } catch { failures.push(key); }
  }
  return { persistent: !store.issue && !routeMetadata.issue && !storyStore.issue && !failures.length };
}
