# 模組化城池：透明彩繪素材與座標

> 2026-11-26 波旬更新：目前 `mara` sprite 改用 `assets/mara-masked-fullbody.png`，保留紫色戲面具、斗篷、蝙蝠翅膀及完整漂浮雙腳；揭面後 PNG 只作預留。下列原概念稿描述與生成來源保留為歷史紀錄。現行 metadata 已同步 `art.js`／`generated-provenance.json`，詳 [新素材來源](../../../docs/play/mara-mask/asset-provenance.json)。

2026-11-23。這批素材是以既有角色、城池與繪本為依據製作的遊戲概念美術；不是經典插圖的史實復原，也不把閱讀完成當作修證。新圖的標牌、對話、書名、經號與操作符號一律由網頁呈現。

## 實際檔案與程式契約

`art.js` 匯出 `ground`、`sprites`、`ART_MANIFEST`、`WORLD_SIZE` 與 `CITY_MODULE_ART`。世界座標為 1600×900；底圖原生 1672×941，比例相容。

```js
ground = {url, src, width, height, sha256, ...};
sprites[key] = {
  url, src, x, y, w, h, atlasWidth, atlasHeight,
  cellRect, alpha32Bounds, sourceSHA256, ...
};
CITY_MODULE_ART = {ground, sprites, ...sprites};
```

`x/y/w/h` 是來源 PNG 的像素座標，左上原點，供 SVG `viewBox` 使用。每個物件依格內 Alpha≥32 的主要輪廓加 8px 邊距，限制在原格內；這是**顯示座標**，沒有裁切或改寫 PNG。`cellRect` 保留原分格範圍。最外圈可能有透明度很低的水彩細粒；透明像素的底 RGB 可能呈棕色，不能將 RGB 預覽誤認為不透明背景。

| 檔案 | 原生尺寸／分格 | 用途 |
|---|---|---|
| `assets/ground-concept.png` | 1672×941，RGB | 留空草地、外緣花草與岸水；沒有既有整城、人物或道路烙在底圖。 |
| `assets/gates-atlas-concept.png` | 1536×1024，3×2 | 六個完整門樓，各格512×512。 |
| `assets/buildings-atlas-concept.png` | 1536×1024，4×3 | 十二種地基／章節物件；列界 y=0、341、683、1024。 |
| `assets/cast-atlas-concept.png` | 1536×1024，3×2 | 城主、念守門人、黑白使、三花使、獨立開卷、雙使合組。 |
| `assets/jhanas-atlas-concept.png` | 1254×1254，2×2 | 四個既有四禪譬喻的小景。 |
| `assets/hindrances-atlas-concept.png` | 1254×1254，2×2 | 貪欲、瞋恚、昏沉、掉悔四位角色。 |
| `assets/companions-atlas-concept.png` | 1536×1024，3×2 | 貓頭鷹、兔、藍鳥、龜、蓮花、鹿；不新增第二位念貓。 |
| `assets/mara-fullbody-concept.png` | 1024×1536，RGBA | 依既有波旬肖像延伸的完整浮空身體、斗篷下擺與雙腳；原肖像不變。 |

所有新 PNG 均由 `image_gen.imagegen` 生成／編輯，透明 atlas 指定 `transparent_background:true`；生成原件保留於 `/workspace/generated_images/`，以 `copyfile` 逐位元複製入倉庫。未使用 Python、SVG 或 CSS 重繪像素、去背、補畫、裁圖、重新編碼；PIL 僅讀取尺寸、透明度、分格邊界與輪廓資料。新 atlas 分格界線最大 Alpha 為 3/255，沒有角色主要輪廓跨到相鄰格。

精確原件位置、原生尺寸、檔案 bytes、SHA-256、透明度與45個主要 sprite 的座標見 `assets/generated-provenance.json`。五蓋與夥伴另有各自完整生成提示及校正紀錄：`assets/hindrances-atlas-concept.provenance.json`、`assets/companions-atlas-concept.provenance.json`。

## 十四組獎勵與素材

| 閱讀關卡 | 主要美術 key／可分件 |
|---|---|
| 四聖諦 | `truth_dock`：沿用獨立法輪碼頭 PNG；免費初始四大花園 `base_garden` 與識城主 `city_lord` 不冒充已讀五陰。 |
| 五陰 | `city_outline` 低城界＋`aggregates_corner` 日常觀察角。 |
| 六處 | `gate_n/ne/se/s/sw/nw`，六門作固定插槽；不是六棟任意旋轉的相同平面圖示。 |
| 十二因緣 | `conditions_wheel` 城側輪庭，中央四大花園不變。 |
| 八正道與十善業道 | `noble_path` 道路與空白路石；文字由 HTML 提供。 |
| 四不壞淨與六念 | `confidence_harbor` 六燈小亭。 |
| 四念處與四顛倒 | `mindfulness_guard` 同一位持燈貓；另有 `guard_post` 值守台。 |
| 四正勤 | `effort_garden` 四種照料狀態的花床。 |
| 安那般那與止觀 | `calm_messenger`、`insight_messenger`、`messenger_pair`、`scroll`、`bamboo`；`messengers` 為兩使合組加卷軸附件。 |
| 四如意足 | `endeavor_boat` 空舟，沒有把旅人烙在船上。 |
| 四禪 | `jhana_bath/spring/lotus/cloth` 四個完整小景；`jhana_garden` 為四景總覽。 |
| 五根五力 | `faculties_links` 五色花／根裝飾，實際連動仍呼應既有區域；不複製念或另蓋定力建築。 |
| 七覺支 | `companion_owl/rabbit/bird/turtle/lotus/deer` 六位既有夥伴；念由既有 `mindfulness_guard` 延續。 |
| 四向四果與十結 | `fruition_guide` 河岸回望平台、白花與鬆開繩意象；不表示玩家已得果。 |

