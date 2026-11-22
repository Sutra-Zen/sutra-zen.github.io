// These positions are calibrated to the generated concept artwork, not canonical geography.
export const ISLANDS = [
 { n:1,id:'four-truths',title:'四聖諦',x:18,y:66,feature:'花林中的法輪，是第一座島的地標。',relation:'四聖諦總說，並連到苦、集、滅、道相關主題。'},
 { n:2,id:'five-aggregates',title:'五陰',x:55,y:73,feature:'林木、泉水、花園、田地與山石，交織成一座相互依存的島。',relation:'從四聖諦「苦」的對讀延伸到五陰。'},
 { n:3,id:'six-senses',title:'六處',x:83,y:53,feature:'六個觀察入口朝向不同景色，旁邊有等待旅人的碼頭。',relation:'與五陰同屬「苦」的對讀，認識眼、耳、鼻、舌、身、意。'},
 { n:4,id:'twelve-links',title:'十二因緣',x:93,y:32,relation:'四聖諦「集」的相關主題。'},
 { n:5,id:'eightfold-path',title:'八正道與十善業道',x:79,y:13,relation:'四聖諦「道」，與勤、定、慧等修道主題對讀。'},
 { n:6,id:'four-fruits-ten-fetters',title:'四向四果與十結',x:63,y:10,relation:'四聖諦「滅」的相關主題。'},
 { n:7,id:'four-purities-six-recollections',title:'四不壞淨與六念',x:8,y:26,relation:'信的主題群。'},
 { n:8,id:'mindfulness',title:'四念處與四顛倒',x:21,y:34,relation:'念的主題群。'},
 { n:9,id:'right-effort',title:'四正勤',x:7,y:40,relation:'勤的主題群。'},
 { n:10,id:'anapana',title:'安那般那與止觀',x:92,y:20,relation:'定的主題群，與四如意足、四禪對讀。'},
 { n:11,id:'iddhipada',title:'四如意足',x:75,y:28,relation:'定的主題群。'},
 { n:12,id:'four-jhanas',title:'四禪',x:20,y:14,relation:'定的主題群。'},
 { n:13,id:'five-roots-powers',title:'五根五力',x:49,y:10,relation:'五根五力總說，連到信、念、勤、定、慧的主題。'},
 { n:14,id:'seven-factors',title:'七覺支',x:35,y:12,relation:'七覺支總說，與念、勤、定、慧相關主題對讀。'}
];
export const RELATIONS = [[1,2],[1,3],[1,4],[1,5],[1,6],[13,7],[13,8],[13,9],[13,10],[13,1],[10,11],[10,12],[14,8],[14,9],[14,12],[14,5]];
export const CITY_SPOTS = [
 {id:'eye',title:'眼門',x:50,y:18,copy:'六座城門對應六內處；這一門表示眼內處。'},
 {id:'ear',title:'耳門',x:77,y:32,copy:'六座城門對應六內處；這一門表示耳內處。'},
 {id:'nose',title:'鼻門',x:78,y:60,copy:'六座城門對應六內處；這一門表示鼻內處。'},
 {id:'tongue',title:'舌門',x:50,y:78,copy:'六座城門對應六內處；這一門表示舌內處。'},
 {id:'body',title:'身門',x:23,y:59,copy:'六座城門對應六內處；這一門表示身內處。'},
 {id:'mind',title:'意門',x:23,y:30,copy:'六座城門對應六內處；這一門表示意內處。'},
 {id:'guardian',title:'守門者・念',x:30,y:59,copy:'守門人譬喻念。旅人小貓與守門人是不同角色。'},
 {id:'messengers',title:'雙使者・止與觀',x:67,y:47,copy:'一對快速使者譬喻止與觀。漢譯1175經「正觀」及校讀在原經對讀另列。'},
 {id:'plaza',title:'中央廣場・四大',x:49,y:48,copy:'中央廣場對應地、水、火、風四大。畫面的材質、泉水、爐火與風中草木是美術演繹。'},
 {id:'lord',title:'城主・識',x:51,y:32,copy:'城主譬喻識，不代表永恆靈魂或不變主宰。'},
 {id:'message',title:'如實話語・涅槃',x:68,y:54,copy:'使者傳達的如實話語譬喻涅槃，不把它改成四聖諦或可蒐集的獎盃。'},
 {id:'road',title:'往返道路・八正道',x:50,y:90,copy:'來時與往返的道路譬喻八正道。道路亮起在遊戲中只作閱讀回饋。'},
 {id:'town',title:'城池・身體',x:50,y:8,copy:'城池譬喻四大所成、受滋養且會變壞的身體。場景的地理位置與造型是教學設計。'}
];
export const COPY = {
 mapTitle:'一張海圖，十四個相遇',cityTitle:'走進六門城池',celebrateTitle:'帶著讀過的故事，回到城池',
 descriptions:{map:'點選島上的小圖，再決定從哪本繪本出發。這一段旅程先走四聖諦、五陰與六處。',city:'沿著石徑探索。點選門樓、人物或廣場，才展開它的法義。',celebrate:'小貓回到熟悉的碼頭，發現城池正悄悄改變。'},
 feedback:['遠處的城池，正等著我們。','岸邊的小徑亮了，下一座島正在等你。','泉水與草木更鮮明了，帶著故事繼續前行。','六門燈火亮起。第一段旅程完成，世界還很遼闊。']
};
