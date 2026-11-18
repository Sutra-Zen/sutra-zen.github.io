2026-11-18追加修正：主按鍵現逐段讀完36段後換圖，移除獨立換段列、專頁下載與出處圖連結。下方截圖／180狀態為舊操作模式歷史驗收；[最新主按鍵完整閱讀回歸與截圖](../seven-sequence/README.md)另列。

# 七覺支｜十二頁試閱

[PR #43](https://github.com/rooneyflower-star/sutrazen-map/pull/43)，分支`feat/seven-factors-review`，從main99b1a1d建立。作者已於2026-11-18授權直接發布，經PR #43處理。正式入口：[導讀](https://rooneyflower-star.github.io/sutrazen-map/seven-factors/)／[繪本](https://rooneyflower-star.github.io/sutrazen-map/seven-factors/book/)。實際Pages與正式備份核對見PR最後紀錄；以下保留原試閱方式與歷史驗收。

- [12頁完整PDF](Seven-Factors-review.pdf)：12張原圖與14條中心疊字，完整36段口白及其對應引文，文字可選取。A3橫式供放大對讀，非網頁操作介面。
- [離線ZIP](../../../downloads/SutraZen-Seven-Factors-Offline.zip)：先完整解壓，執行`python3 start-local.py`，開啟http://127.0.0.1:8765/。包內有說明；不需要Internet素材，影片與外部經典網站除外。

## 畫面

| 項目 | iPad直式768×1024 | iPad橫式1024×768 |
| --- | --- | --- |
| 浮動／第一頁 | [直式](S01-cue1-768x1024.webp) | [橫式](S01-cue1-1024x768.webp) |
| 五蓋中心標籤 | [直式](S03-cue1-768x1024.webp) | [橫式](S03-cue1-1024x768.webp) |
| 念／幕內換經文 | [直式](S04-cue1-768x1024.webp) | [橫式](S04-cue1-1024x768.webp) |
| 輕安臉部特寫 | [直式](S08-cue1-768x1024.webp) | [橫式](S08-cue1-1024x768.webp) |
| 定／可見坐姿 | [直式](S09-cue1-768x1024.webp) | [橫式](S09-cue1-1024x768.webp) |
| 昏沉／左側聚焦 | [直式](S11-cue4-768x1024.webp) | [橫式](S11-cue4-1024x768.webp) |
| 浮動／右側聚焦 | [直式](S11-cue5-768x1024.webp) | [橫式](S11-cue5-1024x768.webp) |
| 念兼助／全幅 | [直式](S11-cue6-768x1024.webp) | [橫式](S11-cue6-1024x768.webp) |
| 總結／最後一頁 | [直式](S12-cue1-768x1024.webp) | [橫式](S12-cue1-1024x768.webp) |
| 主題導讀 | [直式](guide-768x1024.webp) | [橫式](guide-1024x768.webp) |
| 原經來源卡 | [直式](sources-768x1024.webp) | [橫式](sources-1024x768.webp) |

共37張截圖，包括各幕及手機[五蓋](S03-360x800.webp)／[輕安](S08-360x800.webp)／[火候](S11-360x800.webp)。上方段落按鈕切換口白與經文，下方／左右主按鍵切換圖頁，保持12頁而非36頁。

## 本機互動預覽

在完整專案根目錄執行`python3 -m http.server 8765 --bind 127.0.0.1`：

- 導讀：`http://127.0.0.1:8765/seven-factors/index.html`
- 閱讀器：`http://127.0.0.1:8765/seven-factors/book/index.html`
- 第11幕左側：`http://127.0.0.1:8765/seven-factors/book/index.html?scene=S11&cue=4`
- 第11幕右側：同一路徑`?scene=S11&cue=5`

沒有公開互動預覽主機。GitHub HTML程式碼頁不會執行網站；PDF與ZIP可直接下載。

## 實際驗證

360×800、800×360、768×1024、1024×768、1440×900：線上36段×5=180狀態、實際下載ZIP後離線包36段×5=180狀態；14條字及S11各段放大的120個字框核對通過。圖片完整比例、中心座標／字高、字幕在上／經文在下、無水平溢出、同幕經文切換／無殘留、左右聚焦、主翻頁與段落切換、目錄、旋轉／重載保留頁碼及段落、快速點按、首頁／末頁重讀、來源與返回均通過。書架14／原地圖節點、13本舊書開啟／翻頁／回導讀回歸通過。

離線測試確實從導讀下載按鈕取得ZIP，核對CRC、解壓，由本機HTTP供應檔案並封鎖所有其他來源；不替換空白資料或使用線上圖片。環境Chromium政策禁止file://，**直接雙擊本機HTML未測**；也未測實體iPad/Safari及iPad檔案預覽。這些限制與離線包操作方式均隨包附上，未宣稱已完成實機離線驗收。

報告：[validation.json](validation.json)、[PDF全文核對](pdf-validation.json)、[最後結語及最新下載ZIP追加檢查](ending-download-check.json)。無JS或本機HTTP錯誤；最新ZIP原始碼／CSS與包內相同。引文版本與時間校稿見[REVIEW](../../seven-factors/REVIEW.md)。

重現：`python3 scripts/check-seven-factors.py`。重建資料與離線ZIP後再測，詳見交接README。
