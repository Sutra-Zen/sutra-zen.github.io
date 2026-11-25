# 主線對話逐段確認／終幕X自由探索（2026-11-25）

從PR87 main `ea6dafa701670caffb5cd4e4ee4b9df05d4ff467`建`fix/mandatory-mainline-dialogue`。原疑幕與五陰入口顯示即seen，重整可整段消失；作者要求主線不能用回海圖略過，再追加終幕右上X可關，避免不能探索。最終規則：中間只有接著看、無X／略過，Escape及底nav／主閱讀／地標／工具不能繞；最後X/Escape ack回海圖不開書、不計完成，或按進去看看入書。X後終幕seen＋無pending所以正常自由探索且不再重彈。首本尾幕X／Next仍至原城景通知；唯讀replay可各幕自由回海圖。

新增純呈現pending store保存目前sceneId/context，normal show寫checkpoint、Next覆寫、terminal ack清；genericclose及replay不清。保留舊seen schema／首本receipt與cutoff，恢復先過原完成、資格與書籤門檻再精確當幕；同台詞的first-completion context不能丟。reset／restore清pending，local/session quota recovery有baseRaw與null tombstone，壞值不影響reading。歷史合法bookmark0／已完成優先，無pending才用舊seen補未讀段。

cache mandatory-dialogue-1與14本bridge query及game產生檔同步。原台詞／IDs／graph、reading/store／route政策URI、14本原稿／圖／shared reader版面、合法完成／頁碼、備份schema、SEO／Google與30成員Seven離線包保持。Pages legacy main:/及原電車圖不改，QA排除共31。詳[實作](play/mandatory-dialogue/README.md)、[重現及focused驗證](previews/mandatory-dialogue/README.md)。沿既有直接發布授權，正式PR／merge SHA／Pages／live交付證據以新PR為準；實機iPhone／iPad Safari未測。

---

# 清除後電車啟動與接著看／進去看看（2026-11-25）

從已發布PR86／main `dd480b67959e90adc50f2bb8e0c2b1f80197d8f2`建分支`fix/train-zero-completion-start`。實按Settings清除重現：reading與receipt清掉，但active海圖的reset事件立即寫arrival seen；舊電車資格又排除seen／任何bookmark，所以回首頁Start也沒有電車。不是原圖遺失或store雙單例。

電車資格改只看completed為0，每次首頁Start／Continue完整兩段；僅`#opening`中途重整且首段已看、末段未看才續第二段。Settings清除成功回主選單，reset事件不開arrival／不寫seen；失敗保留status與memory/session，避免跳頁丟暫存。作者首頁reset仍原prologue。讀本／城池／書架正常回海圖仍不重插片，歷史完成與頁碼不重置。對話所有中間scene強制「接著看」，真enter-book末段「進去看看」；completion context末段仍接著看至通知，replay末段回到海圖。原作者台詞／ID／graph均不改。

快取train-reset-1及14本bridge query、game產生檔同步；reading/store／route資格URI、原讀本／原圖／shared layout、備份與存檔schema、SEO／Google及30成員離線包保持。Pages維持legacy main:/，QA新增一個排除目錄共30。詳[實作](play/train-zero/README.md)及[重現／驗證](previews/train-zero/README.md)。沿既有直接發布授權以新PR合併及精確SHA Pages／live交付為準。實機iPhone／iPad Safari未測。

---

# 電車上捲字幕與四聖諦至五陰劇本（2026-11-25）

從已發布PR85／main `c6dcee91a535f8a2649886c34b86f781d21708fa` 建立乾淨分支`feat/train-opening-story`。作者12列新版劇本串接群貓三段字幕→選單→電車心聲→法輪遺跡／疑→原生四聖諦→四段讀後尾聲→新增城景通知→五陰湖。開始／繼續與設定按鈕永久2px白框，plain片頭提示無框。作者隨後補原ZIP並指定電車也用上捲字幕、進地圖才頭像對話；已按最新要求實作，先前缺圖／待原件狀態已解除。

完整原ZIP保存於`docs/play/train-opening/source/`；其中PNG1672×941逐位元匯入runtime，無重繪或重新編碼。`assets.json`記錄來源／runtime SHA，ready=true；預設asset gate比對原件、CRC、尺寸與URL通過。電車兩段連續跑完可自然轉場，或點背景／白字提示略過；reduced motion提供靜態捲讀。第一段完全捲過後記既有seen以便重整續第二段；重播不改reading／story／receipt。對話只在地圖上出現。

Phase A保留早期缺圖介面的流程證據：真四聖諦0–28，末頁明確完成才寫1本，4段尾聲先於原新增模組通知，接城池／Five0–3；6個歷史fixture含0書籤、已讀與seen保持。Phase B重新驗真正原圖與最終crawl六尺寸、自然結束／略過、載入錯誤與重試、重整續播／唯讀重播。原7個story IDs含Mara保留，新增train兩ID與doubt-escapes；新版主線依最新劇本不走Mara，舊資料仍有效。

active story/resetJourney cache同為train-opening-1以保單例，中央reading store／route policy URI和內容不改。14書HTML僅bridge query，1192步原生稿／經文／圖片／共享layout與已合併校訂、Google／SEO及30成員Seven離線ZIP保持。source shell與game產生檔同步，Pages維持legacy main:/，QA排除29目錄。詳[實作與素材](play/train-opening/README.md)、[驗證及代表截圖](previews/train-opening/README.md)。沿既有直接發布授權，精確PR／merge SHA／Pages及live證據以本輪PR交付為準。手機平板為Chromium模擬，實機iPhone／iPad Safari未測。

---

# 橫書純文字頁寬版置中／窄版靠左（2026-11-24）

接續已發布PR84／main `8f91fd461db03fc3c43920134af315bae75181c4`，在乾淨分支 `fix/horizontal-text-centering` 處理作者五陰片頭示例及十四本橫排純文字頁。共享CSS僅對 `reader-framed-ending` 的全寬scene加入單一fit-content受限grid欄；標題、口白、總結／表格及引文共用一欄，段內仍左排。寬且有足夠高度的視窗置中，手機直式／短橫式保持左起；橫式scene的scrollport在底部固定列上方結束、page維持深色背景，直式保留原自然文件捲動及頁尾空間；不把直式正文中途經過固定底列後方但可上移讀完的既有行為誤報成本輪新回歸。心經不在此class，維持可容納時置中、窄框最右起讀與原生橫捲。

唯讀名冊確認十四本18個橫書純文字步驟（含五陰／六處片頭、八正道表格、安那般那長總結等）；不是全1192步重新改稿。只改共享CSS及14本CSS快取 `text-center-1`，reader-layout.js、各書原生JS／CSS／資料／插畫與完成資格／書籤全保持，十二因緣44–45最新核定稿亦保留。七覺支30成員離線包同步共享CSS與HTML快取，Pages legacy main:/保持，QA排除共28目錄。 最終CSS的18候選×6尺寸共108組通過，36個基準字級／原文比對、16遊戲代表與8重整、2心經及2一般圖框回歸通過，0JS／同源HTTP；所有候選標題與尾字可達。

詳[設計與保護範圍](readers/horizontal-text/README.md)、[候選名冊／驗證截圖](previews/horizontal-text/README.md)。沿用作者更新發布授權，經PR與精確merge SHA之Pages／live驗收後交付；實際驗證及發布狀態以該PR交付為準，實機iPhone／iPad Safari未測。

---

# 十二因緣44–45頁手機譬喻核可改稿（2026-11-24）

接續已發布PR83／main `3d0699a9958908cae0e667014e3bf4bb65466f79`，於乾淨分支 `fix/twelve-phone-narration` 實作。作者核可前一輪討論的兩頁新版旁白，移除識／名色括號分類及「前一刻名色行為產生前一刻識」，改為依眼與畫面生起看見的識、感到愉快而想繼續看、手指滑動及獼猴攀枝的比喻。同步runtime的scene／page文字與維護CSV；封存原件、SA289經文／來源、插圖、遮罩、頁碼／步數與書籤不變。先前這兩頁「待核定」紀錄至此被新核准取代，八正道69頁及其餘未核可建議仍不改。

僅該書HTML更新資料快取 `twelve-phone-1`，共享字幕／圖框維持已發布 `approved-copy-1`；公開及遊戲共用同一讀本。詳[精確新舊文與維護](readers/twelve-phone/README.md)、[驗證及代表截圖](previews/twelve-phone/README.md)。QA排除新增一處，共27處，Pages維持legacy main:/。 本輪public／ordered／review×6尺寸共18組原生43→44→45→46、45重整、書籤／完成數、回書架／海圖、引文彈窗與圖框／文字避讓皆通過，JS／同源HTTP錯誤0；精確資料差異與15核心檔／21原插畫保護通過。沿用作者更新發布授權，經PR及精確merge SHA之Pages／live驗收後交付；發布狀態與驗證結果以PR交付紀錄為準，實機iPhone／iPad Safari未測。

---

# 核可出處／人物校訂與十四本三行口白（2026-11-24）

從已發布PR80／main `a238a0fb549966ac0510b5b89f18b913c8ec40b6` 建立`fix/approved-reader-copy`，初始乾淨。作者核可五陰7–9頁SA41、43頁完整未來識句；四不壞淨85頁訶梨聚落主長者、四聖諦1頁舍利弗、安那般那76頁阿難。Five新41經來源卡／CSV同步；Purities editorial-corrections及Anapana reader-edits可重建，原storyboard/archive保留。八正道69與十二44–45及其餘未核定稿件不改。原稽核PR81與五城試版PR82仍獨立，未帶入本輪。

作者44頁圖問題為三個硬行碰兩行帶，文字原可捲但初始被截；shared橫式p改自然換行，帶固定預留三行＋段距，各頁圖高仍固定，portrait原flow不變。全14本1192步×6尺寸84組7152樣本PASS，1916尺寸1192步完整原生Next，其餘逐狀態幾何；真稿標準橫式自然wrap後4684個樣本為1–2行、另2342直式flow，無初始裁字／永久clamp。獨立兩個DOM三行邊界fixture通過，不混作原稿；185最長外層代表及四念處8行總結真wheel/rotate/reload通過，圖高spread0px。Focusedpublic/game核可內容／41新卡往返／43→44、心經與結語、回程書籤皆通過，0JS／同源HTTP。實機Safari未測。

approved-copy-1更新14共享載入與遊戲回程、三本外部資料稿，generator同步game。原圖／其餘原稿／完成資格與存檔／首頁心智圖／SEO15／Google保留；離線ZIP30成員6668560bytes同步共享檔，原圖原稿原生書JS位元保持、CRC通過。Pages legacy main:/不改，QA排除26目錄。詳[實作與校訂範圍](readers/approved-copy/README.md)、[全量與focused驗證／截圖](previews/approved-reader-copy/README.md)。依作者既有更新發布授權經獨立PR；正式SHA／Pages／live結果以交付留言為準。

---

# 心經適配置中與深色口白（2026-11-24）

從 PR79 已發布 main `47e4b6ef5c7f51c9aba4766c6bc25eaa790cc239` 建立 `fix/reader-dark-heart-center`，初始乾淨。作者要求心經依版面左右置中、十四本公開／遊戲字幕深色一致；追加小版面應保留最右起讀。心經標題＋原經以真實不伸縮的子元素寬度判定，放得下才 center，超出則原 RTL flex-start／橫向捲讀；字級、直書、紅色重點與圖框保持。共用字幕及結語底色 #1e1e1e、淺字 #fffdf8，原 metadata、圖內標字與原經金／紅字不改。

快取 dark-heart-1，同步十四 HTML／遊戲產生檔與讀本回程，入口無白框 entry-no-frame-1 保留。七覺支離線 ZIP／manifest 同步30成員，其他原稿／圖片／讀本程式／保存／SEO／Google保護；Pages main:/ 不改，QA 排除25目錄。詳[實作](readers/dark-heart/README.md)與[驗證截圖](previews/reader-dark-heart/README.md)。檢查實際 glyph 與盒尺寸避免空盒假置中；實機 Safari 未測。沿本輪持續發布授權經 PR，精確 SHA／Pages／live 以交付留言為準。

驗證通過48組心經配置（156個原生逐段量測）及168組十四本口白配置（552代表樣本）；615檔保護、ZIP30成員CRC／原稿位元比對、JS語法、產生器與SEO15通過。手機／平板為Chromium模擬。

---

# 入口移除焦點外框（2026-11-24）

從已發布 PR78 `39ae4b24a40bcda483e2f443aa3676732ff93372` 建立 `fix/entry-no-focus-frame`，起始乾淨。作者要求入口進入選單沒有白框；來源是自動 focus 的 outline，非按鈕 border。僅取消片頭提示與標題開始／繼續按鈕的 focus-visible 外框，改以文字底線保留鍵盤提示。其他頁面焦點與所有點擊／鍵盤／略過防穿透、存檔及讀本不改。entry-no-frame-1 僅更新入口 CSS／載入鏈，產生器同步，Pages main:/ 不變。手機直橫式／桌面 Chromium 初始焦點無外框，Enter／Space／點選與進入地圖均驗證通過；實機 Safari 未測。沿作者持續發布授權經 PR，精確 SHA／Pages／正式站以交付留言為準。

---

# 十四本等高圖框、心經對齊與入口樣式（2026-11-23）

從已發布 PR77 `3a72b2e33a086714ce30cd80fbebb3ab641d0dc3` 建立 `fix/reader-stable-artwork`，起始乾淨、origin 正確。作者要求縮短回書架標籤、避開各選單、遊戲與道品網頁的十四本圖片同高、序章白字無框與開始／繼續深底淺青字；追加心經框及結語／總結的上方口白對齊。

共用 reader-layout 擴及十四本，reader-controls 新規則以獨立變數固定橫式兩行口白與原經帶，按實際控制項及安全區留白；直式文字自然流動，圖片保持共同高度。自然比例框保留疊字、巢狀六處 art-layer 與遮罩。超寬 related 資料圖以共用畫布 contain 留白。心經用同框與固定上方口白，保留直書／強調／橫向捲動；文字後記與總結從一致上緣開始，段落表格完整可捲。額外圖外提示與窄橫式總結借用口白捲動區，不再縮圖。五陰窄直式長總結移至固定圖框後自然流動，防止覆蓋原經入口；寬版恢復圖內總結。

catalog 只將「回收集書架」改「回到書架」，bridge 只改介面資料／CSS／回程快取；存檔、閱讀資格、完成與原稿不變。開始按鈕局部深底青字，片頭提示透明白字，操作與原片頭文本不改。十四 HTML 只加共用 script／快取與五陰六處版面 metadata，原圖片、經文、口白及聚焦資料保護；離線七覺支產生器補共用 JS，現成 ZIP／manifest 同步重建（30檔），原插圖與內容資料保護。

