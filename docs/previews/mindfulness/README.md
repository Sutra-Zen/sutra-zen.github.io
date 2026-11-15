# 《四念處與四顛倒》試閱與驗證

[實作PR #22](https://github.com/rooneyflower-star/sutrazen-map/pull/22)，分支 `feat/mindfulness-preview`，從main `24983232d11bc9e775641bf444bcbe59055fe1ad` 開始。作者在第04包訊息授權直接發布，取代原交接稿的先試閱限制；實際上線以PR合併及Pages部署為準。

- [導讀入口](https://rooneyflower-star.github.io/sutrazen-map/mindfulness/)
- [完整繪本](https://rooneyflower-star.github.io/sutrazen-map/mindfulness/book/)
- [逐幕圖片與疊字核對](../../mindfulness/layout-audit.md)
- [獨立校稿清單](../../mindfulness/REVIEW_TODO.md)
- [機器驗證結果](validation.json)

25幕保留92段完整口白及既定末幕總結；18筆經文對應27組口白。窄版經文與口白可捲動、直接閱讀；圖片可放大，教學標籤可用圖外文字閱讀。最後一頁可回到第一頁。

| 畫面 | iPad橫式 | iPad直式 |
| --- | --- | --- |
| S03 指定車站圖 | [畫面](S03-1024x768.webp) | [畫面](S03-768x1024.webp) |
| S10 四大與六界分段對讀 | [畫面](S10-1024x768.webp) | [畫面](S10-768x1024.webp) |
| S18 刺藤／水果 | [畫面](S18-1024x768.webp) | [畫面](S18-768x1024.webp) |
| S19 五蓋圖內標籤 | [畫面](S19-1024x768.webp) | [畫面](S19-768x1024.webp) |
| S21 刺藤／蓮花 | [畫面](S21-1024x768.webp) | [畫面](S21-768x1024.webp) |
| S25 總結文字卡 | [畫面](S25-1024x768.webp) | [畫面](S25-768x1024.webp) |

[S25寬版總結疊字](S25-1440x900.webp)

## 本機開啟與重現

下載本次交付的固定SHA完整repository ZIP，解壓後在有根目錄index.html的位置執行：

```sh
python3 -m http.server 8765 --bind 0.0.0.0
```

電腦開 `http://127.0.0.1:8765/mindfulness/`。iPad與電腦同Wi-Fi，將127.0.0.1換成電腦區域網路IP即可。完整ZIP包含所有舊繪本、PDF及原始交接，不是只含新增頁面的局部備份。

```sh
python scripts/build-mindfulness.py --check
python scripts/check-mindfulness.py --screenshots
```

需要Python、Playwright、Pillow、lxml及Chromium。360×800、800×360、768×1024、1024×768、1440×900，共125個逐幕狀態通過；含圖片／完整文字／段落引用、圖片座標與字級、無水平溢出、目錄、翻頁／快速翻頁、縮放、全螢幕與API不可用的備援、經文捲動、來源往返、旋轉保留位置、末頁重讀及七本舊入口。91個原始檔案雜湊與既有七本／共用檔案／Pages設定不變亦通過。

本機測試首頁CDN時，透過系統CA驗證讀取實際公開回應交給Chromium，未關閉TLS驗證。實體iPad/Safari手勢及外部YouTube播放仍待作者確認。
