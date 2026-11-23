# 波旬首次出場：疑退場後的遠觀心想

2026-11-23，從已發布main `71de5285bef079f515abcc44577eb50a4aa8cea3` 建立 `feat/game-mara-observer`。開始時工作樹乾淨、origin為 `https://github.com/Sutra-Zen/sutra-zen.github.io.git`。沿用作者已明確授權的遊戲更新發布流程；精確merge SHA／Pages與正式站結果另記本輪PR交付。

## 作者要求與實作

`play/story/data.js`新增`mara`角色與`mara-watches`場景，文字獨立於原書及經典引文：

> 站在遠方觀看的波旬心想：「可惡，小貓好像慢慢開始破除五蓋了……」

順序為小貓的四聖諦心得 → 疑問號減少／退入霧中 → **波旬遠觀心想** → 原法輪碼頭／城池閱讀回饋 → 前往下一站 → 原小貓五陰湖口白 → 原五陰閱讀器。沒有新增完成本數、能力數字、斷蓋判定或額外獎勵；波旬這句是劇情角色的想法。

頭像來自作者本輪森林附圖右上角色：保留灰棕虎斑、兩琥珀棕眼、紫金斗篷、紅橘小角、帽額金色眼罩形裝飾與雙翼，轉向右側以面向右邊的台詞，移除手持橘貓面具。新圖為透明PNG，沒有烙字；耳、角、翼完整，沿用既有矩形contain頭像與淺藍青瓷／深色半透明UI。原繪本不重畫。詳[素材來源與校對](../../../play/story/assets/MARA.md)。

## 中斷、歷史與重看

沿用`story.v1`已看場景與原first-completion receipt，不新增儲存欄位或另一套閱讀進度。為同時保留中斷續看及舊存檔，`doubt-recedes`繼續作為原完成過場的結束標記：

- 新版此幕的`seenOn: outro-end`延後到波旬幕明確結束才寫入；顯示疑退場時不提前結束整段。
- 波旬顯示時正常記錄其scene ID。中斷時若心得已看、舊結束標記尚未寫入，就恢復疑退場；若波旬已看過則直接恢復波旬幕。兩者仍須先有真實四聖諦完成及末頁位置。
- 波旬按「看看旅程的變化」或任一完成過場明確略過，才寫入原結束標記並顯示原閱讀回饋。
- 舊版已有`doubt-recedes`已看紀錄者不自動補插波旬；歷史completed／URL參數也不能單獨觸發。可從工具「重看四聖諦過場」觀看新版，整段replay不寫seen／完成、不重發回饋。
- 作者確認重置沿用共用story store，會清除波旬scene ID；一般入口沒有作者重置。

`play/story/dialogue.js`只增加延後結束標記的條件；`play/worldmap-v4/worldmap.js`負責恢復場景及最後確認，閱讀資格、解鎖、完成／書籤存檔與receipt程式都不改。

## 快取與原站保護

遊戲／城池／書架互返`v=mara-1`，讀本入口`collectionStory=mara-1`；十四本HTML各**只改既有collection bridge script query**，bridge自身也只更新返回遊戲的版本URL。這些參數只管cache，無權限或解鎖意義。新HTML、bootstrap、story data／store與作者重置使用一致module版本，避免返回舊劇情或使用兩個story store實例。

既有淺藍CSS及原書正文／圖片／經文／操作維持；根首頁／心智圖、十五頁SEO、sitemap／robots／Google檔不改。`play/worldmap-v4/index.html`仍為入口產生器來源，`game/index.html`同步。Pages保留legacy `main:/`，只新增QA排除目錄，合計十八個QA目錄。

## 驗證與預覽

實際結果／截圖見[本輪QA](../../previews/game-mara-story/README.md)。實際原生四聖諦29步、波旬頁重整、原回饋、五陰前四步及返回續讀，與隔離歷史／略過／重看／缺圖／作者重置／五尺寸分開記錄；不把fixture當成十四本實讀。Safari實機未測。

根目錄執行`python3 -m http.server 8765 --bind 127.0.0.1`，開啟`http://127.0.0.1:8765/game/?v=mara-1`。作者重頭測試可用`?author=1&v=mara-1`後確認重置；保留進度者可從工具重看四聖諦過場。

精確發布與固定SHA原始碼ZIP交付記在本輪PR；若ZIP只HEAD驗證可下載，不能稱已做CRC。現有工具沒有Notion連接器，待原對話補記波旬圖、此句台詞及本輪發布連結。表情差分／全身動畫與後續波旬劇情尚未實作。