快取 stable-art-1，遊戲來源與產生器同步，原首頁／心智圖／SEO15／Google 保持，Pages main:/ 不改，QA 排除24目錄。詳[本輪實作](readers/stable-artwork/README.md)、[素材比例稽核](readers/stable-artwork/ratios-audit.json)及[驗證截圖](previews/reader-stable-artwork/README.md)。實際原圖多為約16:9與3:2，4:3支援依 fitting 驗，不冒稱原圖4:3。實機 Safari 未測；依持續發布授權經新 PR，精確 SHA／Pages／正式站證據以交付紀錄為準。

---

# 精簡全景控制、書架修正與對話內完成通知（2026-11-23）

從已發布 PR76 `d82f68533f595db032c8a787a1a2c5606a53fb2f` 建立 `fix/game-simple-panels`，初始乾淨、origin 正確。作者要求移除海圖／城池全景、書架捲動不重影、設定返回遊戲開始、刪右上略過開場，並將城景來源縮為經名加對應經文。追加要求移除「看閱讀回饋」，新增城景與本數直接接在對話腳本末段。

海圖／城池保留拖曳縮放；舊全景快照自動回探索，無返回全景控制。書架只有 stage 單層插畫，外層純色、書本層透明，左右滿寬。設定以 screen=title 回主選單、不重播／重置；片頭只留底部按鍵與原動畫背景點擊。城景彈窗只剩簡短經名／引文／X，創作模組與覺支夥伴不掛 SN35.245。作者指定廣場字句與可讀 SC 版本的差異，已如實記錄來源稽核，不改原經封存。

首本原心得→疑→波旬→五陰湖全文不變，統一「接著看」、不顯示回饋按鍵；最後由同一小貓對話直接通知城景自動新增與本數，分流「前往下一站」／「前往城池看看」。其他書共用通知。最終通知用 completed URL 恢復、經已讀檢查且不寫完成；選擇／Escape／重置還原清 URL，沒有新增存檔或 scene ID。原末頁完成、receipt、資格、reading/story/city store 與備份形狀維持。

快取 simple-ui-1，十四 HTML 只更新 bridge query、bridge 只改回程 query；原正文／經文／圖片／操作、首頁心智圖／SEO15／Google 保護。產生器同步，Pages main:/ 不改，QA 排除23目錄。詳[本輪交接](play/game-simple-ui/README.md)、[來源核對](play/game-simple-ui/source-audit.json)與[實際驗證](previews/game-simple-ui/README.md)。實機 Safari 未測；沿既有授權經新 PR 發布，精確 merge SHA／Pages／正式站證據以 PR 交付為準。

---

# 波旬左上、移除汗滴與滿版書架（2026-11-23）

從已發布main `a9ee6ae8fda9e1ec01822aa013ad85bcdf551f3a` 建立 `fix/game-city-shelf-framing`，初始乾淨、origin正確。作者指定波旬移左上以保留朝右視線、去城主汗，書架左右如城池鋪滿。scene僅改波旬early(500,130)/guardian後(250,230)，移除汗DOM/is-calm/CSS/keyframes；原圖、微晃、點角色X、來源與全景返回不變。

書架stage無外距、case無maxwidth／圓角邊框，原圖襯底滿寬；保留桌面4欄／手機2欄、獨立垂直捲動與底dock，最後一冊仍可達。十四卡／原封面／鎖定／複習資格不改，沒有強塞整書架進100vh。

入口／導覽／回程cacheframing-1，scene與SVG縮圖共用新版模組；原city store/catalog/text/journey與collection/story保持原單例URL與字節。14HTML僅bridge query，bridge僅回程query，generator同步。原站經文／圖片／正文／操作／SEO15／Google保護，Pages main:/維持，QA排除22目錄。詳[呈現調整](play/game-framing/README.md)與[實際驗證](previews/game-framing/README.md)；本輪針對視覺、滾動、複習與保存風險檢查，不為未變更reading重走29。實機Safari未測，沿既有授權發布，精確merge SHA／Pages／live結果以新PR交付為準。

---

# 自動新增城景與精簡城池（2026-11-23）

從已發布main `1ba30cfb016ed6affaefe1a62ee6ae9d1678efd9` 建立 `feat/game-auto-city`，起始乾淨、origin正確。作者改為讀完自動新增，不要長輩手動安置；追加要求完成通知邀請回城。原末頁完成／四段尾聲／閱讀資格保留，通知明寫城池自動新增並提供「前往城池看看」／繼續下一站。

模組原圖與拆分保留，get純由合法completed＋原source前置推導，空／舊安置清單不影響畫面，不造未讀城景；canPlace false、舊API無寫入。city v1/v2旅程備份相容，restore reading即可重建。僅點角色保存對話呈現紀錄，進城不自動開對話。移除上排選項、安置列／＋／計數與大底部文案，繼續閱讀移共用dock，城景滿窗。右上全景圖示、左上back精確恢復，legacy無snapshot回廣場。對話姓名去心想、只有X/Escape；景物來源右上X，非canonical來源label明確。六覺支夥伴各有短創作回應，不冒充原經；garden點擊層高於透明城界而低於其他建物角色。

新city store/import鏈統一auto-city-1；原story/collection/receipt/eligibility與原圖／文字／經文／操作／SEO15／Google保持。14HTML僅bridge query，generator同步，Pages main:/不變，QA排除21目錄。詳[說明與保存格式](play/game-auto-city/README.md)及[實際驗證](previews/game-auto-city/README.md)。真first29與fixture／最後targeted分開；實機Safari未測。延續作者本輪發布授權，新PR交付需核精確merge SHA、Pages成功與正式站結果。

---

# 四聖諦過場先於城池／下一站（2026-11-23）

從已發布main `2720747323f4d3a05474bf0c2919ac5332810cb2` 建立 `fix/game-outro-before-next-station`，起始乾淨、origin正確。作者回報先安置法輪碼頭後才出現四聖諦接五陰對話。本輪把正常首次完成改成心得→疑退場→波旬→五陰短句→原取得面板，再分流城池或下一站；尾幕CTA回取得面板而非直接讀five。

dialogue新增記憶體completion context，沿片段傳遞；cutoff延至尾幕確認／略過，重整可接回尾幕。前段略過仍先顯示尾幕，正常底列／地標不能繞過；設定與reset保留。舊Mara／退場已看但尾幕未看且five完全無書籤的存檔可補尾；已有five position（含0）／已看／已讀不強插。工具replay包含尾幕、唯讀。原receipt/末頁驗證、completed／資格、城池配置與備份schema都不改。

cache互返outro-order-1，原story store仍mara-1單例。14HTML僅bridge query；原經文／口白／圖片／操作、首頁32節點／14書架、SEO15與Google保護。生成來源與game同步，main:/未改，QA排除20目錄。詳[修正說明](play/game-outro-order/README.md)及[實際驗證](previews/game-outro-order/README.md)；真實閱讀與fixture分開，實機Safari未測。依既有授權發布，精確merge SHA／Pages／正式站結果以新PR交付為準。

---

# 模組城池、五蓋偽動畫與心聲（2026-11-23）

從已發布main `6bb59a61d5d045b87102989532a55dc814eafa42` 建立 `feat/game-modular-city`，初始乾淨、origin正確。作者本輪明確授權將前輪模組清單寫成程式，加五蓋圓球搖擺、全身波旬、識城主汗滴及心想，並可發布。城池改為新彩繪草地＋獨立模組；第一本完成先有免費四大花園與識，讀本取得14模組，點卡/拖到＋/自動安置，舊已讀不等於已安置、不要求重讀，不影響原閱讀資格。

city.v1保存placedIds/thoughtSeenIds，local/session基界線備援、missingprereq保留而不補讀；同一念守門人延續七覺支，另六夥伴。五蓋−3°～＋3°、波旬浮動及城主汗滴，減動態停止；心聲以屏幕文字可切換。原故事Mara頭像保護，新城景使用完整空手全身版。SN35.245六門／四大／識／念／雙使／消息涅槃／道路及SA1175差異仍可查，其他回饋為教材延伸。

journey-save統一設定與作者重置，v2備份含原reading v1＋city v1，先驗全部才寫；舊v1還原清city避免跨檔佈置。重置/還原關舊OS/來源與選擇，保留其他站點鍵，無localStorage.clear。快取互返modular-city-1，14HTML僅既有bridge query，原站正文/經文/圖片/操作/SEO/Google、原collection/route資格/receipt/相機/source原件不改；入口產生器同步，main:/部署來源不變，QA排除十九目錄。

完整一鍵驗證通過：真first29／原Mara→免費底盤→手放碼頭→reload→五陰0–3與配置續存；歷史3／7／14、滑列與觸控拖放、五尺寸心聲／鏡頭、v2／舊v1備份還原、兩reset、quota／404重試及實測搖擺／汗滴皆通過。原站32節點／14書架與3裸讀本回歸、615檔保護／產生器／15頁SEO通過，零JS／同源HTTP錯誤。

詳[本輪交接](play/game-modular-city/README.md)、[實測與截圖](previews/game-modular-city/README.md)及play/city/modules/ART.md。實際閱讀與隔離fixture分開記錄，實機Safari未測；固定槽位尚無任意搬移/拆除或逐幀走路。依授權經新PR發布，精確merge SHA／Pages／正式站與固定SHA ZIP以PR交付為準。Notion無連接器，待原對話補記。

---

# 波旬首次出場與中斷續看（2026-11-23）

本輪從已發布main `71de5285bef079f515abcc44577eb50a4aa8cea3` 建立 `feat/game-mara-observer`，起始乾淨、origin正確。依作者本輪森林附圖右上波旬製作透明右向頭像：紫金斗篷、紅橘小角、兩琥珀棕眼、帽額金飾與雙翼保留，手持橘貓面具移除，不重畫原書。PNG與imagegen最終原件相同，來源/hash見play/story/assets/MARA.md。

新mara-watches接在小貓說疑問號減少／退去之後，台詞為「站在遠方觀看的波旬心想：『可惡，小貓好像慢慢開始破除五蓋了……』」，再原完成回饋→五陰湖口白／讀本。波旬心想屬故事，不增設能力、完成或修證判定。以既有doubt-recedes結束標記延後至新幕確認，支援疑退場／波旬頁重整續看，又讓舊已完成過場的存檔不被強插新劇情。略過可回原回饋，工具重看唯讀，作者重置清新scene。存檔schema、資格、完成、原receipt與相機不改。

實測first29原生按鍵→疑退場→波旬頁重整恢復→原回饋→五陰0–3與返回續讀通過；五尺寸、略過／歷史相容／唯讀重看／作者重置／缺圖通過，615檔原站保護、產生器及15頁SEO通過，零JS／同源HTTP錯誤。

快取鏈統一mara-1，十四本HTML各僅更新原bridge script query，其他原字節經精準比對；新模組／作者重置共享story store，淺藍CSS原樣保留。詳[本輪交接](play/game-mara-story/README.md)與[實測／截圖](previews/game-mara-story/README.md)。Pages沿用main:/、QA排除十八目錄，原站SEO／Google／原圖經文及操作保留。沿用明確發布授權經新PR；精確merge SHA／Pages／正式站與固定SHA ZIP以PR交付為準。Safari實機未測，Notion無連接器待原對話補記。

---

# 淺藍青瓷操作與五陰湖銜接（2026-11-23）

本輪從已發布main `0d44d7229195d60bf1781e55e88ab53b8d7fcc7f` 建立 `feat/game-cyan-aggregates`，工作樹起始乾淨、origin正確。依作者要求把遊戲主要／建議操作與目前關卡等深綠語意改成淺藍青瓷，保留深青靛半透明對話／選單與原插畫。加入小貓苦集滅道→苦的心理運作→前往五陰湖短文；四聖諦原完成回饋保留，前往下一站後按新對話CTA才開原五陰。已看過／已有五陰書籤／複習直接續讀；資格、完成冊數及獎勵不變。

故事文字集中於story/data.js，已看紀錄沿用story.v1，作者重置共享同一module instance。處理game／city／shelf／讀本回程的HTML、bridge及CSS快取版本；十四本HTML各只改既有bridge script query，正規化該單一URL後須逐位元等於基準。未帶collection參數的原站閱讀器保持自由閱讀，不套遊戲主題或進度。原站SEO／Google／原圖經文／相機及存檔不改。

實測first29原生按鍵→原回饋→新五陰對話→原五陰0–3與重整／旋轉／返回續讀通過；五尺寸淺藍各狀態及對比、略過／歷史書籤／鎖定／唯讀重看／作者重置、615檔保護、產生器與15頁SEO檢查通過，無JS／本機HTTP錯誤。

詳[本輪交接](play/game-cyan-aggregates/README.md)與[驗證／截圖](previews/game-cyan-aggregates/README.md)。沿用明確遊戲發布授權經新PR，精確merge SHA／Pages／live與固定SHA ZIP以PR交付紀錄為準，不能以本段推定已發布。main:/來源不變，QA排除十七目錄；實機Safari未測。Notion無連接器待原對話補記。

---

# 半透明深色介面、完整頭像與疑過場（2026-11-23）

從已發布main `44dce2f6624e568ff83d6cf79e675fe61a53c325` 建立 `feat/game-doubt-dialogue-theme`，工作樹乾淨、origin正確。作者已明確授權發布前輪保留需求及本輪新增劇情：對話與選單統一深色半透明，背景圖保留原色；小貓頭像取消圓形裁切，完整露耳；新疑角色依原安那般那S03／四禪S05生成透明概念稿，問號由網頁呈現。

新流程保留原arrival，疑只說「愚痴……」，小貓繞過入口後讀原四聖諦。只有真正末頁完成後才接正智／慧根慧力的短心得及問號減少、退入霧中，再回原法輪碼頭回饋／五陰。文案表達理解與練習，不當作斷疑、證果或能力數值；不把疑與愚痴作經義等同。場景演出只屬遊戲故事。

新presentation completion receipt由既有讀本bridge成功完成分支發出，海圖核對／消耗；URL或歷史done不單獨觸發過場。四聖諦HTML只改bridge快取版本一處；發佈補修加入first-reader `collectionStory=doubt-2`／return `v=doubt-2`以避開600秒舊HTML快取，詳[快取補修](play/game-doubt-story/CACHE-FOLLOWUP.md)。其餘原書內容與圖片／資格／順序／store／鏡頭不改。中斷可續短過場，明確略過／重看不重發獎勵；工具可手動看已完成第一本的過場。作者重置連receipt一起清除；儲存失敗邊界保留。

詳[本輪規格與素材](play/game-doubt-story/README.md)、[實際驗證與截圖](previews/game-doubt-story/README.md)。全程實測first29與相關續讀／歷史／資產失敗／五尺寸；不把fixture稱全十四本實讀。Safari實機未測。main:/與原站SEO／Google檔保留，QA排除十六目錄。精確merge SHA／Pages／live與固定SHA ZIP以本輪PR交付為準；Notion無連接器，待補本輪紀錄。

---

# 序幕跑馬燈與作者首頁重置（2026-11-22）

