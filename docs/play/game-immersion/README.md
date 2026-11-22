> 後續海圖全視窗／單列半透明工具列與觸控移交修正見 [最新交接](../game-fullscreen-dock/README.md)。以下保留本輪依序資格、封面原件及首次沉浸殼的歷史驗證。

# 小貓的山海旅程：沉浸介面與依序閱讀

2026-11-22。實作分支 `feat/game-immersion-sequential`，基準為首次遊戲發布 PR60 的 `7e39f04a383ab98d3b747365ea3e513ad7140a0e`；開始及提交前均確認 origin/main，保留既有歷史。沿用作者先前對 `/game/` 的發布授權，經新 PR 進 main。實際 merge SHA、Pages 成功與正式站檢查記於該 PR 交付留言，不以分支存在推定已部署。

## 操作與畫面

- 標題採 SutraZen／小貓的山海旅程／佛法繪本探索遊戲。封面使用作者後補 ZIP 的原始 JPEG；所有標題、按鈕及標牌仍為可替換的網頁文字。開始／繼續後進地圖，閱讀器、城池、書架的返回網址帶明確目的地，不反覆播放標題。
- 地圖、城池、書架共用 `play/game-shell.js/css`：全視窗內容、進度／設定 HUD、安全區與底部「地圖／城池／書架」。心智圖、原網站、來源、備份／還原／確認清除及選用全螢幕收進設定。原繪本不載入此殼，保留上方口白、完整插畫、下方原經與既有按鍵。
- 海圖保留 1600×900 世界、32 地標、46 筆原圖來源關係及既定海岸道路。背景、霧、連線、地標、標牌與可點區共用同一世界變換；新增港口附近城池入口，與底部城池分頁開同頁，不新增經典關係邊。
- `camera.js` 支援拖曳、雙指縮放、＋／－、全圖、目前關卡、邊界限制及拖曳防誤開。鏡頭以世界中心／比例保存於 `sutrazen.play.camera.v1` 的 sessionStorage；切頁、重整、旋轉保留。標牌隨縮放補償可讀大小，全圖改用地理區域定位入口。手勢處理只套地圖，不禁止全站縮放。
- 主入口唯一標示「新關卡」或「閱讀中」，已讀標示不混為新關。完成面板顯示本次亮起的地景、城池部件及 14 本分母；「前往下一站」先回海圖定位，玩家再自行開始閱讀。「看看城池」為次要操作。
- 城池保留 SN35.245 六門版及漢巴平行對讀。寬版、窄版、彈窗均完整使用「念-守門人」，引線指燈籠角色；「如實消息・涅槃」仍指雙使者卷軸。城主鬍鬚與原場景圖層未重畫。書架只列已讀書的複習按鈕，未讀封面不提供開始入口；空書架引導第一站。

## 單一資格規則與保存

`play/route/eligibility.js` 是不依賴儲存的共用判定。主線順序不改 r3：四聖諦、五陰、六處、十二因緣、八正道與十善業道、四不壞淨與六念、四念處與四顛倒、四正勤、安那般那與止觀、四如意足、四禪、五根五力、七覺支、四向四果與十結。

只有第一本尚未完成者可開始／新完成，已完成者可複習。規則同時套用海圖、主按鈕、路線、書架、城池、舊 collection URL、橋接恢復、位置及完成寫入，沒有遊戲自由選讀／一鍵全開。原網站不帶 `collection=1` 的十四本仍公開閱讀，不寫遊戲紀錄。

`sutrazen.play.collection.v1` 的合法歷史 completed IDs、positions 及 activeBook 保留；不把非依序歷史完成取消，也不補造前置完成。未來書的舊書籤保留，但不能解鎖或搶走主線續讀。終章須前十三本完成才揭曉；歷史已完成終章仍保留可複習。

只在末個閱讀步驟按「完成這本」時寫入；store 再確認資格及末頁位置，重複完成不寫入／不發獎。複習保存自己的位置，未改主線 activeBook；末頁書籤從頭重讀，部分書籤接原位置。複習結束回書架，沒有新完成回饋。普通開書、選章、返回、重整、抵達末頁都不計完成。

