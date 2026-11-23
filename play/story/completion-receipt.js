// A presentation-only handoff, not a second completion/eligibility store.
// Issued only after the reader's existing explicit mainline finish succeeds.
export const FIRST_COMPLETION_RECEIPT_KEY='sutrazen.play.story-first-completion.v1';
const valid=value=>value?.version===1&&value?.event==='four-truths-reader-finished';
export function issueFirstCompletionReceipt(){
 const raw=JSON.stringify({version:1,event:'four-truths-reader-finished'});
 for(const name of ['sessionStorage','localStorage']){
  try{globalThis[name].setItem(FIRST_COMPLETION_RECEIPT_KEY,raw);return true;}catch{}
 }
 return false;
}
export function clearFirstCompletionReceipt(){
 let cleared=true;
 for(const name of ['sessionStorage','localStorage']){
  try{globalThis[name].removeItem(FIRST_COMPLETION_RECEIPT_KEY);}catch{cleared=false;}
 }
 return cleared;
}
export function consumeFirstCompletionReceipt(){
 let found=false;
 for(const name of ['sessionStorage','localStorage']){
  try{const raw=globalThis[name].getItem(FIRST_COMPLETION_RECEIPT_KEY);if(raw&&valid(JSON.parse(raw)))found=true;}catch{}
 }
 clearFirstCompletionReceipt();return found;
}
