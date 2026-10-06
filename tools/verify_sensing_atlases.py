"""Independent algebra checks plus local document/link checks, not experimental validation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, math, zipfile, hashlib, numpy as np
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'work'/'atlas-qa';QA.mkdir(parents=True,exist_ok=True)
results={};failures=[]
def check(key,truth,details):
    results[key]={'passed':bool(truth),'details':details}
    if not truth:failures.append(key)

# Construct photons from Bose occupation and losses, independently of the displayed inversion.
gamma=633.0; C=-math.log(1.37); T=np.array([273.15,298.15,333.15,373.15]); A=np.array([0.0,.09,.25,.4])
n=1/(np.exp(gamma/T)-1);PS=1.37*(n+1)*np.exp(-.2);PAS=n*np.exp(-.2-A)
recovered=gamma/(np.log(PS/PAS)+C-A)
check('raman_single_end',np.max(abs(recovered-T))<1e-10,{'max_error_K':float(np.max(abs(recovered-T))), 'source':'Bose occupation, unequal gain, and differential attenuation'})
Atotal=.8;lnRA=gamma/T-C+A;lnRB=gamma/T-C+(Atotal-A)
double=gamma/((lnRA+C+lnRB+C)/2-Atotal/2)
check('raman_double_end',np.max(abs(double-T))<1e-10,{'max_error_K':float(np.max(abs(double-T))), 'assumptions':'same physical coordinate, reciprocal channel losses, stable T'})
uncorrected=gamma/(np.log(PS/PAS)+C)
check('raman_loss_negative_control',np.max(abs(uncorrected-T))>20,{'uncorrected_max_bias_K':float(np.max(abs(uncorrected-T)))})
# Invert an actual non-negative code matrix and check that decoding precedes ratio formation.
code=np.array([[1.,1.,0.],[1.,0.,1.],[0.,1.,1.]]);truth=np.array([.5,2.,4.]);decoded=np.linalg.solve(code,code@truth)
check('coded_impulse_response',np.max(abs(decoded-truth))<1e-12,{'max_error':float(np.max(abs(decoded-truth)))})
# Explicit unit check: Ceps in Hz per dimensionless strain; CT in Hz/K.
Ceps=50e9;CT=1e6;eps=230e-6;dt=12.;shift=Ceps*eps+CT*dt
eps_back=(shift-CT*dt)/Ceps
check('brillouin_compensation',abs(eps_back-eps)<1e-15,{'true_microstrain':eps*1e6,'recovered_microstrain':eps_back*1e6,'uncompensated_microstrain':shift/Ceps*1e6})
# Independent Rayleigh sign test: stretching red-shifts the current spectrum.
nu=np.arange(-100.,100.);ref=np.exp(-nu**2/100);delta=-7.;current=np.exp(-(nu-delta)**2/100)
lags=np.arange(-20,21);corr=[np.sum(ref*np.interp(nu+l,nu,current,left=0,right=0)) for l in lags];found=float(lags[np.argmax(corr)])
check('rayleigh_correlation_sign',found==delta and -found>0,{'current_minus_reference_shift':delta,'matching_lag':found,'q_positive_for_tension':-found>0})
# Time-domain and frequency-domain localization use different measurements.
c=299792458.;ng=1.468;z=321.;tau=2*ng*z/c;kappa=8e11;fb=kappa*tau
check('position_conventions',abs(c*tau/(2*ng)-z)<1e-10 and abs(c*fb/(2*ng*kappa)-z)<1e-10,{'OTDR_position_m':c*tau/(2*ng),'OFDR_position_m':c*fb/(2*ng*kappa)})

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        for k in ('href','src'):
            if k in d:self.links.append((tag,k,d[k]))

pages=[ROOT/'index.html']+list((ROOT/'knowledge').glob('*.html'))+[ROOT/'knowledge'/'atlases'/'das'/'DAS_光路交互图册.html']
missing=[];duplicate=[]
for page in pages:
    p=Links();p.feed(page.read_text(encoding='utf-8'))
    duplicate.extend((str(page.relative_to(ROOT)),id) for id in set(p.ids) if p.ids.count(id)>1)
    for tag,key,value in p.links:
        u=urlsplit(value)
        if u.scheme or value.startswith('//') or not u.path:continue
        target=(page.parent/unquote(u.path)).resolve()
        if not target.exists():missing.append((str(page.relative_to(ROOT)),value))
check('site_local_links',not missing,{'pages':len(pages),'missing':missing})
check('unique_html_ids',not duplicate,{'duplicates':duplicate})
for kind in ['dts','dss']:
    folder=ROOT/'knowledge'/'atlases'/kind
    pdf=folder/(kind.upper()+'_原理光路图册.pdf');reader=PdfReader(pdf)
    text='\n'.join(page.extract_text() or '' for page in reader.pages)
    check(kind+'_pdf_content',len(reader.pages)==24 and '温度' in text and 'Δν' in text,{'pages':len(reader.pages),'extracted_chars':len(text),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()})
    with zipfile.ZipFile(folder/(kind.upper()+'_资料包.zip')) as z:
        corrupt=z.testzip();check(kind+'_zip_integrity',corrupt is None,{'entries':len(z.namelist()),'corrupt':corrupt})
        page=Links();page.feed(z.read('index.html').decode('utf-8'));missing_zip=[]
        for tag,key,v in page.links:
            u=urlsplit(v)
            if u.scheme or not u.path:continue
            if unquote(u.path) not in z.namelist():missing_zip.append(v)
        check(kind+'_portable_links',not missing_zip,{'missing':missing_zip})
    data=json.loads((folder/'atlas.json').read_text(encoding='utf-8'))
    check(kind+'_route_assets',all((folder/'figures'/(r['id']+'.svg')).exists() for r in data['routes']),{'routes':len(data['routes'])})
results['boundary']={'experimental_validation':False,'claim':'Algebra/structure checks only; no validation of an instrument or field inference.'}
(QA/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':len(results)-1,'failed':failures},ensure_ascii=False))
if failures:raise SystemExit(1)
