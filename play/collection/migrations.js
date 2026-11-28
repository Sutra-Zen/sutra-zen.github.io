// Pagination metadata only. This module has no storage or DOM side effects.
import {CATALOG_IDS} from './catalog.js?v=summary-merge-1';

export const CURRENT_POSITIONS_REVISION=2;
export const EIGHTFOLD_BOOK_ID='eightfold-path';
export const EIGHTFOLD_CURRENT_STEPS=110;

// Public readers can use this same zero-based mapping when importing their
// legacy numeric session key into a new revision key. Do not clamp unknown
// positions into the last page: that could turn bad data into a finish step.
export function migrateEightfoldIndex(index,fromRevision=1){
  if(fromRevision===1){
    if(index===109)return 108;
    if(index===110)return 109;
  }
  return index;
}

// Keep the existing v1 envelope readable by older clients. Only the absent
// marker denotes legacy pagination; every returned/exported state has marker2.
// An older client may strip the optional marker. Re-import then conservatively
// returns its old109 bookmark to the summary, while retaining all completions.
export function validateCollectionState(raw){
  const known=id=>CATALOG_IDS.includes(id);
  if(!raw||raw.version!==1||!known(raw.activeBook)||!Array.isArray(raw.completed)||
    raw.completed.some(id=>!known(id))||!raw.positions||typeof raw.positions!=='object'||Array.isArray(raw.positions))throw Error('collection');
  const hasRevision=Object.hasOwn(raw,'positionsRevision');
  if(hasRevision&&raw.positionsRevision!==CURRENT_POSITIONS_REVISION)throw Error('positions-revision');
  const positions={};
  for(const [id,index] of Object.entries(raw.positions)){
    if(!known(id)||!Number.isInteger(index)||index<0||index>10000)throw Error('position');
    positions[id]=id===EIGHTFOLD_BOOK_ID&&!hasRevision?migrateEightfoldIndex(index):index;
  }
  return {version:1,positionsRevision:CURRENT_POSITIONS_REVISION,positions,
    completed:[...new Set(raw.completed)],activeBook:raw.activeBook};
}
