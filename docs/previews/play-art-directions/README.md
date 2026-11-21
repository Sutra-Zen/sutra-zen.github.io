# 美術比較預覽（2026-11-21，未發布）

本輪可在同一頁切換三種地圖畫風；原水彩保留比較，新增塔防地景與奇幻世界。地圖不顯示「相關內容大陸」字樣，主題山群及互通資料保留。六門城池採無格線俯視遊戲場景；書架保留樹屋背景，封面改為直式裝幀。

## 實際截圖

| 畫面 | 桌機 | 手機 |
| --- | --- | --- |
| A 塔防地景 | [完整預覽](map-terrain-1280x900.png) | [手機](map-terrain-390x844.png) |
| B 奇幻世界 | [完整預覽](map-world-1280x900.png) | [手機](map-world-390x844.png) |
| 無棋格六門城池 | [完整預覽](city-topdown-1280x900.png) | [手機](city-topdown-390x844.png) |
| 未收集書封 | [完整預覽](shelf-unearned-1280x900.png) | [手機](shelf-unearned-390x844.png) |
| 已收集書封示意 | [完整預覽](shelf-all-earned-1280x900.png) | [手機](shelf-all-earned-390x844.png) |
| 真實完成一本的測試 | [29步後完成](shelf-actual-first-completion-1280x900.png) | — |

部分／全收集的視覺截圖使用隔離瀏覽器QA存檔，不是作者真實閱讀紀錄。產品仍只在最後一步按「完成這本」才記入一次。

## 本機試閱與檢查

從專案根目錄執行 `python3 -m http.server 8765`，開啟：

- `http://localhost:8765/play/visual-v2/?style=terrain`
- `http://localhost:8765/play/visual-v2/?style=world`
- `http://localhost:8765/play/visual-v2/?style=watercolor`
- `http://localhost:8765/play/visual-v2/?view=city`
- `http://localhost:8765/play/visual-v2/shelf.html`

`python3 scripts/check-play-art-directions.py` 是本輪風險檢查。實際報告見 [validation.json](validation.json)：五種手機／平板橫直及桌機尺寸、320次新地圖節點點選、65次城池熱區、六門／四演出狀態、15書架狀態、真實29步閱讀完成／續讀、來源與受保護檔逐位元比對均通過，無JS／HTTP錯誤。既有三項視覺回歸及SEO檢查另通過。

原閱讀器與存檔邏輯未改，本輪不重複前輪全部1192步；實機Safari、GPU效能及作者的最終美術確認待補。新背景為概念整張畫，尚未全部分層；封面僅縮圖使用滿版取景，不改原插畫檔案或完整閱讀畫面。無公開預覽，未合併main、未發布Pages。
