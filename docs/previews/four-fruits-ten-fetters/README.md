# 《四向四果與十結》試閱

這是第06本的實作分支，**尚未合併main或發布正式站**。

- 分支：`feat/four-fruits-ten-fetters-preview`
- [試閱草稿PR #15](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/15)，目標main，尚未合併。
- 導讀：`four-fruits-ten-fetters/`
- 互動繪本：`four-fruits-ten-fetters/book/`，11幕、74頁。
- 11張插畫來自作者ZIP，13個素材（含2張參考圖）的尺寸／大小／SHA-256全部相符。
- [逐幕配置表與經文切換](../../four-fruits-ten-fetters/layout-audit.md)
- [驗證結果](validation.json)

## 先在iPad直接看畫面

點下表的連結可以看原尺寸截圖；GitHub若顯示檔案工具列，可點Raw開啟圖片。下方截圖均來自實際運行的閱讀器。

| 幕／試閱頁 | iPad橫式 | iPad直式 |
| --- | --- | --- |
| 01 彼岸是什麼／第1頁 | [看圖](S01-1024x768.webp) | [看圖](S01-768x1024.webp) |
| 02 斷開十結／第7頁 | [看圖](S02-1024x768.webp) | [看圖](S02-768x1024.webp) |
| 03 四種姓／第15頁 | [看圖](S03-1024x768.webp) | [看圖](S03-768x1024.webp) |
| 04 同一條修行路／第18頁 | [看圖](S04-1024x768.webp) | [看圖](S04-768x1024.webp) |
| 05 凡夫繞柱／第22頁 | [看圖](S05-1024x768.webp) | [看圖](S05-768x1024.webp) |
| 06 初果須陀洹／第25頁 | [看圖](S06-1024x768.webp) | [看圖](S06-768x1024.webp) |
| 07 欲貪與瞋恚／第33頁 | [看圖](S07-1024x768.webp) | [看圖](S07-768x1024.webp) |
| 08 二果斯陀含／第39頁 | [看圖](S08-1024x768.webp) | [看圖](S08-768x1024.webp) |
| 09 三果阿那含／第46頁 | [看圖](S09-1024x768.webp) | [看圖](S09-768x1024.webp) |
| 10 四果阿羅漢／第55頁 | [看圖](S10-1024x768.webp) | [看圖](S10-768x1024.webp) |
| 11 現世安隱／第63頁 | [看圖](S11-1024x768.webp) | [看圖](S11-768x1024.webp) |

[導讀首頁](guide-768x1024.webp) · [直接顯示的經文來源卡](sources-768x1024.webp) · [首頁書架](shelf-1024x768.webp) · [心智圖入口](map-entry-1024x768.webp)

![柱上五受陰、皮帶貪愛；完整原圖與獨立字幕區](S05-1024x768.webp)

![門閂上的貪瞋；直式閱讀器](S09-768x1024.webp)

## 互動試閱：完整ZIP＋電腦連接iPad

[下載本分支完整試閱ZIP](https://github.com/Sutra-Zen/sutra-zen.github.io/archive/refs/heads/feat/four-fruits-ten-fetters-preview.zip)。ZIP包含完整網站目錄，圖片均為相對路徑，既有五本也一併保留。交付訊息另附固定commit的ZIP，方便留存當次版本。

1. 在電腦下載、解壓ZIP，在解壓後含`index.html`的專案根目錄開啟終端機。
2. 有Python 3的電腦執行`python3 -m http.server 8765 --bind 0.0.0.0`；Windows可用`py -m http.server 8765 --bind 0.0.0.0`。
3. 電腦瀏覽器開啟`http://127.0.0.1:8765/four-fruits-ten-fetters/`，點「開始翻閱」。要檢查新書架與心智圖，則開啟`http://127.0.0.1:8765/`。
4. iPad與電腦連同一Wi-Fi。在電腦網路設定找到區域網路IP，例如`192.168.1.20`，在iPad Safari開啟`http://192.168.1.20:8765/four-fruits-ten-fetters/`（換成實際電腦IP）。伺服器需保持運行；若電腦詢問防火牆，允許這次區域網路連線。
5. 用目錄直接跳第02、05、09幕檢查圖中文字，並測試連續翻頁、橫直旋轉、右下「本頁經文」與回導讀。結束時在電腦終端機按Ctrl+C。

本環境沒有`open_cloud_preview`或桌面JS工具，無法交付已驗證的外部即時互動網址。以上HTTP方式已在測試環境驗證；iPad實體Safari與你家中的Wi-Fi連線尚待實測。不能把`file://`雙擊開HTML或正式站舊網址稱為這次試閱。

## 已完成檢查

- 手機390×844、844×390；iPad768×1024、1024×768。每尺寸74頁，共296個頁面狀態，無本地資產404或JavaScript錯誤。
- 翻頁、首尾停用、11幕目錄、頁碼、鍵盤、滑動、快速點按；維持`touch-action: manipulation`，沒有禁止雙指縮放或正常捲動。
- 橫式經文對話框、關閉、來源跳轉；直式經文直接顯示；手機放大文字時可捲動，捲經文及經文區方向鍵不誤翻頁。
- 換方向、重載、來源往返及回導讀再開書保留頁碼。
- 新導讀四尺寸、首頁第06本與四向四果心智圖入口，以及既有五本開書／下一頁／回導讀。
- 9份官方典籍資料固定版本與節錄核對；經文卡無折疊。SuttaCentral及台大獅子吼服務站畫面、YouTube實際播放、實體Safari未驗證。首頁CDN在測試中以系統CA的HTTP用戶端取得原始公開回應後送入瀏覽器，未關閉TLS驗證。

重現：`python scripts/check-four-fruits-ten-fetters.py --verify-sources --screenshots`。需Python Playwright、Pillow、lxml及Chromium；僅檢查資料可用`python scripts/build-four-fruits-ten-fetters.py --check`。
