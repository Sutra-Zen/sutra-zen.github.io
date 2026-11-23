# 波旬位置、城主表情與滿版書架

2026-11-23，從已發布PR75 main `a9ee6ae8fda9e1ec01822aa013ad85bcdf551f3a` 建立 `fix/game-city-shelf-framing`，起始乾淨、origin為Sutra-Zen/sutra-zen.github.io。延續作者遊戲更新與發布授權，本輪僅調整場景呈現。

- 波旬沿用原朝右的全身圖，不翻轉或重畫；移至城主左上。念守門人尚未出現時為世界座標(500,130)，出現後為(250,230)，避開北／西北城門、貓頭鷹與信心港灣。角色浮動及點擊對話保留。
- 城主汗滴DOM、is-calm汗速標記、CSS與keyframe全部移除；皇冠、鬍鬚、原圖、位置及對話保留。其他五蓋的微晃與減少動態支援不變。
- 書架移除stage外邊距、case寬度上限與圓角邊框，原library-concept.png鋪滿左右；主區同圖襯底，空狀態也沒有棕色側欄。背景原件不改，桌面維持四欄、手機兩欄，書名、原封面及資格完全不變。
- 桌面case最低高度保留1100px以維持書本可讀尺寸，超寬視窗按原圖3:2比例增加；手機保留原兩欄高度與安全邊距。stage仍可垂直捲動，底列不遮住最後一冊，沒有把四排書硬塞進100vh。

UI入口／導航與讀本回程使用 `framing-1` 以避開舊HTML／scene／shelf.css快取。city、thoughts及完成縮圖共用同一個新版scene模組，避免SVG裁窗ID重複。city store/catalog/text與journey-save保持 `auto-city-1` 原URL，collection/story單例、schema、資格、完成通知及四段過場原邏輯不改。

14本原HTML只更新bridge query，bridge只有game回程query改動。根首頁、32心智圖、14本原稿／經文／圖片／操作、SEO15／sitemap／robots／Google原檔保留。生成來源與game同步，Pages仍legacy main:/，新增本輪QA排除後共22個目錄。

驗證採本輪風險：五尺寸加2048×1115書架0／1／14歷史狀態、左右滿版、最末冊捲動可達、已讀複習／鎖定資格與主線保存；城池首次與全城的波旬位置、無汗、對話X／來源／全景返回；原站615保護與入口／SEO檢查。沒有因呈現小改重讀未變更的四聖諦29步，以前輪正式站實讀及本輪逐位元保護為依據。

實際結果與截圖見[本輪驗證](../../previews/game-framing/README.md)，實際操作與隔離歷史fixture分開，實機iPhone／iPad Safari未測。精確merge SHA的Pages與正式站驗收另記本輪PR；本文件不推定已發布。
