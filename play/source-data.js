// Scripture metadata and scene labels are kept separate from progress logic.
export const CITY_TEXT = {
  title: '城池配置草圖',
  description: '六座城門環繞中央四大廣場，守門者代表念，一對使者代表止觀，城主代表識，如實話語代表涅槃，往返道路代表八正道。',
  caption: '依《相應部》SN 35.245 的六門城喻改編；島嶼、修整與亮燈是閱讀回饋。',
  stages: ['城池輪廓', '道路與草木顯現', '中央廣場修整', '六門燈火亮起'],
  stageNotes: [
    '淡淡的城池輪廓，等候第一段閱讀旅程。',
    '讀完第一本，道路與草木顯現。接著前往五陰島。',
    '讀完第二本，中央廣場清楚起來。接著前往六處島。',
    '讀完三本，六座城門亮起。第一段旅程完成，後續旅程仍待探索。'
  ],
  gates: ['眼', '耳', '鼻', '舌', '身', '意'],
  plaza: '中央廣場', elements: ['地', '水', '火', '風'], lord: '城主・識',
  guardian: '守門者・念', messengers: '雙使者・止與觀', message: '如實話語・涅槃',
  road: '往返道路・八正道', body: '城池・四大所成的身體',
  prototype: '配置示意，非正式場景原畫', scroll: '小螢幕可左右捲動查看完整配置。',
  progressOnly: '城景只回應已完成的閱讀，不表示證果、斷結或修學全部完成。',
  consciousness: '城主「識」是經中的譬喻，不代表永恆靈魂或不變主宰。'
};
export const CITY_MAPPING = [
  ['城池', '四大所成、受滋養且會變壞的身體'],
  ['六座城門', '六內處：眼、耳、鼻、舌、身、意'],
  ['守門者', '念'], ['一對快速使者', '止與觀'],
  ['中央廣場', '地、水、火、風四大'], ['城主', '識'],
  ['使者傳達的如實話語', '涅槃'], ['往返道路', '八正道']
];
export const CITY_SOURCES = [
  {id:'sn35.245', title:'《相應部》SN 35.245〈像緊叔迦那樣經〉', edition:'莊春江中譯・SuttaCentral資料', url:'https://suttacentral.net/sn35.245/zh/zhuang', verified:'https://raw.githubusercontent.com/suttacentral/sc-data/482faafde8b9c52689d7926004706939f573cf2b/html_text/zh/pli/sutta/sn/sn35/sn35.245.html'},
  {id:'sn35.204', title:'Kimsuka Sutta: The Riddle Tree', edition:'Ṭhānissaro Bhikkhu英譯・Access to Insight，另編號SN 35.204', url:'https://www.accesstoinsight.org/tipitaka/sn/sn35/sn35.204.than.html', verified:'https://raw.githubusercontent.com/alexgenaud/AccessToInsight/9f446378e0b1987d9596ec4cf853fd026442ee0a/tipitaka/sn/sn35/sn35.204.than.html'},
  {id:'sa1175', title:'《雜阿含經》1175經〈緊獸〉', edition:'求那跋陀羅古漢譯・大正藏T02，No.99，315c–316a', url:'https://cbetaonline.dila.edu.tw/zh/T0099_043', verified:'https://raw.githubusercontent.com/suttacentral/sc-data/482faafde8b9c52689d7926004706939f573cf2b/html_text/lzh/sutta/sa/sa1101-1200/sa1175.html'}
];
