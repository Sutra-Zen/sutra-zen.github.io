# 序幕與作者重置實測

基準為已發布 main `35d59e3bc41faed5fe7b0d22d1a0797398c6de59`；本目錄記錄本機 Chromium 的實際操作，不能用來推定正式站已發布。歷史進度均為獨立瀏覽器測試資料，不是作者的存檔，也不是實際讀完十三本的紀錄。

完整結果：[validation.json](validation.json)。另附獨立審查者的[儲存失敗回歸紀錄](independent-reset-validation.json)，來源為 `/tmp/game-prologue-reset-independent.json`。

## 通過的檢查

- 1280×900、360×800、844×390、768×1024、1024×768：作者三段六個原稿行逐字一致、HTML 可選取；窄版自然換行。序幕期間選單隱藏且 inert，完成後紙卡置中、SutraZen 在卡內，無頁面溢出。
- 一次真實自然播放，未修改動畫時間或跳到片尾：30 秒動畫正常結束一次，隨後可立即按開始。觸控及 Enter／Space／Escape 略過均不穿透開始按鍵；降低動態偏好顯示可捲動全文，必須手動進選單。
- 一般 `/game/`、`?author=0` 及舊預覽路徑均不產生首頁作者按鍵；`/game/?author=1` 的按鍵在五尺寸可實際點擊，目標高度至少 48px。
- 原生確認取消後 localStorage／sessionStorage 逐值不變；確認重置後，僅遊戲 collection、route、story、相應備援與 camera／tip 清除。舊三本原型、原站讀本資料、其他設定及測試角色鍵值保留。
- 重置後重新播放序幕、選單顯示「開始旅程」，第一幕小貓口白重新出現。經原生口白入口進四聖諦，按兩次下一頁、重整與返回後續讀第 3／29 頁；返回海圖不重播序幕或首次口白，城池沒有殘留獎勵。
- 對 canonical 刪除失敗、session 備援刪除失敗及備援刪除／寫入皆失敗注入實際故障：畫面如實提示無法永久保存。能覆寫備援時重載仍為 fresh；若所有備援操作也被拒絕，舊資料可能在重載後回來，符合畫面警告。另以攔截回傳基準版 store 模擬舊快取，同樣防止 stale recovery 復活。
- 615 個原站保護檔含十四本、首頁、SEO／Google 驗證逐位元不變；原資格、路線、讀本橋接、鏡頭、圖像資料不變。collection store 僅允許必要的 `reset()` 清理區塊變更，抽除此區塊後其餘全文與基準一致。零 JavaScript 錯誤與同源 HTTP 錯誤。

## 實際截圖

| 畫面 | 桌面／平板 | 手機 |
| --- | --- | --- |
| 真實播放中的捲動序幕 | [1280×900，播放約十秒](natural-crawl-1280x900.png) | [靜態全文 360×800](prologue-static-top-360x800.png) |
| 降低動態全文 | [768×1024](prologue-static-top-768x1024.png) | [844×390 下半段，可向上捲回](prologue-static-bottom-844x390.png) |
| 序幕後一般選單 | [1280×900](title-after-prologue-1280x900.png)／[1024×768](title-after-prologue-1024x768.png) | [360×800](title-after-prologue-360x800.png)／[844×390](title-after-prologue-844x390.png) |
| 作者試玩入口 | [重置後新選單](author-reset-fresh-menu-1280x900.png) | [直式](author-trial-menu-360x800.png)／[橫式](author-trial-menu-844x390.png) |
| 重置後第一幕與故障提示 | [重新抵達法輪遺跡](author-reset-first-arrival-1280x900.png) | [無法永久保存的如實提示](author-reset-storage-warning.png) |

## 重現方式與限制

在專案根目錄執行 `python3 -B scripts/check-game-prologue.py`。手動預覽可用 `python3 -m http.server 8778 --bind 127.0.0.1`，開啟 `http://127.0.0.1:8778/game/` 或作者 opt-in 入口 `http://127.0.0.1:8778/game/?author=1`。

瀏覽器為桌面 Chromium 的視窗／觸控模擬；未測實機 Safari。此輪未重跑未變動的十四本 1192 步。自然播放驗證只讓一個視窗實際等候完整片尾，其餘尺寸驗證全文、略過、靜態替代與版面；不宣稱所有尺寸都各自自然播放一次。作者 query 只是暫用 UI 開關，不是帳號認證，也不授予跳關資格。
