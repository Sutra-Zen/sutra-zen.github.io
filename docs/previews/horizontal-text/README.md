# 十四本橫書純文字頁的置中驗證

基準已發布PR84 `8f91fd461db03fc3c43920134af315bae75181c4`。本輪只處理橫排純文字欄，沒有改稿、插畫或心經直書設定。

[實作說明](../../readers/horizontal-text/README.md) · [全候選與基準DOM／字級盤點](inventory.json.gz) · [原稿／核心檔與離線包保護](source-validation.json)

## 全候選範圍

14本共18個純文字閱讀步驟，頁碼是使用者看見的1-based閱讀位置。心經13步及有圖總結不混算在橫書純文字候選內。

| 繪本 | 純文字步驟 |
| --- | --- |
| four-truths | 29 |
| five-aggregates | 1、54 |
| six-senses | 1、115 |
| twelve-links | 77 |
| eightfold-path | 109、110、111 |
| four-fruits-ten-fetters | 75 |
| four-purities-six-recollections | 95 |
| mindfulness | 111 |
| right-effort | 81 |
| anapana | 119 |
| iddhipada | 82 |
| four-jhanas | 131 |
| five-roots-powers | 75 |
| seven-factors | 37 |

名冊保留每頁實際可見DOM、字級／行距、正文hash及render API；七覺支37由`showPage(11,6)`到達，不用虛構第37個原始scene。

## 判定方式

原全寬scene僅作縱向捲動與控件安全區；量測其可見、正常流直接子元素共用的實際grid欄及文字Range，不把滿寬空容器當作置中證據。排除caption-sizer等隱藏測量副本。寬版檢左右中心，手機直式／短橫式檢左起；段內保持left/start，原字級／行距與完整原文保持。長文、原經及兩種表格檢末端可達與控件避讓。

## 最終結果與代表畫面

[精簡統計](summary.json) · [完整逐組JSON gzip](validation.json.gz) · [原始資料雜湊與大小](raw-evidence-digests.json)

- 最終CSS完整重驗18頁×6尺寸，共108個公開純文字狀態；不把修正前的73組或其他中間版混作最終結果。各候選以前置定位後原生翻入／片頭初始進入，沒有冒稱全書1192步重讀。
- 寬版整欄中心、窄版左起、段內左排、標題與全文末字可讀通過；36個基準字級／行距／原文字串比較通過。八正道與安那般那表格均在範圍內。
- 最終底部scrollport版本另驗16個遊戲代表狀態（4類×主線／複習×1024／844）、8個重整情境，書籤與完成規則保持。複習已讀末頁重整依既有規則從第1頁重讀，不誤報為必須停末頁；修前48組不計最終case數。
- 心經寬中／窄右與原生橫捲2組、一般插畫43→44圖框及字幕2組回歸正常。JS／同源HTTP錯誤0。
- 橫式scrollport在底部固定控制列之上結束，實際可見字不進入該列，長總結尾字仍可原生捲達；安那般那1024的scrollport底界704px、844短橫底界326px。
- **直式保留原自然文件捲動**：途中正文可從固定底列後方經過，繼續上移即可閱讀，頁尾空間讓最後字可讀。已用同一八正道109／360情境核對[原版同樣行為](portrait-existing-risk.json.gz)，不宣稱全平台所有中途文字零重疊，也沒有在本輪增加另一層直式捲動窗。

| 情境 | 最終畫面 |
| --- | --- |
| 五陰片頭，桌面整欄置中 | [1916×963](public-five-aggregates-p1-1916x963.png) |
| 五陰片頭，手機直式左起 | [360×800](public-five-aggregates-p1-360x800.png) |
| 八正道表格，共用置中欄 | [1280×900](public-eightfold-path-p109-1280x900.png) |
| 安那般那長總結，完整標題與底部選單避讓 | [1024×768](public-anapana-p119-1024x768.png) |

本輪只修改共享CSS及14個CSS快取query，45個原書JS／CSS／CSV和16個核心保護檔保持；離線包30成員CRC通過，只有共享CSS及七覺支HTML快取兩個成員更新。原稿與1192步／圖／心經直書／保存／SEO維持。

正式發布狀態與精確merge SHA／Pages／live以發布PR交付紀錄為準。手機／平板為Chromium模擬，實機iPhone／iPad Safari未測。
