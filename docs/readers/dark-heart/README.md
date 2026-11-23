# 心經置中與統一深色口白

2026-11-24，分支 `fix/reader-dark-heart-center`，由已發布 PR79 `47e4b6ef5c7f51c9aba4766c6bc25eaa790cc239` 建立。起始乾淨、origin 與最新 main 已核對。沿用作者持續發布授權，經 PR、精確 SHA 的 Pages 與正式站確認後交付。

心經的標題與直書原經作為同一字群，實際內容寬度放得下時，在既有圖框內左右置中。框較窄、內容需橫向捲動時，保留原本由最右邊開始的排列，仍可向左捲讀全文。這與作者追加的小版面要求一致，不縮字、不裁原經，不改原有金字、紅色重點、直書方向、圖框高度或上方口白位置。

實作保留原 DOM 與原閱讀器的標題搬移方式。共用 CSS 把心經 `.verse-body` 設為 RTL flex，標題及 `#verse` 不伸展／縮小。`reader-layout.js` 按子元素實際寬度及左右 margin 判斷是否加入 `.reader-heart-fits`；fit 用 center，overflow 用 RTL flex-start。原生 `#verse` 的 flex:1 需以 ID 等級覆蓋，否則會產生滿版空盒而造成「盒子置中、字仍靠右」；本輪以元素與實際 glyph Range 同時驗證。

十四本公開閱讀與遊戲模式使用相同 `reader-controls.css`，上方 `#caption`、`#reader-summary-caption` 統一為不透明 `#1e1e1e` 深底、`#fffdf8` 淺色字。文字結語的底色也相同；原總結標題的可讀金色可保留。原本的淺色來源包括十二因緣預設樣式、四向四果 S01／S10，以及四不壞淨的黑字字幕設定；作者原稿和 storyboard metadata 不改，只覆蓋呈現。圖內疊字、圖片烙字、經文卡、心經原字色及重點不套用此規則。

本次只改共用 CSS／版面 JS、必要載入快取、交接與驗證。讀本各自的 JS／CSS、口白、經文、圖片、聚焦資料、閱讀資格、完成及存檔格式維持。快取版本 `dark-heart-1` 讓原站、遊戲、城池與書架的閱讀回程一致；入口既有 `entry-no-frame-1` 的無白框效果保留。`game/index.html` 仍由共用 shell 產生，Pages 維持 legacy main:/，QA 排除目錄增加為25處。

七覺支離線 ZIP 與 manifest 依最終共用檔重建，30 個成員，原插圖／書稿／書本程式不改。可在根目錄執行 `python3 -m http.server 8000`，由 `http://localhost:8000/game/?v=dark-heart-1` 或原公開讀本網址檢查。

詳 [本輪驗證與截圖](../../previews/reader-dark-heart/README.md)。實測會區分公開與隔離遊戲 fixture、原生翻頁與代表頁量測；不宣稱重讀全部1192步。手機／平板尺寸為 Chromium 模擬，未測實機 Safari。正式發布的 SHA／Pages 與 live 結果以 PR 交付留言為準。
