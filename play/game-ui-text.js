// Interface copy only; stable book IDs, narration and scripture stay separate.
export const GAME_LOCALE='zh-Hant';
export const GAME_FUTURE_LOCALES=Object.freeze(['zh-Hans','en','ja']);
export const GAME_UI=Object.freeze({
 brand:'SutraZen',title:'佛陀的解憂之旅',subtitle:'療癒系佛法繪本遊戲',tagline:'跟著小貓，讀懂煩惱，練習放下。',
 dockLabel:'旅程底部操作列，可左右滑動查看所有操作',dockPrevious:'向左查看旅程選單',dockNext:'向右查看地圖工具',navigation:'遊戲主選單',map:'地圖',city:'城池',shelf:'書架',
 progress:(count,total)=>`已讀 ${count}／${total} 本`,settings:'設定',settingsTitle:'旅程設定',close:'關閉',start:'開始旅程',continue:'繼續旅程',
 titleArtUnavailable:'旅程封面尚未載入，您仍可開始。',localSave:'旅程進度保存在此裝置的瀏覽器。',
 cityStorageUnavailable:'城池配置目前無法永久保存；閱讀仍可繼續，離開分頁後可能需要重新安置。',cityStorageCorrupt:'城池配置暫時無法讀取；已讀紀錄與閱讀位置不受影響。',
 storageUnavailable:'進度目前無法永久保存；離開後可能無法續讀，本次仍可閱讀。',storageCorrupt:'原有存檔暫時無法讀取，您仍可開始閱讀或還原備份。',
 backup:'下載進度備份',restore:'還原進度備份',restored:'已還原閱讀進度與城池配置。',restoredTemporary:'進度已還原；目前無法永久保存，請先保持本分頁開啟。',invalidBackup:'這份檔案不是可用的旅程備份，原有進度未變更。',restoreFailed:'無法讀取這份檔案，請重新選取進度備份。',
 authorReset:'重置進度（試玩用）',authorResetConfirm:'要從頭開始試玩嗎？這會清除此裝置的遊戲閱讀位置、已讀紀錄、城池配置與開場紀錄；原網站繪本與其他設定不受影響。',authorResetDone:'已重置，可以從第一幕重新開始。',authorResetTemporary:'本頁已從頭開始；裝置無法永久保存重置結果，下次可能仍需重置。',
 reset:'清除旅程進度',resetConfirm:'要清除這個瀏覽器的旅程進度嗎？此動作只影響繪本旅程，建議先下載備份。',resetDone:'已清除旅程進度，可以從第一站重新開始。',
 originalMap:'原修道心智圖',originalSite:'SutraZen 原網站',sources:'城池與原經對讀',fullscreen:'進入全螢幕',exitFullscreen:'離開全螢幕',fullscreenUnavailable:'此瀏覽器未能開啟全螢幕，仍可使用目前的滿版介面。',fullscreenNote:'全螢幕為選用功能，不影響閱讀與儲存。',moreLinks:'原網站與對讀',saveTools:'存檔與備份',displayTools:'畫面',
});
