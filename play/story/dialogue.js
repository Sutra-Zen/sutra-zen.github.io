import {STORY_ACTORS,STORY_SCENES,STORY_UI as T} from './data.js?v=mandatory-dialogue-1';
import {storyStore} from './store.js?v=mandatory-dialogue-1';
import {pendingStory} from './pending.js?v=mandatory-dialogue-1';

export function initializeStoryDialogue({host,onAction,onClose,onDismiss,onScene}={}){
 if(!host)throw Error('Missing story dialogue host.');
 const panel=document.createElement('section');panel.className='story-dialogue';panel.hidden=true;panel.setAttribute('aria-label',T.dialogue);
 panel.innerHTML='<button type="button" class="story-dialogue__close" data-story-close hidden>×</button><div class="story-dialogue__portrait"><img alt="" width="1254" height="1254">'+Array.from({length:6},()=>'<span class="story-doubt-mark" data-doubt-portrait-mark aria-hidden="true"></span>').join('')+'</div><div class="story-dialogue__body"><h2 id="story-speaker"></h2><p id="story-line" class="story-dialogue__line"></p><section class="story-dialogue__completion" hidden><h3 id="story-completion-title"></h3><div id="story-completion-content"></div></section><p class="story-dialogue__notice" role="status" hidden></p></div><div class="story-dialogue__actions"><button class="story-dialogue__skip"></button><button class="story-dialogue__next" aria-describedby="story-line"></button></div>';
 host.append(panel);
 let current=null,currentId=null,replay=false,context=null,previousFocus=null;
 const image=panel.querySelector('img'),portrait=panel.querySelector('.story-dialogue__portrait');
 const line=panel.querySelector('.story-dialogue__line'),completion=panel.querySelector('.story-dialogue__completion');
 const completionTitle=panel.querySelector('#story-completion-title'),completionContent=panel.querySelector('#story-completion-content');
 const secondary=panel.querySelector('.story-dialogue__skip'),primary=panel.querySelector('.story-dialogue__next'),closeButton=panel.querySelector('[data-story-close]');
 closeButton.setAttribute('aria-label',T.closeDialogue);
 function clearCompletion(){completion.hidden=true;completionTitle.textContent='';completionContent.replaceChildren();}
 for(const mark of portrait.querySelectorAll('.story-doubt-mark'))mark.textContent=T.questionMark;
 image.addEventListener('error',()=>{image.hidden=true;panel.classList.add('story-dialogue--no-art');});
 image.addEventListener('load',()=>{image.hidden=false;panel.classList.remove('story-dialogue--no-art');});
 function close({restoreFocus=true}={}){
  panel.hidden=true;current=null;currentId=null;context=null;clearCompletion();host.classList.remove('has-story-dialogue');onScene?.(null);
  if(restoreFocus){if(previousFocus?.isConnected&&previousFocus.getClientRects().length)previousFocus.focus({preventScroll:true});else onClose?.();}
 }
 function dismiss(){
  if(!current)return;
  if(!replay&&context!=='completion-reward'&&current.nextSceneId){primary.focus({preventScroll:true});return;}
  const scene=current,reviewing=replay,flow=context;
  if(!reviewing&&flow!=='completion-reward')pendingStory.clear();
  close();onDismiss?.(scene,{replay:reviewing,context:flow});
 }
 function show(id,{replay:reviewing=false,focus=true,context:flow=null}={}){
  const scene=STORY_SCENES[id],actor=scene&&STORY_ACTORS[scene.actorId];if(!actor)return false;
  if(panel.hidden)previousFocus=document.activeElement;
  current=scene;currentId=id;replay=reviewing;context=flow;panel.dataset.scene=id;panel.dataset.actor=scene.actorId;panel.dataset.context=flow||'';portrait.dataset.storyActor=scene.actorId;
  panel.dataset.doubtState=scene.doubtState||'';
  clearCompletion();panel.querySelector('h2').textContent=actor.name;line.hidden=false;line.textContent=scene.text;
  const completing=!reviewing&&flow==='first-completion';
  secondary.hidden=!reviewing;secondary.textContent=reviewing?T.returnToMap:'';
  closeButton.hidden=Boolean(scene.nextSceneId);
  panel.classList.toggle('has-close',!closeButton.hidden);
  primary.textContent=completing||scene.nextSceneId?T.next:replay?T.returnToMap:['enter-first-book','enter-aggregates-book'].includes(scene.action)?T.enter:(scene.nextLabel||T.enter);
  primary.setAttribute('aria-describedby','story-line');
  image.hidden=false;image.src=actor.portrait;
  // The legacy first-outro cutoff is acknowledged only at the new final scene.
  if(!reviewing){if(scene.seenOn!=='outro-end')storyStore.markSeen(id);pendingStory.set(id,flow);}
  const notice=panel.querySelector('.story-dialogue__notice');notice.textContent=storyStore.issue==='corrupt'?T.storageCorrupt:storyStore.issue||pendingStory.issue?T.storageUnavailable:'';notice.hidden=!notice.textContent;
  panel.hidden=false;host.classList.add('has-story-dialogue');panel.scrollTop=0;onScene?.(scene,{replay:reviewing,context:flow});
  if(focus)panel.querySelector('.story-dialogue__next').focus({preventScroll:true});return true;
 }
 // Reward HTML is supplied only by the game's escaped, internal feedback
 // renderer. This view is transient: it is not an authored scene or save flag.
 function showCompletion({bookId,title='',html='',nextLabel=T.completionNext,cityLabel=T.completionCity}={}){
  const actor=STORY_ACTORS.traveler;if(typeof bookId!=='string'||!bookId)return false;
  if(panel.hidden)previousFocus=document.activeElement;
  pendingStory.clear();closeButton.hidden=true;panel.classList.remove('has-close');
  current={actorId:'traveler',bookId,group:'completion-reward'};currentId='completed-'+bookId;replay=false;context='completion-reward';
  panel.dataset.scene=currentId;panel.dataset.actor='traveler';panel.dataset.context=context;portrait.dataset.storyActor='traveler';
  clearCompletion();panel.querySelector('h2').textContent=actor.name;line.textContent='';line.hidden=true;
  completionTitle.textContent=title;completionContent.innerHTML=typeof html==='string'?html:'';completion.hidden=false;
  secondary.hidden=false;secondary.textContent=cityLabel;primary.textContent=nextLabel;
  primary.setAttribute('aria-describedby','story-completion-title story-completion-content');
  image.hidden=false;image.src=actor.portrait;
  const notice=panel.querySelector('.story-dialogue__notice');notice.textContent='';notice.hidden=true;
  panel.hidden=false;host.classList.add('has-story-dialogue');panel.scrollTop=0;onScene?.(current,{replay:false,context});
  primary.focus({preventScroll:true});return true;
 }
 closeButton.addEventListener('click',dismiss);
 secondary.addEventListener('click',()=>{
  if(context!=='completion-reward'){dismiss();return;}
  const scene={...current,action:'completion-city'};close({restoreFocus:false});onAction?.(scene,{context:'completion-reward',replay:false});
 });
 panel.querySelector('.story-dialogue__next').addEventListener('click',()=>{
  if(!current)return;const scene=current,reviewing=replay,flow=context;
  if(flow==='completion-reward'){close({restoreFocus:false});onAction?.({...scene,action:'completion-next'},{context:'completion-reward',replay:false});return;}
  if(scene.nextSceneId){show(scene.nextSceneId,{replay:reviewing,context:flow});return;}
  if(!reviewing)pendingStory.clear();
  close({restoreFocus:false});onAction?.(scene,{replay:reviewing,context:flow});
 });
 panel.addEventListener('keydown',event=>{if(event.key==='Escape'){
  event.preventDefault();
  event.stopPropagation();
  if(!replay&&context!=='completion-reward'&&current?.nextSceneId){primary.focus({preventScroll:true});return;}
  dismiss();
 }});
 return {show,showCompletion,close,get isOpen(){return !panel.hidden;},get currentSceneId(){return currentId;}};
}
