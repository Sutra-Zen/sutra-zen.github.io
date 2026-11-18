#!/usr/bin/env python3
"""Print the complete book12 content for iPad review without deploying a site."""
import functools,hashlib,html,http.server,io,json,re,shutil,subprocess,tempfile,threading
from pathlib import Path
import fitz
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'docs/four-jhanas';OUT=ROOT/'docs/previews/four-jhanas/Four-Jhanas-review.pdf'
STORY=json.loads((D/'storyboard.json').read_text());CAT=json.loads((D/'scripture-catalog.json').read_text());LABELS=json.loads((D/'overlay-layout.json').read_text())['overlays'];BOOK=json.loads((ROOT/'four-jhanas/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'));e=html.escape
STYLE='''@page{size:A4;margin:15mm}*{box-sizing:border-box;print-color-adjust:exact}body{font-family:"Noto Sans CJK TC","Noto Sans TC",sans-serif;font-size:12pt;line-height:1.75;color:#24372e}h1{font-size:24pt}h2{font-size:19pt}h3{font-size:14pt}h1,h2,h3{break-after:avoid}p{margin:6pt 0}.scene{break-before:page}.art{position:relative;container-type:inline-size;break-inside:avoid}.art img{display:block;width:100%;height:auto}.label{position:absolute;text-align:center;font-weight:700;line-height:1.15;white-space:nowrap;text-shadow:0 1px 2px #333}.label[style*="#000000"]{text-shadow:0 1px 2px #fff8}.paragraph{break-inside:avoid;margin:14pt 0}.meta{font-size:9pt;color:#637166;overflow-wrap:anywhere}blockquote{margin:10pt 0;padding-left:12pt;border-left:2px solid #adb9a8;white-space:pre-line;overflow-wrap:anywhere}article{margin-bottom:28pt}table{width:100%;border-collapse:collapse;font-size:10pt}th,td{padding:6pt;border:1px solid #adb9a8;text-align:left}'''
def document():
 body=['<h1>四禪｜完整內容校稿預覽</h1><p>十幕、P001–P130完整字幕及八筆經文卡。文字可選取；互動介面與橫直式畫面另見試閱說明及實際截圖。時間為約略定位，非精準音軌字幕。本PDF供內容對讀，網頁另提供互動閱讀。</p>']
 for scene in STORY:
  sid=scene['id'];body.append(f'<section class="scene"><h2>{sid}｜{e(scene["title"])}</h2><div class="art"><img src="/four-jhanas/assets/{sid}.webp">')
  for o in LABELS[sid]:body.append(f'<div class="label" style="left:{o["x"]}%;top:{o["y"]}%;width:{o["width"]}%;font-size:{o["fontSizeCqw"]}cqw;color:{o["color"]}">{e(o["text"])}</div>')
  body.append('</div><h3>完整字幕</h3>')
  for cue in scene['cues']:body.append(f'<div class="paragraph"><p class="meta">{cue["id"]} · {cue["start"]}–{cue["end"]}</p><p>{e(cue["text"])}</p></div>')
  if sid=='S10':
   table=BOOK['pages'][123]['tableSummary'];body.append('<h3>四禪比較</h3><table><thead><tr><th>項目</th>'+''.join('<th>'+x+'</th>' for x in table['columns'])+'</tr></thead><tbody>')
   for row in table['rows']:body.append('<tr><th>'+row[0]+'</th>'+''.join('<td>'+x+'</td>' for x in row[1:])+'</tr>')
   body.append('</tbody></table>')
  body.append('</section>')
 body.append('<section class="scene"><h2>經文卡</h2>')
 for qid,q in CAT.items():body.append(f'<article><h3>{qid}｜{e(q["source"])}</h3><blockquote>{e(q["text"])}</blockquote></article>')
 body.append('</section><section class="scene"><h2>片尾出處</h2><div class="art"><img src="/four-jhanas/assets/credits.webp"></div></section><section class="scene"><h2>閱讀說明</h2>')
 for block in BOOK['pages'][-1]['textSummary']:
  for text in block['paragraphs']:body.append('<p>'+e(text)+'</p>')
 return '<!doctype html><html lang="zh-Hant-TW"><meta charset="utf-8"><title>四禪｜SutraZen 校稿預覽</title><style>'+STYLE+'</style><body>'+''.join(body)+'</section></body></html>'
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path=='/review.html':
   raw=document().encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(raw)
  else:super().do_GET()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page();page.goto(f'http://127.0.0.1:{server.server_port}/review.html');page.evaluate('()=>document.fonts.ready');page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)');assert page.locator('img').count()==11 and page.locator('.label').count()==7;OUT.parent.mkdir(parents=True,exist_ok=True);page.pdf(path=str(OUT),format='A4',print_background=True);browser.close()
server.shutdown()
with tempfile.TemporaryDirectory(prefix='four-jhanas-pdf-') as tmp:
 raw=Path(tmp)/'full.pdf';shutil.copyfile(OUT,raw);pdf=fitz.open(raw);seen=set()
 for page in pdf:
  for image in page.get_images():
   xref=image[0]
   if xref in seen:continue
   seen.add(xref);data=pdf.extract_image(xref);b=io.BytesIO();Image.open(io.BytesIO(data['image'])).convert('RGB').save(b,'JPEG',quality=92,optimize=True);page.replace_image(xref,stream=b.getvalue())
 pdf.save(OUT,garbage=4,deflate=True);pdf.close()
normalized=re.sub(r'\s+','',subprocess.check_output(['pdftotext','-layout',str(OUT),'-'],text=True))
for scene in STORY:
 for cue in scene['cues']:assert re.sub(r'\s+','',cue['text']) in normalized,cue['id']
for qid,q in CAT.items():assert re.sub(r'\s+','',q['text']) in normalized,qid
with fitz.open(OUT) as pdf:report={'file':OUT.name,'pages':len(pdf),'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'captions':130,'scriptures':8,'textValidation':'all 130 caption and 8 complete quotation strings retained','purpose':'review content; interactive UI tested separately'}
OUT.with_name('pdf-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
