# 第一關HTML快取補修

2026-11-23，從PR69 merge `6d61aede9140746eea5927fe77f04c29c78204a9` 建立 `fix/game-doubt-reader-cache`。

正式四聖諦讀本回傳 `Cache-Control: max-age=600`。只更新HTML內的bridge script query，仍可能先拿到十分鐘內的舊HTML及舊bridge，導致閱讀完成後沒有新的presentation receipt。

本修正只加入版本查詢參數：

- 第一關主線入口：`collectionStory=doubt-2`，讓讀本HTML換快取鍵。
- 第一本文內bridge URL：`?v=doubt-reader-2`。
- collection bridge返回遊戲：`?v=doubt-2`，避免返回舊的game HTML。
- game來源與產生器的worldmap bootstrap：`?v=doubt-reader-2`。
- 地圖／城池／書架三個主入口互返統一帶 `v=doubt-2`；新shell、navigation、city／shelf bootstrap query同步，完成後replaceState也保留版本鍵。

閱讀資格、頁碼、故事、能力、完成紀錄和原正文均不改。作者可用 `/game/?author=1&v=doubt-2` 直接開啟本輪入口。新的key是資產版本，不提供跳關或帳號權限。

針對性測試用舊HTML／舊v1 bridge回應模擬快取，確認新入口含參數而取得新bridge，實際29步完成仍可進過場；原本的介面、法義及多尺寸證據仍見PR69與本目錄驗證，不再擴大重測未改內容。精確補修merge SHA及Pages／live紀錄以補修PR交付為準。
