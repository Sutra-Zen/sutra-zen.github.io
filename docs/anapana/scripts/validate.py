from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'storyboard.json').read_text());q=json.loads((r/'scripture-catalog.json').read_text());m=json.loads((r/'asset-manifest.json').read_text())
assert len(d['scenes'])==12
assert len(q)==41
assert sum(len(s['narration']) for s in d['scenes'])==118
assert sum(len(s['overlays']) for s in d['scenes'])==12
assert len([s for s in d['scenes'] if s['image']])==11
for a in m:
 p=r/a['path'];assert p.is_file(),a['path']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256'],a['path']
for s in d['scenes']:
 for n in s['narration']:
  assert n['quoteIds'] or n['sourceNote'],n['id']
  assert all(x in q for x in n['quoteIds']),n['id']
 for o in s['overlays']:
  assert 0<=o['x']<=100 and 0<=o['y']<=100 and o['x']+o['width']<=100
print('PASS: 12 scenes / 118 paragraphs / 41 quotes / 12 overlays / all asset hashes')
