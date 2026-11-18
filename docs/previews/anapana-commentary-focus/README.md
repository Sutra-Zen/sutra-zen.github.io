# 安那般那安靜處經文與論師漫畫聚焦驗證

2026-11-19，基準main623bc69a。執行`python3 scripts/check-anapana-commentary-focus.py`。

- 五尺寸：360×800、800×360、768×1024、1024×768、1440×900；全部119頁共595狀態，核對原口白、經文、來源、頁碼、字幕在圖上方、無水平溢出及既有S04–S08遮罩。
- S10／S11使用真正主按鍵連續讀完26段，五尺寸130狀態；35個新增格位放大及橫直旋轉，遮罩位置按完整原圖核對，每次僅一格明亮。開頭總說／收尾及切幕無殘留。
- 安靜處803經對固定原典SHA及文字核對，本頁經文視窗、來源sa803連結／返回、導讀／地圖返回、旋轉與重載保留頁碼均通過。快速五次點按後到S02-P06，computed touch-action為manipulation，模擬視窗比例未變。
- 全部原交接雜湊由建置器驗證；118段原口白、12幕、119頁、12條疊字、41筆原引文文字、11張原圖與其餘繪本／共用檔／導讀逐檔不改。唯一新經文為S02-P06節錄，五筆中部經文僅去除標題括註。reader-edits.json保留修訂依據。
- 正式入口：https://rooneyflower-star.github.io/sutrazen-map/anapana/book/ 。本機`python3 -m http.server 8765 --bind 127.0.0.1`，開啟http://127.0.0.1:8765/anapana/book/ 。Pages實際發布及完整固定版本ZIP核對見本次PR。
- 實體iPad／Safari手勢未測，不將Chromium模擬視為實機驗收。

validation.json為實測結果；S10各四格、S11各三格及安靜處各有iPad橫直式截圖。
