"""Deterministic SVG/PDF/HTML authoring. Run from any directory with Python.
Only final educational assets are placed under knowledge/atlases/.
"""
from pathlib import Path
import html, json, math, shutil, zipfile, hashlib, io
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from PIL import Image
from atlas_content import DTS, DSS, REFERENCES, TITLES, SPECIAL_COMPONENTS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'knowledge'/'atlases'
ORIGINAL=ROOT/'光纤传感原理'/'outputs'
QA=ROOT/'work'/'atlas-qa'
OUT.mkdir(exist_ok=True); QA.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('CN','C:/Windows/Fonts/msyh.ttc'))
pdfmetrics.registerFont(TTFont('CNB','C:/Windows/Fonts/msyhbd.ttc'))
INK='#122d40'; BLUE='#1765ad'; GREEN='#21836d'; ORANGE='#c36524'; PURPLE='#7b4db1'; MUTED='#566b79'
W,H=1200,540

def esc(s): return html.escape(str(s),quote=True)
def printable(s):
    # YaHei has no combining circumflex or much-less-than glyph; retain explicit meaning.
    return s.replace('h\u0302','h_hat').replace('≪','<<')
def bi(zh,en,tag='span',attrs=''):
    return f'<{tag} data-zh="{esc(zh)}" data-en="{esc(en)}" {attrs}>{esc(zh)}</{tag}>'

class Drawing:
    def __init__(self,c=None): self.c=c; self.svg=[]; self.boxes=[]; self.texts=[]
    def rect(self,x,y,w,h,fill='#f2f7fa',stroke=BLUE,r=7):
        if self.c:
            self.c.setFillColor(HexColor(fill));self.c.setStrokeColor(HexColor(stroke));self.c.setLineWidth(1.5)
            self.c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=1)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    def text(self,x,y,s,size=16,color=INK,anchor='start',bold=False):
        s=printable(s)
        font='CNB' if bold else 'CN'; width=pdfmetrics.stringWidth(s,font,size)
        self.texts.append((x,y,width,size,anchor,s))
        if self.c:
            self.c.setFont(font,size);self.c.setFillColor(HexColor(color));xx=x-width/2 if anchor=='middle' else x-width if anchor=='end' else x
            self.c.drawString(xx,H-y-size*.9,s)
        self.svg.append(f'<text x="{x}" y="{y+size*.9}" font-size="{size}" text-anchor="{anchor}" fill="{color}" font-weight="{700 if bold else 400}">{esc(s)}</text>')
    def path(self,pts,color=BLUE,dash=False,arrow=True,lw=2.5):
        if self.c:
            self.c.setStrokeColor(HexColor(color));self.c.setLineWidth(lw);self.c.setDash([6,5] if dash else [])
            p=self.c.beginPath();p.moveTo(pts[0][0],H-pts[0][1])
            for x,y in pts[1:]:p.lineTo(x,H-y)
            self.c.drawPath(p);self.c.setDash([])
        self.svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" stroke="{color}" fill="none" stroke-width="{lw}"'+(' stroke-dasharray="6 5"' if dash else '')+'/>')
        if arrow:
            x,y=pts[-1];a,b=pts[-2];theta=math.atan2(y-b,x-a)
            ps=[(x,y),(x-10*math.cos(theta)+4*math.sin(theta),y-10*math.sin(theta)-4*math.cos(theta)),(x-10*math.cos(theta)-4*math.sin(theta),y-10*math.sin(theta)+4*math.cos(theta))]
            if self.c:
                self.c.setFillColor(HexColor(color));p=self.c.beginPath();p.moveTo(ps[0][0],H-ps[0][1]);p.lineTo(ps[1][0],H-ps[1][1]);p.lineTo(ps[2][0],H-ps[2][1]);p.close();self.c.drawPath(p,fill=1,stroke=0)
            self.svg.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in ps)}" fill="{color}"/>')
    def box(self,x,y,w,label,h=54,color=BLUE):
        self.boxes.append((x,y,w,h,label));self.rect(x,y,w,h,stroke=color)
        lines=label.split('\n')
        for i,line in enumerate(lines):self.text(x+w/2,y+(h-len(lines)*20)/2+i*20,line,16,anchor='middle')
    def cir(self,x,y,far=False):
        if self.c:
            self.c.setFillColor(HexColor('#e9f2f9'));self.c.setStrokeColor(HexColor(BLUE));self.c.circle(x,H-y,32,fill=1,stroke=1)
        self.svg.append(f'<circle cx="{x}" cy="{y}" r="32" fill="#e9f2f9" stroke="{BLUE}" stroke-width="2"/>')
        self.text(x,y-9,'CIR',16,anchor='middle',bold=True)
        self.text(x-38,y-26,'2' if far else '1',13)
        self.text(x+31,y-26,'3' if far else '2',13)
        self.text(x+9,y+35,'1' if far else '3',13)
    def fiber(self,x1,x2,y,label='FUT · 感测光纤',back=True):
        self.path([(x1,y),(x2,y)],BLUE)
        if back:self.path([(x2-8,y+18),(x1+8,y+18),(x1,y)],ORANGE)
        self.text((x1+x2)/2,y-58,label,18,anchor='middle',bold=True)
        for x in range(int(x1+35),int(x2-15),35):
            self.path([(x,y-7),(x,y+7)],BLUE,arrow=False,lw=1)
    def save(self,path):
        path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img"><title>Representative optical schematic / 代表性光路概念图</title><rect width="1200" height="540" fill="white"/><g font-family="Microsoft YaHei,Arial,sans-serif">'+''.join(self.svg)+'</g></svg>',encoding='utf-8')
    def verify(self):
        errors=[]
        for x,y,w,s,a,t in self.texts:
            left=x-w/2 if a=='middle' else x-w if a=='end' else x
            if left<0 or left+w>W or y<0 or y+s>H:errors.append('text outside canvas: '+t)
        for i,(x,y,w,h,label) in enumerate(self.boxes):
            if not (0<=x<x+w<=W and 0<=y<y+h<=H):errors.append('box outside canvas: '+label)
            for xx,yy,ww,hh,other in self.boxes[:i]:
                if max(x,xx)<min(x+w,xx+ww)-1 and max(y,yy)<min(y+h,yy+hh)-1:errors.append(f'overlapping boxes: {label} / {other}')
        return errors

