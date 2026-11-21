// UI language is separate from the unchanged stories and their scripture editions.
export const LANGUAGES = Object.freeze({ 'zh-Hant': { available: true }, 'zh-Hans': { available: false }, en: { available: false }, ja: { available: false } });
export const zhHant = {
  cityMarker: '中央城池', travelerCaption: '帶著「念」，一起出發', travelerAlt: '抱著念燈籠的小橘貓旅人，取自七覺支原插畫', title: 'SutraZen 繪本旅程', trial: '試玩版', home: '回修道地圖', eyebrow: '一座島，一本書，一步一步讀。', heading: '跟著小貓，走進佛法繪本', intro: '從四聖諦出發，認識五陰與六處。依自己的步調翻頁，讀完後回來，看看城池慢慢亮起。',
  start: '開始旅程', resume: '繼續閱讀', nextBook: '繼續旅程', reread: '重讀第一本', progress: n => `已讀 ${n}／3 本`, stage: '第一段旅程', first: '從四聖諦開始，不需要操船或答題。', resumeAt: (title, page) => `${title}・接續第 ${page} 頁`,
  mapTitle: '海島閱讀路線', mapHint: '先讀四聖諦，再走向五陰與六處。中央城池記錄這段旅程。', statuses: { locked: '尚未解鎖', available: '可以閱讀', reading: '閱讀中', complete: '已完成' }, unlock: '讀完前一本後開放', read: '開始閱讀', readAgain: '再次閱讀',
  city: '城池的變化', blueprint: '看完整城池配置', sources: '城喻與經典對讀', cityIntro: '每完成一本，城池便多一些光彩。這是閱讀回饋，不是修證或斷結的判定。', later: '後續旅程', laterText: '其餘十一冊仍在原網站公開閱讀。試玩版先走完這三座島，後續路線再慢慢展開。', shelf: '前往原網站書架',
  free: '自由選章', freeTitle: '自由選章，隨心閱讀', freeIntro: '這裡可以選讀三本。閱讀位置另存，不會增加完成冊數，也不會改變依序旅程的進度。', ordered: '回依序旅程', more: '更多選項', clear: '清除這段旅程', clearTitle: '清除旅程紀錄？', clearText: '只清除本試玩版的閱讀位置與完成紀錄，不影響原網站或其他資料。', confirmClear: '確認清除', cancel: '取消', close: '關閉',
  backup: '下載進度備份', restore: '還原進度備份', restored: '進度已還原。', invalid: '無法讀取這份備份，原進度已保留。', restoreTitle: '還原備份？', restoreText: '這會以選取的備份取代目前旅程紀錄。', confirmRestore: '確認還原', reduce: '減少過場動畫', storageUnavailable: '目前無法儲存到裝置，仍可在這個頁面閱讀。離開或重整後，進度可能無法保留。', storageCorrupt: '裝置中的旅程紀錄無法讀取，已先開啟新的旅程；你仍可閱讀，也可還原備份。',
  sailing: '搭船前往閱讀島', sailingText: title => `下一站：${title}。帶著「念」的燈籠，一起出發。`, skip: '略過，開始閱讀',
  completed: title => `《${title}》讀完了`, feedback: ['岸邊的道路與花草顯現了。', '中央廣場的地、水、火、風更清楚了。', '六座城門亮起，第一段路線留下你的閱讀足跡。'], feedbackNote: '城景變化是教學設計；城池本身的經典對應，可在「完整城池配置」查看。', continue: '繼續旅程', allDone: '第一段旅程完成', allDoneText: '四聖諦、五陰、六處，三本都已讀完。可以再讀一次，也可以回書架探索其他繪本。', freeDone: title => `《${title}》自由閱讀結束`, freeDoneText: '這次閱讀沒有加入依序旅程的完成紀錄，原旅程仍保留。',
  prototypeArt: '旅人肖像暫取自七覺支既有插畫；航行以燈籠標記示意。', savedLocal: '免登入・進度儲存在此瀏覽器', noJS: '試玩版需要 JavaScript 才能保存旅程；原繪本仍可從書架閱讀。'
};
export const t = zhHant; // Other locales remain unavailable until UI AND content are reviewed.
