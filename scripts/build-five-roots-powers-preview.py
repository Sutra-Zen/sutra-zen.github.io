#!/usr/bin/env python3
"""Produce a complete selectable-text review PDF without publishing the new book."""
import functools,hashlib,html,http.server,io,json,re,shutil,subprocess,tempfile,threading
from pathlib import Path
import fitz
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];D=R/'docs/five-roots-powers';O=R/'docs/previews/five-roots-powers';O.mkdir(parents=True,exist_ok=True)
story=json.loads((D/'storyboard.json').read_text());cat=json.loads((D/'scripture-catalog.json').read_text());plan=json.loads((D/'reader-plan.json').read_text());labels=json.loads((D/'overlay-layout.json').read_text())['overlays'];book=json.loads((R/'five-roots-powers/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'));e=html.escape
STYLE='''@page{size:A4;margin:15mm}*{box-sizing:border-box;print-color-adjust:exact}body{font-family:"Noto Sans CJK TC","Noto Sans TC",sans-serif;font-size:12pt;line-height:1.75;color:#24372e}h1{font-size:24pt}h2{font-size:19pt}h3{font-size:14pt}h1,h2,h3{break-after:avoid}p{margin:6pt 0}.scene{break-before:page}.art{position:relative;container-type:inline-size;break-inside:avoid}.art img{display:block;width:100%;height:auto}.label{position:absolute;text-align:left;font-weight:700;line-height:1.15;white-space:nowrap;color:#000;text-shadow:0 1px 2px #fff8}.paragraph{break-inside:avoid;margin:14pt 0}.meta{font-size:9pt;color:#637166}blockquote{margin:10pt 0;padding-left:12pt;border-left:2px solid #adb9a8;white-space:pre-line;overflow-wrap:anywhere}'''
def document():
 body=['<h1>五根五力｜完整內容試閱</h1><p>十幕、74段原口白及全部各幕引文。時間為字幕取樣的秒級近似值，未逐字聽校音軌。本PDF供內容校閱，網頁翻頁、讀經、放大及橫直操作另經驗證。</p>']
 n=0
 for s in story:
  sid=s['scene'][:3];body.append('<section class="scene"><h2>'+e(s['scene'])+'</h2><div class="art"><img src="/five-roots-powers/assets/'+sid+'.webp">')
  for o in labels[sid]:body.append(f'<div class="label" style="left:{o["x"]}%;top:{o["y"]}%;width:{o["width"]}%;font-size:{o["fontSizeCqw"]}cqw">'+e(o['text'])+'</div>')
  body.append('</div><h3>完整口白</h3>')
  for cue in s['cues']:
   n+=1;body.append(f'<div class="paragraph"><p class="meta">P{n:03} · {cue["start"]}–{cue["end"]}</p><p>'+e(cue['text'])+'</p></div>')
  for qid in dict.fromkeys(q for p in plan[sid] for q in p['quoteIds']):
   q=cat[qid];body.append('<h3>'+e(q['source'])+'</h3><blockquote>'+e(q['text'])+'</blockquote>')
  if sid=='S02':body.append('<p>'+e(s['scripture'])+'</p>')
  body.append('</section>')
 body.append('<section class="scene"><h2>片尾經典出處</h2><div class="art"><img src="/five-roots-powers/assets/sources.png"></div></section><section class="scene"><h2>經典依據</h2>')
 for text in book['pages'][-1]['textSummary'][0]['paragraphs']:body.append('<p>'+e(text)+'</p>')
 return '<!doctype html><html lang="zh-Hant-TW"><meta charset="utf-8"><style>'+STYLE+'</style><body>'+''.join(body)+'</body></html>'
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if self.path=='/review.html':
   raw=document().encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(raw)
  else:super().do_GET()
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(R)));threading.Thread(target=s.serve_forever,daemon=True).start();dest=O/'Five-Roots-Powers-review.pdf'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();page.goto(f'http://127.0.0.1:{s.server_port}/review.html');page.evaluate('()=>document.fonts.ready');page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)');assert page.locator('img').count()==11 and page.locator('.label').count()==5;page.pdf(path=str(dest),format='A4',print_background=True);b.close()
s.shutdown()
with tempfile.TemporaryDirectory(prefix='roots-pdf-') as tmp:
 raw=Path(tmp)/'full.pdf';shutil.copyfile(dest,raw);pdf=fitz.open(raw);seen=set()
 for page in pdf:
  for row in page.get_images():
   xref=row[0]
   if xref in seen:continue
   seen.add(xref);im=pdf.extract_image(xref);buf=io.BytesIO();Image.open(io.BytesIO(im['image'])).convert('RGB').save(buf,'JPEG',quality=92,optimize=True);page.replace_image(xref,stream=buf.getvalue())
 pdf.save(dest,garbage=4,deflate=True);pdf.close()
text=re.sub(r'\s+','',subprocess.check_output(['pdftotext','-layout',str(dest),'-'],text=True))
for s in story:
 for c in s['cues']:assert re.sub(r'\s+','',c['text']) in text,c['text']
for q in cat.values():assert re.sub(r'\s+','',q['text']) in text,q['quoteId']
with fitz.open(dest) as pdf:report={'pages':len(pdf),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'all74Narrations':'retained','all14QuoteCards':'retained','images':11,'overlays':5}
(O/'pdf-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False),flush=True)
