#!/usr/bin/env python3
"""A twelve-page PDF: original art and every timed narration/scripture pair."""
import functools,hashlib,html,http.server,io,json,re,shutil,subprocess,tempfile,threading
from pathlib import Path
import fitz
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];D=R/'docs/seven-factors';O=R/'docs/previews/seven-factors';O.mkdir(parents=True,exist_ok=True);STORY=json.loads((D/'storyboard.json').read_text());CAT=json.loads((D/'scripture-catalog.json').read_text());e=html.escape
STYLE='''@page{size:A3 landscape;margin:12mm}*{box-sizing:border-box;print-color-adjust:exact}body{font-family:"Noto Sans CJK TC",sans-serif;color:#24372e;margin:0}section{break-after:page;height:272mm}section:last-child{break-after:auto}h1{font-size:20pt;margin:0 0 6mm}h2{font-size:11pt;margin:0 0 2mm}.columns{display:grid;grid-template-columns:1.2fr 1fr;gap:8mm}.art{position:relative;container-type:inline-size}.art img{display:block;width:100%;height:auto}.label{position:absolute;transform:translate(-50%,-50%);text-align:center;line-height:1;font-weight:700;color:#000;white-space:nowrap;text-shadow:0 1px 2px #fff8}.copy{font-size:10.5pt;line-height:1.45}.cue{break-inside:avoid;margin-bottom:3mm}.time{font-size:8pt;color:#637166}.cue p{margin:1mm 0}.source{font-size:9pt;font-weight:700}blockquote{font-size:9pt;line-height:1.4;margin:1mm 0;padding-left:3mm;border-left:2px solid #b3bdaa;white-space:pre-line}.note{font-size:11pt;line-height:1.8;margin-top:6mm}'''
def document():
 parts=[]
 for i,s in enumerate(STORY,1):
  parts.append('<section><h1>七覺支｜'+str(i).zfill(2)+' '+e(s['title'])+'</h1><div class="columns"><div><div class="art"><img src="/seven-factors/assets/'+str(i).zfill(2)+'.webp">')
  for o in s['artOverlay']:parts.append(f'<div class="label" style="left:{o["x"]}%;top:{o["y"]}%;width:{o["width"]}%;font-size:{o["fontSizeCqw"]}cqw">'+e(o['text'])+'</div>')
  parts.append('</div><p class="note">時間為每秒抽樣的近似定位，並非音軌精校。網頁可在同頁切換段落，經文及第11幕左右聚焦同步；本PDF以全圖供對讀。</p>')
  if i==12:parts.append('<p class="note">本繪本依《雜阿含經》第713、714、715、810經與《中部》第10經製作，解讀仍請以原經為準。也希望這本繪本能成為您走入經藏的起點。</p>')
  parts.append('</div><div class="copy">')
  for cue in s['cues']:
   parts.append('<div class="cue"><span class="time">'+e(cue['startTime'])+'</span><p>'+e(cue['text'])+'</p>')
   for q in cue['quoteIds']:parts.append('<p class="source">'+e(CAT[q]['source'])+'</p><blockquote>'+e(CAT[q]['text'])+'</blockquote>')
   parts.append('</div>')
  parts.append('</div></div></section>')
 return '<!doctype html><html lang="zh-Hant-TW"><meta charset="utf-8"><style>'+STYLE+'</style><body>'+''.join(parts)+'</body></html>'
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if self.path=='/review.html':
   raw=document().encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(raw)
  else:super().do_GET()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();out=O/'Seven-Factors-review.pdf'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();page.goto(f'http://127.0.0.1:{server.server_port}/review.html');page.evaluate('()=>document.fonts.ready');page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)');page.pdf(path=str(out),print_background=True,prefer_css_page_size=True);b.close()
server.shutdown()
with tempfile.TemporaryDirectory(prefix='seven-pdf-') as tmp:
 src=Path(tmp)/'full.pdf';shutil.copyfile(out,src);pdf=fitz.open(src);seen=set()
 for page in pdf:
  for row in page.get_images():
   xref=row[0]
   if xref in seen:continue
   seen.add(xref);raw=pdf.extract_image(xref);buf=io.BytesIO();Image.open(io.BytesIO(raw['image'])).convert('RGB').save(buf,'JPEG',quality=92,optimize=True);page.replace_image(xref,stream=buf.getvalue())
 pdf.save(out,garbage=4,deflate=True);pdf.close()
text=re.sub(r'\s+','',subprocess.check_output(['pdftotext','-layout',str(out),'-'],text=True))
for s in STORY:
 for c in s['cues']:assert re.sub(r'\s+','',c['text']) in text,c['id']
for q in CAT.values():assert re.sub(r'\s+','',q['text']) in text,q['quoteId']
with fitz.open(out) as pdf:assert len(pdf)==12;report={'pages':len(pdf),'all36Narrations':'retained','all16ScriptureCues':'retained','bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(O/'pdf-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report),flush=True)
