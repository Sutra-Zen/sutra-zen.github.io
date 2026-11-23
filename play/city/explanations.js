// Short city-panel copy. Source metadata is for audit only, never panel text.
// Keep the original archived scripture intact; see the source audit for the
// author's requested title / plaza wording and the current SuttaCentral edition.
const DISPLAY_TITLE = '相應部35相應245經／如緊叔迦經';
const SOURCE = Object.freeze({
  uid: 'sn35.245',
  translator: '莊春江',
  observedTitle: '像緊叔迦那樣經',
  url: 'https://suttacentral.net/sn35.245/zh/zhuang',
  apiUrl: 'https://suttacentral.net/api/suttas/sn35.245/zhuang?lang=zh',
  staticUrl: 'https://raw.githubusercontent.com/suttacentral/sc-data/636911e1d624b355d86fb3eae3d461bca298466e/html_text/zh/pli/sutta/sn/sn35/sn35.245.html',
  checkedAt: '2026-11-23',
  archivedPath: 'docs/play/canonical/sn35.245.html',
  archivedSHA256: '02a831885b965c463abd72814329e589ab8e8d9edecae25ad8a4ad9aa39e0426',
  location: '城喻義釋段',
  wording: 'verbatim-excerpt',
});
const canonical = (text, source = SOURCE) => Object.freeze({
  title: DISPLAY_TITLE, text, kind: 'canonical', source,
});
const extended = (title, text) => Object.freeze({ title, text, kind: 'extended' });

const cityBody = canonical('『城市』，這是對於這父母生成、米粥積聚、無常削減、磨滅、破壞、分散法之四大身的同義語；');
const sixDoors = canonical('『六道門』，這是對於六內處的同義語；');
const guard = canonical('『守門人』，這是對於念的同義語；');
const messengers = canonical('『一對快速使者』，這是對於止觀的同義語；');
const lord = canonical('『城主』，這是對於識的同義語；');
const message = canonical('『如實話語』，這是對於涅槃的同義語；');
const road = canonical('『來時路』，這是對於八支聖道的同義語，即：對於正見、……（中略）對於正定。');
const plaza = canonical(
  '『在中央四衢街道』，這是四大的同義語，即：地界的、水界的、火界的、風界的。',
  Object.freeze({
    ...SOURCE,
    wording: 'author-supplied-variant',
    observedText: '『在中央廣場』，這是對於四大的同義語，即：對於地界、對於水界、對於火界、對於風界；',
    verification: '作者指定用語；可讀的 SuttaCentral 現行 API 與官方 main 仍使用 observedText。莊春江主站的現行版本因網路 403 未能核實。',
  }),
);

export const CANONICAL_EXPLANATIONS = Object.freeze({
  plaza, town: cityBody,
  eye: sixDoors, ear: sixDoors, nose: sixDoors,
  tongue: sixDoors, body: sixDoors, mind: sixDoors,
  guardian: guard, messengers, lord, message, road,
});

// Some modules mix a canonical object and a teaching scene. The city outline
// uses CANONICAL_EXPLANATIONS.town; city_body here is the Five Aggregates corner.
export const MODULE_EXPLANATIONS = Object.freeze({
  truth_dock: extended('四聖諦・法輪碼頭', '苦、集、滅、道，指出苦及苦止息的道路。'),
  city_body: extended('五陰觀察角', '從色、受、想、行、識五個面向，回看身心經驗。'),
  six_gates: sixDoors,
  conditions_wheel: extended('十二因緣・緣起之輪', '回看經驗與苦如何依條件生起、止息。'),
  noble_path: road,
  confidence_harbor: extended('四不壞淨與六念', '念佛、念法、念僧、念戒、念施、念天，讓我們回顧六念的修習。'),
  mindfulness_guard: guard,
  effort_garden: extended('四正勤・照料花園', '預防、拔草、播種與持續照料，呈現防惡、斷惡、生善、增善。'),
  calm_insight_messengers: messengers,
  endeavor_boat: extended('四如意足・調心小舟', '回看欲、勤、心、觀，以及鬆緊調整的故事。'),
  jhana_garden: extended('四禪・靜水庭園', '澡粉團、湧泉、蓮花池與白布覆身，回看四禪的四個譬喻。'),
  faculties_links: extended('五根五力', '信、精進、念、定、慧，隨已讀內容相互呼應。'),
  awakening_companions: extended('七覺支', '念、擇法、精進、喜、輕安、定、捨，幫助我們依心的狀態調整用功。'),
  fruition_guide: extended('四向四果與十結', '回看修學的方向、果位與十結的教法。'),
});
