import { CATALOG } from '../collection/catalog.js';
import { getGameBookAccess, isFinalGameBookRevealed } from './eligibility.js';
import {
  routeOrder, FINAL_BOOK_ID, FIRST_THIRTEEN, rewardDefinitions,
  combinationScenes, facultiesSources, landmarkBooks, endingDefinition,
} from './data.js';
export { routeOrder, FINAL_BOOK_ID, FIRST_THIRTEEN } from './data.js';
const catalog = new Map(CATALOG.map(book => [book.id, book]));
export const routeBooks = Object.freeze(routeOrder.map((id, index) => Object.freeze({ ...catalog.get(id), order: index + 1 })));
export { rewardDefinitions, combinationScenes, canonicalCorrespondences, endingDefinition, landmarkBooks } from './data.js';
const array = value => value instanceof Set ? [...value] : Array.isArray(value) ? value : [];
const doneSet = completed => new Set(array(completed).filter(id => routeOrder.includes(id)));
const hasEvery = (set, ids) => ids.every(id => set.has(id));
const missing = (set, ids) => ids.filter(id => !set.has(id));
function knownFinal(set) { return isFinalGameBookRevealed(set); }

export function recommendNextBook(completed, supportedBookIds = routeOrder) {
  const set = doneSet(completed), supported = new Set(array(supportedBookIds));
  return routeOrder.find(id => supported.has(id) && !set.has(id)) || null;
}
export function sceneAvailability(completed) {
  const set = doneSet(completed);
  return Object.fromEntries(combinationScenes.map(scene => [scene.id, {
    ...scene, available: hasEvery(set, scene.requiredBookIds), missingBookIds: missing(set, scene.requiredBookIds),
  }]));
}
export function deriveCityState(completed, positions = {}, metadata = {}) {
  const set = doneSet(completed), combinations = sceneAvailability(completed);
  const rewards = rewardDefinitions.map(reward => {
    const earned = set.has(reward.bookId), available = earned && hasEvery(set, reward.requiredBookIds);
    return { ...reward, earned, available, preview: earned && !available, missingBookIds: missing(set, reward.requiredBookIds) };
  });
  const features = Object.fromEntries(rewards.map(reward => [reward.id, reward.available]));
  features.four_elements_plaza = features.city_body;
  features.city_lord = features.city_body;
  features.truthful_message = combinations.city_allegory.available;
  features.garden_irrigation = features.city_body && combinations.garden_irrigation.available;
  const stage = features.city_body ? (features.six_gates ? 3 : 2) : (features.truth_dock ? 1 : 0);
  const facultiesZones = Object.fromEntries(Object.entries(facultiesSources).map(([id, source]) => {
    const linked = set.has('five-roots-powers') && set.has(source.bookId);
    const placement = ['five-aggregates', ...(id === 'mindfulness' ? ['six-senses'] : [])];
    return [id, { ...source, linked, available: linked && hasEvery(set, placement),
      preview: set.has('five-roots-powers') && !(linked && hasEvery(set, placement)),
      sourceCompleted: set.has(source.bookId),
      conditionsLinked: id === 'wisdom' && linked && set.has('twelve-links'),
      missingBookIds: missing(set, ['five-roots-powers', source.bookId, ...placement]),
    }];
  }));
  return {
    stage, stageId: ['initial_outline', 'dock_and_city_silhouette', 'city_body_and_lord', 'six_gate_city'][stage],
    completedBookIds: routeOrder.filter(id => set.has(id)), features, rewards, facultiesZones,
    sceneFlags: Object.fromEntries(Object.entries(combinations).map(([id, scene]) => [id, scene.available])),
    finalChapterRevealed: knownFinal(set, positions, metadata),
    ending: { ...endingDefinition, available: combinations.ending_release.available },
  };
}
export function routeStatus(completed, positions = {}, metadata = {}) {
  const set = doneSet(completed), finalChapterRevealed = knownFinal(set, positions, metadata);
  const combinations = sceneAvailability(completed), nextBookId = recommendNextBook(completed);
  const books = routeOrder.map((id, index) => {
    const book = catalog.get(id), completedBook = set.has(id), position = positions?.[id];
    const access = getGameBookAccess(id, completed, positions);
    return { ...book, ...access, order: index + 1, completed: completedBook,
      revealed: id !== FINAL_BOOK_ID || finalChapterRevealed,
      mainlineTitle: id === FINAL_BOOK_ID && !finalChapterRevealed ? '尚未揭曉的旅程' : book.title,
      // Reading position never creates a completion. Completed re-reading keeps its bookmark.
      position: Number.isInteger(position) && position >= 0 ? position : null,
      inProgress: access.canStart && access.hasBookmark,
    };
  });
  const landmarks = Object.fromEntries(Object.entries(landmarkBooks).map(([id, bookId]) => [id, {
    ...getGameBookAccess(bookId, completed, positions), id, bookId, active: set.has(bookId),
    visible: bookId !== FINAL_BOOK_ID || finalChapterRevealed,
  }]));
  return {
    version: '2026-11-22-r3', eligibilityPolicy: 'strict-sequential-v1', total: routeOrder.length,
    completedBookIds: routeOrder.filter(id => set.has(id)), count: set.size,
    nextBookId, books, finalChapterRevealed,
    endingAvailable: combinations.ending_release.available,
    ending: { ...endingDefinition, available: combinations.ending_release.available },
    combinations, landmarks,
    world: { pathBaseVisible: true, harborAccessible: true,
      pathActive: set.has('eightfold-path'), wholesomeLakeActive: set.has('eightfold-path'),
      gardenActive: set.has('right-effort'), irrigationActive: combinations.garden_irrigation.available },
    city: deriveCityState(completed, positions, metadata),
  };
}
