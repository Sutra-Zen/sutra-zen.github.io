import {routeOrder} from '../../route/data.js';
import {isFinalGameBookRevealed} from '../../route/eligibility.js';
import {MODULES,MODULE_IDS,MODULE_BY_ID,THOUGHT_IDS,BASE_PLINTH} from './catalog.js';
import {MODULE_UI} from './text.js';

// This store owns arrangement and presentation flags only. It does not import
// the collection store, change completed books, or grant reading eligibility.
export const CITY_STORAGE_KEY='sutrazen.play.city.v1';
export const CITY_SESSION_KEY='sutrazen.play.city.session.v1';
export const CITY_LAYOUT_EVENT='sutrazen:city-layout';
const fresh=()=>({version:1,placedIds:[],thoughtSeenIds:[]});
const clone=value=>JSON.parse(JSON.stringify(value));
// Public backup contract: object or JSON string -> sanitized city-v1 object;
// invalid values throw before any persistence or event. No reading data enters.
export function validateCityBackup(value){
  const raw=typeof value==='string'?JSON.parse(value):value;
  if(!raw||typeof raw!=='object'||Array.isArray(raw)||raw.version!==1||
    !Array.isArray(raw.placedIds)||!Array.isArray(raw.thoughtSeenIds)||
    raw.placedIds.some(id=>!MODULE_IDS.includes(id))||raw.thoughtSeenIds.some(id=>!THOUGHT_IDS.includes(id))||
    Object.hasOwn(raw,'completed')||Object.hasOwn(raw,'positions')||Object.hasOwn(raw,'completedBookIds'))throw Error('city-schema');
  return {version:1,placedIds:[...new Set(raw.placedIds)],thoughtSeenIds:[...new Set(raw.thoughtSeenIds)]};
}
const bookSet=completed=>new Set((completed instanceof Set?[...completed]:Array.isArray(completed)?completed:[]).filter(id=>routeOrder.includes(id)));
export function deriveCityModules(saved,completed){
  const state=validateCityBackup(saved),done=bookSet(completed),baseVisible=done.has(BASE_PLINTH.requiredBookId),savedPlaced=new Set(state.placedIds),effective=new Set();
  // The catalog is dependency ordered. No missing prerequisite is inserted.
  for(const module of MODULES){
    if(baseVisible&&savedPlaced.has(module.id)&&module.requiredBookIds.every(id=>done.has(id))&&module.requires.every(id=>effective.has(id)))effective.add(module.id);
  }
  const modules=MODULES.map(module=>{
    const unlocked=done.has(module.bookId),missingBookIds=[...new Set([...(baseVisible?[]:[BASE_PLINTH.requiredBookId]),...module.requiredBookIds.filter(id=>!done.has(id))])],missingModuleIds=module.requires.filter(id=>!effective.has(id));
    const placed=effective.has(module.id),available=unlocked&&!missingBookIds.length&&!missingModuleIds.length;
    const revealed=module.bookId!=='four-fruits-ten-fetters'||isFinalGameBookRevealed(done);
    return {...module,revealed,title:revealed?module.title:MODULE_UI.unrevealedTitle,displayTitle:revealed?module.title:MODULE_UI.unrevealedTitle,
      description:revealed?module.description:MODULE_UI.unrevealedDescription,inventoryAssetKey:revealed?module.inventoryAssetKey:null,
      unlocked,earned:unlocked,available,canPlace:available&&!placed,placed,savedPlaced:savedPlaced.has(module.id),
      missingBookIds,missingModuleIds,status:placed?'placed':!unlocked?'locked':available?'available':'waiting',
      slots:module.slots.map(slot=>({...slot,available:placed&&(!slot.requires||slot.requires.every(id=>effective.has(id))),visible:placed&&(!slot.requires||slot.requires.every(id=>effective.has(id)))})),
    };
  });
  return {version:1,completed:routeOrder.filter(id=>done.has(id)),placedIds:MODULE_IDS.filter(id=>effective.has(id)),savedPlacedIds:[...state.placedIds],thoughtSeenIds:[...state.thoughtSeenIds],baseVisible,
    base:{...BASE_PLINTH,visible:baseVisible,slots:BASE_PLINTH.slots.map(slot=>({...slot,visible:baseVisible,available:baseVisible}))},modules,inventory:modules};
}

