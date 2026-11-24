from pathlib import Path
import functools,http.server,importlib.util,json,threading
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit',root/'scripts/audit-reader-caption-scripture.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
rows=json.loads((a.OUT/'pages.json').read_text());by={(r['book'],r['page']):r for r in rows};result={'scope':'Fourteen game review readers, three native consecutive steps each; all-completed disposable fixtures only. No completion action.','checks':[],'javascriptErrors':[],'httpErrors':[]}
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(a.Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for b in a.ORDER:
   index=next(r['page']-1 for r in rows if r['book']==b and r['scripture'] and r['openDialog']);fixture={'version':1,'completed':a.ORDER,'positions':{b:index},'activeBook':'four-truths'}
   ctx=browser.new_context(viewport={'width':1280,'height':900},reduced_motion='reduce',storage_state={'cookies':[],'origins':[{'origin':base.rstrip('/'),'localStorage':[{'name':'sutrazen.play.collection.v1','value':json.dumps(fixture)}]}]});pg=ctx.new_page();pg.on('pageerror',lambda e:result['javascriptErrors'].append(str(e)));pg.on('response',lambda r:result['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
   pg.goto(base+b+'/book/?collection=1&collectionReturn=game&collectionReview=1&collectionPage='+str(index)+'&collectionStory=dark-heart-1');pg.wait_for_function('(id)=>document.body.dataset.collectionBook===id&&!!window.SutraZenCollectionBridge',arg=b)
   trace=[]
   for i in range(index,min(index+3,by[(b,1)]['total'])):
    pg.evaluate('()=>new Promise(requestAnimationFrame)');r=pg.evaluate(a.EXTRACT,b);expected=by[(b,i+1)];assert r['page']==i+1,(b,r['page'],i+1)
    for k in ['caption','scripture','sourceHref','sourceHidden']:assert r[k]==expected[k],(b,i,k)
    trace.append(i+1)
    if i<index+2:pg.locator('#next').click()
   saved=pg.evaluate('JSON.parse(localStorage.getItem("sutrazen.play.collection.v1"))');assert saved['completed']==a.ORDER and saved['activeBook']=='four-truths'
   result['checks'].append({'book':b,'nativePages':trace,'contentExactPublicMatch':True,'completedAndActiveUnchanged':True});ctx.close();print(b,trace,'game content equals public',flush=True)
  browser.close()
 result['result']='passed';assert not result['javascriptErrors'] and not result['httpErrors']
finally:
 server.shutdown();(a.OUT/'game-runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
