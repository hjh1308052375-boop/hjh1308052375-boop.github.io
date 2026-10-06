"""Export diagram PNGs and contact sheets for visual review; keep QA out of website output."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, json
from PIL import Image, ImageOps, ImageDraw
from build_sensing_atlases import ROOT, OUT, QA, make_components, package

POPPLER=Path('C:/Users/dell/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')

def render(job):
    source,prefix,single=job
    args=[str(POPPLER),'-png','-scale-to','1200']
    if single:args+=['-singlefile']
    subprocess.run(args+[str(source),str(prefix)],check=True,capture_output=True)

jobs=[]
for kind in ['dts','dss']:
    dest=QA/kind;dest.mkdir(exist_ok=True)
    jobs.append((OUT/kind/(kind.upper()+'_原理光路图册.pdf'),dest/'page',False))
    for p in (OUT/kind/'figures').glob('*.pdf'):jobs.append((p,p.with_suffix(''),True))
with ThreadPoolExecutor(max_workers=3) as executor:list(executor.map(render,jobs))
for kind in ['dts','dss']:
    images=sorted((QA/kind).glob('page-*.png'))
    cellw,cellh=420,315
    for group in range(0,len(images),12):
        subset=images[group:group+12];sheet=Image.new('RGB',(cellw*3,cellh*4),'#e7edf2');draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(subset):
            im=Image.open(p).convert('RGB');im.thumbnail((cellw-15,cellh-28));x=(i%3)*cellw+(cellw-im.width)//2;y=(i//3)*cellh+23
            sheet.paste(im,(x,y));draw.text(((i%3)*cellw+12,(i//3)*cellh+5),kind.upper()+' '+p.stem,fill='#122d40')
        sheet.save(QA/(kind+f'-contact-{group//12+1}.jpg'),quality=94)
    folder=OUT/kind
    comps=json.loads((folder/'atlas.json').read_text(encoding='utf-8'))['components']
    package(kind,(ROOT/'knowledge'/(kind+'-optical-atlas.html')).read_text(encoding='utf-8'),comps,kind.upper()+'_原理光路图册.pdf')
print('Rendered 48 atlas pages and 13 diagram PNGs; refreshed both portable packages.')
