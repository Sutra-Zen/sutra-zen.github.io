# 主線逐段接續與終幕X：focused驗證

[實作／保存範圍](../../play/mandatory-dialogue/README.md) · [完整focused結果](validation.json) · [原版重現](before-proof.json) · [pending儲存驗證](pending-storage-validation.json) · [原稿與核心保護](source-validation.json)

基準PR87／`ea6dafa701670caffb5cd4e4ee4b9df05d4ff467`。原版抵達疑幕、獨立五陰入口一顯示就markseen，重整後visibleDialogs=0；「先看看地圖」也能略過未完劇情。本輪中間段強制接著看，終幕可X ack回自由探索或Enter入書，checkpoint精確保留未確認當幕。以下為實際focused結果；正式PR／merge SHA／Pages／live證據以本輪PR為準。

- fresh抵達3幕逐幕原生Next／reload，均恢復同一幕；前2無X／secondary，Escape、底部city/shelf、main、tools及實際可點地標均不能繞過、不寫reading。中途回title→train→map仍接疑幕。
- 終幕X清checkpoint、沒有開書或產生書籤；可自由城池／書架／海圖，然後目前關卡直接原Four0→1，重整返回不重彈。另有終幕「進去看看」直接原Four0分支。
- 獨立Five入口重整仍同幕，終幕Escape等效X，不開書／書籤；稍後正常原Five0直入。
- 合法Four已完成28／receipt隔離fixture的4段尾聲逐幕reload精確，前3的Escape／nav／main／tools／地標都擋，末X至原城景通知，城池可進、再讀Five0，count仍1。這不是實際重讀29頁。
- Four0／Four2／Five0／all14四個歷史fixture，stale pending被清、原reading保持、不強插對話。Replay中段Escape／secondary及終幕X自由退出，reading／seen／pending／receipt的local/session原始值不變。
- 中間段Settings仍可開；reset在title前清pending，0本完成的靜態電車完整、再抵達從頭。原生檔案input還原legacy reading v1亦清pending，書籤2仍優先。
- 故意只讓pending local寫入失敗、session正常，notice可見，reload精確續疑幕，reading不改。獨立模型另驗未知／train／錯context拒絕、corrupt隔離、quota恢復context、clear tombstone與stale fallback拒絕。
- 代表尺寸360×800、844×390、1024×768；JS／同源HTTP錯誤0。18個changed/newJS語法、game產生器／SEO15、14HTML僅bridgecache、45原書JS/CSS/CSV、23核心/圖片/CSS、seen schema／台詞／IDs／graph、原圖ZIP／PNG與30成員Seven離線包保持通過。

| 畫面 | 截圖 |
| --- | --- |
| 抵達終幕，右上X與「進去看看」並存 | [360×800](arrival-terminal-x-360x800.png) |
| 首本尾幕X仍接原城景通知 | [1024×768](completion-terminal-x-1024x768.png) |
| Settings重置已清pending，仍能完整進電車 | [1024×768](reset-cleared-pending-train-1024x768.png) |

隔離瀏覽器資料，不改作者存檔；本輪只原生Four0–1及Five0，未重讀29頁／14本全稿。手機／平板是Chromium viewport/touch模擬，實機iPhone／iPad Safari未測。
