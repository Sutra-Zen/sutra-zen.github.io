// Shelf interface copy only; book titles and canonical content remain in catalog/data.
export const T = {
 title:'複習書架', subtitle:'讀完的故事，都在這裡。', caseLabel:'已讀繪本複習書架',
 count:n=>`已讀 ${n}／14 本`, fraction:n=>`${n}／14`,
 review:title=>`複習《${title}》`, cover:title=>`《${title}》已讀封面`,
 reviewed:'✓ 已讀・點選複習', locked:'沿旅程逐步開放', unknown:'尚未揭曉',
 emptyTitle:'書架正等著第一本故事', emptyCopy:'從第一站開始，讀完的繪本就會留在這裡，隨時可以再讀。', first:'前往第一站',
 notice:'目前無法把進度永久存入此裝置，當次仍可繼續。',
 corrupt:'裝置中的進度暫時無法讀取。你仍可前往第一站，或從設定還原備份。',
 allRead:'十四本都已讀完，可以隨時複習。',
};
