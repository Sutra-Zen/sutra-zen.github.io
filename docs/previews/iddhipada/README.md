# 四如意足｜審閱版本

原審閱分支 `feat/iddhipada-review`，[PR #34](https://github.com/rooneyflower-star/sutrazen-map/pull/34)，基準main `140f62221726485916f3992d8ea6f5782e7507b5`。作者已於審閱交付後指示「直接發布吧」，改由本PR發布。實際部署與備份結果見PR最後核對。正式[導讀](https://rooneyflower-star.github.io/sutrazen-map/iddhipada/)與[繪本](https://rooneyflower-star.github.io/sutrazen-map/iddhipada/book/)。以下保留原校稿PDF、截圖與本機試閱方式。

## 先在iPad直接看

- [完整內容校稿PDF](Iddhipada-review.pdf)：9幕原圖及教學字、全部81段口白／時間／P與Q對應、11筆完整經文卡及獨立結語。文字可選取；這是內容校稿版，操作介面請看下列實際截圖或本機互動版。
- [手機畫面](S07-360x800.webp)、[直式導讀](guide-768x1024.webp)、[橫式導讀](guide-1024x768.webp)。

| 核對項目 | iPad橫式1024×768 | iPad直式768×1024 |
| --- | --- | --- |
| 欲定圖內標題 | [S02](S02-1024x768.webp) | [S02](S02-768x1024.webp) |
| 精進定避讓貓臉 | [S03](S03-1024x768.webp) | [S03](S03-768x1024.webp) |
| 心定與下方兩張經文卡 | [S04](S04-1024x768.webp) | [S04](S04-768x1024.webp) |
| 觀定避讓提燈 | [S05](S05-1024x768.webp) | [S05](S05-768x1024.webp) |
| 無字正式四格圖＋四標籤 | [S06](S06-1024x768.webp) | [S06](S06-768x1024.webp) |
| 前後上下等標題避開貓臉 | [S07](S07-1024x768.webp) | [S07](S07-768x1024.webp) |
| 四如意足總覽 | [S08](S08-1024x768.webp) | [S08](S08-768x1024.webp) |
| 抵岸與古漢譯 | [S09](S09-1024x768.webp) | [S09](S09-768x1024.webp) |
| 統一來源卡 | [來源](sources-1024x768.webp) | [來源](sources-768x1024.webp) |

另有[經典依據結語](ending-768x1024.webp)。全部9幕兩方向截圖均在本目錄。

[書架與鎖頭](shelf11-1024x768.webp)、[既有地圖入口](map-entry-1024x768.webp)、[圖片放大視窗](S06-zoom-1024x768.webp)也已核對。

## 開啟互動試閱

下載[審閱分支ZIP](https://github.com/rooneyflower-star/sutrazen-map/archive/refs/heads/feat/iddhipada-review.zip)，解壓縮後，在有首頁 `index.html` 的專案根目錄執行：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

電腦開啟 `http://127.0.0.1:8765/iddhipada/index.html`（導讀）或 `http://127.0.0.1:8765/iddhipada/book/index.html`（繪本）。首頁可檢查第11本書架、其餘3本鎖頭與既有四如意足地圖節點。

iPad測試：電腦與iPad連同一區域網路，命令的bind改成 `0.0.0.0`，iPad Safari開啟 `http://電腦的區域網路IP:8765/iddhipada/index.html`；結束用Ctrl+C。這是本機試閱，不是公開部署。

GitHub的HTML檔案頁只顯示程式碼；沒有宣稱iPad「檔案」快速預覽或雙擊HTML可以執行完整網站。此環境沒有可交付的公開預覽主機，互動版本已透過上述HTTP方式實測。

## 驗收與重建

```sh
python3 docs/iddhipada/scripts/validate.py
python3 scripts/build-iddhipada.py --check
python3 scripts/check-iddhipada.py --screenshots --verify-sources
python3 scripts/build-iddhipada-preview.py
node --check iddhipada/book/book.js
node --check iddhipada/book/book-data.js
```

環境需Python3、Pillow、lxml、Playwright、`/usr/bin/chromium`；PDF建置另用PyMuPDF與Poppler的pdftotext。

9幕、81段原口白、11筆卡、13條疊字、9張原圖及全部原檔雜湊核對。81段各一頁，加一頁獨立結語，共82頁。360×800、800×360、768×1024、1024×768、1440×900共410個頁面狀態，並測65個放大字框狀態。確認完整比例、字幕在上／經文在下、無水平溢出、圖框百分比及cqw、原文／譯意分層、上一頁／下一頁／目錄／經文捲動與視窗／來源往返／放大關閉／旋轉重載保留頁碼／快速按鍵／末頁重讀。首頁書架與地圖入口、十本舊書的開啟／翻頁／返回均檢查；舊書、共用元件及Pages設定與基準main逐檔不變。

[validation.json](validation.json)記錄結果。實體iPad/iPhone Safari原生手勢、外部註解站畫面及YouTube播放未驗收；見[待校稿事項](../../iddhipada/REVIEW_TODO.md)與[位置核對](../../iddhipada/layout-audit.md)。
