# 帳號／專案改名後的一次性驗證

2026-11-19，基準main `2ec341a6ffa1a4f0108183da980e9af85c55bd31`；新專案https://github.com/Sutra-Zen/sutra-zen.github.io ，正式站https://sutra-zen.github.io/ 。initial-state.json記錄實際repository ID、Pages來源、初始main與工作樹／remote。

## 已驗證

- 專案ID1441581789與原庫相同，main包含十四本及安那般那最新修正；初始工作樹乾淨，不需stash、reset或搬移資料夾，origin更新。
- Pages API：legacy，source main的`/`，無CNAME，HTTPS強制，managed pages-build-deployment，沒有追蹤的自訂workflow。沿用原發布方式。
- 29份網站HTML，325個本機相對連結／圖片／樣式／程式引用全部存在，沒有舊站網域或舊專案網址前綴。既有七覺支離線ZIP CRC通過，內部文字檔沒有舊站網址。
- 360×800、800×360、768×1024、1024×768、1440×900：每尺寸從書架進入十四本，各實際載入圖片、下一頁／上一頁、返回導讀、返回首頁，共70個完整閱讀器動線，無JS或本地HTTP錯誤、無水平溢出。五陰原有第一頁純文字，先正常翻到插畫再驗圖，沒有把純文字頁誤當缺圖。
- 所有網站HTML／CSS／JS、原圖、原稿、讀經及翻頁內容與基準main逐檔一致；只改規則、說明、維護中文件連結、四支檢查的預設根路徑及本次驗證工具／記錄。

## 重現及限制

執行 `python3 scripts/check-site-migration.py` 可在暫時的本機HTTP根路徑測試；`--url https://sutra-zen.github.io/` 才是正式站直接測試，兩者不能混稱。實測本機命令：

```sh
python3 scripts/check-site-migration.py --tailwind-js /tmp/tailwind-site.js --lucide-js /tmp/migration-lucide.min.js
```

這兩個檔案是執行環境的套件副本，不是專案素材；參數只在測試瀏覽器替換CDN請求，網站本身未改用副本。Tailwind為既有下載檔，Lucide於本次從原unpkg網址讀取，雜湊見local-validation.json的cdnSubstitutions。環境瀏覽器受外站憑證限制，Tailwind伺服器另對該環境請求回Cloudflare1010；本輪沒有宣稱CDN連線已驗收，也未關閉TLS驗證。

**正式站直接驗收尚未完成。** 現行雲端允許清單未包含sutra-zen.github.io，實際CONNECT403；已透過非阻塞問題請作者在環境設定新增／儲存套用。GitHub API發布及Pages建置核對不受此host限制，不能把此403當作網站不存在或部署失敗。設定套用後需再執行正式站檢查。實體Safari亦未測。

本機報告local-validation.json、首頁及安那般那橫直截圖位於此目錄；本次PR補上最終合併SHA／Pages及workflow成功證據／完整固定SHA ZIP核對。Notion尚未寫入，見../../releases/site-migration-notion.md。
