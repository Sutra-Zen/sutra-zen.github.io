# 五陰已核可的引文配對校訂

基準：a238a0fb549966ac0510b5b89f18b913c8ec40b6。範圍限作者核可的第7–9頁來源及第43頁下方引文；頁碼、上方口白、圖片、聚焦、操作與其他經文不改。

## 第7–9頁：四大與四大造色

- 原來源：../#sa46。
- 新來源：../#sa41。
- 第7頁引文保留「云何色如實知？」。
- 第8–9頁引文保留「諸所有色，一切四大及四大造色，是名色，如是色如實知。」。
- 五陰導讀新增第41經〈五轉〉來源卡，顯示同段原文、古漢譯版本／求那跋陀羅譯、中文原經及註解入口。既有第46經全文保持原樣。

第41經官方原檔：
https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa41.html

SHA-256：b4185cd91b4f30421f438529fc1826a9cfe8e5b03fb30930191772b475f9ad11

所核版本為SuttaCentral所收CBETA大正藏T02、No.99；原檔footer明載Guṇabhadra／求那跋陀羅、宋譯。去除網頁大正藏行碼後，新增來源卡的完整節錄可在原檔連續找到。

## 第43頁：未來識句

原下方引文（保留作追溯，不再公開顯示）：

    多聞聖弟子於此受……想……行……識受陰作如是學：『我今現在為現在識所食，
    於過去世已曾為識所食，如今現在；

作者核可的新下方引文：

    我今已為現在識所食，若復樂著未來識者，亦當復為彼識所食，如今現在。

上方口白仍是：

    我現在被識所束縛，如果我繼續貪愛未來的識，
    將來也會被識所束縛，就像現在一樣。

來源仍為第46經。官方原檔：
https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa1-100/sa46.html

SHA-256：bb952b4ba160a5973d0894546f7833723e48cbe5f650a164a4b56f0c0c902f8a

新句在原檔的識三世執取段連續存在，與既有五陰導讀第46經全文也相同；沒有修改該全文。

## 實際資料來源與維護方式

- 執行時直接讀取five-aggregates/book/index.html內的inline scenes；其原生頁面陣列按scenes[].pages展開。
- five-aggregates/storyboard.csv是同庫維護分鏡表，本次只改第7、8、9筆的經文連結及第43筆的經文cell。保留UTF-8 BOM、既有欄序、記錄順序、CSV引號及其他cell。
- 檢查scripts/內的build／generate及storyboard引用後，沒有會重建五陰inline scenes／本導讀的建置器；不要套用其他主題的build-five-roots-powers.py。
- 來源與CSV原錯標／重複句已完整保存在本紀錄及基準commit；不回寫其他未核可作者詮釋，也不帶入獨立稽核PR或五城試作。

## 驗證

- inline scenes逐cell差異僅(第7頁source、第8頁source、第9頁source、第43頁verse)四項，全部口白相同，16幕／54頁不變。
- CSV逐cell差異也僅上述四項，未整檔重排。
- 導讀原有位元在移除新增SA41卡後完全相同；第46經article與整個head保持相同，沒有改SEO、canonical或其他來源卡。
- 新來源卡節錄及第43頁新句均在固定版本原經中連續匹配。
- python3 -B scripts/build-seo.py --check：15頁head、sitemap、robots及Google驗證檔通過。

外站註解入口沿用既有公開單經路由。原典內容校核使用上述官方固定版本；先前直接Buddhaspace讀取受CONNECT403限制，不把官方資料核對冒稱外站畫面驗收。

Focused Chromium驗證通過360×800、844×390、768×1024：原生Next第6→7→8→9頁皆指SA41，原生來源操作進入新卡並返回第9頁；第42→43頁顯示作者完整新句，橫式本頁經文對話同句；來源卡版本／譯者、兩個按鈕及完整節錄可讀，無水平溢出，0 JavaScript／同源HTTP錯誤。這是指定位置的內容／動線驗證，不冒稱重新讀完54頁；實機Safari未測。
