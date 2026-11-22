// Shared game navigation. Original public pages are not modified or injected.
// UI copy is separate from book titles, narration and scripture.
export const NAV_TEXT = Object.freeze({
  label: '遊戲導覽', map: '海圖', mindmap: '心智圖', city: '城池', shelf: '書架',
});
export const NAV_ITEMS = Object.freeze([
  { id: 'map', href: new URL('../game/', import.meta.url).href },
  { id: 'mindmap', href: new URL('../index.html#map-heading', import.meta.url).href },
  { id: 'city', href: new URL('./city/', import.meta.url).href },
  { id: 'shelf', href: new URL('./visual-v2/shelf.html', import.meta.url).href },
].map(item => Object.freeze({ ...item, label: NAV_TEXT[item.id] })));
const castleIcon = '<svg class="sz-game-nav__castle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M3 21V7h3V4h3v3h6V4h3v3h3v14M3 12h18M3 21h18M9 21v-5a3 3 0 0 1 6 0v5"/><path d="M6 9h.01M18 9h.01"/></svg>';
export function renderGameNavigation({ active } = {}) {
  return `<nav class="sz-game-nav" aria-label="${NAV_TEXT.label}">${NAV_ITEMS.map(item => `<a class="sz-game-nav__link${item.id === active ? ' is-active' : ''}" data-game-nav="${item.id}" href="${item.href}"${item.id === active ? ' aria-current="page"' : ''}>${item.id === 'city' ? castleIcon : ''}<span>${item.label}</span></a>`).join('')}</nav>`;
}
