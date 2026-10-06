"""Restore full existing derivations and emit math with local KaTeX rendering."""
from pathlib import Path
import html, json, re
from math_content import EQUATIONS, COMPONENTS

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'knowledge'/'atlases'/'das'/'derivations.json'

def math_html(tex,inline=False):
    cls='math-inline' if inline else 'math-display'
    tag='span' if inline else 'div'
    return f'<{tag} class="{cls}" data-display="{"inline" if inline else "block"}" data-tex="{html.escape(tex,quote=True)}">{html.escape(tex)}</{tag}>'

def step_math(eq):
    if eq not in EQUATIONS:raise ValueError('No explicit TeX conversion: '+eq)
    return math_html(EQUATIONS[eq])

INLINE = {
 'ΔνB = Cε Δεfiber + CT ΔT':EQUATIONS['ΔνB = Cε Δεfiber + CT ΔT'],
 'Δεavg=-Δφg/(Kε Lg)':r'\Delta\overline\varepsilon=-\frac{\Delta\phi_g}{K_\varepsilon L_g}',
 'Kε=4πneff(1-pe)/λ':r'K_\varepsilon=\frac{4\pi n_{\mathrm{eff}}(1-p_e)}{\lambda}',
 'nR = 1/[exp(γ/T)-1]':r'n_R=\frac1{e^{\gamma/T}-1}',
 'γ = h ΔνR/kB':r'\gamma=\frac{h\Delta\nu_R}{k_B}',
 'AΔ(z)=∫0^z[αAS(s)-αS(s)]ds':r'A_\Delta(z)=\int_0^z[\alpha_{\mathrm{AS}}(s)-\alpha_{\mathrm S}(s)]\,\mathrm ds',
 'νs=νp-Δν':r'\nu_s=\nu_p-\Delta\nu',
 'νLO=ν0-νoffset':r'\nu_{\mathrm{LO}}=\nu_0-\nu_{\mathrm{offset}}',
 'ν0-νB':r'\nu_0-\nu_B',
 'γ/T+AΔ(0,L)/2':r'\frac\gamma T+\frac{A_\Delta(0,L)}2',
 'Δz≈c/(2ng Bm)':r'\Delta z\simeq\frac c{2n_gB_m}',
 'c/(2ng δfm)':r'\frac c{2n_g\delta f_m}',
 'εfiber':r'\varepsilon_{\mathrm{fiber}}', 'εhost':r'\varepsilon_{\mathrm{host}}',
 'Δεfiber':r'\Delta\varepsilon_{\mathrm{fiber}}', 'Cε':r'C_\varepsilon', 'CT':r'C_T',
 'Kε':r'K_\varepsilon', 'KT':r'K_T', 'δν<0':r'\delta\nu<0', 'q>0':r'q>0',
}

def rich_bi(zh,en,tag='span',attrs=''):
    def rich(text):
        pattern='|'.join(re.escape(k) for k in sorted(INLINE,key=len,reverse=True))
        result=[];pos=0
        for m in re.finditer(pattern,text):
            result.append(html.escape(text[pos:m.start()]));result.append(math_html(INLINE[m[0]],True));pos=m.end()
        result.append(html.escape(text[pos:]));return ''.join(result)
    return f'<{tag} {attrs}><span data-lang="zh" lang="zh-CN">{rich(zh)}</span><span data-lang="en" lang="en" hidden>{rich(en)}</span></{tag}>'

def component_math(component):
    eq=component.get('eq')
    if not eq:return ''
    tex=eq if '\\' in eq else COMPONENTS[component['key']]
    return math_html(tex)

