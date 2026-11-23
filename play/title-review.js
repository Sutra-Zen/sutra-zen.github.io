import {resetJourney} from './journey-save.js?v=auto-city-1';

// Temporary author opt-in UI, not authentication or a game unlock mechanism.
// Turn this off when the author-testing round ends; ordinary /game/ never
// creates the reset control. It grants no access to uncompleted books.
export const AUTHOR_REVIEW_ENABLED = true;
export function authorReviewEnabled(url = location.href) {
  const address = new URL(url);
  return AUTHOR_REVIEW_ENABLED && /^\/game(?:\/|$)/.test(address.pathname) && address.searchParams.get('author') === '1';
}

export function resetAuthorJourney() { return resetJourney(); }
