# 電車上捲字幕至五陰：最終驗證與截圖

作者補交原始ZIP後，正式1672×941PNG已逐位元匯入；最終電車依最新要求改為滿版插畫上的連續上捲字幕，進地圖才出現頭像對話。Phase B通過，沒有未解決阻擋項。實際發布證據以本輪PR的精確merge SHA、Pages及live紀錄為準。

[實作／完整12列劇本](../../play/train-opening/README.md) · [原圖來源／SHA](../../play/train-opening/assets.json) · [精簡結果](summary.json) · [完整Phase B gzip](phase-b-validation.json.gz) · [獨立crawl複驗](independent-crawl-review.json) · [原始報告雜湊](raw-evidence-digest.json)

## 最終原圖與跑馬燈 Phase B

- 6尺寸：1916×963、1280×900、1024×768、768×1024、844×390、360×800。實際原圖載入，兩段HTML文字完整、無頭像框，白字提示沒有按鈕外框；手機臉部／耳朵保持在crop內，文字可讀可捲。
- 正常動畫實等700ms確認向上移動；獨立一次20秒完整自然播放（無seek／freeze）及650ms暖光後到法輪遺跡。首段milestone後重整只續第二段；milestone測試的92%seek明列，不冒充自然播放。
- 減少動畫採靜態捲讀；略過與連點不穿透讀本，唯讀電車重播保持reading／story／receipt原始儲存值。
- 故意abort原圖請求會顯示失敗／重試，第二次實際載入成功。最終title白框、原生Four0→1→2／重整／返回不重插電車通過。
- JavaScript／同源HTTP錯誤0；故障注入是測試刻意abort，非HTTP404。獨立複驗另實等首段離場→重整接第二段，以及短橫式完整自然播放。使用隔離資料，不改作者存檔。

## 代表畫面

| 畫面 | 截圖 |
| --- | --- |
| 正常上捲字幕示意，**為截圖暫停於50%** | [1280×900](phase-b-train-moving-freeze-1280x900.png) |
| 手機直式：正式原圖與減少動畫靜態文字 | [360×800](phase-b-train-static-360x800.png) |
| 手機橫式：正式原圖與靜態文字 | [844×390](phase-b-train-static-844x390.png) |
| 寬版減少動畫文字 | [1280×900](phase-b-train-static-1280x900.png) |
| 入口兩個白框按鍵，原群貓背景 | [1280×900](title-white-frames-1280x900.png)／[360×800](title-white-frames-360x800.png) |
| 四聖諦尾聲望向五陰湖，仍為最終同一份劇本 | [1280×900](phase-a-native-outro-tail-1280x900.png) |

## 先前 Phase A 的原生閱讀與相容驗證

[完整Phase A gzip](phase-a-validation.json.gz)／[當時摘要](phase-a-summary.json)記錄原圖補交前的明示缺圖UI。其舊電車逐段對話框已被最終crawl取代，相關fallback截圖只是歷史證據，**不是目前正式畫面**。原生讀本與地圖尾聲在最終crawl改版時未改，因此保留其實際閱讀驗收：

- 真四聖諦0–28逐步原生Next，末頁按「完成這本」前不計數，明確完成才寫1本／發receipt；依序first-book-insight→doubt-escapes→doubt-recedes→toward-aggregates-lake，再出現新增城景通知、城池／下一站。
- 五陰0→1→2→3，旋轉／重整／map-shelf往返保持3；過場不增加已讀數或跳關。這次最終crawl只另走Four0–2，未重讀29步。
- 6個歷史fixture：Four0／Four8／Five0／all14／arrivalSeen／doubtSeen，保留進度並跳過新電車；四聖諦尾聲末段重整可恢復。

[story相容與quota恢復](story-compatibility.json)保留原7個IDs含Mara，新增3個IDs且不寫reading store；[原稿與核心保護](source-validation.json)確認14HTML只改bridge cache、45原書JS／CSS／CSV、19核心檔與30成員Seven離線包保持。預設原圖asset gate、遊戲產生器及SEO15檢查通過。

手機／平板為Chromium視窗與touch模擬，未測實機iPhone／iPad Safari。
