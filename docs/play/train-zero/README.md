# 零本完成的電車啟動與對話按鈕

2026-11-25接續已發布PR86／main `dd480b67959e90adc50f2bb8e0c2b1f80197d8f2`。作者回報在設定清除進度後看不到電車；要求尚未完成一本時每次從首頁啟動都播放，進繪本前的中間對話用「接著看」、最後才「進去看看」。

## 重現原因

設定的清除原本只重置資料，留在活動海圖；同步journey-state事件立刻顯示arrival並又寫入已看紀錄。電車資格同時排除任何書籤／已看對話，因此清除後甚至回首頁也被阻擋。[驗證](../../previews/train-zero/README.md)保留原版的實際按鍵重現，並非推測存檔未清乾淨。

## 修正行為

- `canPlayTrainOpening`僅判定`completed.length===0`；有書籤、曾看過電車／抵達對話，都不阻擋從首頁重新播放。至少已完成一本則原本正常續程。
- 首頁開始／繼續都從電車第一段播兩段。只有中途載入`#opening`且首段已看、末段未看，才續第二段；完整看過後新一次啟動仍從頭播。既有story flags/schema保持。
- Settings清除成功返回主選單；reset事件只關閉舊對話／更新地圖，不預先顯示或標記抵達對話。電車結束後才出現第一次抵達。作者首頁重置仍使用原prologue流程。若清除無法永久保存，保留當頁暫存及既有提示，不強制換頁丟失記憶體恢復。
- 海圖／城池／書架／讀本回程仍沿用既有`#map/#city/#shelf`規則，不在遊戲中往返時反覆插片。播放電車不重置頁碼、不改完成紀錄或閱讀資格。
- 共有後續scene的中間段強制「接著看」；真正以enter-first-book／enter-aggregates-book進書的末段「進去看看」。首次抵達三段因此是接著看→接著看→進去看看。四聖諦完成context的末段仍「接著看」至城景通知，因為該步尚未直接進下一本；唯讀重播末段「回到海圖」。所有敘事文字、ID、圖與原經均不改。

active runtime快取改`train-reset-1`，維持同一story/reset單例；中央reading store／route policy URI、備份與schema保持。十四本HTML僅更新bridge query，game產生器同步；原插畫、共享reader CSS／JS、1192步及合法歷史完成／書籤保持。Pages保留legacy main:/，本輪QA目錄排除，共30處。實際測試與代表截圖見[驗證報告](../../previews/train-zero/README.md)；精確PR／merge SHA／Pages／live發布證據以本輪PR為準，實機iPhone／iPad Safari未測。
