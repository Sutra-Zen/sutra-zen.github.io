# 四禪／安那般那閱讀整理驗證（2026-11-18）

基準main：`e578c2a85131c646ad4986e8c1367d7d60f8e652`；實作分支：`fix/jhanas-table-anapana-focus`。

正式入口：[四禪繪本](https://sutra-zen.github.io/four-jhanas/book/)／[安那般那繪本](https://sutra-zen.github.io/anapana/book/)。發布是否完成，以本次PR最後的Pages／公開檔案核對為準。

## 本次畫面

| 修改 | iPad直式768×1024 | iPad橫式1024×768 | 手機360×800 |
| --- | --- | --- | --- |
| 瞋恚避開小怪獸臉部 | [五蓋](jhanas-S05-768x1024.webp) | [五蓋](jhanas-S05-1024x768.webp) | [五蓋](jhanas-S05-360x800.webp) |
| 原圖表格保留，圖下不再重複 | [四禪總結](jhanas-S10-768x1024.webp) | [四禪總結](jhanas-S10-1024x768.webp) | [四禪總結](jhanas-S10-360x800.webp) |
| 身隨觀逐格聚焦 | [身](anapana-S04-768x1024.webp) | [身](anapana-S04-1024x768.webp) | [身](anapana-S04-360x800.webp) |
| 受隨觀逐格聚焦 | [受](anapana-S05-768x1024.webp) | [受](anapana-S05-1024x768.webp) | [受](anapana-S05-360x800.webp) |
| 心隨觀逐格聚焦 | [心](anapana-S06-768x1024.webp) | [心](anapana-S06-1024x768.webp) | [心](anapana-S06-360x800.webp) |
| 法隨觀逐格聚焦 | [法](anapana-S07-768x1024.webp) | [法](anapana-S07-1024x768.webp) | [法](anapana-S07-360x800.webp) |

另有[放大後的第二格](anapana-zoom-768x1024.webp)。四禪[24頁PDF](../four-jhanas/Four-Jhanas-review.pdf)同步更新，逐字核對全部130段字幕與8筆完整經文。

## 範圍與結果

Chromium觸控模擬五種尺寸：360×800、800×360、768×1024、1024×768、1440×900。

- 安那般那S04–S07的55筆口白逐頁核對，共275個狀態；16格各驗放大／關閉，共80個放大狀態。確認目前格透明、另外三格76%遮黑，座標與圖片實際像素範圍一致。介紹／收尾與非指定幕不殘留遮罩。
- 四禪S05的6頁與S10的7頁，共65個狀態；確認瞋恚在圖高17%、標籤下緣不進臉部區域，讀經與圖下無重複表格，全部對應引文照常顯示。
- 測試字幕在上／經文在下、原圖完整比例、無水平溢出、上下頁／目錄、放大關閉、快速連按、讀經視窗與捲動、返回導讀、旋轉保留頁碼及安那般那末頁重讀。無本機HTTP或JavaScript錯誤，報告見[validation.json](validation.json)。
- 安那般那119頁資料逐位元組不變；四禪130段字串／時間／經文不變，只有重複表格資料與瞋恚位置調整。原圖、共用遮罩／控制檔、其他10本、首頁與Pages設定逐檔比對不變。

這是本次受影響畫面的針對性檢查，沒有宣稱重新逐頁驗收所有繪本。實體iPad/iPhone Safari手勢仍未測。

重現檢查（需Python、Pillow、lxml、Playwright及`/usr/bin/chromium`）：

```sh
python3 scripts/check-reading-focus.py
```

本機試閱可於專案根目錄執行 `python3 -m http.server 8765 --bind 127.0.0.1`，再開 `/four-jhanas/book/?scene=S05&page=14` 或 `/anapana/book/?scene=S04&page=18`。
