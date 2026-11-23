# 模組城池：本機整合驗證

基準：`6bb59a61d5d045b87102989532a55dc814eafa42`。本目錄是本輪本機驗證，並非正式網站發布證明。

完整重現：

```sh
python3 -B scripts/check-game-modular-city.py
```

[最終驗證報告](validation.json) 的 `result` 為 `passed`，無非預期 JavaScript 或 HTTP 錯誤。最後一次一鍵執行包含實際完整四聖諦 29 步、末頁明確完成、原有疑／波旬對話、閱讀獎勵、進城手動安置法輪碼頭，以及五陰原閱讀器 0–3 步的重新整理、旋轉與續讀。城池不阻擋下一本閱讀。

其餘安置、相依、備份及故障測試使用**獨立合成歷史存檔**，不表示實際讀完十四本。已驗證：

- 舊十四本已讀存檔擁有 14 項、初始安置 0 項；原生自動安置後為 14 項；重複安置不計數。
- 六門須先放身體城池；四念處守門人須滿足相依；只有歷史七覺支紀錄時保留所有權與待安置紀錄，不補齊未讀前置。
- 原生滑鼠拖放、CDP 單指垂直拖放與卡片列水平滑至第十四張；無誤放、無殘留拖曳影像。
- 六門恰為六座、念守門人恰為一位；七覺支的六位其他夥伴與念燈柔光不重畫守門人。
- 1280×900、360×800、844×390、768×1024、1024×768：實際點擊城主／波旬、內心 OS 固定於螢幕座標、縮放與回全景、文字與 48px 操作區、無頁面橫向溢出。截圖含最新全身波旬素材。
- 普通動態實測五個五蓋角色旋轉介於 ±3°、城主汗滴顯隱；減少動態偏好下停止動畫。
- 設定重設及作者重設的取消不改存檔；確認只清遊戲自己的閱讀／城池資料，保留其他網站鍵值。
- 真正下載與還原 v2 閱讀＋城池備份；壞資料無部分寫入；舊 v1 閱讀備份清除不相符城池、保留書籤；配額失敗以暫時存檔誠實提示且可重新載入。
- 注入素材 404 後重試仍顯示錯誤提示，草地與閱讀不被阻擋。
- 615 個原站檔案保護；十四本 HTML 僅橋接 query 版本更新，正規化後全文與基準相同；原經、原圖、原閱讀器 JS/CSS、首頁 SEO 與 Google 驗證檔不變。橋接僅回程快取 query 更新。首頁 14 冊、32 心智圖主題及前三本獨立閱讀模式的翻頁／原經／回地圖通過。

## 實際畫面

- [真實第一本完成後的城池基底：尚未安置](native-first-city-base-unplaced-1280x900.png)
- [真實手動安置法輪碼頭](native-truth-dock-hand-placed-1280x900.png)
- [五陰續讀後回城，安置仍保留（手機）](native-city-persists-after-reading-360x800.png)
- [歷史前三本：拖放安置六門](historical-three-native-drag-six-gates-1280x900.png)
- [歷史四念處：手放單一守門人](historical-mindfulness-hand-placed-one-guardian-1280x900.png)
- [歷史十四本：明確按自動安置後的全城](historical-all14-explicit-autoplace-1280x900.png)
- [手機全身波旬與螢幕座標心聲](mara-screen-thought-camera-independent-360x800.png)
- [手機橫式心聲](mara-screen-thought-camera-independent-844x390.png)
- [平板直式心聲](lord-screen-thought-768x1024.png)
- [平板橫式心聲](lord-screen-thought-1024x768.png)

## 獨立元件證據

以下報告由 `camera_controls` 的獨立元件測試提供，來源為 `/workspace/artifacts/modular-city-scene/`；與上面的正式整合流程分開，不冒稱為另一輪完整讀書測試：

- [五尺寸元件驗證](independent-scene-validation.json)
- [原生手勢與故障驗證](independent-scene-gesture-validation.json)
- [四尺寸單指拖放驗證](independent-scene-touch-drag-validation.json)

## 限制

本輪為 Chromium 桌面尺寸、滑鼠與 CDP 觸控模擬，**未測 iPhone／iPad 實機 Safari**。未重新翻完全部十四本；原內容與未變更的閱讀核心以逐位元保護及既有測試紀錄為依據。全部十四項安置畫面屬明確標示的歷史存檔測試。正式網站需另依精確 merge SHA 的 Pages 成功與實際 HTTPS 流程驗收。
