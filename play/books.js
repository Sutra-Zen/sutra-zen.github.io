// Stable IDs and original reader locations; story/scripture remain in their original books.
export const BOOKS = Object.freeze([
  { id: 'four-truths', title: '四聖諦', path: '../four-truths/book/', thumbnail: '../four-truths/book/images/footprints.jpg', symbol: '☸︎' },
  { id: 'five-aggregates', title: '五陰', path: '../five-aggregates/book/', thumbnail: '../five-aggregates/book/images/a01.webp', symbol: '❀' },
  { id: 'six-senses', title: '六處', path: '../six-senses/book/', thumbnail: '../six-senses/cover.webp', symbol: '⌂' }
]);
export const BOOK_IDS = BOOKS.map(book => book.id);
