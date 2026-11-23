// Interface and module descriptions are separate from scripture and book text.
export const MODULE_LOCALE = 'zh-Hant';
export const MODULE_FUTURE_LOCALES = Object.freeze(['zh-Hans', 'en', 'ja']);

export const MODULE_COPY = Object.freeze({
  truth_dock: {title:'法輪碼頭',description:'讀完四聖諦後，岸邊的法輪碼頭顯現，作為閱讀旅程的起點。'},
  city_body: {title:'城界與五陰觀察角',description:'沿著城界，從色、受、想、行、識五個面向回看經驗；中央四大花園與識城主仍是原來的底盤。'},
  six_gates: {title:'六道城門',description:'眼、耳、鼻、舌、身、意六門隨閱讀顯現，讓我們認識六內處的入口。'},
  conditions_wheel: {title:'城側緣起之輪',description:'城側的緣起輪庭隨閱讀顯現，回看經驗與苦如何依條件生起和止息。'},
  noble_path: {title:'道路與善行生活',description:'往返道路與善行生活場景隨閱讀顯現，回顧八正道和十善業道。'},
  confidence_harbor: {title:'信心港灣與六念燈景',description:'在港灣點亮六念燈景，回看四不壞淨與六念的故事。'},
  mindfulness_guard: {title:'念-守門人',description:'讓同一位念-守門人進駐六門，回看身、受、心、法四種觀察。'},
  effort_garden: {title:'四正勤照料花園',description:'以預防、拔草、播種及持續照料，回看四正勤的善巧努力。'},
  calm_insight_messengers: {title:'止觀雙使與呼吸場景',description:'止、觀雙使與安靜的呼吸場景隨閱讀顯現；完整城喻仍依各相關讀本與城景齊備呈現。'},
  endeavor_boat: {title:'調心小舟',description:'港灣中的調心小舟，帶我們回看欲、勤、心、觀及鬆緊調整的故事。'},
  jhana_garden: {title:'四禪靜水庭園',description:'澡粉團、湧泉池、蓮花池及白布覆身的既有譬喻庭園隨閱讀顯現。'},
  faculties_links: {title:'五根五力區域呼應',description:'信、勤、念、定、慧區域隨已讀內容相互呼應；尚缺的來源讀本不會自動補齊。'},
  awakening_companions: {title:'七覺支夥伴',description:'念-守門人與貓頭鷹、兔子、藍鳥、烏龜、蓮花、小鹿六位夥伴協調城景；念仍是原來的守門人。'},
  fruition_guide: {title:'果位與十結導覽',description:'既有河岸、花與繫縛意象的導覽場景隨閱讀顯現；這是讀本完成的回饋，不表示取得果位。'},
});

export const MODULE_SLOT_LABELS = Object.freeze({
  'four-elements-garden':'地水火風四大廣場','city-lord':'識・城主',
  'gate-n':'眼門','gate-ne':'耳門','gate-se':'鼻門','gate-s':'舌門','gate-sw':'身門','gate-nw':'意門',
  'mindfulness-guardian':'念-守門人','calm-insight-messengers':'止・觀使者',
});

export const MODULE_UI = Object.freeze({
  autoNoticeTitle:'城池有新變化',
  rewardAdded:title=>`城池已自動新增「${title}」。快到城池看看新的變化吧！`,
  rewardUnlocked:title=>`「${title}」已隨閱讀顯現，可以回城看看。`,
  rewardAlreadyPlaced:title=>`「${title}」已在城中顯現，可以回城看看。`,
  rewardAwaiting:title=>`已讀過「${title}」的相關故事；其餘來源讀本齊備後，城景就會顯現。`,
  inventoryTitle:'城池模組',openInventory:'安置模組',closeInventory:'收起',
  place:'安置',placeFailed:'暫時無法安置，請再試一次。',autoPlace:'自動安置',placeAll:'一鍵安置已取得模組',
  selectedHint:title=>`已選擇${title}，點發光的＋安置，或把卡片拖到＋。`,
  placed:'已顯現',available:'已顯現',locked:'尚未取得',unlocked:'已取得',
  needsPlacement:'請先安置',needsReading:'尚需完成讀本',inspect:'認識',
  messageLabel:'如實消息・涅槃',
  actorLabel:id=>({lord:'識・城主',guardian:'念-守門人',messengers:'止・觀使者',desire:'五蓋眾・貪欲',anger:'五蓋眾・瞋恚',sloth:'五蓋眾・昏沉',restlessness:'五蓋眾・掉悔',doubt:'五蓋眾・疑',mara:'波旬',source_plaza:'地水火風四大廣場','awakening-owl':'擇法夥伴・貓頭鷹','awakening-rabbit':'精進夥伴・兔子','awakening-bird':'喜夥伴・藍鳥','awakening-turtle':'輕安夥伴・烏龜','awakening-lotus':'定夥伴・蓮花','awakening-deer':'捨夥伴・小鹿'})[id]||'城裡的角色',
  zoomIn:'放大',zoomOut:'縮小',fit:'全景',retryArt:'重新載入插畫',
  artFailed:'部分插畫尚未載入，可繼續操作或重試。',
  exploreHint:'拖曳或雙指縮放，點選角色看對話，點選景物看出處。',
  dragHint:'拖曳或雙指縮放，點選角色看對話，點選景物看出處。',cancelSelection:'取消選擇',
  storageIssue:'城中的對話紀錄目前無法永久保存；城景仍會依閱讀進度顯示。',
  sessionIssue:'本次對話紀錄暫存在這個分頁，尚未永久存入裝置。',
  corruptStorage:'原有城中紀錄無法讀取；閱讀進度不受影響，城景仍會依已讀內容顯示。',
  emptyInventory:'讀完繪本後，就能在這裡取得對應模組。',
  baseWaiting:'先讀完四聖諦，四大花園與識城主就會在草地上顯現。',
  baseTitle:'四大花園與識城主',
  baseDescription:'中央廣場對應地、水、火、風四大；花園與城主扮相是故事的美術呈現。',
  baseFree:'起始底盤，不計入十四個閱讀獎勵。',
  readingUnaffected:'城景是閱讀回饋，不影響下一本的閱讀資格，也不判定修證。',
  unrevealedTitle:'尚未揭曉的城景',unrevealedDescription:'隨閱讀旅程前進，最後一站的城景會逐漸揭曉。',
  reset:'清除心想紀錄',resetConfirm:'要清除城中的已看心想紀錄嗎？城景仍依已讀內容顯示，閱讀進度與原網站資料不會變更。',
  unknownModule:'找不到這個城市模組。',alreadyPlaced:'這個模組已安置。',
  notUnlocked:'請先讀完對應繪本。',missingBase:'請先完成四聖諦，讓起始底盤顯現。',
  invalidBackup:'這份城市配置備份無法讀取，原配置未變更。',
  placedCount:count=>`城景已顯現 ${count}／14 項`,
  missingModules:titles=>`尚待相關城景：${titles.join('、')}`,
  missingBooks:titles=>`尚需完成：${titles.join('、')}`,
});
