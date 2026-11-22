# 小貓背景序幕與作者重置入口

2026-11-22，分支 `feat/game-prologue-author-reset` 從已發布main `35d59e3bc41faed5fe7b0d22d1a0797398c6de59` 建立。工作樹起始乾淨，origin對應Sutra-Zen/sutra-zen.github.io。接續既有遊戲發布授權；精確merge SHA與Pages／正式站驗收，以本輪PR的交付紀錄為準。

## 使用方式

- 一般遊戲：`/game/`。在作者原小貓背景上先播放由下往上的序幕，完成後顯示原本置中選單。點一下畫面／「略過開場」，或按Enter、Space、Escape可進選單；略過不直接開始遊戲。
- 作者試玩：`/game/?author=1`。選單多一個「重置進度（試玩用）」；確認後重新播放片頭，選單變「開始旅程」，進海圖時重新顯示小貓抵達法輪遺跡的原開場。
- 普通網址沒有建立這個首頁重置按鍵。`play/title-review.js` 的 `AUTHOR_REVIEW_ENABLED` 可在試玩結束後關閉；query opt-in只是暫用工具顯示開關，不是身分認證或解鎖資格。
- 從繪本、城池、書架返回的 `#map` 或完成回饋路由沿用原邏輯，直接回遊戲；不反覆播放序幕。

原有設定、進度備份與「重看開場對話」仍可使用。本輪沒有擴寫小貓後續台詞、反派或終章。

## 片頭原稿與結構

[作者截圖原文](user-prologue-copy.md)完整保留三段六行，在 `play/prologue/data.js` 集中管理，和原經引文、繪本口白分開；不是一段被標為原經的引述。所有文字由HTML呈現，原作者JPEG未重新編碼或修改。

`play/prologue/prologue.js` 是無儲存操作的獨立畫面控制器，`initializePrologue({host,onComplete})` 提供start／finish／destroy及isPlaying。動態依文字與視窗計算30–45秒播放，調整尺寸保留進度；背景分頁暫停。完成／略過只回呼一次，阻擋同一次或緊接的點擊穿透去啟動閱讀。選單在片頭期間隱藏、inert且不可操作。降低動態偏好改可捲動靜態全文＋「進入選單」，保留原文。

原圖載入失敗時仍可閱讀序幕及進入選單。新檔與所有依賴的query版本一致，來源 `play/worldmap-v4/index.html` 和產生後 `game/index.html` 由既有建置程式同步。

## 重置範圍

首頁按鍵先以確認對話提示；取消不改資料。確認時呼叫既有collection與routeMetadata的reset API，以及本輪補上的storyStore.reset：

- 遊戲十四本的完成集合、閱讀位置與目前目標。
- 路線的已知／已開啟／已演出紀錄。
- 小貓開場的已看過紀錄與同分頁備援。
- 遊戲鏡頭 `sutrazen.play.camera.v1` 及操作提示 `sutrazen.play.map-tip.v1` 的session紀錄。

不使用localStorage.clear，不列舉刪除全站資料，也不重置原站讀本自己的資料、其他設定或舊三本原型。城池與書架依既有完成集合自然回初始狀態，不另造獎勵副本。

另修正既有collection.reset在session備援無法刪除時的邊界：改寫入fresh備援並回報儲存失敗，避免原值為null時重新載入又復活舊已讀紀錄；只改reset清理，不改讀本資格、資料格式或一般寫入。版本化作者工具也核對舊共用store快取的備援清理，避免為了快取更新而在同頁建立兩份store；只有原刪除成功時才補做清理，不誤刪仍需要的fresh備援。

story/store新reset與主海圖、對話、作者工具共用相同版本的module instance，防止只刪磁碟紀錄但記憶體仍「看過」。可讀卻無法刪除／寫入時，以符合原值的session備援保留本分頁fresh狀態並明示無法永久保存；不假稱裝置紀錄已確實清除。

## 驗證、預覽與限制

根目錄啟動 `python3 -m http.server 8778 --bind 127.0.0.1`，開啟 `http://127.0.0.1:8778/game/?author=1`。

```sh
python3 -B scripts/build-game-entry.py --check
python3 -B scripts/build-seo.py --check
python3 -B scripts/check-game-prologue.py
```

具體結果與五尺寸截圖見[實測紀錄](../../previews/game-prologue/README.md)。原站615檔、十四本原稿與圖像、正式首頁／SEO／Google驗證、資格／順序／橋接／鏡頭本身不改；本輪不重跑未變動的十四本1192步。瀏覽器驗證為桌面Chromium／CDP，實機iPhone／iPad Safari未測。

Pages仍為legacy main根目錄。本輪QA目錄加入排除，累計十五個證據目錄不進部署；原有排除不刪。Notion沒有可用連接器，待補本輪PR、精確merge SHA、Pages run、正式站及固定SHA ZIP至既有紀錄。