`messengers.attachments` 宣告獨立 `scroll` 的相對位置百分比。場景若另放可點卷軸，應關閉合組內的預設附件，避免出現兩張卷軸。雙使、卷軸、守門人與城主各有真實透明彩繪來源，不以幾何占位符替代。

`city_lord.attachments` 沿用既有 `city-lord-facial-hair-layer.png` 的真實透明毛髮圖，key 為 `lord_facial_hair`。位置相對城主 viewBox 為左22.4%、上39%、寬70.3%、高36.8%，覆蓋新 cast 稿鬍間剩下的小口部；已實際以網頁 SVG 合成檢查，鼻、雙眼、皇冠與耳朵保留，沒有以幾何圖形補畫。新 cast PNG 與既有毛髮 PNG 都未改動。

SVG 引用 atlas 時，來源 image 必須裁切在自己的 viewBox 範圍內，包含 nested attachments；單靠 `preserveAspectRatio="meet"` 會在長寬比不同的容器中洩漏鄰格。這是顯示層裁切，與修改來源 PNG 不同。

NPC keys 為 `mara`、`hindrance_desire`、`hindrance_anger`、`hindrance_sloth`、`hindrance_restlessness`、`hindrance_doubt`；`lord`、`guardian`、`hindrance_ill_will` 等是相同 sprite 的程式別名，不是新增人物。

## 生成依據與提示重點

1. **共用城池／角色風格來源**：先檢視 `play/visual-v2/assets/city-scroll-audience-concept.png`。草地底圖要求移除全部建築、城門、人物、道路及廣場，只保留明亮草地、邊緣植被與水岸，為獨立模組留空。六門要求3×2等格，保留橘瓦、淺石與固定俯視戰棋相機，畫出不同方向的門樓；無人物、標牌或文字。
2. **建設 atlas**：4×3依序為四大花園、低六角城界、日常觀察角、緣起輪庭、八路石道路、六燈亭、值守台、四正勤四花床、竹林溪流、空舟、五色根花、河岸回望台。各件保持局部地基、透明間距，沒有完整城景矩形背景，沒有大型宮殿取代每本獎勵。
3. **城中 cast**：以同一城圖編輯取得完整城主、念、黑白／三花使、獨立空白卷軸及兩使合組；保留暖棕眼、既有衣裝與毛色，不新增異色眼、角或面具。小皇冠、八字鬍與山羊鬍保留；角色全身、耳冠與腳完整。新稿不是原城圖的逐像素機械裁切，角色一致性仍由作者檢查。
4. **四禪小景**：先檢視 `four-jhanas/assets/S10.webp`，依木盆澡粉、湧泉、蓮池、白布覆身四個既有譬喻編輯為獨立小景，移除原圖表格與全部字牌；不是經典逐字內容或修行效果保證。
5. **五蓋**：以 `anapana/assets/S03.webp` 與 `four-jhanas/assets/S05.webp` 為角色來源；疑直接沿用已獨立透明 PNG，不重生第五隻。
6. **七覺支**：以 `seven-factors/assets/12.webp` 的六位既有夥伴為來源，保留衣物／道具與外觀，去除原標籤及中心念貓。第一版鹿耳跨格未使用；第二版縮入各格後才交付。
7. **既有獨立圖**：法輪碼頭及 `doubt-creature-concept.png` 沿用原件與原來源紀錄。波旬以 `play/story/assets/mara-portrait-concept.png` 為身份參考，用 imagegen 延伸為新檔 `mara-fullbody-concept.png`，保留棕琥珀雙眼、紅橘角、金色眼罩造型額飾與紫金披風，補完整下擺、兩空手及兩垂腳；沒有手持橘貓面具。原肖像逐位元保護，仍供原有對話使用；新圖不是將胸像改名為全身。完整提示與來源雜湊見 `assets/mara-fullbody-concept.provenance.json`。

## 美術限制與法義界線

- 這是第一版模組組裝稿。六門的前後角度、城界接縫與小景比例須在實際固定插槽中校位；不是可在任何位置無縫拼接的通用建築瓦片套件。
- 角色為完整靜態 sprites，可用少量位移、浮動、暖光及獨立汗滴演出；尚無正式走路／轉身／開門動畫幀，不能宣稱完成逐幀角色動畫。
- 四大花園、六門、念、識、止觀雙使與道路的法義標示依 SN35.245 主城骨架；法輪碼頭、花園、小舟、七夥伴等為繪本遊戲延伸。漢譯《雜阿含》1175 的四門／四守門者只作平行對讀，不混成此六門城的配置。
- 全部文字與互動熱區在 HTML／SVG 文字層，原生 PNG 沒有新增中文標牌。換介面語言不等於已翻譯原有十四本繪本。
