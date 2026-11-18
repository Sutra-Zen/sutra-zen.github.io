#!/usr/bin/env python3
"""Package a relative-file, fetch-free offline reader; no image Base64 or CDN."""
import hashlib,json,zipfile
from pathlib import Path
from lxml import html,etree
R=Path(__file__).resolve().parents[1];out=R/'downloads/SutraZen-Seven-Factors-Offline.zip';out.parent.mkdir(exist_ok=True)
files={}
for p in (R/'seven-factors').rglob('*'):
 if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
for name in ['reader-controls.css','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','guide-header.css','guide-ui.css']:files[name]=(R/name).read_bytes()
for name in ['seven-factors/index.html','seven-factors/book/index.html']:
 tree=html.fromstring(files[name])
 for node in tree.xpath('//a[@download]'):
  parent=node.getparent();parent.remove(node)
 for node in tree.xpath('//iframe'):
  a=etree.Element('a',href='https://www.youtube.com/watch?v=8tlCxoV5x5I',target='_blank');a.text='連線觀看影片（需要網路）';node.getparent().replace(node,a)
 for node in tree.xpath('//a[@href="../index.html" and contains(@class,"guide-return")]|//a[@href="../../index.html"]'):node.text='回離線目錄'
 for node in tree.xpath('//a[starts-with(@href,"https://")]'):node.set('title','外部來源，需要網路；本頁節錄可離線閱讀')
 files[name]=html.tostring(tree,encoding='utf-8',doctype='<!doctype html>')
files['index.html']='''<!doctype html><html lang="zh-Hant-TW"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>七覺支離線目錄</title><link rel="stylesheet" href="guide-ui.css"><body class="topic-guide"><main class="wrap guide-content"><h1>七覺支離線繪本</h1><p><a href="seven-factors/book/index.html">開始閱讀十二頁繪本</a></p><p><a href="seven-factors/index.html">主題導讀與經文節錄</a></p><p>本包的插圖、口白、經文、翻頁與放大均可離線使用。影片與外部原經網站需要網路。</p></main></body></html>'''.encode()
files['README.txt']='''七覺支離線繪本
請先完整解壓ZIP，保持目錄結構；建議以下述本機網站方式在瀏覽器開啟index.html。
共有12頁、36段口白；主按鍵依序讀完全部36段口白、當時經文與聚焦，保留12幅圖頁；不需另外切換段落。
不需要登入或外部圖片，請勿只從壓縮檔內預覽單一HTML。
已測方式：解壓後在該目錄執行 python3 start-local.py ，瀏覽器開啟 http://127.0.0.1:8765/ ，無外部網路仍可翻頁。
直接開啟file://未在本次環境驗證（受管理瀏覽器禁止本機檔案網址）。
iPad/iPhone的「檔案」快速預覽不一定執行JavaScript，不能當作瀏覽器離線驗收。實際iPad Safari／下載解壓流程仍請實機確認。
影片和外部經典連結需要網路；本包內的原經節錄可以直接離線讀。
'''.encode()
files['start-local.py']=b'''import http.server,functools\nfrom pathlib import Path\nroot=Path(__file__).resolve().parent\nprint("Open http://127.0.0.1:8765/ ; Ctrl+C to stop")\nhttp.server.ThreadingHTTPServer(("127.0.0.1",8765),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(root))).serve_forever()\n'''
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name,raw in sorted(files.items()):
  info=zipfile.ZipInfo(name,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,raw)
with zipfile.ZipFile(out) as z:assert z.testzip() is None
report={'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':{name:hashlib.sha256(raw).hexdigest() for name,raw in sorted(files.items())},'format':'standard ZIP,relative files,no CDN or Base64','physicalSafari':'not tested'}
(R/'docs/seven-factors/offline-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(out.name,report['bytes'],'bytes',len(files),'files')
