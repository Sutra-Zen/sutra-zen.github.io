# `/game/` 首次發布驗證（2026-11-22）

本資料記錄部署前本機驗證；是否已上線，仍以精確merge SHA的Pages成功及正式站驗收紀錄為準。正式入口為`https://sutra-zen.github.io/game/`，共用城池、書架、出處頁分別沿用`/play/city/`、`/play/visual-v2/shelf.html`、`/play/sources.html`；這些頁的海圖／回旅程會返回`/game/`。

本機從專案根目錄執行：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

同一台電腦開啟`http://127.0.0.1:8765/game/`。`/game/`只是共用同一海圖程式的入口，沒有另建存檔或複製十四本故事。

## 畫面

| 內容 | 證據 |
| --- | --- |
| 新玩家入口 | [開始旅程](new-player-game-1280x900.png) |
| 新名稱與共用海圖 | [桌機](game-free-map-1280x900.png)／[手機](game-free-map-390x844.png) |
| 完整城池、廣場北緣城主與右前方雙使／開卷 | [桌機](city-full-labels-1280x900.png)／[手機](city-full-labels-390x844.png)／[平板](city-full-labels-768x1024.png) |
| 鬍鬚合成與短解 | [桌機](city-lord-composite-1280x900.png)／[手機](city-lord-composite-390x844.png) |
| 新圖精簡閱讀回饋 | [四聖諦](fixture-final-art-feedback-four-truths-390x844.png)／[五陰與同一鬍鬚層](fixture-final-art-feedback-five-aggregates-390x844.png)／[六處](fixture-final-art-feedback-six-senses-390x844.png) |
| 第十四本回饋 | [明標有效存檔情境](fixture-final-art-feedback-four-fruits-ten-fetters-390x844.png) |
| 原生閱讀與前三本完成 | [直式原閱讀器](native-reader-five-aggregates-390x844.png)／[實際讀完後](native-three-completed-game.png) |

完整城池及新圖回饋使用隔離瀏覽器的有效備份情境，方便檢查全部角色及不同完成數，不是作者真實閱讀紀錄。前三本實際198步的操作另有獨立原生紀錄；其執行時城圖仍在修正，因此沒有把舊肖像回饋截圖當成新圖驗收。

底圖實際原生為1671×941，完整顯示；臉部髮層原生1536×1024 RGBA，由瀏覽器在相同圖框合成，並同步用於城主近照及五陰獎勵。沒有稱為原生4K。素材原件、SHA與座標見[來源清單](../../play/game-release/generated-assets.json)。

## 驗證方法與結果

完整重新驗證：

```sh
python3 -B scripts/check-game-release.py
```

若只修正城圖／標牌，可重用已完成的原生198步紀錄；工具會先比對11個閱讀核心／入口／原書SHA，任何不符就拒絕重用：

```sh
python3 -B scripts/check-game-release.py --reuse-native-reading
```

- [原生198步紀錄](native-first-three.json)：四聖諦29、五陰54、六處115逐頁Next，每本只有末步明確完成才計數；回到`/game/`顯示1／2／3本與相應城景狀態，再進十二因緣第0步。包括第5步重整／返回續讀、第3步手機／平板旋轉、舊v1及無關鍵保留。此輪只執行一次，再以一致的核心SHA重用，沒有為純美術重複走198步。
- [整合報告](validation.json)：五尺寸1280×900、390×844、844×390、768×1024、1024×768，共160次海圖及70次城池原生點擊；指定全文、可選HTML、完整圖框、六門、導覽／出處返回、精簡回饋均通過。消息引線每尺寸都落在原圖卷軸中心(1081,465)，長度小於250原圖像素；手機頂排不裁切。JS與本機HTTP錯誤均0。
- 公開頁標示試玩版；`/game/`隱藏技術美術審稿區，歷史海圖仍保留自身入口及返回方式。
- 自由選讀開書／翻頁／選到末章不會自動完成；正式按完成只得該本，沒有補齊前兩本。城池可原生重讀、重整與續讀。普通collection仍回書架，舊三本v1及獨立閱讀皆不被新入口覆寫。
- 現有14本存檔原始字串保持；壞JSON初始不被清除，儲存不可用仍可閱讀並有提示。儲存被禁用時不承諾跨頁保存。
- 對正式main `b9a0dad2`核對595個原書／原稿／圖片檔；14本HTML只增加既定選用模組，移除其標籤及插入換行後逐位元相同。首頁、15頁SEO／sitemap／robots／Google檔及共用操作保持；核心store／route／舊旅程對`a2b3225`不變，collection橋接僅新增白名單`collectionReturn=game`的目的地／標籤分支。
- [模型報告](model-check.json)：root本輪執行全部16,384種完成集合檢查通過。原14本1192步完整內容驗證保留，未重新走遍未變動的全文。
- `build-game-entry.py --check`通過；Pages仍main根目錄，新增Jekyll排除僅限`docs/previews/`內的遊戲QA資料，不排除原書／來源或遊戲執行素材。

## 尚未驗證

實機iPhone／iPad Safari、原生手勢及GPU效能未測；桌面Chromium尺寸模擬不等於實機。此資料不宣稱外部經文供應者已實際載入，也不把本機成功當作正式發布成功。正式站部署證據另由release與production smoke紀錄提供。
