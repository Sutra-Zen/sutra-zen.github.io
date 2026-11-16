# 安那般那與止觀｜試閱

2026-11-16，原審閱分支 `feat/anapana-review`。作者已於交付後授權直接發布，由PR #28進行。以下保留原試閱與驗收方式；正式發布結果見PR #28最終核對記錄及最新HANDOFF。正式入口為 https://rooneyflower-star.github.io/sutrazen-map/anapana/ 。

## 開啟互動試閱

1. 下載 [審閱分支完整ZIP](https://github.com/rooneyflower-star/sutrazen-map/archive/refs/heads/feat/anapana-review.zip)，解壓縮。
2. 在解壓後的專案根目錄（有 `index.html` 的一層）執行：

   ```sh
   python3 -m http.server 8765 --bind 127.0.0.1
   ```
3. 在瀏覽器開啟 [主題導讀](http://127.0.0.1:8765/anapana/index.html) 或 [互動繪本](http://127.0.0.1:8765/anapana/book/index.html)。首頁 `http://127.0.0.1:8765/` 可檢查第10本書架及原安那般那地圖節點。

iPad實測時，可在同一區域網路的電腦將上述bind改為 `0.0.0.0`，iPad Safari開啟 `http://電腦的區域網路IP:8765/anapana/index.html`。這是本機試閱，不是發布GitHub Pages。關閉伺服器用Ctrl+C。

管理環境的Chromium禁止 `file://` 導覽，因此**沒有宣稱解壓後直接雙擊HTML或iPad「檔案」預覽可執行完整繪本**。互動試閱已實測使用上述HTTP方式。GitHub檔案頁只顯示程式碼，並不是可互動網站；若暫不啟動伺服器，可先直接看下方截圖。

## iPad橫直式截圖

| 核對項目 | 橫式1024×768 | 直式768×1024 |
| --- | --- | --- |
| 五蓋標籤 | [S03](S03-1024x768.webp) | [S03](S03-768x1024.webp) |
| 圖下主題字、圖上字幕 | [S04](S04-1024x768.webp) | [S04](S04-768x1024.webp) |
| 心悅／心定原圖對照 | [S06](S06-1024x768.webp) | [S06](S06-768x1024.webp) |
| 調身三提示、窄圖移到圖外 | [S10](S10-1024x768.webp) | [S10](S10-768x1024.webp) |
| 文字總覽 | [S12](S12-1024x768.webp) | [S12](S12-768x1024.webp) |
| 總覽後段及共同結語 | [末段](S12-end-1024x768.webp) | [末段](S12-end-768x1024.webp) |
| 導讀 | [導讀](guide-1024x768.webp) | [導讀](guide-768x1024.webp) |
| 原經來源卡 | [來源](sources-1024x768.webp) | [來源](sources-768x1024.webp) |
| 論師補充獨立區 | [補充](commentary-1024x768.webp) | [補充](commentary-768x1024.webp) |

另有[手機S10圖外提示](S10-360x800.webp)及[S10放大視窗](S10-zoom-1024x768.webp)。

[書架第10本與其餘鎖頭](shelf-1024x768.webp)也已核對。

全部12幕的兩方向截圖均在本目錄，可直接點開檢查；S01–S11沒有裁圖，S12為可選取文字總覽。

## 可重現驗收

```sh
python3 docs/anapana/scripts/validate.py
python3 scripts/build-anapana.py --check
python3 scripts/check-anapana.py --screenshots --verify-sources
node --check anapana/book/book.js
node --check anapana/book/book-data.js
```

瀏覽器驗收使用Playwright及 `/usr/bin/chromium`，另需Pillow、lxml。`validation.json` 記錄尺寸、逐頁狀態與限制。360×800、800×360、768×1024、1024×768、1440×900各119頁，共595個狀態，逐筆檢查原口白／經文／疊字、完整圖比例、字幕在上經文在下、無水平溢出及按鍵位置。另測翻頁、12幕目錄、本頁經文與捲動、來源往返、返回導讀與地圖、放大關閉、快速點按、旋轉／重載保留頁碼、最後頁重讀、首頁書架／地圖及九本舊書入口。原始38檔及六份原典雜湊核對，舊書／共用元件／Pages設定對照main基準不變。

實體iPad/iPhone Safari的原生手勢、YouTube實際播放及外部註解站畫面尚未驗收；不以Chromium尺寸模擬代替。引文待校事項見 [REVIEW_TODO](../../anapana/REVIEW_TODO.md)，初值座標與分層見 [layout-audit](../../anapana/layout-audit.md)。
