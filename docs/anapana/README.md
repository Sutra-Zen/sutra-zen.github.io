# 安那般那與止觀・Codex交接包

兩包均須下載，解壓後合併同名資料夾。每包小於32,000,000 bytes。Part1包含文件、JSON、定位影格與前6張原圖；Part2包含後5張原圖。原圖不改像素、不降解析度。沒有包含原始MOV，未製作新網站。

入口：CODEX_PROMPT.txt → docs/STORYBOARD.md → storyboard.json。對應經文：scripture-catalog.json。疊字：overlays.json與docs/OVERLAY_SPEC.md。圖檔清單與雜湊：asset-manifest.json。

Notion來源：https://app.notion.com/p/419cf2ef57db81d99f88d90cfadce19a

所有相對路徑以本資料夾為根。原圖assets/S01.png至S11.png；references/source-screenshot.png為使用者提供出處；Sxx-video.png是成片定位截圖（含字幕與疊字），只供比對，不得誤作正式插畫。小字或來源校勘疑點見SOURCE_NOTES。時間碼為秒級估計，非精準字幕時間軸。

完整性驗證：在本資料夾執行 `python3 scripts/validate.py`，只使用Python標準函式庫。

資料狀態：118段口白依字幕轉錄，41筆引文尚未逐一外部校勘；可進行實作，正式內容仍保留使用者校稿步驟。12條疊字座標是可用初值，需在真正的閱讀器中視覺驗收。封包僅交接所提供的素材與分鏡，不含網站發布操作。
