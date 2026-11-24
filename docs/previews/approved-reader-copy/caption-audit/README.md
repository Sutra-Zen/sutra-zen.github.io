# 十四本字幕可讀性全量驗證

結果：**通過**。測試於本機隔離瀏覽器執行，未改原稿或正式遊戲進度。

**14本 × 6尺寸＝84組，共7,152個原閱讀狀態樣本**。1916×963逐本由第一步按Next直到末步，完整1,192步軌跡（1,178次Next點擊＋14本初始頁）；其餘五尺寸以原生showPage(pageArg,cueArg)逐狀態作幾何取樣，不能說六尺寸均原生完整翻讀。

尺寸：1916×963、1280×900、1024×768、768×1024、844×390、360×800。

## 實際字幕與圖高

- 4,684個普通橫式字幕樣本自然換行後：4,187個一行、497個兩行；套用新自然換行後，這些實際口白在六種尺寸沒有三行普通橫式案例，因此不宣稱原稿三行案例被實讀。所有字幕初始均完整出現在三行預留帶內。
- 2,342個普通直式字幕樣本保留自然文件流；心經/結語/總結另分類，圖內烙字、教學疊字、aria-hidden的caption-sizer不誤算。
- 逐文字節點Range檢查實際glyph位置與段落間距；沒有永久line-clamp、hidden子祖先裁字或不可捲到尾字的局部口白。
- 每本／尺寸普通圖片的高度差最大 **0px**，未因字幕段落數改變。
- 真正局部溢出只有四念處第110步在844×390的8行總結帶：程序可捲到末字；另實際mouse wheel捲到256px最大值，閱讀索引不變，旋轉至直式、重整、返回橫式均留在同一步。
- 185個各page class/region/書本/尺寸最長文字代表，額外測到scene/body/html祖先及末字的螢幕可達性，0失敗。
- 兩個**獨立暫時DOM版面fixture**在既有五陰第44步植入3段／3行，用原字級與原p間距驗1916×963、844×390，三行glyph完整、圖高不變；不寫原稿、不新增pageID、不計入1,192步。

## 各書覆蓋

| 繪本ID | 原閱讀步數 | 六尺寸樣本 | 1916原生軌跡 | 圖高最大差 |
|---|---:|---:|---:|---:|
| four-truths | 29 | 174 | 29 | 0.0px |
| five-aggregates | 54 | 324 | 54 | 0.0px |
| six-senses | 115 | 690 | 115 | 0.0px |
| twelve-links | 77 | 462 | 77 | 0.0px |
| eightfold-path | 111 | 666 | 111 | 0.0px |
| four-purities-six-recollections | 95 | 570 | 95 | 0.0px |
| mindfulness | 111 | 666 | 111 | 0.0px |
| right-effort | 81 | 486 | 81 | 0.0px |
| anapana | 119 | 714 | 119 | 0.0px |
| iddhipada | 82 | 492 | 82 | 0.0px |
| four-jhanas | 131 | 786 | 131 | 0.0px |
| five-roots-powers | 75 | 450 | 75 | 0.0px |
| seven-factors | 37 | 222 | 37 | 0.0px |
| four-fruits-ten-fetters | 75 | 450 | 75 | 0.0px |

JS／同源HTTP錯誤0；shared CSS／JS前後SHA相同。Chromium模擬尺寸與pointer/wheel，不當作iPhone／iPad Safari實機驗證。

檔案：summary.json（精簡統計）、full-samples.json.gz（完整逐樣本，可用Python gzip解壓）、ancestor-reach.json、three-line-fixture.json；只有1張真實總結捲動截圖。
