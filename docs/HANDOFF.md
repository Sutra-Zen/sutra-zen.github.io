# 第12本《四禪》實作與審閱（2026-11-18）

從最新main `c4e6670d30416b4203767287cf14cd754dea8dd7` 建立 `feat/four-jhanas-review`。作者本次要求製作與驗證，尚未明確授權新書發布；**勿自行合併main或部署，也勿沿用前一本四如意足的發布授權。**

- 新增 `four-jhanas/` 主題專頁、`four-jhanas/book/` 閱讀器；在本分支接上書架第12本及原有四禪地圖節點。14支影片不變，12本可讀、2本鎖定僅屬此分支。
- 作者ZIP的15份原檔完整存 `docs/four-jhanas/`；CRC、SHA256SUMS、11圖尺寸／解碼核對。10幕、P001–P130字串與時間完整保留，另接片尾出處與共同經典依據結語，共132頁、10幕目錄。
- S08使用9A373B0F-ECD4-4060-971F-47B1ED7DDFEF.jpeg，S09使用3A1C9428-025F-40E8-8A5C-0E400BAE3862.jpeg；已目視確認第四禪第三格「捨淨念、一心」。不帶入兩張停用舊圖，原圖不改，網頁使用同尺寸WebP。
- 沿用安那般那的上方字幕／完整原圖／下方經文、目錄、讀經視窗、放大、橫直式控制與末頁重讀；共用元件不改。7條圖內疊字以圖片左上百分比與cqw定位。S01由戒生定位於右下；S02原建議壓到窗框，調至y45.2%、1.8cqw，落於窗下貓額上方，詳見overlay-layout與REVIEW。原圖牌字不重疊。
- 四禪各幕四直欄依【第幾格】採既有76%遮黑聚焦，總覽收束回全幅，放大旋轉同步；不拆裁原圖。S10完整表格外另提供可選取HTML文字表，圖外口白與原經不混用。
- Q01–Q08原文分段從JSON逐筆提取，定義／第四格譬喻依段切換。前五幕不補造Q卡，僅列經名與主題連到導讀。已讀官方固定版DN2莊春江中譯、SA483古漢譯，導讀有戒／護根／正念正知／知足／五蓋與四禪的分類節錄；來源、SHA、比對與斷句差異獨立保存。
- 其他舊書資料與原圖均不改；驗證器逐檔比較既有十一書、共用CSS／JS及Pages設定。完整檢查／PDF與橫直式截圖見 `docs/previews/four-jhanas/README.md`；實體Safari、外部影片播放及音軌逐字聽校未測。時間約1–3秒誤差，不冒稱精準字幕。
- 本次沒有公開互動預覽主機，交付PDF、截圖及已驗證的本機HTTP試閱方式。Notion未讀寫；原始交接不依賴外部Notion。
- 實測360×800、800×360、768×1024、1024×768、1440×900全132頁，共660頁面狀態、35放大字框與20分格放大狀態通過，無本機HTTP／JS錯誤。逐段字串／時間／Q配對、原圖比例、疊字座標、來源往返、翻頁／目錄／重載旋轉保留頁碼／快速按鍵／末頁重讀／書架及地圖／舊十一書入口通過；25頁PDF的130段字幕及8筆完整引文全文核對通過。

---

# 四如意足公開經文與內部註記整理（2026-11-17）

依作者對已發布繪本的修正指示，從main `97dc5fb6496accbcae16fa8f1c02fb64cc5e70ca` 建立 `fix/iddhipada-scripture-copy`，承接本書發布後的文字修正。

- S08四頁的公開Q09直接使用已核對SN51.11〈以前經〉莊春江中譯漏盡段；標示經名及譯者，移除「影片下緣摘錄」與轉錄／譯者未定／神通比較等作者說明。原交接與影片錄文仍保留，不把它們冒署名為莊春江。
- S03–S05的精進定、心定、觀定移除提到Q03的內部對照句，其餘譯意與經文不動。原始P／Q編號仍供程式配對，不作讀者介面文案。
- 修訂獨立存 `docs/iddhipada/reader-edits.json`，建置器、閱讀器與校稿PDF同步使用；原30份交接檔、9張圖、81段口白／時間／頁碼、13疊字、11卡配對及操作不改。空的作者說明不產生空白段落；閱讀器資料／程式快取更新。
- 生成一致性、原檔雜湊、既有瀏覽器驗收及PDF全文核對結果見本次PR；圖上字幕／圖下經文、橫直式按鍵、來源往返維持既有方式。實體Safari與外部影片播放未另行驗收。
- 發布後核對實際Pages建置、公開閱讀器資料及快取版本，並提供固定合併SHA的完整ZIP。此環境未提供Notion工具，尚未寫入；待補記 `docs/releases/iddhipada-scripture-copy-notion.md`。

---

# 第11本《四如意足》發布授權（2026-11-16）

作者於交付審閱版後明確指示「直接發布吧」。**此授權取代下方本書原審閱限制，允許將PR #34合併至main並發布GitHub Pages。** main仍以 `140f62221726485916f3992d8ea6f5782e7507b5` 為基準，發布同一審閱內容；只移除導讀／閱讀器noindex及試閱標示、改用正式快取版號，不改9幕、81段口白、11筆Q卡、13條疊字、原圖或既有十本。