本機儲存失敗會顯示說明，並以同頁籤 `sutrazen.play.collection.session.v1` 延續；記錄失敗時 canonical 原值，僅原值不變時使用，不與外部還原的紀錄合併。localStorage 成功後移除備援。兩種儲存皆禁用時只保留當頁記憶，不假稱可跨頁保存。清除只處理遊戲自己的鍵，無 `localStorage.clear()`。

歷史美術比較頁與 `/play/city/inspection.html` 改為獨立、無儲存讀寫的審稿展示。玩家城池不接受 `?review=all` 變成全開狀態，也不放審稿切換；審稿頁沒有遊戲閱讀／完成操作。

## 封面、產生來源與範圍

原封 ZIP 與指示原稿保留於 [handoff/](handoff/)。原圖從 `0封面.jpeg` 複製成指定 runtime 名稱 `play/assets/CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg`，沒有重生或重新編碼。原生 2752×1536、1,561,826 bytes，SHA-256 `fc7cb28c894890127a20fd1bb898d2448950d51be86c3b36200faa6c2ae523e9`；[匯入紀錄](title-asset.json) 含 ZIP SHA 與逐位元核對。背景貓群為裝飾，旅人仍用既有金袍橘虎斑划船圖；本輪沒有新增角色原畫。

`play/worldmap-v4/index.html` 為共用來源，`scripts/build-game-entry.py` 產生 `/game/index.html`，以根路徑匯入共用模組，不再依賴 `<base>`。文案分於 `game-ui-text.js`、worldmap/text.js、city/text.js、shelf-copy.js，故事及經文仍讀原閱讀器；其他語系只保留結構，未宣稱全書已翻譯。

本輪 615 個原站受保護檔案對基準逐位元未改：十四本 HTML／圖文／經文／來源、根首頁／心智圖、SEO／sitemap／robots／Google 驗證及共用閱讀操作。未新增首頁遊戲推廣、帳號、service worker、原生 App 或新代管。Pages 維持 main 根目錄；`_config.yml` 只再排除本輪 QA 證據，共十個遊戲 QA 目錄，原始碼及 GitHub 截圖仍保留。

## 檢查、預覽與限制

在專案根目錄啟動 `python3 -m http.server 8765 --bind 127.0.0.1`，開 <http://127.0.0.1:8765/game/>。測試使用獨立瀏覽器資料，不更改作者存檔。

```sh
python3 -B scripts/build-game-entry.py --check
python3 -B scripts/build-seo.py --check
node play/route/check-eligibility.mjs
node play/route/check-eligibility-recovery.mjs
node play/route/check-route.mjs
python3 -B scripts/check-game-reader-policy.py
python3 -B scripts/check-game-immersion.py
```

[實際報告與五尺寸截圖](../../previews/game-immersion/README.md) 記錄：原生 29 步四聖諦完成／複習、中途重整與續讀、所有入口禁止越關、合法亂序歷史與未來書籤、6 組複習位置、設定／錯誤儲存、地圖世界座標與鼠控／CDP 雙指手勢、跨頁鏡頭、原站保護雜湊及零 JS／本機 HTTP 錯誤。純模型另覆蓋 16,384 個完成子集。未改的十四本 1192 步原稿仍沿用前輪完整驗證，沒有把舊自由選章測試當成現行規則。

尺寸為 1280×900、360×800、844×390、768×1024、1024×768。這是桌面 Chromium 模擬，**未驗證實機 iPhone／iPad Safari 手勢與效能**。既有場景仍非完整獨立人物／建物動畫層，完整終章演出及其他語系待後續；閱讀完成只代表閱讀紀錄。正式站驗收完成後，精確 merge SHA、Pages run、固定 SHA 原始碼 ZIP 及未完成項補於 PR 交付紀錄。Notion 工具不可用，見 [待補筆記](PENDING_NOTION.md)。
