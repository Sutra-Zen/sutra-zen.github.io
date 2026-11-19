#!/usr/bin/env python3
"""Verify all readers' map/source actions, complete artwork, bands and controls."""
import argparse, functools, hashlib, http.server, io, json, subprocess, threading, urllib.request, urllib.error, zipfile
from pathlib import Path
from urllib.parse import urlsplit, unquote
from lxml import html
from PIL import Image
from playwright.sync_api import sync_playwright

R=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--live',action='store_true');args=parser.parse_args()
O=Path('/workspace/artifacts/reader-navigation-live') if args.live else R/'docs/previews/reader-navigation'
O.mkdir(parents=True,exist_ok=True)
names=[a.get('href').split('/')[1] for a in html.parse(str(R/'index.html')).xpath('//ol[@class="sz-books"]//a[contains(@class,"sz-ready")]')]
legacy=names[:4]
report={'mode':'live HTTPS via TLS-verifying urllib transport' if args.live else 'local HTTP',
        'pageStates':0,'navigationStates':0,'dialogStates':0,'rotationStates':0,'layoutStates':0,
        'errors':[],'httpErrors':[],'publicFiles':{},'books':{},'physicalSafari':'not tested',
        'cdnMode':'Test browser receives existing downloaded Tailwind/Lucide; no CDN availability claim'}
for name in names:
    tree=html.parse(str(R/name/'book/index.html'))
    links=tree.xpath('//div[@class="reading-links"]/a')
    assert [a.text_content() for a in links]==['閱讀原經','回修道地圖']
    assert links[1].get('href')=='../../index.html'
    assert tree.xpath('string(//*[@id="open-verse"])')=='本頁經文'
    assert tree.xpath('//link[contains(@href,"reader-controls.css")]')

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
    def copyfile(self,source,outputfile):
        try:super().copyfile(source,outputfile)
        except (BrokenPipeError,ConnectionResetError):pass
server=None
if args.live:base='https://sutra-zen.github.io/'
else:
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)))
    threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
cache={}
release=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
if args.live:report['mergeCommit']=release
def live_transport(route):
    # Preserve TLS/host verification using the environment's supported HTTPS client.
    url=route.request.url
    if url not in cache:
        fresh=url+('&' if '?' in url else '?')+'release='+release
        try:
            with urllib.request.urlopen(urllib.request.Request(fresh,headers={'User-Agent':'Mozilla/5.0','Cache-Control':'no-cache'}),timeout=40) as response:
                raw=response.read();status=response.status;mime=response.headers.get('Content-Type','application/octet-stream')
        except urllib.error.HTTPError as error:
            if urlsplit(url).path!='/favicon.ico': raise
            route.fulfill(status=error.code,body=error.read(),content_type=error.headers.get('Content-Type','text/plain'));return
        path=unquote(urlsplit(url).path).lstrip('/')
        if not path or path.endswith('/'):path+='index.html'
        assert status==200 and raw==(R/path).read_bytes(),path
        report['publicFiles'][path]={'status':status,'sha256':hashlib.sha256(raw).hexdigest(),'matchesMergedFiles':True}
        cache[url]=(raw,status,mime)
    raw,status,mime=cache[url];route.fulfill(status=status,body=raw,content_type=mime)
def settle(page):
    page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0)')
    page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def geometry(page):
    return page.evaluate('''()=>{const $=s=>document.querySelector(s),r=s=>$(s).getBoundingClientRect().toJSON(),img=$('#art'),a=r('#art'),scale=Math.min(a.width/img.naturalWidth,a.height/img.naturalHeight);return {
      picture:img.checkVisibility()?{x:a.x+(a.width-img.naturalWidth*scale)/2,y:a.y+(a.height-img.naturalHeight*scale)/2,width:img.naturalWidth*scale,height:img.naturalHeight*scale}:null,
      caption:$('#caption').checkVisibility()?r('#caption'):null,verse:$('.scripture').checkVisibility()?r('.verse-body'):null,band:$('.scripture').checkVisibility()?r('.scripture'):null,
      links:r('.reading-links'),classes:$('.page').className,fit:getComputedStyle(img).objectFit,
      overflow:document.documentElement.scrollWidth>innerWidth,ratio:img.naturalWidth/img.naturalHeight}}''')
