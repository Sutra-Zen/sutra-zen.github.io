# 淺藍青瓷操作與五陰湖過場

2026-11-23，分支 `feat/game-cyan-aggregates`，基準 main `0d44d7229195d60bf1781e55e88ab53b8d7fcc7f`，origin為 `https://github.com/Sutra-Zen/sutra-zen.github.io.git`，開始時工作樹乾淨。作者沿用遊戲直接更新發布的授權；正式上線必須以本輪PR的精確merge SHA／Pages成功及正式站檢查為準。

## 變更

- `play/game-theme.css`與`play/story/dialogue.css`：主要／建議操作、目前關卡地標、閱讀狀態、目前分頁、路線及城池選取狀態，統一淺藍青瓷漸層與深青字。保留深青靛半透明面板、金色角色名與原插畫，包含hover、focus、disabled可讀性。
- `play/story/data.js`：加入作者的小貓口白「原來，四個重要的真理是苦、集、滅、道。但我還不太懂苦的心理運作……那邊有座五陰湖，去看看好了！」。這是遊戲故事，不是經典引文或五陰原稿。
- `play/worldmap-v4/worldmap.js`：四聖諦原完成心得／疑退場與閱讀回饋照舊。按「前往下一站」定位五陰湖後顯示短對話；按「前往五陰湖」才進原五陰閱讀器。直接從海圖／路線合法開啟五陰也共用此引導。既有五陰書籤、已讀複習或已看過對話不插話；「先看看地圖」只收起對話。
- 新scene沿用 `sutrazen.play.story.v1` 已看紀錄；不新增閱讀完成、能力分數或獎勵。CTA重新檢查目前合法關卡，再走原閱讀入口。作者重置與地圖／對話使用同一個story store module instance。
- 新入口與地圖／城池／書架互返帶 `v=cyan-1`。三處開書帶 `collectionStory=cyan-1`；十四本HTML**各只改既有collection bridge script的快取query**，bridge自身只更新回遊戲的版本URL。這些參數只管快取，不提供權限；未帶`collection=1`的原站讀本保持獨立模式。原文與其他HTML bytes以正規化單一script URL逐本比對。
- `play/worldmap-v4/index.html`仍是 `scripts/build-game-entry.py` 的唯一入口來源，產生的`game/index.html`同步。故事／title作者重置的import query及深色主題cache query同步，避免新舊JS／CSS混用。

## 檢查與預覽

實際測試結果與截圖見[本輪證據](../../previews/game-cyan-aggregates/README.md)。使用Chromium手機／平板橫直及桌面尺寸；不宣稱已測iPhone／iPad實機Safari。

本機在專案根目錄執行：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

開啟 `http://127.0.0.1:8765/game/?v=cyan-1`。保留作者試玩入口 `?author=1&v=cyan-1` 的確認重置，普通入口不顯示重置。已讀五陰的玩家不會因本次更新被重新插話或清除進度。

原站首頁／心智圖、十五頁SEO、Google驗證原檔、原書插畫／口白／經文／操作、十四本順序與資格、存檔格式及相機程式均保留。Pages仍legacy `main:/`；只將新QA目錄加入既有exclude，合計十七個QA目錄，沒有改發布來源。

## 交接與待補

發布時將精確merge SHA、Pages run、正式站結果、固定SHA原始碼ZIP記到本輪PR交付留言。現有工具沒有Notion連接器；待原對話補記本次配色、五陰湖口白及該交付連結。ZIP若只驗證HEAD可下載，應明說未完整下載或CRC驗證。
