# 書架小圖盤點（第二輪視覺試作，2026-11-21）

本次盤點只新增視覺試作資產與紀錄，不修改第一版旅程的閱讀、解鎖、存檔或完成邏輯。原網站14本公開繪本也維持可讀。完整逐檔路徑、尺寸、SHA-256與DOM定位見 `thumbnail-inventory.json`。

## 找到的實際來源

最初建立書架的commit為 `6aaa1af08a4a205a29d840b6d430bcc7f334d378`（以JSON中的完整commit為準）。該版 `index.html` 的 `.sz-books` 有14本：第01本已可讀，使用足印插畫；第02至14本的鎖頭封面由主題SVG小圖、HTML書名及另一個共用鎖頭SVG組成。

這13張主題小圖是 **inline SVG**，不是WebP，也不是Base64／data URL。最初及本次工作基準的首頁皆無 `data:image`。因此不能把它們稱為「原WebP縮圖」，也不為符合副檔名而假造點陣圖。

已從最初HTML逐本取出 `play/visual-v2/assets/shelf-02.svg` 至 `shelf-14.svg`。保留原始SVG元素、路徑、圓形、viewBox與線條設定，只加入獨立SVG檔解碼所需的 `xmlns` 及結尾換行。JSON同時記錄原inline片段及輸出SVG的雜湊，以免宣稱檔案逐位元相同。沒有描摹、重畫、轉成WebP或把新字烙進圖內。

另外取出13個鎖頭封面共用且逐位元相同的鎖頭SVG為 `play/visual-v2/assets/shelf-lock.svg`，原片段／輸出檔雜湊見JSON的 `commonLock`。鎖頭狀態仍由網頁決定，不把鎖頭烙進主題圖。

第01本沒有同系列的原鎖頭圖示；若試作用法輪，應說明它是新製作的介面標記。原足印封面仍列於盤點，不能說原繪本或原圖缺失。

## 14本對應

| 編號 | 書名 | 原鎖頭小圖 | 現有封面來源 |
| --- | --- | --- | --- |
| 01 | 四聖諦 | 原本無此類SVG；可另做法輪介面標記 | `four-truths/book/images/footprints.webp` |
| 02 | 五陰 | `shelf-02.svg` | `five-aggregates/book/images/a10.webp` |
| 03 | 六處 | `shelf-03.svg` | `six-senses/cover.webp`（由shelf.css套用） |
| 04 | 十二因緣 | `shelf-04.svg` | `twelve-links/cover.webp` |
| 05 | 八正道與十善業道 | `shelf-05.svg` | `docs/eightfold-path/assets/02-right-view.webp` |
| 06 | 四向四果與十結 | `shelf-06.svg` | `docs/four-fruits-ten-fetters/assets/s01.webp` |
| 07 | 四不壞淨與六念 | `shelf-07.svg` | `docs/four-purities-six-recollections/assets/IMG_0395.jpeg` |
| 08 | 四念處與四顛倒 | `shelf-08.svg` | `docs/mindfulness/assets/8ACD7BAD-64C1-476B-A4AD-7A63F5A2048E.png` |
| 09 | 四正勤 | `shelf-09.svg` | `docs/right-effort/assets/6FEE22D5-C7AA-476E-810C-DDE063530A82.png` |
| 10 | 安那般那與止觀 | `shelf-10.svg` | `anapana/assets/S01.webp` |
| 11 | 四如意足 | `shelf-11.svg` | `iddhipada/assets/S01.webp` |
| 12 | 四禪 | `shelf-12.svg` | `four-jhanas/assets/S06.webp` |
| 13 | 五根五力 | `shelf-13.svg` | `five-roots-powers/assets/S03.webp` |
| 14 | 七覺支 | `shelf-14.svg` | `seven-factors/assets/12.webp` |

目前首頁第03本仍留有原SVG在HTML內，但`shelf.css`以真實封面背景取代並隱藏SVG。只讀img標籤會漏掉六處封面，這次已另核對CSS。

## 試作用法與限制

- 未閱讀的旅程節點可顯示以上原主題SVG；書名、編號、鎖頭與狀態繼續使用可替換的HTML／SVG文字。
- 已讀節點若改用現有插畫縮圖，使用JSON列出的真實本庫圖檔，不聲稱這些是新的獨立遊戲插畫。
- 第04至14本僅為「後續旅程」的視覺安排，不因此開放或偽造第一版的遊戲完成紀錄；原網站讀者仍可自由閱讀14本。
- SVG小圖是網站介面圖示，不是經文原圖，也不替代作者指定的小橘貓角色稿。
- 本次沒有新增角色姿勢或去背立繪。

## 已執行核對

14個標題及順序與最初書架逐項相同；13個SVG的viewBox均為80×80並通過XML解析；14個現有封面檔案存在、經Pillow實際解碼、記錄真實像素尺寸及SHA-256。原首頁、shelf.css與所有原圖均未改動。這是資產盤點，不等於完整第二輪畫面的實機驗收。
