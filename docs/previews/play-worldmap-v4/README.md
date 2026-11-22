# 山海世界map-v4／路線r3試閱（2026-11-22，未發布）

本輪依作者附件正文版本2026-11-22-map-v4與2026-11-22-r3，更新獨立遊戲試稿；原網站、十四本內容與Pages main:/維持不變。

## 優先比較畫面

| 畫面 | 預覽 |
| --- | --- |
| 3840×2160無線網頁輸出 | [無線版](worldmap-3840x2160-no-lines.png) |
| 同構圖有線網頁輸出 | [有線版](worldmap-3840x2160-with-lines.png) |
| 未解鎖迷霧 | [桌機](initial-overview-1280x900.png)／[手機](initial-overview-390x844.png) |
| 完整地景與可換文字 | [桌機](all-fourteen-overview-1280x900.png)／[平板](all-fourteen-overview-768x1024.png) |
| 皇冠短鬍子城主、黑白／三花雙使 | [城池角色完整配置](city-actual-all-1280x900.png) |
| 正式讀完四聖諦的實際回饋 | [法輪木碼頭](actual-feedback-four-truths-1280x900.png) |
| 正式讀完五陰的實際回饋 | [城體、廣場與城主](actual-feedback-five-aggregates-1280x900.png) |
| 正式讀完六處的實際回饋 | [六門與後續閱讀](actual-feedback-six-senses-1280x900.png) |
| 不混淆的兩書獎勵 | [僅花田](fixture-effort-only-1280x900.png)／[僅公路溪湖](fixture-path-only-1280x900.png)／[皆完成與灌溉](fixture-path-and-effort-1280x900.png) |

完整地景、角色或亂序完成的展示使用隔離瀏覽器QA存檔，不是作者真實閱讀紀錄；actual-feedback三張則由實際逐頁閱讀、正式按完成產生。

3840×2160是瀏覽器3倍像素密度的真實網頁輸出，文字與線層重繪；**底圖原生仍1672×941，並非原生4K插畫**。四張區域細節稿不是可拼接的精確象限，完整同構圖原生4K、正式拆層及終章完整演出尚待補。尺寸與輸出方法詳 [high-resolution-export.json](high-resolution-export.json)，圖稿來源詳 [generated-assets.json](../../play/worldmap-v4/generated-assets.json)。

## 本機試閱

```sh
python3 -m http.server 8765 --bind 0.0.0.0
```

開啟 `http://localhost:8765/play/worldmap-v4/`。自由看完整地景可加 `?mode=free`；不會因此得到任何完成紀錄。點「開始／繼續閱讀」進入原完整閱讀器，最後按「完成這本」回此地圖看城景，再讀下一本。一般collection仍回舊書架；新功能只在新增collectionReturn參數啟用。

## 實測結果與界線

- `python3 -B scripts/check-play-worldmap-v4.py`：五尺寸、32個地標原生點選、兩排五欄四橋、46來源線、有線／無線同底圖與錨點、迷霧／標牌／平移、獨立花田與公路、亂序獎勵自動安置、末關知悉／揭曉及終章條件、存檔與原網站保護。見 [validation.json](validation.json)。
- 新主流程實際29＋54＋115＝198個閱讀步驟，未修改頁碼製造成功；每本正式末步才記完成、顯示真實城景，下一本為十二因緣。中途重整、返回續讀、手機旋轉、自由閱讀四禪續讀與重讀不重計通過。
- `python3 -B scripts/check-play-route-r3.py`：13組語意情境、全部16384完成子集、原本機存檔與metadata隔離，見 [route-model-validation.json](route-model-validation.json)。`node play/route/check-route.mjs`亦通過。
- 原14書、圖文／經文、collection store與舊v1逐位元保留。collection讀本橋接只新增選用返回網址／文字，其餘normalized bytes保留；原普通收集／獨立閱讀回歸通過。
- SEO --check、JavaScript語法及diff檢查通過。實機Safari、GPU動畫效能未測；未重跑未變動的全部1192步內容。

實際範圍、原喻／創作、語言及4K限制詳 [實作說明](../../play/worldmap-v4/README.md)。沒有可用公開預覽，未合併main或部署正式站。
