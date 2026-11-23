# 自動城池：整合驗證

基準：`1ba30cfb016ed6affaefe1a62ee6ae9d1678efd9`。本目錄為本機實測，正式發布須另核對精確 merge SHA 的 Pages／HTTPS 結果。

```sh
python3 -B scripts/check-game-auto-city.py
```

[驗證報告](validation.json) 為 `passed`，無 JavaScript 或非預期 HTTP 錯誤。單一腳本可重現完整檢查。

只有 `nativeFirstAutoCityFive` 是**真正從第一頁逐次按下一頁讀完四聖諦 29 步、再按末頁「完成這本」**。依序走完心得、疑退場、波旬、五陰湖尾幕後，才顯示自動新增法輪碼頭的通知；按「前往城池看看」，碼頭已在場，不須安置。實際點城主對話與 X、點廣場經典出處與 X，再全景／精確返回鏡頭，回地圖讀五陰 0–3、重整、旋轉及回城，書籤仍在，完成數仍為 1。

## 實際畫面

- [真實第一本完成：尾聲之後的新城景通知](actual-first29-auto-city-notice-1280x900.png)
- [真實第一本完成：已自動出現碼頭的大城景](actual-first29-city-automatic-dock-1280x900.png)
- [城主對話只留右上 X](actual-first29-lord-dialogue-1280x900.png)
- [真實第一本完成：全景模式](actual-first29-overview-1280x900.png)
- [五陰續讀返回城池（手機）](actual-five-resume-city-360x800.png)
- [歷史 3 本，自動顯現六門](historical-3-read-automatic-1280x900.png)
- [歷史 7 本，自動顯現單一守門人](historical-7-read-automatic-1280x900.png)
- [歷史 14 本，自動完整城景](historical-14-read-automatic-1280x900.png)
- [手機直式：大城景與底列](automatic-city-seven-360x800.png)
- [手機橫式](automatic-city-seven-844x390.png)
- [平板直式](automatic-city-seven-768x1024.png)
- [平板橫式](automatic-city-seven-1024x768.png)
- [擇法貓頭鷹對話](companion-owl-dialogue-1280x900.png)
- [精進兔子對話](companion-rabbit-dialogue-1280x900.png)
- [喜藍鳥對話](companion-bird-dialogue-1280x900.png)
- [輕安烏龜對話](companion-turtle-dialogue-1280x900.png)
- [定蓮花對話](companion-lotus-dialogue-1280x900.png)
- [捨小鹿對話](companion-deer-dialogue-1280x900.png)

以上「歷史」及五尺寸／六夥伴畫面為**明確標示的獨立合成存檔**，不表示本輪讀完全部十四本。全景保留自然縮放的完整城景；返回後恢復原鏡頭與正常閱讀字級。

## 已驗證

- 移除上方選項列、庫存、＋、選取、拖放、手動／自動安置按鈕與安置數；移除「心想」「換個人想什麼」「繼續佈置」等舊玩家介面。閱讀進度與續讀保留在底列，城市本身占滿視窗。
- 歷史 1／3／7／14 本，即使舊 `placedIds` 為空也依已讀自動顯現；舊布局與已讀不符時不會贈送未讀場景。只有七覺支的非順序歷史紀錄不補前置讀本。進城與重新整理不改閱讀原始 JSON，亦不為自動城景寫入安置資料。
- 六門恰為六座、守門人恰為一位；六位七覺支夥伴逐一原生點擊開各自創作對話、右上 X 關閉。仍只有一位念守門人，沒有第二隻念貓；六個對話紀錄沿原 city v1 格式保存、重新整理及重複點擊不重複計數。
- 1280×900、360×800、844×390、768×1024、1024×768：整合畫面原生單指拖曳、雙指縮放、旋轉、不誤開角色／來源，無頁面外溢。右上全景與左上返回精確還原鏡頭；舊無返回快照的全景紀錄仍能回正常城景。
- 真正下載 v2 閱讀＋城池備份，重設取消完全不改資料；確認只清遊戲資料、保留無關鍵值。v2／舊 v1 還原皆由已讀重新顯現城景；壞 city 資料不造成部分寫入。
- 615 個原站檔案保護；十四本 HTML 只允許 bridge cache query 更新、正規化後全文等同基準。原稿、經文、原圖、閱讀 core、receipt、資格、路線、SEO 與 Google 驗證檔保留。首頁 14 冊／32 主題、前三本獨立閱讀的翻頁／原經／回地圖，以及 SEO／遊戲入口建置檢查通過。

最後驗證範圍：先完整跑過原生 29 步與全矩陣；之後修正透明城界攔廣場點擊，以及補六位夥伴對話，僅針對最終程式重驗歷史 3／7／14 廣場來源與 X、全部六位夥伴、保存與閱讀資料不變，未因互不相干的點擊小修重讀整本。報告 `runScope` 保留此區分。

## 獨立元件證據與限制

由 `camera_controls` 元件測試提供，來源 `/workspace/artifacts/auto-city-scene/`，與整合主流程分開：

- [五尺寸原生鏡頭／點擊／故障／減少動態](independent-scene-validation.json)
- [全景標牌自然縮放及返回](independent-overview-validation.json)

本輪為 Chromium 尺寸、滑鼠與 CDP 觸控模擬，**未測實機 iPhone／iPad Safari**。未重翻全部十四本；原內容以逐位元保護與既有完整閱讀測試為依據。雲端存檔不在本輪範圍。
