#!/usr/bin/env python3
"""Check paragraph-to-panel mapping and actual dark/clear pixels in both comic layouts."""
import functools,http.server,io,json,subprocess,threading
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/right-effort-focus'
BASE='3d9830eb65877547e6c272eb8466a816411e0baa'
EXPECTED={'S03':[None,None,'tl','tr','bl','br',None,None],'S07':[None,'tl','tm','tm','tr','bl','bl','bm','br']}
BOOK=json.loads((ROOT/'right-effort/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'))
old_book=json.loads(subprocess.check_output(['git','show',BASE+':right-effort/book/book-data.js'],cwd=ROOT).decode().split('const BOOK = ')[1].rstrip(';\n'))
old_book['layout']='caption-art-scripture'
assert BOOK==old_book
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def settle(page):
 page.wait_for_function('document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0')
 page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def geometry(page,selector):return page.locator(selector).evaluate('e=>e.getBoundingClientRect().toJSON()')
def check_frame(page,frame,mask):
 a=geometry(page,frame);b=geometry(page,mask)
 for key in ['x','y','width','height']:assert abs(a[key]-b[key])<1,(frame,key,a,b)
def main():
 OUT.mkdir(parents=True,exist_ok=True);server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/right-effort/book/'
 report={'baseline':BASE,'viewports':[],'pageStates':0,'javascriptErrors':[],'physicalIPadSafari':'not tested','opacity':.76}
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for w,h in [(360,800),(800,360),(768,1024),(1024,768)]:
   page=b.new_page(viewport={'width':w,'height':h},has_touch=True);page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)));page.goto(url);page.wait_for_function('typeof showPage==="function"')
   for scene,mapping in EXPECTED.items():
    start=next(s['start'] for s in BOOK['scenes'] if s['id']==scene)
    page.evaluate('i=>showPage(i)',start);settle(page)
    original=Image.open(io.BytesIO(page.screenshot())).convert('RGB')
    panels=page.evaluate('s=>PANEL_FOCUS.scenes[s].panels',scene)
    for local,expected in enumerate(mapping):
     page.evaluate('i=>showPage(i)',start+local);settle(page)
     mask=page.locator('#art-frame .picture-panel-focus')
     assert mask.evaluate('e=>e.hidden')==(expected is None)
     if expected:
      assert mask.get_attribute('data-active-panel')==expected
      assert mask.locator('span.active').count()==1 and mask.locator('span:not(.active)').count()==len(panels)-1
      check_frame(page,'#art-frame','#art-frame .picture-panel-focus')
      rect=geometry(page,'#art-frame');current=Image.open(io.BytesIO(page.screenshot())).convert('RGB')
      for panel in panels:
       point=(round(rect['x']+rect['width']*(panel['x']+panel['width']/2)/100),round(rect['y']+rect['height']*(panel['y']+panel['height']/2)/100))
       before=original.getpixel(point);after=current.getpixel(point)
       want=before if panel['id']==expected else tuple(round(.24*v+.76*c) for v,c in zip(before,(5,12,20)))
       assert all(abs(a-e)<=2 for a,e in zip(after,want)),(scene,local,panel['id'],before,after,want)
      if (w,h) in [(768,1024),(1024,768)]:
       current.save(OUT/f'{scene}-{expected}-{w}x{h}.webp',lossless=True,method=6)
     report['pageStates']+=1
    # Next and previous pages update the highlighted cell; rotation and zoom keep it aligned.
    page.evaluate('i=>showPage(i)',start+2);settle(page);before=page.locator('#position-text').inner_text();page.locator('#next').tap();page.locator('#previous').tap();assert page.locator('#position-text').inner_text()==before
    active=mapping[2];page.set_viewport_size({'width':h,'height':w});settle(page)
    assert page.locator('#art-frame .picture-panel-focus').get_attribute('data-active-panel')==active
    check_frame(page,'#art-frame','#art-frame .picture-panel-focus');page.set_viewport_size({'width':w,'height':h});settle(page)
    page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete && document.querySelector("#zoom-art").naturalWidth>0');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
    assert page.locator('#zoom-frame .picture-panel-focus').get_attribute('data-active-panel')==active
    check_frame(page,'#zoom-frame','#zoom-frame .picture-panel-focus');page.locator('#image-dialog form button').click()
   page.select_option('#page-select','S10');settle(page);assert page.locator('#art-frame .picture-panel-focus').evaluate('e=>e.hidden')
   assert page.locator('#closing-shade').evaluate('e=>!e.hidden && getComputedStyle(e).opacity==="0.6"')
   page.select_option('#page-select','S11');assert page.locator('#art-frame .picture-panel-focus').evaluate('e=>e.hidden');page.locator('#next').tap();settle(page);assert page.locator('#position-text').inner_text()=='1 / 81 頁'
   assert page.locator('#art-frame .picture-panel-focus').evaluate('e=>e.hidden');page.close();report['viewports'].append({'width':w,'height':h,'comicParagraphs':17,'pixelDimming':'passed','rotationZoomNavigation':'passed'});print(f'{w}x{h}: 17 comic paragraph states; exact bright/dark pixels, zoom and rotation passed',flush=True)
  b.close()
 server.shutdown();assert not report['javascriptErrors'];(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
