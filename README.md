# SutraZen

佛法修道地圖與十四本互動繪本，以繁體中文閱讀導讀、插畫、口白及經文。

- 正式網站：https://sutra-zen.github.io/
- GitHub專案：https://github.com/Sutra-Zen/sutra-zen.github.io
- 維護規則：[AGENTS.md](AGENTS.md)
- 專案現況：[docs/PROJECT.md](docs/PROJECT.md)
- 最新交接：[docs/HANDOFF.md](docs/HANDOFF.md)

這是原 `rooneyflower-star/sutrazen-map` 改名後的同一個專案，保留完整歷史與既有內容。網頁從網域根目錄提供，不加專案名稱前綴。雲端資料夾可能仍叫 `/workspace/sutrazen-map`，不影響正式網址。

## 本機閱讀與檢查

在專案根目錄執行：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

開啟 http://127.0.0.1:8765/ 。請使用HTTP方式；檔案管理器的HTML預覽不等於瀏覽器完整執行JavaScript。特定繪本的建置／驗證說明見交接文件及scripts/；遷移後根路徑檢查可執行 `python3 scripts/check-site-migration.py`。

## 繪本旅程試玩版

遊戲入口為 `/game/`，與原首頁、心智圖及十四本繪本並存。本機可開 http://127.0.0.1:8765/game/ 。入口共用 `play/worldmap-v4/` 的程式、資料與素材；`python3 -B scripts/build-game-entry.py --check` 可確認入口模板同步。城池與收集書架讀取同一份本機閱讀紀錄，只有末步明確完成才計入已讀。

首次公開實作與發布界線見 [遊戲交接](docs/play/game-release/README.md)。公開驗收以該次 PR 的精確 merge SHA、Pages 成功及正式 `/game/` 結果為準。遊戲 QA 圖片保留在 GitHub；`_config.yml` 僅排除九個遊戲測試證據目錄，避免大型審稿截圖占用 Pages 體積，不排除繪本或來源素材。

## 發布方式

已核對GitHub Pages使用 **main分支、根目錄 `/`**，由GitHub內建的 `pages-build-deployment` 自動建置與部署，沒有自訂發布workflow。維護時從最新main建立分支及PR，獲授權才合併；合併後確認同一SHA的Pages建置成功，再驗證正式網址。保留此流程，不需改成其他部署服務。

每次發布提供固定版本ZIP備份，並記錄驗證結果。Notion工具不可用時交付待補記文字，明確說明尚未寫入。

網站SEO與Google驗證維護：見[逐頁清單及建置說明](docs/seo/README.md)，交接版本2026-11-21-r2。全站metadata檢查：`python3 -B scripts/build-seo.py --check`。請永久保留根目錄Google驗證原檔。