從已發布main `35d59e3bc41faed5fe7b0d22d1a0797398c6de59` 建立 `feat/game-prologue-author-reset`，起始乾淨、origin正確。作者希望重看首次小貓口白與片頭；新 `/game/` 先在原貓咪JPEG上播放作者三段六行原文，由下往上捲動，播完／點一下／鍵盤略過才顯示既有置中選單。返回海圖不重播。降低動態模式提供可捲動靜態全文與進入選單。

首頁重置只在暫用作者入口 `/game/?author=1` 建立，普通玩家入口不顯示；未來可關閉 `AUTHOR_REVIEW_ENABLED`，它不是權限機制。確認後僅清遊戲collection、路線metadata、story已看紀錄及遊戲camera/tip session，取消不變，不用localStorage.clear、不碰原站讀本資料。修正既有collection.reset忽略session備援刪除失敗、可能重載復活舊紀錄的邊界，只動reset清理與如實回報。連同同一module instance中的story記憶體一起重置，重頭開始會再次出現第一幕口白。儲存失敗明示本分頁狀態與永久保存限制。

新 `play/prologue/` 純呈現、文字集中可替換；新 `play/title-review.js` 隔離試玩工具。原圖、原書、資格、進度格式與source graph不改。來源HTML／產生後game及快取版本同步；詳[本輪交接](play/game-prologue/README.md)與[測試截圖](previews/game-prologue/README.md)。main:/發布方式保留，QA排除十五目錄；精確merge SHA、Pages／live與固定SHA ZIP記本輪PR交付。實機Safari未測，Notion無連接器待補PR及發布紀錄。

---

# 城池原色雲霧、路線回饋與小貓開場（2026-11-22）

從最新main `be78106f6414ebf447eaedadd5c94883359be58e` 建立 `feat/game-city-story`，起始工作樹乾淨、origin仍為Sutra-Zen/sutra-zen.github.io。最新指示取代上輪港口城池徽章：海圖示意入口移除，保留固定底列城池；原圖鏡頭範圍、半島避讓與全圖返回不改。

城池保留完整原色底圖，未解鎖改局部雲霧；依作者 `SutraZen_Codex_Route_Unlocks_v2.md` 正文r3補五根五力區域連動、七覺支既有夥伴等回饋。法義資訊分清SN35.245六門城喻／《雜阿含》1175平行差異與教材美術延伸，不將後者全冠城喻經號。沿用completed與既有selectors，不新增閱讀認證或自動完成。

新 `play/story/` 提供頂部頭像對話與作者原句的首次穿越開場。無進度新玩家自動顯示一次，工具可重看；看過紀錄獨立於閱讀存檔。橘貓金袍頭像1254×1254透明生成概念稿待作者確認，沒有燈籠；其他角色與後續劇情尚未製作。原繪本口白、經文、圖片與操作不變。

詳[本輪交接](play/game-city-story/README.md)及[實測與截圖](previews/game-city-story/README.md)。本輪驗證受影響的開場、入口、雲霧與回饋，未把fixture當十四本實讀；實機Safari未測。Pages沿用main:/，QA排除共十四目錄。沿用已有遊戲發布授權經PR，精確merge SHA／Pages／live及固定SHA ZIP以PR交付為準；Notion無連接器，[待補記錄](play/game-city-story/PENDING_NOTION.md)。

---

# 原圖範圍與港口城池入口簡化（2026-11-22）

作者三張截圖顯示半城拼貼、外海異色不自然，最新指示取代前輪外圍海洋方案。從0971b459 main建feat/game-original-frame，工作樹乾淨。一般探索以原1600×900圖cover可讀區，鏡頭限制原圖左／上／右及底緣；底列實際高度從可讀區扣除，拖到南側極限時半島在底列上方，單色藍底只在被列覆蓋的區域。全景fit原圖、不含外海，異比例空間採深色底襯；保留兩處返回箭頭及前鏡頭快照，舊存檔必要clamp不改閱讀進度。

港口半座城景、海岸裁切與跨接路移除，改共享城門圖示＋「城池」文字的簡潔UI徽章，完整城景仍點開呈現。原圖alpha混色與外海pattern不載入，原PNG不改。保留32地標／46來源關係、原書與首頁SEO、遊戲資格／store／bridge及main:/。新QA排除後十三目錄。

詳[本輪交接](play/game-original-frame/README.md)、[實測截圖](previews/game-original-frame/README.md)。驗證五尺寸鏡頭四界／半島／原圖全景／返回、舊外海鏡頭及必要觸控續讀，實機Safari未測；不重走未改1192步。沿用遊戲發布授權經新PR，精確merge SHA Pages／live及固定ZIP記PR；Notion不可用待補文字留交接。

---

# 外海留白避讓八正道半島與全圖返回（2026-11-22）

從最新 main53e8eee0建立feat/game-ocean-overview，工作樹乾淨、origin正確。依作者截圖回饋，在原1600×900地圖外加入外海留白，鏡頭可讀區避讓實際底列＋16px，讓八正道半島可完整移到操作列上方；原插畫／32地標／46來源關係維持同原點，沒有單獨縮放或改動資料。海水為原圖無地景區的runtime SVG pattern，原PNG不改。

全圖記住先前位置及縮放，左上明顯返回箭頭與底列返回按鈕還原同一鏡頭；重複全圖不覆蓋返回點。camera既有session命名空間相容舊資料，與閱讀進度分開；旋轉／底列變高時全圖重新適配。頂部返回僅全圖期間出現，原本底列與全視窗背景保留，標題紙卡品牌修正保留。

詳[本輪交接](play/game-ocean-overview/README.md)、[截圖與檢查](previews/game-ocean-overview/README.md)。針對鏡頭與兩個返回入口、半島避擋、觸控及必要續讀驗證，原站615檔與store／資格／橋接／資料保護；實機Safari未測。QA排除共十二目錄，Pages仍main:/。沿用遊戲發布授權經新PR合併，精確SHA Pages／live／固定ZIP記PR交付；Notion不可用，待補文字在本輪交接。

---

# 首頁品牌移入紙卡及標題資產版本（2026-11-22）

依作者實際截圖修正：SutraZen 放在米色紙卡內右下角，採正常文流靠右，不再作為居中 flex 的另一個項目；紙卡本身保持水平／垂直置中。主標為「佛陀的解憂之旅」，保留指定副標與引導句。針對截圖所見新舊文字／樣式混用，僅首頁入口、title module、文案與CSS加入一致版本查詢參數，動態樣式載入同步，避免快取沿用舊版。無須清除進度。來源HTML與game產生器同步。從8700dc9 main建立fix/game-title-brand-in-card，工作樹乾淨；五尺寸及舊快取模擬驗證後依既有授權發布，精確SHA／Pages／live與固定ZIP留新PR。實機Safari未測，Notion不可用待補本次紙卡內品牌位置。

---

# 遊戲首頁文案與品牌位置（2026-11-22）

從最新 main `a32a4b667f41d162cdda20edc08f9cdf0f58f6db` 建立 `feat/game-title-copy`，起始工作樹乾淨。依作者原句更新主標「佛陀的解憂之旅」、副標「療癒系佛法繪本遊戲」、粗體引導「跟著小貓，讀懂煩惱，練習放下。」；SutraZen 從紙卡移至首頁右下角，保留安全區。文案集中 game-ui-text.js，來源 worldmap HTML 與 game 產生器同步，背景／開始續讀／進度與原繪本不改。沿用遊戲發布授權經 PR 發布，精確 merge SHA／Pages／live 記於 PR 交付留言。

五尺寸 Chromium 檢查主標／副標／引導句、品牌位置與開始操作；實機 Safari 未測。Notion 不可用，待補記本次新名稱與三行文案及新 PR 的固定 SHA ZIP。

---

# 海圖全視窗、半透明底列與觸控拖曳修正（2026-11-22）

作者遊玩後要求地圖占滿視窗、所有常用控制集中於最底下一列且半透明覆蓋地圖，並修正單指拖動、首頁置中及港口半座城堡入口。從最新 main／PR61 merge `ab311d9a2e030cf7e608e3bd9bc83a006445532e` 建立 `feat/game-fullscreen-dock`；起始工作樹乾淨、remote 正確，沿用 `/game/` 發布授權。新 PR 的交付留言會記精確 merge SHA、Pages 與正式站結果，不能用本文件推定已上線。

海圖 `.wm-viewport` 現為全視窗 `inset:0`，沒有頂部 HUD／底部導覽的保留色帶。進度、續讀含頁碼、地圖／城池／書架、目前關卡、全圖＋－、工具與設定移入同一半透明底列。寬版一列全顯示，窄版列內可滑／48px左右箭頭，維持按鍵與文字大小；原生工具 dialog 從底列上方開啟，路線選擇關工具後再顯示主題。相同底列套城池／書架，原讀本不注入。

實際重現觸控錯誤：從地名標牌拖80px只走第一13.33px，原因是子元素隱含capture移交視口時的冒泡lostpointercapture被當成取消。相機現在區分子元素移交與視口真正失去capture，保留雙指／取消／防誤開。港口城景以既有原圖＋鬍鬚層微縮，半座在世界左界外，露出城門並以短路接港口；標牌可換語言，未改來源關係。首頁原始貓咪JPEG及開始／繼續保留，標題紙卡水平垂直置中，短橫式卡內可捲。

實作與邊界見 [本輪交接](play/game-fullscreen-dock/README.md)，[實際檢查／截圖](previews/game-fullscreen-dock/README.md)。615 原站保護檔、store／資格／讀本橋接及32地標／46關係保留；新QA排除後共十一目錄，main:/與SEO／Google原檔不改。實機 Safari 尚未驗證，Notion工具不可用，待補筆記含於本輪交接。正式發布依原授權經新PR，再核精確SHA Pages與live，提供固定SHA ZIP。

---

# 小貓的山海旅程：沉浸介面、原始封面與統一關卡（2026-11-22）

沿用作者先前對 `/game/` 可直接發布的授權，本輪從最新 main／PR60 merge `7e39f04a383ab98d3b747365ea3e513ad7140a0e` 建立 `feat/game-immersion-sequential`；origin 正確、開始時工作樹乾淨，提交前 fetch 確認 main 未變。新版經新 PR 進 main，精確 merge SHA、Pages 成功與正式站驗收將記於該 PR 交付留言。下方舊自由選讀、任意 activeBook 續讀及玩家 review-all 屬歷史設計，不再是現行遊戲規則。

作者補上的 `0封面.zip` 已 CRC 核對；實際 `0封面.jpeg` 逐位元複製成指定 runtime 名稱 `play/assets/CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg`，原生 2752×1536、SHA256 `fc7cb28c894890127a20fd1bb898d2448950d51be86c3b36200faa6c2ae523e9`，未重新生成／編碼。原 ZIP、提示稿、匯入紀錄保留於 `docs/play/game-immersion/`。品牌 SutraZen，主標「小貓的山海旅程」、副標「佛法繪本探索遊戲」均為 HTML；背景貓群僅裝飾，旅人沿用既有金袍橘虎斑小船圖。

新共用滿版殼：進度／設定 HUD、底部地圖／城池／書架，次級設定含心智圖、原網站、經典來源、備份／還原／確認清除及選用全螢幕。閱讀器／城池／書架返回不重播標題；原讀本不注入遊戲主選單，原經區與按鍵保留。產生器與 worldmap 來源同步，根路徑匯入取代 `<base>`。1600×900 地理與 32 主題／46 原關係不改；所有圖層共用鏡頭，支援拖曳／雙指／＋－／全圖／目前關卡、拖後防誤開、旋轉及跨頁鏡頭保持。港口新增城池入口；全圖用區域定位，放大保留可讀標牌與主要關卡光暈。

`route/eligibility.js` 共用資格落到地圖／主按鈕／路線／書架／城池／舊 collection URL／書籤恢復／位置與完成寫入。只有第一本未完成可開始；已完成才可複習。順序仍 r3 十四本（十二因緣前段、五根五力在七覺支前、四向四果最後），未解鎖舊書籤保留但不能搶主線。合法歷史亂序 completed IDs 不取消，也不補前置完成；歷史已讀終章仍可看。原網站十四本不帶 collection 的網址仍自由閱讀、不寫遊戲進度。

末步明確按「完成這本」才過關，store 再核資格及末步索引，重複操作冪等。複習不加本數／獎勵／不改主線，部分書籤續讀、末頁書籤從頭；結束回書架。新完成面板顯示地景、城池部件與已讀／14，主按鈕「前往下一站」只回海圖定位，次要「看看城池」。書架沒有未讀開始按鈕，空狀態可前往第一站。城池保留六門及卷軸對應，寬／窄／彈窗完整「念-守門人」；未取得部件只引導目前關卡。審稿移到獨立 inspection，舊美術比較頁也無正式進度模組或 Storage 讀寫。

儲存沿用 `sutrazen.play.collection.v1`，保留合法資料；localStorage 失敗時以有 canonical base 值界線的同頁籤 session 備援跨頁續讀，外部還原優先，不合併成另一完成集合。兩者皆禁用則當頁仍可讀並明說限制。沒有全站 clear 或 service worker。介面文案分開集中，其他語系／原生 App／帳號未新增。

驗證通過：實際原生按鍵走完第一本 29 步及完整複習；中途重整／旋轉／返回續讀；6 組三入口複習位置；所有入口越關阻擋；未來書籤、歷史亂序／終章及全完成隔離資料；儲存故障／備份還原／取消及只清遊戲；5 尺寸 1280×900、360×800、844×390、768×1024、1024×768 的三分頁與地圖鏡頭／世界座標；Chromium CDP 雙指縮放取消不誤開；獨立審稿零 Storage。純模型含 16384 完成子集。615 個原網站正文／經文／插圖／14 本 HTML／首頁／SEO／Google／操作與建置保護檔對基準逐位元未改。原 1192 步報告保留為未變原稿依據，不以舊自由模式代替本輪資格驗證。零 JS／本機 HTTP 錯誤。

詳細架構／待補見 [本輪交接](play/game-immersion/README.md)，[實際截圖與報告](previews/game-immersion/README.md)。根目錄啟動 `python3 -m http.server 8765 --bind 127.0.0.1`，開 `http://127.0.0.1:8765/game/`；正式網址僅在 exact merge-SHA Pages 與 live 確認後回報。新增 QA 排除使 `_config.yml` 合計十目錄，main:/ 發布來源不變。實機 iPhone／iPad Safari 手勢及效能未測；既有插畫未全拆動畫層、完整終章演出及其他語系仍待後續。Notion 工具不可用，待補筆記在 `play/game-immersion/PENDING_NOTION.md`；發布時提供固定 merge-SHA ZIP。

---

# 繪本旅程首次公開試玩：/game/（2026-11-22，已獲本輪發布授權）