def diagram(route,c=None):
    d=Drawing(c);typ=route['topology']
    d.text(24,13,route['id']+'  '+route['name'],21,bold=True)
    d.text(24,45,route['en'],15,color=MUTED)
    if typ.startswith('raman'):
        d.box(35,142,128,'Laser / LD\n激光源');d.box(225,142,145,'Pulse / IM\n编码' if typ=='raman_coded' else 'Pulse / IM\n脉冲门控')
        d.path([(163,169),(225,169)]);d.text(185,142,'B0',14)
        d.path([(370,169),(448,169),(468,180)]);d.text(390,139,'B1',14);d.cir(500,180)
        d.box(225,77,145,'AWG / trigger',38,color=PURPLE);d.path([(297,115),(297,142)],PURPLE,True)
        if typ=='raman_double':
            d.path([(532,180),(615,180)]);d.box(615,152,105,'SW · A / B',56)
            # One physical U-shaped fiber, interrogated alternately at A and B.
            # Backscatter returns to the active end; it is not transmitted A→B light.
            d.path([(720,166),(760,166),(760,137),(1090,137),(1090,250),(760,250),(760,194),(720,194)],BLUE,arrow=False)
            d.path([(790,137),(970,137)],BLUE);d.path([(970,155),(790,155)],ORANGE)
            d.path([(790,250),(970,250)],BLUE);d.path([(970,268),(790,268)],ORANGE)
            d.path([(615,194),(555,194),(532,180)],ORANGE)
            d.text(850,93,'FUT · 同一光纤的两端',17);d.text(774,147,'A',15);d.text(775,228,'B',15)
            d.text(850,273,'交替测量 / alternate',15,color=MUTED)
        else:
            d.path([(532,180),(700,180)]);d.fiber(700,1135,180)
            d.text(824,217,'B2S / B2AS · Raman return',14,color=ORANGE)
        d.path([(500,212),(500,275)],ORANGE);d.box(425,275,150,'Raman WDM\n双谱带分离',60,color=GREEN)
        receiver='SNSPD / SPAD' if typ=='raman_count' else 'PD / APD + TIA'
        d.box(230,365,175,receiver+'\nStokes',58,color=GREEN);d.box(610,365,175,receiver+'\nanti-Stokes',58,color=PURPLE)
        d.path([(425,305),(317,305),(317,365)],GREEN);d.text(323,327,'B2S',14,color=GREEN)
        d.path([(575,305),(697,305),(697,365)],PURPLE);d.text(704,327,'B2AS',14,color=PURPLE)
        d.box(425,453,150,'TCSPC / TDC' if typ=='raman_count' else 'ADC · 同步采样',45,color=PURPLE)
        d.path([(317,423),(317,475),(425,475)],PURPLE,True);d.path([(697,423),(697,475),(575,475)],PURPLE,True)
        d.box(920,355,208,'REF bath + RTD\n参考温区 + 温度计',60,color=GREEN)
        d.path([(1024,355),(1024,250 if typ=='raman_double' else 198)],GREEN,True);d.text(1050,316,'thermal',12,color=GREEN)
        d.text(810,463,'Ratio → calibration → T(z)',16,color=INK)
    elif typ in ('botda','dpp','bofda','bocda'):
        d.box(24,145,125,'NLL + ISO\n同源激光');d.box(200,145,75,'1×2 OC')
        d.path([(149,172),(200,172)]);d.text(165,146,'B0',14)
        d.box(310,145,125,'IM · CW sine' if typ=='bofda' else 'IM · τ1 / τ2' if typ=='dpp' else 'CW pump' if typ=='bocda' else 'IM · pulse')
        d.box(466,145,100,'EDFA');d.box(600,145,60,'PC');d.cir(720,172)
        for x1,x2 in [(275,310),(435,466),(566,600),(660,688)]:d.path([(x1,172),(x2,172)])
        d.text(668,115,'Bp',14);d.fiber(752,1078,172,'FUT · pump → / ← probe')
        d.cir(1110,172,True);d.path([(1142,172),(1180,172)],BLUE);d.text(1142,119,'dump',13)
        d.path([(236,199),(236,367),(310,367)],BLUE)
        d.box(310,340,125,'SSB-EOM\nνs=νp-Δν');d.box(470,340,105,'BPF · νs')
        d.path([(435,367),(470,367)]);d.text(440,391,'Bs',14,color=GREEN)
        if typ=='bocda':
            d.box(610,340,140,'Delay · 延迟');d.path([(575,367),(610,367)]);d.path([(750,367),(1110,367),(1110,204)],GREEN)
            d.box(24,77,125,'FM driver',38,color=PURPLE);d.path([(86,115),(86,145)],PURPLE,True)
        else:
            d.box(620,340,70,'PC');d.path([(575,367),(620,367)]);d.path([(690,367),(1110,367),(1110,204)],GREEN)
        d.path([(720,204),(720,245)],GREEN);d.box(653,245,135,'PD + TIA\nprobe out',58,color=GREEN)
        d.box(841,245,145,'VNA / lock-in' if typ=='bofda' else 'ADC / DAQ',58,color=PURPLE);d.path([(788,274),(841,274)],PURPLE,True)
        d.text(950,325,'i(t, Δν)' if typ!='bofda' else 'H(fm, Δν)',14,color=PURPLE)
        if typ=='bofda':
            d.box(310,442,220,'VNA output · fm',42,color=PURPLE);d.path([(420,442),(420,415),(292,415),(292,126),(370,126),(370,145)],PURPLE,True)
        elif typ!='bocda':
            d.box(310,78,125,'AWG / gate',38,color=PURPLE);d.path([(372,116),(372,145)],PURPLE,True)
        d.box(620,442,190,'RF · scan Δν',42,color=PURPLE);d.path([(620,463),(595,463),(595,495),(280,495),(280,413),(375,413),(375,394)],PURPLE,True)
        d.text(872,454,'BFS → ΔT / Δεfiber',17)
    elif typ in ('botdr','twcotdr'):
        d.box(25,145,155,'NLL + optical scan' if typ=='twcotdr' else 'NLL + ISO');d.box(220,145,85,'1×2 OC')
        d.path([(180,172),(220,172)]);d.text(185,140,'B0',14)
        d.box(355,145,130,'IM · pulse');d.box(525,145,115,'EDFA' if typ=='botdr' else 'launch');d.cir(735,172)
        for a,b in [(305,355),(485,525),(640,703)]:d.path([(a,172),(b,172)])
        d.text(660,141,'Bp',14);d.fiber(767,1140,172)
        d.path([(735,204),(735,255)],ORANGE);d.box(663,255,145,'BPF · Brillouin' if typ=='botdr' else 'Rayleigh return',58,color=ORANGE)
        d.path([(735,313),(735,365)],ORANGE);d.box(657,365,155,'2×2 OC + BPD\n相干接收',58,color=GREEN)
        if typ=='botdr':
            d.path([(262,199),(262,394),(340,394)],GREEN);d.box(340,365,215,'SSB-EOM + BPF\nLO frequency shift',58,color=GREEN)
            d.path([(555,394),(657,394)],GREEN);d.text(576,366,'BL',16,color=GREEN)
        else:
            d.path([(262,199),(262,394),(657,394)],GREEN);d.text(300,366,'BL · local oscillator',16,color=GREEN)
        d.box(930,365,155,'ADC / spectra',58,color=PURPLE);d.path([(812,394),(930,394)],PURPLE,True)
        d.box(355,78,130,'AWG / trigger',38,color=PURPLE);d.path([(420,116),(420,145)],PURPLE,True)
        d.text(25,465,'BOTDR: spontaneous Brillouin / 自发布里渊' if typ=='botdr' else 'Step νm between pulses / 脉冲之间步进光频',17)
        d.text(810,455,'i(t, νm) → local spectrum',16)
    elif typ=='ofdr':
        d.box(25,145,150,'TLS · ν sweep');d.box(225,145,85,'1×2 OC');d.cir(500,172)
        d.path([(175,172),(225,172)]);d.text(184,140,'B0',14)
        d.box(355,145,75,'Tap OC');d.path([(310,172),(355,172)]);d.path([(430,172),(468,172)]);d.text(438,141,'B1',14)
        d.fiber(532,1110,172,'FUT · Rayleigh fingerprint')
        d.path([(500,204),(500,335),(640,335)],ORANGE);d.text(520,301,'B2 · return',15,color=ORANGE)
        d.path([(267,199),(267,380),(355,380)],GREEN);d.box(355,354,160,'Reference arm\n参考光程',56,color=GREEN)
        d.path([(515,382),(610,382),(640,358)],GREEN);d.text(530,398,'BL',15,color=GREEN)
        d.box(640,318,120,'2×2 OC',62,color=GREEN);d.box(840,318,115,'BPD',62,color=GREEN)
        d.path([(760,338),(840,338)],GREEN);d.path([(760,360),(840,360)],ORANGE)
        d.box(1040,318,130,'ADC / DAQ',62,color=PURPLE);d.path([(955,349),(1040,349)],PURPLE,True)
        d.path([(392,145),(392,82),(420,82)],BLUE);d.box(420,56,270,'Aux MZI + PD\n扫频非线性校正',54)
        d.path([(690,83),(1150,83),(1150,318)],PURPLE,True);d.text(838,59,'k-clock / resample',15,color=PURPLE)
        d.text(25,457,'Beat → distance FFT → local spectral correlation',18)
    d.text(24,518,'Blue=launch / 蓝:发射  Orange/green=return/probe / 橙绿:回波/探测  Purple dashed=electrical / 紫虚线:电学  Green dashed=thermal / 绿虚线:温度参考',11,color=MUTED)
    return d