// get(completed) derives ownership from a read-only caller snapshot; it never
// auto-places. canPlace is boolean. Mutation methods return a result object:
// {ok,changed,placedIds,placedNow,issue,persistence,reason?}. `ok` in memory
// means the current document changed, not that a permanent write succeeded.
// exportBackup returns JSON; restoreBackup accepts a validated object or JSON.
export function createCityStore(storage,session,eventTarget=globalThis.window){
  if(storage===undefined){try{storage=globalThis.localStorage;}catch{storage=null;}}
  if(session===undefined){try{session=globalThis.sessionStorage;}catch{session=null;}}
  let state=fresh(),issue=null,persistence='local',localRaw=null,localReadable=true;
  try{if(!storage)throw Error('unavailable');localRaw=storage.getItem(CITY_STORAGE_KEY);if(localRaw){try{state=validateCityBackup(localRaw);}catch{issue='corrupt';}}}
  catch{localReadable=false;issue='unavailable';persistence='memory';}
  try{
    const raw=session?.getItem(CITY_SESSION_KEY),record=raw&&JSON.parse(raw);
    if(record&&record.version===1&&(record.baseRaw===null||typeof record.baseRaw==='string')){
      if(!localReadable||record.baseRaw===localRaw){state=validateCityBackup(record.state);issue='unavailable';persistence='session';if(!localReadable)localRaw=record.baseRaw;}
      else session?.removeItem(CITY_SESSION_KEY);
    }
  }catch{}
  const announce=()=>{if(typeof eventTarget?.dispatchEvent==='function'&&typeof CustomEvent!=='undefined')eventTarget.dispatchEvent(new CustomEvent(CITY_LAYOUT_EVENT,{detail:{issue,persistence}}));};
  function saveRecovery(){
    try{if(!session)throw Error('unavailable');session.setItem(CITY_SESSION_KEY,JSON.stringify({version:1,baseRaw:localRaw,state}));persistence='session';return true;}
    catch{persistence='memory';return false;}
  }
  function persist(){
    try{
      if(!storage)throw Error('unavailable');const raw=JSON.stringify(state);storage.setItem(CITY_STORAGE_KEY,raw);localRaw=raw;issue=null;persistence='local';
      try{session?.removeItem(CITY_SESSION_KEY);}catch{
        // Canonical data wins after a successful write. Keep recovery aligned
        // if removal is denied so a null/unchanged base cannot revive old data.
        try{session?.setItem(CITY_SESSION_KEY,JSON.stringify({version:1,baseRaw:localRaw,state}));}
        catch{issue='unavailable';persistence='memory';}
      }
    }catch{issue='unavailable';saveRecovery();}
    announce();
  }
  const result=(ok,{changed=false,placedNow=[],reason}={})=>({ok,changed,placedIds:[...state.placedIds],placedNow,issue,persistence,...(reason?{reason}:{})});
  const get=completed=>({...deriveCityModules(state,completed),issue,persistence});
  const canPlace=(id,completed)=>Boolean(get(completed).modules.find(module=>module.id===id)?.canPlace);
  const api={
    get,get issue(){return issue;},get persistence(){return persistence;},canPlace,
    place(id,completed){
      if(!Object.hasOwn(MODULE_BY_ID,id))return result(false,{reason:'unknown-module'});
      const module=get(completed).modules.find(module=>module.id===id);
      if(module.placed)return result(true,{reason:'already-placed'});
      if(!module.canPlace)return result(false,{reason:!module.unlocked?'locked':module.missingBookIds.length?'missing-books':'missing-modules'});
      state.placedIds=[...new Set([...state.placedIds,id])];persist();return result(true,{changed:true,placedNow:[id]});
    },
    placeAll(completed){
      const placedNow=[];
      // Re-evaluate after each placement; each unlocked module can satisfy the
      // next module's placement prerequisite without inventing a book finish.
      for(const module of MODULES){if(canPlace(module.id,completed)){state.placedIds=[...new Set([...state.placedIds,module.id])];placedNow.push(module.id);}}
      if(placedNow.length)persist();return result(true,{changed:Boolean(placedNow.length),placedNow,...(!placedNow.length?{reason:'nothing-placeable'}:{})});
    },
    markThoughtSeen(id){
      if(!THOUGHT_IDS.includes(id))return result(false,{reason:'unknown-thought'});
      if(state.thoughtSeenIds.includes(id))return result(true,{reason:'already-seen'});
      state.thoughtSeenIds.push(id);persist();return result(true,{changed:true});
    },
    reset(){
      state=fresh();issue=null;let localReset=false,sessionReset=true;
      try{if(!storage)throw Error('unavailable');storage.removeItem(CITY_STORAGE_KEY);localRaw=null;localReset=true;}
      catch{issue='unavailable';}
      try{if(!session)throw Error('unavailable');session.removeItem(CITY_SESSION_KEY);}
      catch{sessionReset=false;issue='unavailable';}
      persistence=localReset?'local':'memory';
      if(!localReset||!sessionReset)saveRecovery();
      announce();return result(true,{changed:true});
    },
    exportBackup:()=>JSON.stringify(state,null,2),
    restoreBackup(value){
      let restored;try{restored=validateCityBackup(value);}catch{return result(false,{reason:'invalid-backup'});}
      const changed=JSON.stringify(restored)!==JSON.stringify(state);state=restored;persist();return result(true,{changed});
    },
  };
  if(typeof eventTarget?.addEventListener==='function')eventTarget.addEventListener('storage',event=>{
    if(event.key!==CITY_STORAGE_KEY)return;
    try{
      state=event.newValue?validateCityBackup(event.newValue):fresh();localRaw=event.newValue;issue=null;persistence='local';
      try{session?.removeItem(CITY_SESSION_KEY);}catch{
        // An external reset/restore is authoritative. If recovery cannot be
        // removed, replace it at the new canonical boundary, never merge it.
        try{if(!session)throw Error('unavailable');session.setItem(CITY_SESSION_KEY,JSON.stringify({version:1,baseRaw:localRaw,state}));}
        catch{issue='unavailable';persistence='memory';}
      }
    }
    catch{issue='corrupt';}
    announce();
  });
  return api;
}
export const cityStore=createCityStore();
