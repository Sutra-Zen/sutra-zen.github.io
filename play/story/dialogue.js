import {STORY_ACTORS,STORY_SCENES,STORY_UI as T} from './data.js?v=doubt-1';
import {storyStore} from './store.js?v=doubt-1';

export function initializeStoryDialogue({host,onAction,onClose,onDismiss,onScene}={}){
 if(!host)throw Error('Missing story dialogue host.');
 const panel=document.createElement('section');panel.className='story-dialogue';panel.hidden=true;panel.setAttribute('aria-label',T.dialogue);
 panel.innerHTML='<div class="story-dialogue__portrait"><img alt="" width="1254" height="1254">'+Array.from({length:6},()=>'<span class="story-doubt-mark" data-doubt-portrait-mark aria-hidden="true"></span>').join('')+'</div><div class="story-dialogue__body"><h2 id="story-speaker"></h2><p id="story-line" class="story-dialogue__line"></p><p class="story-dialogue__notice" role="status" hidden></p></div><div class="story-dialogue__actions"><button class="story-dialogue__skip"></button><button class="story-dialogue__next" aria-describedby="story-line"></button></div>';
 host.append(panel);
 let current=null,currentId=null,replay=false,previousFocus=null;
 const image=panel.querySelector('img'),portrait=panel.querySelector('.story-dialogue__portrait');
 for(const mark of portrait.querySelectorAll('.story-doubt-mark'))mark.textContent=T.questionMark;
 image.addEventListener('error',()=>{image.hidden=true;panel.classList.add('story-dialogue--no-art');});
 image.addEventListener('load',()=>{image.hidden=false;panel.classList.remove('story-dialogue--no-art');});
 function close({restoreFocus=true}={}){
  panel.hidden=true;current=null;currentId=null;host.classList.remove('has-story-dialogue');onScene?.(null);
  if(restoreFocus){if(previousFocus?.isConnected&&previousFocus.getClientRects().length)previousFocus.focus({preventScroll:true});else onClose?.();}
 }
 function dismiss(){const scene=current,reviewing=replay;close();onDismiss?.(scene,{replay:reviewing});}
 function show(id,{replay:reviewing=false,focus=true}={}){
  const scene=STORY_SCENES[id],actor=scene&&STORY_ACTORS[scene.actorId];if(!actor)return false;
  if(panel.hidden)previousFocus=document.activeElement;
  current=scene;currentId=id;replay=reviewing;panel.dataset.scene=id;panel.dataset.actor=scene.actorId;portrait.dataset.storyActor=scene.actorId;
  panel.querySelector('h2').textContent=actor.name;panel.querySelector('.story-dialogue__line').textContent=scene.text;
  panel.querySelector('.story-dialogue__skip').textContent=scene.dismissLabel||T.skip;
  panel.querySelector('.story-dialogue__next').textContent=scene.nextSceneId?(scene.nextLabel||T.next):replay?T.returnToMap:(scene.nextLabel||T.enter);
  image.hidden=false;image.src=actor.portrait;
  if(!reviewing)storyStore.markSeen(id);
  const notice=panel.querySelector('.story-dialogue__notice');notice.textContent=storyStore.issue==='corrupt'?T.storageCorrupt:storyStore.issue?T.storageUnavailable:'';notice.hidden=!notice.textContent;
  panel.hidden=false;host.classList.add('has-story-dialogue');panel.scrollTop=0;onScene?.(scene);
  if(focus)panel.querySelector('.story-dialogue__next').focus({preventScroll:true});return true;
 }
 panel.querySelector('.story-dialogue__skip').addEventListener('click',dismiss);
 panel.querySelector('.story-dialogue__next').addEventListener('click',()=>{
  if(!current)return;const scene=current,reviewing=replay;
  if(scene.nextSceneId){show(scene.nextSceneId,{replay:reviewing});return;}
  close({restoreFocus:false});onAction?.(scene,{replay:reviewing});
 });
 panel.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();dismiss();}});
 return {show,close,get isOpen(){return !panel.hidden;},get currentSceneId(){return currentId;}};
}
