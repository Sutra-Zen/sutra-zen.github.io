# 對話文字選單與繪本字幕留白

2026-11-25，接續已發布PR88／main `a079a9191425e18b24dfd9371f52e91532802158`，分支`fix/dialogue-buttons-reader-space`。環境恢復後，完成作者先前待辦的兩項：終幕以完整文字選項取代X，與減少寬版多留的第三行字幕空間。

## 終幕兩個文字選項

主線中間仍只有「接著看」，原checkpoint精確續幕與導航門禁不變。最後一段移除X，顯示「回到地圖」和「閱讀下一關」：前者只確認對話並清pending，回自由探索、不開書或計完成；後者經原資格／書籤判定，直接開合法目前關卡。工具重播保持唯讀，可回地圖，終幕只留一個回地圖按鈕。

四聖諦首本尾幕保留完整作者台詞，並在同一面板加入原本的讀完提示、地景亮起、城池自動新增與已讀本數。兩個選項直接回圖或進五陰，不再先繞到另一層通知選單。新增通知沿用原純讀renderer，不重發獎勵；原seen cutoff、receipt、完成數與pending context保持。其餘書的完成通知亦提供回地圖／閱讀下一關；十四本全完成時保留「觀看旅程結尾」，回地圖仍可自由探索。

## 同一視窗固定兩行或三行

原`reader-layout.js`一律`capLine*3`造成寬版多留一行。實際14本字幕量測確認1280×900、1024×768、844×390與900×600最多兩行；667×375及800×600確有三行需求，字級與實際可用寬度須一併考慮。

共享框架現在以`scene.clientWidth < 36 * capFont + 168 ? 3 : 2`統一決定預算。同一viewport／字級所有書與頁一致，不因當頁短句或段數伸縮；寬版收回一行留白，窄版需三行時保留；圖像仍依原比例與寬度上限縮放，受高度限制時可實際增高，已到寬度上限者不強行放大。既有長文內捲、原字級、控件避讓、直式文件流、心經直書置中／窄框右起及結語欄位維持。極窄長句仍可捲完整，不line-clamp或刪文。只改shared JS，reader-controls CSS未變。

## 來源、保存與產生流程

遊戲cache `dialogue-two-1`保持story/reset/pending單例，讀本shared layout cache `reader-two-1`。十四本HTML僅bridge／shared layout query，原生book JS/CSS/CSV與插畫、經文／台詞、route資格、合法完成／位置、seen/pending/reading/city與備份schema均保持。source worldmap shell與產生的/game同步；Seven Factors離線ZIP重新產生30成員，只有shared layout JS與其book HTML的query改動，原書及原圖逐位元不變。

[測試與代表畫面](../../previews/dialogue-reader-space/README.md)區分原生操作及完成fixture。Pages保持legacy main:/，本輪QA排除共32目錄。發布沿作者既有授權，精確PR／merge SHA／Pages及正式站證據記於本輪PR；實機iPhone／iPad Safari未測。
