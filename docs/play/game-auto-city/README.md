# 自動新增城景與精簡城池

2026-11-23，基準 main `1ba30cfb016ed6affaefe1a62ee6ae9d1678efd9`，分支 `feat/game-auto-city`，起始乾淨、origin為Sutra-Zen/sutra-zen.github.io。依作者最新決定取代手動安置：模組拆分保留，完成閱讀後自動顯現，延續本輪網站修正與發布授權。

## 玩家流程

原繪本末頁明確「完成這本」仍是唯一過關入口。四聖諦完整尾聲（心得、疑退場、波旬、五陰湖）先結束，再出現原完成通知框：**城池已自動新增「法輪碼頭」，快到城池看看新的變化吧！** 提供「前往城池看看」與「前往下一站」，不強迫進城。

城池不再要求拖卡片／按＋／安置或自動安置。原14組圖像模組仍各自顯示與動畫；已讀玩家直接得到對應城景，不必重讀。模組原先的來源讀本與前置城景條件仍保留，歷史非依序已讀不補出未讀內容。第一本後已有四大花園、識城主及法輪碼頭，第三本後六門出現，第七本四念處的念守門人仍依原條件出現。

上方整排選項、下方安置清單／計數與下一站說明大區塊移除。繼續閱讀移到共用底部選單，城景滿視窗，底列覆在背景上。只留草地右上角全景圖示；進全景後，左上「返回城池」恢復進全景前的鏡頭。舊鏡頭若沒有返回快照則回四大花園。拖曳、雙指縮放及旋轉沿用原相機，不強制方向、不加全站手勢禁令。

點城主、波旬、五蓋、念守門人、止觀使者及六位覺支夥伴看各自對話；姓名不加「心想」，沒有換人／繼續佈置按鈕，右上X或Escape關閉。進城不自動開對話。六位夥伴短句是遊戲創作，與原經、原繪本口白分開，不當成原經或修證認證。

點景物看原有出處與相關已讀本複習，來源視窗同樣用右上X關閉。SN35.245 六門版與SA1175平行差異維持；場景延伸的來源連結標為「查看相關繪本出處」。四大花園點擊層在透明城界之上、其他建築與角色之下，避免後續城牆把廣場來源擋住。全景標牌隨圖縮小，回探索恢復可讀字級。

## 保存與相容

- `deriveCityModules` 只依合法completed及原requiredBookIds/requires推導 `placedIds`／`visible`；這些欄位現在表示自動顯現，`displayMode:'automatic'`。`get`零寫入／零事件，閱讀完成、書籤、資格不變。
- 原city v1的 `placedIds`／`thoughtSeenIds` 備份形狀保留；`savedPlacedIds`只作舊資料metadata，不決定畫面。舊空／部分／錯序配置不會遮掉已讀城景，也不能造未讀城景。
- 舊 `place`／`placeAll` API保留為無寫入相容介面，玩家端不再呼叫；`canPlace:false`。只有點角色可保存對話呈現紀錄，不因進城或動畫新增紀錄。
- v2旅程備份與v1閱讀備份仍可還原；還原閱讀即可重建城景，不依賴舊安置清單。整個旅程reset清閱讀後才回空草地；單獨清城中紀錄不抹掉已讀城景。禁用或損壞city儲存不影響依completed顯示城景。
- 點夥伴的6個呈現ID加入原合法集合，未改v1形狀，既有備份仍接受。沒有帳號、雲端、service worker或新增儲存命名空間。

## 修改範圍與驗證

主要檔案為 `play/city/city.js/css`、`thoughts.js/css`、`modules/store.js/scene.js/css/catalog.js/text.js`，以及完成通知、集中UI文字、入口cache。所有新字使用HTML／集中字典；未重畫或裁改原圖片。

`auto-city-1` 統一城池store/catalog/text/scene/thoughts與各共用import；collection與story的原單例URL保持不變。十四本HTML只改bridge query，回程與導覽同步，來源 `play/worldmap-v4/index.html` 生成game入口。原首頁／32心智圖／14書架、書本文字／經文／圖片／閱讀操作、SEO15／sitemap／robots／Google檔不改。Pages仍legacy main:/，本輪QA僅增排除目錄，合計21個。

最新檢查請使用 `python3 -B scripts/check-game-auto-city.py`；早期手動安置腳本及報告保留為對應舊版歷史。實際流程、合成歷史存檔、五尺寸及最後針對性回歸分開見[本輪驗證與截圖](../../previews/game-auto-city/README.md)。實機iPhone／iPad Safari未測。

本機：根目錄 `python3 -m http.server 8765 --bind 127.0.0.1` 後開 `http://127.0.0.1:8765/game/?v=auto-city-1`。精確merge SHA、Pages與正式站驗收記在本輪PR，不由本文件推定已發布。
