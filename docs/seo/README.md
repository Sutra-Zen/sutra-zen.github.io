# SutraZen SEO 與 Google 驗證（2026-11-21-r2）

本次以最新main `db3a882b4ec2d4dd7647cbbeef9f4622a214cb84` 開始，工作區起初乾淨，origin為 `https://github.com/Sutra-Zen/sutra-zen.github.io.git`。使用交接版本 **2026-11-21-r2**；作者最後補充明確授權將SEO及Google驗證檔一起發布，取代附件README原先只試閱的階段指示。既有GitHub Pages `main:/` 與管理流程保留。

`seo_pages.json` 是原交接JSON逐位元副本，提供15頁唯一的title、description、canonical；其中stage及website_status描述交接快照，不代表現在的發布或Google收錄狀態。原README／CODEX_PROMPT存於handoff-2026-11-21-r2/供追溯。實際驗證報告見../previews/seo-r2/validation.json；發布SHA、Pages與正式網址驗收證據記入本次PR。

## 逐頁套用清單

每頁均更新或補入單一title、description、canonical，OG／Twitter文字與這三項同步；以下15個canonical也是sitemap的精確集合。完整逐頁description保留在seo_pages.json及驗證報告。

|順序|主題／source_path|HTML title|canonical|
|---|---|---|---|
|00|首頁 · `index.html`|佛法繪本與三十七道品修道地圖｜SutraZen|https://sutra-zen.github.io/|
|01|四聖諦 · `four-truths/index.html`|四聖諦是什麼？苦集滅道的繪本導讀｜SutraZen|https://sutra-zen.github.io/four-truths/|
|02|五陰 · `five-aggregates/index.html`|五陰與五受陰有何不同？色受想行識導讀｜SutraZen|https://sutra-zen.github.io/five-aggregates/|
|03|六處 · `six-senses/index.html`|六處是什麼？六根、六境、六識的關係｜SutraZen|https://sutra-zen.github.io/six-senses/|
|04|十二因緣 · `twelve-links/index.html`|十二因緣是什麼？十二支與緣起的繪本導讀｜SutraZen|https://sutra-zen.github.io/twelve-links/|
|05|八正道與十善業道 · `eightfold-path/index.html`|八正道與十善業道：修行方向與日常善行｜SutraZen|https://sutra-zen.github.io/eightfold-path/|
|06|四向四果與十結 · `four-fruits-ten-fetters/index.html`|四向四果與十結：果位與煩惱止息的關係｜SutraZen|https://sutra-zen.github.io/four-fruits-ten-fetters/|
|07|四不壞淨與六念 · `four-purities-six-recollections/index.html`|四不壞淨與六念：清淨信心與日常憶念｜SutraZen|https://sutra-zen.github.io/four-purities-six-recollections/|
|08|四念處與四顛倒 · `mindfulness/index.html`|四念處與四顛倒：身、受、心、法導讀｜SutraZen|https://sutra-zen.github.io/mindfulness/|
|09|四正勤 · `right-effort/index.html`|四正勤是什麼？斷惡修善的四個方向｜SutraZen|https://sutra-zen.github.io/right-effort/|
|10|安那般那與止觀 · `anapana/index.html`|安那般那與止觀：十六勝行繪本導讀｜SutraZen|https://sutra-zen.github.io/anapana/|
|11|四如意足 · `iddhipada/index.html`|四如意足是什麼？欲勤心觀與專注的條件｜SutraZen|https://sutra-zen.github.io/iddhipada/|
|12|四禪 · `four-jhanas/index.html`|四禪有何不同？初禪至第四禪比較與譬喻｜SutraZen|https://sutra-zen.github.io/four-jhanas/|
|13|五根五力 · `five-roots-powers/index.html`|五根五力：信、精進、念、定、慧的作用｜SutraZen|https://sutra-zen.github.io/five-roots-powers/|
|14|七覺支 · `seven-factors/index.html`|七覺支是什麼？認識覺支與用功的調整｜SutraZen|https://sutra-zen.github.io/seven-factors/|

## 真正的建置來源

共享 `scripts/site_seo.py` 從交接JSON讀取文案，只更新head中的metadata，不重新序列化正文。`scripts/build-seo.py` 用於15頁的靜態套用及搜尋檔案建置；`--check` 驗證已提交HTML、sitemap、robots及驗證檔原始雜湊。