作者本輪明確要求更新海圖及城池並直接發布有`/game/`的網址；此授權取代下方歷史試作的不得發布限制。沿用新專案`Sutra-Zen/sutra-zen.github.io`，起始`a2b3225`乾淨，最新main為`b9a0dad2c2c34d7e15e6dc5e55d6125de630f57b`且已包含於原型歷史，建立`release/game-first-playable`。整批現有旅程與本輪修正由[發布PR60](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/60)進main，保留PR58／59原型審閱歷史；Pages仍用legacy main根目錄。實際發布狀態與精確merge SHA必須以PR60交付、Pages及正式站驗收記錄核對，不能由此授權段落推定已上線。

新增`game/index.html`實際共用山海地圖，非iframe、非轉址、不複製圖文。`<base>`指回原worldmap模組／素材位置，`scripts/build-game-entry.py`管理五項必要殼差異：base、標題、品牌返回、試玩版標記與隱藏內部美術審稿區。正式入口為`https://sutra-zen.github.io/game/`。海圖名稱改「安那般那與止觀竹林」「六念燈塔」，建物本身仍保留木造畫風。固定海圖按鈕、城池／書架／經典配置返回皆指新入口；舊worldmap入口與普通collection、獨立原閱讀器保持相容。

城池全圖改為接見使者的場景：皇冠橘貓城主前移到廣場北緣，後方建物保留；黑白與三花止觀使者到右前方，朝向城主，共持展開米白卷軸。城主八字鬍接山羊鬍覆住嘴巴，新增獨立RGBA鬍鬚圖層；全城、城主局部與五陰完成獎勵皆以同份合成函式畫出，避免局部漏層。原生底圖1671×941、髮層1536×1024，實際來源／SHA及放置表見`docs/play/game-release/generated-assets.json`，原件及舊版本保留，沒有Python改畫。

可替換HTML標牌改「地水火風四大廣場」「止・觀使者」「如實消息・涅槃」。卷軸中心為原圖64.6918%／49.4155%，消息用近旁短引線；城主與使者的引線避開臉。卷軸／鬍鬚／方位是故事美術，SN35.245六門城喻、城主識、四大、念、止觀及涅槃的對應與漢巴平行對讀不改。新法義說明保留卷軸是場景道具，不冒充經文明文。

保存與完成邏輯不改：沿用`sutrazen.play.collection.v1`及r3metadata，橋接只增加白名單`collectionReturn=game`及相應返回文字／網址；未開遊戲參數時原書介面不變。前三本共29＋54＋115＝198步已從新入口實際逐頁走完，末步明確完成才記1／2／3冊及stage1／2／3，回新入口看精簡回饋並接十二因緣；中途重整、旋轉、返回續讀與舊儲存鍵保留。全14本1192步原稿驗證沿用歷史證據；本輪不重新走未變內容。純模型再次通過16384個完成子集。

根目錄新增最小`_config.yml`只排除九個遊戲QA證據目錄，原圖、來源、舊預覽PDF及整個Git歷史皆保留。a2來源約957MB，排除182.6MB遊戲審稿證據後約775MB再加本輪小幅素材，避免Pages體積上限；不改Pages發布來源，不加全站service worker，不動首頁推廣、14本書架／32節點或15頁SEO／sitemap／robots／Google原件。排除路徑的截圖改從GitHub／PR查閱，不能報成正式站圖片網址。

本輪五尺寸160次海圖＋70次城池原生對話、全文標牌／全幅圖框／手機標牌無裁切、卷軸短線落點、新入口往返城池／書架／來源均通過。全城、城主局部及五陰獎勵都確認含鬍鬚圖層；自由先讀末章只完成該本、重讀不重計、普通collection／獨立閱讀／舊v1隔離、壞檔及儲存禁用仍可讀通過。616個原書／來源／首頁／SEO保護檔對正式main相同（14本HTML僅既定opt-in module），21個核心對原型相同，完成與保存函式未改。無JS／本機HTTP錯誤。

本輪實作與限制見`docs/play/game-release/README.md`，完整本機驗收與截圖見GitHub內`docs/previews/play-game-release/`，主要檢查為`scripts/check-game-release.py`、入口模板與SEO --check。維護檔diff通過；原經鏡像及作者原封交接檔的既存空白原樣保留，不為格式檢查改原文。實機iPhone／iPad Safari及原生觸控未驗證；未完成語系、完整終章演出與完整獨立人物／建築動畫層仍待後續。未新增帳號服務或把閱讀完成當作修證。

Notion工具本輪不可用，待補文字留在`docs/play/game-release/PENDING_NOTION.md`；沒有代為寫入。發布時提供精確merge SHA的GitHub原始碼ZIP備份及Pages／正式站結果。

---

# 獨立城池、八字鬍標牌與完成回饋（2026-11-22，試閱未發布）

依作者最新說明延續`preview/journey-visual-v2`及草稿PR59，起始HEAD為`fd7d44cfa1975914d82134b41ee57c1f4a018a94`。正式main仍為`b9a0dad2c2c34d7e15e6dc5e55d6125de630f57b`，remote正確；本輪不合併main、不部署Pages。PR59仍以`feat/picture-book-journey-v1`為base，不是直接對正式main。

港口斜線實際是原「道路總說→八正道總說」來源邊，顯示錨點落在港口及右下驛站，直線恰好穿過四禪。現在來源端點不變，改沿下方半島公路；作者指定的四禪→四如意足→港口另存`MAP_CONNECTIONS`地理交通層，明標`relation:false`，不新增經典／原心智圖關係，不改閱讀次序或解鎖。原46筆來源ID、端點、順序與資料檔保留。

新增`play/city/`獨立完整城池，無需先操作小貓。海圖、視覺比較及收集書架共用`play/navigation.js/css`固定導覽：海圖／心智圖／城堡圖示＋城池／書架；只對這些試閱頁啟用，不改原首頁導覽。城池保留醒目的續讀與回海圖，14個可選HTML標牌、六門及圖內SVG引線，手機短標牌／放大平移、各部件簡短法義與原繪本重讀。標牌與操作文字集中於`CITY_COPY['zh-Hant']`，其他語系保留結構，不宣稱已翻譯。舊`visual-v2/?view=city`轉到新頁並保留合法審稿參數。

新城池概念圖以原角色加清楚的八字鬍，保留皇冠及下巴短鬍子；止觀黑白貓與三花貓不改。新圖原生1672×941完整顯示，不裁切、不稱原生4K；角色與門樓仍未全部拆成獨立動畫稿。預設依實際閱讀紀錄顯示；`?review=all`為明標、不寫存檔的完整配置審稿。港口旁的小城池入口依作者本輪結論留待後續美術，不新增到海圖。

完成回饋改為小型新部件／原書縮圖＋簡短文字；主要「繼續下一本」、次要「看看城池」。不再嵌入整張城池或強迫先看城。六處最後一步且前三本確實齊備才提示第一段旅程完成；十四本完成仍只計十四本。城池續讀保留實際部分閱讀／重讀位置，部件的「重新閱讀」明確從該本開頭。收藏完成條件、橋接、唯一完成集合與route核心本輪均未改。

本輪Chromium驗證通過：5尺寸×3頁共15次固定導覽／捲動後入口、5尺寸×14標牌共70次原生部件點選、六門與全幅圖框／引線對齊、標牌開關／放大／無水平溢出；原生五陰第0→3步、重整與旋轉、城池續讀第3→4步，已讀重讀仍保留頁碼與完成數。實際按Next走完四聖諦29步，末頁到達不計、明確完成才得1／14，精簡回饋可直入五陰；另外隔離存檔測末本明確完成到14與可選城池入口。619個原書／來源、核心store／route／bridge、首頁及SEO保護檔對起始HEAD逐位元不變，原46線不變。無JS／本機HTTP錯誤。

舊worldmap-v4檢查同步新城池／精簡回饋介面，另以兩尺寸10個城景／6個回饋隔離存檔驗證原取得條件、先得角色等待與自動安置、舊入口合法審稿轉址。全站SEO15頁／sitemap／robots／Google原件、JS語法及diff檢查通過。新輸出有線／無線3840×2160皆為瀏覽器重繪截圖，不是原生4K插畫；舊版輸出留作歷史。

新圖來源與SHA、實作及待補分層見`docs/play/city-entry/`；本輪可重跑驗收及截圖見`docs/previews/play-city-entry/`及`scripts/check-play-city-entry.py`。前輪全14本1192步及前三本198步完整驗證仍作未變原稿的證據，本輪不為美術改版重跑全部原書。實機iPhone／iPad Safari、原生手勢及GPU效能未測。

試閱：專案根目錄執行`python3 -m http.server 8765`，開`http://localhost:8765/play/worldmap-v4/`及`http://localhost:8765/play/city/`；完整城池畫稿加`?review=all`。沒有公開預覽，不能把正式站預定路徑當成已發布；本輪無發布ZIP或Notion寫入。

---

# 山海世界map-v4、閱讀路線r3與貓角色城池（2026-11-22，待確認、未發布）

本輪附件檔名雖為v1／v2，實際正文是2026-11-22-map-v4及2026-11-22-r3，已完整閱讀、原封留存與SHA記錄於docs/play/worldmap-v4/handoff/。使用者最新說明優先：地圖無鎖頭、未解鎖用薄霧、六念改木造；城主同主角橘虎斑外觀加皇冠／短鬍子／披肩，止觀雙使為黑白貓與三花貓。沿用preview/journey-visual-v2及草稿PR59，起始4f4e1fd乾淨；fetch後main與origin/main均b9a0dad2。未授權合併或正式部署。

新增play/worldmap-v4/。世界1600×900同矩形縮放／平移，七覺支上排y108、五根五力下排y243；信／念／勤／定／慧x432／672／912／1152／1392。左側兩總覽改卷軸；信欄無信覺支／正信橋。中段為湖灣、木造六念燈塔、鏡影林、花田、竹林／船塢／靜水庭園、雙湖、輪庭、法輪及馬車驛站；八正道因素從山／上方島排移至下方半島四組橋y810，公路西段卷軸沿用同一本。新版32地標及3個輔助地景仍只歸14本，原NODES32／EDGES46逐位元保留；合併概念的20個成員以明示sourceParentId相容ID列出，不冒稱既有個別ID或新增法義邊。直接相鄰與同書地景提示分開；有線／無線同底圖、同標籤與同錨點，只有線層開關。校正文字「喜・息・定・捨覺支」「安那般那與止觀」及完整東側名稱。

play/route/將路線、獎勵、擺放與已知／已開書名及動畫記錄分開；十二因緣第4，七覺支第13，四向四果第14。唯一完成集合仍為既有sutrazen.play.collection.v1的completed，不重設／重排／複製紀錄；sutrazen.play.v1保持獨立。新metadata只存書名知悉與演出記錄，不存完成或頁碼。主按鈕續讀實際activeBook的有效書籤（含重讀）；routeStatus.nextBookId仍推薦路線中第一本未完成書。只有正式末步完成才計一次，選書／開書／返回／到末頁不計。自由先讀末本只完成該本；positions末本0也是已知。主線前13本揭曉末本，已知書名不遮回；全14本才開終章條件，未造第15本。

一書多地標與亂序閱讀由固定ID集合推導。八正道完成只活化公路／驛站／橋／溪湖，四正勤花田獨立；兩本皆完成才追加灌溉。完整城喻依五陰、六處、八正道、四念處、安那般那五ID，不硬寫第9關；已得但缺城體／城門的角色先預覽，補齊後自動安置。終章頁只呈現作者已給方向及核對的SA262經句，完整終章演出尚未製作，implemented:false明記。

城池改貓角色新圖、獨立透明法輪木碼頭；SN35.245城喻對應／原幾何圖／漢巴差異保留。真實完成四聖諦→碼頭，五陰→城體／四大／皇冠短鬍子城主，六處→六門；念守門人、止觀雙使、道路及如實消息各依其實際完成與擺放條件。城景預設讀實際collection，另有明標不寫進度的審稿切換。全部圖路徑按模組解析，可在新地圖完成回饋重用。背景人物／門樓仍以羽化預留層管理，非完整獨立動畫素材。

必要的小幅橋接：play/collection/reader-bridge.js僅對新collectionReturn=worldmap-v4參數切換返回網址與文字；其餘normalized bytes與4f4e1fd一致，正式末頁完成／保存程式不改。新地圖讀完會返回真實城景回饋並繼續下一本；普通collection仍回舊書架。書架排列保留，但「下一本」依r3推薦，導覽連到新地圖。十四本HTML、原圖／口白／經文與共用操作、舊v1及collection store逐位元保護，原首頁／心智圖／SEO／Google／Pages main:/不改。

新無字母圖原生1672×941，四張區域細節圖各1672×941，城池1536×1024，木碼頭RGBA1536×1024，原件與SHA見generated-assets.json。另輸出有線／無線各3840×2160實際網頁截圖，文字由網頁重新描繪；這是瀏覽器輸出尺寸，不是原生4K插畫。四區另生圖與母圖有差異，沒有拼接或作互動座標；完整同構圖原生4K與正式分層素材仍待補。新標牌／群組／操作文案集中於text.js，zh-Hans/en/ja只留結構、不冒稱全書翻譯。

驗證：r3全部16384個完成子集、13組語意情境、舊key保留／末關知悉／組合不循環通過。實際新主流程按Next走完29＋54＋115＝198步，各末步後真實城景stage1／2／3及十二因緣推薦正確；第5步重整與返回續讀、手機旋轉、自由四禪第5步主按鈕續讀、已讀重讀不重計、普通collection／獨立閱讀回歸通過。五尺寸32地標、46來源線／共同底圖與錨點、同欄四橋、無鎖頭／迷霧／標牌、14城池來源熱區與亂序安置、花田四組狀態／末關六組狀態、壞檔／不可用儲存仍可閱讀通過；無JS／本機HTTP錯誤。前輪1192步完整驗證保留，本輪未重走未變內容。實機Safari／GPU效能未測。scripts/check-play-worldmap-v4.py、check-play-route-r3.py、play/route/check-route.mjs、SEO --check、JS與維護檔diff檢查為本輪依據（原封路線附件末尾空行提示保留，不改作者原件）；詳docs/previews/play-worldmap-v4/。

試閱：根目錄python3 -m http.server 8765後開http://localhost:8765/play/worldmap-v4/，自由模式加?mode=free；原v2比較保留，新城池入口../visual-v2/?view=city。無公開預覽；正式站未發布，無發布ZIP／Notion改版寫入。

---

# 繪本旅程美術比較：兩版地圖、俯視城池與精裝書封（2026-11-21，待確認、未發布）

作者提供六張參考圖並要求試畫供選擇，未授權正式發布。本輪延續preview/journey-visual-v2及草稿PR59，基準dedc066；起始工作樹乾淨，origin仍為Sutra-Zen/sutra-zen.github.io，main與origin/main維持b9a0dad2。不得沿用其他任務的發布授權。

互通海圖可切換原水彩／塔防地景／奇幻世界，預設塔防地景；移除「相關內容大陸」可見標題，不刪陸地、主題或來源資料。新全景1672×941與1448×1086完整顯示，依原圖比例分別校準32個互動位置與道路，不以cover裁切後套舊座標。原圖32鍵／33來源實例／46關係資料保留，活動仍31個主題／32入口，八正道兩入口仍共一本；定群三山與右下道回左道路維持。新背景沒有烙入中文，主題、線層與按鈕仍由網頁提供。

