from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[1]
a=json.loads((r/'storyboard.json').read_text());q=json.loads((r/'scripture-catalog.json').read_text());m=json.loads((r/'asset-manifest.json').read_text())
assert len(a['scenes'])==9
assert sum(len(s['narration']) for s in a['scenes'])==81
assert len(q)==11
assert sum(len(s['overlays']) for s in a['scenes'])==13
for s in a['scenes']:
 assert (r/s['image']).is_file()
 for p in s['narration']:
  assert p['startSeconds']<p['endSeconds']
  assert all(k in q for k in p['quoteIds'])
for f in m:
 b=(r/f['path']).read_bytes();assert len(b)==f['bytes'];assert hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
print('OK: 9 scenes, 81 paragraphs, 11 quotes, 13 overlays; all files and hashes match.')
