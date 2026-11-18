# 七覺支：收件與實作

兩份普通ZIP已安全合併：原storyboard.md、Codex_Prompt.txt與images/01–13共15檔。CRC／SHA-256與圖片尺寸見input-zips.json、receipt.json。原檔不改；本目錄的storyboard.json是依Markdown整理的程式資料，不冒稱作者原JSON。

網站為`seven-factors/`導讀及`seven-factors/book/`閱讀器；接原書架14和既有七覺支總說地圖節點。從main99b1a1d建立`feat/seven-factors-review`，作者於2026-11-18另行授權直接發布，經PR #43處理，取代原審閱限制。

保持12幅圖及36段原口白：主上一頁／下一頁、方向鍵與滑動依序讀完全部36段，讀完當幕才換圖。計數顯示36段與12圖頁，幕目錄仍可直接定位。原上方獨立換段控制已移除，避免只用主按鍵時漏讀。第12幕六段都讀完後才顯示回第一頁；舊scene/page/cue網址與記憶位置保留。

專頁不再顯示下載按鈕或原片經典出處截圖連結。離線ZIP留存並同步更新控制，可由既有檔案網址取得；原圖與交接不刪除。

- S08用臉部特寫08.png，S09用可見坐姿09.png；完整比例、不裁切。原圖標籤只顯示一次。
- 14條網頁字以**中心點**百分比定位，`translate(-50%,-50%)`在本書是正確錨點，勿套用其他書的左上座標規則。字級依原稿為圖高約13%（覺支）或9%（五蓋／火候），換算cqw。正常圖與放大圖同規則。
- S11只新增昏沉／浮動兩字；第4段聚焦左42%、第5段聚焦右42%，其餘總說／守護／念兼助全幅。中央16%念燈一直保留。使用原共用76%遮罩，未改共用檔。
- S12七個名稱已烘焙，不加HTML副本。13.jpeg僅留存為原始素材，專頁連結已依作者指示移除，不放入故事。
- 16個影片經文顯示區間按時間配對，包含同頁換文；見REVIEW。解說輕安，原引文保留猗息／猗覺分。

## 下載與離線

原先為本書新增下載按鈕，現已依作者要求從專頁移除，未改其他書。離線產物保留並同步維護。產物`downloads/SutraZen-Seven-Factors-Offline.zip`含29檔、插圖、資料與共用控制，不含CDN／遠端圖片／Base64。原全尺寸PNG留在本交接目錄，離線包用同尺寸WebP。

解壓後執行 `python3 start-local.py`，開啟 `http://127.0.0.1:8765/`。本機伺服器不需要Internet；外部原經／影片需連線，本包的原文節錄可直接離線讀。測試確實從導讀按鈕下載ZIP、核對CRC、解壓後由本機HTTP供應，封鎖所有其他來源，逐段／逐頁驗證。

本環境受管理Chromium禁止file://（ERR_BLOCKED_BY_ADMINISTRATOR），未驗證直接雙擊HTML。iPad檔案快速預覽不保證執行JS；實體Safari／iPad下載解壓流程亦未測，不能把本機HTTP模擬當成實機驗收。

## 重建

```sh
python3 scripts/build-seven-factors.py
python3 scripts/build-seven-factors-offline.py
python3 scripts/check-seven-factors-sequence.py
python3 scripts/build-seven-factors-preview.py
```

先重建資料／導讀，再重建離線包。原文／引文區別見[REVIEW](REVIEW.md)，試閱與實際結果見[預覽說明](../previews/seven-factors/README.md)。
