import {STORY_SCENES} from './data.js?v=character-pronouns-1';

// A presentation checkpoint only; it never grants reading/completion rights.
export const STORY_PENDING_KEY='sutrazen.play.story-pending.v1';
export const STORY_PENDING_SESSION_KEY='sutrazen.play.story-pending.session.v1';
function validate(value){
 if(value===null)return null;
 const scene=value&&STORY_SCENES[value.sceneId];
 if(value?.version!==1||!scene||scene.group==='train-opening'||![null,'first-completion'].includes(value.context)||
   (value.context==='first-completion'&&scene.group!=='first-completion'&&value.sceneId!=='toward-aggregates-lake'))throw Error('checkpoint');
 return {version:1,sceneId:value.sceneId,context:value.context};
}
export function createPendingStoryStore(storage,session){
 let state=null,localRaw=null,readable=true,issue=null;
 if(storage===undefined){try{storage=globalThis.localStorage;}catch{storage=null;}}
 if(session===undefined){try{session=globalThis.sessionStorage;}catch{session=null;}}
 try{if(!storage)throw Error('unavailable');localRaw=storage.getItem(STORY_PENDING_KEY);if(localRaw)state=validate(JSON.parse(localRaw));}catch{readable=false;issue='unavailable';}
 try{
  const raw=session?.getItem(STORY_PENDING_SESSION_KEY),recovery=raw&&JSON.parse(raw);
  if(recovery?.version===1&&(recovery.baseRaw===null||typeof recovery.baseRaw==='string')){
   if(!readable||recovery.baseRaw===localRaw){state=validate(recovery.state);issue='unavailable';if(!readable)localRaw=recovery.baseRaw;}
   else session?.removeItem(STORY_PENDING_SESSION_KEY);
  }
 }catch{}
 function write(value){
  state=value;
  try{
   if(!storage)throw Error('unavailable');
   const raw=state?JSON.stringify(state):null;
   if(raw)storage.setItem(STORY_PENDING_KEY,raw);else storage.removeItem(STORY_PENDING_KEY);
   localRaw=raw;issue=null;session?.removeItem(STORY_PENDING_SESSION_KEY);
  }catch{
   issue='unavailable';
   try{session?.setItem(STORY_PENDING_SESSION_KEY,JSON.stringify({version:1,baseRaw:localRaw,state}));}catch{}
  }
 }
 return {get:()=>state?{...state}:null,get issue(){return issue;},set(sceneId,context=null){let value;try{value=validate({version:1,sceneId,context});}catch{return false;}write(value);return true;},clear(){write(null);}};
}
export const pendingStory=createPendingStoryStore();
