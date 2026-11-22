# 小貓的山海旅程：沉浸介面與依序閱讀驗證

本目錄保存本機驗證證據；正式發布結果另記新 PR 的精確 merge SHA、Pages 與 live 交付留言。由 repository 根目錄執行：

```sh
python3 -m http.server 8000
```

開啟 <http://localhost:8000/game/>。全套獨立 UI 檢查可用 `python3 -B scripts/check-game-immersion.py` 重跑；檢查使用獨立瀏覽器資料，不會讀取作者的瀏覽器存檔。

[實際驗證報告](validation.json) 包含：

- 原生按鍵逐步讀完四聖諦 29 個閱讀步驟；中途重整、橫直切換、返回地圖再續讀。抵達末頁不計完成，按「完成這本」才增加本數。
- 完成回饋的「前往下一站」留在海圖並定位五陰，沒有自動開書；完整複習不再次計數或重播獎勵。
- 地圖、書架、城池六組複習入口：完成書停在末頁時從第 1 步重讀；部分書籤續原步，重整與下一頁正常，主線與本數保留。
- 未開放六處／四禪的舊 collection URL 與新返回參數都受限制；原網站無 collection 的兩本仍可正常按下一頁，不寫入遊戲紀錄。
- 未來書籤、非依序的歷史完成、歷史終章完成、前十三本完成及全部完成等隔離存檔情境；書架只提供已完成書的複習入口。
- 五個尺寸的地圖拖曳防誤開、放大、全圖、目前關卡、相同圖層變換、跨分頁／重整相機保留，以及尺寸切換。另以 Chromium CDP 模擬雙指縮放與取消，沒有觸發誤開或整頁縮放。
- 設定的備份／還原、取消清除、無效備份保留、清除僅影響本遊戲，以及儲存損壞／不可用仍可閱讀。
- 歷史美術比較頁及獨立城池 inspection 的實際零 Storage 觸碰與無遊戲讀本操作。
- 對照 `7e39f04a383ab98d3b747365ea3e513ad7140a0e`，615 個受保護檔案逐位元未改：十四本正文、口白、經文、圖片、原 HTML、根首頁／SEO／Google 驗證與相關產生程序。

封面採作者後補的原始 JPEG，SHA-256 為 `fc7cb28c894890127a20fd1bb898d2448950d51be86c3b36200faa6c2ae523e9`，原圖 2752 × 1536。已用實際載入的原檔重拍以下五尺寸；開始前沒有下載十四本繪本圖片。

| 畫面 | 桌機 | 手機直式 | 手機橫式 | 平板直式 | 平板橫式 |
| --- | --- | --- | --- | --- | --- |
| 開始畫面 | [1280×900](title-1280x900.png) | [360×800](title-360x800.png) | [844×390](title-844x390.png) | [768×1024](title-768x1024.png) | [1024×768](title-1024x768.png) |
| 目前關卡 | [1280×900](map-current-1280x900.png) | [360×800](map-current-360x800.png) | [844×390](map-current-844x390.png) | [768×1024](map-current-768x1024.png) | [1024×768](map-current-1024x768.png) |
| 全圖 | [1280×900](map-overview-1280x900.png) | [360×800](map-overview-360x800.png) | [844×390](map-overview-844x390.png) | [768×1024](map-overview-768x1024.png) | [1024×768](map-overview-1024x768.png) |
| 城池初始 | [1280×900](city-1280x900.png) | [360×800](city-360x800.png) | [844×390](city-844x390.png) | [768×1024](city-768x1024.png) | [1024×768](city-1024x768.png) |
| 空書架 | [1280×900](shelf-empty-1280x900.png) | [360×800](shelf-empty-360x800.png) | [844×390](shelf-empty-844x390.png) | [768×1024](shelf-empty-768x1024.png) | [1024×768](shelf-empty-1024x768.png) |

完整原生流程的 [閱讀畫面](reader-768x1024.png)、[第一次完成回饋](completion-first-book-1024x768.png)、[定位下一站](map-next-station-1024x768.png) 與 [只完成一本的書架](shelf-one-completed-1024x768.png)。

另附專項檢查的 [全完成城池](city-all-completed-fixture-390x844.png) 及 [全完成書架](shelf-all-completed-fixture-390x844.png)。這兩張使用明確隔離的歷史存檔測試資料，供觀察完整外觀；不代表測試者本輪原生讀完十四本，也沒有改動真實使用者紀錄。

本輪未測實機 Safari；手機、平板與手勢均為桌面 Chromium 模擬。先前 1192 步原繪本測試維持原報告，不以舊版自由選章驗收取代本輪的依序閱讀規則。新畫面與相機仍需作者在實機檢查舒適度。

專項原始結果：[資格模型](eligibility-model.json)、[儲存備援模型](storage-recovery-model.json)、[讀本橋接與越關](reader-policy.json)、[16384 子集與獎勵](route-rewards-model.json)、[鏡頭契約](camera-contract.json)、[獨立殼與歷史審稿隔離](independent-shell-gallery-validation.json)。這些報告保存實際檢查範圍，不將模擬完成資料寫成原生讀完紀錄。
