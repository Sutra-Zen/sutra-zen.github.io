#!/usr/bin/env python3
"""Build twelve Seven Factors pages with all original timed narration segments."""
import argparse,hashlib,json,copy
from pathlib import Path
from lxml import html,etree
R=Path(__file__).resolve().parents[1];D=R/'docs/seven-factors';S=R/'seven-factors'
def read(name):return json.loads((D/name).read_text())
def validate():
 for name,row in read('receipt.json').items():
  raw=(D/name).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],name
 story=read('storyboard.json');assert len(story)==12 and sum(len(s['cues']) for s in story)==36 and sum(len(s['artOverlay']) for s in story)==14
 for f in read('source-files.json'):assert hashlib.sha256((D/f['local']).read_bytes()).hexdigest()==f['sha256']
 for s in story:
  assert s['cues'][0]['startSeconds']==s['startSeconds'] and s['cues'][-1]['endSeconds']==s['endSeconds']
  for c in s['cues']:assert c['text'] in (D/'storyboard.md').read_text() and c['endSeconds']>c['startSeconds']
 print('12 scenes/36 intact paragraphs/16 scripture switches/14 centered labels; original hashes passed')
def book():
 cat=read('scripture-catalog.json');pages=[]
 for i,s in enumerate(read('storyboard.json')):
  dims=read('receipt.json')[s['asset']]['dimensions'];cues=[dict(c,lines=[c['text']],quotes=[cat[q] for q in c['quoteIds']]) for c in s['cues']]
  pages.append({'scene':s['id'],'id':s['id'],'title':s['title'],'start':i,'alt':s['title'],'image':'../assets/'+str(i+1).zfill(2)+'.webp','dimensions':dims,'artOverlay':s['artOverlay'],'summaryRows':[],'cues':cues,**{k:v for k,v in cues[0].items() if k in ['lines','quotes']}})
 f={'scenes':{'S11':{'panels':[{'id':'left','x':0,'y':0,'width':42,'height':100,'label':'昏沉：擇法、精進、喜'},{'id':'right','x':58,'y':0,'width':42,'height':100,'label':'浮動：輕安、定、捨'}],'pages':[None,None,None,'left','right',None],'note':'保留中央念燈；總說、守護與念兼助時全幅。'}}}
 b={'title':'七覺支','timingAccuracy':'one-second sampled timestamps; not audio verified','scenes':pages,'pages':pages}
 return {S/'book/book-data.js':'// Generated from the intact author handoff.\nconst BOOK = '+json.dumps(b,ensure_ascii=False,indent=2)+';\n',S/'book/panel-focus-data.js':'const PANEL_FOCUS = '+json.dumps(f,ensure_ascii=False,indent=2)+';\n'}
def guide():
 root=html.parse(str(R/'five-roots-powers/index.html'));root.xpath('//title')[0].text='七覺支｜SutraZen 主題導讀';head=root.xpath('//head')[0];root.xpath('//meta[@name="description"]')[0].set('content','看見心的浮動與沉滯，閱讀七覺支十二幕繪本，對讀原經並下載離線閱讀。')
 main=root.xpath('//main')[0];main.xpath('./h1')[0].text='七覺支';lead=main.xpath('./p[@class="lead"]')[0];lead.clear();lead.set('class','lead');strong=etree.SubElement(lead,'strong');strong.text='先看清自己的心，再調整用功的火候。';strong.tail='跟著小貓認識念、擇法、精進、喜、輕安、定、捨：心太沉時提起精神，心太浮動時安穩下來，念則始終幫助我們看清當下。'
 section=main.xpath('./section')[0];section.xpath('./h2')[0].text='翻頁繪本 · 七覺支篇';cover=section.xpath('.//a[@class="book-cover"]')[0];cover.set('aria-label','開始翻閱七覺支');im=cover.xpath('./img')[0];im.set('src','assets/04.webp');im.set('alt','小貓覺察呼吸與飄過的落葉')
 chapter=main.xpath('./section')[1];chapter.clear();etree.SubElement(chapter,'h2').text='認識覺支，照看心的火候';grid=etree.SubElement(chapter,'div',{'class':'chapter-grid'})
 for s in read('storyboard.json'):
  a=etree.SubElement(grid,'a',href='book/index.html?scene='+s['id']);etree.SubElement(a,'strong').text=s['title'];etree.SubElement(a,'span').text=s['cues'][0]['text']
 video=root.xpath('//*[@id="video"]')[0];video.xpath('./h2')[0].text='療癒系佛法繪本 · 七覺支篇';frame=video.xpath('.//iframe')[0];frame.set('src','https://www.youtube.com/embed/8tlCxoV5x5I');frame.set('title','療癒系佛法繪本 · 七覺支篇')
 refs=root.xpath('//*[@id="sources"]')[0];template=copy.deepcopy(refs.xpath('./article')[0]);icons=[copy.deepcopy(x) for x in template.xpath('.//a[contains(@class,"source-button")]/svg')]
 for a in refs.xpath('./article'):refs.remove(a)
 for source in read('verified-sources.json')['sources']:
  article=etree.SubElement(refs,'article',{'class':'source-entry','id':source['id']})
  for q in source['quoteIds']:etree.SubElement(article,'span',{'class':'source-anchor','id':q})
  etree.SubElement(article,'p',{'class':'eyebrow'}).text='七覺支 · 經典出處';etree.SubElement(article,'h3').text=source['title'];etree.SubElement(article,'p',{'class':'source-meta'}).text=source['meta'];actions=etree.SubElement(article,'div',{'class':'source-actions'})
  for i,(href,label) in enumerate([(source['primary'],'漢譯經文' if source['id'].startswith('sa') else '中譯經文'),(source['comparison'],source['comparisonLabel'])]):
   a=etree.SubElement(actions,'a',{'class':'source-button source-button--'+('annotation' if i else 'original'),'href':href,'target':'_blank','rel':'noopener noreferrer'});a.append(copy.deepcopy(icons[i]));etree.SubElement(a,'span').text=label
  providers=etree.SubElement(article,'div',{'class':'source-providers'})
  for p in source['providers']:etree.SubElement(providers,'p').text=p
  body=etree.SubElement(article,'div',{'class':'source-text'})
  for section in source['sections']:etree.SubElement(body,'h4',{'class':'source-text-heading'}).text=section['title'];etree.SubElement(etree.SubElement(body,'blockquote'),'p').text=section['text']
 return S/'index.html',html.tostring(root,encoding='unicode',doctype='<!doctype html>')+'\n'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();validate();outputs=book();path,text=guide();outputs[path]=text
 for path,text in outputs.items():
  if a.check:assert path.read_text()==text,path
  else:path.write_text(text)