城池換成1536×1024俯視遊戲概念圖，無棋格／紅藍戰鬥區；實際核對六門、四大廣場、守門者與雙使者後校準13個法義熱區。SN35.245對應與原工程配置／漢巴對讀保留；人物熱區避開臉部。初始較淡、道路亮起、廣場亮起及六門燈光四狀態只供審稿，不寫入進度。修正直接開?view=city時桌機全景隱藏熱區的初始狀態不一致。

收集書架保留既有樹屋背景。未收集為直立布面裝幀、金色原主題圖示／法輪、書脊／金框／編號及書名；已收集使用目前首頁各書插畫縮圖與下緣暗色書名。滿版直式取景只作用於封面縮圖，沒有修改原圖檔或閱讀器的完整原比例。兩種狀態依真實完成集合顯示，沒有加假完成按鈕或封面樣式切換器。收集／前三本旅程的存檔、完成條件、續讀、經文、原閱讀器與原網站逐位元保留。

實測兩個新畫風×五尺寸共320次節點原生點選；31主題／32入口／46關係、主題資源與畫風保留、定位／全景／開關及無區域標題通過。俯視城池五尺寸共65次法義熱區點選、六門與四狀態通過。書架五尺寸×未收集／部分／全收集15個測試狀態，封面比例與書名無截斷；部分／全收集截圖為隔離瀏覽器的QA存檔示意，並非作者真實紀錄。另實際點完四聖諦29步（第5步重整續讀）再按完成，確認只解鎖該書；已讀重讀第6步→7→重整／返回保留。舊三本進度及無關儲存鍵不變，無JS／HTTP錯誤，沒有水平溢出。前輪1192步全書驗證保留，純美術修改不重複全走十四本。

scripts/check-play-art-directions.py及既有network／continent／visual-v2相容檢查通過，舊三檢查的本輪報告留/tmp以免改寫歷史截圖；SEO --check、語法及diff檢查通過。新報告與實際截圖見docs/previews/play-art-directions/，新素材原件／尺寸／SHA見docs/play/visual-v2/art-direction-generated-assets.json。實體iPhone／iPad Safari及正式GPU效能未測。

新地圖、城池仍是生成概念畫稿，不稱作者已確認的正式分層原畫；山、門樓與人物仍在整張背景中，正式獨立動作／拆層待確認。play/首頁、正式心智圖、十四本內容／圖片、SEO／sitemap／robots／Google原檔與Pages main:/不改。根目錄啟動python3 -m http.server 8765後開/play/visual-v2/?style=terrain、?style=world、?view=city或shelf.html；無公開預覽，正式站未發布，本輪無發布ZIP／Notion改版寫入。

---

# 相關內容長條大陸、主題山群與十四本收集書架（2026-11-21，試做未發布）

作者最新要求優先：移除可點的「相關內容」小島，下方橫排改為一塊長條陸地，每個主題為山峰；定群安那般那與止觀／四如意足／四禪為三峰群聚。右下道／八正道入口沿陸地道路接回左側道路。沿用preview/journey-visual-v2及草稿PR59，無合併／部署授權；正式main仍b9a0dad2。

新增透明連續海岸大陸、四款山峰圖集及空書架水彩背景，仍是待確認的概念美術。原32鍵／33入口來源證據不改；場景實際移除相關內容按鈕，成31唯一主題／32可點入口（八正道兩入口同一本），其中下排15山峰、上方17島嶼。原相關內容的連線成區域接觸，標題改為相關內容大陸；未刪其他互通關係。大陸有西側相連半島；道回道路改為曲線土路，取樣點皆在透明地層的實際陸地範圍，非跨海直線。主角維持無燈籠握槳旅人。

新增play/visual-v2/shelf.html可操作收集書架：十四本未收集時顯示初版13個鎖頭SVG／第01法輪，末步明確按完成才解封面，換成現有首頁書架真實縮圖。任意閱讀一本只計該本、重讀不重複；十四本全收集才顯示總收集完成。所有書仍可讀，鎖頭是成就狀態，不封鎖原站。原圖／字幕／經文／操作與語系限制保留，不以新圖改寫繪本。

必要整合：play/collection/catalog.js／store.js／reader-bridge.js／reader.css，十四本HTML各只新增單一選用module（?collection=1才啟用），其他原內容及程式逐位元／資料雜湊保持。原前三本journey bridge與sutrazen.play.v1都保留；新收集採sutrazen.play.collection.v1，含version、positions、completed去重集合、activeBook。獨立閱讀模式無新介面；收藏模式左上回收集書架，保留原經／地圖／經文按鍵。七覺支按36段口白＋結語37步保存(page,cue)，全14合計1192步；catalog totalSteps為導航metadata。已收集書重讀中途可續讀。

支援自動位置、備份／確認還原、確認清除，錯誤備份保留現狀，毀損或儲存不可用說明後仍可讀；不使用localStorage.clear，不動舊旅程／其他資料。沒有由開書／目錄／最後頁抵達自動計完成，也沒有假完成按鈕。未自動猜測遷移原三本完成紀錄，兩種紀錄分開保留。UI文字與原經內容分離，收集畫面繁中，其他語系未對外冒稱完成。

十個既有繪本建置--check及全站SEO通過。現有建置器不產生book/index.html，無需改其原稿模板；七覺支離線包建置器僅在離線副本去掉未打包的collection script，避免缺檔。已/tmp排演ZIP CRC與script存在，正式downloads包／manifest雜湊不改。

驗證：實際逐頁Next完整14本1192步，再明確完成；先單獨讀第14本僅得1本，之後全14封面解鎖。原資料雜湊、獨立模式、每本手機／平板／桌機5尺寸與旋轉、重讀續讀不重計、目錄／重整／返回不計完成、備份還原／無效資料／壞檔／不可用儲存／舊key保留均通過。地圖5尺寸逐點32入口、31鍵、15山峰／3定群峰、移除相關內容島、道路端點與陸地位置、無中心遮擋／外部溢出通過。無JS／本機HTTP錯誤；實機Safari及裝置原生手勢未測。scripts/check-play-collection.py、check-play-continent.py及更新後舊視覺檢查可重跑。

完整功能／存檔／舊紀錄界線詳docs/play/collection/README.md；地圖詳docs/play/visual-v2/CONTINENT.md，素材dims／SHA見continent-generated-assets.json。實際截圖／報告見docs/previews/play-collection/、play-continent/。本機HTTP下開/play/visual-v2/與/play/visual-v2/shelf.html；無公開預覽，不能聲稱正式站已上線。本輪不發布、不做正式版ZIP或Notion改版寫入。

---

# 旅人不持念燈籠、原心智圖改為互通群島（2026-11-21，待確認、未發布）

作者最新說明優先：三十七道品皆重要，主角不再抱念燈籠；海圖應保持原心智圖的多方向互通，閱讀導覽大致呈反向L，由右下四聖諦，苦的五陰／六處、集的十二因緣等，走向左上五根五力／七覺支。本輪延續preview/journey-visual-v2及草稿PR59，不合併／部署；v1及正式站不改。

新增透明中性划船小貓、四種小島圖集與水彩海面；活動v2全部boat()及頁腳改用握槳新稿，移除道具念字。S11僅作面容毛色服裝參考，舊燈籠PNG及過去截圖只存歷史，不再由活動場景載入。城喻「守門者＝念」是另一角色的經典對應，保留不刪。正式角色與動作尚待作者核定；原繪本插圖未重繪。

預設畫面為互通海圖，原十四島構圖留作比較。network-data.js核對原32個主題鍵、33個可點實例（八正道兩處入口同一本）、46筆原DOM連線／共框關係，保留原像素位置與來源證據。network.js另設DISPLAY展示間距使每個節點變為可點小島，尤其展開四聖諦內部小格，避免五陰六處重疊；不能宣稱逐像素複製原DOM或每條關係都是經文明文因果。原共框連線使用群組接觸點；原道回道路的方向保留。

金色路線只作閱讀建議，與淡色原圖對讀／群組水路分層，後續十一本文獻順序仍可調整，沒有改v1前三本解鎖。點任一島可進對應既有專頁及完整繪本；點四念處或「看念的互通」，念根念力／念覺支／正念／四念處等縱向主題與相鄰連線亮起，可從對讀按鈕切換。沒有把相同書本的新入口當作額外完成冊數。

五尺寸1280×900、390×844、844×390、768×1024、1024×768實測33入口逐一實際點擊，按鈕中心重疊0；念鏈對讀／原專頁原閱讀器連結／航線與互通開關／定位／清除選取／全景與平移均通過，所有活動主角不載入燈籠版；零localStorage寫入，無JS／本機HTTP錯誤。66個v1／前三本／首頁SEO保護檔對5056201逐位元相同，原三個視覺分頁也回歸通過。scripts/check-play-network.py與check-play-visual-v2.py可重跑，截圖與報告見docs/previews/play-network/。實機Safari未測。

本機根目錄HTTP下開/play/visual-v2/。NETWORK.md記原圖來源與閱讀航線界線，CHARACTER.md記角色新規格，network-generated-assets.json列新圖尺寸／alpha／SHA。無公開預覽、未發布，正式main仍b9a0dad2。

---

# 繪本旅程第二輪視覺提案（2026-11-21，待確認、未發布）

作者要求從網站卡片／幾何城圖轉為童書冒險視覺；本輪只做可檢查方案與預覽，不覆蓋功能原型或正式站。從PR58原型5056201延續preview/journey-visual-v2；最新main仍b9a0dad2且起始工作樹乾淨。新增play/visual-v2/，保留原play/首頁、app、存檔、解鎖、閱讀橋接、三本原稿、經典對照、原網站首頁與SEO／Pages。

已用指定七覺支S11中央橘貓作畫風／角色參考，生成四個待確認概念PNG：群島全景1536×1024、六門城池1536×1024、小貓木船透明圖1536×1024、花草增長透明圖2172×724。完整畫面取代三卡／工程圖的主視覺；HTML提供十四主題標記、前三島閱讀彈窗、十一後續旅程說明、關聯線、13城池探索點（止觀合一對）、可展開法義、初始及三次返城演出。圖內無新增中文，念字與標籤為網頁文字。模擬狀態不寫入或清除原型儲存；原工程圖仍從參考入口查看。

原未讀小圖已從最初書架6aaa1af抽取十三個原SVG，保留原幾何並記錄來源雜湊；四聖諦原無同系列圖，以法輪另作標記。十四島關係由實際心智圖核對，非十四關線性修證流程；只有前三島示範閱讀路線。其餘原書均已可讀，不能寫成原書未上架。

這些是作者尚未核定的構圖／角色概念，不稱正式分層美術。背景中的門樓、人物與原有植栽仍扁平；小貓與船同圖。待補正式母圖3600×2200／城池2400×1800，以及對齊門樓／守門者／雙使者／空船／角色新姿勢和動畫層，詳docs/play/visual-v2/ART-BRIEF.md。COMPOSITION.md保留原構圖建議並明記當前畫稿的14島／13城池實際座標，generated-assets.json列實際尺寸／透明度／SHA。尚未將新畫面接管原遊戲閱讀及進度，確認後才完整改版。

驗證：scripts/check-play-visual-v2.py核對66個原型／前三本／首頁SEO保護檔對5056201逐位元不變，十四本現圖與十三原SVG來源／雜湊通過；手機直橫、平板直橫、桌機五尺寸下十四島彈窗、十三城池說明、狀態／圖層／全景／定位及完成回饋正常，模擬零localStorage寫入，無JS／本機HTTP錯誤。只重驗新視覺及保留界線，不因全圖預覽重抄198頁。實際截圖／報告見docs/previews/play-visual-v2/；實機Safari與正式GPU動畫效能未測。

本機根目錄啟動python3 -m http.server 8765後開http://localhost:8765/play/visual-v2/。沒有公開預覽，不將預定網址寫成已上線。不合併main／發布Pages，本輪無發布ZIP／Notion改版寫入事項。

---

# 佛法繪本旅程第一版試做（2026-11-21，未發布）

本次作者明確要求完成可操作試做，不自行合併main／發布，不能沿用其他任務授權。從最新main b9a0dad2建立feat/picture-book-journey-v1，起始工作樹乾淨、origin對應Sutra-Zen/sutra-zen.github.io。新區域play/獨立提供海島閱讀路線、開始／續讀、可略過短過場、三本末頁明確完成、城池0–3狀態回饋、逐本解鎖、第一段旅程完成與原書架入口。

前三本沿用實際原閱讀器：四聖諦29頁、五陰54頁、六處115頁，共198步；沒有另寫簡略故事。各book/index.html只新增一支opt-in module引用，移除此行後與基準逐位元相同；原pages/scenes雜湊亦相同。只在journey參數啟用進度橋接，遊戲模式重用左上回簡介slot為回旅程以免壓口白；原經／回修道地圖／本頁經文、獨立模式、快按、旋轉及原圖經文保留。首頁、#map-heading、14本書架32節點、全站SEO／sitemap／robots／Google原檔與Pages main:/都不改，沒有新增首頁宣傳。

依序／自由模式各存位置，重讀另記replayBook以確保三本完成後仍可中途續讀；完成冊數僅依序且按末頁完成時計入一次；自由選第三本不補完前兩本。進度命名空間sutrazen.play.v1，支援續讀、備份／確認還原、確認清除且不動其他localStorage。格式或儲存異常說明後仍可閱讀；儲存不可用時跨頁與重整不保證續讀。介面繁中完整，另三語只留結構、未提供假完成選單。

城池主採SN35.245六門版，六門／念／止觀雙使者／四大廣場／識／涅槃話語／八正道路完整配置可檢查；漢譯1175四門四識住、四守門四念處另對讀。大正藏使者「正觀」保留，CBETA止／正校記獨立列出。原資料／英譯另一編號已核對固定SHA，直接外站有代理403，沒有宣稱被擋頁面已載入。城池變化僅閱讀回饋，不代表證果、斷結或全14本修學完成。

角色暫引用已核對的七覺支S11原圖中央抱念燈籠小橘貓肖像（SVG視窗，未改原圖），航行用船與念燈籠標記；海島／城池是簡單示意美術。未假稱完成去背立繪或正式場景。待補同角色站立／坐船／探索／閱讀立繪、正式水彩島城及五蓋／波旬演出；不影響前三本完整流程。規格、存檔／語言架構與本機試閱詳docs/play/README.md，來源詳SOURCES.md。

scripts/check-play.py已實際點按走完三本198步及自由六處115步，完成／續讀／重整／原經往返／重讀不重計／自由不計／鎖定直接URL／下載還原確認／壞檔及不可用儲存均通過。手機直橫、平板直橫、桌機五尺寸與旋轉通過，原首頁實際節點三卡／14本／原閱讀入口通過。無JS及本機HTTP錯誤；原正文資料與保護檔逐位元核對、SEO --check及diff檢查通過。截圖／報告見docs/previews/play/。實體Safari及YouTube播放未測，無可用公開預覽服務；本機python3 -m http.server 8765後開http://localhost:8765/play/。預定正式/play/尚未上線，本輪不需發布ZIP或Notion改版寫入。

