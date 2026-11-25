# 對話文字選單與字幕留白：驗證與畫面

[實作](../../play/dialogue-reader-space/README.md) · [原稿／核心／離線包保護](source-validation.json) · [對話完整結果](story/validation.json) · [閱讀器完整結果](reader/report.json)

基準為PR88／`a079a9191425e18b24dfd9371f52e91532802158`。本輪本機檢查全部通過；正式發布的精確merge SHA、Pages與live紀錄以本輪PR為準。

## 兩個文字選項

- 抵達終幕無X、按鈕為「回到地圖／閱讀下一關」。Map不開書、不創書籤或計完成，可真城池／書架／海圖探索、重整不重彈；ReadNext直接原Four0–1。中間仍只有接著看、Escape／City不能繞，重整精確原幕。
- 合法Four已完成28／receipt隔離fixture涵蓋360×800、844×390、1024×768：末幕保留原台詞及同一份原新增地景／城池／count1，重整保持checkpoint/context。Map直接回圖且沒有第二層通知或Five書籤；ReadNext直接原Five0–1，count仍1。這不是本輪實際重讀29頁。
- 正常Five入口同兩選項且無不相干獎勵；genericFive完成通知兩分支可回圖或合法Six0。非依序歷史（只Five完成／Four2）會續合法Four2，不能跳鎖定Six。all14的Map不自動彈結語，明確結語按鈕可正常開既有結尾，沒有第15本。
- arrival/outro重播末幕只留可見、可鍵盤操作的Map，reading／seen／pending／receipt local/session bytes不改。舊Four0保持優先；實際Settings reset仍清pending→title→完整減少動畫電車→fresh抵達。
- 面板文字、回饋、按鈕不互覆，兩按鈕各48px以上且可達。短橫844×390的長回饋需要內捲，已用原生wheel確認全文／本數／按鈕可達；沒有宣稱全部初始都塞進視窗。JS／同源HTTP錯誤0，原生只抽Four／Five0–1，完成／全14是隔離fixture。

| 畫面 | 截圖 |
| --- | --- |
| 抵達終幕兩文字鈕 | [手機直式](story/arrival-two-buttons-360x800.png) |
| 原台詞與讀後提示在同一末幕 | [360×800](story/first-tail-inline-360x800.png)／[1024×768](story/first-tail-inline-1024x768.png) |
| 短橫式可內捲長回饋 | [844×390](story/first-tail-inline-844x390.png) |

## 繪本字幕與圖高

14本普通圖文的140個配置（8 public尺寸＋2 game-review尺寸）、280個最長／短句代表與28次原生Next通過。普通矩陣的逐書成功記錄見[原始log](reader/verify.log)；特殊頁helper原本假設純文字頁也有可見caption，後續只修helper並補跑特殊頁，沒有改產品來源或重跑已通過的普通矩陣。[follow-up log](reader/finalize.log)與完整report記錄22個特殊頁及共同圖高對比。

- 同一視窗14本共同圖高差0px，包含1280×720、844×390、667×375、800×600、900×600；最長和短句翻頁圖高一致，原文、字級／行距、比例與控制項避讓保持。
- 844×390通常兩行；667×375五陰44真三行。十二因緣41在667×375真四行，保留三行帶並可原生wheel捲到末段，不截字或縮字。[窄版捲讀](reader/twelve-four-lines-scrolled-667x375.png)
- 14結語及4心經橫／直式共22個特殊配置通過；心經保留完整直書／RTL，結語全文與原grid欄位可讀；旋轉與重整保持頁碼。
- 精確before/after：1280×720字幕帶110→82px，圖549.594→577.594px（+28）；1916×963圖792.594→820.594px（+28）。1280×900原本受圖寬上限限制，字幕同減28px但圖高保持648.875px；沒有強行放大破壞原比例上限。
- [全字幕字寬量測gzip](reader/probe-threshold.json.gz)／[800與900視窗量測](reader/probe-compact-tablet.json.gz)／[候選名冊](reader/longest-candidates.json.gz)及[原始SHA](reader/raw-digests.json)保留分析證據。這是完整文字量測加原生代表頁，不是重新逐步讀完1192步。

| 畫面 | 截圖 |
| --- | --- |
| 兩行帶與較大的圖框 | [修改前](reader/four-truths-before-1280x720.png)／[修改後](reader/four-truths-after-1280x720.png) |
| 五陰長字幕，844保留兩行 | [844×390](reader/five-long-844x390.png) |
| 更窄畫面保留三行 | [667×375](reader/five-long-667x375.png) |

17個runtime只更新cache，原45個book JS/CSS/CSV、22核心／圖片／shared CSS與seen/pending/reading/route保存資格皆保持；shared layout只改預算公式與驗證用CSS變數。原電車ZIP／PNG保護，Seven離線包30成員CRC／SHA符合，只有shared layout及其HTML query改動。Game產生器／SEO15／19個changedJS語法通過。

使用隔離瀏覽器資料；手機／平板為Chromium viewport/touch模擬，實機iPhone／iPad Safari與螢幕閱讀器未測。