def overlap(a,b):return min(a['x']+a['width'],b['x']+b['width'])-max(a['x'],b['x'])>1 and min(a['y']+a['height'],b['y']+b['height'])-max(a['y'],b['y'])>1

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    sizes=[(360,800),(800,360),(768,1024),(1024,768),(1440,900)] if not args.live else [(360,800),(1024,768)]
    for w,h in sizes:
        page=browser.new_page(viewport={'width':w,'height':h},has_touch=True)
        page.on('pageerror',lambda e:report['errors'].append(str(e)))
        page.on('response',lambda r:report['httpErrors'].append([r.status,r.url]) if r.url.startswith(base) and r.status>=400 and not r.url.endswith('favicon.ico') else None)
        page.route('https://www.youtube.com/**',lambda r:r.abort())
        page.route('https://cdn.tailwindcss.com/**',lambda r:r.fulfill(content_type='application/javascript',body=Path('/tmp/tailwind-site.js').read_bytes()))
        page.route('https://unpkg.com/**',lambda r:r.fulfill(content_type='application/javascript',body=Path('/tmp/migration-lucide.min.js').read_bytes()))
        if args.live:page.route(base+'**',live_transport)
        for name in names:
            page.goto(base+name+'/book/');page.wait_for_function('typeof showPage==="function"')
            n=page.evaluate('pages.length');report['books'][name]={'pageItems':n}
            indices=list(range(n)) if name in legacy and w>h and not args.live else sorted(set([0,1,n//2,n-2,n-1]))
            dialog=False
            for i in indices:
                page.evaluate('i=>showPage(i)',i);settle(page)
                g=geometry(page)
                try:
                    assert not g['overflow'],g
                    assert page.locator('.reading-links a').all_text_contents()==['閱讀原經','回修道地圖']
                    if g['picture'] and 'text-scene' not in g['classes'] and 'afterword-scene' not in g['classes']:
                        assert g['fit']=='contain'
                        if g['caption']:assert g['picture']['y']>=g['caption']['bottom']-1,g
                        if g['band']:assert g['picture']['y']+g['picture']['height']<=g['band']['y']+1,g
                        if w>h and g['verse']:assert not overlap(g['verse'],g['links']),g
                        report['layoutStates']+=1
                except AssertionError:
                    page.screenshot(path=str(O/f'failure-{name}-{i}-{w}x{h}.png'));raise
                report['pageStates']+=1
                if not dialog and page.locator('#open-verse').is_visible():
                    page.locator('#open-verse').click();assert page.locator('#verse-dialog').is_visible()
                    assert page.locator('#dialog-verse').inner_text().strip()
                    page.locator('#verse-dialog form button').click();dialog=True;report['dialogStates']+=1
            # Restart and the same map/source pair must remain available at the end.
            if name=='seven-factors':page.evaluate('showPage(pages.length-1,pages[pages.length-1].cues.length)')
            else:page.evaluate('showPage(pages.length-1)')
            settle(page);assert '回到第一頁' in page.locator('#next').inner_text(),name
            page.locator('#next').click();assert page.locator('#position-text').inner_text().lstrip().startswith('1 /'),name
            page.locator('#next').tap();position=page.locator('#position-text').inner_text();page.locator('#previous').tap()
            assert page.locator('#position-text').inner_text().lstrip().startswith('1 /')
            assert page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction')=='manipulation'
            assert page.evaluate('visualViewport.scale')==1
            page.locator('#next').tap();assert page.locator('#position-text').inner_text()==position
            page.set_viewport_size({'width':h,'height':w});settle(page)
            assert page.locator('#position-text').inner_text()==position;report['rotationStates']+=1
            page.set_viewport_size({'width':w,'height':h});settle(page)
            if not args.live and name in legacy+['seven-factors'] and (w,h) in [(768,1024),(1024,768)]:
                Image.open(io.BytesIO(page.screenshot())).save(O/f'{name}-{w}x{h}.webp',lossless=True,method=6)
            page.locator('.reading-links a').first.click()
            page.wait_for_url(lambda u: bool(urlsplit(u).fragment) and '/book/' not in urlsplit(u).path)
            assert page.locator('[id="'+unquote(urlsplit(page.url).fragment)+'"]').count()>0
            page.go_back();page.wait_for_function('typeof showPage==="function"');settle(page)
            maplink=page.locator('.reading-links a[href="../../index.html"]');maplink.click()
            page.wait_for_selector('.sz-books .sz-ready');assert page.locator('.sz-books .sz-ready').count()==14
            assert urlsplit(page.url).path in ['/','/index.html'];report['navigationStates']+=1
            print(w,h,name,'passed',flush=True)
        page.close()
    browser.close()
if server:server.shutdown()
assert not report['errors'] and not report['httpErrors'],report
(O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['publicFiles','books']},ensure_ascii=False),flush=True)
