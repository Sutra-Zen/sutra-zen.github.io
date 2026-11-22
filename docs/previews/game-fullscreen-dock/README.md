# 全幅海圖與單列底部控制列：實際驗證

本輪證據以 `ab311d9a2e030cf7e608e3bd9bc83a006445532e` 為基準，使用隔離 Chromium 瀏覽器。本目錄是本機驗證，不能用來推定已發布。

從 repository 根目錄啟動 `python3 -m http.server 8000`，開啟 <http://localhost:8000/game/>；完整針對性檢查為 `python3 -B scripts/check-game-fullscreen-dock.py`。

[驗證報告](validation.json) 記錄：

- 五尺寸的 `.wm-viewport` 及 `#game-content` 均從 `(0, 0)` 延伸到完整視窗，沒有預留頂部或底部網頁橫帶，也沒有外頁溢出。
- 桌機控制同列；手機同一列可內部橫滑，有左右箭頭。導航、閱讀主按鈕、進度、目前關卡、全圖、放大／縮小、工具、設定都在同一個半透明 dock。
- 每個 dock 操作可聚焦並捲入可見區；工具原生彈窗位於 dock 上方，不受橫捲容器裁切。鍵盤 Enter／Escape 與關閉後焦點還原正常。
- 原生 Tab 走過 32 個地標及港口城池入口，鏡頭會讓鍵盤焦點出現在 dock 上方；滑鼠點選與關閉彈窗則不額外移動鏡頭。
- Chromium CDP 模擬單指拖動背景、從標牌開始拖動、取消及雙指縮放，均未誤開讀本；dock 的橫滑只捲動控制列，沒有拖動地圖。
- 原生按鍵翻到第六個閱讀步驟，重整、旋轉、返回海圖及主按鈕續讀保留位置。讀本沒有覆蓋經文的遊戲 dock，本數仍為零；未開放四禪的直接遊戲網址仍受限制。
- 全圖中的港口半城入口可原生點入城池，沒有額外計數或改動閱讀進度。
- 615 個原網站內容／圖片／經文／讀本 HTML／首頁／SEO／Google 驗證與相關建置檔逐位元未改，遊戲儲存、資格、讀本橋接及地圖資料也未改。

| 畫面 | 桌機 | 手機直式 | 手機橫式 | 平板直式 | 平板橫式 |
| --- | --- | --- | --- | --- | --- |
| 置中開始畫面 | [1280×900](title-centered-1280x900.png) | [360×800](title-centered-360x800.png) | [844×390](title-centered-844x390.png) | [768×1024](title-centered-768x1024.png) | [1024×768](title-centered-1024x768.png) |
| 初始海圖與控制列 | [1280×900](map-initial-dock-1280x900.png) | [360×800](map-initial-dock-360x800.png) | [844×390](map-initial-dock-844x390.png) | [768×1024](map-initial-dock-768x1024.png) | [1024×768](map-initial-dock-1024x768.png) |
| 主要按鈕聚焦 | [1280×900](map-dock-1280x900.png) | [360×800](map-dock-360x800.png) | [844×390](map-dock-844x390.png) | [768×1024](map-dock-768x1024.png) | [1024×768](map-dock-1024x768.png) |
| 工具向上展開 | [1280×900](tools-up-1280x900.png) | [360×800](tools-up-360x800.png) | [844×390](tools-up-844x390.png) | [768×1024](tools-up-768x1024.png) | [1024×768](tools-up-1024x768.png) |

[全圖、港口半城與第六步續讀](map-overview-harbor-844x390.png)。全圖時因保留完整 16:9 世界，超寬視窗可出現藍色側邊；互動地圖容器仍覆蓋完整視窗。

[鍵盤定位鏡頭外地標](keyboard-landmark-focus-1280x900.png)。

這次沒有重新走未改內容的 1192 步或首本 29 步。完整原稿及依序資格的前輪報告保持原樣。本輪為桌面 Chromium 模擬，未宣稱實測 iPhone／iPad Safari；仍需作者在實機確認拖曳與橫滑的手感。

[實際地圖拖到港口後的半座城池](harbor-half-castle-1024x768.png)；[標題置中／短橫式與安全區](title-centering.json)、[單指接管專項](single-finger.json)、[觸控後點選時間矩陣](touch-tap-matrix.json)。時間矩陣區分瀏覽器是否產生原生 click；Chromium 減少動畫模式下，拖完僅30ms就再次觸碰可能不發出相容 click，300ms正常。沒有加自動代點擊或把模擬結果稱為實機 Safari。
