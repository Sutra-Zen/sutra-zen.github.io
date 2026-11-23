# 精簡遊戲介面與劇本回饋：整合驗證

基準：`d82f68533f595db032c8a787a1a2c5606a53fb2f`。本輪分段完成整合與最後針對性驗證，[最終報告](validation.json) 為 `passed`，JavaScript／非預期 HTTP 錯誤皆為 0。

```sh
python3 -B scripts/check-game-simple-ui.py
```

腳本保留單一執行入口，涵蓋下列全部功能。正式發布仍須另核對精確 merge SHA 的 Pages 與 HTTPS 流程。

## 實際驗證

- **真正讀完四聖諦 29 步**：逐次按下一頁，末頁明確完成後，依序心得、疑退場、波旬、五陰湖，只有「接著看」；Escape 不跳幕。最後通知直接在劇本對話中，沒有舊回饋 modal／「看閱讀回饋」／「看看旅程的變化」。兩選項是「前往城池看看」「前往下一站」。重整可回通知；實際選城池後接五陰 0–3、重整返回，完成數仍為 1。
- 六尺寸最後通知（1280×900、360×800、844×390、768×1024、1024×768、2048×1115）使用**隔離的已完成末頁／已確認尾聲 fixture**重現，並非另外讀完六次。文字與兩按鈕在 dock 上可達；Escape 清除呈現 URL、不改進度；下一站只定位。通知中重設後重整不復活舊通知，未讀完成 URL 不會偽造完成或新增城景。
- 地圖／城池共 12 組尺寸測試：全景、全圖與返回鏡頭按鈕完全移除，舊 overview 存檔自動回正常探索；實際單指拖曳、雙指縮放，地圖＋／−／定位與重整仍可用，閱讀資料不變。
- 書架六尺寸 × 空書架／十四本歷史，共 12 組：只有 `.collection-stage` 一層原 library 圖，body／main／case 與 pseudo 沒有第二張同圖。實際 CDP 向上／向下滑到頂、中、底並再滑邊界，未出現第二個書架頂圖；滿寬、14 卡、閱讀資格與存檔保留。
- 廣場來源六尺寸逐字比對作者指定短句，只含經名、引句及 X。延伸場景只呈主題說明、不誤掛 SN35.245，沒有圖片、複習、關卡或外連按鈕。六位創作動物用簡短覺支對應；念-守門人保留原角色台詞，兩者不混稱為同一經的原句。
- 序章六尺寸：三段六行原文完整、可選取，只有底部「點一下進入選單」；原生 click／Enter／Space 有防穿透，減少動態模式可手動閱讀。另實際等待設定 30 秒的自然播放完整結束一次，沒有 seek 或快轉。
- 地圖／城池／書架的設定可回遊戲開始選單，不重播序章、不清 reading／city／story 原字串。實際續到原五陰 index 8、重整仍在；作者重設取消不改資料，確認才清遊戲進度並重新序章／首次到達。
- 615 個原站檔案、原稿／經文／圖片／SEO／Google 保護；reading、資格、receipt、存檔格式、備份與素材保留，只允許必要 cache query。SEO／遊戲入口產生器通過。實機 iPhone／iPad Safari 未測。

除明確標示的真正首冊流程，其餘已讀冊數均為**歷史測試存檔**；本輪未聲稱實讀全部十四本。

## 代表截圖

- [真正 29 步後：劇本內的完成通知](native-first29-final-notice-dialogue-1280x900.png)
- [手機完成通知：最後全寬排版 fixture](final-notice-fixture-360x800.png)
- [桌面書架頂部](shelf-14-top-1280x900.png)／[中段](shelf-14-middle-1280x900.png)／[底部](shelf-14-bottom-1280x900.png)
- [手機空書架頂部](shelf-0-top-360x800.png)／[中段](shelf-0-middle-360x800.png)／[底部](shelf-0-bottom-360x800.png)
- [只有經名與作者指定引句的來源](plaza-short-quote-360x800.png)
- [夥伴簡短覺支對應](seven-correspondence-awakening-owl-1280x900.png)
- [城池移除全景與返回控制](city-simple-controls-360x800.png)
- [設定直接返回開始選單](settings-shelf-direct-title-menu-360x800.png)
- [片頭唯一底部 CTA](prologue-bottom-cta-360x800.png)
- [實際自然播放中的文字](natural-prologue-crawl-1280x900.png)
- [作者重設後重新首次到達](author-reset-fresh-arrival-360x800.png)

Git 保留上述 15 張代表圖，完整數值矩陣仍在 validation。其他完整矩陣截圖移至此工作環境 `/tmp/game-simple-ui-full-matrix/`，不增加 PR 或 Pages 負擔；重新執行腳本會重建再挑選代表圖。

[獨立地圖控制測試](independent-map-controls-validation.json) 來自 `camera_controls` 的 `/workspace/artifacts/map-simple-panels/validation.json`，測 source entry 的鏡頭／舊狀態復原，與本輪實際 `/game/` 整合分開。

報告 `runScope` 保留先完成的真正閱讀／全矩陣，以及最後 guardian 期望澄清、通知 reset URL 清理、手機全寬排版後的針對性重驗；未因這些呈現小修反覆重讀整本。瀏覽器驗證為 Chromium 與 CDP 模擬，並非實機 Safari。
