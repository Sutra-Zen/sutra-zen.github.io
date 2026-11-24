# 五大城地形分區試版

分支 `feat/worldmap-five-cities`，由已發布 main／PR80 `a238a0fb549966ac0510b5b89f18b913c8ec40b6` 建立。作者要求在北方群島下方的既有主陸地，以順著地形與海岸的線圖圈出五城，並加極淡底色。作者已確認保留原縱向對應：西到東為**淨信城、正念城、精進城、禪定城、智慧城**。

這是地理區域名稱，與既有五組地景對應。北方群島、左側共同港口與下方八正道半島維持原圖；不新增關卡、不更動十四本順序、資格、完成或存檔。原圖與角色插畫完全保留。

## 呈現方式

- 新 `play/worldmap-v4/city-regions.js` 保存1600×900世界座標的主陸地海岸與五區地形資料。`renderCityRegions({label,names})` 回傳分區層，直接放在既有`.wm-world`內；同一相機帶動背景、線界、地名、霧與原地標。
- 各區以不規則閉合形狀及四條共享內界形成五城；外岸描一次，避免相鄰區各畫一條造成粗線。描線沿林地、河道與沿岸配置，並裁切於主陸地。
- 底色約6%透明度，依序為米金、青綠、暖杏、淡藍、淡紫。CSS `--wm-city-tint-opacity:0`可供審稿比較僅邊界的效果；沒有增加玩家操作選單。
- 城名是網頁文字，集中於`play/worldmap-v4/text.js`的`cityNames`，不烙進圖片。family ID、原書ID及解鎖邏輯不依賴顯示語言；既有繁中介面與未完成語言的顯示規則維持。
- 新層使用`pointer-events:none`，城名不充當關卡按鈕，原有地標可直接點擊。文字標牌開關也控制城名顯示；省界仍保留作地理輪廓。

新CSS／JS與文字載入使用`five-cities-1`，僅更新海圖來源及由`scripts/build-game-entry.py`產生的`game/index.html`。未改原首頁、心智圖、繪本原稿／經文、閱讀器、城池、書架或Pages發布來源。前一輪內容稽核另保留於[PR81](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/81)，沒有把稽核建議混入這次地圖試做。

## 審閱方式

本輪先提供試版與截圖，尚未合併或公開部署。由專案根目錄啟動：

```sh
python3 -m http.server 8765
```

開啟`http://127.0.0.1:8765/game/?v=five-cities-1#map`。這是實際本機HTTP啟動方法，並非已上線的公開預覽。

[實際截圖與驗證範圍](../../previews/worldmap-five-cities/README.md)。分區圖層總覽直接使用相同HTML／SVG實作層，另有真正遊戲內畫面，兩者在紀錄中分別標示。手機／平板的Chromium操作模擬與實機Safari須分別記錄。
