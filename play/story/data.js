// Authored game narration, separate from book manuscripts and scripture.
// Stable actor/scene IDs are language-independent; only zh-Hant is available.
export const STORY_LOCALE = 'zh-Hant';
export const STORY_FUTURE_LOCALES = Object.freeze(['zh-Hans', 'en', 'ja']);
export const STORY_ACTORS = Object.freeze({
 traveler: Object.freeze({name:'小貓',portrait:new URL('./assets/kitten-traveler-portrait-concept.png',import.meta.url).href}),
 doubt: Object.freeze({name:'五蓋眾・疑',portrait:new URL('./assets/doubt-creature-concept.png',import.meta.url).href}),
 mara: Object.freeze({name:'波旬',portrait:new URL('./assets/mara-portrait-concept.png',import.meta.url).href}),
});
export const STORY_SCENES = Object.freeze({
 'train-desires': Object.freeze({actorId:'traveler',bookId:'four-truths',group:'train-opening',
  text:'好想買雙新鞋，也好想放一天假去看海。\n怎麼愈滑手機，想要的就愈多啊？',
  nextSceneId:'train-breathless'}),
 'train-breathless': Object.freeze({actorId:'traveler',bookId:'four-truths',group:'train-opening',
  text:'錢得省著花，時間也總是不夠。\n唉，我怎麼連喘口氣，都覺得是在耽誤事情？',
  action:'train-arrival'}),
 'arrival-at-wheel': Object.freeze({actorId:'traveler',bookId:'four-truths',group:'arrival',
  text:'咦？我剛才明明還擠在電車上滑手機……怎麼一抬頭，就到了法輪遺跡？進去看看！',
  nextSceneId:'doubt-at-ruins',nextLabel:'接著看'}),
 'doubt-at-ruins': Object.freeze({actorId:'doubt',bookId:'four-truths',group:'arrival',doubtState:'waiting',
  text:'愚痴……',nextSceneId:'doubt-detour',nextLabel:'接著看'}),
 'doubt-detour': Object.freeze({actorId:'traveler',bookId:'four-truths',group:'arrival',doubtState:'waiting',
  text:'這是什麼小傢伙？滿身都是問號，還堵在門口。借過一下……好吧，我從旁邊繞。',
  action:'enter-first-book',nextLabel:'閱讀下一關'}),
 'first-book-insight': Object.freeze({actorId:'traveler',bookId:'four-truths',group:'first-completion',doubtState:'thinning',
  text:'苦、集、滅、道，原來這就是四聖諦。剛才在電車上，我只會喊「好煩」。現在我懂了，那份煩惱，也是一種苦啊。',
  nextSceneId:'doubt-escapes',nextLabel:'接著看'}),
 'doubt-escapes': Object.freeze({actorId:'doubt',bookId:'four-truths',group:'first-completion',doubtState:'receding',
  text:'哎呀！趕快逃！',nextSceneId:'doubt-recedes'}),
 'doubt-recedes': Object.freeze({actorId:'traveler',bookId:'four-truths',group:'first-completion',doubtState:'receding',seenOn:'outro-end',
  text:'咦，牠身上的問號少了好幾個。等等，你要去哪裡？',
  nextSceneId:'toward-aggregates-lake',nextLabel:'接著看'}),
 'mara-watches': Object.freeze({actorId:'mara',bookId:'four-truths',group:'first-completion',
  text:'站在遠方觀看的波旬心想：「可惡，小貓好像慢慢開始破除五蓋了……」',
  action:'show-first-completion',nextLabel:'接著看'}),
 'toward-aggregates-lake': Object.freeze({actorId:'traveler',bookId:'five-aggregates',group:'book-entry',
  text:'可是，從「好想要那雙鞋」到「心裡好煩」，中間到底發生了什麼？那邊有座五陰湖，去看看吧！',
  action:'enter-aggregates-book',nextLabel:'閱讀下一關',dismissLabel:'回到地圖'}),
});
export const STORY_UI = Object.freeze({
 dialogue:'旅程對話',enter:'進去看看',next:'接著看',skip:'先看看地圖',replay:'重看開場對話',
 replayCompletion:'重看四聖諦過場',replayTrain:'重看電車過場',returnToMap:'回到地圖',readNext:'閱讀下一關',questionMark:'？',
 completionTransitionNext:'接著看',completionNext:'前往下一站',completionCity:'前往城池看看',
 doubtStageLabel:'滿身問號的疑，停在法輪遺跡入口',
 storageUnavailable:'這次仍可閱讀；裝置無法保存對話紀錄，下次可能再次顯示。',
 storageCorrupt:'對話紀錄無法讀取，閱讀進度不受影響。',
});
