// Fictional city inner voices. Separate from scripture and reading completion.
import {STORY_ACTORS} from '../story/data.js?v=summary-merge-1';
import {renderSprite} from './modules/scene.js?v=summary-merge-1';
const COPY=Object.freeze({
 label:'城池角色對話',close:'關閉對話',
 lordName:'識・城主',maraName:'波旬',guardianName:'念-守門人',messengersName:'止・觀使者',
 lordEarly:'哎呀，花園裡怎麼來了這麼多客人？先慢慢看清楚，聽聽大家在說什麼吧。',
 lordWatched:'有人幫忙留意城門，我可以先聽清楚、看清楚，再慢慢回應。花園也需要繼續照料呢。',
 maraEarly:'只有花園和碼頭，大家還忙成一團。讓我在附近看看，有沒有熱鬧可湊！',
 maraGates:'哼，門蓋得倒漂亮，卻連個看門的都沒有！',
 maraWatched:'那位提燈的傢伙開始留意我們了……先到旁邊看看。',
 guardian:'先看看來的是誰，再提醒大家。六道門仍要正常通行，我會留意眼前發生的事。',
 messengersReady:'我們帶著展開的卷軸來了。到四大廣場，把消息清楚地傳達給城主吧。',
 messengersWaiting:'卷軸準備好了。等道路與接引的條件齊備，再去四大廣場傳達消息吧。',
 desireName:'五蓋眾・貪欲',desire:'那邊的甜點看起來好好吃……這個也想要，那個也想帶走！',
 angerName:'五蓋眾・瞋恚',anger:'哼，我現在就是不高興！先讓我在旁邊轉兩圈。',
 slothName:'五蓋眾・昏沉',sloth:'眼皮好重……先讓我在草地上睡一下。',
 restlessnessName:'五蓋眾・掉悔',restlessness:'這邊看看，那邊也得看看……我又想到剛才的事了！',
 doubtName:'五蓋眾・疑',doubt:'真的要走這條路嗎……？先在附近看看好了。',
 owlName:'擇法夥伴・貓頭鷹',owl:'七覺支中的擇法覺支。',
 rabbitName:'精進夥伴・兔子',rabbit:'七覺支中的精進覺支。',
 birdName:'喜夥伴・藍鳥',bird:'七覺支中的喜覺支。',
 turtleName:'輕安夥伴・烏龜',turtle:'七覺支中的輕安覺支。',
 lotusName:'定夥伴・蓮花',lotus:'七覺支中的定覺支。',
 deerName:'捨夥伴・小鹿',deer:'七覺支中的捨覺支。',
});
export const CITY_THOUGHT_LOCALE='zh-Hant';
export const CITY_THOUGHT_FUTURE_LOCALES=Object.freeze(['zh-Hans','en','ja']);
const FIGURES=Object.freeze({
 lord:{asset:'city_lord',name:'lordName',id:'city-lord-introduction'},
 mara:{asset:'mara',name:'maraName',id:'mara-at-city'},
 guardian:{asset:'mindfulness_guard',name:'guardianName',id:'mindfulness-guardian-introduction'},
 messengers:{asset:'messengers',name:'messengersName',id:'calm-insight-messengers-arrival'},
 desire:{asset:'hindrance_desire',name:'desireName',id:'desire-at-city'},
 anger:{asset:'hindrance_anger',name:'angerName',id:'anger-at-city'},
 sloth:{asset:'hindrance_sloth',name:'slothName',id:'sloth-at-city'},
 restlessness:{asset:'hindrance_restlessness',name:'restlessnessName',id:'restlessness-at-city'},
 doubt:{asset:'hindrance_doubt',name:'doubtName',id:'doubt-at-city'},
 'awakening-owl':{asset:'companion_owl',name:'owlName',text:'owl',id:'awakening-owl-at-city'},
 'awakening-rabbit':{asset:'companion_rabbit',name:'rabbitName',text:'rabbit',id:'awakening-rabbit-at-city'},
 'awakening-bird':{asset:'companion_bird',name:'birdName',text:'bird',id:'awakening-bird-at-city'},
 'awakening-turtle':{asset:'companion_turtle',name:'turtleName',text:'turtle',id:'awakening-turtle-at-city'},
 'awakening-lotus':{asset:'companion_lotus',name:'lotusName',text:'lotus',id:'awakening-lotus-at-city'},
 'awakening-deer':{asset:'companion_deer',name:'deerName',text:'deer',id:'awakening-deer-at-city'},
});
function thought(actor,state){
 const placed=new Set(state.placedIds||[]),figure=FIGURES[actor];if(!figure||!state.baseVisible)return null;
 if(actor==='guardian'&&!placed.has('mindfulness_guard'))return null;
 if(actor==='messengers'&&!placed.has('calm_insight_messengers'))return null;
 if(actor.startsWith('awakening-')&&!placed.has('awakening_companions'))return null;
 let key=figure.text||actor,id=figure.id;
 if(actor==='lord')key=placed.has('mindfulness_guard')?'lordWatched':'lordEarly';
 if(actor==='mara'){
  key=placed.has('mindfulness_guard')?'maraWatched':placed.has('six_gates')?'maraGates':'maraEarly';
  if(key==='maraGates')id='six-gates-unwatched';
 }
 if(actor==='messengers')key=placed.has('noble_path')&&placed.has('mindfulness_guard')?'messengersReady':'messengersWaiting';
 return {actor,id,asset:figure.asset,name:COPY[figure.name],text:COPY[key]};
}
export function initializeCityThoughts({host,getState,onSeen,onClose}={}){
 const panel=document.createElement('section');panel.className='city-thought';panel.hidden=true;panel.setAttribute('aria-label',COPY.label);
 panel.setAttribute('role','dialog');panel.setAttribute('aria-labelledby','city-thought-speaker');
 panel.innerHTML='<button class="city-thought__close" data-city-thought-close type="button" aria-label="'+COPY.close+'">×</button><div class="city-thought__portrait" aria-hidden="true"></div><div class="city-thought__body"><h2 id="city-thought-speaker"></h2><p class="city-thought__line"></p></div>';
 host.append(panel);let current=null,opener=null;
 function close(){if(panel.hidden)return;panel.hidden=true;current=null;host.classList.remove('has-city-thought');if(opener?.isConnected&&opener.getClientRects().length)opener.focus({preventScroll:true});else onClose?.();}
 function show(actor='lord',{remember=true,focus=true}={}){
  const value=thought(actor,getState());if(!value)return false;
  if(panel.hidden)opener=document.activeElement;current=value;panel.dataset.actor=actor;panel.dataset.thought=value.id;
  panel.querySelector('h2').textContent=value.name;panel.querySelector('.city-thought__line').textContent=value.text;
  const portrait=panel.querySelector('.city-thought__portrait');
  if(value.actor==='mara'){
   const image=document.createElement('img');image.src=STORY_ACTORS.mara.portrait;image.alt=value.name;
   image.width=1254;image.height=1254;image.draggable=false;
   image.addEventListener('error',()=>{image.hidden=true;},{once:true});
   portrait.replaceChildren(image);
  }else portrait.innerHTML=renderSprite(value.asset,{label:value.name});
  panel.hidden=false;host.classList.add('has-city-thought');panel.scrollTop=0;if(remember)onSeen?.(value.id);
  if(focus)panel.querySelector('[data-city-thought-close]').focus({preventScroll:true});return true;
 }
 panel.querySelector('[data-city-thought-close]').addEventListener('click',close);
 panel.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();close();}});
 return {show,close,get isOpen(){return !panel.hidden;},get currentActor(){return current?.actor||null;}};
}
