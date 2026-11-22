// Authored game narration, separate from book manuscripts and scripture.
// Stable actor/scene IDs are language-independent; only zh-Hant is available.
export const STORY_LOCALE = 'zh-Hant';
export const STORY_FUTURE_LOCALES = Object.freeze(['zh-Hans', 'en', 'ja']);
export const STORY_ACTORS = Object.freeze({
  traveler: Object.freeze({
    name: '小貓',
    portrait: new URL('./assets/kitten-traveler-portrait-concept.png', import.meta.url).href,
  }),
});
export const STORY_SCENES = Object.freeze({
  'arrival-at-wheel': Object.freeze({
    actorId: 'traveler',
    bookId: 'four-truths',
    text: '咦？我剛才明明還趴在窗邊等朋友回訊息……怎麼一抬頭，就到了法輪遺跡？進去看看！',
    action: 'enter-first-book',
  }),
});
export const STORY_UI = Object.freeze({
  dialogue: '旅程對話',
  enter: '進去看看',
  skip: '先看看地圖',
  replay: '重看開場對話',
  returnToMap: '回到海圖',
  storageUnavailable: '這次仍可閱讀；裝置無法保存開場紀錄，下次可能再次顯示。',
  storageCorrupt: '開場紀錄無法讀取，閱讀進度不受影響。',
});
