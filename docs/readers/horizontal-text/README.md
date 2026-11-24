# 橫書純文字內容欄的響應式置中

作者指出五陰第1頁「片頭・我是誰？」在大螢幕偏左，要求橫書寬版置中、窄版左起，心經直書則保留窄版右起。本輪從已發布PR84 `8f91fd461db03fc3c43920134af315bae75181c4` 建立 `fix/horizontal-text-centering`。

## 實作

- `reader-controls.css`只新增純文字頁`reader-framed-ending`的版面。scene維持原全寬、完整縱向捲動與控件安全間距，以grid單欄`fit-content(min(100%,48rem))`把可見標題、口白、總結、表格與原經放在同一個閱讀欄。
- 欄寬依內容縮合，最多48rem，窄時受100%可用寬度限制。直接子元素`min-width:0;max-width:100%`避免表格／長文把手機推出畫面。grid列高採`max-content`，避免長總結在固定高度scene中把標題壓成0；超出部分仍由原scene捲讀。原段內左排、字級、行距、強調色與文字保持。
- 視窗寬至少690px且高至少480px時，整欄左右置中。手機直式及844×390等短橫式維持可用內容區左起；長文可捲讀，不縮字。寬橫式左右安全間距取兩側控件需求的較大值，防止末頁較寬的重讀按鈕把中軸推偏。
- 橫式純文字的scrollport在底部固定選單上方結束，頁面承接相同深色背景，避免中途正文被底部連結覆蓋。底部保留量由CSS的rem與safe-area獨立計算，避免依賴以scene底界反算的變數造成回授。直式保留原文件捲動與頁尾空間；途中正文可捲過固定底列後方，能繼續上移讀完，本輪沒有改成另一層直式捲動窗。
- 未新增DOM wrapper或改各書renderers，避免與原生心經標題移動、頁碼／選章及結語重啟流程互相干擾。心經`reader-framed-heart`與一般插畫頁`reader-stable-artwork`不套用新grid；心經原本寬時置中、窄時右起及完整橫捲保持。

十四本的18個純文字候選均盤點，包含五陰／六處片頭與片尾、八正道109–111、安那般那119的長總結與表格，其餘各書末頁。名冊與實際六尺寸驗證見[驗證紀錄](../../previews/horizontal-text/README.md)。

## 快取、離線與保護

14本HTML只將共享CSS載入key更新為`text-center-1`，各JS的既有query保持；十二因緣最新資料query仍`twelve-phone-1`。公開讀本與遊戲使用同一原生讀本與共用CSS。game產生檔不需改動且`--check`仍須通過。

七覺支離線ZIP沿既有產生器更新共30成員，僅共享CSS與該書HTML快取內容改變；原稿、原經、原圖與原書JS／CSS保留。所有14本的資料／CSV／內嵌稿與原資產、reader-layout.js、資格與存檔、首頁心智圖、SEO／Google及Pages main:/保持。

實際本機／正式站結果與精確merge SHA以驗證資料及發布PR交付為準。手機／平板為Chromium模擬，實機iPhone／iPad Safari未測。
