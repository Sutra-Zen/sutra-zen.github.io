> 目前遊戲請以[沉浸式旅程與統一資格規則](../game-immersion/README.md)為準。以下保留本階段的歷史設計與驗證；舊的遊戲自由選讀／任意書籤優先已移除，十四本公開原網址仍自由閱讀。

# 繪本旅程首次公開試玩發布檢查

本次依作者的新指示，準備將現有旅程實作以 `/game/` 提供公開試玩。正式首頁、十四本導讀與原繪本網址不替換；`/game/` 是共用既有山海世界執行程式的輕量入口，沒有複製一份大型美術或另建閱讀內容。公開是否完成，以精確 merge SHA 的 Pages 成功及正式網址驗收為準，本文件本身不是已發布的證明。

## 分支與發布來源

檢查時，正式 `main` 為 `b9a0dad2c2c34d7e15e6dc5e55d6125de630f57b`；原型分支的 `a2b3225220cbf579d5ace90352081dee91fb753e` 已包含這個 main，沒有落後的正式內容需要覆蓋。原草稿 PR58 以 main 為目標，PR59 以 PR58 的實作分支為目標。首次公開版使用獨立 `release/game-first-playable` 分支，將完整實作及本次發布修正一起送入最新 main；保留原型分支與原草稿的審閱歷史，不必依序合併兩個草稿。

GitHub Pages API 確認現有 `build_type: legacy`、`source.branch: main`、`source.path: /`、正式網址 `https://sutra-zen.github.io/`，沿用 GitHub 管理的 `pages build and deployment` 流程。沒有更換部署分支、Pages 來源或新增自訂部署 workflow。公開試玩入口刻意保留 `noindex,nofollow`；這不影響既有十五個首頁／導讀的 SEO 設定。

## Pages 體積保護

原型 `a2b3225` 的 Git 追蹤檔案合計 **957,103,187 bytes**，其中 `docs/previews/` 合計 **431,370,460 bytes**。這是部署來源檔案的估計，不是 GitHub 實際產出的 Pages artifact 大小，也不包括 `.git/`。接近 Pages 已發布網站的 1 GB 上限，因此本次不複製 `/play/` 美術到 `/game/`，也不再增加重複的 4K 全畫面匯出。

根目錄新增最小 `_config.yml`，只排除本次遊戲歷程的九個 QA 證據目錄。以 `a2b3225` 為基準，這九個目錄合計 **182,597,158 bytes**，扣除後的部署來源估計為 **774,506,029 bytes**；本次新增兩張圖與小幅程式／文件還須另計。實際 Pages artifact 仍以發布流程為準。

排除目錄如下：

- `docs/previews/play`
- `docs/previews/play-art-directions`
- `docs/previews/play-city-entry`
- `docs/previews/play-collection`
- `docs/previews/play-continent`
- `docs/previews/play-network`
- `docs/previews/play-visual-v2`
- `docs/previews/play-worldmap-v4`
- `docs/previews/play-game-release`

圖片、報告及原型審閱證據仍留在 Git／GitHub，不刪除歷史；發布後應從 GitHub 分支或 PR 查閱這些證據，不能把被排除的 QA 路徑當成正式網站網址。排除範圍不涵蓋既有其他預覽、論文 PDF、交接原圖、來源文件或任何繪本目錄。既有瀏覽器程式沒有引用這些九個 QA 目錄。其餘 `docs/` 中確實被書架封面、讀本或來源入口引用的素材照常發布。沒有新增 `.nojekyll`；排除設定由原有 legacy Jekyll 流程執行。

本目錄 `runtime-assets.json` 記錄本次檢查的九個排除路徑及其精確檔案體積、扣除後的來源估計、完整 `/play/` 執行檔案與素材清單，以及十四本目錄中的既有封面／導讀／閱讀器入口。`/play/` 清單刻意包含保留的舊原型，作為公開執行依賴的保守超集合，不聲稱每個舊畫風素材都會在 `/game/` 首屏下載。清單逐檔檢查存在、SHA-256、未被排除，並透過本機 HTTP HEAD 確認可提供；真正的公開結果仍須隨精確 merge SHA 重新驗收。

## 內容與進度界線

城池公開標牌使用「地水火風四大廣場」「止・觀使者」「如實消息・涅槃」。這是既有 SN35.245 六門城喻的標牌整理，不改原經或把閱讀完成當作修證成果。城主的皇冠、鬍子與卷軸是故事美術；城主代表識，不代表永恆主宰。

本機收集存檔仍使用 `sutrazen.play.collection.v1`；同網域的既有測試進度可沿用。既有前三本旅程存檔另行保留。只有閱讀器最後一步按「完成這本」才登記完成；回海圖、看城、自由選讀、審稿預覽或重讀不增加假完成。公開入口、城池、書架與閱讀後返回路徑必須可連續操作。

原心智圖來源的 46 筆關係保持原檔與端點；定區「四禪→四如意足→港口」仍是另列的地理展示交通線，不新增教義關係。公開入口隱藏內部美術審閱控制，舊 `/play/worldmap-v4/` 的試稿比較入口保留。

完整美術仍為作者可繼續調整的試玩素材；母圖原生解析度、來源與 SHA 見各階段素材清單。本輪城景使用 1671×941 的 `city-scroll-audience-concept.png`，城主的鬍子以獨立透明素材共用於城景、城主特寫與小型完成回饋，見本目錄 `generated-assets.json`。大型畫面截圖不等於原生4K原畫。

獨立發布整合檢查實測390×844的 Chromium 尺寸模擬：`/game/` 的試玩標示與隱藏美術審閱區、實際進入四聖諦再返回 `/game/`、完成數仍為0、城池三組標牌、城主主畫面及特寫的共用鬍子圖層、十四本書架與固定導覽皆通過，沒有本機HTTP錯誤、JS錯誤或外部水平溢出。沒有把審稿模式寫成實際閱讀完成。這個獨立檢查沒有重跑1192步；完整／本輪操作驗收另見各QA報告。實機 Safari 沒有測試時，仍須與桌面 Chromium 的手機／平板尺寸模擬分開回報。
