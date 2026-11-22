# 開場對話與城池閱讀回饋：實際驗證

本機驗證通過，基準 `be78106f6414ebf447eaedadd5c94883359be58e`；此處不能推定正式站已發布。根目錄執行 `python3 -m http.server 8000`，開啟 <http://localhost:8000/game/>。完整針對性檢查為 `python3 -B scripts/check-game-city-story.py`。

[主驗證報告](validation.json) 包含：

- 五尺寸的首次上方對話、透明小貓肖像、可選取的作者原句、清楚的閱讀／先看地圖按鈕，且不覆蓋底列。海圖已無城池徽章，底部城池入口保留。
- 對話在顯示時就記錄一次；未關閉直接前往城池再返回、書架返回、讀本返回、重整及還原同一瀏覽器存檔都不自動重播。手動重播只回目前主線，不重開第一本或改寫進度。
- 從新對話的「進去看看」真正逐步讀完四聖諦 29 步，末頁按完成才記錄一本並顯示法輪碼頭回饋；下一站留在海圖定位五陰。再完整複習 29 步沒有新增本數、重播回饋或改變主線。
- 開場紀錄與閱讀紀錄分開；儲存失效仍可閱讀，同頁籤返回不重播。模型另驗證重複紀錄、未知場景、壞資料、quota 寫入失敗、session 備援與外部新紀錄優先。注入一次肖像下載失敗時仍有全文及操作，重播可恢復肖像。
- 五尺寸城池初始保持完整顏色，只在尚未取得的部件使用局部柔雲；沒有整幅灰階、低透明度或重複底圖遮罩。
- 依旅程順序完成前十二本時沒有七覺支夥伴；前十三本才顯示六個既有繪本角色局部，加上同一位念守門人的念燈暖光。五根五力連線只連動實際完成的來源書。
- 七覺支等創作城景標為「繪本場景延伸」；原城喻與混合場景另有分類。延伸獎勵已讀時連到該繪本專頁出處，未取得時沒有錯指城喻頁的來源按鈕。詳情切換會回到頂端，來源標題與關閉鈕可見。
- 稀疏歷史存檔不補造前置完成：只完成七覺支時先保留待安置預覽；五陰＋七覺支時六個角色可見，念守門人仍待城門與四念處齊備，畫面及狀態文字都明示等待。未來書籤不解鎖或生成獎勵。
- 615 個原站內容／經文／插圖／讀本 HTML／首頁／SEO／Google 驗證與建置保護檔未變，存檔／資格／橋接／旅程順序／來源拓樸及既定首頁也未變。零非預期 JavaScript／HTTP 錯誤。

| 畫面 | 桌機 | 手機直式 | 手機橫式 | 平板直式 | 平板橫式 |
| --- | --- | --- | --- | --- | --- |
| 首次開場 | [1280×900](map-intro-1280x900.png) | [360×800](map-intro-360x800.png) | [844×390](map-intro-844x390.png) | [768×1024](map-intro-768x1024.png) | [1024×768](map-intro-1024x768.png) |
| 城池 0 冊 | [1280×900](city-0-1280x900.png) | [360×800](city-0-360x800.png) | [844×390](city-0-844x390.png) | [768×1024](city-0-768x1024.png) | [1024×768](city-0-1024x768.png) |
| 前 13 本歷史存檔示意 | [1280×900](city-13-history-fixture-1280x900.png) | [360×800](city-13-history-fixture-360x800.png) | [844×390](city-13-history-fixture-844x390.png) | [768×1024](city-13-history-fixture-768x1024.png) | [1024×768](city-13-history-fixture-1024x768.png) |
| 七覺支來源／創作分類 | [1280×900](companions-source-history-fixture-1280x900.png) | [360×800](companions-source-history-fixture-360x800.png) | [844×390](companions-source-history-fixture-844x390.png) | [768×1024](companions-source-history-fixture-768x1024.png) | [1024×768](companions-source-history-fixture-1024x768.png) |

[真實首本完成回饋](intro-first-book-completion-1280x900.png)。城池 13 本等示意採隔離的合法歷史存檔，**不代表本輪逐頁完成十三或十四本**，也沒有修改作者的瀏覽器。只有上述首本完成及複習使用真實主按鈕全程操作；前輪 1192 步原稿報告保持原樣。

另附由獨立 reviewer 執行、原封複製的 [四組歷史×五尺寸檢查](independent-city-review.json) 與 [五尺寸共 70 次原生城景點選](independent-city-interactions.json)。來源分別為 `/tmp/game-city-independent-review.json` 與 `/tmp/game-city-independent-interactions.json`，範圍是本輪城景與來源互動，不是全十四本閱讀宣稱。

肖像為本輪新生成的透明概念稿；城中六位夥伴使用既有七覺支原圖 SVG 局部，沒有將它們宣稱為新製獨立角色稿。實測為桌面 Chromium／CDP，未測實機 iPhone／iPad Safari。
