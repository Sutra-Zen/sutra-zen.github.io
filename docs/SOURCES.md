# 原經與註解查找備忘

## 台大獅子吼：四阿含

由總入口主動查找各部、卷次與經名，不限於雜阿含。未搜尋到或收到環境 403，不代表沒有來源。

- 總入口：https://buddhaspace.org/main/modules/dokuwiki/
- 增壹阿含〈四諦品第二十五〉：https://buddhaspace.org/agama1/25.html
- 中阿含第30經〈象跡喻經〉：使用者提供的完整段落 URL 已保存在 four-truths/index.html 的 ma30 卡片；此為 agama2/7.html 的特定段落，不以雜阿含編號路徑猜測。

## SN 22.48：中文優先與對照

- 中文入口：https://suttacentral.net/sn22.48/zh/zhuang （莊春江譯）
- 已實際讀取的出版方資料：https://github.com/suttacentral/sc-data/blob/main/html_text/zh/pli/sutta/sn/sn22/sn22.48.html
- 文件明載 author=莊春江、相應部22相應48經及「蘊經」，可核對五蘊、五取蘊的定義。
- 已實際讀取的巴利原文：https://github.com/suttacentral/bilara-data/blob/published/root/pli/ms/sutta/sn/sn22/sn22.48_root-pli-ms.json
- 中譯摘錄採原文兩段「比丘們！凡任何色…」；巴利對照採 sn22.48:1.5 與 sn22.48:2.2，不自行改寫引文。

2026-11-14 的直接服務站請求遭環境 403；GitHub 出版資料讀取成功。以上中文來源內容已核對，服務站實際頁面呈現、定位及真實 iPad/Safari 仍需獨立驗證。

## 八正道與十善業道

- 主軸：雜阿含784；另核對241、748、749、771、777、785、1039，以及中阿含16、42、189、200。
- 典籍資料固定版本：SuttaCentral `sc-data` commit `14085ec66e6d2ad0f45565a32c614c35e037ec07`。12份原檔均已讀取並在固定 commit 重新驗證雜湊。
- 路徑：`html_text/lzh/sutta/sa/sa701-800/sa784.html` 等分組；中阿含為 `html_text/lzh/sutta/ma/ma42.html` 等。詳見 `docs/eightfold-path/verified-sources.json` 的逐經來源、SHA-256、節錄與選文。
- 結尾「希有諸人民…生死難度岸」確定出自雜阿含771；第13段以 HTML 重建對照表，沒有挪用截圖當正式文字或加入心經。
- 直接台大獅子吼入口仍遭環境 CONNECT 403；中阿含深層定位尚未實際驗證，先提供明標「四阿含總入口」的註解入口，勿把雜阿含 `/agama/sub/` 套到中阿含。後續可直接從總入口查該經卷次，再替換深層網址。
- 故事110筆保持原樣，影片轉錄／原典節錄／校訂建議分開；配對與校訂說明見 `docs/eightfold-path/verification.md`。

## 四向四果與十結（第06本試閱）

- 主軸：EA 28.7，《增壹阿含經》卷20〈聲聞品第二十八〉第七經；另核對 SA490、266、71、297，DA5〈小緣經／初小緣經〉、DA9〈眾集經〉、MA16〈伽藍經〉及 SN46.55 莊春江中譯。
- 已讀取 SuttaCentral `sc-data` 固定 commit `c7bba0f184e66904949d4918587975fb7fd7ec69` 的9份原檔。檔案路徑、SHA-256、13組下緣選文及四雙八輩等導讀節錄，見 `docs/four-fruits-ten-fetters/verified-sources.json`；驗證腳本可重新下載核對。
- EA 開頭的「邠陀利華」與二果段的「邠陀利花」各依原文保留；正文「猶如邠陀利花，晨朝剖花，向暮萎死」符合本次交接訂正，未改成早摘晚長。SA266 狗子繫柱全文已核對，未把柱與皮帶的故事標示當成原典逐字引文。
- DA9 五上結的原典次序與插畫次序分開；DA5 四雙八輩用於導讀補充，不把四種姓角色分配給四果。SA71 只取「斷關」句，SA297 在導讀補回無明離欲生明的語境。
- SN46.55 明標「莊春江中譯」，中文連結在前、巴利原文對照在後。原典的「惡意」與故事的「瞋恚」不互相改寫。
- 台大獅子吼四阿含總入口及卷頁的直接請求仍遭環境 CONNECT 403。雜阿含沿用既有專站單經入口；增壹、長、中阿含先使用明標的四阿含總入口，未猜測未核實的深層錨點。SuttaCentral 經文內容經官方 GitHub 資料確認，服務站畫面與外部影片播放未驗證。
