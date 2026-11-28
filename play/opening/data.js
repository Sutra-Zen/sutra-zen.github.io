// The author's supplied illustration must be imported before this flag is true.
// The fallback is an explicit image-unavailable notice, never substitute art.
export const OPENING_VERSION='summary-merge-1';
export const TRAIN_ART=Object.freeze({
 ready:true,
 url:new URL('./assets/commuter-train.png',import.meta.url).href,
});
export const TRAIN_SCENE_IDS=Object.freeze(['train-desires','train-breathless']);
export const TRAIN_UI=Object.freeze({
 label:'電車上的小貓',continue:'點一下繼續旅程',retry:'重新載入插畫',
 readingHint:'可上下捲動閱讀，讀完後繼續旅程',
 imageAlt:'橘色虎斑小貓穿著金黃色外套，坐在電車窗邊滑手機，其他貓乘客在四周。',
 imageLoading:'正在載入電車插畫……',
 imageUnavailable:'電車插畫暫時無法顯示，你仍可以繼續故事。',
 storageUnavailable:'這次仍可繼續；裝置無法保存過場紀錄，下次可能再次顯示。',
});

export const TRAIN_TIMING=Object.freeze({pixelsPerSecond:44,minDurationMs:20000,maxDurationMs:45000,edgeGapPx:24,followthroughMs:350});
