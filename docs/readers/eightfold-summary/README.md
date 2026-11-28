# 八正道總結頁合併（2026-11-28）

作者要求原第109、110頁合成一頁：移除各頁上方重複的四句偈頌，保留一份總結表，在下方經典區列出完整八句。原先兩頁下方已各有完整《雜阿含經》771經〈彼岸〉節錄，因此不改原經字句、標點、來源或原表六列。

`docs/eightfold-path/reader-edits.json`記錄展示合併，`scripts/build-eightfold-path.py`仍先驗證原13場110段及11幅原圖，再合併scene13兩段並加原後記。原handoff／storyboard／verified-sources不改；runtime共110頁，前108頁逐物件相同，109為合併總結，110為原後記。renderer只在空白口白時隱藏caption。共用版面、已核可「由戒生定」、原字幕／原經／原圖及其他十三本維持。

## 書籤與備份

以下皆為零起算書位：舊108與109皆對應新108，舊110對應新109。其餘書位、既有非順序完成紀錄及activeBook保持；不把越界值夾到末頁，也不放寬下一關資格。抵達後記仍須明確按「完成這本」。

- collection key與`version:1`保持；`positionsRevision:2`區分新書位。缺標記的舊輸入才遷移，經同一個純validator處理local、session recovery、storage event及兩種備份，輸出必帶標記，避免匯出／還原或重整再次位移。外層journey backup仍version2。
- 八正道新遊戲reader URL帶`collectionPageVersion=2`。未帶版本的歷史`collectionPage`先遷移；移除一次性書位query後保留版本。公開讀本的原生session key改`.v2`，只在新key不存在時讀舊key並遷移。
- 八正道bridge在保存／完成前核對110頁；若混載舊111頁cache，保留原query僅refresh一次，仍不一致時顯示重載／回程提示，停止寫入與完成。
- 所有遊戲相對module imports、入口及十四本bridge統一`summary-merge-1`，維持同一套store／catalog／政策模組實例。舊版已開分頁若將選用標記剝除，新版會保守回到總結而保留完成紀錄；不以新schema令舊客戶端誤判壞檔。
- 真兩分頁故障測試發現既有storage event在session拒刪、仍可寫入時可能於外部分頁reset後復活舊fallback。最小修復沿reset模式，拒刪時用當下state/baseRaw覆寫recovery並保留unavailable提示；不合併完成集合。兩種儲存皆拒寫時仍只有當頁記憶狀態可用。

## 驗證範圍

focused UI六個public／review／順序主線代表，360×800、844×390、2048×1113，核對原表、完整八句可達、頂部無重複、原生109→110、書籤重整與末頁明確完成。獨立真store測試21例涵蓋遷移、備份、reset、quota recovery、雙分頁事件、鎖關及完成；另有上述拒刪故障before／after。混載111頁專項核對有界refresh及禁止寫入。未宣稱重讀全部十四本，實機iPhone／iPad Safari未測。精確Pages與正式站驗證以本輪PR交付紀錄為準。
