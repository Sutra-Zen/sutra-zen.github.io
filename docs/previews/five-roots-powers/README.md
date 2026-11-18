# 五根五力｜完整試閱與驗收

[草稿PR #41](https://github.com/rooneyflower-star/sutrazen-map/pull/41)，分支：`feat/five-roots-powers-review`，基準main：`2376c9cafb4b59e5eeba6aaa2833ec3c900497fc`。新書先供作者審閱，尚未合併或部署正式站；同輪安那般那止觀四式的更新已另外透過PR #40發布。

## 在iPad直接看

[22頁完整試閱PDF](Five-Roots-Powers-review.pdf)含十幕全圖、五組黑字、全部74段原口白及起訖時間、14張完整引文、片尾來源圖與既有經典依據結語。文字可選取，PDF內容逐字核對通過。PDF用於內容校稿；互動操作另見以下實際截圖與測試。

| 檢查項目 | iPad直式768×1024 | iPad橫式1024×768 |
| --- | --- | --- |
| S01晴天無牌中央島 | [直式](S01-page1-768x1024.webp) | [橫式](S01-page1-1024x768.webp) |
| S02樹根譬喻 | [直式](S02-page13-768x1024.webp) | [橫式](S02-page13-1024x768.webp) |
| S03原圖五牌，不重複疊字 | [直式](S03-page19-768x1024.webp) | [橫式](S03-page19-1024x768.webp) |
| S04信，x60/y46 | [直式](S04-page28-768x1024.webp) | [橫式](S04-page28-1024x768.webp) |
| S05精進，x73/y11 | [直式](S05-page34-768x1024.webp) | [橫式](S05-page34-1024x768.webp) |
| S06念，x77/y11 | [直式](S06-page41-768x1024.webp) | [橫式](S06-page41-1024x768.webp) |
| S07定，x77/y11 | [直式](S07-page49-768x1024.webp) | [橫式](S07-page49-1024x768.webp) |
| S08慧，x64/y11 | [直式](S08-page56-768x1024.webp) | [橫式](S08-page56-1024x768.webp) |
| S09風雨中央島 | [直式](S09-page66-768x1024.webp) | [橫式](S09-page66-1024x768.webp) |
| S10棟樑 | [直式](S10-page71-768x1024.webp) | [橫式](S10-page71-1024x768.webp) |
| 片尾來源圖 | [直式](S10-page75-768x1024.webp) | [橫式](S10-page75-1024x768.webp) |
| 主題導讀 | [直式](guide-768x1024.webp) | [橫式](guide-1024x768.webp) |
| 原經來源卡 | [直式](sources-768x1024.webp) | [橫式](sources-1024x768.webp) |

另有手機[信](S04-360x800.webp)、[精進](S05-360x800.webp)、[慧](S08-360x800.webp)，以及[片尾來源圖放大視窗](credits-zoom-768x1024.webp)。

## 開啟互動版

在本分支的專案根目錄執行：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

- 專頁：`http://127.0.0.1:8765/five-roots-powers/index.html`
- 繪本：`http://127.0.0.1:8765/five-roots-powers/book/index.html`
- 信根試排：`http://127.0.0.1:8765/five-roots-powers/book/index.html?scene=S04`
- 來源圖：`http://127.0.0.1:8765/five-roots-powers/book/index.html?scene=S10&page=75`

首頁書架第13本及既有五根五力地圖節點均接入本分支。沒有公開互動預覽主機；上述是本機HTTP路徑，不把GitHub程式碼頁、雙擊HTML或iPad檔案快速預覽說成可操作網站。PDF與截圖可以直接下載閱讀。

## 驗證結果

360×800、800×360、768×1024、1024×768、1440×900：全76頁共380個狀態通過，五條疊字的25個放大狀態、來源圖5個放大狀態通過。核對全部口白／時間／引文、完整原圖比例、黑字百分比／cqw與無transform偏移、上方字幕／下方經文、無水平溢出、上下頁／目錄／讀經與捲動／放大關閉／來源往返／旋轉重載保留頁碼／快速點按／末頁重讀。書架13、原地圖入口及其他12本開啟／翻頁／回導讀通過。

無本機HTTP或JS錯誤，[完整報告](validation.json)與[PDF核對](pdf-validation.json)已留存。首頁外部CSS／圖示以實際CDN回應攔截供應，網站檔案沒有換成測試stub。實體Safari、外部影片播放、音軌精校及引文版本差異仍待作者覆核，詳見[REVIEW](../../five-roots-powers/REVIEW.md)。

```sh
python3 scripts/build-five-roots-powers.py --check
python3 scripts/check-five-roots-powers.py
python3 scripts/build-five-roots-powers-preview.py
```

需Python、Pillow、lxml、Playwright及`/usr/bin/chromium`；PDF另需PyMuPDF與pdftotext。
