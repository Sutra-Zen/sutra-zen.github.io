#!/usr/bin/env python3
"""Create a selectable-text iPad review PDF without deploying the website."""
import functools,hashlib,html,http.server,io,json,re,shutil,subprocess,tempfile,threading
import fitz
from PIL import Image
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs/iddhipada';OUT=ROOT/'docs/previews/iddhipada/Iddhipada-review.pdf'
story=json.loads((DOCS/'storyboard.json').read_text());quotes=json.loads((DOCS/'scripture-catalog.json').read_text());layout=json.loads((DOCS/'overlay-layout.json').read_text())['overlays']
e=html.escape
def clock(t):return f'{int(t)//60:02}:{int(t)%60:02}'
def document():
 body=['<h1>四如意足｜完整內容校稿預覽</h1><p>審閱分支，未發布正式站。本PDF保留9幕、81段口白與11筆經文卡，方便在iPad直接閱讀；互動按鍵與橫直式畫面另見試閱說明和截圖。時間碼僅供影片定位，約有1–3秒誤差。</p>']
 for s in story['scenes']:
  body.append(f'<section class="scene"><h2>{s["sceneId"]}｜{e(s["title"])}</h2><div class="art"><img src="/iddhipada/assets/{s["sceneId"]}.webp" width="1672" height="941">')
  for o in layout[s['sceneId']]:body.append(f'<div class="label" style="left:{o["x"]}%;top:{o["y"]}%;width:{o["width"]}%;font-size:{o["fontSizeCqw"]}cqw;color:{o["color"]}">{e(o["text"])}</div>')
  body.append('</div><h3>完整口白</h3>')
  for p in s['narration']:body.append(f'<div class="paragraph"><p class="meta">{p["id"]} · {clock(p["startSeconds"])}–{clock(p["endSeconds"])} · {"、".join(p["quoteIds"])}</p><p>{e(p["text"])}</p></div>')
  body.append('</section>')
 body.append('<section class="scene"><h2>經文卡｜Q01–Q11</h2><p>Q01–Q08為交接稿的巴利摘錄與中文譯意，中文譯意未署名為莊春江；Q09保留影片摘錄及譯者未定的註記；Q10–Q11為古漢譯。</p>')
 for qid,q in quotes.items():
  body.append(f'<article><h3>{qid}｜{e(q["source"])}</h3>')
  if q['sourceType']=='pali_with_editorial_chinese_paraphrase':body.append(f'<p>{e(q["translationNote"])}</p><h4>巴利原文</h4><blockquote lang="pi">{e(q["originalText"])}</blockquote>')
  else:body.append(f'<blockquote>{e(q["originalText"])}</blockquote><p>{e(q["translationNote"])}</p>')
  body.append(f'<p class="meta"><a href="{e(q["sourceUrl"])}">{e(q["sourceUrl"])}</a></p></article>')
 body.append('</section><section class="scene"><h2>閱讀說明</h2><p>本繪本依《相應部》第51相應的相關經文與《雜阿含經》第561經製作。口白中的划船、引擎與抵岸是故事譬喻，解讀仍請以原經文為準。</p><p>也希望這本繪本能成為您走入經藏的起點。</p></section>')
 return '''<!doctype html><html lang="zh-Hant-TW"><meta charset="utf-8"><title>四如意足｜SutraZen 校稿預覽</title><style>
 @page{size:A4;margin:15mm}*{box-sizing:border-box}body{font-family:"Noto Sans CJK TC","Noto Sans TC",sans-serif;font-size:12pt;line-height:1.75;color:#24372e}h1{font-size:24pt}h2{font-size:19pt}h3{font-size:14pt}h4{font-size:12pt}h1,h2,h3,h4{break-after:avoid}p{margin:6pt 0}.scene{break-before:page}.art{position:relative;container-type:inline-size;break-inside:avoid}.art img{display:block;width:100%;height:auto}.label{position:absolute;text-align:center;font-weight:700;line-height:1.15;text-shadow:0 1px 2px #000,0 0 3px #333;white-space:nowrap}.label[style*="#000000"]{text-shadow:0 1px 2px #fff8}.paragraph{break-inside:avoid;margin:14pt 0}.meta{font-size:9pt;color:#637166;overflow-wrap:anywhere}blockquote{margin:10pt 0;padding-left:12pt;border-left:2px solid #adb9a8;overflow-wrap:anywhere}blockquote[lang=pi]{font-family:Georgia,serif}a{color:inherit}article{margin-bottom:28pt}*{print-color-adjust:exact}
 </style><body>'''+''.join(body)+'</body></html>'
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path=='/review.html':
   data=document().encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
  else:super().do_GET()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page();page.goto(f'http://127.0.0.1:{server.server_port}/review.html');page.evaluate('()=>document.fonts.ready');assert page.locator('img').count()==9 and page.locator('.label').count()==13;page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth===1672)');OUT.parent.mkdir(parents=True,exist_ok=True);page.pdf(path=str(OUT),format='A4',print_background=True,display_header_footer=False);browser.close()
server.shutdown()
with tempfile.TemporaryDirectory(prefix='iddhipada-pdf-') as tmp:
 raw=Path(tmp)/'full.pdf';shutil.copyfile(OUT,raw)
 # Compress only raster illustrations; keep Chromium's Unicode text maps intact.
 pdf=fitz.open(raw);seen=set()
 for page in pdf:
  for image in page.get_images():
   xref=image[0]
   if xref in seen:continue
   seen.add(xref);data=pdf.extract_image(xref);compressed=io.BytesIO()
   Image.open(io.BytesIO(data['image'])).convert('RGB').save(compressed,'JPEG',quality=90,optimize=True)
   page.replace_image(xref,stream=compressed.getvalue())
 pdf.save(OUT,garbage=4,deflate=True);pdf.close()
text=subprocess.check_output(['pdftotext','-layout',str(OUT),'-'],text=True);normalized=re.sub(r'\s+','',text)
for s in story['scenes']:
 for p in s['narration']:assert re.sub(r'\s+','',p['text']) in normalized,p['id']
for qid,q in quotes.items():
 assert re.sub(r'\s+','',q['originalText']) in normalized,qid
 assert re.sub(r'\s+','',q['translationNote']) in normalized,qid
with fitz.open(OUT) as pdf:
 report={'file':OUT.name,'pages':len(pdf),'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'originalNarrationParagraphs':81,'completeQuoteCards':11,'selectableText':'all original narration/quotation/note strings verified with pdftotext','purpose':'content review only; interactive UI tested separately; not deployed'}
OUT.with_name('pdf-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PDF contains all 81 exact narration paragraphs and all 11 complete quote cards; selectable text verified:',OUT)
