# 深色半透明介面與「疑」的首次過場

2026-11-23（Asia/Taipei），分支 `feat/game-doubt-dialogue-theme` 從已發布main `44dce2f6624e568ff83d6cf79e675fe61a53c325` 建立。起始乾淨、origin仍為Sutra-Zen/sutra-zen.github.io。本輪作者明確授權更新與發布；精確merge SHA、Pages及正式站結果記本輪PR交付，不以本機截圖代替發布證據。

## 介面與素材

`play/game-theme.css` 是固定啟用的深藍／炭色半透明介面，不另設夜間切換。標題紙卡、對話、工具／設定／來源／完成面板及底列有實際alpha，暖白文字、暖金標示與綠色主要操作；地圖、城池與書封原圖不加整層灰階、透明度或暗幕。各遊戲入口及shared shell將主題載在既有CSS之後。

小貓肖像取消圓形overflow裁切，改矩形透明容器、內距與contain，保留完整雙耳。沒有重畫小貓或修改原繪本。

「五蓋眾・疑」為依作者參考圖新生成的透明暫用概念稿，原生1254×1254。角色出自安那般那S03／四禪S05同構圖右側的藍灰雲絨生物；來源與hash見 [素材紀錄](../../../play/story/assets/DOUBT.md)。新PNG沒有嵌字或問號，對話與世界中的金色問號均由網頁呈現，方便日後替換文字或演出。

## 作者文案與短流程

故事稿和原經、繪本口白分開，集中在 `play/story/data.js`。新玩家維持原抵達台詞，接著：

1. 五蓋眾・疑只說「愚痴……」。
2. 小貓：「這隻滿身問號的生物是什麼啊？竟然擋在入口……我先繞過牠，進去看看好了。」
3. 按「開始閱讀四聖諦」進入原29步完整繪本。
4. 真正按末頁完成後，小貓對苦與離苦的路更清楚，提到繼續練習「正智」與「慧根／慧力」。
5. 問號從七個漸減為兩個，疑退進局部薄霧；再顯示既有法輪碼頭回饋與下一站五陰。

文案依作者允許作短句修整，以理解與練習方向表達成長，不另增能力分數、修證判定或提前完成五根五力。疑的台詞是故事角色發言，不把「疑＝愚痴」當成經義定義；退場是本次閱讀場景演出，不宣稱讀一本書已斷五蓋或取得果位。

世界演出由 `play/story/doubt-stage.js/css` 負責：和原海圖共用1600×900座標與鏡頭，位於法輪入口旁，點擊穿透、不擋標牌；等待／變少／退場狀態只由故事控制器決定，本身不寫進度或推關。降低動態模式改直接呈現較少問號／隱去，不強制等待動畫。有角色演出的短對話暫時避讓上方對話框，讓疑位於對話框與底列之間；收起後恢復原鏡頭可用範圍，鏡頭演算法與原圖未改。對話可略過；明確略過完成過場後不在下次返回強制重播。

## 真實完成事件與儲存邊界

完成過場不只看 `?completed=four-truths`。既有 `play/collection/reader-bridge.js` 僅在資格及末頁檢查通過、既有store.complete真正成功的mainline分支，發出presentation receipt：

`sutrazen.play.story-first-completion.v1`

receipt只存版本與事件名稱，不存另一份已讀集合／頁碼／能力。海圖消耗receipt，再核對真實完成集合、末頁位置與已看過疑的開場；歷史完成紀錄、偽URL、原站自由閱讀、重讀或僅選到末頁而未按完成，不會因此製造新完成。

若完成過場中途重整，已顯示的第一句與尚未顯示的末句可接續；尾段已顯示或明確略過即不再自動重播。歷史已有第一本位置者直接續讀，不插入新的強制入場。工具保留「重看開場對話」，並為已完成四聖諦者提供「重看四聖諦過場」；手動重看不寫seen、receipt或已讀紀錄，也不更改主線。

現有 `sutrazen.play.story.v1` 版本與seenSceneIds仍相容原arrival ID。作者 `/game/?author=1` 的重置連同receipt清除，普通入口不增加試玩重置鈕；舊的儲存失敗／備援處理保留。兩種Storage皆不可用時仍保留閱讀操作，過場回傳可能不能保存，完成回饋仍沿用原流程；不假稱已永久保存。

## 必要的小幅讀本調整

十四本正文、口白、經文、圖片、一般讀本JS／CSS不動。四聖諦 `book/index.html` 僅把既有collection bridge的script URL改為 `?v=doubt-reader-2`，避免舊快取漏掉完成receipt。首次主線的讀本網址另帶 `collectionStory=doubt-2`，返回遊戲帶 `v=doubt-2`，讓HTML快取也換鍵；詳[快取補修](CACHE-FOLLOWUP.md)。bridge只新增可降級的receipt helper載入與成功後一行通知；讀本階段該helper載入失敗仍可照常閱讀／完成並回原回饋，不改資格、完成寫入或原頁碼流程；獨立開原書時module仍不啟動遊戲模式。

`play/collection/store.js`、解鎖資格、十四本順序、地圖拓樸、原鏡頭與序幕原稿保留。主題與故事依賴的版本同步，storyStore在海圖、對話與作者重置共用同一module instance。

## 驗證與試玩

根目錄執行 `python3 -m http.server 8780 --bind 127.0.0.1`，開啟 `http://127.0.0.1:8780/game/?author=1`，可略過片頭並重置從頭試看。

```sh
python3 -B scripts/build-game-entry.py --check
python3 -B scripts/build-seo.py --check
python3 -B scripts/check-game-doubt-story.py
```

實際截圖與結果見[本輪驗證](../../previews/game-doubt-story/README.md)。615原站保護檔中只允許四聖諦HTML單一快取tag差異；normalize該tag後全文相同，其他原檔逐位元不變。本輪走第一本29步及相關重讀／續讀／歷史／失敗情境，未宣稱重走十四本1192步。手機／平板為Chromium模擬，實機Safari未測。

Pages仍使用legacy main:/；QA排除新增本輪，共十六目錄。素材尚待作者確認的細節為新疑角色正式獨立稿；其他五蓋、波旬與後續劇情未擅自新增。Notion無可用連接器，待補本輪PR、精確SHA、Pages run及固定SHA ZIP。