def cache_das_derivations():
    source=ROOT/'光纤传感原理'/'outputs'/'DAS_代表性光路图册.tex'
    if not source.exists():
        if not DATA.exists():raise FileNotFoundError('Missing full DAS derivation source')
        return
    text=source.read_text(encoding='utf-8')
    parts={};pattern=r'\\begin\{minipage\}\[t\]\{[^}]*\}(.*?)\\end\{minipage\}'
    for page in text.split(r'\newpage'):
        found=re.search(r'\\bfseries (0[1-9])\\quad',page)
        if found:
            columns=re.findall(pattern,page,re.S)
            if len(columns)!=2:raise ValueError('Expected both derivation columns: '+found[1])
            parts['DAS'+found[1]]=columns
        if '统一符号、器件变换与相位约定' in page:
            parts['conventions']=re.findall(pattern,page,re.S)
    if len(parts)!=10:raise ValueError('Full DAS source missing routes or conventions')
    DATA.write_text(json.dumps({'source':'original DAS editable TeX, full branch equations and conditions','routes':parts},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def latex_prose_to_html(body):
    tokens={}
    def token(fragment,block):
        key=f'MATHPLACEHOLDER{len(tokens):05d}';tokens[key]=fragment
        return '\n\n'+key+'\n\n' if block else key
    def display(match):
        tex=match.group(1) if match.group(1) is not None else r'\begin{aligned}'+match.group(2)+r'\end{aligned}'
        return token(math_html(tex),True)
    body=re.sub(r'\\\[(.*?)\\\]|\\begin\{align\*\}(.*?)\\end\{align\*\}',display,body,flags=re.S)
    body=re.sub(r'(?<!\\)\$(.*?)(?<!\\)\$',lambda m:token(math_html(m[1],True),False),body,flags=re.S)
    body=re.sub(r'\\sect\{([^{}]*)\}',lambda m:token('<h4>'+html.escape(m[1])+'</h4>',True),body)
    body=re.sub(r'\\textbf\{([^{}]*)\}',r'\1',body)
    body=re.sub(r'\\note\{([^{}]*)\}',lambda m:'\n\n说明：'+m[1]+'\n\n',body)
    body=body.replace(r'\par','\n\n').replace('本图册','这里').replace('此图册','这里')
    def restore(s):
        for _ in range(2):
            for key,value in tokens.items():s=s.replace(key,value)
        return s
    result=[]
    for paragraph in re.split(r'\n\s*\n',body.strip()):
        p=paragraph.strip()
        if not p:continue
        result.append(restore(p) if p in tokens else '<p>'+restore(html.escape(p))+'</p>')
    return '<div class="detailed-derivation">'+''.join(result)+'</div>'

def das_details(id):
    data=json.loads(DATA.read_text(encoding='utf-8'))
    return ''.join(latex_prose_to_html(column) for column in data['routes'][id])

def add_math_assets(content):
    if 'vendor/katex/katex.min.css' not in content:
        content=content.replace('</head>','<link rel="stylesheet" href="vendor/katex/katex.min.css"><link rel="stylesheet" href="math.css"><script defer src="vendor/katex/katex.min.js"></script><script defer src="math.js"></script></head>')
    return content

def upgrade_basic_principles():
    p=ROOT/'knowledge'/'dfos-principles.html';content=p.read_text(encoding='utf-8')
    # Preserve the explanations following the two existing average-strain equations.
    def avg(m):
        original=m[1]
        if 'ε̄' not in original:return m[0]
        note=re.search(r'<small>.*?</small>',original,re.S)
        tex=r'\overline{\varepsilon}(z,t)=\frac1{L_g}\int_{z-L_g/2}^{z+L_g/2}\varepsilon_{\mathrm{axial}}(s,t)\,\mathrm ds'
        return math_html(tex)+(note[0] if note else '')
    content=re.sub(r'<div class="equation">(.*?)</div>',avg,content,flags=re.S)
    p.write_text(add_math_assets(content),encoding='utf-8')

def validate_local_equations():
    from atlas_content import DTS,DSS
    for r in DTS+DSS:
        for s in r['steps']:
            if s['equation'] not in EQUATIONS:raise ValueError(r['id']+': '+s['equation'])

if __name__=='__main__':
    cache_das_derivations();validate_local_equations();upgrade_basic_principles()
    print('Cached full original DAS derivations and enabled local math rendering.')
