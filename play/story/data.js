// Authored game narration, separate from book manuscripts and scripture.
// Stable actor/scene IDs are language-independent; only zh-Hant is available.
export const STORY_LOCALE = 'zh-Hant';
export const STORY_FUTURE_LOCALES = Object.freeze(['zh-Hans', 'en', 'ja']);
export const STORY_ACTORS = Object.freeze({
 traveler: Object.freeze({name:'小貓',portrait:new URL('./assets/kitten-traveler-portrait-concept.png',import.meta.url).href}),
 doubt: Object.freeze({name:'五蓋眾・疑',portrait:new URL('./assets/doubt-creature-concept.png',import.meta.url).href}),
});
export const STORY_SCENES = Object.freeze({
 'arrival-at-wheel': Object.freeze({actorId:'traveler',bookId:'four-truths',group:'arrival',
  text:'咦？我剛才明明還趴在窗邊等朋友回訊息……怎麼一抬頭，就到了法輪遺跡？進去看看！',
  nextSceneId:'doubt-at-ruins',nextLabel:'進去看看'}),
 'doubt-at-ruins': Object.freeze({actorId:'doubt',bookId:'four-truths',group:'arrival',doubtState:'waiting',
  text:'愚痴……',nextSceneId:'doubt-detour',nextLabel:'接著看'}),
 'doubt-detour': Object.freeze({actorId:'traveler',bookId:'four-truths',group:'arrival',doubtState:'waiting',
  text:'這隻滿身問號的生物是什麼啊？竟然擋在入口……我先繞過牠，進去看看好了。',
  action:'enter-first-book',nextLabel:'開始閱讀四聖諦'}),
 'first-book-insight': Object.freeze({actorId:'traveler',bookId:'four-truths',group:'first-completion',doubtState:'thinning',
  text:'讀完四聖諦，苦與離苦的路好像清楚一點了。「正智」和「慧根／慧力」，我也想繼續慢慢練習！',
  nextSceneId:'doubt-recedes',nextLabel:'接著看',dismissLabel:'看閱讀回饋'}),
 'doubt-recedes': Object.freeze({actorId:'traveler',bookId:'four-truths',group:'first-completion',doubtState:'receding',
  text:'咦，剛才那隻怪生物身上的問號變少了……牠退進霧裡，入口也露出來了。先把剛才學到的記在心裡，再走下一站吧！',
  action:'show-first-completion',nextLabel:'看看旅程的變化',dismissLabel:'看閱讀回饋'}),
});
export const STORY_UI = Object.freeze({
 dialogue:'旅程對話',enter:'進去看看',next:'接著看',skip:'先看看地圖',replay:'重看開場對話',
 replayCompletion:'重看四聖諦過場',returnToMap:'回到海圖',questionMark:'？',
 doubtStageLabel:'滿身問號的疑，停在法輪遺跡入口',
 storageUnavailable:'這次仍可閱讀；裝置無法保存對話紀錄，下次可能再次顯示。',
 storageCorrupt:'對話紀錄無法讀取，閱讀進度不受影響。',
});
