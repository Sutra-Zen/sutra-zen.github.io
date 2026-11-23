# 四聖諦完成尾聲：流程順序驗證

基準：`2720747323f4d3a05474bf0c2919ac5332810cb2`。本目錄記錄本機瀏覽器實測，不是正式發布證明。

重現完整檢查：

```sh
python3 -B scripts/check-game-outro-order.py
```

[實際結果](validation.json) 為 `passed`，無 JavaScript／非預期 HTTP 錯誤。報告將原生閱讀流程與合成歷史存檔分開記錄。只有 `nativeFirstTailCityFive` 真正從第一頁逐次按「下一頁」讀完四聖諦 29 步，並在末頁明確按「完成這本」。未用頁碼捷徑製造完成紀錄。

已驗證的新順序：**心得 → 疑退場 → 波旬 → 五陰湖銜接 → 原閱讀獎勵 → 可先進城安置 → 五陰原閱讀器**。波旬頁與五陰湖銜接頁重新整理後保留待完成片段；尾幕顯示時的 seen 紀錄不冒充尾聲已確認，只有尾幕確認／略過才到原獎勵。

原生流程另實際進城手放法輪碼頭，再回地圖開五陰，翻到第 4 個閱讀步驟、重新整理與旋轉手機尺寸後返回，仍保留書籤與碼頭；不再重播五陰湖過場，也未增加第二本完成數。

## 實際截圖

- [真實讀完 29 步後，五陰銜接在獎勵之前](actual-first29-tail-before-reward-1280x900.png)
- [尾幕重新整理後仍是完成鏈](actual-first29-tail-restored-1280x900.png)
- [尾幕確認後的原獎勵面板](actual-first29-reward-after-tail-1280x900.png)
- [先進城手動安置碼頭](actual-first29-city-handplaced-dock-1280x900.png)
- [五陰 index 3 續讀返回（手機）](actual-five-index3-return-360x800.png)
- [手機直式尾幕](tail-pending-fixture-360x800.png)
- [手機橫式尾幕](tail-pending-fixture-844x390.png)
- [平板直式尾幕](tail-pending-fixture-768x1024.png)
- [平板橫式尾幕](tail-pending-fixture-1024x768.png)
- [桌面尾幕](tail-pending-fixture-1280x900.png)

五尺寸尾幕截圖使用**清楚標示的獨立 pending 存檔 fixture**，不是另外讀完五次第一本。檢查全角色肖像、可讀文字、48px 按鍵、清青色 CTA 對比、底列不遮擋與頁面不溢出。

## 邊界與回歸

- 完成鏈期間實際點擊底列地圖／城池／書架、主讀本、工具及地標，並以鍵盤啟動導覽，皆不能繞過尾幕；不寫閱讀／城池／對話額外進度。
- 設定仍可使用：取消重設不改任何存檔；確認重設清自己的進度與舊尾聲，保留無關鍵值，從同一 story v1 實例重新顯示到達對話。
- 前段略過仍先到五陰湖尾幕，重新整理仍停在未確認的尾幕；尾幕略過才到原獎勵；下一站只定位五陰，不強制開書或再播尾幕。
- 舊 Mara＋cutoff 已見、未見尾幕且未開五陰的末頁存檔可補尾。舊版 insight＋尾幕 seen 但未見 Mara 的存檔，仍先補疑退場與 Mara，不跨過未看的角色。
- 只靠歷史完成、已確認尾幕、五陰書籤 index 0／4、四聖諦複習中途，皆不強插完成尾幕；未解鎖五陰的未來書籤不會越關。
- 工具重播包含尾幕且唯讀：不新增 seen、不變更收藏／城池、不出獎勵、不開讀本。
- 原 615 個站點檔案保護；十四本 HTML 僅 bridge cache query 的窄例外，正規化後全文與基準相同。閱讀 core、receipt、資格、route、城池安置及原圖／經文／SEO／Google 驗證檔保留。

獨立唯讀程式審查亦確認 context 傳遞、Five 第 0 頁書籤排除、複習末頁條件、舊存檔片段補齊及 replay 分支，未編輯 runtime。

實機 iPhone／iPad Safari **未測**；此輪為 Chromium 桌面尺寸與原生瀏覽器點擊。未重翻全部十四本；發布成功需另核對精確 merge SHA 的 Pages 與正式 HTTPS 流程。

最後驗證範圍：完整原生 29 步／城池／五陰及五尺寸已先通過；最後兩項小修（前段略過後重整仍留尾幕、設定重設後關窗回焦新到達 CTA）另針對最終程式重跑全部 skip／history／replay／reset cases，並更新來源保護。未因焦點小修反覆重讀未變更的整本。完整檢查腳本仍保留單一執行入口。
