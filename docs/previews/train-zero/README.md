# 清除進度後電車與對話按鈕：實際驗證

[實作](../../play/train-zero/README.md) · [完整focused結果](validation.json) · [原版問題重現](before-reset-proof.json) · [原稿／圖片／核心保護](source-validation.json)

基準是PR86／`dd480b67959e90adc50f2bb8e0c2b1f80197d8f2`。實按原版Settings confirm後reading與receipt清除，但active map立刻寫arrival seen，再回title Start確實沒有train。修正版已通過下列focused驗證；正式發布的精確SHA／Pages及live證據以本輪PR為準。

- 真Settings取消保持raw存檔；確認清除返回title，電車前尚未寫arrival seen。按開始實際載入原PNG並出現完整兩段。
- 4個零本完成fixture（全新、全seen、書籤0、書籤2＋首段seen）均可從首頁開始完整兩段，原reading存檔保持。另測`#opening`首段-only可續第二段，已完成1本從首頁正常直接續程。
- 原生抵達3段按鈕依序「接著看／接著看／進去看看」；前兩段不開書，最後進原Four讀本，0→1→2／重整可續。讀本、城池、書架回海圖不插電車；再次返回title按繼續則整段電車可播，書籤2仍在。
- 正常Five入書末段「進去看看」可入原Five且完成數仍1；arrival/outro唯讀重播前段接著看、末段回到海圖，reading/story/receipt不改。合法Four已完成／receipt隔離fixture驗四段mandatory尾聲全「接著看」、Escape／城池不能繞過，最後才通知新增城景。此fixture不是完整重讀29頁。
- 真作者首頁reset仍有群貓prologue，再Start有完整電車。載入後故意注入local/session寫刪失敗，Settings reset不換頁，顯示暫時重置提示、當頁memory為fresh，舊canonical保留被誠實回報、沒有提前arrival seen。
- 代表尺寸360×800、844×390、1024×768；JS／同源HTTP錯誤0。17個changedJS語法、產生器、SEO15、14HTML僅bridge cache、45原書JS/CSS/CSV、24核心/圖片/CSS保護、原作者PNG／ZIP與30成員Seven離線包保持皆通過。

| 畫面 | 截圖 |
| --- | --- |
| 真Settings清除後，Start成功顯示原電車插畫及兩段字幕 | [1024×768](settings-reset-train-loaded-1024x768.png) |
| 第三段才出現「進去看看」 | [360×800](arrival-final-enter-360x800.png) |
| 故意注入存檔失敗，保留提示及原分頁 | [1024×768](failed-reset-keeps-status-no-redirect-1024x768.png) |

測試使用隔離瀏覽器資料；本輪未重讀十四本／完整29頁，也未重新驗未改動的插畫構圖。手機／平板為Chromium touch／viewport模擬，實機iPhone／iPad Safari未測。
