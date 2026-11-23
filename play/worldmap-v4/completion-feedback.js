import {cityStore} from '../city/modules/store.js';
import {renderSprite} from '../city/modules/scene.js';
import {MODULE_UI as U} from '../city/modules/text.js';

const escape=value=>String(value).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
export function compactCompletionFeedback(id,state){
 const module=cityStore.get(state.completedBookIds).modules.find(item=>item.bookId===id);
 if(!module||!module.unlocked)return '';
 const copy=module.placed?U.rewardAlreadyPlaced(module.title):module.canPlace?U.rewardUnlocked(module.title):U.rewardAwaiting(module.title);
 return `<section class="wm-compact-reward" data-completed-book="${escape(id)}" data-reward-available="${module.canPlace||module.placed}" data-city-placement="${module.placed?'placed':module.canPlace?'available':'waiting'}"><div class="wm-reward-feature">${renderSprite(module.slots.find(slot=>!slot.effect)?.assetKey,{className:'wm-reward-feature-art',label:module.title})}</div><p>${escape(copy)}</p></section>`;
}
