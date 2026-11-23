# 「疑」過場與深色半透明介面實測

本機基準：main `44dce2f6624e568ff83d6cf79e675fe61a53c325`。一般入口 `/game/`；作者試玩入口 `/game/?author=1`。本目錄不是發布證明；正式站狀態須核對本輪精確 merge SHA 的 Pages 與實際網址。

[完整結果](validation.json)來自 `scripts/check-game-doubt-story.py` 的原生瀏覽器操作。另附兩個獨立元件審查者的[問號與退場圖層報告](independent-stage-validation.json)及[主題／全耳肖像報告](independent-theme-validation.json)，分別複製自 `/workspace/artifacts/doubt-stage/validation.json`、`/tmp/game-dark-theme/results.json`。另附獨立唯讀審查者的[十種receipt／歷史狀態檢查](independent-receipt-guards.json)，原件為 `/tmp/game-doubt-independent-guards.json`。歷史資料均為隔離測試 profile，不讀寫作者資料；不以 fixture 宣稱完成整本閱讀。

## 實際通過

- **第一本完整走完**：原到達台詞 →「疑」唯一台詞「愚痴……」→ 小貓決定繞過入口 → 原繪本。實際按 Next 走過 index 0–28，途中 index 5 重整／旋轉／回圖再續讀；最後按「完成這本」才由 0 變 1 本。
- **真完成後過場**：實際 reader receipt 被消耗後，出現小貓「正智」「慧根／慧力」仍需慢慢練習的兩句創作口白；世界圖層問號由 7 減至 2，角色退入霧，再顯示原法輪碼頭回饋。「前往下一站」只定位五陰，不自動開書。
- **不虛增進度**：開書、中途返回、重整、歷史已完成＋偽造 `completed` 網址、僅有 receipt、未來書籤，都不製造完成或自動退場。書架原生複習利用章節選單到末步完成，不發新 receipt；顯式重看過場不改 collection 或 seen 原值。
- **對話續演與略過**：已看第一句、尚未看最後句的隔離資料只續最後句；明確略過則確認整段，不在下次進圖強制重播。作者重置會清新 scene ID 及 local／session receipt，原 v1 namespace、原網站及其他鍵值保留；取消逐值不變。
- **故障可讀**：各別封鎖小貓或疑的圖片，全文及按鍵仍能進原讀本並實際翻頁。只在 reader 封鎖非必要 receipt helper，從明示的 index 27 fixture 按 Next 至 28、明確完成，仍得到正常原回饋；不冒稱這個故障案例完整翻過 29 步。
- **五尺寸**：1280×900、360×800、844×390、768×1024、1024×768 的首頁、設定、到達／疑對話、工具、城池來源框及書架。深色半透明表面保留實際 alpha；以最亮白色底圖估算，標題主文字對比 8.39:1、口白 9.13:1，均超過 AA。原生 modal backdrop 透明，世界圖片沒有全局 filter／opacity 暗化；沒有新增主題切換器。小貓完整矩形 contain、無圓形裁切，雙耳完整；旅人不顯疑的問號。按鍵至少 48px、對話不壓底列、無頁面溢出。
- **演出可見區**：五尺寸另外量測世界角色完整框及每個可見問號，均位於對話下緣與底列上緣之間；過場關閉後暫時 top inset 回到 0。首遇截圖為全新 profile；五尺寸 post 導演配置另用清楚標示的完成 fixture，不混入真 29 步結果。橫式真完成的三張截圖已在最終移鏡版重新以原生 29 步產生。
- **原站保護**：615 個保護檔中 614 逐位元相同；四聖諦 HTML 僅 bridge 的版本參數改動，normalize 該參數後全文相同。口白、經文、插圖、讀本 JS／CSS、正式首頁／SEO／Google 檔完全保留；資格、collection store、route、camera、原稿及舊素材不變。bridge 只加收據預載／成功後發出與非必要載入失敗退化；重置 helper 只多清收據及一致快取版本。零 JS／同源 HTTP 錯誤。

## 代表畫面

| 畫面 | 截圖 |
| --- | --- |
| 深色首頁 | [桌面](title-dark-1280x900.png)／[手機](title-dark-360x800.png) |
| 深色設定 | [平板](settings-dark-768x1024.png) |
| 小貓完整雙耳、原到達台詞 | [手機直式](arrival-full-ears-360x800.png)／[橫式](arrival-full-ears-844x390.png) |
| 疑與問號、唯一台詞 | [手機直式](doubt-before-reading-360x800.png)／[平板橫式](doubt-before-reading-1024x768.png) |
| 實際 29 步後縮問號與退場 | [問號減少](actual-first-read-questionmarks-thinning-844x390.png)／[退場](actual-first-read-creature-receded-844x390.png) |
| 五尺寸 post 演出可見區（隔離完成 fixture） | [手機直式](post-director-isolated-fixture-360x800.png)／[平板直式](post-director-isolated-fixture-768x1024.png) |
| 原完成回饋 | [第一本法輪碼頭](actual-first-book-reward-844x390.png) |
| 城池與書架局部深色表面 | [城池來源](city-dark-dialog-360x800.png)／[書架](shelf-dark-360x800.png) |

## 重現與限制

根目錄執行 `python3 -B scripts/check-game-doubt-story.py`。手動可用 `python3 -m http.server 8780 --bind 127.0.0.1`，開啟 `http://127.0.0.1:8780/game/`；試玩重置加 `?author=1`。

這是桌面 Chromium 的尺寸及輸入模擬，沒有實機 Safari 驗證。角色演出是可獨立略過的教學故事，不是證果或斷疑的判定；新「疑」素材仍為待作者確認的概念稿。原書未改，故不重跑十四本 1192 步。此次完整原生閱讀只計前述 29 步；歷史、pending、故障與近末步複習案例均獨立標示。
