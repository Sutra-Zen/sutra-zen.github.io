// Coordinate game-only reading and city layout without changing reader policy.
import {store,SESSION_FALLBACK_KEY} from './collection/store.js';
import {CATALOG_IDS} from './collection/catalog.js';
import {cityStore,validateCityBackup} from './city/modules/store.js?v=auto-city-1';
import {routeMetadata} from './route/metadata.js';
import {storyStore} from './story/store.js?v=mandatory-dialogue-1';
import {pendingStory} from './story/pending.js?v=mandatory-dialogue-1';
import {clearFirstCompletionReceipt} from './story/completion-receipt.js?v=doubt-1';

export const JOURNEY_BACKUP_FORMAT='sutrazen.journey';
export const JOURNEY_BACKUP_VERSION=2;
const known=id=>CATALOG_IDS.includes(id);
function validateCollection(raw){
 if(!raw||raw.version!==1||!known(raw.activeBook)||!Array.isArray(raw.completed)||raw.completed.some(id=>!known(id))||!raw.positions||typeof raw.positions!=='object'||Array.isArray(raw.positions))throw Error('collection');
 for(const [id,index] of Object.entries(raw.positions))if(!known(id)||!Number.isInteger(index)||index<0||index>10000)throw Error('position');
 return {version:1,positions:{...raw.positions},completed:[...new Set(raw.completed)],activeBook:raw.activeBook};
}
export function validateJourneyBackup(input){
 const raw=typeof input==='string'?JSON.parse(input):input;
 if(raw?.format===JOURNEY_BACKUP_FORMAT){
  if(raw.version!==JOURNEY_BACKUP_VERSION)throw Error('version');
  return {collection:validateCollection(raw.collection),city:validateCityBackup(raw.city),legacy:false};
 }
 return {collection:validateCollection(raw),city:null,legacy:true};
}
export function exportJourneyBackup(){
 return JSON.stringify({format:JOURNEY_BACKUP_FORMAT,version:JOURNEY_BACKUP_VERSION,collection:store.get(),city:JSON.parse(cityStore.exportBackup())},null,2);
}
function clearPresentation(){
 const failures=[];routeMetadata.reset();storyStore.reset();pendingStory.clear();
 if(!clearFirstCompletionReceipt())failures.push('first-completion-receipt');
 for(const key of ['sutrazen.play.camera.v1','sutrazen.play.city.camera.v1','sutrazen.play.map-tip.v1']){
  try{sessionStorage.removeItem(key);}catch{failures.push(key);}
 }
 return failures;
}
const announce=reason=>window.dispatchEvent(new CustomEvent('sutrazen:journey-state',{detail:{reason}}));
export function restoreJourneyBackup(input){
 let validated;try{validated=validateJourneyBackup(input);}catch{return {ok:false,reason:'invalid'};}
 // Every section is validated before the first mutation. Legacy backups contain
 // no layout: never carry another save's city into the restored reading profile.
 if(!store.restoreBackup(JSON.stringify(validated.collection)))return {ok:false,reason:'invalid'};
 const cityResult=validated.legacy?cityStore.reset():cityStore.restoreBackup(validated.city);
 const failures=clearPresentation();announce('restore');
 return {ok:cityResult.ok,persistent:!store.issue&&!cityStore.issue&&!routeMetadata.issue&&!storyStore.issue&&!pendingStory.issue&&!failures.length,legacy:validated.legacy};
}
export function resetJourney(){
 const failures=[];store.reset();
 // Keep the existing defence against cached reader-store session cleanup.
 if(!store.issue){try{sessionStorage.removeItem(SESSION_FALLBACK_KEY);}catch{failures.push(SESSION_FALLBACK_KEY);try{sessionStorage.setItem(SESSION_FALLBACK_KEY,JSON.stringify({version:1,baseRaw:null,state:store.get()}));}catch{}}}
 cityStore.reset();failures.push(...clearPresentation());announce('reset');
 return {persistent:!store.issue&&!cityStore.issue&&!routeMetadata.issue&&!storyStore.issue&&!pendingStory.issue&&!failures.length};
}
