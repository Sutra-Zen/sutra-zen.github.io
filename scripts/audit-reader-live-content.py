from pathlib import Path
from lxml import html
from urllib.parse import urljoin,urlparse
import concurrent.futures,hashlib,json,subprocess,urllib.request
root=Path(__file__).resolve().parents[1];reportdir=root/'docs/audits/reader-caption-scripture';pages=json.loads((reportdir/'pages.json').read_text());books=list(dict.fromkeys(r['book'] for r in pages));paths=set()
for b in books:
 index=b+'/book/index.html';paths.add(index)
 for src in html.fromstring((root/index).read_bytes()).xpath('//script/@src'):
  rel=urlparse(urljoin('https://sutra-zen.github.io/'+index,src)).path.lstrip('/')
  if rel.startswith(b+'/book/'):paths.add(rel)
paths.add('play/collection/reader-bridge.js')
def check(path):
 req=urllib.request.Request('https://sutra-zen.github.io/'+path+'?v=source-audit-20261124',headers={'Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=60) as res:
  data=res.read();expected=(root/path).read_bytes();return {'path':path,'status':res.status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'equalsAuditedRepository':data==expected}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:files=list(pool.map(check,sorted(paths)))
report={'base':'https://sutra-zen.github.io/','baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'tls':'Normal HTTPS CA verification','files':files,'result':'passed' if all(r['status']==200 and r['equalsAuditedRepository'] for r in files) else 'differences'}
(reportdir/'live-files.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(report['result'],len(files),'HTML/native data and render scripts/bridge match live')