---

# 安那般那調身卡補完整八法（2026-11-21）

依作者要求，將流程中過短的「以坐姿、肩頭、眼舌與呼吸等細節」改為八項完整白話說明：足、眼、身、肩、頭、齒與唇、舌、息。逐項依本頁既有《菩提道次第廣論》卷十四引述蓮花戒《修次中編／下編》的原文整理，使用編號清單；齒與唇合為一項，沒有誤增為九法。原文來源卡、16項主線與原書119頁不改。新增樣式僅作用於anapana-flow內的posture-eight清單，保留原手機／平板排列與來源連結。沿用上一輪已授權的流程發布維護範圍及main:/ Pages；360×800、390×844、768×1024、1024×768、1280×900實測八項完整、無溢出及來源錨點通過，無JS／本機HTTP錯誤；build-anapana.py --check及build-seo.py --check通過。CSS快取版本同步更新。報告與截圖留存/workspace/artifacts/anapana-eight-posture/；合併SHA與發布／ZIP驗收記於本次PR。實體Safari及影片播放未測。

---

# 安那般那導讀流程正式整合（2026-11-21）

作者已明確回覆「可發佈」，取代下方二稿僅預覽的限制。沿用preview/anapana-study-flow及PR #56，由main 0e3d7cdd的正式安那般那專頁整合已確認設計：綠色主線禪定準備→十六勝行，右上直接顯示完整四組16項及原翻譯備註；暖色調身／數隨止兩張卡平行補充，不另加必經修證關卡。原獨立表格不再重複，原章節入口集中於流程底部。

正式修改anapana/index.html，新增局部命名空間anapana/study-flow.css；沿用既有header、唯一H1、封面、影片與來源卡。十六項、四組名稱、順序與備註核對原表相同；video段落起至頁尾逐位元保留，經文與來源資料／繪本119頁／圖片／閱讀器及首頁14本32節點不改。現有SEO與Google驗證檔保留，建置器讀取既有導讀後僅更新來源卡與SEO，不會覆蓋新流程。

五尺寸360×800／390×844／768×1024／1024×768／1280×900檢查無溢出、截字、卡片排列及手機閱讀順序，四個原入口及來源／延伸錨點通過；15條S02／S04／S08繪本往返路徑、前後翻頁及回導讀正常，無JS／本機HTTP錯誤。build-anapana.py --check與build-seo.py --check通過。實際整合截圖與報告見docs/previews/anapana-study-flow/release-*；實體Safari與YouTube播放未測。沿用Pages main:/，精確mergeSHA、Pages同SHA、正式站與完整固定版本ZIP證據記於PR #56。

此工作環境未提供Notion工具，尚未寫入；待補記文字見docs/releases/anapana-study-flow-notion.md。

---

# 安那般那導讀路線二稿：完整十六項整合右上，僅預覽（2026-11-21）

作者要求先畫符合來源層次的流程初稿、不要發布；本輪進一步建議把原十六勝行表格整合到流程右上。main基準0e3d7cdd，試作分支preview/anapana-study-flow、草稿PR56；只有docs/previews/anapana-study-flow/與本交接紀錄更新。anapana正式導讀、繪本、經文／圖片／建置／SEO及Google驗證檔都不改，不得沿用前一輪SEO發布授權合併此稿。

綠色經典主線及暖色調身／數隨止平行補充維持。二稿將原表四組、完整16項與心悅／心定對照心喜／心攝的原備註，整合進右上十六勝行卡片，分四列顯示；移除草稿下方的獨立表格。逐一比對4組名稱、16項順序與備註文字均相同，沒有新增改寫經義。手機保持主線完整顯示後再列補充；圖示仍表示導讀／參照關聯，不另訂數隨止→觀→十六勝行的必經程序。

來源核對與第一稿相同，詳預覽README（含已核讀PDF134–135）。1200×1200／768×1024／390×844重新檢查完整詞項、備註、卡片無截字／溢出、對齊、閱讀順序與延伸錨點，均通過，無JS／本機HTTP錯誤；實體Safari未測。build-seo.py --check通過。作者確認前不改正式站、不合併main、不發布Pages。

---

# SEO與Google驗證檔：2026-11-21-r2（2026-11-21）

從最新main db3a882b4ec2d4dd7647cbbeef9f4622a214cb84開分支feat/seo-2026-11-21-r2，origin新專案正確、原工作樹乾淨。先讀附件README／seo_pages.json，再讀專案規則。作者最後補充明確授權SEO與Google驗證原檔一起提交發布，取代包內只試閱指示。沿用Pages main:/及管理流程，發布後精確mergeSHA／正式站證據記於本次PR。

15頁只改head：title、description、canonical採原交接JSON逐頁文案，補OG／Twitter及只含真實WebSite／WebPage的JSON-LD，分享圖只引用既存檔。四個實際產生guide head的程式（安那般那／四禪／五根五力／七覺支）最後使用共用site_seo.py；其餘11頁是手維護HTML、既有book建置器不覆寫guide。建置用build-seo.py，檢查用check-seo.py。完整來源追查、逐頁清單及維護指令：docs/seo/README.md。

新增根目錄sitemap.xml（精確15個canonical、無lastmod）與robots.txt（原無規則，維持公開存取，不另改模型訓練政策）；未變更reader的noindex／canonical／標題。根目錄googlee0c995331ec518ae.html原件53bytes，SHA256 05359eab14af74d4d9e757d4c4c179ee57c1c455986e09c0bebbdee637f86225，直接複製附件、不改任何字元或換行。後續不可刪除；建置--check會檢查存在與原雜湊，規則已寫入AGENTS。

所有15頁正文（含經文／書架／32節點三入口／影片與深連結）逐位元不變；reader／原圖／分鏡／CSS及PR54四正勤來源JSON保留。15頁metadata唯一且符合JSON、body與非SEO head保留、sitemap XML／URL集合、robots政策保留與冪等性、原Google檔、本機18網址及14張分享圖HTTP／解碼、4guide重建輸出與4個既有--check均通過；15頁Chromium DOM head／原H1及JS／本機HTTP無錯。報告docs/previews/seo-r2/validation.json。純head變更，未重跑所有繪本每頁；實體Safari未測，首頁CDN測試用既存副本，影片播放未測。

本輪依作者分工，不操作Notion、vidIQ、Google帳戶或Search Console介面的驗證／提交sitemap／成效追蹤。VideoObject缺少完整可信上傳日期等資料，保留為後續選項；不編造日期、FAQ或收錄保證。網站檔案發布成功與Google帳戶已完成驗證／搜尋已收錄是分開的狀態。

---

# 四正勤專頁SN49經號標題修正（2026-11-21）

依作者提供的SuttaCentral固定commit482faafde8b9c52689d7926004706939f573cf2b中譯HTML，核對「相應部49相應 23－34經」及「力量所作等經十二則」；官方檔HTTPS200，且與既存canonical/sn49.23-34.html逐位元相同。將right-effort/index.html的來源標題改為「《相應部》49.23–34（節錄）｜依戒修習四正勤」，同步docs/right-effort/verified-sources.json的同名title。現有建置腳本沒有此標題常值，build-right-effort.py只建置繪本資料，不改其程式或繪本。原始交接／影片錄文中的SN49.23–24保留，未當作本次專頁標題誤植改寫。

兩份實作檔逐位元比對，均只替換一次標題；經文節錄、莊春江譯者資訊、中譯sn49.23-34/zh/zhuang及巴利sn49.23/pli/ms按鈕、六格小花、所有繪本／圖片／CSS不變。既有建置--check通過。360×800、768×1024、1024×768檢查標題換行與無水平溢出，兩按鈕實際另開分頁並發出原網址請求；無頁內JS／HTTP錯誤。

**尚未完成外站載入驗收：** 本環境連suttacentral.net兩網址均被代理網路政策403封鎖，Chromium報ERR_TUNNEL_CONNECTION_FAILED；不得宣稱SuttaCentral實際內容已正常載入。已向作者提出允許suttacentral.net並套用後重試的需求。報告／截圖見docs/previews/right-effort-source-title/。沿用main:/ Pages；本次合併SHA、正式本站標題與固定版本完整ZIP結果記入PR。實體Safari未測。

此工作環境未提供Notion工具，尚未寫入；待補記docs/releases/right-effort-source-title-notion.md。

---

# 安那般那繪本出處補完整書名及卷次（2026-11-21）

依作者要求，將繪本S10之Q32–Q38的「蓮花戒大師《修次中編／下編》（《廣論》引述）」改為「蓮花戒大師《修次中編／下編》（《菩提道次第廣論》卷十四引述）」。修改verified-sources.json的readerSourceLabel並由既有建置器同步14頁；更新book-data.js快取版本。導讀原已使用完整名稱，維持不變；119頁、118段口白、41筆原引文、時間、分鏡、圖片及閱讀操作全部保留。

建置／--check通過，資料逐位元比對確認僅14個source字串變動。390×844、768×1024、1024×768共42個受影響頁狀態，來源換行、無水平溢出、前後翻頁與經文視窗通過；無JS／本機HTTP錯誤，實體Safari未測。報告與截圖見docs/previews/anapana-guanglun-source/。沿用本書已發布內容的維護授權與既有main:/ Pages流程；實際合併SHA、正式站與固定版本ZIP記入本次PR。

此工作環境未提供Notion工具，尚未寫入；待補記docs/releases/anapana-guanglun-source-notion.md。

---

# 全部心智圖節點統一三張配色入口（2026-11-21）

作者已確認配色試排並明確要求「每一個心智圖點下去的介面都改成這樣，可直接發佈」，取代上一輪只試閱的限制。由最新main02843bde延續試排，實作分支feat/map-topic-resource-cards。32個可點節點皆採專頁說明／翻頁繪本／繪本影片三張卡片，淡紫／淡藍／淡珊瑚配色、左側色線及圖示底框沿用已確認設計。

30個主題及子項直接連到對應十四本的導讀、閱讀器與原YouTube網址；道路總說與相關內容總說是跨主題總覽，前兩卡明寫「從書架選擇主題導讀／繪本」，影片卡連既有影片區；點擊頁內入口會關閉彈窗。原精簡說明、所有標題、原影片網址及新分頁行為保留，書架／十四本／插圖／經文／首頁iframe不改。共用樣式改名map-topic-resources.css，新增節點應沿用此結構。

五尺寸160個彈窗狀態、70條十四本導讀／繪本／圖片／前後翻頁／回地圖路徑及總覽跳轉／影片新分頁通過，無JS／本機HTTP錯誤或水平溢出；原說明逐節點核對、所有相對入口及首頁腳本語法亦通過。驗證與截圖見docs/previews/map-topic-resources/及scripts/check-map-topic-resources.py；正式發布後同SHA的Pages建置、正式站驗收與完整ZIP結果記於本次PR。實體Safari與YouTube實際播放未測；Chromium測試使用既存CDN副本，正式站透過TLS驗證的HTTPS回應驗收。

此工作環境未提供Notion工具，尚未寫入。待補記文字：docs/releases/map-topic-resources-notion.md。

---

# 修道地圖三入口試排，先截圖確認（2026-11-21）

作者明確指定此為重要改動，先試作截圖、不要發布。從最新main02843bde建立preview/map-three-entry-links，僅五根五力總說試排三入口：專頁說明（完整導讀與經典出處）、翻頁繪本（依自己的步調閱讀）、繪本影片（連續觀看，免翻頁）。上方三段精簡說明完全不改，原影片ID與新分頁行為保留，導讀／閱讀器直接使用既有路徑。三張同樣式可點卡片，以圖示／箭頭區分，取代舊影片大框及合併導讀繪本連結。

作者後續要求加底色：專頁說明淡紫、翻頁繪本淡藍、繪本影片淡珊瑚，搭配同色細邊／左側色線與白色圖示底框。只調整樣式，文案、排列、連結及其他內容不改；五尺寸已重新檢查並更新截圖。

map-topic-preview.css僅作用新卡片；dhammaData其他節點、所有十四本與iframe不動。五尺寸與三連結／關閉／無溢出驗證通過，實際截圖與限制見docs/previews/map-three-links/。影片未測實際播放、實體Safari未測。作者確認前不得將此試排合併main或發布，不能沿用前幾輪發布授權。確認後再決定其他節點完整套用，不將單節點prototype當成全站已改。

---

# 四不壞淨第1幕原圖錯字替換（2026-11-21）

作者以1107518A-B643-40F7-82D9-CE2C27F541A9.PNG.zip提供修正隨法行／隨信行／須陀洹／涅槃的正式圖片；PNG1679×937、4104182bytes，SHA-256 e0f4cd6a9d12e19b35aded3ea027a00c6e6d7731ff37b41daf9abd762892245a。直接保留原PNG，未重繪、裁切或轉檔。原IMG_0393.jpeg及原manifest留存，新增replacement-assets.json，image-assignments.json新增S01→assets/S01-corrected.png；建置器同時驗原素材與替換素材。第1幕12頁改用新圖／尺寸，總95頁、原93筆口白及所有經文／時間／分鏡／疊字不改，之前S06僧不壞淨／S07聖戒對應維持。初始HTML圖片及資料快取同步更新。

五尺寸85個S01及鄰幕／收尾狀態，原圖SHA與完整比例、上下字幕／經文、目錄／翻頁／快按／旋轉／讀經／末頁重讀／回地圖通過，無JS／本機HTTP錯誤及溢出。見docs/previews/four-purities-corrected/。依作者持續維護發布授權，以PR合併main並核對Pages同SHA、正式新站圖片／資料與固定版本完整ZIP；實際證據補於PR。Notion工具未提供、尚未寫入，待補記docs/releases/four-purities-image-notion.md。實體Safari未測。

---

# 十四本回修道地圖與閱讀格式統一（2026-11-20）

作者明確要求統一加入回修道地圖並發布。從main a3dc88dc建立fix/unified-reader-map-navigation；前九本補直接返回../../index.html，十四本固定閱讀原經／回修道地圖同一組位置，前三本經文按鈕改本頁經文。共用reader-controls.css以實際scene寬度留出左下兩連結空間，避免五陰等書舊gutter值造成壓文；觸控manipulation及末頁重讀維持。

另實測發現前四本仍把字幕與經文疊在橫式圖上，直式負邊距亦壓圖。這四本及八正道無疊字頁用新增reader-layout.js／共用CSS保留圖外上下欄、完整原比例及響應式量測；八正道原overlay-scene、心經直書、純文字／結語及每書圖中文字／疊字資料均保留。來源／故事／原圖、各書原有JS與CSS、內嵌腳本及styles逐檔不改，不重做內容或閱讀器。早期七本沒有後期圖片放大的差異已在audit記錄，本輪專注共同導航及呈現修正。

