# SutraZen 網站 HTML 與搜尋設定實作

交接版本：**2026-11-21-r2**
整理日期：2026-11-21（Asia/Taipei）
範圍：首頁＋14 個主題導讀，共 **15 頁**。本批網站 SEO 狀態皆為「待交接」。

**分工：Codex 負責網站 HTML、相關建置來源及站台搜尋設定；影片說明與 vidIQ、Notion 維護、Google 帳戶操作及搜尋成效追蹤，由使用者與 ChatGPT 在原對話繼續處理。** 此包只交接網站實作，附件資料足以開工，無需先取得 Notion 存取權。

- 專案：[Sutra-Zen/sutra-zen.github.io](https://github.com/Sutra-Zen/sutra-zen.github.io)
- 正式網站：[SutraZen](https://sutra-zen.github.io/)
- 文案溯源：[Notion 主表](https://app.notion.com/p/8f8daff1a1714a8481cef0deba7909ac)
- 分工與進度：[Notion 交接頁](https://app.notion.com/p/41fcf2ef57db8116ac3ae1b08b219840)

## 1. 使用方式與本次交付

先讀本 README，再讀 `seo_pages.json`；`CODEX_PROMPT.txt` 可獨立貼給 Codex。JSON 包含全部 15 頁的標題、摘要、正式網址、檔案路徑與逐頁備註。

從最新 main 開始，先讀 `AGENTS.md`、`docs/PROJECT.md`、`docs/HANDOFF.md`，確認 remote 與現有工作區變更。本次完成可審閱的修改、預覽與驗證紀錄；正式發布依使用者後續指示及專案規則處理。先前單一經號修正的發布指令已完成，不延伸為本批 SEO 發布指令。

## 2. 基準版本與已完成的四正勤修正

本次確認的 main 基準：[`db3a882b4ec2d4dd7647cbbeef9f4622a214cb84`](https://github.com/Sutra-Zen/sutra-zen.github.io/commit/db3a882b4ec2d4dd7647cbbeef9f4622a214cb84)。開始實作時重新確認最新 main，保留更新的內容。

四正勤來源卡已在 [PR #54](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/54) 修正完成：

> 《相應部》49.23–34（節錄）｜依戒修習四正勤

`right-effort/index.html` 與 `docs/right-effort/verified-sources.json` 已同步；[對應 SHA 的 Pages 流程](https://github.com/Sutra-Zen/sutra-zen.github.io/actions/runs/44856163354) 成功，正式四正勤專頁 HTTP 200 並顯示新標題。這項修正已完成，保留現有標題、經文與按鈕連結。

本次驗收確認的是本站標題及 href；沒有把兩個 SuttaCentral 外站內容載入列為已驗證。這不影響本批 SEO 工作。

SEO 仍待實作：同日原始查核涵蓋首頁與 14 導讀；本次複查首頁、四正勤、六處、十二因緣，仍未見 canonical，六處與十二因緣仍缺 description，根目錄 `sitemap.xml`、`robots.txt` 仍回傳 404。robots.txt 不存在本身不代表封鎖搜尋。

## 3. 逐頁資料如何套用

| JSON 欄位 | 實作用途 |
| --- | --- |
| `source_path` | 相對於專案根目錄的導讀 HTML；進一步追查真正產生它的來源。 |
| `seo_title` | 該頁 HTML `<title>` 的完整文字。 |
| `meta_description` | 該頁 `<meta name="description" content="…">`。 |
| `canonical_url` | 該頁 `<link rel="canonical" href="…">`；也是本批 sitemap 的網址。 |
| `primary_question` | 內容定位參考，不是搜尋量數據，也不要求自動新增 FAQ 或改 H1。 |
| `implementation_note` | 該主題應保留的內容界線與必要注意。 |
| `website_status` | 此交接快照的實作狀態；不是部署或收錄證明。 |

每頁更新已有標籤，缺少才新增，避免重複 `title`、description 或 canonical。標題與摘要已依現有內容整理；不要整段貼入 YouTube 長說明或堆疊 Hashtag。文字長度是編輯取捨，不作 Google 的硬性字數上限。

| 順序 | 頁面 | 檔案 |
| --- | --- | --- |
| 00 | 首頁 | `index.html` |
| 01 | 四聖諦 | `four-truths/index.html` |
| 02 | 五陰 | `five-aggregates/index.html` |
| 03 | 六處 | `six-senses/index.html` |
| 04 | 十二因緣 | `twelve-links/index.html` |
| 05 | 八正道與十善業道 | `eightfold-path/index.html` |
| 06 | 四向四果與十結 | `four-fruits-ten-fetters/index.html` |
| 07 | 四不壞淨與六念 | `four-purities-six-recollections/index.html` |
| 08 | 四念處與四顛倒 | `mindfulness/index.html` |
| 09 | 四正勤 | `right-effort/index.html` |
| 10 | 安那般那與止觀 | `anapana/index.html` |
| 11 | 四如意足 | `iddhipada/index.html` |
| 12 | 四禪 | `four-jhanas/index.html` |
| 13 | 五根五力 | `five-roots-powers/index.html` |
| 14 | 七覺支 | `seven-factors/index.html` |

首頁文案以 JSON `order: 0` 為準。維持可見 H1「三十七道品修道地圖」。

## 4. 優先實作

### 15 頁 metadata 與建置來源

1. 依 JSON 套用全部 15 頁的 title、description、canonical，優先補六處、十二因緣的摘要。
2. canonical 使用正式絕對網址：首頁 `https://sutra-zen.github.io/`，導讀 `https://sutra-zen.github.io/<slug>/`。同一導讀的 `/slug/index.html` 與 `/slug/` 採同一 canonical，保留原經錨點連結的用途。
3. 查明各頁 head 是手寫或由何處產生。若模板、資料檔或建置步驟會覆寫 metadata，應同步真正來源，避免下次建置遺失；不因存在 `build-*.py` 就無差別重建全部繪本。
4. 保留既有正文、經典出處、原圖、分鏡、reader 控制與深連結，以及首頁 14 本書架、32 個心智圖節點的專頁／繪本／影片入口卡片。
5. `book/` 閱讀器與導讀用途不同；不批次將全部 reader canonical 指到導讀，也不批次新增 noindex。

### sitemap.xml 與 robots.txt

- 在根目錄建立有效的 `sitemap.xml`，本批精確包含 JSON 內 15 個 canonical_url。不要重複列出 `index.html`、舊網域、錨點或查詢參數。
- `lastmod` 有可靠的實際內容修改日期才填，沒有則省略。
- 根目錄 `robots.txt` 明列 `Sitemap: https://sutra-zen.github.io/sitemap.xml`，並依站主既有政策確保搜尋存取未被誤封。
- Googlebot、Bingbot、OAI-SearchBot 的搜尋用途與 GPTBot 等模型訓練用途分開處理，保留站主既有訓練政策。
- 部署沿用 GitHub Pages 的 main 分支、根目錄 `/` 及 GitHub 管理的 `pages-build-deployment`。

### 取得實際驗證值後：Google 網站驗證

使用者取得真正的 Google HTML 驗證檔或驗證標記後，Codex 再將原檔放到網站根目錄，或將原標記放到首頁 head；保留原檔名與內容，並確保後續建置不覆蓋。驗證完成後仍保留驗證檔／標記。目前沒有實際驗證值時，將此項列為待補，繼續完成其餘 SEO，不填示意 token。

## 5. 第二優先：分享預覽與結構化資料

可補 `og:title`、`og:description`、`og:url` 與合適的 Twitter card，文字對齊本批文案。圖片沿用真實、可公開讀取的圖檔並確認絕對 URL；六處目前封面含 data URI，應另核對可沿用的公開圖檔，不直接使用 base64 作為 `og:image`。

可依真實內容加入 WebSite／WebPage 資料。VideoObject 先核對頁面用途、影片標題、縮圖、上傳日期與 embed URL；資料不完整就清楚列出待補項。若加入 JSON-LD，驗證語法與來源。這些設定不代表保證取得豐富結果或 AI 引用。`llms.txt` 不列為本批必要交付。

## 6. 驗收與回報

1. 15 頁 title、description 非空且各自適切；canonical 精確對應 JSON。每頁各有一組設定，沒有舊網址或非預期 noindex。
2. 透過本機 HTTP 開啟首頁與 14 導讀，確認主要正文與原有入口可讀。解析 sitemap，確認 loc 集合恰為本批 15 個 canonical，robots 的 Sitemap 指向正確。
3. 檢查產生來源與 diff，確保之後建置能保留 metadata，經文、原圖、分鏡、reader 控制與已完成的四正勤經號修正沒有意外變更。
4. 分享圖片與 JSON-LD 若有改動，核對實際可用的 URL、JSON 語法與真實資料。
5. 可見文字或導覽有改動時，驗證受影響頁面的手機／平板橫直式與「導讀 → 繪本 → 原經 → 回地圖」。純 head 變更以 metadata、網址、建置來源及差異檢查為主，不重跑全部繪本的每頁操作。
6. 交付修改檔案、逐頁套用清單、可審閱 diff／PR／commit、實際驗證結果及未完成項，並更新 `docs/HANDOFF.md`。回報中註明使用交接版本 `2026-11-21-r2`。
7. 未來依使用者指示正式發布後，核對精確 merge SHA 的 Pages 成功與正式網址，回報實際套用結果。Notion 進度由原對話更新，不由 Codex 代寫。Google 收錄狀態與成效在原對話後續追蹤。

## 7. 參考依據

- [Google 搜尋摘要](https://developers.google.com/search/docs/appearance/snippet)
- [標準網址](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Sitemap 概覽](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
- [robots.txt 規則](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec)
- [Google 網站擁有權驗證](https://support.google.com/webmasters/answer/9008080?hl=zh-Hant)
- [OpenAI 搜尋與訓練爬蟲](https://developers.openai.com/api/docs/bots)

專案規則以開工時最新 main 的 `AGENTS.md`、`docs/PROJECT.md`、`docs/HANDOFF.md` 為準。此包不含網站完整原始碼或繪本圖片，逐頁資料足以對應現有 repository 實作。
