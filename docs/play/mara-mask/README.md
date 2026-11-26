# 波旬蒙面造型與城池角色

2026-11-26，接續已發布 PR89／main `e05cad72747769adbbd9ed4a713c6a237ed353f4`。作者確認揭面前、揭面後的對話頭像及城池全身預覽，並授權更新發布。

目前遊戲使用**揭面前**版本：紫色戲面具戴在臉上，紫色兜帽、繫帶與小蝙蝠翅膀保持一致。城池仍位於原左上位置、朝右，沿用完整衣襬及雙腳的漂浮圖。原漂浮 CSS、減少動畫規則、世界座標及角色 ID 保持。

故事共用 `STORY_ACTORS.mara.portrait` 改指新蒙面頭像。城池點波旬的對話亦使用同一張頭像，避免將全身圖縮進手機頭像欄；其他角色仍用原 SVG sprite。角色對話的姓名、台詞、關閉／焦點行為與紀錄不變；頭像載入失敗時保留可閱讀的姓名與文字。

最新四聖諦至五陰主線仍依作者上一版劇本，不為換圖插回舊 `mara-watches`。該保留場景使用新版共用頭像。未新增終章、揭面事件、台詞或進度條件；揭面後兩張圖僅保存供後續演出使用，沒有任何目前 runtime 引用，也不因完成十四本而提前切換。

## 素材與維護

- 對話頭像：[蒙面](../../../play/story/assets/mara-masked-portrait.png)、[揭面後預留](../../../play/story/assets/mara-unmasked-portrait.png)。
- 城池全身：[蒙面](../../../play/city/modules/assets/mara-masked-fullbody.png)、[揭面後預留](../../../play/city/modules/assets/mara-unmasked-fullbody.png)。
- [來源、尺寸與 SHA-256](asset-provenance.json)記錄四張 imagegen 預覽的原始 PNG。全部逐位元匯入，沒有程式重繪、裁圖、去背、翻轉或重新編碼。
- 新全身 sprite 的 SVG viewBox 依原圖 Alpha≥32 範圍加 8px 邊界。`art.js` 與 `assets/generated-provenance.json` 同步尺寸／座標／雜湊；原概念稿 PNG、原 provenance 及歷史檔仍保留，舊 metadata 另記於 `previousMara`。
- 共享入口／回程 import 鏈使用 `mara-mask-1`，避免瀏覽器重用舊圖來源。十四本讀本只更新 bridge query；正文、經文、插畫、原生讀本、共用版面、資格、完成與存檔格式不變。
- `/game/index.html` 由 `scripts/build-game-entry.py` 從共享 worldmap shell 產生。Seven Factors 離線產生器會移除 game bridge，因此本輪重新產生的 30 成員 ZIP 與前版逐位元相同。

## 驗證範圍

本輪針對角色換圖、手機／平板版面、漂浮／減少動畫及對話互動做 focused 驗證，不宣稱重新逐頁閱讀十四本。[截圖與實際結果](../../previews/mara-mask/README.md)分別標記隔離完成紀錄 fixture 與保留場景的元件預覽。正式 merge SHA、Pages 部署與正式站驗收以發行 PR 留言為準。實機 iPhone／iPad Safari 未測。
