from pathlib import Path
from html.parser import HTMLParser
import json,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];base='/kor-0020-web';origin='https://mcyj.github.io'+base
class Doc(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
checks=[]
for lang in ['ko','en']:
 for route in ['','guide','privacy','terms','support']:
  p=R/lang/route/'index.html';s=p.read_text();doc=Doc();doc.feed(s)
  expected=origin+'/'+lang+'/'+(route+'/'if route else'')
  assert f'<html lang="{lang}">'in s
  assert ('link',{'rel':'canonical','href':expected})in doc.tags
  assert all(any(t=='link'and a.get('rel')=='alternate'and a.get('hreflang')==l for t,a in doc.tags)for l in ['ko','en','x-default'])
  assert any(t=='meta'and a.get('name')=='description'and len(a.get('content',''))>25 for t,a in doc.tags)
  assert s.count('<h1>')==1 and '<main id="main">'in s
  assert '<script'not in s and '<form'not in s and 'play.google.com/store/apps'not in s and 'apps.apple.com/'not in s
  assert not re.search(r'(?<![0-9])500(?![0-9])',s)
  for tag,a in doc.tags:
   if tag=='img':assert a.get('alt')is not None and a.get('width')and a.get('height')
   href=a.get('href')or a.get('src')
   if href and href.startswith(base+'/'):
    rel=href[len(base)+1:];q=R/rel
    assert (q/'index.html').is_file()if href.endswith('/')else q.is_file(),href
  checks.append(str(p.relative_to(R)))
urls=[e.text for e in ET.parse(R/'sitemap.xml').getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(urls)==11 and len(set(urls))==11 and all(u.startswith(origin+'/')for u in urls)
css=(R/'assets/style.css').read_text();assert 'word-break:keep-all'in css and '@media(max-width:620px)'in css and 'prefers-reduced-motion'in css and ':focus-visible'in css
assert 'All rights reserved'not in(R/'README.md').read_text()
print(json.dumps({'result':'PASS','localizedRoutes':len(checks),'sitemapRoutes':len(urls),'sourceRoutes':checks,'downloadCTAsEnabled':False,'externalScripts':0,'responsiveCss':True,'siteIdentity':'kor-0020 Pro'},ensure_ascii=False))
