# 主線對話逐段接續與終幕關閉

2026-11-25接續PR87／main `ea6dafa701670caffb5cd4e4ee4b9df05d4ff467`，分支`fix/mandatory-mainline-dialogue`。作者要求中間對話不能用返回海圖略過，並追加最後一段右上「×」可關閉，或按「進去看看」入書，讓看完對話後仍能探索城池與書架。

## 最終互動

- 一般主線中間段只有「接著看」，沒有略過／X；Escape、底部導覽、目前關卡／主閱讀按鈕、地標與工具不能繞過或換掉這段。設定仍能備份／還原／清除。
- 沒有下一段的終幕才顯示右上「×」。X或Escape代表確認這段已看完，只回海圖、不開讀本、不計完成；稍後仍可自由探索或從目前關卡進書，不反覆彈出已確認對話。「進去看看」則直接進原繪本。
- 四聖諦讀後四段沿用既有尾聲／資格／receipt門檻；最後X或「接著看」都接原新增城景通知，再自行選城池／下一站。不能從前三段直接跳通知，也不把對話當成閱讀完成。
- 工具中的唯讀重播各幕可回海圖，末幕也有X，完全不寫seen、pending、reading或receipt。電車動畫、標題與零本完成啟動規則保持。

## 精確接續與資料邊界

舊seen-on-show不足以恢復未確認當幕：原版疑幕／五陰入口顯示後重整就消失。本輪保留既有seen schema及首本pending語義，另加`play/story/pending.js`的純呈現checkpoint `{version:1,sceneId,context}`。normal show存目前幕、Next以下一幕覆寫；終幕確認才清。generic close不清，避免途中離開／重整丟進度。context區分同一五陰湖台詞在首本尾聲或獨立入口的角色。

local key為`sutrazen.play.story-pending.v1`，session fallback為`sutrazen.play.story-pending.session.v1`；quota恢復綁baseRaw，清除有null tombstone以免舊fallback復活。壞／未知／train scene不被當成讀本權限；恢復前仍驗原資格、合法完成、末頁與書籤。既有合法bookmark含0、已完成者優先，不被舊pending強插。沒有pending時才以原seen補尚未結束的抵達段落，終幕seen＋無pending視為已確認。reset／restore共用clearPresentation清pending，reading／city備份版本及shape保持。

active cache `mandatory-dialogue-1`同步story／reset單例與14本bridge query，產生器同步/game。原台詞／IDs／graph、14本1192步／原圖／經文、共享讀本版面、主線資格／完成保存與SEO／Google保持；電車原ZIP／PNG逐位元不變。Pages仍legacy main:/，QA目錄排除新增一處共31。[focused驗證與代表畫面](../../previews/mandatory-dialogue/README.md)區分實際按鍵與隔離完成fixture，正式發布證據以本輪PR精確SHA／Pages／live紀錄為準；實機iPhone／iPad Safari未測。
