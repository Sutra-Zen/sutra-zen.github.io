# 原圖邊界、完整全圖與城池徽章驗證

本機驗證通過，基準為 `0971b459e5c1eab99460ba4ad3cdb75ec6ce2685`；此處不代表正式站已發布。

根目錄啟動 `python3 -m http.server 8000` 後開 <http://localhost:8000/game/>；完整針對性檢查為 `python3 -B scripts/check-game-original-frame.py`。

[UI 報告](validation.json)／[相機專項報告](focused-camera-validation.json) 證實：

- 五尺寸原生觸控拖到左、右、上、下四個極限，原圖均覆蓋 dock 上方的全部視窗，沒有露出外接海色。一般模式縮小及雙指縮小均停在 cover 下限。
- 全圖依原本 1600×900 完整適配可讀區，沒有外海留白造成額外縮小；必要留白採深色底。明確返回、全圖重整及旋轉來回後可精確返回有效原視角。
- 舊低縮放鏡頭及含外海位置的舊返回快照安全限制在原圖內，閱讀存檔原樣保留。
- 沒有外海 SVG／請求、圖片 alpha mask 或半城圖片；港口為 HTML／SVG 導覽徽章。實際五尺寸均約 98.83×52 CSS px，360px 全圖亦完整可見。一般視圖及全圖的原生點選均能進入城池，沒有增加完成本數。
- 真實翻兩步、重整、旋轉、返回後續讀第 3／29 步；未開放四禪的直接遊戲網址仍受限制。0 JavaScript／本機 HTTP 錯誤。
- 615 個原站保護檔及遊戲存檔／資格／橋接／32 地標與 46 來源關係、首頁文案與原封面未變。沒有重跑未改內容的 29 步或 1192 步。

| 畫面 | 桌機 | 手機直式 | 手機橫式 | 平板直式 | 平板橫式 |
| --- | --- | --- | --- | --- | --- |
| 一般原圖視野 | [1280×900](original-explore-1280x900.png) | [360×800](original-explore-360x800.png) | [844×390](original-explore-844x390.png) | [768×1024](original-explore-768x1024.png) | [1024×768](original-explore-1024x768.png) |
| 完整全圖／城池徽章 | [1280×900](original-overview-1280x900.png) | [360×800](original-overview-360x800.png) | [844×390](original-overview-844x390.png) | [768×1024](original-overview-768x1024.png) | [1024×768](original-overview-1024x768.png) |
| 返回原視角 | [1280×900](original-returned-1280x900.png) | [360×800](original-returned-360x800.png) | [844×390](original-returned-844x390.png) | [768×1024](original-returned-768x1024.png) | [1024×768](original-returned-1024x768.png) |
| 最左邊界／一般城池入口 | [1280×900](edge-left-1280x900.png) | [360×800](edge-left-360x800.png) | [844×390](edge-left-844x390.png) | [768×1024](edge-left-768x1024.png) | [1024×768](edge-left-1024x768.png) |
| 最右邊界 | [1280×900](edge-right-1280x900.png) | [360×800](edge-right-360x800.png) | [844×390](edge-right-844x390.png) | [768×1024](edge-right-768x1024.png) | [1024×768](edge-right-1024x768.png) |
| 最上邊界 | [1280×900](edge-top-1280x900.png) | [360×800](edge-top-360x800.png) | [844×390](edge-top-844x390.png) | [768×1024](edge-top-768x1024.png) | [1024×768](edge-top-1024x768.png) |
| 最下邊界 | [1280×900](edge-bottom-1280x900.png) | [360×800](edge-bottom-360x800.png) | [844×390](edge-bottom-844x390.png) | [768×1024](edge-bottom-768x1024.png) | [1024×768](edge-bottom-1024x768.png) |

另有 [舊低縮放安全恢復](legacy-v1-low-scale-safe.png) 與 [舊外海返回快照安全恢復](old-padded-return-safe.png)。這些使用隔離測試存檔，不觸碰作者瀏覽器。

操作為桌面 Chromium／CDP 模擬；未測實機 iPhone／iPad Safari。
