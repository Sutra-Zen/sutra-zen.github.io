import {cityStore} from '../city/modules/store.js?v=auto-city-1';
import {renderSprite} from '../city/modules/scene.js?v=character-pronouns-1';
import {MODULE_UI as U} from '../city/modules/text.js?v=auto-city-1';

const escape=value=>String(value).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
export function compactCompletionFeedback(id,state){
 const module=cityStore.get(state.completedBookIds).modules.find(item=>item.bookId===id);
 if(!module||!module.unlocked)return '';
 const copy=module.placed?U.rewardAdded(module.title):U.rewardAwaiting(module.title);
 return `<section class="wm-compact-reward" data-city-auto-notice data-completed-book="${escape(id)}" data-reward-available="${module.placed}" data-city-placement="${module.placed?'automatic':'waiting'}"><div class="wm-reward-feature">${renderSprite(module.slots.find(slot=>!slot.effect)?.assetKey,{className:'wm-reward-feature-art',label:module.title})}</div><p><strong>${U.autoNoticeTitle}</strong><br>${escape(copy)}</p></section>`;
}
