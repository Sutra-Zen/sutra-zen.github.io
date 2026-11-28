// Shared game-only access rules. Public readers without collection=1 remain free.
// This module has no persistence and does not import selectors or a store.
import { routeOrder, FINAL_BOOK_ID, FIRST_THIRTEEN } from './data.js?v=summary-merge-1';
import { CATALOG } from '../collection/catalog.js?v=summary-merge-1';
const catalog = new Map(CATALOG.map(book => [book.id, book]));
const values = completed => completed instanceof Set ? [...completed] : Array.isArray(completed) ? completed : [];
export const completedGameBookIds = completed => [...new Set(values(completed).filter(id => catalog.has(id)))];
export function currentGameBookId(completed) {
  const done = new Set(completedGameBookIds(completed));
  return routeOrder.find(id => !done.has(id)) || null;
}
export function canStartGameBook(id, completed) {
  return catalog.has(id) && currentGameBookId(completed) === id;
}
export function canReviewGameBook(id, completed) {
  return catalog.has(id) && completedGameBookIds(completed).includes(id);
}
export function canReadGameBook(id, completed) {
  return canStartGameBook(id, completed) || canReviewGameBook(id, completed);
}
export function canCompleteGameBook(id, completed) {
  // Repeated completion is handled as a no-write success by the store; a review
  // is never eligible for a new completion event or reward.
  return canStartGameBook(id, completed);
}
export function isFinalGameBookRevealed(completed) {
  const done = new Set(completedGameBookIds(completed));
  return done.has(FINAL_BOOK_ID) || FIRST_THIRTEEN.every(id => done.has(id));
}
export function getGameBookAccess(id, completed, positions = {}) {
  const book = catalog.get(id), canStart = canStartGameBook(id, completed), canReview = canReviewGameBook(id, completed);
  const at = positions?.[id], hasBookmark = Boolean(book && Number.isInteger(at) && at >= 0 && at < book.totalSteps);
  return {
    id, known: Boolean(book), canStart, canReview, canRead: canStart || canReview,
    canComplete: canStart, isCurrent: canStart,
    status: canReview ? 'completed' : canStart ? (hasBookmark ? 'reading' : 'available') : 'locked',
    hasBookmark,
    // A preserved future bookmark is not an entry or a mainline resume target.
    resumePosition: (canStart || canReview) && hasBookmark ? at : null,
    totalSteps: book?.totalSteps || 0,
  };
}
