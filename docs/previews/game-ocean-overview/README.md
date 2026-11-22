# 外海留白、半島可視區與全圖返回

本機針對性驗證通過；基準為 `53e8eee0db9d2465ea5f584a840649d3c73d0f8d`。本目錄不代表正式站已發布。

根目錄執行 `python3 -m http.server 8000` 後開 <http://localhost:8000/game/>。獨立檢查可重跑 `python3 -B scripts/check-game-ocean-overview.py`。

[UI 驗證報告](validation.json) 與 [相機專項報告](focused-camera-validation.json) 分開記錄實際操作及直接 API 邊界情境：

- 五尺寸均先真實拖曳、放大，再進入全圖；使用明確返回按鈕後，`x`、`y`、`scale` 在 `0.000001` 容差內回到原視角。
- 重複全圖／返回不漂移，全圖中重整、旋轉來回後仍可返回。專項另直接呼叫三次 `fit()`，確認沒有覆寫原視角快照。
- 全圖中完整原圖及八正道半島位於 dock 上方，五尺寸最小間距約 67 CSS px。原生 Tab 走到四橋與驛站時，標牌亦在 dock 上方；標牌中心與原圖座標誤差小於 1px。
- 外海延伸一度造成瀏覽器原生焦點捲動；改用僅限相機容器的 `overflow:clip` 後，全流程 `.wm-viewport.scrollLeft/scrollTop` 始終為零，避免視覺位置偏離相機資料。
- 沒有舊視角快照的 v1 存檔及手動縮小到全圖，都有可用的返回入口，回到目前關卡的正常縮放；沒有捏造歷史視角或修改閱讀進度。
- 提供舊版 unversioned 文案的攔截情境下，實際載入版本化新文案，返回按鈕沒有 `undefined`。
- 原生單指背景／標牌拖曳、雙指縮放、取消、dock 橫滑、翻五步後重整／旋轉／返回續讀、未開放書阻擋及半城入口維持正常。
- 615 個原站內容／原圖／經文／讀本 HTML／首頁／SEO／Google 驗證與建置保護檔未變；遊戲存檔、資格、橋接、地理及來源關係資料、既定首頁文案與封面也未變。沒有重跑未改內容的 29 步或 1192 步。

| 畫面 | 桌機 | 手機直式 | 手機橫式 | 平板直式 | 平板橫式 |
| --- | --- | --- | --- | --- | --- |
| 拖曳／放大後 | [1280×900](explore-before-1280x900.png) | [360×800](explore-before-360x800.png) | [844×390](explore-before-844x390.png) | [768×1024](explore-before-768x1024.png) | [1024×768](explore-before-1024x768.png) |
| 全圖與返回入口 | [1280×900](overview-safe-1280x900.png) | [360×800](overview-safe-360x800.png) | [844×390](overview-safe-844x390.png) | [768×1024](overview-safe-768x1024.png) | [1024×768](overview-safe-1024x768.png) |
| 精確返回原視角 | [1280×900](explore-returned-1280x900.png) | [360×800](explore-returned-360x800.png) | [844×390](explore-returned-844x390.png) | [768×1024](explore-returned-768x1024.png) | [1024×768](explore-returned-1024x768.png) |
| 半島標牌鍵盤定位 | [1280×900](peninsula-keyboard-1280x900.png) | [360×800](peninsula-keyboard-360x800.png) | [844×390](peninsula-keyboard-844x390.png) | [768×1024](peninsula-keyboard-768x1024.png) | [1024×768](peninsula-keyboard-1024x768.png) |

舊 v1 沒有快照的 [返回前](legacy-v1-no-snapshot-before.png)／[返回目前關卡後](legacy-v1-no-snapshot-after.png)，以及手動縮小的 [返回前](manual-zoom-out-before.png)／[返回後](manual-zoom-out-after.png)。這些是隔離鏡頭存檔測試，不會讀取作者的瀏覽器進度。

最終外海取自原圖水域局部，以低對比紋理鋪排，沒有重繪或改動原圖；與原圖的水紋邊界仍可辨。港口半城保留原先半裁設定。功能測試使用桌面 Chromium／CDP，未測實機 iPhone／iPad Safari。
