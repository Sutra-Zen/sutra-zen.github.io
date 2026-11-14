# 畫面疊字與四格閱讀焦點：試閱截圖

本資料夾保留發布前的試閱截圖。作者後續已明確授權直接發布本版，實際上線以 PR #12 與對應 GitHub Pages 部署結果為準。

## 先行試排：正志

正志的兩行原文字樣獨立置於圖片內，已從上緣章節小字移除：

```text
八正道：正志
十善業道：不貪，不瞋恚
```

先檢視左側，毒花和整塊DANGER/TOXIC木牌沒有可容納兩行字的空間；本次改試排於圖內上方中央偏右（x44.5%、y2.5%、寬41%、靠左），保留木牌、貓眼鼻口、羅盤與鐵槍。會覆到少量貓耳／額頂毛色，仍需作者確認視覺取向。這是本次避讓試排，**不是原影片座標還原**。

橫式為旁白和經文保留上下區域，圖片完整等比例置於其間；位置均相對實際圖片。同幕旁白採最大高度預留，避免換句時圖片及疊字跳動。直式仍保留上方旁白、圖片、下方經文和底部控制。

- [手機橫式](right-intention-phone-landscape.png)
- [手機直式](right-intention-phone-portrait.png)
- [iPad橫式](right-intention-ipad-landscape.png)
- [iPad直式](right-intention-ipad-portrait.png)

各幕文字、座標、對齊、寬度、字級與直式覆寫存於 `docs/eightfold-path/storyboard.json` 的 `presentation`，原字幕與經文內容不變。

## 其他試閱截圖

- 五陰原三格：[橫式](five-aggregates-panels-phone-landscape.png)／[直式](five-aggregates-panels-phone-portrait.png)
- 六處四格：[橫式](six-senses-panels-phone-landscape.png)／[直式](six-senses-panels-phone-portrait.png)
- 正語完整對照與四格：[橫式](right-speech-phone-landscape.png)／[直式](right-speech-phone-portrait.png)

五陰現有13張原圖裡，多格漫畫是「宿命神通」三格圖；此版保留原圖不等寬的三格，只遮暗另外兩格。六處六組四格均為三暗一亮。原圖、全書頁數、字幕、經文及舊有疊字保留。

## 驗證結果

Chromium觸控模擬在390×844、844×390、768×1024、1024×768，各檢查八正道110頁、五陰54頁、六處115頁，共1116次頁面狀態，全部通過。檢查逐頁內容保留、圖片載入與比例、各狀態的疊字／遮罩、圖片百分比定位、同幕位置穩定、與旁白／經文／控制的避讓、正志近似保護區、翻頁／鍵盤／滑動、方向切換頁碼及經文對話框。另驗證來源導讀與瀏覽器返回保留頁碼、長經文捲動不誤翻。

- [機器可讀測試摘要](validation.json)
- [旁白白字像素檢查](caption-paint-results.json)
- 測試腳本：`scripts/check-picture-book-overlays.py`
- 另以 `scripts/check-panel-caption-paint.py` 比較遮罩開關前後的白字像素，確認五陰／六處四尺寸的旁白不被遮暗。
- 分鏡布局與頁碼映射：`docs/eightfold-path/overlay-layout.md`
- 真實iPad/Safari未測；所有未記明原影片座標都屬本次試排。

## 完整互動試閱

下載此分支的ZIP並完整解壓，或clone此分支。在儲存庫根目錄執行：

```sh
python -m http.server 8765
```

以瀏覽器開啟：

- 八正道：`http://127.0.0.1:8765/eightfold-path/book/`
- 五陰：`http://127.0.0.1:8765/five-aggregates/book/`
- 六處：`http://127.0.0.1:8765/six-senses/book/`

本環境沒有對外即時預覽工具；作者已改為直接發布後從正式站確認。上面的GitHub截圖保留供對照，不必先下載ZIP。正式站更新結果以PR #12與對應Pages為準。
