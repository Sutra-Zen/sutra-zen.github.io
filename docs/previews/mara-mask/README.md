# 波旬蒙面造型驗證與代表截圖

結果：本機 focused 驗證通過。基準為 PR89 main `e05cad72747769adbbd9ed4a713c6a237ed353f4`。本輪沒有重新逐頁讀完十四本。

- [實際互動報告](runtime-report.md)與[結構化紀錄](validation.json)：1／3／7／14 本合法依序已讀的隔離測試存檔 × 360×800、844×390、1024×768、1280×900，共16組城池畫面與原生鏡頭操作。這些是 fixture，不是本輪實讀成果。
- 點波旬顯示共用新頭像，X關閉與焦點正常；原閱讀存檔位元保持。650ms 真實漂浮取樣與 reduced-motion 停止通過，完整面具、兜帽、雙翼及雙腳留在SVG圖框內。
- 最新正式工具重播仍維持作者原四幕，不插入舊波旬。舊 `mara-watches` 只以獨立唯讀元件fixture驗證新頭像；不冒稱一般工具可開此幕。runtime未請求揭面後圖片，JS／同源HTTP錯誤為0。
- [獨立來源保護](source-validation.json)：632個受保護檔、50張舊圖保持，十四本HTML僅bridge query；新四圖逐位元吻合核可預覽，manifest／sprite座標／provenance一致。22個變更JS語法通過，故事台詞／IDs／graph、城池位置／CSS、完成資格及保存邏輯不變。
- 共享game產生器、SEO15、原電車素材檢查及diff檢查通過；Seven離線ZIP重新產生仍與前版相同。正式站精確merge SHA／Pages／live證據以發行PR交付留言為準。

| 畫面 | 截圖 |
| --- | --- |
| 手機蒙面波旬完整漂浮身形 | [360×800](city-masked-mara-1-360x800.png) |
| 完整城池仍使用蒙面版 | [1280×900](city-masked-mara-14-1280x900.png) |
| 短橫式城池點角色的新頭像 | [844×390](city-mara-new-portrait-7-844x390.png) |
| 保留舊場景的獨立唯讀元件 | [1280×900](legacy-mara-component-new-portrait-1280x900.png) |

手機／平板為 Chromium 視窗模擬；實機 iPhone／iPad Safari 未測。root已實際查看手機完整身形及短橫式對話截圖。
