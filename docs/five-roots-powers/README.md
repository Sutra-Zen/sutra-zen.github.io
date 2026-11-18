# 第13本《五根五力》交接與實作

作者兩份普通ZIP已合併，沒有同名檔衝突；原包共14檔：storyboard.json、storyboard.md、CODEX_PROMPT.txt與11張PNG。原包沒有README或manifest，本檔為實作補充，receipt.json與input-zips.json為收件時產生的CRC／SHA-256記錄，未冒稱原作者清單。

原檔完整保留。`assets/S01.png`晴天無牌、`S03.png`已有「信、精進、念、定、慧」、`S09.png`風雨；各幕依JSON指定，不按上傳順序。S04、S05是1671×941，S10是1670×941，其餘正圖1672×941；不強行裁成相同尺寸。sources.png為1231×820，網頁片尾原檔可放大。

結構：

- `storyboard.json`／`storyboard.md`：十幕、74段完整口白、原始起訖時間與各幕引文，不修改。
- `scripture-catalog.json`：從原稿提取14張可重用引文卡，保留原詞／標點／斷行。S02承接SN48.43，樹根抗風說明獨立於引文。
- `reader-plan.json`：P001–P074與Q配對；S04–S08先對應646經、再依口白切至647經。S09使用675經及SN48.43，S10使用654經。
- `overlay-layout.json`：S04–S08五組黑字，x/y完全沿用原稿，未指定的字框寬度及字級另記為試排值；S03原圖牌字不重疊。
- `canonical/`／`verified-sources.json`：官方固定版原典五份及巴利對照，導讀節錄與影片錄文分開。外站註解頁因CONNECT403未驗證呈現，不能說不存在。
- 網頁為`five-roots-powers/`及`five-roots-powers/book/`，沿用最新安那般那閱讀器，接原書架13及既有地圖節點。

74段各一頁，另加片尾來源圖與共用經典依據結語，共76頁、目錄十幕。時間為秒級近似，非精準音軌字幕。作者於2026-11-18另行授權直接發布，取代原審閱限制；以PR #41發布，實際Pages與完整備份驗證見該PR。

重建：`python3 scripts/build-five-roots-powers.py`；核對：同指令加`--check`。互動驗收：`python3 scripts/check-five-roots-powers.py`。PDF：`python3 scripts/build-five-roots-powers-preview.py`。

試閱及待校項目見[預覽說明](../previews/five-roots-powers/README.md)與[REVIEW](REVIEW.md)。