|頁面|原有來源及這次同步方式|
|---|---|
|安那般那與止觀|`scripts/build-anapana.py` 的compile_guide最後呼叫apply_page_seo|
|四禪|`scripts/build-four-jhanas.py` 的guide最後呼叫apply_page_seo|
|五根五力|`scripts/build-five-roots-powers.py` 的guide最後呼叫apply_page_seo|
|七覺支|`scripts/build-seven-factors.py` 的guide最後呼叫apply_page_seo；會覆蓋從五根五力模板繼承的metadata，保證七覺支自己的canonical及JSON-LD|
|其餘11頁（首頁＋10導讀）|既有HTML為來源；相關build程式只產生繪本資料，沒有會覆寫這些導讀head的建置器。透過build-seo.py更新，不重建繪本|

```sh
python3 -B scripts/build-seo.py
python3 -B scripts/build-seo.py --check
python3 -B scripts/check-seo.py --browser
```

check-seo.py同時包含本批r2相對固定基準的正文／範圍稽核；後續另行授權的正文修改不應為了重跑舊批次稽核而恢復舊稿。日常metadata維護使用build-seo.py --check。

修改SEO文案後執行套用指令，提交JSON與受影響HTML。新增會產生導讀head的程式時，最後呼叫apply_page_seo。四個既有導讀建置器的`--check`均已驗證；原reader產生函式不改，81／119／131／75等頁數與既有資料維持。正式Pages仍直接發布已提交靜態檔，不引入新的伺服器、Node依賴或部署工作流程。

## robots、sitemap與索引界線

基準版本沒有robots.txt或其他站主爬蟲／訓練限制，15個導讀沒有noindex。新增 `User-agent: *`／`Allow: /` 保持既有公開存取政策，明列Sitemap網址。Googlebot、Bingbot、OAI-SearchBot可抓取；沒有自行新增GPTBot等訓練爬蟲限制，也沒有以允許搜尋為理由覆蓋未來的獨立訓練政策。套用程式保留robots原有規則與其他sitemap，只補齊本站Sitemap行。

sitemap.xml精確15個正式canonical；不列重複index.html、book閱讀器、Google驗證檔、原經錨點、查詢參數或舊網域。未填lastmod。所有閱讀器的既有robots／noindex及獨立標題原封不動，沒有將reader全部canonical到導讀。

## 分享預覽與結構化資料

15頁OG及Twitter title／description／URL對齊SEO文案。sharing-images.json只列repository中原有的真實插圖與其相對檔案路徑，轉為正式絕對URL；未新增／重繪／修改圖片。六處使用既存six-senses/cover.webp，沒有拿data URI作og:image。首頁沿用系列四聖諦足印插圖作分享預覽，alt明示其主題。分享圖皆已本機HTTP200及圖片解碼驗證，正式URL另於發布驗收核對。

JSON-LD僅提供可核對的WebSite（首頁）及WebPage（15頁），不加入VideoObject、FAQ、虛構作者、上傳日期、內容修改日期或修行效果保證。VideoObject的影片日期等資料不在本包，留待後續資料齊全時處理；llms.txt不在本批。

## Google驗證原檔與分工

`googlee0c995331ec518ae.html` 放在repository根目錄，與index.html同層。原件53bytes，SHA-256 `05359eab14af74d4d9e757d4c4c179ee57c1c455986e09c0bebbdee637f86225`；直接複製附件，不改檔名／文字／換行，不製成模板、不放入docs。site-verification.json只記錄檔名、大小與雜湊，build-seo.py會驗證原件並在缺失或被改動時失敗，絕不自動以示意值重建。後續更新不可刪除該根目錄原檔。

正式URL：https://sutra-zen.github.io/googlee0c995331ec518ae.html

Codex完成網站設定及檔案發布；vidIQ影片說明、Notion維護、Google帳戶／Search Console內的「驗證／提交sitemap」及成效追蹤由原ChatGPT對話處理。檔案可公開讀取不代表已在Search Console按下驗證，也不等於Google已收錄。

## 已執行的檢查

15頁head值及唯一性、逐頁body原始位元組／H1／非SEO head樣式及程式不變，14本書架／32個節點保留，四正勤PR54標題與來源JSON保留，sitemap XML及精確網址集合、robots多組規則保留與冪等性、Google原件雜湊、14張既有分享圖本機HTTP／解碼、四個guide重建輸出與已提交HTML一致。四個reader生成函式AST未變、既有四建置器--check通過。15頁亦以本機HTTP在Chromium核對title／description／canonical與原H1，沒有JS或本機HTTP錯誤。

此輪只有head與搜尋設定變更，沒有重跑所有繪本每頁的操作。Chromium測試的首頁Tailwind／Lucide使用既存下載副本，影片iframe未測播放；實體Safari及Google收錄成效未測。正式站精確mergeSHA的Pages與18個必要網址／分享圖驗收結果見本次PR。
