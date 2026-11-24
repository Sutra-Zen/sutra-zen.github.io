# 十二因緣手機譬喻：核可旁白校訂

基準：3d0699a9958908cae0e667014e3bf4bb65466f79。作者核准移除第44–45頁不一致的名色／識括號，採下列完整旁白。範圍僅兩頁白話文案，不延伸修訂其他未核可項目。

## 核可後文案

第44頁：

> 這就像你在滑手機：依著眼睛與畫面，生起看見的識。
> 看見有趣的內容，心裡感到愉快，也生起繼續看的念頭。

第45頁：

> 這個念頭帶動手指往下滑，又看見了下一則內容。
> 就像小猴子換著抓樹枝，我們的心也在不同的經驗間不斷轉變。

## 校訂前文案封存

第44頁原文：

> 這就像你在滑手機：眼睛看到一張圖片（名色），心裡覺得「真有趣」（識）
> 前一刻的名色行為產生了前一刻的識。

第45頁原文：

> 這個念頭推動手指往下滑（新的名色），又讓你看到了下一則內容（新的識）
> 我們的心就是這樣，抓著一個體驗，搖過下一個體驗。

原始全文亦可由上述基準commit還原；不把新的白話句子宣稱為原影片逐字字幕。原時間定位值保留，不宣稱本輪精聽或改製音軌。

## 實際來源與同步

- twelve-links/book/book-data.js的BOOK.pages[43].lines、BOOK.pages[44].lines是閱讀器直接顯示的第44／45頁。
- 同檔BOOK.scenes[10].subtitles[4–7].text是同場維護資料，本輪同步四句，start／end不改。
- twelve-links/storyboard.csv第44、45筆的字幕欄同步同文；UTF-8 BOM、原欄序、引用格式及其他cell保留，未整檔重排。
- scripts/下沒有引用十二因緣／此CSV的build或generate腳本。本次直接維護已存在的資料來源，沒有新增虛構產生器。

## 保留內容

第44與45頁的289經原文、經號、來源、圖片與遮罩保持原值：

> 彼心、意、識日夜時刻，須臾轉變，異生、異滅。猶如獼猴遊林樹間，須臾處處，攀捉枝條，放一取一。彼心、意、識亦復如是，異生、異滅。

- 第44頁圖片：../assets/scene-11-right-dark.webp；mask保持空字串。
- 第45頁圖片：../assets/scene-11.webp；mask保持left。
- 兩頁均number=289，來源由原reader映射../#sa289；source映射程式不改。
- 18筆scenes、19個含後記的選章、77個閱讀步驟、原頁碼與書籤索引不改；其餘旁白、時碼、標牌、插畫及引文完全不改。

本幕保留心意識如獼猴攀枝般轉變的生活譬喻；不再用圖片＝名色、有趣＝識的括號，也不再聲稱前一念名色製造前一念識。289經原文不是本輪改寫對象。

原經入口：https://suttacentral.net/sa289/lzh/taisho
固定官方原檔：https://raw.githubusercontent.com/suttacentral/sc-data/a5758387a32a950671780bc213aa2d4debbe1362/html_text/lzh/sutta/sa/sa201-300/sa289.html

## 精確資料差異

- book-data.js只變更8個字串值：4個scenes字幕text＋兩頁各2條lines；全部其他JSON值與JSON之外bytes相同。
- CSV只變更(44,字幕)與(45,字幕)兩個cell，其餘cell及原排序相同。
- 原book-data.js SHA-256：0c240707d54397261d1329496b585f727caf99b0daaac03e71c32408340901ca
- 原storyboard.csv SHA-256：26b05bd1aa8ccd4a5f0f3967c9f57de8fc48cc66a1669507af662fe4263ee269
- node --check及git diff --check由本輪驗證執行；實際瀏覽器結果隨交付紀錄補記。
- 該書HTML僅更新資料載入快取為 `twelve-phone-1`；共享閱讀器、guide與遊戲規則不改。六尺寸及三種模式的實際驗證與截圖見[驗證紀錄](../../previews/twelve-phone/README.md)，精確發布狀態以PR交付留言為準。
