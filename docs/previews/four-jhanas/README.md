# 四禪｜試閱紀錄與正式入口

分支 `feat/four-jhanas-review`（[PR #36](https://github.com/rooneyflower-star/sutrazen-map/pull/36)），基準main `c4e6670d30416b4203767287cf14cd754dea8dd7`。作者已於2026-11-18授權直接發布，經PR #36處理；實際發布結果見該PR最終核對。正式入口：[主題專頁](https://rooneyflower-star.github.io/sutrazen-map/four-jhanas/)／[互動繪本](https://rooneyflower-star.github.io/sutrazen-map/four-jhanas/book/)。以下保留原試閱與驗收方式。

2026-11-18更新：五蓋「瞋恚」已上移避開臉，S10圖下重複HTML表與讀經轉錄已移除，PDF同步更新。以下舊截圖保留作歷史驗收；[最新橫直式截圖與340個受影響頁面狀態驗證](../reading-focus/README.md)另列。

## 直接在iPad看

- [完整校稿PDF（24頁）](Four-Jhanas-review.pdf)：十幕全圖及7條疊字、130段字幕／起迄時間、8筆完整經文、原圖總結表與獨立閱讀說明。文字可選取；操作介面另見下方實際截圖。
- [手機守護六根](S02-360x800.webp)、[手機第四禪第三格](S09-360x800.webp)、[手機總結表](S10-360x800.webp)。

| 核對項目 | iPad橫式1024×768 | iPad直式768×1024 |
| --- | --- | --- |
| 由戒生定在右下格 | [S01](S01-page1-1024x768.webp) | [S01](S01-page1-768x1024.webp) |
| 守護六根在窗下、貓頭上方 | [S02](S02-page7-1024x768.webp) | [S02](S02-page7-768x1024.webp) |
| 五蓋圖內標籤及圖外全稱 | [S05](S05-page14-1024x768.webp) | [S05](S05-page14-768x1024.webp) |
| 初禪逐格閱讀 | [S06](S06-page22-1024x768.webp) | [S06](S06-page22-768x1024.webp) |
| 第二禪逐格閱讀 | [S07](S07-page51-1024x768.webp) | [S07](S07-page51-768x1024.webp) |
| 第三禪新版原圖 | [S08](S08-page70-1024x768.webp) | [S08](S08-page70-768x1024.webp) |
| 第四禪「捨淨念、一心」 | [S09第三格](S09-page112-1024x768.webp) | [S09第三格](S09-page112-768x1024.webp) |
| 四禪總結表 | [S10](S10-page124-1024x768.webp) | [S10](S10-page124-768x1024.webp) |
| 導讀 | [專頁](guide-1024x768.webp) | [專頁](guide-768x1024.webp) |
| 統一原經來源卡 | [來源](sources-1024x768.webp) | [來源](sources-768x1024.webp) |

另有[第四禪第三格放大視窗](fourth-third-panel-zoom.webp)及[經典依據結語](../four-jhanas-ending/ending-768x1024.webp)。

## 開啟互動版

下載[分支ZIP](https://github.com/rooneyflower-star/sutrazen-map/archive/refs/heads/feat/four-jhanas-review.zip)，解壓後在有首頁index.html的專案根目錄執行：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

專頁：`http://127.0.0.1:8765/four-jhanas/index.html`。

繪本：`http://127.0.0.1:8765/four-jhanas/book/index.html`。

第四禪第三格：`http://127.0.0.1:8765/four-jhanas/book/index.html?scene=S09&page=112`。

首頁可測第12本書架與原四禪地圖節點。iPad與電腦連同一區域網路時，將bind改成 `0.0.0.0`，iPad Safari開啟 `http://電腦的區域網路IP:8765/four-jhanas/`。結束伺服器用Ctrl+C。本機試閱不會變更GitHub Pages正式站。

沒有宣稱直接雙擊HTML、GitHub程式碼頁或iPad「檔案」快速預覽可以執行完整網站。PDF與截圖可直接開啟，互動版需上述HTTP方式。

## 重建與檢查

```sh
python3 scripts/build-four-jhanas.py --check
python3 scripts/check-four-jhanas.py --screenshots
python3 scripts/build-four-jhanas-preview.py
node --check four-jhanas/book/book.js
node --check four-jhanas/book/book-data.js
node --check four-jhanas/book/panel-focus-data.js
```

環境需Python3、Pillow、lxml、Playwright、`/usr/bin/chromium`；PDF另用PyMuPDF和Poppler的pdftotext。檢查結果見validation.json與pdf-validation.json。

以下為原132頁審閱版的驗收記錄；作者移除片尾頁後現為131頁，[最新末頁驗收](../four-jhanas-ending/README.md)另列。

五種尺寸：360×800、800×360、768×1024、1024×768、1440×900，全132頁共660個狀態；另驗35個放大字框狀態與20個分格放大狀態。核對字幕／時間／經文、完整圖片比例、百分比與cqw、字幕在上經文在下、無水平溢出、上一頁／下一頁／目錄／讀經與捲動／放大關閉／來源往返／旋轉重載保留頁碼／快速點按／末頁重讀、地圖與書架、舊十一書入口。實體Safari與外部影片播放尚未測。

來源及待校細節見[REVIEW](../../four-jhanas/REVIEW.md)。
