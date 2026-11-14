# Notion 改版紀錄待補記

此工作環境未提供 Notion 工具，尚未寫入。
目標：https://www.notion.so/40bcf2ef57db81658247c1e8268c3ccd

## 2026-11-14｜改善繪本快速連按翻頁誤放大

五本繪本的翻頁按鈕共用 reader-controls.css，加入 touch-action: manipulation，橫直式皆生效。保留雙指縮放與捲動，未限制整頁縮放、未加入翻頁延遲。製作規則要求未來繪本沿用共用設定。完成手機及iPad橫直尺寸的樣式與連按模擬檢查；實際Safari手勢改善由作者在正式站實測。發布以本次PR與Pages結果為準。
