"""Check every served TeX expression with the exact vendored KaTeX engine."""
from pathlib import Path
from html.parser import HTMLParser
import json, subprocess, re
from math_content import MACROS

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'work'/'atlas-qa';QA.mkdir(parents=True,exist_ok=True)
class Formulas(HTMLParser):
    def __init__(self):super().__init__();self.math=[];self.links=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'data-tex' in a:self.math.append({'tex':a['data-tex'],'display':a.get('data-display')!='inline'})
        if tag in ('script','link'):
            self.links.append(a.get('src') or a.get('href'))
        if 'id' in a:self.ids.append(a['id'])

names=['das-optical-atlas.html','dts-optical-atlas.html','dss-optical-atlas.html','dfos-principles.html']
entries=[];counts={}
for name in names:
    content=(ROOT/'knowledge'/name).read_text(encoding='utf-8');p=Formulas();p.feed(content)
    counts[name]=len(p.math);entries.extend(dict(page=name,**e) for e in p.math)
    assert 'vendor/katex/katex.min.js' in p.links and 'math.js' in p.links
    assert len(p.ids)==len(set(p.ids)), 'Duplicate ids'
    if name=='dfos-principles.html':assert 'id="resolution"' not in content and 'href="#resolution"' not in content
    if name.startswith('das-'):assert content.count('class="detailed-derivation"')==20
    for path in filter(None,p.links):
        if not path.startswith(('http:','https:')):assert (ROOT/'knowledge'/path).exists(),path
source=json.loads((ROOT/'knowledge'/'atlases'/'das'/'derivations.json').read_text(encoding='utf-8'))['routes']
assert len(source)==10 and all(len(columns)==2 for columns in source.values())
inp=QA/'equations.json';inp.write_text(json.dumps({'entries':entries,'macros':MACROS},ensure_ascii=False),encoding='utf-8')
program=r'''const fs=require('fs'),k=require('./knowledge/vendor/katex/katex.min.js');
const data=JSON.parse(fs.readFileSync('work/atlas-qa/equations.json','utf8')),errors=[];
for(const e of data.entries){try{k.renderToString(e.tex,{displayMode:e.display,throwOnError:true,strict:'ignore',trust:false,macros:data.macros});}catch(err){errors.push({page:e.page,tex:e.tex,error:err.message});}}
fs.writeFileSync('work/atlas-qa/math-parse.json',JSON.stringify({version:k.version,total:data.entries.length,errors},null,2));
console.log(JSON.stringify({version:k.version,total:data.entries.length,errors}));if(errors.length)process.exit(1);'''
node='C:/Users/dell/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
subprocess.run([node,'-e',program],cwd=ROOT,check=True)
print(json.dumps(counts))
