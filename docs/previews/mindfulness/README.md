# 《四念處與四顛倒》試閱與驗證

初版[PR #22](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/22)已發布。作者回饋後，從main `1d964bbd8d6c9d0c05aa725f36da1b44d8ffb078` 建立 `fix/mindfulness-consistent-reader`，[修正PR #23](https://github.com/Sutra-Zen/sutra-zen.github.io/pull/23)，改為與第06／07本相同的閱讀器與原經來源卡。實際修正版上線以新的PR合併及Pages部署為準。

- [導讀入口](https://sutra-zen.github.io/mindfulness/)
- [完整繪本](https://sutra-zen.github.io/mindfulness/book/)
- [逐幕圖片與疊字核對](../../mindfulness/layout-audit.md)
- [獨立校稿清單](../../mindfulness/REVIEW_TODO.md)
- [機器驗證結果](validation.json)

25幕保留92段完整口白，依原標點分成109張上方字幕頁，再接既定總結與阿含經依據製作說明，共111頁。18筆經文對應27組口白，顯示於下方經文帶；手機可直接捲動，橫式沿用本頁經文視窗。插畫完整保留，可點選放大。最後一頁可回到第一頁。

| 畫面 | iPad橫式 | iPad直式 |
| --- | --- | --- |
| S03 指定車站圖 | [畫面](S03-1024x768.webp) | [畫面](S03-768x1024.webp) |
| S10 四大與六界分段對讀 | [畫面](S10-1024x768.webp) | [畫面](S10-768x1024.webp) |
| S18 刺藤／水果 | [畫面](S18-1024x768.webp) | [畫面](S18-768x1024.webp) |
| S19 五蓋圖內標籤 | [畫面](S19-1024x768.webp) | [畫面](S19-768x1024.webp) |
| S21 刺藤／蓮花 | [畫面](S21-1024x768.webp) | [畫面](S21-768x1024.webp) |
| S25 總結文字卡 | [畫面](S25-1024x768.webp) | [畫面](S25-768x1024.webp) |
| 阿含經依據與重讀 | [畫面](afterword-1024x768.webp) | [畫面](afterword-768x1024.webp) |

[S25寬版總結疊字](S25-1440x900.webp)

[與舊書相同的原經來源卡](sources-768x1024.webp)

## 本機開啟與重現

下載本次交付的固定SHA完整repository ZIP，解壓後在有根目錄index.html的位置執行：

```sh
python3 -m http.server 8765 --bind 0.0.0.0
```

電腦開 `http://127.0.0.1:8765/mindfulness/`。iPad與電腦同Wi-Fi，將127.0.0.1換成電腦區域網路IP即可。完整ZIP包含所有舊繪本、PDF及原始交接，不是只含新增頁面的局部備份。

```sh
python scripts/build-mindfulness.py --check
python scripts/check-mindfulness.py --screenshots --verify-sources
```

需要Python、Playwright、Pillow、lxml及Chromium。360×800、800×360、768×1024、1024×768、1440×900，共555個逐頁狀態通過；含圖片／完整文字／段落引用、圖片座標與字級、上下文字帶避讓、無水平溢出、目錄、翻頁／快速翻頁、圖片放大、經文視窗／捲動、來源往返、旋轉保留精確頁碼、末頁重讀及七本舊入口。翻頁按鍵與目錄位置逐尺寸與第07本量測相同。91個原始檔案雜湊與既有七本／首頁／共用檔案／Pages設定不變亦通過；7份官方原典／中譯原檔已重新下載核對SHA-256。

實體iPad/Safari手勢、外部YouTube播放及台大獅子吼服務站實際畫面仍待確認。
