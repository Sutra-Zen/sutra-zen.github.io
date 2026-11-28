// Stable IDs and original site paths. These labels are UI copy, not scripture.
// totalSteps is verified reader navigation metadata, not a copy of narration or scripture.
// Seven Factors counts 36 cues + its closing reading step, rather than only 12 scenes.
// Every URL is relative to this module; resolve using new URL(value, import.meta.url).
export const CATALOG = [
  {
    "id": "four-truths",
    "title": "四聖諦",
    "number": 1,
    "totalSteps": 29,
    "reader": "../../four-truths/book/",
    "guide": "../../four-truths/",
    "unreadIcon": null,
    "cover": "../../four-truths/book/images/footprints.webp"
  },
  {
    "id": "five-aggregates",
    "title": "五陰",
    "number": 2,
    "totalSteps": 54,
    "reader": "../../five-aggregates/book/",
    "guide": "../../five-aggregates/",
    "unreadIcon": "../visual-v2/assets/shelf-02.svg",
    "cover": "../../five-aggregates/book/images/a10.webp"
  },
  {
    "id": "six-senses",
    "title": "六處",
    "number": 3,
    "totalSteps": 115,
    "reader": "../../six-senses/book/",
    "guide": "../../six-senses/",
    "unreadIcon": "../visual-v2/assets/shelf-03.svg",
    "cover": "../../six-senses/cover.webp"
  },
  {
    "id": "twelve-links",
    "title": "十二因緣",
    "number": 4,
    "totalSteps": 77,
    "reader": "../../twelve-links/book/",
    "guide": "../../twelve-links/",
    "unreadIcon": "../visual-v2/assets/shelf-04.svg",
    "cover": "../../twelve-links/cover.webp"
  },
  {
    "id": "eightfold-path",
    "title": "八正道與十善業道",
    "number": 5,
    "totalSteps": 110,
    "reader": "../../eightfold-path/book/?collectionPageVersion=2",
    "guide": "../../eightfold-path/",
    "unreadIcon": "../visual-v2/assets/shelf-05.svg",
    "cover": "../../docs/eightfold-path/assets/02-right-view.webp"
  },
  {
    "id": "four-fruits-ten-fetters",
    "title": "四向四果與十結",
    "number": 6,
    "totalSteps": 75,
    "reader": "../../four-fruits-ten-fetters/book/",
    "guide": "../../four-fruits-ten-fetters/",
    "unreadIcon": "../visual-v2/assets/shelf-06.svg",
    "cover": "../../docs/four-fruits-ten-fetters/assets/s01.webp"
  },
  {
    "id": "four-purities-six-recollections",
    "title": "四不壞淨與六念",
    "number": 7,
    "totalSteps": 95,
    "reader": "../../four-purities-six-recollections/book/",
    "guide": "../../four-purities-six-recollections/",
    "unreadIcon": "../visual-v2/assets/shelf-07.svg",
    "cover": "../../docs/four-purities-six-recollections/assets/IMG_0395.jpeg"
  },
  {
    "id": "mindfulness",
    "title": "四念處與四顛倒",
    "number": 8,
    "totalSteps": 111,
    "reader": "../../mindfulness/book/",
    "guide": "../../mindfulness/",
    "unreadIcon": "../visual-v2/assets/shelf-08.svg",
    "cover": "../../docs/mindfulness/assets/8ACD7BAD-64C1-476B-A4AD-7A63F5A2048E.png"
  },
  {
    "id": "right-effort",
    "title": "四正勤",
    "number": 9,
    "totalSteps": 81,
    "reader": "../../right-effort/book/",
    "guide": "../../right-effort/",
    "unreadIcon": "../visual-v2/assets/shelf-09.svg",
    "cover": "../../docs/right-effort/assets/6FEE22D5-C7AA-476E-810C-DDE063530A82.png"
  },
  {
    "id": "anapana",
    "title": "安那般那與止觀",
    "number": 10,
    "totalSteps": 119,
    "reader": "../../anapana/book/",
    "guide": "../../anapana/",
    "unreadIcon": "../visual-v2/assets/shelf-10.svg",
    "cover": "../../anapana/assets/S01.webp"
  },
  {
    "id": "iddhipada",
    "title": "四如意足",
    "number": 11,
    "totalSteps": 82,
    "reader": "../../iddhipada/book/",
    "guide": "../../iddhipada/",
    "unreadIcon": "../visual-v2/assets/shelf-11.svg",
    "cover": "../../iddhipada/assets/S01.webp"
  },
  {
    "id": "four-jhanas",
    "title": "四禪",
    "number": 12,
    "totalSteps": 131,
    "reader": "../../four-jhanas/book/",
    "guide": "../../four-jhanas/",
    "unreadIcon": "../visual-v2/assets/shelf-12.svg",
    "cover": "../../four-jhanas/assets/S06.webp"
  },
  {
    "id": "five-roots-powers",
    "title": "五根五力",
    "number": 13,
    "totalSteps": 75,
    "reader": "../../five-roots-powers/book/",
    "guide": "../../five-roots-powers/",
    "unreadIcon": "../visual-v2/assets/shelf-13.svg",
    "cover": "../../five-roots-powers/assets/S03.webp"
  },
  {
    "id": "seven-factors",
    "title": "七覺支",
    "number": 14,
    "totalSteps": 37,
    "reader": "../../seven-factors/book/",
    "guide": "../../seven-factors/",
    "unreadIcon": "../visual-v2/assets/shelf-14.svg",
    "cover": "../../seven-factors/assets/12.webp"
  }
];
export const CATALOG_IDS = CATALOG.map(book => book.id);
export const COLLECTION_TEXT = {
  returnShelf: '回到書架',
  completeBook: '完成這本',
  nextPage: '下一頁',
  storageTitle: '閱讀紀錄提醒',
  storageUnavailable: '這個瀏覽器暫時無法保存閱讀紀錄，離開後可能無法續讀；本次仍可閱讀。',
  storageCorrupt: '原有收集紀錄無法讀取，這次會從新的紀錄開始。十四本繪本仍可自由閱讀。',
  keepReading: '繼續閱讀',
  integrationUnavailable: '收集紀錄暫時無法使用，仍可閱讀原繪本。',
  paginationUnavailable: '新版讀本尚未完整載入，這一頁暫不更新閱讀進度。請重新載入讀本，或回到旅程再試。',
  reloadReader: '重新載入讀本',
  returnJourney: '回到旅程',
};