- 正式導讀：https://rooneyflower-star.github.io/sutrazen-map/iddhipada/
- 正式繪本：https://rooneyflower-star.github.io/sutrazen-map/iddhipada/book/
- 發布經 [PR #34](https://github.com/rooneyflower-star/sutrazen-map/pull/34)；實際合併SHA、Pages建置／公開檔案核對與固定合併SHA的完整ZIP，記錄於PR最終發布驗證。不以先前審閱ZIP代替正式備份。
- 審閱版已通過五尺寸410個頁面狀態、65個放大字框狀態及舊十本入口檢查；發布前重核原檔／資料生成／JS語法／相對連結與原書不變。實體Safari手勢、影片播放、時間精校及來源措辭差異仍保留REVIEW_TODO，發布不等於這些項目已完成校勘。
- 此工作環境未提供Notion工具，尚未寫入改版頁；待補記 `docs/releases/iddhipada-notion.md`。

---

# 第11本《四如意足》審閱實作（2026-11-16）

最新main基準 `140f62221726485916f3992d8ea6f5782e7507b5`，實作分支 `feat/iddhipada-review`，[草稿PR #34](https://github.com/rooneyflower-star/sutrazen-map/pull/34)。**本次使用者明確要求審閱，不合併main、不公開部署。先前各書發布授權不適用本次。**

- 新增 `iddhipada/` 導讀及 `iddhipada/book/` 閱讀器；審閱分支接書架第11本、原有四如意足地圖節點。14個影片不變，11本可讀、3本鎖定。沒有新增重複地圖節點。
- 兩包普通ZIP完整合併於 `docs/iddhipada/`，30原始檔符合receipt與manifest；9正式PNG、1有字備用、9定位影格均解碼。網站用9張同尺寸WebP，原圖與交接JSON不改，無MOV上站。
- 9幕、81段口白、P01–P81／時間／Q對應完整保留；另加既有格式的經典依據結語，82頁、9幕目錄。11經文卡按段重用，Q01–08中文譯意不冒名莊春江，Q09影片錄文譯者未定，Q10–11古漢譯。導讀另用5份官方來源核對的中譯／古漢譯節錄與4份巴利對照。
- 沿用最新安那般那的字幕在上／全幅圖／經文在下、共享reader-controls／reader-restart、目錄、頁碼、經文視窗、放大與橫直按鍵。13條疊字以圖片左上百分比及cqw定位；8個字框避讓人物／燈，初值與調整記錄分開。S06正式無字版加4條教學字，原圖帆字不重疊。
- 實測360×800、800×360、768×1024、1024×768、1440×900全82頁，共410狀態，65個放大字框狀態；翻頁、目錄、長文捲動、兩卡切換、來源往返、導讀／地圖返回、快速翻頁、旋轉重載保留頁碼、最後頁重讀及舊十本入口通過。十本舊書、共用檔與Pages設定逐檔不變。實體Safari、外站頁面及YouTube播放未測。
- 試閱與截圖：`docs/previews/iddhipada/README.md`；另提供完整可選字PDF（81段及11卡逐字檢查）。互動試閱用本機HTTP；不將GitHub檔案頁、PDF或不存在的正式路徑冒充互動預覽。
- `docs/iddhipada/REVIEW_TODO.md` 保留時間精校、巴利拼寫、Q09譯者及公園／精舍、依出要等差異；原口白／引用不擅改。來源固定commit與SHA在verified-sources。此工作環境未提供Notion工具，尚未寫入；待補記 `docs/iddhipada/notion-review-note.md`。

---

# 移除原經區說明句（2026-11-16）

依作者要求，移除安那般那專頁閱讀原經區的白話詮釋／影片錄文／版本對讀說明句，其他內容與連結不變；承接發布授權。生成一致性與差異檢查通過。Notion工具未提供，尚未寫入；待補記：docs/releases/anapana-source-intro-notion.md。

---

# 移除閱讀器與專頁的多餘說明（2026-11-16）

依作者對已發布繪本的文字整理指示，從main `444df223dd9bdb47a1e4e914ee27d28aa2f73fed` 建立 `fix/anapana-reader-labels`，承接本書發布修正授權。

- 第09幕六頁不再顯示「論師實修手記是本片創作名稱／不是真實古籍」或「無下緣經文／影片自撰轉場」；此幕沒有引文，公開資料的context／sourceNote設為null，整個空白經文帶隱藏，不留下空框。
- 金剛寺本閱讀器來源名稱統一為《安般守意經》金剛寺本，移除（論文轉引）與（止息段補訂）；專頁同卡簡化為「金剛寺本引文」。來源的論文書目、PDF、版本介紹與所有引文原字不改。
- 移除專頁論師來源區的「創作卷軸／S09轉場／以下兩組來源」整段，保留論師來源區標題及兩張來源卡。JS不再插入創作名稱解說，資料建置與快取版本同步更新，避免重建或瀏覽器快取恢復舊標示。
- 118段口白、119頁、全部引文（含止息末兩句）、原圖、來源連結及操作不變。原交接、PDF／XML與核對狀態仍保留於內部文件及metadata，不因公開標示簡化而更動原始證據。
- 已以四尺寸360×800、800×360、768×1024、1024×768核對S09六頁及S11十二頁，共72個狀態：指定文字不見、S09無空白經文框、無水平溢出、字幕與經文沒有遮圖、目錄／旋轉／對話窗與來源往返正常。逐筆比較所有原口白及引文不變，另外七張來源卡不變，既有static_checks及生成／JS語法檢查通過。截圖與結果見docs/previews/anapana-reader-labels/；實體Safari未測。

此工作環境未提供Notion工具，尚未寫入；待補記為docs/releases/anapana-reader-labels-notion.md。發布後核對Pages、公開導讀／閱讀器及兩個JS快取版本，提供固定合併SHA完整ZIP。

---

# 論師引文同步到導讀與閱讀器（2026-11-16）

依作者最新指示，從main `6d52462ac661c055d702c3e31172a5b8720f4347` 建立 `fix/anapana-commentary-reader`，承接本書已發布內容的修正授權。本節取代先前「來源卡修訂而閱讀器保留影片摘引」的公開呈現規則；原始交接JSON及影片錄文檔仍原樣保存，便於追溯。

- 導讀修次卡第一行加「蓮花戒大師」，下方保留《菩提道次第廣論》卷十四引述／宗喀巴大師造／法尊法師譯，區分修次作者與廣論轉引者。
- 止息段使用作者這次提供的全文，包含原字「爲」、標點與「何用是止？但欲從是止念。」末兩句。metadata保留PDF原節錄，標明止息全文為作者補訂，並以「論文轉引／止息段補訂」區分；不假稱附件原段逐字包含補句。
- 公開閱讀器S10的Q32–Q38以CBETA廣論引文更新（包括「自鼻至臍」），來源明列蓮花戒與廣論引述；S11的Q39–Q40改用附件論文的數／隨引文（投二／莫投二），Q41使用作者補訂的止息全文。來源返回仍為Q32–Q41錨點，連到對應CBETA原文卡／PDF與版本介紹卡。
- verified-sources.json之commentarialSources作為兩介面的共同資料。build-anapana.py同時產生導讀兩張卡與閱讀器10組論師引文；修次依原口白的部位對應分成7組，沒有改動敘事順序。--check同時檢查導讀與book-data，防止只更新一邊。book-data的快取版本已更新。
- 118段口白、119頁／12幕、11張原圖與12條疊字、原始交接38檔及九本舊書完整保留；Q01–Q31內容保持原樣。只有S10／S11共26頁的下緣論師引文與來源標示更新，翻頁與版型不變。
- 既有驗證器已分開核對原始錄文與公開修訂內容，並以導讀全文重組修次7組、比對數／隨／止三段及作者完整止文，避免缺句。五尺寸595逐頁狀態、24個放大標籤狀態、舊九本入口與共用按鍵座標均通過。另四尺寸共8次專門核對Q35／Q41下緣文字、本頁經文對話窗及來源往返保留第99／114頁。新截圖與驗證見docs/previews/anapana-commentary/；實體Safari未測。

此工作環境未提供Notion工具，尚未寫入；待補記在docs/releases/anapana-commentary-notion.md。發布後應核對Pages與公開導讀／book-data／快取版本，並提供固定合併SHA完整ZIP備份。

---

# 金剛寺本來源卡改用附件論文轉引（2026-11-16）

依作者對已發布網站的來源修正指示，從main `1d16a34267e7ecbaf73543cab4580d32739bd67c` 建立 `fix/anapana-kongoji-source`，承接本書發布授權。只更新安那般那導讀的anban來源卡，不再使用影片摘引或出處截圖附錄。兩個按鈕沿用現有樣式：閱讀論文PDF（附件原檔、定位PDF第130頁）與版本介紹（作者提供的維基百科網址）。Q39–Q41來源錨點保留，三段數／隨／止引文直接顯示。

附件212202.pdf是鄧翠盈（釋妙博）2008年佛光大學宗教學系碩士論文《漢魏晉中國佛教安般禪觀─以〈安般守意經〉為中心》，共167頁；不是金剛寺抄本原件。已讀封面、相關章節及註396／403／407，並實際渲染核對PDF第130–133頁（論文頁122–125）。來源卡清楚標示論文轉引，不把維基百科當原經，也不拿大正藏本比較欄或作者解說混作金剛寺引文。原PDF完整存references/212202.pdf，SHA-256為6b8a5905f14894cad909b3bbe5d96a41be4b987cee32854478cc7f61c546d674；節錄與頁碼、文字處理規則存verified-sources.json之commentarialSources/anban。

節錄只去除PDF排版空白，以Unicode NFC處理相容漢字，保留「无」「出息至竟投二」「出息至竟當隨莫投二」「遍止鼻頭」與論文標點；不接上論文此段沒有的舊影片末句。原119頁閱讀器／41筆影片錄文仍保存，不以來源卡修正暗改原故事；差異記錄於REVIEW_TODO與來源metadata，若日後改閱讀器需另按作者指示處理。

維基百科外站請求受環境代理403限制，按作者提供網址保留，未引用未讀文章的內容。其餘七張來源卡（含前次CBETA卡）、原始38份交接、插畫、書架／地圖、九本舊書與共用元件不變。已於360×800、768×1024、1024×768驗證三段直接可讀、無水平溢出、PDF新視窗定位#page=130、Q39來源往返保留第107頁；本地PDF HTTP200且原檔雜湊相符，其他七卡不變，既有static_checks通過。檢查器增加PDF頁碼驗證，避免把#page=130誤當HTML錨點。截圖／結果見docs/previews/anapana-kongoji/；實體Safari未測。此工作環境未提供Notion工具，尚未寫入；待補記在docs/releases/anapana-kongoji-notion.md。發布時須核對Pages、公開PDF與來源卡，並提供固定合併SHA完整ZIP備份。

---

# 安那般那調身八法改用CBETA原文（2026-11-16）

依作者對已發布網站的修正指示，從main `e95d873c3f9816cb54701f173640f5ea66b2eba3` 建立 `fix/anapana-cbeta-source`，承接本書的發布授權。只修改導讀的《修次中編／下編》來源卡：使用作者指定CBETA網址與完整引文，移除該卡「閱讀對應段落／對照出處截圖」的附錄入口，改成同樣式的「閱讀原文」按鈕與直接顯示的「原文節錄」。Q32–Q38來源錨點保留。這是《菩提道次第廣論》卷十四引述中／下編，明列宗喀巴造／法尊譯，不冒充已各別校勘兩編原本。

CBETA網頁直接請求受代理403限制，網址按作者提供保留；已改讀CBETA官方xml-p5a固定版本 `741971afbbf665797e874443cd8b4746ee4487da` 的B/B10/B10n0067.xml，核對段落pB10p0718a2401（0718a24–0718b03）的完整引文，僅忽略XML換行空白，文字與作者所貼完全相符。原檔存canonical/B10n0067.xml，雜湊／出處／譯者及節錄存verified-sources.json的commentarialSources。

閱讀器119頁、原始交接38檔、11張插畫、41筆影片錄文、其餘七張來源卡與其它九本不改動；原圖／來源影格檔保留追溯。SOURCE_NOTES原檔不改，REVIEW_TODO補記此來源卡已更新。此環境仍未提供Notion工具，尚未寫入；待補記在docs/releases/anapana-cbeta-notion.md。已於360×800、768×1024、1024×768驗證完整引文直接顯示、指定網址、無水平溢出及S10的Q32來源往返保留第93頁；其他七張來源卡逐位元組相同，既有static_checks通過。截圖／結果見docs/previews/anapana-cbeta/。實體Safari與CBETA外站畫面未測。發布後核對Pages、公開檔案與固定合併SHA完整ZIP。

---

# 第10本發布授權（2026-11-16）

作者於審閱實作交付後明確指示「直接發佈」，取代下方歷史審閱限制。以PR #28發布《安那般那與止觀》；不改動已驗證的119頁、原始交接與其它九本。移除新專頁／閱讀器的試閱noindex及導讀標題中的試閱字樣，快取版本改為正式標記。

發布完成必須核對實際合併SHA、GitHub Pages build成功及公開首頁／導讀／閱讀器／圖片檔案，並下載固定合併SHA完整ZIP核對CRC及追蹤檔案。以下595個頁面狀態為同一套內容與互動的發布前驗收，不代表實體Safari驗收。正式入口為 https://rooneyflower-star.github.io/sutrazen-map/anapana/ 與 /anapana/book/；成功與否以發布回報及PR #28最終驗證記錄為準。

本環境工具清單仍無Notion搜尋／讀取／更新工具，尚未寫入改版頁。待補記文字為 `docs/releases/anapana-notion.md`；不得稱為已補記。來源疑點仍保留REVIEW_TODO，不因作者授權發布而自行改寫引文。

---

# 第10本《安那般那與止觀》審閱實作（2026-11-16）

**本次作者只授權審閱實作，不合併main、不部署正式站。** 從最新main `0034db754a478bbce76c79b0dbe7479822dfee76` 建立 `feat/anapana-review`，以draft PR交付。GitHub Pages仍為main根目錄，書架第10本只在本分支開放，正式站不變。

- 已讀AGENTS、PROJECT、HANDOFF、SOURCES及兩包交接README／STORYBOARD／OVERLAY_SPEC／SOURCE_NOTES／完整storyboard、catalog、overlays與來源快照。兩包是互補普通ZIP，合併後38份原檔保存在 `docs/anapana/`，兩包CRC、38檔大小／SHA-256、27張圖像的尺寸／解碼均通過；含11張正式PNG、16張參考影格與出處相關圖，無缺件、無重繪。`receipt.json`記錄原始接收，`asset-manifest.json`保持原樣。
- `anapana/`主題導讀及 `anapana/book/`閱讀器接上第10本、既有安那般那地圖窗與來源入口。14本中10本可讀、4本鎖定（僅審閱分支）。沿用既有影片 `QzAUik0ePm8`，不依賴影片即可完整閱讀；首頁所有14支影片及既有地圖資料鍵不變。
- 使用最新四正勤已修正的「上方字幕、完整插畫、下方經文」與既有按鍵／目錄／頁碼／本頁經文視窗／來源返回／圖片放大／最後頁重讀。共用reader-controls.css與reader-restart.js未修改。118段完整口白各一頁，加S12既定可選取總覽，共119頁、12幕。經文依各段quoteIds配對，41筆影片錄文不改寫，來源與引文預設顯示，長文可捲動。sourceNote在引文卡外獨立標示；S09無下緣引文不猜配，S09–11明標論師補充。
- 只加overlays.json的12條字，以完整原圖及外框為基準，左上錨定百分比／cqw，沒有translate置中。座標及字色／字級沿用初值，對照原圖／影格核對，未聲稱精準還原其它影片座標。S03短名、S04–07下緣標題、S10第三格三提示保留；原圖文字不重疊加字，不拆裁四格。圖寬低於600px時S10小字改為圖外由左至右一行，放大圖恢復全部三條圖內標籤。11份WebP副本保持原尺寸，原PNG不變。
- 導讀沿用共同header／guide-ui及原經卡：六份官方sc-data固定版本的SA801、802、803、464、560、MN118已實際讀取及再次驗證SHA；原檔與節錄保存在canonical/及verified-sources.json。MN118提供具名莊春江中譯及巴利入口，影片譯文不冒署譯者。修次中／下編與安般守意經金剛寺版另設兩張論師補充卡，提供相應段落與原出處截圖，版本尚未覆核。「論師實修手記」明列為創作卷軸名稱；沒有新增SN54.1。
- S12保留五組完整文字與四列十六勝行表，心悅／心定與原圖令心喜／令心攝刻意對照。共同阿含依據及「解讀仍請以原經文為準／走入經藏的起點」閱讀說明另標為編輯文字，不算入118段影片口白，不含「溫柔」。
- `python3 scripts/check-anapana.py --screenshots --verify-sources`：360×800、800×360、768×1024、1024×768、1440×900，共595個逐頁狀態通過，核對文字／引文配對／疊字座標字級、未裁圖比例、字幕在上經文在下及無水平溢出。另測12幕目錄、前後翻頁、長經文捲動／對話窗、來源往返、回導讀與地圖、放大關閉、S10旋轉切換、快速點按scale=1、重載／旋轉保留精確頁碼及末頁重讀。共用按鍵位置與第09本相差小於1px。首頁書架／原地圖節點及九本舊書入口／下一頁／返回均通過；舊書全目錄、共用檔案及Pages設定逐位元組對照基準不變。JS語法與新增程式／編輯文件的空白檢查通過；兩份原交接OVERLAY_SPEC／SOURCE_NOTES的尾空行原樣保留，不為格式檢查改動原檔，無本地HTTP或JS錯誤。
- 試閱方法、橫直式各幕截圖與validation.json見 `docs/previews/anapana/`。本環境無託管試閱工具，未捏造公開試閱網址；完整分支ZIP解壓後以本機HTTP伺服器開啟anapana/index.html或anapana/book/index.html，可於同一區網供iPad測試。管理瀏覽器禁止file://，未宣稱直接雙擊或iPad檔案預覽可執行完整閱讀器。實體iPad Safari手勢、外站註解畫面與YouTube實際播放未測。
- 原SOURCE_NOTES全部保留，異文／版本問題另見 `docs/anapana/REVIEW_TODO.md` 與source-comparison.json。Q01經號／用字、803短列與影片展開句、MN118影片譯句、修次版本及金剛寺本的字形仍待作者確認，不自行修訂故事或經義。
- 目前工具清單沒有Notion搜尋、讀取或更新功能；未讀寫外部Notion頁面，已利用包內NOTION_SNAPSHOT完成交接，不影響實作。此次未發布，未把審閱版稱為正式發布或正式版備份。

---

# 四正勤字幕位置統一與住法經註解定位（2026-11-15）

從main `d85447988322c00c1428f9c1f69f3f65d4e29e32` 建立fix/right-effort-caption-layout。依作者最新指示，恢復與其他繪本相同的「上方字幕、完整插畫、下方經文」，取代舊交接及前次實作的圖下口白要求；後續不得再依舊交接將字幕移回圖下。

將caption DOM順序及橫式圖片保留空間恢復為最近四念處的配置，移除第09本原有的圖下字幕覆寫。翻頁、目錄、本頁經文、來源、圖片放大、重讀及S03／S07逐格遮黑保留；81頁口白／引文與11幕對應均不變，book-data僅更新layout描述。原圖、原始交接、書架、其他八本及共用檔案不變。

住法經註解按鈕使用作者提供的完整九五／穢品住法經第九定位URL，專頁與verified-sources.json同步；網址的依據為作者提供，不假稱外站畫面已驗證。來源說明見SOURCES最新紀錄。

check-right-effort.py更新驗收方向，重新檢查五尺寸405個逐頁狀態，量測所有故事頁caption底端不超過圖片頂端、圖片底端不超過經文頂端；另重驗四尺寸68個漫畫段落的實際亮／暗像素、放大與旋轉對齊。截圖更新於docs/previews/right-effort/及right-effort-focus/。實體Safari仍未測；發布需核對Pages、公開檔案及固定SHA完整ZIP。

此工作環境未提供Notion工具，尚未寫入；待補記：docs/releases/right-effort-caption-notion.md。

---

# 四正勤漫畫逐格遮黑（2026-11-15）

從main `3d9830eb65877547e6c272eb8466a816411e0baa` 建立fix/right-effort-comic-focus，依作者對已發布繪本的指示補上漫畫閱讀提示，承接本書發布授權。

- 共用既有picture-panel-focus.js／css，未修改共用檔案。新書panel-focus-data.js記錄原圖分格邊界與每段口白的亮格；四格／六格的非閱讀格使用與舊書相同的76%暗色，閱讀格保留原亮度。
- S03第1–2段總覽，第3／4／5／6段依序亮生欲／方便／精勤／心攝受，第7–8段收束顯示全圖。S07第1段總覽，第2段亮第1格，第3–4段第2格，第5段第3格，第6–7段第4格，第8段第5格，第9段第6格。
- 依原圖白色分隔線量取邊界：四格以1672×941圖的x=784、y=443分割；六格x=553／1116、y=467。遮罩以實際完整圖片範圍定位，旋轉與放大視窗同步，無指標事件、不遮住翻頁操作。圖片替代文字提示目前閱讀的格位。
- 這次作者要求覆蓋原交接「其他幕無遮罩」的漫畫展示方式；只有S03／S07增逐格遮黑，S10原60%總結暗幕保留。所有原圖、原始交接、81頁完整口白／引文、書架、專頁及共用檔案保持不變。
- 原check-right-effort.py的405個逐頁狀態及舊八本入口通過；另check-right-effort-focus.py在360×800、800×360、768×1024、1024×768核對共68個漫畫段落狀態。實際截圖像素驗證亮格不變、暗格76%混色，並測試前後翻頁、總覽／離幕清除、放大及旋轉對齊、末頁重讀。截圖與結果見docs/previews/right-effort-focus/；實體Safari未測。
- Notion工具未提供，尚未寫入；待補記見docs/releases/right-effort-focus-notion.md。發布後仍須核對合併SHA、Pages成功與固定SHA完整ZIP。

---

# 第09本《四正勤》（2026-11-15）

從最新main `cd1cb6f743d773afe9ea22c6c548384c7760ef75` 建立feat/right-effort，[PR #25](https://github.com/rooneyflower-star/sutrazen-map/pull/25)。已讀AGENTS、PROJECT、HANDOFF、SOURCES、完整兩包交接README／CODEX_PROMPT／NARRATION_REVIEW／SOURCE_NOTES／storyboard／catalog／manifest，並檢查最近四念處的實際實作。作者本次明確授權直接發布。

- 兩包已安全合併至docs/right-effort/；33項清單檔案的大小與SHA-256、26張圖像解碼與尺寸核對通過，無缺件。原JSON、9張正式圖、2張備用圖、14張參考影格／出處圖及片尾影格完整保留。Notion匯出只供追溯，不依賴外部Notion媒體。
- `right-effort/`導讀與`right-effort/book/`閱讀器接上書架09及原有四正勤心智圖窗；14本中9可讀、5鎖定。沿用原#video-09的RqWhPhhP8eY；全部14支影片不變。
- 沿用最新四念處的翻頁／目錄／頁碼／本頁經文／來源返回／圖片放大／重讀及共用reader-controls.css、reader-restart.js；本次作者明確要求圖下口白及經文，故只在新書將文字帶放到完整圖片之下，取代專案一般的上方字幕位置，沒有修改舊書或另做側欄。
- 11幕、80段完整口白依次逐頁顯示，再接S11原片尾閱讀說明，共81頁。13筆引文逐段配對，S02 Q02→Q03、S04 Q05→Q06→Q05、S05 Q07→Q08→Q07、S06 Q09→Q10→Q09明確核對；S10原片無下緣引文，不額外猜配。
- 5組artOverlay（含S10四行）照leftPct／topPct／widthPct／fontSizeCqw，以未裁切圖片左上定位、居中對齊、無translate。原圖已有的六根、四格、六格文字保留且不另加標籤。只有S10有0.6暗幕；圖片及標籤在放大視窗亦保持比例。與交接影格並列核對位置。
- 導讀沿用共同header／guide-ui、封面、影片及6張原經來源卡。官方sc-data固定版本的SA877、879、254、MA95、SN49.1–12、49.23–34已實際讀取與重新核對雜湊，原檔及節錄見verified-sources.json／canonical/。SA877／879經名依交接更正。Q12影片未標經號，公開經名不加猜測數字；所讀MA95選文與卷23相符，故提供其原典連結。合刊資料沒有全部配入各幕。
- 影片錄文不自動改寫，異文與S07／08詮釋留REVIEW_TODO。S11原片只稱阿含，另附相應部依據及「解讀仍請以原經文為準」編輯說明；末句依作者既有指示移除「溫柔」，原textCard與end.jpg不變。未把編輯說明計入80段口白。
- `python scripts/check-right-effort.py --screenshots --verify-sources`：360×800、800×360、768×1024、1024×768、1440×900，共405個逐頁狀態通過。全部口白／引文／切換、圖片比例／標籤座標／遮罩、文字在圖下及無遮圖、無水平溢出、控制位置與四念處相同、目錄、翻頁、快速點按、經文視窗／捲動／來源、放大、旋轉／重載／返回保留頁碼、末頁重讀及八本舊入口通過。舊八本、共用檔案及Pages設定與基準逐位元組相同。
- 截圖及驗證見docs/previews/right-effort/；實體iPad Safari、外部影片及註解站畫面尚未驗證。發布後應確認實際合併SHA與Pages及正式檔案，提供固定SHA完整ZIP，不以push成功代替部署成功。
- 此工作環境未提供Notion工具，尚未寫入；待補記文字在docs/releases/right-effort-notion.md。

---

# 第08本原經節錄分類與定位連結（2026-11-15）

從main `7a5ac6131d2d4e437f7686915c94f5dec7784265` 建立 `fix/mindfulness-source-excerpts`。依作者指示，移除專頁最後的「影片引文來源影格」卡，保留研究論文PDF／DOI及repository內全部原始影格，並將影格用途記入 `docs/releases/mindfulness-excerpts-notion.md`。此環境未提供Notion工具，尚未寫入。

中阿含98經改為觀身、觀受、觀心、觀法四類，共11段可直接閱讀的節錄：行住坐臥、呼吸、不淨、六界、死屍觀；三受、身心／食無食／欲無欲、內外觀受；如實知心／內外觀心；五蓋、七覺支。新增節錄皆從已核官方固定版本原檔截取，保留髦／膽、碎粖、調悔等原檔文字，沒有改動繪本影片錄文。分類及扁平節錄清單同步記入verified-sources.json。

MA98、MA102註解按鈕照作者提供的完整百分比編碼URL更新，可定位該經；不再只用卷頁。網址見verified-sources.json。其餘來源卡、繪本111頁、書架、舊七本、共用檔案與Pages設定保持不變。手機360、iPad768直向及1024橫向核對分類、節錄、連結、無水平溢出與繪本來源往返；原典節錄包含關係及原始91檔雜湊檢查通過。驗證與截圖見docs/previews/mindfulness-excerpts/。發布仍須核對合併SHA、Pages及完整ZIP。

---

# 第08本介面統一與阿含經結語（2026-11-15）

依作者對已發布版本的回饋，從最新main `1d964bbd8d6c9d0c05aa725f36da1b44d8ffb078` 建立 `fix/mindfulness-consistent-reader`，[PR #23](https://github.com/rooneyflower-star/sutrazen-map/pull/23)，修正本書導讀／閱讀器，承接本次網站直接發布授權。以下取代初版的整幕側欄閱讀方式；原始交接與下方歷史紀錄保留。

- 閱讀器採用第06／07本的實際HTML與CSS結構：上方字幕、完整插畫、下方經文；手機底部按鍵、橫式左右按鍵、右上目錄與頁碼、本頁經文視窗及閱讀原經入口均相同，不再使用整幕側欄或另一組常駐工具列。完整92段口白按原標點分頁，逐段拼接與原文相同，共109張字幕頁＋既定S25總結＋製作說明＝111頁。
- 25幕、圖片對應、18筆影片錄文、27組段落對應及圖片百分比標籤不變。每頁顯示所屬段落的下緣經文；S10前後兩組不混用，S18補充／S20承接仍明標。手機經文可直接捲動，橫式可開啟與舊書相同的本頁經文視窗。點選插畫可放大，沒有另一組常駐放大／全螢幕按鈕。
- 新增最後一頁共同製作說明，列實際依據的中阿含念處經、念經、雜阿含、增壹阿含及增支部顛倒經，包含「解讀仍請以原經文為準」與「走入經藏的起點」，不含「溫柔」。末頁沿用回到第一頁。
- 導讀把作者提供的四段總結潤稿為觀身／觀受／觀心／觀法四段，分別說明對治淨、樂、常、我顛倒，未把詮釋當成新的經文引句。
- 原經區改為舊書相同的7張來源卡：經名、版本／莊春江中譯、漢譯或中譯經文按鈕、註解或巴利對照按鈕、同一組圖示及供應者文字，節錄直接顯示。18筆影片影格及論文PDF另保留為來源資料。舊Q01–Q18連結仍可到對應經卡。
- 已讀並核對7份官方sc-data原典／中譯原檔；SHA-256及導讀節錄見 `verified-sources.json`，原檔在 `canonical/`。中阿含98／102的卷24／25由CBETA XML確認。台大獅子吼外站請求仍受環境403限制，未假稱驗證服務站畫面。原影片異文另記REVIEW_TODO，未改繪本錄文或原始交接。
- `python scripts/check-mindfulness.py --screenshots --verify-sources`：360×800、800×360、768×1024、1024×768、1440×900，共555個逐頁狀態通過；實際量測翻頁按鍵與目錄位置和第07本相差小於1px。完整文字、圖片比例／標籤、無水平溢出、來源、經文視窗／捲動、快速翻頁、旋轉／重載保留精確頁碼、圖片放大及末頁重讀通過；七本舊入口正常，原七本／首頁／共用檔案／Pages設定與基準逐位元組不變。
- 截圖見 `docs/previews/mindfulness/`，包含橫直末頁與來源卡。實體iPad Safari、外部影片及註解站畫面仍未驗證。發布時核對新合併SHA、Pages成功及固定SHA ZIP，不以本機測試代替正式站驗證。
- 已把相同閱讀器結構、原經來源卡及結語要求補入AGENTS，供後續新增繪本遵循。此工作環境未提供Notion工具，尚未寫入；本次待補記：`docs/releases/mindfulness-ui-notion.md`。

---

# 第08本《四念處與四顛倒》實作與發布交接（2026-11-15）

作者在第04包訊息明確授權「收齊你就可以做專頁和繪本了，可直接發佈」，取代舊交接提示中的先試閱限制。本次從最新main `24983232d11bc9e775641bf444bcbe59055fe1ad` 的實作分支 `feat/mindfulness-preview` 完成，[PR #22](https://github.com/rooneyflower-star/sutrazen-map/pull/22)，原有七本及GitHub Pages設定保持不變。是否正式上線以PR實際合併SHA及相應Pages成功為準，交付時另提供固定SHA ZIP備份。

## 完整素材及內容

- 作者新上傳的四個分包均已安全解壓至 `docs/mindfulness/`；依 `SPLIT_MANIFEST.json` 核對91個原始檔案的大小、SHA-256，缺件為零。25張原圖（含1張備用）、全部參考影格／字幕證據及論文PDF均保留，不依賴GitHub中未傳完的舊交接分支。
- 已讀專案四份文件及v3交接README、CODEX_PROMPT、NARRATION_REVIEW、SCRIPTURE_REVIEW、完整storyboard、經文目錄與素材清單。v3的25幕、18筆經文及27組段落對應相符。
- `mindfulness/` 導讀和 `mindfulness/book/` 閱讀器接上首頁書架第08本，以及原有「四念處」「四顛倒」心智圖視窗；書架14本中8可讀、6鎖定。既有14支影片ID全部保留，新導讀沿用現有#video-08影片 `EQjXvgt5OOA`。
- 25幕依JSON順序配圖，S01–S24共92段完整口白，不以webCopy取代。S25只顯示既定四行總結，沒有把原稿的實作提示當作原片口白。所有來源插畫使用repository相對路徑，不重新生成、轉Base64或裁切。
- S03採指定車站；S18刺藤／水果與S21刺藤／蓮花各用指定圖。原圖文字不重疊加字；artOverlay使用原圖左上角百分比及cqw字級，以實際圖片框定位，並以交接影格核對。小螢幕可讀圖外標籤文字、放大原圖；S25在圖片不足900px寬時用完整文字卡。
- 口白與經文分層且可選取。18筆經文按27組對應直接顯示在相應段落組後；S15／S16同段引文各合併顯示一次但保留3組段落範圍。S10第1、2段配Q05，第3、4段配Q06；S18補充對照Q15及S20承接Q13明標關係。原片無引文的頁面沒有自行配經。校稿note與reviewNote只留在原始文件及獨立REVIEW_TODO。

## 介面與驗證

- 導讀沿用共同guide-header／guide-ui，右上只有回修道地圖、現有YouTube預覽、直接顯示經文來源卡；另提供身受心法章節入口、四顛倒對照、附件論文PDF／DOI及逐筆經文證據影格。
- 閱讀器沿用手機直式底部、橫式左右按鍵和右上目錄／頁碼，載入共享reader-controls.css、reader-restart.js。完整口白與直接顯示的經文置於閱讀欄，可獨立捲動；提供全螢幕、圖片放大、來源返回、末頁重讀、鍵盤、滑動及快速翻頁。旋轉／重載／來源往返保留幕號。全螢幕API不可用時採可退出的頁內模式。
- `python scripts/check-mindfulness.py --screenshots` 通過：360×800、800×360、768×1024、1024×768、1440×900，共125個逐幕狀態。核對92段口白、18筆經文／27組對應、23張實際經文卡、所有原圖比例、座標字級、無水平溢出，以及翻頁／目錄／縮放／全螢幕與備援／來源往返／旋轉／重讀。無本地HTTP或JavaScript錯誤。
- 七本既有閱讀器的開啟／下一頁／返回通過。其全部目錄、共用CSS／JS與Pages設定逐位元組對照基準main未變。首頁原有心智圖資料鍵和全部影片不變。
- 截圖及重現方法：`docs/previews/mindfulness/README.md`；逐幕疊字表：`docs/mindfulness/layout-audit.md`；自動驗證結果：`docs/previews/mindfulness/validation.json`。
- 實體iPad/Safari與外部YouTube實際播放尚未測試。首頁CDN透過系統CA驗證取得真實公開回應供Chromium測試，未停用TLS驗證。

## 待作者校稿及改版紀錄

- 原故事和影片引文保留，不把教學詮釋冒充經文。S10四大口白／六界引文、S12四諦、S15食無食、S16內外觀、S20四禪、S22星空及S23／24經名等完整提醒見 `docs/mindfulness/REVIEW_TODO.md`，原始兩份REVIEW文件亦原樣保留。
- 此工作環境未提供Notion工具，尚未寫入指定改版頁。待補記文字在 `docs/releases/mindfulness-notion.md`；不得把備妥文字稱為已寫入。

---

# 四念處交接第03包接收（2026-11-15）

第03包已合併至docs/mindfulness/，重複檔案一致；所有已到齊檔案均通過大小／SHA-256驗證，新收到圖片可正常解碼，PDF標頭正常。接收與缺件清單見receipt-status.json。仍等第04包；未修改或發布網站。

# 四念處交接第02包接收（2026-11-15）

第02包已安全合併至docs/mindfulness/，重複清單內容一致；新增插畫及全部已到齊素材通過尺寸／SHA-256核對，25幕asset路徑均已存在。詳receipt-status.json。仍等第03、04包的參考圖、論文與字幕資料；未改網站、未發布。

# 四念處交接分包接收（2026-11-15）

目前只收到第01包，已存docs/mindfulness/並核對v3、25幕、18筆經文、27組段落對應。11張插畫尺寸／SHA-256與已到齊檔案的分包清單雜湊驗證通過。接收狀態與缺件清單見receipt-status.json。分支feat/mindfulness-preview；等第02、03、04包全部合併並核對後，再完整閱讀交接稿與實作。尚未修改正式網站，不部署main。

# 第07本導讀刪除兩段製作說明（2026-11-15）

依作者指示，從導讀移除「繪本保留影片敘事…」及「第08幕影片原字幕提到…」兩段。保留原經卡、經文來源、人物釋義及全部繪本內容；核對紀錄仍留在文件中。已確認精確移除兩段及四張原經卡保留。

# 圖片對應與七本結語修正（2026-11-15）

作者已確認第07本來源圖放反：僧不壞淨S06改用IMG_0400.jpeg（合掌、象鹿與田地），聖戒成就S07改用IMG_0401.jpeg（白色光罩、望遠鏡）。原JPEG與原交接manifest保留，正式對應存image-assignments.json並由build腳本套用；章名百分比座標、字幕與經文不變。

七本最後一句統一移除「溫柔」，改為「也希望這本繪本能成為您走入經藏的起點。」；六處無JS備援文字亦同步，八正道及第06／07本的產生資料來源同步，避免重建後還原舊文。僅改指定結語，其他故事文字保留。

第07本導讀刪除作者指定的四入流分／四不壞淨及圖牌用語說明段落。原經卡與連結保留。

針對S06／S07全部27個頁面狀態於手機／iPad四尺寸驗證圖片、章名、字幕與尺寸；另驗七本末頁結語和回到第一頁功能。原圖雜湊維持。實體Safari仍未測。發布後須核對Pages及正式檔案，提供固定merge SHA ZIP；Notion待補記在docs/releases/picture-book-copy-notion.md，尚未寫入。

---

# 第07本《四不壞淨與六念》（2026-11-15）

作者本次明確授權直接上線。實作PR：https://github.com/rooneyflower-star/sutrazen-map/pull/19 。分支`feat/four-purities-six-recollections`從最新main `31ebc8679723ab9908f771436bc0563cc4b04270`建立。正式部署須核對實際合併SHA與Pages成功，不能以push成功代替。

## 完成實作

- 已讀專案四份規則與附件README、完整JSON／Markdown分鏡、manifest；附件原樣保存在`docs/four-purities-six-recollections/`。8張正式JPEG及11張參考影格／截圖的尺寸、大小、SHA-256全部相符，沒有重新生成或嵌入Base64。
- `four-purities-six-recollections/`導讀與`book/`閱讀器：8幕93筆原字幕＋同圖收尾＋獨立製作說明，共95頁。影片`jCXyluhcEb0`，首頁#video-07保留，書架第07本開放，14本中7可讀、7鎖定；四不壞淨與六念心智圖窗都接上導讀。
- 沿用共同guide-header／guide-ui與最新第06本閱讀器，右上只有回修道地圖，影片為真正YouTube iframe，原經4張卡直接顯示，沒有恢復折疊或加影片下重複連結。製作說明只放繪本末頁。
- `topSubtitle`黑字靠左、淺底，與圖片分層；6個章名照`artOverlay`原百分比／字級，以實際圖片框定位。END沿用六念圖，65%黑幕與兩行白字，不混入上緣字幕。原圖木牌完整保留。見`layout-audit.md`及逐幕橫直截圖。
- 下緣經文與來源在圖片之外，橫直式皆能展開本頁經文；保留經文捲動、目錄、頁碼、返回／重載／旋轉記憶、快速翻頁設定。載入共同reader-controls.css及reader-restart.js，最後一頁回到第一頁。
- 原有六本的全部檔案、插畫、共用CSS／JS與Pages設定保持基準位元組相同。

## 經文與素材核對

- 官方SuttaCentral sc-data固定commit `c7bba0f184e66904949d4918587975fb7fd7ec69`：SN55.1莊春江中譯、SA61、843、554，共4份原檔與雜湊／節錄已核對，資料見verified-sources.json。中文優先，SN另附巴利原文入口，SA各有台大獅子吼單經註解連結。
- S06 05:51五分功德原句取SA554，正確標註下緣經名與來源；原分鏡仍保存影片沿標SN55.1的紀錄。S03依分鏡只顯示經名。
- 已向作者提出兩項選擇，尚未收到回覆前保留原交接：S08「長者摩訶男」與SA554「訶梨聚落主長者」的人名差異（導讀已明說）；S06／07的正式圖JSON對應與影片背景分配相反（沒有擅自交換原圖）。這些差異詳列layout-audit.md，不宣稱影片圖面完全相同。後續依作者回覆可作獨立校訂，不覆寫原交接。

## 驗證與交付

- `python scripts/check-four-purities-six-recollections.py --verify-sources --screenshots`：390×844、844×390、768×1024、1024×768四尺寸，共380個逐頁狀態通過。核對全部字幕／經文、圖片尺寸／比例、章名中心小於1px誤差及cqw字級、邊界／按鍵避讓、同幕位置穩定、末頁重讀、目錄、快速翻頁、鍵盤、經文展開／放大文字捲動／來源往返、回導讀、重載與旋轉保留頁碼。
- 新書架及兩個心智圖入口、既有六本開書／下一頁／回導讀皆通過；無本地HTTP或JavaScript錯誤。首頁CDN測試取系統CA驗證的實際公開回應交給Chromium，未關閉TLS驗證。
- 導讀／閱讀器正式入口、PR與固定合併SHA ZIP會在交付訊息提供。逐幕試閱截圖與完整目錄ZIP方法：`docs/previews/four-purities-six-recollections/README.md`。
- 實體iPad/Safari、外部YouTube播放與典籍服務站實際畫面未驗證。此工作環境未提供Notion工具，尚未寫入；待補記文字在`docs/releases/four-purities-six-recollections-notion.md`。

---

# 全繪本末頁重讀（2026-11-15）

作者確認第06本介面，授權套用其餘五本。共用reader-restart.js依末頁頁碼將原下一頁按鈕改為回到第一頁，非末頁保留原操作；共用CSS在橫式為文字按鈕留出空間。06本保留原實作。故事、經文、圖像與頁數不變。手機與iPad橫直式驗證結果見本次PR。

# 第06本結語與重讀（2026-11-15）

導讀移除溫柔起點段，繪本新增第75頁製作說明：以增壹阿含28.7為主、參照阿含與相應部，解讀以原經為準。原11幕74筆故事資料不變。末頁下一頁按鈕改為「回到第一頁 ↺」，橫直式沿用原控制位置，僅這本試行。手機與iPad四尺寸測過結語捲動、重讀、接續下一頁、目錄與旋轉；實體Safari待作者確認。截圖見docs/previews/book06-afterword/。

# 第06本註解連結補正（2026-11-15）

依作者提供的四個網址，將增壹28.7、長阿含9與5、中阿含16的註解導讀換為卷頁／段落連結，移除「四阿含總入口」標示。經文、閱讀器與其他專頁不變。精確網址見SOURCES最新段落。

# 發布授權（2026-11-15，Asia/Taipei）

作者已明確授權直接發布PR #15，取代本次先試閱限制。發布須確認合併SHA及Pages成功。原五本保持不變。Notion工具未提供，尚未寫入；待補記見docs/releases/four-fruits-notion.md。

# SutraZen — current handoff

Last updated: 2026-11-14
Status: **第06本《四向四果與十結》導讀與繪本試閱完成；等待作者在iPad確認，未合併或發布。**

## 分支與交接

- 實作分支 `feat/four-fruits-ten-fetters-preview`，以最新main `bc29ec604dacf8515245669c553af8c27318a95d` 開始；已讀AGENTS、PROJECT、HANDOFF、SOURCES及實際八正道／十二因緣介面。
- 試閱草稿PR：https://github.com/rooneyflower-star/sutrazen-map/pull/15 ，目標main；尚未合併。
- fetch `content/four-fruits-ten-fetters-handoff`，固定交接commit `d82957317cd6733553c97149ebb49d1bd7bd7bad`，只帶入 `docs/four-fruits-ten-fetters/`。四份交接文字檔與作者附件ZIP逐位元組一致，完整讀取README、JSON／Markdown分鏡與manifest後實作。
- 插畫取自作者附件 `SutraZen_Four_Fruits_Ten_Fetters_Handoff.zip`，11張正式WebP及2張reference的檔名、尺寸、大小與SHA-256全部符合清單。S05採柱上「五受陰」、皮帶上「貪愛」版本；reference僅供比對，未用作內頁。

## 已完成

- `four-fruits-ten-fetters/` 主題導讀與 `book/` 74頁閱讀器；首頁#06由鎖定改為可讀，14本中6可讀、8鎖定；既有「四向四果」心智圖窗追加導讀／繪本入口，原影片#video-06及YouTube ID `n0bco_NPmRI` 保留。
- 導讀沿用共用header、guide UI、封面入口與16:9 YouTube iframe；右上只保留「回三十七道品修道地圖」，沒有另加快捷列或影片下重複連結。9張來源卡的經文直接顯示，不採折疊；含四向／四果的原典說明及溫柔起點結語。
- 11幕、74筆原字幕的字句、順序及時間標記全部保留；S02／03交界01:26、04:10「邠陀利花」、05:00與05:04作者原句均核對。`bottomScripture.cues` 的15個經文狀態按時間切換，原經選文與故事分開。
- `topSubtitle` 皆上緣靠左；S01／S10黑字淺底，其餘白字暗底。`artOverlay` 全空，未加圖內標題、果位名牌或頁頂摘要。幕名只在目錄／輔助科技標題出現。
- 每幕預留最長旁白高度，圖片不隨同幕字幕切換而跳動。橫式在上下文字與左右按鍵之間完整等比例顯示原圖，直式上下排列；S02兩側十結、S05柱／帶、S09貪／瞋門閂都在完整畫框內。逐幕核對表見 `docs/four-fruits-ten-fetters/layout-audit.md`。
- 沿用現有橫直式控制、目錄、頁碼、原經／本頁經文對話框、返回及session頁碼。載入根目錄 `reader-controls.css`，快速翻頁使用 `touch-action: manipulation`，保留雙指縮放與正常捲動。沒有修改既有五本及共用樣式或Pages設定。
- 原資料在交接目錄，`scripts/build-four-fruits-ten-fetters.py` 產生閱讀器資料；圖片均用repository相對路徑，未嵌Base64。

## 原典核對

- 9份原典／中譯均實際從SuttaCentral官方 `sc-data` 固定commit `c7bba0f184e66904949d4918587975fb7fd7ec69` 讀取並核對。逐檔SHA-256、13組經文選文及導讀補充見 `verified-sources.json`；測試可重新下載驗證。
- EA28.7正文邠陀利「花」與開頭列舉的「華」各依原文保留。DA9列舉次序／戒盜結與插畫排列／戒取分開；SA266繫狗比喻、SA71斷關、SA297無明離欲生明語境皆有來源卡說明。
- SN46.55先呈現莊春江中譯，附巴利原文入口；故事「瞋恚」與中譯「惡意」各保留原句。DA5四雙八輩只在導讀解釋，未把四種姓角色等同四果。

## 驗證與試閱

- `python scripts/check-four-fruits-ten-fetters.py --verify-sources --screenshots`：手機390×844、844×390、iPad768×1024、1024×768，每尺寸74頁，共296個頁面狀態；全文、來源、圖像／黑白字、靠左、零疊字、比例／邊界／按鍵避讓與同幕位置穩定通過。
- 翻頁、快速點按、首尾停用、11幕目錄、鍵盤、滑動、經文展開／關閉／來源、放大文字捲動及不誤翻頁、回導讀／重載／旋轉保留頁數通過。四尺寸導讀、新書架／心智圖入口及舊五本開書／下一頁／回導讀亦通過；無本地HTTP錯誤或JavaScript錯誤。
- 原有五本、根目錄共用CSS與Pages設定與基準main逐位元組一致。JS／Python語法、資料重建及diff空白檢查通過。
- `docs/previews/four-fruits-ten-fetters/README.md` 含逐幕橫直截圖、資料完整性結果、GitHub完整ZIP下載及電腦HTTP伺服器連接同Wi-Fi iPad的方法。截圖是無損WebP，原插畫不改動。交付訊息另給固定commit ZIP。

## 尚待作者／外部環境驗證

- **實體iPad/Safari** 的快速點按、雙指縮放、經文捲動與旋轉未測；Chromium觸控模擬不等同實機驗收。
- 本環境缺少 `open_cloud_preview` 及桌面JS工具，沒有可驗證的外部即時互動網址。提供可下載的完整目錄與已測HTTP開啟方式，不把正式站舊網址當成本次預覽。
- SuttaCentral服務站畫面、YouTube實際播放、台大獅子吼深層註解定位未驗證。台大獅子吼直接請求遭環境CONNECT 403，增壹／長／中阿含先保留明標四阿含總入口，未猜測深層錨點；已核對的官方經文資料不受影響。
- 本次最新指示是先試閱，**不要因先前其他書的發布授權而合併本PR或推main**。這次沒有正式發布，沒有新增正式發布或Notion已寫入的宣稱。

---

# Prior handoff and release history

# SutraZen — current handoff

Last updated: 2026-11-14
Status: Rapid-tap navigation fix prepared for publication and author device testing.

- User requests this setting on all existing/future readers, in portrait and landscape, for live device testing.
- Added shared `reader-controls.css`: `.controls button { touch-action: manipulation; }`, imported by all five book readers. No global zoom restriction, viewport limit, debounce, artwork/text/data or navigation logic changes.
- AGENTS.md and PROJECT.md require the shared stylesheet for future readers and preservation of pinch zoom/scrolling.
- Verify computed styles and rapid taps at 390×844, 844×390, 768×1024, 1024×768. Chromium simulation cannot prove real iPad/Safari double-tap behavior; author will test on device after publication.
- Publication must be verified against actual PR merge commit and Pages success; supply exact GitHub ZIP. No Notion tool available; pending record in `docs/releases/rapid-taps-notion.md`, not written to Notion.

---

# Prior handoff and release history

# SutraZen — current handoff

Last updated: 2026-11-14
Status: **十八界與四格疊字、偈頌排版、結語及原經直讀修正已完成；依作者本次持續修正及直接從正式站檢視的指示進行發布。**

## 本次修正

- PR：https://github.com/rooneyflower-star/sutrazen-map/pull/13 。分支 `fix/reader-labels-and-scripture`，基準 main `f01ffa80e6936c81572f8b9d29e99bb084ab26e5`。先確認最新main，保留原圖、原字幕、經文與既有操作；只有作者點名的字樣與新增結語作內容調整。
- 六處第二幕的十八界標籤按原圖1536×1024中六扇窗的實際中心排列，根／境／識三排都在各自窗內。資料存於該幕 `windowLayout`；全圖以實際顯示圖片百分比定位，原四格、遮罩和內嵌圖片不變。
- 八正道惡行四格右下只標「心不定」，移除「十惡業：」；其餘確屬惡業的標籤保留。善行四格移除左上「八正道：正業」，前段保留不偷盜／不殺生，安睡頁沒有多餘字樣，圖像與焦點不因空疊字跳動。
- 雜阿含771的原典轉錄 `excerpt` 與來源雜湊保留，新增 `displayExcerpt` 去除全形縮排並排成四行；忽略空白後字句／標點完全相同。導讀與閱讀器採同一呈現文本。
- 八正道仍保留13幕／110筆原字幕，另加第111頁製作結語（目錄第14項）；重用既有繪本的溫柔起點說明，明確寫「解讀仍請以原經文為準」。不是新增故事分鏡或改寫原字幕。
- 五本導讀的原經內容直接顯示。四聖諦2個、五陰1個、六處1個、八正道12個折疊區塊改為普通文字區，十二因緣原已直顯；原引文、來源按鈕與錨點保留。閱讀器的橫式本頁經文對話框維持。
- 更新變更資產的版本查詢，避免舊CSS／JS與新頁面混用。

## 驗證與發布交付

- 三本111／54／115頁於390×844、844×390、768×1024、1024×768，共1120次頁面狀態通過；原110／54／115頁的字幕、經文、圖像及順序保留（771僅空白排版）。
- 另測十八界所有逐頁標籤都落在對應窗框內、格位文字修正、善行整幕圖片穩定、771四行偈頌、最後結語／頁碼／返回保留、五個原經導讀皆預設顯示且無需點開。詳見 `scripts/check-reader-polish.py`、`scripts/check-picture-book-overlays.py` 及本次release驗證摘要。實體iPad/Safari未測。
- 作者上一輪明確表示繪本通常無法試閱，要求直接發布；本次是同一輪正式站檢視後的持續修正，完成檢查後發布本次具體變更，不擴張成其他未指定工作的發布權限。
- 合併與正式上線須核對實際PR的merge commit及對應Pages成功結果，並查驗正式網址；不能以git push成功替代上線驗證。正式ZIP採該merge commit的GitHub固定下載，實際下載核對。
- 此工作環境未提供Notion工具，尚未寫入。待補記文字保存於 `docs/releases/reader-polish-notion.md`，實際發布資訊另記本次PR。

---

# Prior handoff and release history

# SutraZen — current handoff

Last updated: 2026-11-14
Status: **作者已明確授權發布畫面疊字與多格閱讀焦點修正；以 PR #12 的合併與 Pages 結果為準。**

## 2026-11-14 — PR #12 直接發布授權

- 作者最新指示「通常繪本我無法試閱，你直接發布吧」，明確授權發布這次已完成的疊字與遮罩修正，取代本輪先前的試閱限制。這是本次授權，不擴張成所有未來工作的發布授權。
- PR：https://github.com/rooneyflower-star/sutrazen-map/pull/12 。沿用已通過1116頁面檢查與8組旁白像素檢查的實作；另對八正道閱讀器資產加入版本查詢，避免舊JS快取與新HTML混用。圖片、字幕、經文、分頁及疊字位置不另改。
- 正式入口：`eightfold-path/book/`、`five-aggregates/book/`、`six-senses/book/`。發布須確認實際merge commit的Pages成功，並檢查線上資產與互動。
- 每次正式發布提供精確merge commit的GitHub固定ZIP，實際下載驗證，避免只交付對話附件。
- 此工作環境未提供Notion工具，尚未寫入；待補記內容存於 `docs/releases/picture-book-overlays-notion.md`。實際發布資訊另記於PR。

## 本次授權與範圍

- 作者要求把八正道的主題／十善對照從頂端章節小字改為獨立插畫疊字；先完成正志橫直式截圖，再依分鏡完成其餘各幕，並為五陰與六處加入多格閱讀遮暗。
- 從最新 main `51d6572ae9069e703cc25bd12631397df1b6ed78` 建立 `fix/picture-book-overlays`。先完成試閱分支與PR；作者已另就PR #12明確授權發布，見本頁最新紀錄。

## 完成實作

- 重新完整讀取 `docs/eightfold-path/storyboard.md`，區分上緣旁白、插畫主題、下緣經文三層。移除錯誤的頂端章節摘要；幕名仍留在目錄。
- 正志兩行完整保留：「八正道：正志」「十善業道：不貪，不瞋恚」。左側沒有足夠空位，試排於圖內上方中央偏右，避開毒花、木牌、眼鼻口、羅盤與槍身；會覆到少量耳朵／額頂毛色，供作者確認。非原影片座標還原。
- 各幕的文字、百分比座標、對齊、寬度、字級、直式覆寫、字幕適用範圍與試排註記存於 `docs/eightfold-path/storyboard.json` 每幕 `presentation`。原字幕與原典選文不變。只有分鏡明載的惡行格位、善行格位與正業切換狀態改變文字；其餘同幕位置內容固定。無指定疊字的01／13幕不加。
- 橫式為旁白與經文留出圖外上下區域，圖片完整等比例顯示於中間；每幕以最長旁白預留高度，直式同樣保留高度，避免換字幕時圖片與疊字跳動。翻頁與目錄操作保持原介面。
- 八正道惡行／善行四格保留三暗一亮，疊字依格位與當頁顯示，不再全部堆在頂端。正語完整口四善對照暫放相鄰暗格，避免蓋住道歉場景。
- 六處六組四格（眼、耳、鼻、舌、身、意）加入三暗一亮，依既有字幕與受／想／行／過患位置切換。全書115頁、原疊字、字幕、經文、原圖與noscript回退不變。
- 五陰實際多格素材是宿命神通三格圖，依原圖x480／1024邊界（全寬1536）保留不等寬格位，第4／5／6頁依左中右聚焦、遮暗其餘兩格；沒有把三格切成四格。全書54頁原內容不變。
- `picture-panel-focus.js/.css` 為五陰與六處共用遮罩，依object-fit:contain的實際圖片範圍定位，排除留黑邊；資料在各書 `book/panel-focus-data.js`。八正道也使用相同76%暗度，沒有新增操作按鈕。

## 試閱與後續

- 正志先行橫直式截圖已推送，後續完整截圖及操作說明見 `docs/previews/picture-book-overlays/README.md`；各幕布局說明見 `docs/eightfold-path/overlay-layout.md`。
- 驗證腳本：`scripts/check-picture-book-overlays.py`。覆蓋110／54／115頁於390×844、844×390、768×1024、1024×768，檢查原文與原圖保留、各狀態、座標及遮罩範圍、疊字不碰字幕／經文／控制、正志避讓區、同幕不跳動、翻頁／鍵盤／滑動／方向與經文對話框。最終測試結果以本分支驗證紀錄為準。
- 完成上述四尺寸共1116次頁面檢查，全部通過；另測來源導讀／瀏覽器返回保留頁碼與長經文捲動隔離，並在五陰／六處四尺寸比對遮罩開關前後的白字像素，確認旁白不被遮暗。見試閱資料夾 `validation.json`。
- 實體iPad/Safari未測；所有未明示原影片座標均標為本次試排。正志避讓與正語暗格上的完整對照仍待作者看圖確認。
- 試閱階段未發布；作者現已授權發布本版，以PR #12的merge commit及Pages結果為準。Notion仍須明確區分待補記與實際寫入。

---

# Prior handoff and release history

# SutraZen — current handoff

Last updated: 2026-11-14
Status: **八正道與十善業道已獲作者明確發布授權；發布記錄見 PR #11 與對應 GitHub Pages 部署結果。**

## 2026-11-14 — 八正道發布授權與交付

- 作者明確指示「你直接發布吧，我看有問題再來改」，授權把本次新增內容合併 main 並發布；此最新指示取代本頁先前的試閱等待狀態。
- 發布 PR：https://github.com/rooneyflower-star/sutrazen-map/pull/11 。移除新主題導讀的 noindex；閱讀器沿現有慣例保留。故事、圖片、控制與所有舊書保持試閱測試版本。
- 正式入口：`eightfold-path/`（導讀）、`eightfold-path/book/`（110頁繪本）、首頁第05本與八正道心智圖說明窗。
- 合併與部署須以 PR 的 merge commit 及該 SHA 的 Pages 成功結果為準；不能只因 git push 成功而聲稱已上線。發布後另外驗證正式網址與新書操作。
- 每次正式發布的 ZIP 使用精確 merge commit。前次對話附件下載失敗，這次另提供 GitHub `/archive/<mergeSHA>.zip` 固定版本下載入口，並保留本地檔與 SHA-256。
- 此工作環境未提供 Notion 工具，尚未寫入改版頁。待補記文字保存於 `docs/releases/eightfold-path-notion.md`，不要把提供文字當成已更新 Notion。
- 暫定封面、白話校訂建議、實機 Safari、外部影片及註解深層定位等原有待確認項目仍保留，見下方。

## 本次範圍與基準

- 實作分支 `feat/eightfold-path-preview`，從最新 main `0236fca0c8ca0edbe3972bf51e4211ec33fd4e2f` 起作。已 fetch 並核對交接分支 `content/eightfold-path-handoff` 的 commit `e121f3c1f78535243ffbf75599a7f4e1e272e0fa`，只帶入 `docs/eightfold-path/`。
- 完整讀取最新 main 的四份規則／專案文件及交接 README、Markdown/JSON 分鏡、manifest；不依賴過去對話或 Notion 啟動實作。原交接檔原樣保留。

## 完成內容

- `eightfold-path/` 主題導讀、真實 YouTube 預覽（wabgCGL-Cfk）、12張經典卡；沿用 `guide-header.css`、`guide-ui.css`，右上只保留「回三十七道品修道地圖」，沒有新增額外快捷列或影片下重複連結。
- `eightfold-path/book/` 沿用最新十二因緣的橫直式、左右／底部控制、目錄、頁碼、經文展開、來源、返回與 session 閱讀位置。故事與原經均為可選取 HTML 文字。
- 13段、110筆原字幕依序製成110頁；11張正式原圖尺寸、大小與 SHA-256 全符，沒有重繪、刪鏡或 Base64。正志使用指定高清圖，正命完整末句保留；05/06段共用善行四格，13段為文字總結。
- 四格以 HTML 遮罩依字幕聚焦：每頁一格亮、三格暗；與原圖共同比例，未裁切圖像。
- 首頁第05本新增閱讀／導讀／原經，書架保留14本順序，分支內5可讀、9鎖定；八正道心智圖原說明窗增加導讀入口，原影片和既有道路連線保留。
- 現有四本閱讀器／導讀／插畫及共用樣式全部保持位元組相同。GitHub Pages 設定仍為 main 根目錄。

## 經文與校訂

- 12部參考經從 SuttaCentral 官方公開典籍資料核對，固定 commit 及雜湊見 `docs/eightfold-path/verified-sources.json`。片尾偈頌確定為雜阿含771。
- 下緣選文按段落主題配對，未假稱已復刻影片逐句經文時間。原故事、原分鏡轉錄、原典節錄與建議改寫各自分開。
- 鐵槍、世俗／出世間精進與正念、正定、筏喻的具體待校建議，見 `docs/eightfold-path/verification.md`；未擅自套用到原110筆字幕。
- 台大獅子吼直接存取遭 CONNECT 403；中阿含註解先提供明標四阿含總入口，深層經文定位待後續驗證，沒有套用雜阿含路徑猜測。

## 已通過的驗證

- Chromium 觸控模擬390×844、844×390、768×1024、1024×768，各110頁，共440次頁面檢查：全文、插畫、頁碼、三暗一亮與長寬比、無水平溢出。
- 翻頁、首尾停用、鍵盤、滑動、目錄、經文捲動不誤翻、橫式對話框／來源跳轉、方向切換／重載／返回保留頁數。
- 書架與心智圖新入口，以及既有四本的開書、翻頁與返回。建置／完整性腳本、JS語法與 diff 空白檢查通過。測試命令和範圍見 verification.md。

## 交付與剩餘項目

- 本次提供試閱分支／PR、完整目錄 ZIP 與四格焦點示範。導讀入口 `eightfold-path/`，閱讀器入口 `eightfold-path/book/`。
- 本環境缺少 `open_cloud_preview` 與桌面 JS 工具，不能提供經驗證的外部即時預覽 URL。ZIP 附本機 HTTP 啟動方式；file:// 被瀏覽器政策封鎖，未宣稱雙擊 HTML 已測試。
- 缺貓群片頭封面原圖，暫以正見地圖配 HTML 書名，內頁圖像完整。待作者確認封面與另列的白話校訂建議。
- 實體 iPad/Safari、外部 YouTube 播放及台大獅子吼深層定位未驗證。
- 作者已就本書明確授權正式發布，見本頁最新發布紀錄；上線結果以 PR #11 與 Pages 為準。原試閱版本完整保留於 commit `6c00958`。

---

# Prior handoff and release history

# SutraZen — current handoff

Last updated: 2026-11-14
Status: Twelve-link preview approved; user explicitly authorized production publication. Verify the Pages run for this release before claiming live deployment.

## Current implementation
- `twelve-links/` contains the native guide and reader, 77 pages (18 narrative scenes plus the original afterword), 18 original reader illustrations, cover, 5460×7170 Wheel of Life, storyboard and SHA-256 manifest.
- The fourth shelf entry links to the book, guide and original scriptures; 14 books total, 4 readable, 10 locked. Existing three books, map, artwork and video embeds are preserved.
- Fixed scripture-dialog navigation and keyboard navigation after button focus. Reading position survives guide navigation and orientation changes.
- Static full-frame Wheel of Life has 12 outer labels at least 12px. The author accepted the image and requested fine adjustments to birth/name-and-form endpoints; revision two includes these and a Four Noble Truths-style 16:9 YouTube frame.
- Removed the guide's trial badge and noindex directive for release. Reader noindex follows the established reader convention.

## Verified before publication
- All 77 pages at 390×844, 844×390, 768×1024 and 1024×768: illustrations, page numbers, scripture content, page buttons, keyboard, simulated swipe, scene menu, orientation retention and scripture dialog navigation.
- Original BOOK data and image hashes preserved; native local paths/anchors and fourth shelf entry checked. Revised coordinates and 16:9 video layout checked at four sizes.
- Downloadable single-file trial routing tested over local HTTP. Production reader does not use the trial's iframe packaging.

## Remaining verification and release record
- Real iPad/Safari and actual external YouTube playback were not tested in this environment. External scripture and independent image source/license records remain unverified; original credits are preserved.
- Publication is explicitly authorized by the user, after preview review. This document records approval and implementation, not evidence of a completed Pages run.
- Supply a ZIP from the exact published commit and report the deployment result. If Notion tools are absent, provide pending text for https://www.notion.so/40bcf2ef57db81658247c1e8268c3ccd and clearly state it has not been written.

---

# Earlier design and preview history

Last updated: 2026-11-14
Status: Design notes prepared; no coding or deployment authorized by this document alone.

## Current priority: Twelve Dependent Origination (十二因緣) picture book

### Decisions from ChatGPT discussion
- A high-resolution Wheel of Life / bhavacakra (生命之輪) illustration is planned to explain the twelve links.
- The latest preferred direction is a full-frame/static illustration with legible labels, rather than fragile hotspots or excessive interactions.
- Place labels along the outer curved edge of the twelve-link ring where possible, so they do not cover the important visual content.
- Label connector endpoints should touch the edge of the relevant sector, not extend into the sector center.
- Preserve consistency with prior picture books for reading/navigation controls and portrait/landscape layouts.
- The author reported that some preview controls were unresponsive; this has not been diagnosed or reproduced in this repository.
- The author could not reliably preview the latest twelve-link draft and asked to try publishing for direct review, but publication was not verified.

### What is actually verified
- On 2026-11-14 the repository root contained five-aggregates/, four-truths/, six-senses/, index.html, shelf.css, README.md.
- No twelve-dependent-origination directory was present at the repository root.
- Therefore the latest twelve-link HTML and artwork cannot be assumed to exist in GitHub.

### Codex next steps — only when explicitly requested
1. Inspect the existing picture books and identify their actual navigation and responsive layout conventions.
2. Locate the latest twelve-link source/artwork in the repository. If absent, request the approved draft/assets from the author or ChatGPT handoff; do not invent them.
3. Implement the agreed static/full-frame artwork and outer-edge labels without obscuring the illustration.
4. Check all controls in portrait and landscape; test on a real browser when available.
5. Provide a reviewable preview or branch and describe test results.
6. Publish only with explicit user approval.

### Handoff maintenance
After each implementation task, record: approved scope, changed files, tests performed, known limitations, preview/deployment status, and the next decision needed.

### Do not treat as final without verification
- Copyright/license status and image attribution for the Wheel of Life image
- Exact final label positions and source artwork resolution
- Final HTML/JS implementation
- Live deployment and tablet behavior

## 2026-11-14 — 十二因緣整合試閱（本地，等待作者確認）

Approved scope: recover and integrate the supplied preview, preserve all artwork and pages, fix defects, and prepare a reviewable trial before any publication.

- Added `twelve-links/`: native guide/book pages, separate CSS/JS/data, extracted original assets, a 77-row storyboard and SHA-256 manifest. No iframe is needed for normal website reading.
- Preserved the exact BOOK data: 18 narrative scenes (76 pages) plus the original afterword (page 77 / scene 19). Preserved all 18 reader illustration hashes, the original cover and 5460×7170 Wheel of Life.
- Fixed scripture-dialog navigation to real guide anchors and keyboard arrows while a navigation button retains focus. Session reading position survives guide/book navigation.
- Kept the full static Wheel of Life at its natural ratio. Adjusted outer-ring leader endpoints and made all 12 labels at least 12px, without overlapping labels at tested widths. Final visual alignment remains subject to author review.
- Prepared the fourth shelf entry and readable count in the local branch; other books, artwork, map and videos are unchanged.
- Local Chromium tested all 77 pages at 390×844, 844×390, 768×1024 and 1024×768, including image loading, scripture content, keyboard/buttons, simulated swipes, scene menu, orientation retention and scripture-dialog links. Downloadable single-file preview was separately tested over local HTTP, including its parent/iframe scripture routing.
- Preview-only single HTML packaging uses an iframe for portability; production directory uses normal links. Browser policy blocked file:// testing, so offline file execution is not claimed as verified.
- Not verified: real iPad/Safari, independent image license/source records and all external reference sites. Existing credits retained; no publication authorized until author confirms trial.
- Status: local preview branch only; no push, PR, production merge or deployment performed. Next: author reviews trial, labels and image credits; then explicitly approves publication.

### Preview follow-up: wheel endpoint corrections and consistent video UI
- Author approved the image, requesting the birth endpoint move slightly inward to its sector boundary and the name-and-form endpoint move outward. Updated only those two endpoints in both the rendered SVG and coordinate data; other labels/artwork remain unchanged.
- Added the same 16:9 lazy-loaded YouTube iframe component used by the Four Noble Truths guide, plus a direct YouTube fallback link, for video yaWXpSQqOx4.
- Rebuilt the downloadable trial. This remains an unpushed local preview, awaiting confirmation before publication. Video layout can be checked locally; external playback depends on YouTube/network access and is not claimed unless verified.

## 2026-11-14 — Consistent topic-guide headers
- User authorized direct publication after comparing all four completed guides. Standardized Four Noble Truths, Five Aggregates, Six Senses and Twelve Links to a single SutraZen brand and right-side 「回三十七道品修道地圖」 link to the site root.
- All four guides use the same root `guide-header.css` and header markup. The twelve-link guide no longer has a separate three-item header menu; its scripture and reading links remain in page content and the reader.
- Scope is guide headers only. Reading controls, book text/data, illustrations, map, shelf and videos remain unchanged.
- Validate shared styling at mobile and desktop widths, root return link, and each guide-to-reader entry before deployment. Actual Pages status must be checked; real iPad/Safari remains unverified.

## 2026-11-14 — Common guide UI and real video previews
- User requested direct publication after finding Five Aggregates used a green link placeholder instead of a YouTube iframe. Replaced it with the same real 16:9 lazy-loaded embed used in all four guides.
- Added root guide-ui.css for common content width, title/lead typography, spacing and video presentation, while retaining guide-header.css for the single return-to-map header.
- Removed extra same-page shortcuts outside the scripture sections, repeated end-of-guide reading CTA, source index shortcuts and separate under-video links. Primary book covers, real scripture sections, source citations within them, shelf and reader navigation remain.
- Guide content, scripture quotations and reader files/artwork must be preserved; validate all four at phone, tablet and desktop widths before release. Real iPad/Safari and external YouTube playback remain separate unverified checks unless exercised.

## 2026-11-14 — Consistent scripture source cards
- User authorized publication of the screenshot's source-card recommendation. Shared ChatGPT link was blocked by environment CONNECT 403; implementation follows the visible screenshot, not an unverified claim of reading the shared response.
- Standardized existing reference cards with edition/location metadata, pill buttons, original-text versus annotated-guide roles and explicit provider labels. Added matching 台大獅子吼 annotations to 雜阿含 cards using the same existing /agama/sub/<number>.html route pattern.
- Chinese canon links are labeled 漢譯經文, annotations 註解導讀. Pali originals, modern Chinese/English translations and Chinese treatises retain distinct correct labels. No unrelated 七覺支／第713經 entry was added merely because it appears in the sample screenshot.
- Scripture quotations, local source IDs, reader files and illustrations remain unchanged. Outbound provider retrieval may be blocked by network policy; syntactic link consistency and live local publication checks do not establish external-site availability.

## 2026-11-14 — Complete Āgama annotations and Chinese SN 22.48
- Corrected the earlier incomplete discovery: 台大獅子吼 covers all four Āgamas. Added the author's exact 增壹阿含 25.html and 中阿含象跡喻經 section URLs to Four Noble Truths source cards, preserving existing primary texts.
- Located SN 22.48 Chinese text independently in SuttaCentral's authoritative sc-data repository (`html_text/zh/pli/sutta/sn/sn22/sn22.48.html`, author 莊春江), after direct provider access returned 403. Added Chinese-first access, explicit translator/language, and a faithful excerpt with Pali comparison from bilara-data root segment sn22.48:2.2. Kept existing English/Pali links.
- Aligned the Bahiya source card with the same grouped actions and explicit Chinese translator. Moved its existing separate Pali link into the group without changing its destination or quotations.
- Added durable research instructions in AGENTS.md and sources in docs/SOURCES.md. Direct external website/anchor retrieval remains unverified where blocked; database content verification is not described as a successful provider-site visit.
