# 四如意足・Codex交接包

兩包皆需下載，解壓後合併同名資料夾。每包小於32,000,000 bytes，為互補的普通ZIP。Part1含全部文件與JSON、定位影格、S01–S05原圖；Part2含S06–S09原圖及S06有字備用圖。MOV不包含。

讀取順序：CODEX_PROMPT.txt → docs/STORYBOARD.md → docs/OVERLAY_SPEC.md → docs/SOURCE_NOTES.md。結構化資料：storyboard.json、scripture-catalog.json、overlays.json。Notion原始快照在docs/NOTION_SNAPSHOT.md；離線閱讀請用STORYBOARD.md，其圖片已換成包內路徑。

內容：9幕、81段口白、11筆Q經文卡、13條教學疊字；9張正式原圖＋1張有字備用圖＋9張影片定位影格。原圖不修改像素。時間碼為約1–3秒誤差的字幕定位，未完成音軌逐字聽校；最後時間以影片443.77秒為準，Notion表格顯示到07:23。

原經文類型：Q01–Q08巴利摘錄與本頁中文譯意；Q09影片下緣摘錄；Q10–Q11古漢譯。現代譯文連結為閱讀對照，不將本頁譯意署名莊春江。口白為影片創作，維持與原經的區別。

合併後在本資料夾執行 python3 scripts/validate.py。asset-manifest.json含所有交付檔案的SHA256及大小。不要用references影片截圖取代assets正式原圖。頁面：https://app.notion.com/p/41acf2ef57db818cb5b1e8f03025b9b8
