# 城池波旬／書架滿版：窄範圍驗證

基準：`a9ee6ae8fda9e1ec01822aa013ad85bcdf551f3a`。本機結果為 [passed](validation.json)，JavaScript 與非預期 HTTP 錯誤皆為 0；正式發布需另核對精確 merge SHA 的 Pages／HTTPS。

```sh
python3 -B scripts/check-game-framing.py
```

本輪是位置與 CSS 修正，**沒有重跑四聖諦 29 步**。所有 0／1／14 本完成數皆為明確標示的獨立歷史測試存檔。實際複習 0–3、重新整理、返回及續讀主線為原生按鈕操作，沒有把測試存檔冒充完成整本。

## 已驗證

- 書架六尺寸：1280×900、360×800、844×390、768×1024、1024×768、2048×1115，各測 0／1／14 本，共 18 組。main、stage 與 case 左右滿寬，無原 max-width、外距、stage padding 或棕色空邊。瀏覽器自身垂直捲軸寬度另列於 geometry。
- 十四張卡保留，未讀是非互動 placeholder；可複習按鈕／封面數恰等於已讀數。實際滾到第十四張：手機橫直式使用 CDP 單指滑動，其他尺寸使用原生滑鼠滾輪。未讀點擊不開書；十四本歷史存檔可原生點開第十四本原閱讀器，再回書架。
- 已完成首冊的末頁書籤從複習第 0 步重新開始，實際翻到第 3 步、重整、返回書架。原主線仍是五陰、書籤 index 8 未變，再從地圖主按鈕確實進入五陰 index 8；完成數仍為 1。
- 城池六尺寸 × 第一冊／全部十四冊，共 12 組：波旬世界座標在城主左上方，沿用朝右的原圖；汗滴 DOM 節點為 0。原生點波旬／右上 X、廣場來源／X、全景與返回均可操作，返回精確恢復 x／y／scale，閱讀 JSON 逐位元不變。
- 自動新增模組通知與「前往城池看看」原生分流保留（明示為已確認尾聲的歷史 fixture smoke，不是新的完成證明）。
- 615 個原站檔案保護，原稿／經文／圖片／操作／首頁 SEO／Google 保留。閱讀、資格、story、receipt、storage schema、備份與原 library 圖保護；只允許 UI 快取 query 的窄例外。遊戲入口產生器與 SEO 檢查通過。

## 實際截圖

- [2048×1115 十四冊滿寬書架](shelf-14-historical-2048x1115.png)
- [2048×1115 滾到末排](shelf-14-last-row-2048x1115.png)
- [桌面空書架](shelf-0-historical-1280x900.png)
- [桌面只完成一本](shelf-1-historical-1280x900.png)
- [手機直式完整已讀書架](shelf-14-historical-360x800.png)
- [手機直式末排](shelf-14-last-row-360x800.png)
- [手機橫式末排](shelf-14-last-row-844x390.png)
- [平板直式](shelf-1-historical-768x1024.png)
- [平板橫式](shelf-14-historical-1024x768.png)
- [真實複習第 3 步返回書架](native-review-first-index3-return-360x800.png)
- [第一冊城池：波旬左上](city-1-overview-1280x900.png)
- [完整城池：波旬左上](city-14-overview-1280x900.png)
- [波旬對話與 X](city-1-mara-dialogue-1280x900.png)
- [手機全景](city-1-overview-360x800.png)

[獨立城池元件報告](independent-city-framing-validation.json) 來自 `camera_controls` 的 `/workspace/artifacts/city-mara-framing/validation.json`，與本整合矩陣分開。

未測 iPhone／iPad **實機 Safari**；本輪為 Chromium 尺寸、滑鼠與 CDP 觸控模擬。未改畫或替換 library／波旬原圖，沒有重新驗收或宣稱讀完全部十四本。
