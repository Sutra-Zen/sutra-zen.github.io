import * as cityArt from '../visual-v2/city-tactics.js';
import {routeBooks} from '../route/selectors.js';
import {T} from './text.js';

const catalogURL=new URL('../collection/catalog.js',import.meta.url);
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const roles={'five-aggregates':'lord','six-senses':'gates',mindfulness:'guardian',anapana:'messengers'};
const fallbackCrops={lord:[745,205,215,205],gates:[740,30,190,150],guardian:[420,530,150,150],messengers:[1010,430,170,150]};
function rewardArt(id,title){
 if(id==='four-truths')return `<img class="wm-reward-feature-art" src="${new URL('../visual-v2/assets/city-dharma-dock-concept.png',import.meta.url).href}" alt="${escape(title)}">`;
 const role=roles[id],crop=(cityArt.CITY_REWARD_CROPS||fallbackCrops)[role];
 if(role&&crop){
  const box=Array.isArray(crop)?crop:[crop.x,crop.y,crop.w,crop.h];
  return `<svg class="wm-reward-feature-art" viewBox="${box.join(' ')}" role="img" aria-label="${escape(title)}">${cityArt.renderCitySVGImages()}</svg>`;
 }
 const book=routeBooks.find(b=>b.id===id);
 return book?`<img class="wm-reward-feature-art wm-reward-book-art" src="${new URL(book.cover,catalogURL).href}" alt="${escape(book.title)}">`:'';
}
export function compactCompletionFeedback(id,state){
 const reward=state.city.rewards.find(r=>r.bookId===id);
 if(!reward)return '';
 const copy=reward.available?(T.rewardCopy[id]||T.rewardReady(reward.title)):T.rewardPending(reward.title);
 return `<section class="wm-compact-reward" data-completed-book="${id}" data-reward-available="${reward.available}"><div class="wm-reward-feature">${rewardArt(id,reward.title)}</div><p>${escape(copy)}</p></section>`;
}
