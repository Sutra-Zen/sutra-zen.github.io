# 後四本口白／出處內容稽核

基準 `a238a0fb549966ac0510b5b89f18b913c8ec40b6`。唯讀審查，未修改repo。

41幕、321段作者口白、49筆不同引文全部審讀；口白逐段與作者JSON一致。沒有發現錯經號、跨幕錯配或最近介面修改導致的內容誤植。

| 繪本 | 幕 | 原口白 | 目前閱讀步驟 | 不同引文 |
|---|---:|---:|---:|---:|
| 四如意足 | 9 | 81 | 82 | 11 |
| 四禪 | 10 | 130 | 131 | 8 |
| 五根五力 | 10 | 74 | 75 | 14 |
| 七覺支 | 12 | 36 | 37 | 16 |

## 三項原稿既有的引文標示／錄文差異

### final4-01 MN10摘要沒有在閱讀卡上標成摘要

七覺支，頁 31,32,33,34,35,36，Q16。

現字：有念覺支時，了知有念覺支；沒有時，了知沒有。了知未生起的覺支如何生起，以及已生起的覺支如何修習圓滿。
原典：當自己有念覺支時，了知：『我有念覺支。』當自己沒有念覺支時，了知：『我沒有念覺支。』如其未生起念覺支之生起而了知，如其已生起念覺支之圓滿修習而了知；

經號及「知有無／令生／圓滿」教義配對正確。引文是把原段縮寫並泛稱覺支的影片中文摘要，並非所核莊春江逐字原文；卡片現只有經名和blockquote，讀者可能當作原經逐字。不是CSS或翻頁配錯。

建議：保留作者摘要，卡片明標「內容摘要／意譯」，另供既有完整莊譯原段；不默改口白。
位置：seven-factors/book/book-data.js:1102；作者稿 docs/seven-factors/storyboard.md:233；既有待校說明 docs/seven-factors/REVIEW.md:9。
來源：https://suttacentral.net/mn10/zh/zhuang；官方原檔：https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/zh/pli/sutta/mn/mn10.html

### final4-02 SN48.43影片譯句與所核莊譯不同，須分版本

五根五力，頁 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,66,67,68,69,70，Q01。

現字：沙洲之前的水流與沙洲之後的水流……信根者，可謂信力；信力者，可謂信根。精進根者，可謂精進力。
原典：［分］該島東邊的水與該島西邊的水……凡信根者，是信力；凡信力者，是信根，凡活力根者，是活力之力。

經號/河島譬喻/五根五力同法的意旨都吻合，無前後章串錯。詞句承作者影片錄文，未署現代譯者，與導讀標明莊春江的完整節錄不同，不能宣稱逐字等於莊譯。

建議：卡片註「影片摘錄／譯者待確認」，或經作者決定後統一採具名譯本；不把這列成錯誤經號。
位置：five-roots-powers/book/book-data.js:225；作者稿 docs/five-roots-powers/storyboard.md:41；既有待校說明 docs/five-roots-powers/REVIEW.md:11。
來源：https://suttacentral.net/sn48.43/zh/zhuang；官方原檔：https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/zh/pli/sutta/sn/sn48/sn48.43.html

### final4-03 675經錄文多一個「是」

五根五力，頁 66,67,68,69,70，Q13。

現字：念力者，當知是四念處。
原典：念力者，當知四念處。

經號和法義正確；大正藏該句無「是」，目前影片錄文多一「是」，不可稱逐字完全相同。作者原稿已如此，不是新UI漏植。

建議：若採逐字古漢譯，經作者核可刪「是」；若保留影片，明標錄文／整理。
位置：five-roots-powers/book/book-data.js:2110；作者稿 docs/five-roots-powers/storyboard.md:306；既有待校說明 docs/five-roots-powers/REVIEW.md:12。
來源：https://suttacentral.net/sa675/lzh/taisho；官方原檔：https://raw.githubusercontent.com/suttacentral/sc-data/c7bba0f184e66904949d4918587975fb7fd7ec69/html_text/lzh/sutta/sa/sa601-700/sa675.html

## 已排除的誤判

- 四如意足：鐵球心理轉化、掃描身體、心理防備、公園／渡船是原影片白話譬喻，已有translationNote與SOURCE_NOTES區分原經，不是誤換經文。SN51.20上下原釋含身體不淨、光明心含光明想，不應把故事說成原經逐字；此界線已保留。
- 四如意足：Q09 runtime已改為具名莊春江SN51.11原句，與官方檔精確相合；舊scripture-catalog仍保存影片原錄文，不能反向把正確runtime當誤植。
- 四禪：SA483卡字序與原經相同，但作者斷句「不苦不樂，捨淨念、一心」與大正藏「不苦不樂捨，淨念一心」不同，既有REVIEW已記，屬斷句/版本呈現，非經號錯配。
- 四禪：前五幕依作者只標DN2主題，沒有完整Q卡；各主題確實可在DN2找到，非漏配或別本經文。
- 七覺支：S11總說大小火前段保持原影片當時微劣心Q13；P029起切掉心Q14，P030切念兼助Q15。對齊原稿時間，不是前幕殘留。

## 證據與限制

重抓22份官方漢譯／莊譯／巴利全文，均符合封存SHA；receipt：`/tmp/sutra-final4-sources/download-results.json`。機器可讀逐Q／頁碼矩陣：`/tmp/sutra-audit-final4.json`。

- 非音軌逐字聽校；審查依作者交接文字與現行閱讀資料。
- Buddhaspace首頁/675註解頁及莊春江讀經站SN51.13受網路CONNECT403；已重抓SuttaCentral官方固定版本22份漢譯/莊譯/巴利全文，hash全部符合封存，未將403當成無經。
- 本子任務是內容與來源審查；root另做實際DOM顯示及頁碼配對驗證。