五尺寸1115頁狀態、988圖文幾何、70來源／返回動線、70旋轉、58讀經視窗及末頁重讀／快按通過，無溢出、JS／HTTP錯誤。詳見docs/previews/reader-navigation/及scripts/check-reader-navigation.py。七覺支離線ZIP同步共用CSS，29檔CRC／全部雜湊與本機返回入口驗證通過。新書規則加入AGENTS，後續不可再漏返回地圖。

正式網域允許設定已套用；本次發布後核對Pages／managed workflow同SHA、HTTPS原始檔及正式URL瀏覽器動線，證據與固定SHA完整ZIP記入PR。瀏覽器的代理憑證以具TLS驗證的urllib傳送原站回應處理，首頁CDN測試用下載副本；非實體Safari驗收。Notion工具未提供、尚未寫入，待補記docs/releases/reader-navigation-notion.md。

---

# GitHub改名銜接與根網域發布（2026-11-19）

本專案已由原rooneyflower-star/sutrazen-map改名為 **Sutra-Zen/sutra-zen.github.io**，GitHub ID仍1441581789，main基準2ec341a6完整保留十四本與最新安那般那修正。正式網址 **https://sutra-zen.github.io/**，不加舊專案前綴。首次檢查工作目錄/workspace/sutrazen-map、main且工作樹乾淨，沒有丟棄或重設修改；固定掛載名稱保留，origin已更新為https://github.com/Sutra-Zen/sutra-zen.github.io.git。雲端儲存庫設定仍使用相同repository_id，不應因資料夾舊名另建或覆蓋專案。

已讀AGENTS／PROJECT／本HANDOFF及實際程式，核對GitHub Pages API：legacy，main的根目錄/，無CNAME，HTTPS強制，正式網址如上。GitHub管理dynamic/pages/pages-build-deployment，沒有本庫自訂workflow；本次沿用分支PR合併main後自動發布，不更換來源或部署平台。最新確認結果存docs/previews/site-migration/initial-state.json；發布後同SHA建置／workflow與完整ZIP證據記入本次PR。

網站HTML／CSS／JS本身採相對路徑，沒有舊帳號或舊站網址，也沒有需修正的/sutrazen-map/前綴；全部網站程式／原圖／繪本內容逐檔不改。已更新README、AGENTS、PROJECT、維護中的試閱與待補記文件網址，四支舊檢查程式的預設本機網址改為根路徑。原作者交接檔、原始prompt／manifest與已存歷史報告保留，不為改名破壞原始雜湊。

遷移檢查scripts/check-site-migration.py與報告／截圖docs/previews/site-migration/。本機已檢查29份網站HTML、325個相對資產／連結；五尺寸十四本入口、圖片、前後翻頁、返回導讀再回首頁共70狀態通過，無JS或本機HTTP錯誤。管理瀏覽器的外部CDN連線受限制，本機測試明確使用既存Tailwind與下載的Lucide副本，不代表CDN外站驗收。

**直接正式站瀏覽驗收待完成：** 現行環境允許清單只有舊站host、沒有sutra-zen.github.io，實際CONNECT收到403；已請作者在環境設定新增並套用。GitHub API可讀寫／發布，此403不等於GitHub Pages發布失敗。未核准前不得宣稱正式站HTTP／圖片／翻頁已實測，套用後需重試新網域。本機Chromium測試不等於實體Safari。此環境未提供Notion工具，尚未寫入，待補記docs/releases/site-migration-notion.md。

---

# 安那般那：安靜處經文與論師漫畫聚焦（2026-11-19）

依作者對已發布本書的修正要求，S02-P06直接補《雜阿含經》第803經「或入林中、閑房、樹下，或空露地，端身正坐，繫念面前。」節錄，取代原補充說明；已對本庫固定版本原典SHA及文字核對，節錄末標點作句號。來源可從經文區／本頁經文視窗連回既有sa803卡。五筆中部118經標題移除「（影片譯文）」，引文本身不改、不冒署譯者。reader-edits.json保留公開修正，原交接41筆／118段及圖不改。

S10依P03–04／05–07／08–11／12–14依次亮起四欄，P01–02總說全幅；S11依P01–04數息、P05–07隨息、P08–09止三欄聚焦，P10–12收尾全幅。沿用共用76%遮罩、完整圖百分比、放大與旋轉同步；S10小圖的圖外五官標籤只在第三格或總說顯示。既有S04–08遮罩／119頁／12幕／12條疊字／口白／其他來源內容與導讀不改。

驗證腳本scripts/check-anapana-commentary-focus.py：五尺寸595頁狀態、130主按鍵漫畫狀態、35放大／旋轉狀態及來源往返／快速點按通過，無JS或本地HTTP錯誤。報告／橫直式截圖docs/previews/anapana-commentary-focus/。依本書持續發布維護授權經PR更新；實際Pages同SHA與固定版本完整ZIP結果記入PR後才聲稱上線。實體Safari未測。此工作環境未提供Notion工具、尚未寫入，待補記docs/releases/anapana-commentary-focus-notion.md。

---

# 書架說明移除與兩篇導讀重寫（2026-11-19）

依作者指示移除首頁書架冊數與製作中說明，14本書架／連結不改。七覺支原導讀取每幕第一句，造成念等卡片無定義；改為七項完整說明（含意義、修習及白話譬喻），另以文字說明火候／念兼助及覺支生起圓滿。五根五力導讀改為僅五項「根／力」卡片，每項整合SA646法門對應及SA647進一步說明，移除其餘故事分鏡卡；原經來源區保留。

文案存docs/seven-factors/guide-topics.json與docs/five-roots-powers/guide-topics.json，建置器同步，七覺支離線包更新導讀。繪本資料、口白、原引文、程式與插圖不改。五尺寸兩導讀無水平溢出、全部60次卡片閱讀器入口核對；來源區及閱讀器逐檔與原版相同。報告／截圖docs/previews/guide-explanations/。本次承接兩本發布後維護，Pages及完整ZIP結果記入PR。Notion工具未提供、尚未寫入，待補記docs/releases/guide-explanations-notion.md。

---

# 七覺支末段圖片與結語修正（2026-11-19）

同圖在第36段縮小，是共用reader-at-end樣式晚載入覆蓋本書寬度；原結語放在畫面下方不易發現。依作者指示，36段原故事後加入獨立可翻閱的經典依據／走入經藏的起點結語，主按鍵讀到結語才重讀。原12圖與36段／引文完整保留，原稿資料不改。插畫頁寬度以較高選擇器優先級保持最大完整圖，文字結語沿用既有afterword版型。離線ZIP同步。五尺寸驗證第35／36段圖寬一致、結語可見、前後翻閱／旋轉／重讀；實體Safari未測。發布後Pages及固定SHA備份見本次PR。Notion工具未提供、尚未寫入，待補記docs/releases/seven-ending-notion.md。

---

# 七覺支連續閱讀修正與專頁精簡（2026-11-18）

依作者指出第一個覺支像被跳過，從main fe9c5d9建立fix/seven-factors-continuous-reading，承接本書發布後維護。核對book-data.js與原稿：36段口白／時間／16引文區間完全保留，沒有因中斷遺失；問題是主按鍵直接換圖頁，導致同幕後續段落須用另一組控制才能讀到。

- 主上一頁／下一頁、方向鍵與滑動全部改為同一條36段順序，讀完當幕段落才換圖。保留12幅圖與原幕目錄，移除上方獨立換段控制；計數同時顯示36段進度／12圖頁。末頁重讀僅在第36段觸發，不會一進第12幕就跳回開頭。舊scene/page/cue連結與儲存位置仍可用。
- 專頁移除下載繪本按鈕及底部原片經典出處截圖連結；原經來源卡保留，原圖／交接檔不刪除。建置器同步，離線ZIP也更新相同翻頁行為，閱讀器快取已更新。其餘13書／共用檔／首頁／Pages設定不改。
- 本次新回歸以真正主按鍵走完36段，五尺寸正向180、反向180、離線包正向180狀態，逐段核對原口白／時間對應引文及焦點，確認含「第一個，是念覺支」。另驗鍵盤、模擬滑動、旋轉重載與第12幕全部六段、最後重讀。結果及截圖見docs/previews/seven-sequence/；先前舊版測試是直接操作段落選單，未涵蓋主按鍵完整閱讀路徑，不能用來證明此問題不存在。
- 實體Safari未測；離線仍以解壓本機HTTP＋封鎖外部來源驗證。發布後於本次PR核對Pages／公開檔案／固定SHA完整ZIP。Notion工具未提供、尚未寫入；待補記docs/releases/seven-sequence-notion.md。

---

# 第14本《七覺支》發布授權（2026-11-18）

作者明確指示「可直接發佈」。**此授權取代下方第14本的審閱限制，允許將PR #43合併main並發布GitHub Pages。** 發布已驗收的同一版本，只移除導讀／閱讀器noindex、更新正式快取與重新打包相同離線內容；不改12頁、36段口白、16引文區間、14中心疊字及S11聚焦／操作。原13書與Pages設定不改。

- 導讀：https://sutra-zen.github.io/seven-factors/
- 繪本：https://sutra-zen.github.io/seven-factors/book/
- 離線包：https://sutra-zen.github.io/downloads/SutraZen-Seven-Factors-Offline.zip
- PR #43發布後記錄實際合併SHA、對應成功Pages建置、公開檔案／離線包與固定SHA完整ZIP驗證。既有180線上／180離線段落狀態、120放大字框及13書回歸驗收沿用；發布前重核生成／原檔SHA／JS與已驗收內容不變。
- 離線驗收仍是解壓後本機HTTP＋封鎖外部連線，不代表file://直開、實體Safari或iPad下載解壓流程已測；音軌精校及外站畫面亦未驗證。限制隨ZIP與README保留。
- 此工作環境未提供Notion工具，尚未寫入；待補記docs/releases/seven-factors-notion.md已更新為正式發布。

---

# 第14本《七覺支》十二頁試閱（2026-11-18）

從最新main `99b1a1d96169917ad682f8df72649b0da1cd8388` 建立 `feat/seven-factors-review`（草稿PR #43）。本輪只交付預覽與實測，**不得自行合併main或部署新書，不能沿用第13本發布授權。** 正式站仍13本；書架14／七覺支總說的新入口只在本分支。

- 兩包CRC與15份原檔／13圖SHA完整保留於docs/seven-factors/。原稿只有Markdown／Prompt，storyboard.json與scripture-catalog.json由本次逐句整理，保持36段口白與原時間，不冒稱原作者JSON。01–12依原序，08特寫／09坐姿核對，13出處截圖只供專頁來源連結，不額外加入故事頁。
- 依作者指定12頁，每幕一個圖頁；上方新增同樣式上一段／時間選單／下一段切換同頁口白、當時引文與聚焦，主左右／下方按鍵仍切圖頁。最後頁下方放既有經典依據與走入經藏的起點結語、主按鍵回第一頁，不另加第13頁。旋轉與重載保留頁及段落。
- 14條疊字採本書指定的中心百分比錨點，translate(-50%,-50%)是本書正確做法，不套舊書左上規則。覺支字高13%／五蓋與火候9%依完整原圖比例換算cqw，正常／放大同步。S11只加昏沉／浮動，S12原有七牌不重疊。第11幕第4段左42%聚焦、第5段右42%聚焦，中央16%念燈保留，其餘段全幅。
- 16個原片經文區間按時間配對，落實S04／06／10／11同幕換文；解說輕安，引文保留猗息／猗覺分。導讀五張來源卡使用已讀官方固定SA713／714／715／810及MN10原文，影片錄文與原典差異另存REVIEW，不冒署名莊春江。其他13書／共用檔／Pages配置／14影片逐檔不改，根資料只解鎖書架14與追加七覺支總說入口。
- 主分支實際沒有下載／離線程式，本書新增同來源按鈕樣式的離線ZIP，29檔約6.7MB、無CDN／遠端圖片或Base64。含本機啟動腳本與操作說明，外部影片／原經網址仍需網路。不要宣稱沿用不存在的下載器。
- 五尺寸360×800、800×360、768×1024、1024×768、1440×900：180線上段落狀態＋180實際下載ZIP／解壓後離線段落狀態、120個放大字框均通過；書架／地圖、13舊書入口／翻頁／返回正常。追加五尺寸最後結語與最新ZIP內容檢查通過。12頁PDF的36段及16引文全文保留；37張截圖與報告在docs/previews/seven-factors/。
- 離線實測是本機HTTP供應解壓檔並封鎖所有其他來源；file://被管理Chromium政策禁止（ERR_BLOCKED_BY_ADMINISTRATOR），未驗證直接雙擊HTML。實體iPad／Safari、iPad下載解壓流程、外部影片、音軌精校及外部註解頁呈現尚未驗證，不把模擬說成實機。沒有公開互動預覽主機，交付PDF、ZIP與本機HTTP路徑。
- 此工作環境未提供Notion工具，尚未寫入；待補記docs/releases/seven-factors-notion.md。

---

# 五根五力移除片尾出處圖（2026-11-18）

依作者截圖移除繪本第75頁經典出處圖，承接本書發布後維護。74段故事直接接經典依據結語，總頁數75、目錄十幕。原74段口白／時間／引文、五條疊字及專頁經典出處不變；原圖與交接檔留存，不刪除。建置器及校稿PDF同步移除該頁，舊第76頁連結與儲存頁碼落到新末頁，快取更新。本次僅核對五尺寸末頁／翻頁／重讀／舊連結與原內容一致性，實體Safari未測。發布後Pages及固定SHA ZIP記於本次PR。Notion工具未提供、尚未寫入；待補記docs/releases/five-roots-remove-credits-notion.md。

---

# 第13本《五根五力》發布授權（2026-11-18）

作者明確指示「可以直接發佈五根五力」。**此授權取代下方第13本的審閱限制，允許將PR #41合併main並部署GitHub Pages。** 發布已驗收的同一版本，移除導讀／閱讀器noindex、更新正式快取版號，不改十幕、74段口白與時間、14引文卡、五條疊字、來源圖／結語共76頁及原十二書。

- 主題專頁：https://sutra-zen.github.io/five-roots-powers/
- 繪本：https://sutra-zen.github.io/five-roots-powers/book/
- 發布經PR #41；實際合併SHA、對應成功Pages建置、公開檔案及固定SHA完整ZIP驗證，於發布後記入該PR，不以先前審閱檔代替正式備份。
- 先前五尺寸380頁面狀態、25放大疊字及5來源圖放大狀態沿用；發布前重核生成一致性、原素材／原書不變與JS語法，發布後驗證實際公開檔案。不因發布宣稱已完成實體Safari、影片播放、音軌精校或引文版本差異的校勘。
- 此工作環境未提供Notion工具，尚未寫入改版頁；待補記docs/releases/five-roots-powers-notion.md已更新為正式發布紀錄。

---

# 第13本《五根五力》完整試閱（2026-11-18）

