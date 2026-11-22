> 作者後續三張截圖已改採[原圖邊界與港口徽章](../game-original-frame/README.md)，不再延伸外海或顯示半幅城景。以下保留前輪設計與驗證歷史。

# 外海留白與全圖返回

2026-11-22。從 main `53e8eee0db9d2465ea5f584a840649d3c73d0f8d` 建立 `feat/game-ocean-overview`，起始工作樹乾淨、origin 正確。依作者遊玩回饋延續 `/game/` 已授權發布流程；精確 merge SHA、Pages、正式站與固定 SHA ZIP 以新 PR 交付紀錄為準。

原圖及地標仍使用同一個 1600×900 原點，沒有縮放某一層或修改 32 地標／46 來源關係。`ocean-frame.js` 在外圍增加左／右200、上140、下220世界單位的外海邊界，原圖、霧、連線、城池及點擊區仍一起變換。外海使用既有原圖左上無地景海水區域的 SVG pattern 延伸，未更動／重新生成原 PNG，也沒有烙字。外海底色取自原圖海水，低對比紋理混合顯示；原圖邊緣以8–12世界單位的CSS透明漸層柔化接海，地標座標不移動。較窄比例視窗多出的空間同樣顯示海水。

鏡頭仍占滿視窗，但可讀區會避開下方 dock 實際高度＋16px，與上／左／右安全區。全圖以加入外海後的邊界完整入鏡，讓八正道半島及其南側海水位於操作列上方；平移邊界也允許移入外海，不再把最下方地景卡在 dock 後面。這是鏡頭構圖留白，不是縮小或裁切原插畫。

進入「全圖」時先記住當前 x/y/scale，只記第一次，重複 fit 不蓋掉原位置。左上「← 返回海圖」與底列切換後的返回按鈕共用同一動作，回到進全圖前的位置及縮放。返回資訊保存在既有 camera session 命名空間，舊格式仍可讀；不使用 completed 或閱讀書籤冒充鏡頭狀態。旋轉／dock變高時重新構圖全圖，返回時只按新視窗必要範圍限制，不重置閱讀進度。舊版已停在全圖、但沒有返回快照的相機紀錄，以及手動縮小至總覽者，也會有返回箭頭；此時回目前關卡的一般倍率，不假稱能還原未曾儲存的舊鏡頭。

相機 API：`outerPadding`、`getInsets()`、`fit()`、`returnFromOverview()`；`getState()` 提供 `canReturn`／`overviewExplicit`／`outerBounds`／`safeInsets`／`visibleViewport`。worldmap 的 onChange 更新兩處返回介面，ResizeObserver 讓可讀區隨底列高度變化。入口 HTML、CSS／相機模組版本與 game 產生器同步，原標題紙卡品牌位置保留。

[實際驗證與截圖](../../previews/game-ocean-overview/README.md)：五尺寸檢查原圖／半島完整性、下方遮擋、手指平移／縮放、同座標層、真實平移及縮放後全圖→返回、重複全圖、旋轉／重整，以及必要的閱讀續讀／鎖定回歸。原站615保護檔及store／policy／原讀本／資料不變。本輪不重走未改的1192步，實機iPhone／iPad Safari未測。

本機從根目錄啟動 `python3 -m http.server 8765 --bind 127.0.0.1` 後開 <http://127.0.0.1:8765/game/>。驗證入口為 `python3 -B scripts/check-game-ocean-overview.py`；另執行 game 產生器與 SEO --check。Pages 仍 main:/；新增本輪證據排除後共十二個遊戲 QA 目錄，原圖與來源不排除。

Notion工具不可用，待補記「外海留白避讓八正道半島、全圖可返回原鏡頭」及新PR的精確merge SHA／固定ZIP；未代為寫入外部服務。
