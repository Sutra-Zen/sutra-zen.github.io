# 獨立城池與沿海連線修正（2026-11-22，未發布）

本輪只供審閱，未合併main或部署正式網站。從專案根目錄啟動：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

在同一台電腦開啟`http://127.0.0.1:8765/play/city/`；海圖為`/play/worldmap-v4/`，書架為`/play/visual-v2/shelf.html`。三處共用頂欄的城堡SVG按鈕直接進城池，捲頁後仍可操作。這些是本機試閱路徑，不是已上線的正式網址。

## 實際畫面

| 畫面 | 預覽 |
| --- | --- |
| 完整16:9城池與HTML標牌 | [桌機](city-all-labels-1280x900.png)／[手機](city-all-labels-390x844.png)／[平板](city-all-labels-768x1024.png) |
| 城主短解與重讀入口 | [手機](city-lord-meaning-390x844.png) |
| 真實讀完四聖諦後的精簡回饋 | [桌機](actual-compact-four-truths-1280x900.png)／[手機](actual-compact-four-truths-390x844.png)／[橫式窄高](actual-compact-four-truths-844x390.png) |
| 第十四本的回饋 | [有效備份書籤情境](fixture-final-compact-1024x768.png) |
| 修正後來源線與地理出入線 | [海圖](coastal-relations-1280x900.png) |
| 新版3840×2160網頁輸出 | [無線](worldmap-3840x2160-no-lines.png)／[有線](worldmap-3840x2160-with-lines.png) |

四聖諦回饋由實際29個原閱讀步驟、末步明確按完成產生；沒有直接改頁碼製造成功。城池全景與末本回饋使用隔離瀏覽器的有效備份情境，不代表作者實際閱讀紀錄。

3840×2160是瀏覽器以3倍像素密度重繪HTML／SVG後截取世界圖層，**底圖原生仍1672×941，並非原生4K插畫**。這兩張輸出使用空白進度的自由探索，沒有製造完成紀錄或修改原圖檔。方法及尺寸記於[validation.json](validation.json)的`highResolutionExport`。

## 驗證

```sh
python3 -B scripts/check-play-city-entry.py
```

- 基準`fd7d44c`的619個保護檔逐位元保持：十四本原書／原稿／圖片、collection store／catalog／bridge、route、舊旅程與根首頁／SEO／Google檔／共用操作。
- 五尺寸：1280×900、390×844、844×390、768×1024、1024×768；15次頂欄捲頁／原生進城操作，70次城池元件對話、六門、可選取HTML文字、同圖框SVG指示線、標牌開關與放大平移，沒有外部水平溢出或`[object Object]`文字。
- 四聖諦29步逐頁閱讀，抵達末頁不計完成，明確完成才成為1／14；精簡回饋的下一本／看看城池分開，沒有強迫嵌入整張城池。下一本實際進入五陰第0步。
- 城主元件可原生進五陰、翻頁、重整續讀，返回城池後繼續原位置；旋轉與已讀重讀保留書籤，不增加冊數。原v1及無關儲存鍵保持。
- 有效末本第74步備份加上13本完成的隔離情境，正式按完成後只加入末本為14／14，不產生第15本。
- 原46筆關係的ID、from／to及順序保留；港口與八正道分支改沿既有海岸公路，端點保持、中央不再斜穿。四禪→四如意足→港口另標為作者指定地理出入線，不冒充原來源關係、語意相鄰、推薦或完成條件。

完整報告：[validation.json](validation.json)。另收錄[相容性報告](legacy-compatibility.json)：兩尺寸共10種城景、六種前三本精簡回饋情境、已得角色待安置與舊city網址轉向；這份補充沒有重跑198步，也未改寫歷史報告。

本輪沒有重新走完未變動的198／1192步全書流程，先前完整報告仍保留。上述裝置尺寸為Chromium模擬；實機iPhone／iPad Safari、GPU效能及外站內容載入未驗收。新城池仍為待作者確認的整張概念圖，非完整獨立動畫層。