從最新main `2376c9cafb4b59e5eeba6aaa2833ec3c900497fc` 建立 `feat/five-roots-powers-review`（草稿PR #41）。本輪要求完成製作、提供預覽與測試；新書先供審閱，**不要自行合併main或部署，不能沿用其他繪本的發布授權。** 同輪安那般那S08遮黑已另經PR #40發布，main仍只有12本可讀；以下第13本書架／地圖變更只在審閱分支。

- 兩包CRC核對後合併，14份原檔與11圖完整存docs/five-roots-powers/；原包沒有README／manifest，本次補充文件與收件雜湊記錄另明標。S01晴天無牌、S03五牌已烘焙、S09風雨版本已目視核對。S04/S05寬1671、S10寬1670，其餘正圖寬1672，原比例保留。
- 新增five-roots-powers/導讀及book/，沿用安那般那上字幕／完整圖／下經文、橫式左右／直式下方按鍵、目錄、讀經、放大、末頁重讀。74段原口白與近似時間完整，另加可放大的原sources.png及共用經典依據結語，共76頁、十幕目錄。
- 五組黑字的x/y完全依原稿，左上錨定於實際圖片：信60/46、精進73/11、念77/11、定77/11、慧64/11。原稿未指定寬度字級，試排寬12%（精進18%）／5cqw，另存overlay-layout；S03不加字，放大與旋轉同步，不聲稱精準還原影片。
- 14張原稿引文卡與逐段配對保留，S02樹根抗風是補充說明；SN48.43中央島河流、SA654棟樑不混用。導讀五張來源卡依官方固定原檔直接顯示，中文優先／古漢譯／莊春江中譯／註解或巴利對照格式同舊書。影片與原典措辭差異另見REVIEW，未自動改稿或把影片文字冒署名莊春江。
- 380個頁面狀態、25個放大疊字與5個來源圖放大狀態通過，五尺寸無水平溢出／本機HTTP或JS錯誤，書架13與原地圖入口、其他12本入口及操作回歸通過。根資料只改五根五力節點與書架13，原14影片、其他節點、12舊書／共用檔／Pages設定逐檔不變。22頁PDF完整74段及14筆引文全文核對通過；30張實際截圖、報告與本機HTTP路徑在docs/previews/five-roots-powers/。
- 無公開互動預覽主機，PDF／截圖可直接閱讀，不能把GitHub HTML檔案頁當成網站。實體Safari、外站影片與台大獅子吼頁面呈現、音軌精校及引文版本差異尚未驗收。此工作環境未提供Notion工具，尚未寫入；待補記docs/releases/five-roots-powers-notion.md。

---

# 安那般那止觀四式聚焦（2026-11-18）

依作者新增指示，從main b362653建立fix/anapana-four-ways-focus，承接本書發布後維護。S08先止後觀、先觀後止、掉亂後止、止觀並行四欄依P06–08、P09–11、P12–13、P14–15切換，P01–05總說全幅。沿用共用76%遮罩，放大／旋轉同步，不改原圖、119頁資料或口白／引文。位置見docs/anapana/panel-focus.md。

五尺寸75個受影響頁面及20個放大狀態、目錄切幕清除、快速翻頁與旋轉保留頁碼通過；結果與8張截圖在docs/previews/anapana-four-ways/。實體Safari未測。發布後於本次PR核對Pages與固定SHA完整ZIP。Notion工具未提供、尚未寫入，待補記docs/releases/anapana-four-ways-notion.md。

本次作者同時交付五根五力兩包，已在工作區安全合併並核對11圖；新書另從這次main建立審閱分支，不因安那般那維護授權而發布新書。

---

# 四如意足漫畫逐格聚焦（2026-11-18）

依作者對已發布四如意足繪本的修正要求，從最新main `7f19874e1380102577eae1a6a34f2bf6a99a7326` 建立 `fix/iddhipada-panel-focus`，承接本書的發布後維護授權。

- S01鐵球到木棉四欄：P01–04第一格、P05–09第二格、P10–12第三格、P13–14第四格；P15收束全幅。S06四種偏差二乘二：P50左上、P51右上、P52左下、P53右下；P48–49介紹及P54–55收束全幅。S08四欄是整體總覽，沒有單格敘述，保持全幅。
- 使用既有共用picture-panel-focus.js/css，一格明亮、三格76%遮黑。框線以完整1672×941圖片實測，保留格間留白；放大與旋轉同步。資料與全書P編號配對見iddhipada/book/panel-focus-data.js及docs/iddhipada/panel-focus.md。
- 注意本書paragraphNumber是全書段號，不同於安那般那的幕內段號；共用遮罩呼叫使用currentIndex - scene.start + 1，避免第六幕錯位。切幕／非漫畫／結語清空遮罩。
- 原82頁book-data.js逐位元組不變，81段口白／時間、11卡及13疊字、全部原圖／來源／PDF不改。共用檔案、首頁、其他11本與Pages設定不改。
- 生成一致性與素材雜湊通過；五尺寸360×800、800×360、768×1024、1024×768、1440×900的Chromium觸控模擬，115個漫畫頁面狀態、40個放大狀態及35個非漫畫狀態全部通過。核對字幕／經文／圖內標籤完整、比例／遮罩座標／無水平溢出、目錄、讀經捲動、旋轉保留頁碼、快速翻頁與末頁重讀。19張截圖及報告見docs/previews/iddhipada-focus/。實體Safari尚未測；不宣稱重跑全書410個狀態。
- 發布後核對合併SHA、對應Pages建置、公開檔案與固定SHA完整ZIP，記於本次PR。此工作環境未提供Notion工具，尚未寫入；待補記docs/releases/iddhipada-focus-notion.md。

---

# 四禪閱讀整理／安那般那十六勝行逐格聚焦（2026-11-18）

依作者對已發布繪本的修正指示，從最新main `e578c2a85131c646ad4986e8c1367d7d60f8e652` 建立 `fix/jhanas-table-anapana-focus`，承接這兩本的發布後維護授權。

- 四禪S10原圖已有完整表格，移除圖下重複HTML比較表及讀經視窗轉錄，建置器與24頁校稿PDF同步；主題專頁的獨立表格保留。S05「瞋恚」x29%、寬14%不變，y29%移至17%，避開臉部，詳見overlay-layout與REVIEW。原圖、130段字幕／時間、8筆原經與131頁不變。
- 安那般那S04–S07身受心法共16格，使用既有共用遮罩，當頁一格亮、三格76%遮黑。四幕介紹與收束回全幅，放大與旋轉同步；框線以完整1672×941原圖的格界計算，保留米色外框與間隙。配對存panel-focus-data.js，幕內P編號／格位與像素範圍見docs/anapana/panel-focus.md。原119頁資料、118段口白、41筆引文及12疊字全部不改。
- 兩本既有上方字幕／完整圖片／下方經文、目錄、按鍵、放大、讀經與末頁重讀維持；共用檔案、首頁、其他10本、來源與Pages設定不改。S12純文字總覽沒有重複圖表，保留。
- 生成一致性、原檔雜湊及來源逐筆不變核對通過；Chromium觸控模擬360×800、800×360、768×1024、1024×768、1440×900，本次340個受影響頁面狀態與80個聚焦放大狀態通過，無本機HTTP或JS錯誤。檢查快速點按、目錄、讀經捲動、上下頁、返回導讀、旋轉頁碼與末頁重讀。報告與19張截圖見docs/previews/reading-focus/；實體Safari未測，不冒稱重跑全書全部狀態。
- 發布後核對對應成功Pages建置、公開檔案與固定合併SHA完整ZIP，結果記入本次PR。此環境未提供Notion工具，尚未寫入；待補記docs/releases/reading-focus-notion.md。

---

# 四禪移除片尾出處頁（2026-11-18）

依作者截圖指示「這頁出處不需要了可移除」，從main `e3806f255ca1ed020b58b8d03f03d61686f56c3c` 建立 `fix/four-jhanas-remove-credits`，承接本書已授權的上線修正。

- 刪除原第131頁的整張片尾出處圖及該頁出處說明；P130故事結束後直接接閱讀說明／經典依據，總頁數由132改為131，目錄仍是十幕。原130段字幕、時間、八筆經文及配對、7條疊字與原有操作不改，導讀原經區保留。
- 建置器同步移除該頁，避免重建恢復。原交接README要求附片尾的歷史說明由本次作者指示取代；原圖、原始ZIP內容與雜湊記錄僅留存，不刪除或重繪。校稿PDF也移除此圖，現為24頁。
- 舊第132頁網址及舊儲存頁碼自動落到新的最後一頁，避免移除一頁後跳回開頭；快取版號已更新。閱讀器現在131頁，回到第一頁功能維持。
- 生成一致性、原檔SHA、JS語法與前130頁逐筆不變核對通過；本次只重測五尺寸末三頁、前後翻頁、最後頁重讀、舊連結／記憶／旋轉重載，結果與截圖見docs/previews/four-jhanas-ending/。先前660狀態報告為原132頁版本的歷史驗收，不冒稱新版本已重跑全部655狀態。實體Safari未測。
- 發布後應核對Pages、公開資料及固定合併SHA ZIP。此環境未提供Notion工具，尚未寫入；待補記docs/releases/four-jhanas-remove-credits-notion.md。

---

# 第12本《四禪》發布授權（2026-11-18）

作者本輪明確指示「直接發佈吧」。**此授權取代下方四禪的審閱限制，允許將PR #36合併至main並發布GitHub Pages。** 發布已驗收的同一版本，移除導讀／閱讀器noindex與試閱標示、更新正式快取版號；不變更十幕、P001–P130、Q01–Q08、原圖、7條疊字與既有十一書。

- 專頁：https://sutra-zen.github.io/four-jhanas/
- 繪本：https://sutra-zen.github.io/four-jhanas/book/
- 發布經 [PR #36](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/36)。實際合併SHA、對應成功Pages建置、公開檔案與固定合併SHA完整ZIP，記錄在PR最後發布驗證；不以先前審閱ZIP代替正式備份。
- 既有五尺寸660頁面狀態、35放大疊字及20分格放大狀態驗收結果沿用；發布前重核生成一致性、原檔SHA、JS語法、相對路徑與原書不變。實體Safari、外部影片播放、音軌精校及來源斷句差異仍依REVIEW記錄，不因發布宣稱已完成。
- 此工作環境未提供Notion工具，尚未寫入改版頁；待補記 `docs/releases/four-jhanas-notion.md`。

---

# 第12本《四禪》實作與審閱（2026-11-18）

從最新main `c4e6670d30416b4203767287cf14cd754dea8dd7` 建立 `feat/four-jhanas-review`（[草稿PR #36](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/36)）。作者本次要求製作與驗證，尚未明確授權新書發布；**勿自行合併main或部署，也勿沿用前一本四如意足的發布授權。**

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

- 正式導讀：https://sutra-zen.github.io/iddhipada/
- 正式繪本：https://sutra-zen.github.io/iddhipada/book/
- 發布經 [PR #34](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/34)；實際合併SHA、Pages建置／公開檔案核對與固定合併SHA的完整ZIP，記錄於PR最終發布驗證。不以先前審閱ZIP代替正式備份。
- 審閱版已通過五尺寸410個頁面狀態、65個放大字框狀態及舊十本入口檢查；發布前重核原檔／資料生成／JS語法／相對連結與原書不變。實體Safari手勢、影片播放、時間精校及來源措辭差異仍保留REVIEW_TODO，發布不等於這些項目已完成校勘。
- 此工作環境未提供Notion工具，尚未寫入改版頁；待補記 `docs/releases/iddhipada-notion.md`。

---

# 第11本《四如意足》審閱實作（2026-11-16）

最新main基準 `140f62221726485916f3992d8ea6f5782e7507b5`，實作分支 `feat/iddhipada-review`，[草稿PR #34](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/34)。**本次使用者明確要求審閱，不合併main、不公開部署。先前各書發布授權不適用本次。**

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

發布完成必須核對實際合併SHA、GitHub Pages build成功及公開首頁／導讀／閱讀器／圖片檔案，並下載固定合併SHA完整ZIP核對CRC及追蹤檔案。以下595個頁面狀態為同一套內容與互動的發布前驗收，不代表實體Safari驗收。正式入口為 https://sutra-zen.github.io/anapana/ 與 /anapana/book/；成功與否以發布回報及PR #28最終驗證記錄為準。

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

從最新main `cd1cb6f743d773afe9ea22c6c548384c7760ef75` 建立feat/right-effort，[PR #25](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/25)。已讀AGENTS、PROJECT、HANDOFF、SOURCES、完整兩包交接README／CODEX_PROMPT／NARRATION_REVIEW／SOURCE_NOTES／storyboard／catalog／manifest，並檢查最近四念處的實際實作。作者本次明確授權直接發布。

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

依作者對已發布版本的回饋，從最新main `1d964bbd8d6c9d0c05aa725f36da1b44d8ffb078` 建立 `fix/mindfulness-consistent-reader`，[PR #23](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/23)，修正本書導讀／閱讀器，承接本次網站直接發布授權。以下取代初版的整幕側欄閱讀方式；原始交接與下方歷史紀錄保留。

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

作者在第04包訊息明確授權「收齊你就可以做專頁和繪本了，可直接發佈」，取代舊交接提示中的先試閱限制。本次從最新main `24983232d11bc9e775641bf444bcbe59055fe1ad` 的實作分支 `feat/mindfulness-preview` 完成，[PR #22](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/22)，原有七本及GitHub Pages設定保持不變。是否正式上線以PR實際合併SHA及相應Pages成功為準，交付時另提供固定SHA ZIP備份。

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

作者本次明確授權直接上線。實作PR：https://github.com/Sutra-Zen/sutra-zen.github.io/pull/19 。分支`feat/four-purities-six-recollections`從最新main `31ebc8679723ab9908f771436bc0563cc4b04270`建立。正式部署須核對實際合併SHA與Pages成功，不能以push成功代替。

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
- 試閱草稿PR：https://github.com/Sutra-Zen/sutra-zen.github.io/pull/15 ，目標main；尚未合併。
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

- PR：https://github.com/Sutra-Zen/sutra-zen.github.io/pull/13 。分支 `fix/reader-labels-and-scripture`，基準 main `f01ffa80e6936c81572f8b9d29e99bb084ab26e5`。先確認最新main，保留原圖、原字幕、經文與既有操作；只有作者點名的字樣與新增結語作內容調整。
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
- PR：https://github.com/Sutra-Zen/sutra-zen.github.io/pull/12 。沿用已通過1116頁面檢查與8組旁白像素檢查的實作；另對八正道閱讀器資產加入版本查詢，避免舊JS快取與新HTML混用。圖片、字幕、經文、分頁及疊字位置不另改。
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
- 發布 PR：https://github.com/Sutra-Zen/sutra-zen.github.io/pull/11 。移除新主題導讀的 noindex；閱讀器沿現有慣例保留。故事、圖片、控制與所有舊書保持試閱測試版本。
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
