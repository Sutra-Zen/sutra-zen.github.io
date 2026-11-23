# 精簡控制、單層書架與對話內完成通知

日期：2026-11-23。分支 `fix/game-simple-panels`，基準為已發布 PR76 `d82f68533f595db032c8a787a1a2c5606a53fb2f`。原工作樹乾淨，origin 為 `Sutra-Zen/sutra-zen.github.io`；延續作者對本輪遊戲修正的發布授權，經 PR、精確 SHA 的 Pages 與正式站驗證後才算發布。

## 玩家操作

- 海圖與城池不再有全景／返回全景按鍵；海圖保留目前關卡、＋／－，兩地仍可拖曳與雙指縮放。過去全景鏡頭自動恢復探索，沒有返回快照時定位目前關卡／四大廣場。`0`／`Home` 不再進入隱藏全景。
- 書架插畫只畫在捲動容器 `.collection-stage` 一次，以 `background-attachment: local` 跟隨內容；書本層透明，外層是純色。左右滿寬，四欄／兩欄與十四本、已讀複習資格不改，捲到頂底也不露出第二幅拱門。
- 設定新增「回到遊戲開始畫面」，以 `screen=title` 顯示主選單，不重播片頭、不清除閱讀／劇情／城景。繼續仍回合法目前關卡。片頭只留底部「點一下進入選單」，保留正常動畫背景點擊、鍵盤、自然結束與降低動態的靜態閱讀。
- 建物／道具來源只顯示經名與對應經文、右上 X；不再附閱讀、關卡或來源連結。創作景物只解釋相關主題，六位覺支動物的點選對話各說明相應覺支。角色本身仍可點開對話。
- 移除「看閱讀回饋」及獨立完成面板。首次實際完成依序為心得、疑退場、波旬、前往五陰湖短句，再由同一小貓對話直接說明本次城景新增、地景與已讀本數。最後只有「前往下一站」／「前往城池看看」兩個選擇。其他書也用同一對話通知。

## 劇情與保存界線

首本過場的主要操作統一為「接著看」，沒有略過按鈕，Escape 不跳過劇情。原故事正文、場次 ID、末頁「完成這本」、receipt 與閱讀資格均保留。

最終通知是暫時的 `completion-reward` 對話，不新增 `seenSceneIds` 或存檔欄位。當前網址的 `completed=<已讀ID>` 只用於重整後恢復通知；必須先通過現有已讀檢查，網址不能寫完成或解鎖。下一站／城池／Escape／重置與還原都會清除通知網址。前段尚未確認時，沿用原劇情狀態接回；完整過場結束後重整只回最後通知。

閱讀與城景依然自動保存；複習不改主線、不重複發放模組。city v1、reading v1、備份 v1/v2 與原有儲存鍵不變。新顯示文字集中於 `game-ui-text.js`、`story/data.js` 與 `city/explanations.js`；介面新增內容使用 HTML 文字。

## 經文與創作內容

`play/city/explanations.js` 集中十三個城喻解釋與十四模組的簡短說明。真正城界使用 `town` 原經，五陰觀察角用創作的 `city_body` 說明，避免把兩者混同。

四大廣場的標題及句子按作者此次指定呈現：

> 相應部35相應245經／如緊叔迦經
>
> 『在中央四衢街道』，這是四大的同義語，即：地界的、水界的、火界的、風界的。

可讀取的 SuttaCentral 官方資料與正式 API 仍是「像緊叔迦那樣經／在中央廣場／對於地界」版本；沒有把作者指定字句冒稱為已從該 API 核得的新版本。其餘十二則摘錄按可讀官方譯文逐字核對。譯者網站在本環境被代理阻擋，不能判定其版本。詳 [來源核對紀錄](source-audit.json)。原經封存檔、原繪本原經與口白完全未改；來源 metadata 只供稽核，不在遊戲彈窗增加說明或按鍵。

## 檔案與產生流程

主要改動在 `play/worldmap-v4/`、`play/story/dialogue.*`、`play/city/`、`play/visual-v2/shelf.css`、共用 shell／navigation／title／prologue。`game/index.html` 仍由 `scripts/build-game-entry.py` 從 worldmap shell 產生；不能只手改生成檔。

新 UI 快取版本 `simple-ui-1`。十四原讀本 HTML 僅更新既有 bridge query；bridge 僅改返回遊戲的快取網址。collection／route／story store、city store／catalog、圖像與存檔維持原模組單例。既有首頁與心智圖、十四公開閱讀器、十五頁 SEO、sitemap、robots、Google 驗證檔與 Pages `main:/` 不變。新增 QA 目錄排除，累計二十三處。

## 檢查與預覽

在專案根目錄執行：

```sh
python3 -m http.server 8000
```

用 `http://localhost:8000/game/?v=simple-ui-1`；`screen=title` 可直接看開始選單，`author=1` 保留暫時作者重置工具。不要在真實進度上測重置。

```sh
python3 -B scripts/build-game-entry.py --check
python3 -B scripts/build-seo.py --check
python3 -B scripts/check-game-simple-ui.py
```

實際操作、截圖與測試限制記在 [本輪驗證](../../previews/game-simple-ui/README.md)。完整首本使用原生逐頁操作，歷史進度與不同完成冊數另以隔離 fixture 測試，不混稱真實讀完十四本。iPhone／iPad 實機 Safari 與其橡皮筋捲動未測，Chromium 尺寸／觸控模擬會明確分列。正式網址與發布證據以新 PR 交付紀錄為準。
