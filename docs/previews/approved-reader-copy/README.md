# 核可讀本修正與十四本字幕驗證

基準PR80 `a238a0fb549966ac0510b5b89f18b913c8ec40b6`，分支`fix/approved-reader-copy`。繁中讀本／遊戲共用原稿與閱讀器；本輪僅核可校訂及字幕呈現。

## 遮字問題的前後比較

作者圖中的五陰44頁有兩個硬換行，原橫式帶只預留兩行。原本可捲到底，但初看末行被截；沒有把它誤說成原稿遺失。現在橫式自然換行，統一預留三行及段落間距，圖片高度不隨當頁文字改變，原字串／頁碼不拆改。

| 情境 | 修改前 | 修改後 |
| --- | --- | --- |
| 作者相近桌面1916×963，公開讀本 | [前](before-five44-1916x963.png) | [後](after-five44-public-1916x963.png) |
| 平板橫式1024×768，後圖為遊戲複習 | [前](before-five44-1024x768.png) | [後](after-five44-review-1024x768.png) |
| 手機橫式844×390，公開讀本 | [前](before-five44-844x390.png) | [後](after-five44-public-844x390.png) |

[前測數據](before-diagnosis.json)使用Git基準版本攔截提供，不混入新CSS。後測為最終runtime。各組都實際由43按下一頁到44，對照全文與原資料相同；所有後測初始scrollTop為0，文字不需先捲動才可見。

## 十四本全量檢查

[人讀說明與各書表](caption-audit/README.md) · [精簡統計](caption-audit/summary.json) · [完整逐樣本gzip](caption-audit/full-samples.json.gz) · [資料雜湊](caption-audit/full-samples-digest.json)

- **14本×6尺寸＝84組、7,152樣本**，包含全1,192個原閱讀步驟。
- 1916×963逐本原生Next完整1,192步軌跡（1,178次點擊＋14個初始頁）；另五尺寸每個原閱讀狀態以showPage作幾何取樣，不冒稱每尺寸都完整原生實讀。
- 六尺寸：1916×963、1280×900、1024×768、768×1024、844×390、360×800。
- 4,684個標準橫式口白樣本在新自然換行下實際為4,187個一行、497個兩行，初始全部可見；預留三行是版面容量，沒有聲稱這些實際稿件都出現三行。2,342個普通直式樣本維持自然文件流。
- 另以2個明確獨立的暫時DOM三段／三行fixture檢1916與844的容量、原字級及段落間距，不寫原稿、不新增頁ID，也不計入1,192步。
- 逐文字Range、父子裁切、實際末glyph可達及185個外層最長文字代表檢查全通過。普通圖框每本／尺寸的頁間高度差 **0px**。
- 唯一局部長文字為四念處110步844×390的8行總結帶，已實際wheel捲到末字，旋轉／重整仍保持110步；[截圖](caption-audit/overflow-mindfulness-110-844x390.png)。這個保留的總結捲動不當成普通口白被裁字。

## 核可內容、模式與來源

[Focused結果](after-validation.json)核對五陰44頁public／game review×3尺寸、7→8→9來源及SA41新卡往返，43頁作者完整句／SA46／本頁經文對話；三本人物更正各兩mode，重整書籤均保持。14本各兩張普通圖框共28個smoke、心經寬版置中／窄框最右起讀原生橫捲、3種結語與按鈕避讓正常。

[五陰資料及三尺寸動線](five-source-validation.json) · [三句精準資料差異](narration-validation.json) · [原圖、待定原稿與離線包保護](source-guard.json)

[41經新來源卡](guide-sa41-360.png) · [43頁指定的新句](reader43-844.png) · [心經寬版](after-heart-1916x963.png) · [心經窄版](after-heart-844x390.png)

八正道69頁與十二因緣44–45頁資料保持基準原樣。其餘原口白／經文、插畫、場景、閱讀ID與1192步、資格／存檔形狀、首頁心智圖／SEO／Google皆保護；13個非五陰讀本HTML只有快取差異。原始storyboard封存保留；核可校訂可由產生器重建。七覺支離線30成員CRC／共享檔精確比對／原圖原稿與原書JS前版相同均通過。

以上檢查JavaScript／同源HTTP錯誤0。遊戲為隔離合法書籤／已讀fixture，不改作者存檔、不以fixture冒稱新過關。手機／平板為Chromium尺寸與操作模擬，未測實機iPhone／iPad Safari。

[實作與本機方式](../../readers/approved-copy/README.md)。正式部署狀態與精確SHA／Pages／live證據見PR交付留言；不把本機驗證冒稱已發布。