def make_components():
    shared=OUT/'shared';shared.mkdir(exist_ok=True)
    catalogue=ORIGINAL/'DAS_元件实物与作用.json'
    cached=shared/'components-source.json'
    if catalogue.exists():
        source=json.loads(catalogue.read_text(encoding='utf-8'))
        cached.write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    else:
        source=json.loads(cached.read_text(encoding='utf-8'))
    needed={k for r in DTS+DSS for k in r['components']}; comps=[]
    names={
      'ld':('Pulsed laser source','选择与拉曼谱带、脉冲能量及光纤匹配的光源；照片为封装示例，不保证适合所有拉曼系统。','Select a laser matched to Raman bands, pulse energy, and fiber. The package photo does not certify suitability for every Raman system.'),
      'fiber':('Sensing fiber / cable','拉曼、布里渊或瑞利散射介质；单模/多模、涂覆与光缆结构按测量机制选择。','The Raman/Brillouin/Rayleigh scattering medium; choose mode count, coating, and cable design for the mechanism.'),
      'bpf':('Optical bandpass filter','选出布里渊或调制边带，抑制 ASE；拉曼双谱带用专用 WDM，不能直接复用该滤波器。','Select Brillouin/modulation bands and reject ASE. Raman requires dedicated dual-band filters.'),
      'iq':('Single-sideband optical modulator','生成可扫描的光频差；须选边带、抑载波并稳定偏置。','Generate a scanned optical-frequency offset; select a sideband, suppress the carrier, and stabilize bias.'),
      'im':('Intensity modulator / pulse gate','生成脉冲、编码或小信号强度调制；记录脉冲边沿、消光比和调制深度。','Generate pulses, codes, or small-signal intensity modulation; characterize edges, extinction, and modulation depth.'),
      'pd':('Photoreceiver + TIA','探测 BOTDA 探测光输出，或辅助干涉仪信号；光谱响应与带宽按支路匹配。','Detect BOTDA probe output or auxiliary interferometer signals; match spectral response and bandwidth.'),
      'computer':('Host computation','完成比值标定、谱拟合、傅里叶变换、相关与误差传播；算法不是光学元件。','Perform calibration, spectral fitting, Fourier transforms, correlation, and uncertainty propagation; algorithms are not optical components.'),
    }
    english={'nll':'Narrow-linewidth laser','ld_driver':'Laser current / TEC controller','awg':'Waveform / trigger generator','cir':'Three-port optical circulator','adc':'Synchronous digitizer','iso':'Optical isolator','splitter':'Optical splitter','edfa':'Erbium-doped optical amplifier','pc':'Polarization controller','dds':'RF frequency synthesizer','bias':'Modulator bias controller','tls':'Swept tunable laser','coupler2_dk':'2×2 optical coupler','delay':'Reference / delay fiber','bpd':'Balanced photoreceiver','fpga':'Digital processing hardware'}
    roles_en={
      'nll':'Provide a coherent source for Brillouin interrogation and a same-source local oscillator; stability and linewidth affect spectral estimation.',
      'iso':'Pass launch light and suppress optical feedback into the laser.',
      'splitter':'Divide source power into pump/probe or measurement/reference arms; include splitting loss in the power budget.',
      'coupler2_dk':'Mix return and reference fields into two complementary outputs for balanced detection.',
      'cir':'Route port 1 to 2 for launch and port 2 to 3 for returning probe/backscatter.',
      'edfa':'Amplify the selected launch band; account for ASE, gain dynamics, and nonlinear effects.',
      'pc':'Control polarization to reduce coherent fading and variation of Brillouin gain.',
      'bpd':'Subtract two complementary receiver currents to extract coherent mixing while reducing common-mode intensity noise.',
      'adc':'Sample synchronized receiver voltages; characterize sampling interval, bandwidth, and trigger delay.',
      'awg':'Generate synchronized pulse gates, codes, or sinusoidal modulation for the selected route.',
      'dds':'Set the RF drive frequency for optical sideband generation and pump-probe detuning scans.',
      'ld_driver':'Drive laser current and temperature; calibrate how these settings affect optical frequency and power.',
      'bias':'Stabilize the operating point of MZ/IQ modulators and suppress undesired carrier/sideband leakage.',
      'fpga':'Implement timing, coding, and digital processing; the algorithm is hosted by electronics rather than a separate optical device.',
      'tls':'Sweep optical frequency continuously for OFDR; an auxiliary interferometer measures scan nonlinearity.',
      'delay':'Set an optical reference delay or the modulation correlation offset; actual delay requires calibration.',
    }
    roles_zh={
      'nll':'提供相干光源与同源本振；光频稳定度及线宽影响布里渊和瑞利谱估计。',
      'iso':'允许发射方向传光，抑制反向反馈进入激光器。',
      'splitter':'将源光分到泵浦/探测或测量/参考支路；分光比与插入损耗需计入功率预算。',
      'coupler2_dk':'把回波与参考光混合成两条互补输出，供平衡检测。',
      'cir':'发射时端口 1→2；回波或反向探测光由端口 2→3 接入接收器。',
      'edfa':'放大选定的发射谱带；考虑 ASE、增益动态及非线性效应。',
      'pc':'控制偏振，减少相干衰落及布里渊增益变化；不能保证所有位置始终匹配。',
      'bpd':'对互补输出的光电流作差，提取相干混频并减小共模强度噪声。',
      'adc':'同步采样接收电压；标定采样间隔、带宽和触发零点。',
      'awg':'按路线产生同步脉冲门控、发射码或小信号正弦调制。',
      'dds':'设置射频驱动频率，控制光学边带及泵浦-探测光频差扫描。',
      'ld_driver':'提供激光电流与温控；须标定驱动参数对光频和功率的实际影响。',
      'bias':'稳定 MZ / IQ 调制器工作点，控制载波与非目标边带泄漏。',
      'fpga':'执行时序、编码和数字处理；算法依托电子硬件，不是独立光学元件。',
      'tls':'连续扫描光频供 OFDR 使用；辅助干涉仪记录扫频非线性。',
      'delay':'设置参考光程或相关域调制延迟；实际延迟需标定。',
    }
    equations={
      'nll':'B0(t)=sqrt(P0) exp[i(2πν0t+φL)]', 'ld':'B1(t)=sqrt(P0) a(t)',
      'tls':'ν(t)=ν0+κt', 'iso':'Pforward=Tiso Pin; Treverse≪Tiso',
      'splitter':'P1≈ηPin; P2≈(1-η)Pin', 'coupler2_dk':'Bout=U2×2 Bin',
      'cir':'port 1 → 2; port 2 → 3', 'edfa':'Pout≈G Pin+PASE',
      'bpf':'Bout(ν)=Hopt(ν) Bin(ν)', 'im':'Bpulse(t)=a(t) B0(t)',
      'iq':'νs=νp-Δν (selected sideband)', 'pc':'Bout=JPC Bin',
      'fiber':'treturn≈2ngz/c (calibrated origin)', 'delay':'τarm=ng Larm/c (one way)',
      'pd':'i=R P+b; V=ZT*i', 'bpd':'idiff=R(P+ - P-)',
      'adc':'V[k]=V(t0+k ΔtADC)', 'awg':'Vdrive(t)=programmed waveform',
      'dds':'fRF=programmed frequency', 'ld_driver':'νlaser=f(I,Tlaser)',
      'bias':'VMZ=Vbias+Vdrive', 'fpga':'ĥ=D y (example: code decoding)',
      'computer':'observable → calibration → uncertainty',
    }
    for v in source:
        if v['key'] not in needed:continue
        v=dict(v);v['en']=english.get(v['key'],v['abbr']);v['role_en']='See the optical branch and calibration conditions for the selected route.';v['note_en']='Manufacturer appearance example; wavelength, bandwidth, and packaging need separate selection.'
        if v['key'] in names:v['en'],v['role'],v['role_en']=names[v['key']]
        if v['key'] in roles_en:v['role_en']=roles_en[v['key']]
        if v['key'] in roles_zh:v['role']=roles_zh[v['key']]
        # Strip obsolete DAS route numbers and equations from reused catalogue entries.
        v.pop('routes',None);v['eq']=equations[v['key']]
        v['note']='厂家外观示例，非性能推荐；须另行核对波长、带宽、光功率及实际封装。'
        v['image_kind']='manufacturer_photo';v['source_url']=v['photo']['page']
        v['asset']='shared/'+v['id']+'.png'
        source_image=ORIGINAL/('DAS_元件实物图片/'+v['id']+'.png')
        if source_image.exists():shutil.copy2(source_image,shared/(v['id']+'.png'))
        elif not (shared/(v['id']+'.png')).exists():raise FileNotFoundError(v['asset'])
        comps.append(v)
    for i,v in enumerate(SPECIAL_COMPONENTS,1):
        v=dict(v);v['id']=f'X{i:02}';v['image_kind']='functional_schematic';v['source_url']=None;v['asset']='shared/'+v['id']+'.svg'
        (shared/(v['id']+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 180"><rect width="400" height="180" rx="12" fill="#edf4f8"/><path d="M20 90H100M300 90H380" stroke="{BLUE}" stroke-width="4"/><rect x="100" y="35" width="200" height="110" rx="8" fill="white" stroke="{BLUE}" stroke-width="2"/><text x="200" y="88" text-anchor="middle" font-family="Arial" font-size="18" fill="{INK}">{esc(v["abbr"])}</text><text x="200" y="122" text-anchor="middle" font-family="Microsoft YaHei,Arial" font-size="14" fill="{MUTED}">功能示意 / schematic</text></svg>',encoding='utf-8')
        comps.append(v)
    return comps

def paragraph(c,x,y,text,width,size=11,leading=17,color=INK,font='CN'):
    text=printable(text)
    c.setFont(font,size);c.setFillColor(HexColor(color));line=''
    for char in text:
        if line and char in '，。；：！？、,;:!?)]}' and pdfmetrics.stringWidth(line+char,font,size)>width:
            c.drawString(x,y,line+char);y-=leading;line='';continue
        if char=='\n' or pdfmetrics.stringWidth(line+char,font,size)>width:
            c.drawString(x,y,line);y-=leading;line='' if char=='\n' else char
        else:line+=char
    if line:c.drawString(x,y,line);y-=leading
    return y

def make_pdf(kind,routes,comps):
    out=OUT/kind;out.mkdir(exist_ok=True)
    name=kind.upper()+'_原理光路图册.pdf';c=canvas.Canvas(str(out/name),pagesize=(842,595));c.setTitle(TITLES[kind][0]);c.setAuthor('Junhao Hu · educational notes')
    page=0
    def begin(title,subtitle=''):
        nonlocal page;page+=1
        c.setFillColor(HexColor(INK));c.rect(0,550,842,45,fill=1,stroke=0);c.setFillColor(HexColor('#ffffff'));c.setFont('CNB',17);c.drawString(32,566,title)
        if subtitle:paragraph(c,32,532,subtitle,770,10,15,MUTED)
    def end():
        c.setStrokeColor(HexColor('#d9e2e8'));c.line(32,38,810,38);c.setFont('CN',8);c.setFillColor(HexColor(MUTED));c.drawString(32,23,'概念示意 / Not to scale · 非实测 / No measured data · 2026-10-06');c.drawRightString(810,23,str(page));c.showPage()
    begin(TITLES[kind][0],TITLES[kind][1]);y=494
    y=paragraph(c,32,y,TITLES[kind][2],770,15,24)
    for r in routes:
        y-=12;y=paragraph(c,32,y,r['id']+' · '+r['name']+' / '+r['en'],770,12,19)
        y=paragraph(c,55,y,r['observable'],747,10,16,MUTED)
    paragraph(c,32,87,'阅读顺序：元件 → 光路 → 支路公式 → 标定与限制 → 原始来源。光学分辨率、应变标距、采样间距分别定义。',775,10,16);end()
    used=[v for v in comps if any(v['key'] in r['components'] for r in routes)]
    for i in range(0,len(used),4):
        begin('元件与作用 / Components', '厂家照片仅作外观示例；X 编号为原创功能示意，明确区分，未冒充实物照片。')
        for j,v in enumerate(used[i:i+4]):
            x=32+(j%2)*395;top=490-(j//2)*215
            c.setFillColor(HexColor('#f5f8fa'));c.roundRect(x,top-183,380,198,8,fill=1,stroke=0)
            paragraph(c,x+12,top,v['id']+' · '+v['name'],352,11,17,font='CNB')
            paragraph(c,x+12,top-24,v['eq'],352,8.5,12,BLUE)
            if v['image_kind']=='manufacturer_photo':c.drawImage(str(OUT/v['asset']),x+14,top-118,width=112,height=83,preserveAspectRatio=True,anchor='c',mask='auto')
            else:
                c.setStrokeColor(HexColor(BLUE));c.roundRect(x+14,top-104,110,58,5,fill=0,stroke=1);paragraph(c,x+22,top-65,v['abbr'],95,9,13);paragraph(c,x+19,top-91,'功能示意',95,9,13,MUTED)
            yy=paragraph(c,x+138,top-45,v['role'],230,10,15)
            paragraph(c,x+138,yy-4,v['note'],230,8.7,13,MUTED)
            if v['source_url']:
                paragraph(c,x+12,top-143,v.get('maker','')+' · '+v.get('model',''),350,8,12,MUTED)
                c.linkURL(v['source_url'],(x+12,top-176,x+367,top-144),relative=0)
                paragraph(c,x+12,top-166,'来源：厂家产品页（点击本区域）',350,8,11,BLUE)
        end()
    begin('统一符号、标定与解释边界 / Shared conventions')
    notes=[
      'B0：源场；B1 / Bp：入纤探测或泵浦；Bs：反向连续探测光；BL：本振或参考；B2：散射回波。i 是接收电流；功率记 P。',
      't：发射后采样时间；z：沿光纤距离；c：真空光速；ng：群折射率（拉曼为发射/接收通道的有效值，需校准）；τp：脉宽；ν：光频；Δν：泵浦与探测光频差；fm：电调制频率。',
      '温度 T 使用 K；温差 ΔT 的数值可用 K 或 °C。应变 εfiber 是无量纲；1 με = 10^-6。温度/应变灵敏度须用实际光纤与封装标定。',
      'ΔνB = Cε Δεfiber + CT ΔT：一次频移只有一个独立方程，不能同时唯一确定温度与应变。',
      '瑞利指纹：δν 定义当前谱相对参考的光频移；q=-δν/ν0。通常拉伸红移，δν<0、q>0。相关实现必须与这一符号约定一致。',
      '空间分辨率是对相邻变化的区分能力；标距是应变估计的窗口长度；采样间距是输出坐标间隔。三者不能互换。',
      'εfiber ≠ εhost：涂覆、光缆、黏结、滑移、剪滞和热膨胀改变应变传递。温度补偿后也不能未经验证直接宣称结构应变。',
      '所有光路是选定代表架构，非施工图；谱拟合、相关和数值自检不等于仪器性能或实验验证。DTS 死水段对齐：纯原理图，无现场输入，不适用。',
    ];y=507
    for n in notes:y=paragraph(c,32,y,n,778,12,19)-12
    end()
    for r in routes:
        begin(r['id']+' · '+r['name'],r['en'])
        c.saveState();c.translate(28,152);c.scale(786/W,786/W);diagram(r,c);c.restoreState()
        paragraph(c,32,126,r['summary'],778,11,17)
        paragraph(c,32,86,'解释边界：'+r['limits'],778,10,16,ORANGE);end()
        begin(r['id']+' · 支路公式 / Branch equations',r['observable']+' / '+r['obs_en'])
        y=503
        for s in r['steps']:
            y=paragraph(c,32,y,s['label'],778,10.5,15,BLUE,font='CNB')
            y=paragraph(c,32,y-2,s['equation'],778,11.5,18)
            y=paragraph(c,32,y-1,s['zh'],778,10,15,MUTED)-12
        if y<49:raise ValueError(f'Formula PDF page overflow: {r["id"]} bottom={y}')
        for k in r['refs']:
            c.linkURL(REFERENCES[k]['url'],(32,40,805,52),relative=0)
        end()
    refkeys=list(dict.fromkeys(k for r in routes for k in r['refs']))
    for i in range(0,len(refkeys),5):
        begin('原始来源与证据范围 / Primary sources');y=501
        for k in refkeys[i:i+5]:
            ref=REFERENCES[k];y=paragraph(c,32,y,ref['title'],778,11,17)
            y=paragraph(c,32,y-2,ref['url'],778,9,14,BLUE)
            c.linkURL(ref['url'],(32,y,805,y+17),relative=0)
            y=paragraph(c,32,y-2,ref['evidence'],778,9,14,MUTED)-20
        end()
    c.save();return name,page

def header():
    home=(ROOT/'index.html').read_text(encoding='utf-8')
    h=home[home.index('<header>'):home.index('</header>')+9]
    h=h.replace('href="#','href="../index.html#').replace('href="knowledge/index.html"','href="index.html"').replace('href="notes/','href="../notes/').replace('href="datasets/','href="../datasets/')
    return h

def shell(title,en,body,extra=''):
    return f'<!doctype html><html lang="zh-CN" data-title-zh="{esc(title)} · 胡俊昊" data-title-en="{esc(en)} · Junhao Hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · 胡俊昊</title><meta name="description" content="{esc(title)}：元件、代表性光路、支路公式与解释边界。"><link rel="icon" href="../favicon.svg"><link rel="stylesheet" href="../style.css"><link rel="stylesheet" href="knowledge.css"><link rel="stylesheet" href="atlas.css"></head><body><a class="skip" href="#main">跳至正文 / Skip to content</a>{header()}<main id="main">{body}</main><footer>{bi("胡俊昊 / Junhao Hu","Junhao Hu / 胡俊昊")}<a href="index.html">{bi("返回知识目录","Back to Knowledge")}</a><span>© 2026 Junhao Hu</span></footer><script src="../app.js"></script>{extra}</body></html>'

def atlas_html(kind,routes,comps,pdfname):
    title,en,zhdesc,endesc=TITLES[kind]
    body='<section class="article-hero"><div class="breadcrumbs"><a href="../index.html">'+bi('首页','Home')+'</a> / <a href="index.html">'+bi('知识','Knowledge')+'</a> / '+kind.upper()+'</div>'+bi('仪器原理 · 元件 / 光路 / 公式','INSTRUMENT PRINCIPLES · COMPONENTS / PATHS / EQUATIONS',attrs='class="eyebrow"')+bi(title,en,'h1')+bi(zhdesc,endesc,'p','class="lede"')
    body+='<div class="atlas-links"><a class="primary" href="atlases/'+kind+'/'+pdfname+'">PDF 图册 / PDF atlas</a><a href="atlases/'+kind+'/'+kind.upper()+'_资料包.zip">SVG + PNG + 源码 / Source package</a><a href="das-optical-atlas.html">DAS</a><a href="'+('dss' if kind=='dts' else 'dts')+'-optical-atlas.html">'+('DSS' if kind=='dts' else 'DTS')+'</a></div></section>'
    body+='<section class="atlas-controls" aria-label="Atlas controls"><label for="route-filter">'+bi('路线筛选','Route filter')+'</label><select id="route-filter"><option value="all" data-zh="全部路线" data-en="All routes">全部路线</option>'
    for r in routes:body+=f'<option value="{r["id"]}" data-zh="{esc(r["id"]+" · "+r["name"])}" data-en="{esc(r["id"]+" · "+r["en"])}">{esc(r["id"]+" · "+r["name"])}</option>'
    body+='</select><div class="atlas-tabs" role="group" aria-label="Content"><button type="button" data-view="components" aria-pressed="false">'+bi('元件与作用','Components')+'</button><button type="button" data-view="routes" aria-pressed="true">'+bi('光路与公式','Paths & equations')+'</button><button type="button" data-view="conventions" aria-pressed="false">'+bi('标定与来源','Calibration & sources')+'</button></div><output id="atlas-status" aria-live="polite"></output></section>'
    body+='<section id="view-components" hidden><p>'+bi('照片为已有 DAS 图册中的厂家外观示例；X 编号为原创功能示意，明确区分。具体器件需按测量波长、谱带和带宽选型。','Photos reuse manufacturer appearance examples from the DAS atlas. X-numbered images are original functional schematics. Select actual devices for wavelength, bands, and bandwidth.')+'</p><div class="component-grid">'
    for v in comps:
        relevant=[r['id'] for r in routes if v['key'] in r['components']]
        if not relevant:continue
        isphoto=v['image_kind']=='manufacturer_photo'
        body+=f'<article class="component" data-routes="{" ".join(relevant)}"><div class="component-head"><strong>{v["id"]} · {esc(v["abbr"])}</strong>{bi("厂家外观" if isphoto else "功能示意","Manufacturer image" if isphoto else "Functional schematic",attrs="class=asset-kind")}</div><button class="image-zoom" type="button" data-zoom="atlases/{esc(v["asset"])}" aria-label="放大 / Enlarge"><img loading="lazy" src="atlases/{esc(v["asset"])}" alt="{esc(v["name"])}" data-alt-zh="{esc(v["name"])}" data-alt-en="{esc(v["en"])}" width="400" height="180"></button>'+bi(v['name'],v['en'],'h2')+'<div class="component-equation">'+esc(v['eq'])+'</div>'+bi(v['role'],v['role_en'],'p')+bi(v['note'],v['note_en'],'p','class="component-note"')
        if isphoto:body+=f'<a href="{esc(v["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(v.get("maker",""))} · '+bi('原始来源 ↗','Original source ↗')+'</a>'
        else:body+=bi('原创功能示意；不是实物照片。','Original functional illustration; not a product photo.','small')
        body+='</article>'
    body+='</div></section><section id="view-routes">'
    for r in routes:
        body+=f'<article class="atlas-route" id="{r["id"]}" data-route="{r["id"]}"><div class="route-top"><span>{r["id"]} · {r["mechanism"]}</span>'+bi(r['name'],r['en'],'h2')+'</div>'+bi(r['summary'],r['sum_en'],'p')+f'<figure class="route-figure"><button class="image-zoom" type="button" data-zoom="atlases/{kind}/figures/{r["id"]}.svg" aria-label="放大光路 / Enlarge path"><img src="atlases/{kind}/figures/{r["id"]}.svg" alt="{esc(r["name"])}" data-alt-zh="{esc(r["name"])}" data-alt-en="{esc(r["en"])}" width="1200" height="540" loading="lazy"></button><figcaption>'+bi('代表性概念架构，非按比例、非实测；蓝色为发射，橙/绿色为回波或探测；紫虚线为电学，绿虚线为参考温区。','Representative conceptual architecture, not to scale or measured data. Blue: launch; orange/green: return or probe; purple dashed: electrical; green dashed: thermal reference.')+'</figcaption></figure><p class="observable">'+bi('直接观测：'+r['observable'],'Observable: '+r['obs_en'])+'</p><details class="formula-details" open><summary>'+bi('支路公式与解调过程','Branch equations & processing')+'</summary><ol class="formula-steps">'
        for s in r['steps']:
            body+='<li><h3>'+esc(s['label'])+'</h3><div class="equation">'+esc(s['equation'])+'</div>'+bi(s['zh'],s['en'],'p')+'</li>'
        body+='</ol></details><aside class="callout">'+bi('解释边界：'+r['limits'],'Interpretation limits: '+r['limits_en'],'p')+'</aside><p class="route-sources">'+bi('依据：','Sources: ')
        for k in r['refs']:body+=f'<a href="{esc(REFERENCES[k]["url"])}" target="_blank" rel="noopener noreferrer">{esc(REFERENCES[k]["title"].split(". ")[0])}</a> '
        body+='</p></article>'
    body+='</section><section id="view-conventions" hidden><div class="convention-grid"><article><h2>'+bi('统一符号与参考状态','Symbols & reference states')+'</h2>'+bi('温度 T 使用 K；温差 ΔT 可用 K 或 °C。应变无量纲，1 με = 10⁻⁶。B 表示复光场，P 为功率，i 为电流；t 为往返时延，z 为沿纤距离。','T is in kelvin; ΔT may use K or °C. Strain is dimensionless; 1 με = 10⁻⁶. B is complex field, P power, i current; t is round-trip delay and z fiber distance.','p')+bi('ν 是光频，Δν 是泵浦-探测光频差；fm 是电学调制频率。瑞利 δν 是当前谱相对参考的有符号光频移，q = -δν/ν0。','ν is optical frequency, Δν pump-probe optical detuning, and fm electrical modulation frequency. Rayleigh δν is the signed current-minus-reference optical-frequency shift; q = -δν/ν0.','p')+'</article><article><h2>'+bi('三个空间尺度','Three spatial scales')+'</h2>'+bi('光学分辨率、应变标距与采样间距分别定义。不能把密集输出点、差分脉宽尺度或细时间箱，直接当作已验证的分辨率。','Optical resolution, strain gauge length, and sample spacing are distinct. Dense output points, pulse-width differences, or narrow time bins do not prove resolution.','p')+'</article><article><h2>'+bi('温度—应变解耦','Temperature–strain separation')+'</h2><div class="equation">ΔνB = Cε Δεfiber + CT ΔT<br>q = Kε Δεfiber + KT ΔT</div>'+bi('每个频移提供一个方程；两个未知量需要独立观测或明确约束。灵敏度与符号按实际光纤、封装、参考状态标定。','Each shift supplies one equation. Two unknowns need independent observations or explicit constraints; calibrate sensitivities and signs for fiber, packaging, and reference.','p')+'</article><article><h2>'+bi('光纤应变到结构应变','Fiber strain to structural strain')+'</h2><div class="equation">εfiber ≠ εhost</div>'+bi('涂覆、黏结、滑移、剪滞及热膨胀改变传递关系。温度补偿只处理一部分交叉敏感，不能替代机械耦合验证。','Coating, bonding, slip, shear lag, and thermal expansion alter transfer. Temperature compensation cannot replace mechanical-coupling validation.','p')+'</article></div><h2>'+bi('原始来源','Primary sources')+'</h2><ol class="references">'
    for k in dict.fromkeys(k for r in routes for k in r['refs']):
        ref=REFERENCES[k];body+=f'<li><a href="{esc(ref["url"])}" target="_blank" rel="noopener noreferrer">{esc(ref["title"])}</a><small>{esc(ref["evidence"])}</small></li>'
    body+='</ol><p class="knowledge-disclaimer">'+bi('这是原理教学资料。光路与简化公式经过结构和数值自检；未进行仪器搭建、实验性能验证或现场解释。DTS 死水段对齐：纯原理示意，无现场输入，不适用。','Educational principles material. Schematics and simplified equations undergo structural/numerical checks; no instrument construction, experimental performance, or field interpretation is claimed. DTS dead-water alignment is inapplicable to these input-free principles diagrams.')+'</p></section><dialog id="atlas-zoom"><button type="button" id="zoom-close" aria-label="关闭 / Close">×</button><img id="zoom-image" alt=""><p id="zoom-caption"></p></dialog>'
    return shell(title,en,body,'<script src="atlas.js"></script>')

def integrate_das():
    target=OUT/'das';target.mkdir(exist_ok=True)
    files=['DAS_光路交互图册.html','DAS_代表性光路图册_标号修订.pdf','DAS_全部单图_SVG_PNG.zip','DAS_元件实物来源.md','DAS_图册说明.json']
    for name in files:
        if (ORIGINAL/name).exists():shutil.copy2(ORIGINAL/name,target/name)
        elif not (target/name).exists():raise FileNotFoundError(name)
    # Keep existing diagrams/formulas unmodified. Add a Knowledge return link to the standalone viewer.
    p=target/files[0];content=p.read_text(encoding='utf-8')
    if '../../das-optical-atlas.html' not in content:content=content.replace('<body>','<body><p style="padding:12px 24px;margin:0;background:#eef4f7"><a href="../../das-optical-atlas.html">← 返回 DAS 知识页 / Back to DAS Knowledge</a></p>',1)
    p.write_text(content,encoding='utf-8')
    body='<section class="article-hero"><div class="breadcrumbs"><a href="index.html">'+bi('知识','Knowledge')+'</a> / DAS</div>'+bi('DAS 光路与原理图册','DAS optical-path and principles atlas','h1')+bi('已有项目正式接入知识栏目：35 类元件、九类代表性光路、逐支路公式与 21 页 PDF。','The existing project joins Knowledge: 35 components, nine representative paths, branch equations, and a 21-page PDF.','p','class="lede"')+'<div class="atlas-links"><a class="primary" href="atlases/das/DAS_光路交互图册.html">'+bi('打开交互图册','Open interactive atlas')+'</a><a href="atlases/das/DAS_代表性光路图册_标号修订.pdf">PDF 图册</a><a href="atlases/das/DAS_全部单图_SVG_PNG.zip">SVG / PNG / TikZ 素材包</a></div></section><section class="knowledge-guide"><article><h2>'+bi('内容与阅读顺序','Contents & reading order')+'</h2>'+bi('先认识激光器、调制器、环形器、耦合器、接收器和采集硬件，再按光路浏览发射、回波、混频和应变解调。图册可按路线筛选元件、切换公式并放大查看。','Start with lasers, modulators, circulators, couplers, receivers, and acquisition hardware; then trace launch, return, mixing, and strain recovery. Filter components by route, switch formulas, and zoom diagrams.','p')+'</article><article><h2>'+bi('原理与解释边界','Principles & limits')+'</h2>'+bi('DAS 通常恢复沿纤动态应变或应变率；声压转换取决于光缆与机械耦合。光学分辨率、标距与通道间距必须区分。图示为概念图，非实测数据。','DAS typically recovers dynamic axial fiber strain or strain rate; conversion to pressure depends on cable/mechanical coupling. Distinguish optical resolution, gauge length, and channel spacing. The diagrams are conceptual, not measurements.','p')+'</article></section><section class="knowledge-grid"><article class="topic-card"><h2>DTS</h2>'+bi('温度传感：元件、光路和标定。','Temperature sensing: components, paths, and calibration.','p')+'<a class="card-link" href="dts-optical-atlas.html">'+bi('进入 DTS 图册','Explore DTS')+'</a></article><article class="topic-card"><h2>DSS</h2>'+bi('应变传感：布里渊、瑞利和温度补偿。','Strain sensing: Brillouin, Rayleigh, and temperature compensation.','p')+'<a class="card-link" href="dss-optical-atlas.html">'+bi('进入 DSS 图册','Explore DSS')+'</a></article></section>'
    (ROOT/'knowledge'/'das-optical-atlas.html').write_text(shell('DAS 光路与原理图册','DAS optical-path and principles atlas',body),encoding='utf-8')
    return files

def update_knowledge():
    topics=json.loads((ROOT/'knowledge'/'topics.json').read_text(encoding='utf-8'))
    new=[('das','DAS 光路与原理图册','DAS optical-path and principles atlas','35 类元件、九类光路与逐支路公式，配套交互图册和 PDF。','35 components, nine paths, and branch equations, with an interactive atlas and PDF.'),('dts',TITLES['dts'][0],TITLES['dts'][1],TITLES['dts'][2],TITLES['dts'][3]),('dss',TITLES['dss'][0],TITLES['dss'][1],TITLES['dss'][2],TITLES['dss'][3])]
    for i,(kind,zh,en,desc,de) in enumerate(new,5):
        slug=kind+'-optical-atlas';item=dict(slug=slug,number=f'{i:02}',category='instrumentation',title=dict(zh=zh,en=en),summary=dict(zh=desc,en=de))
        topics=[t for t in topics if t['slug']!=slug];topics.append(item)
    (ROOT/'knowledge'/'topics.json').write_text(json.dumps(topics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    p=ROOT/'knowledge'/'index.html';s=p.read_text(encoding='utf-8');start=s.index('<section class="knowledge-grid"');end=s.index('</section>',start)+len('</section>')
    grid='<section class="knowledge-grid" aria-label="Knowledge topics">'
    for t in topics:
        zhcat='仪器原理' if t['category']=='instrumentation' else '基础原理' if t['category']=='foundations' else '井下应用';encat='INSTRUMENT PRINCIPLES' if t['category']=='instrumentation' else 'FOUNDATIONS' if t['category']=='foundations' else 'DOWNHOLE APPLICATIONS'
        grid+='<article class="topic-card"><div class="card-top"><span class="index">'+t['number']+'</span>'+bi(zhcat,encat,attrs='class="category-tag"')+'</div>'+bi(t['title']['zh'],t['title']['en'],'h2')+bi(t['summary']['zh'],t['summary']['en'],'p')+f'<a class="card-link" href="{t["slug"]}.html">'+bi('阅读这一主题','Explore this topic')+'</a></article>'
    s=s[:start]+grid+'</section>'+s[end:]
    s=s.replace('从四个相互连接的主题开始：先建立直觉，再阅读技术细节、适用条件和原始参考资料。','从基础概念和井下应用，到 DAS、DTS、DSS 仪器原理图册：逐步阅读元件、光路、公式与解释边界。')
    s=s.replace('Begin with four connected topics. Build intuition first, then explore the technical details, assumptions, and original references.','From foundations and downhole applications to DAS, DTS, and DSS atlases: explore components, paths, equations, and interpretation limits.')
    s=s.replace('可以按 01 → 04 顺序阅读。','可先读 01 → 04，再进入 05 → 07 原理图册。').replace('Read 01 → 04 in order.','Read 01 → 04 first, then explore atlases 05 → 07.')
    p.write_text(s,encoding='utf-8')
    p=ROOT/'index.html';s=p.read_text(encoding='utf-8');s=s.replace('分布式光纤的基本原理、井下布设、油气井生命周期与水泥水化监测。四个双语主题，从入门概念逐步深入技术细节。','分布式光纤的基本原理与井下应用，以及 DAS、DTS、DSS 原理图册：从元件、光路到公式与解释边界。').replace('Sensing principles, downhole deployment, the well life cycle, and cement hydration monitoring. Four bilingual topics, from accessible introductions to technical detail.','Sensing foundations and downhole applications, plus DAS, DTS, and DSS atlases: from components and optical paths to equations and interpretation limits.');p.write_text(s,encoding='utf-8')
    # Add atlas navigation to the basic-principles topic without altering its scientific text.
    p=ROOT/'knowledge'/'dfos-principles.html';s=p.read_text(encoding='utf-8');marker='<!-- instrument-atlas-links -->'
    if marker not in s:
        links=marker+'<section class="topic-section"><h2>'+bi('继续阅读：仪器原理图册','Continue: instrument-principles atlases')+'</h2><p>'+bi('按元件、光路和公式进一步理解三类传感的实现。','Explore implementations through components, optical paths, and equations.')+'</p><div class="atlas-links">'+''.join(f'<a href="{k}-optical-atlas.html">{k.upper()} · '+bi('原理图册','Principles atlas')+'</a>' for k in ['das','dts','dss'])+'</div></section>'
        s=s.replace('<div class="article-footer">',links+'<div class="article-footer">')
        if 'atlas.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="atlas.css"></head>')
    p.write_text(s,encoding='utf-8')

def package(kind,html_content,comps,pdfname):
    folder=OUT/kind
    local=html_content.replace('href="../style.css"','href="style.css"').replace('href="knowledge.css"','href="knowledge.css"').replace('href="atlas.css"','href="atlas.css"').replace('src="../app.js"','src="app.js"').replace('src="atlas.js"','src="atlas.js"').replace('atlases/'+kind+'/','').replace('atlases/shared/','shared/')
    local=local.replace('href="../favicon.svg"','href="favicon.svg"')
    own_zip=kind.upper()+'_资料包.zip'
    local=local.replace(f'<a href="{own_zip}">SVG + PNG + 源码 / Source package</a>','<a href="atlas.json">内容与来源 / Content & sources</a>')
    # Navigation remains an explicit link to the public website in the portable edition.
    local=local.replace('href="../index.html','href="https://hjh1308052375-boop.github.io/index.html').replace('href="index.html"','href="https://hjh1308052375-boop.github.io/knowledge/index.html"')
    for page in ['das-optical-atlas.html','dts-optical-atlas.html','dss-optical-atlas.html']:
        local=local.replace(f'href="{page}"',f'href="https://hjh1308052375-boop.github.io/knowledge/{page}"')
    local=local.replace('href="../notes/','href="https://hjh1308052375-boop.github.io/notes/').replace('href="../datasets/','href="https://hjh1308052375-boop.github.io/datasets/')
    with zipfile.ZipFile(folder/(kind.upper()+'_资料包.zip'),'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('index.html',local)
        for path in sorted(folder.rglob('*')):
            if path.is_file() and path.suffix!='.zip':z.write(path,path.relative_to(folder).as_posix())
        needed={k for r in (DTS if kind=='dts' else DSS) for k in r['components']}
        for v in comps:
            if v['key'] in needed:z.write(OUT/v['asset'],v['asset'])
        for name,p in [('style.css',ROOT/'style.css'),('knowledge.css',ROOT/'knowledge'/'knowledge.css'),('atlas.css',ROOT/'knowledge'/'atlas.css'),('atlas.js',ROOT/'knowledge'/'atlas.js'),('app.js',ROOT/'app.js'),('favicon.svg',ROOT/'favicon.svg'),('atlas_content.py',ROOT/'tools'/'atlas_content.py'),('build_sensing_atlases.py',Path(__file__))]:z.write(p,name)

def main():
    comps=make_components();report={'date':'2026-10-06','figures':{},'pdfs':{},'claims':'Conceptual teaching material; structural/numerical checks do not constitute experimental validation.'}
    for kind,routes in [('dts',DTS),('dss',DSS)]:
        folder=OUT/kind;figures=folder/'figures';figures.mkdir(parents=True,exist_ok=True)
        for r in routes:
            d=diagram(r);errors=d.verify()
            if errors:raise ValueError((r['id'],errors))
            d.save(figures/(r['id']+'.svg'));report['figures'][r['id']]={'canvas_bounds':'passed','box_overlap':'passed','topology':r['topology'],'sources':r['refs']}
            c=canvas.Canvas(str(figures/(r['id']+'.pdf')),pagesize=(W,H));diagram(r,c);c.showPage();c.save()
        data={'title':TITLES[kind][0],'routes':routes,'components':[v for v in comps if any(v['key'] in r['components'] for r in routes)],'references':{k:REFERENCES[k] for k in dict.fromkeys(k for r in routes for k in r['refs'])},'figure_record':{'tool':'deterministic Python SVG + ReportLab','imagegen':False,'measurement_data':False,'dead_water_alignment':'checked/not required: principles diagram, no field data','date':'2026-10-06'}}
        (folder/'atlas.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        pdfname,pages=make_pdf(kind,routes,comps);report['pdfs'][kind]={'file':pdfname,'pages':pages}
        webpage=atlas_html(kind,routes,comps,pdfname);(ROOT/'knowledge'/(kind+'-optical-atlas.html')).write_text(webpage,encoding='utf-8')
        (folder/'文件说明.md').write_text(f'# {TITLES[kind][0]}\n\n{len(routes)} 类代表路线。阅读顺序：元件、光路、支路公式、标定与限制、原始来源。\n\n- {pdfname}：{pages} 页，中文说明与英文标题。\n- atlas.json：可编辑内容、参考来源与元件来源。\n- figures/：可编辑 SVG 与矢量 PDF；PNG 导出随资料包提供。\n- 主网页：knowledge/{kind}-optical-atlas.html，支持中英文、路线筛选、元件筛选、公式折叠、图片放大。\n- tools/atlas_content.py 与 tools/build_sensing_atlases.py：内容与确定性构建源。\n\n厂家照片复用 DAS 图册已保存来源，不作为性能推荐；X 编号明确为功能示意。所有光路为概念架构，非施工图、非实测。简化公式自检不能替代实验验证。已核对脉宽/分辨率、温度—应变交叉敏感及瑞利谱移符号。\n',encoding='utf-8')
        package(kind,webpage,comps,pdfname)
    report['das_files']=integrate_das();update_knowledge()
    # The public Knowledge presentation is point-by-point notes, not a PDF/atlas portal.
    from sensing_notes import refresh_notes
    refresh_notes()
    (QA/'build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    ignore=ROOT/'.gitignore';text=ignore.read_text(encoding='utf-8') if ignore.exists() else ''
    for pattern in ['光纤传感原理/','work/','__pycache__/']:
        if pattern not in text.splitlines():text=text.rstrip()+'\n'+pattern+'\n'
    ignore.write_text(text.lstrip('\n'),encoding='utf-8')
    print(json.dumps({'routes':len(DTS)+len(DSS),'components':len(comps),'pdfs':report['pdfs']},ensure_ascii=False))

if __name__=='__main__':main()
