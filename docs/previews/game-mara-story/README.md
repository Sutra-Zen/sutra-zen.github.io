# 波旬旁觀過場實測

基準 main：`71de5285bef079f515abcc44577eb50a4aa8cea3`。[完整結果與逐步閱讀記錄](validation.json)由 `python3 -B scripts/check-game-mara-story.py` 產生；本目錄記錄本機驗證，正式發布須另核對精確 merge SHA 的 Pages 與實際網址。

## 真實閱讀主流程

原到達／疑入口 → 原四聖諦 index 0–28 的全部原生 Next → 明確「完成這本」→ 小貓 insight → 疑退場 → **波旬** → 原法輪碼頭回饋 → 五陰湖口白 → 原五陰 0、1、2、3。

波旬的 speaker 為「波旬」，完整 HTML 口白逐字核對：

> 站在遠方觀看的波旬心想：「可惡，小貓好像慢慢開始破除五蓋了……」

實際停在波旬頁重新載入，仍恢復同一句波旬，collection 完成集合與位置沒有改寫。波旬已看旗標可以存在，但原 `doubt-recedes` 結束旗標保持 pending；按 CTA 才結束過場並顯示原回饋。進五陰後再重整、轉手機直式及返回，繼續第 4／54 頁，已讀數仍只有第一本。

## 針對性回歸

- 1280×900、360×800、844×390、768×1024、1024×768：獨立 pending profile 恢復波旬；完整矩形 contain、不切角、無圓形遮罩或疑的問號，全文與兩個 48px 以上按鍵都在底列上方，CTA 保持焦點，沒有頁面溢出。淺青主操作與世界插畫原色保留。
- 五尺寸實際按略過，會確認結束旗標並顯示原回饋；重整後不重播、不重新開回饋，也不增加完成冊數。
- 舊版已有 `first-book-insight`／`doubt-recedes` 的已完成紀錄，即使帶 `completed` 網址也不強播新增波旬。透過既有「重看四聖諦過場」才依序重看三段，collection／seen 原始字串不變，不開新書、不發獎勵。
- 作者重置用另一個隔離 pending profile：原生確認取消後 storage 逐值相同；確認會清掉新波旬旗標與 pending，保留原網站、舊原型及其他鍵，重新顯示第一本到達口白。namespace／存檔版本仍為 v1，沒有新增進度欄位或分數。
- 只封鎖波旬圖片的故障注入仍顯示完整口白與按鍵；能繼續原回饋、五陰湖及原五陰 reader，並實際按一次 Next。此案例明列為隔離 fixture，沒有冒稱走完整本。
- 615 原站保護檔中，14 本 HTML 僅 bridge 快取 query 變更，各換回自身基準 query 後全文相同；其餘原文、經文、圖片、reader JS／CSS、首頁／SEO／Google 檔逐位元保留。資格、collection store、receipt、route、prologue、camera、圖譜、淺青主題與既有素材不變。bridge return／story store／reset 的 cache import 僅以精準 query 例外放行。
- 零 JavaScript／同源 HTTP 錯誤。所有歷史、五尺寸 pending、重置及故障資料都是獨立測試 profile，與前述真實 29 步分開標示。

## 最終角色素材

`play/story/assets/mara-portrait-concept.png` 原生 **1254×1254、RGBA**，alpha 範圍 0–255；alpha≥32 的可見範圍為 `[52,67,1178,1177]`，主輪廓沒有貼到畫布邊緣。SHA-256：

`8e8067e3b67ae6037f2e9562b91d9ae14a9d667b92b6d7a2de389ba36d48f63c`

已人工查看原圖及實際手機／橫式／平板畫面：角色朝右，兩個琥珀色眼睛、紅橘雙角、額前金色飾物、雙翼及披風完整，沒有手持面具。這是本輪新角色概念稿，不替換既有繪本原圖；文案是角色心聲，不是經文引文、修學評分或斷結判定。

## 截圖索引

| 畫面 | 截圖 |
| --- | --- |
| 真 29 步後波旬 | [重新載入前](actual-first29-mara-before-reload-844x390.png)／[恢復同一句](actual-first29-mara-restored-844x390.png) |
| 全角色與按鍵（隔離 pending fixture） | [手機直式](mara-pending-isolated-360x800.png)／[手機橫式](mara-pending-isolated-844x390.png)／[平板直式](mara-pending-isolated-768x1024.png)／[平板橫式](mara-pending-isolated-1024x768.png)／[桌面](mara-pending-isolated-1280x900.png) |
| 確認後的原閱讀回饋 | [法輪碼頭](actual-first29-original-reward-844x390.png) |
| 五陰實際閱讀與返回續讀 | [第 4／54 頁](actual-five-resume-360x800.png) |

## 預覽與限制

根目錄啟動 `python3 -m http.server 8780 --bind 127.0.0.1`。一般入口：`http://127.0.0.1:8780/game/?v=mara-1`；作者試玩：`http://127.0.0.1:8780/game/?author=1&v=mara-1`。

驗證為桌面 Chromium 的尺寸及輸入模擬，未測實機 iPhone／iPad Safari。未重跑未變動的十四本 1192 步；本輪完整原生閱讀只計第一本 29 步及五陰前四步，其他案例明確標為 fixture。既有序幕、三分頁與閱讀資格維持原樣。
