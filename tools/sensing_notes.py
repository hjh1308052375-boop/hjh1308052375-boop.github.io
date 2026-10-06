"""Point-by-point Knowledge pages. PDFs and downloadable atlas portals are not page content."""
from pathlib import Path
import json, shutil, zipfile

ROOT=Path(__file__).resolve().parents[1]

INTRO={
 'das':dict(title='DAS：原理与实现方式',en='DAS: principles and implementations',lead='分点理解分布式声学传感：测到了什么、怎样获得信号、有哪些代表性实现，以及如何解释。',lead_en='Understand distributed acoustic sensing point by point: observations, acquisition, representative implementations, and interpretation.',
   points=[('测量对象','通常测量沿光纤的动态轴向应变或应变率；应变、应变率与声压之间不能直接画等号。','Measurement','Usually dynamic axial fiber strain or strain rate; strain, strain rate, and acoustic pressure are not interchangeable.'),('基本机制','窄线宽光在光纤中产生瑞利背散射。光程扰动改变散斑强度、相位或局部频谱；不同路线读取的信息不同。','Mechanism','Coherent Rayleigh backscatter carries changes in intensity, phase, or local spectrum. Different implementations read different observables.'),('位置定位','脉冲 OTDR 用往返时延定位；连续扫频 OFDR 用拍频定位。两者的位置编码方式不同。','Localization','Pulsed OTDR uses round-trip delay; swept OFDR uses beat frequency. Their location encodings differ.'),('解释前提','光缆与介质的机械耦合、标距、偏振衰落及仪器输出单位，决定信号能解释到哪一层。','Interpretation','Cable coupling, gauge length, polarization fading, and output units determine what can be inferred.')],
   flow=[('发射光','Launch light'),('沿纤瑞利散射','Rayleigh backscatter'),('接收强度或复光场','Intensity or coherent reception'),('相位/谱移解调','Phase / spectral-shift recovery'),('标定与物理解释','Calibration & interpretation')]),
 'dts':dict(title='DTS：原理与实现方式',en='DTS: principles and implementations',lead='从拉曼强度比出发，分点介绍温度测量、单端与双端标定，以及布里渊、瑞利测温的条件。',lead_en='Start with Raman intensity ratios, then explore temperature sensing, single/double-ended calibration, and the conditions for Brillouin/Rayleigh thermometry.',
   points=[('测量对象','输出沿光纤的温度分布 T(z,t)。空间坐标是光纤距离，映射到井深或结构位置需要独立安装记录。','Measurement','The temperature distribution T(z,t) along the fiber. Mapping fiber distance to well depth or structural position needs installation records.'),('常见实现','拉曼 DTS 比较 Stokes 与 anti-Stokes 强度。二者的温度响应不同，经增益、背景和差分衰减校正后转换为温度。','Common implementation','Raman DTS compares Stokes and anti-Stokes intensities, then calibrates gains, background, and differential attenuation.'),('其他测温路线','布里渊 BFS 与瑞利谱移也对温度敏感，但同时对光纤应变敏感；测温时必须控制或独立测量应变。','Other routes','Brillouin BFS and Rayleigh spectral shifts respond to temperature and fiber strain; thermometry requires known or independently measured strain.'),('标定与误差','参考温度区、局部熔接/弯曲损耗、热平衡和时间同步，是可靠测温的一部分。','Calibration','Reference temperature sections, local splice/bend losses, thermal equilibrium, and timing alignment are part of reliable thermometry.')],
   flow=[('发射脉冲或扫频光','Pulse or sweep'),('温度相关散射','Temperature-sensitive scattering'),('接收两谱带或频谱','Receive bands / spectra'),('比值或谱移计算','Ratio / spectral shift'),('标定为 T(z,t)','Calibrate T(z,t)')]),
 'dss':dict(title='DSS：原理与实现方式',en='DSS: principles and implementations',lead='分点理解布里渊和瑞利应变测量，比较时域、频域与相关域定位，并说明温度补偿和应变传递。',lead_en='Understand Brillouin and Rayleigh strain sensing, compare time/frequency/correlation localization, and examine temperature compensation and strain transfer.',
   points=[('测量对象','测量光纤自身的轴向应变或应变变化。光纤应变不自动等于围岩、套管或结构应变。','Measurement','Axial fiber strain or strain change. Fiber strain is not automatically formation, casing, or structural strain.'),('两类主要机制','布里渊路线估计局部 BFS；瑞利路线比较参考与当前散射指纹，估计局部谱移。','Mechanisms','Brillouin methods estimate local BFS; Rayleigh methods correlate current and reference fingerprints to recover local spectral shifts.'),('温度交叉敏感','ΔνB = Cε Δεfiber + CT ΔT。只有一个频移时，需要独立温度信息或明确约束才能计算应变。','Cross-sensitivity','ΔνB = Cε Δεfiber + CT ΔT. A single shift needs independent temperature information or explicit constraints to recover strain.'),('应变传递','涂覆、黏结、光缆结构、滑移与剪滞影响 εfiber 到 εhost 的关系；温度补偿不能替代机械耦合验证。','Strain transfer','Coating, bonding, cable construction, slip, and shear lag affect εfiber-to-εhost transfer. Temperature compensation cannot replace coupling validation.')],
   flow=[('发射/参考状态','Interrogate / reference'),('局部散射谱','Local scattering spectrum'),('频移或谱相关','Shift / correlation'),('温度补偿','Temperature compensation'),('光纤应变与传递验证','Fiber strain & transfer validation')]),
}

def das_routes():
    names=[('强度直检 φ-OTDR / DVS','Direct-intensity φ-OTDR / DVS'),('外差相干 φ-OTDR','Heterodyne coherent φ-OTDR'),('零差相干 φ-OTDR','Homodyne coherent φ-OTDR'),('延迟 MZI 与 3×3 耦合器','Delayed MZI with a 3×3 coupler'),('非平衡 Michelson 与 PGC','Unbalanced Michelson with PGC'),('双脉冲自外差 φ-OTDR','Dual-pulse self-heterodyne φ-OTDR'),('啁啾脉冲 CP-φ-OTDR','Chirped-pulse CP-φ-OTDR'),('频率扫描 FS-φ-OTDR','Frequency-scanned FS-φ-OTDR'),('扫频相干 OFDR','Swept coherent OFDR')]
    descriptions=[
      ('脉冲回波直接进入光电接收器，比较各位置的散斑强度变化。','Directly detect pulse returns and compare local speckle-intensity changes.','瑞利散斑强度变化','Rayleigh speckle intensity changes','强度与相位一般是非线性关系，可定位振动，不能仅凭强度差直接换算定量应变。','Intensity is generally nonlinear in phase: vibration localization alone does not yield quantitative strain.',['i=R |Br|²; D=i(t,T)-i(t,T0)','z=c(t-t0)/(2ng)']),
      ('回波与同源连续本振混频，用平衡探测和电域下变频恢复复光场。','Mix the return with a same-source CW oscillator; balanced detection and electrical down-conversion recover the complex field.','外差拍频的 I/Q 与相位','Heterodyne I/Q and phase','低通须保留扰动带宽，并校正本振、接收链和偏振衰落。','Retain the disturbance bandwidth and calibrate the LO, receiver chain, and polarization fading.',['idiff=2R Re[Br BL*]','C_hat=LPF[idiff exp(-iΩA t)]/R; φ=arg(C_hat)']),
      ('用 90° 光学混频器及两对平衡探测器，直接得到两条正交电信号。','A 90° optical hybrid and two balanced pairs directly produce quadrature signals.','同频相干 I/Q 与相位','Homodyne coherent I/Q and phase','校正 I/Q 偏置、增益差及正交误差；Q 端口顺序改变时相位符号也改变。','Correct I/Q offsets, gain mismatch, and quadrature error; swapping Q ports changes the phase sign.',['C_hat=(I+iQ)/R','φ=atan2(Q,I)']),
      ('回波分到两条延迟不同的支路，再由 3×3 耦合器形成三条相移干涉信号。','Split the return into unequal-delay arms; a 3×3 coupler forms three phase-shifted interference signals.','两散射区之间的相位差','Phase difference between two scattering regions','标距由臂时延差设定，脉宽决定的空间分辨率另行定义；需校准三通道增益和端口相移。','Arm delay sets the gauge length, independently of pulse resolution; calibrate three-channel gains and port phases.',['φ=atan2[sqrt(3)(i1-i2), 2i0-i1-i2]','Lg=c τd/(2ng)']),
      ('反射式双臂由法拉第旋转镜返回，在一臂施加相位载波，读取前两谐波。','Faraday mirrors return the two arms; apply a phase carrier to one arm and recover the first two harmonics.','相位载波的谐波系数','Phase-carrier harmonic coefficients','有效调制深度是双程量；载波与采集需同步，避开贝塞尔系数接近零的工作点。','Use the effective round-trip modulation depth, synchronize carrier/acquisition, and avoid near-zero Bessel coefficients.',['i=I0+V cos(φ-C cos x)','h1=2V J1(C) sinφ; h2=-2V J2(C) cosφ']),
      ('同源光产生频率不同、发射时刻不同的一对脉冲，使回波在接收时相互干涉。','Launch a same-source pulse pair with different frequencies and delays; overlapping returns interfere.','两回波之间的拍频相位','Beat phase between two returns','两路 RF 的时钟、门控与相对初相需要锁定，并选择回波重叠区。','Lock the RF clocks, gates, and relative phase, and select the return-overlap region.',['ΔΩ=Ω1-Ω2','C_hat=LPF[i exp(-iΔΩt)]/R; Lg≈c ΔTpair/(2ng)']),
      ('在一个脉冲内部线性扫频，对前后强度迹线做局部相关，估计等效频谱平移。','Chirp within each pulse and correlate local intensity traces to estimate an equivalent spectral shift.','局部迹线时间平移 δu','Local trace time shift δu','须标定啁啾斜率、保持足够相关，并控制温度交叉敏感。相关滞后符号取决于定义。','Calibrate chirp slope, retain sufficient correlation, and control thermal cross-sensitivity. Lag sign depends on its definition.',['IT(u)≈I0(u+δu); ΔνR=-κ δu','Δε=κ δu/[ν0(1-pe)]  (ΔT=0)']),
      ('在脉冲之间逐频扫描，为每个位置构造局部瑞利频谱，再与参考谱相关。','Step frequency between pulses, build a local spectrum by position, and correlate it with a reference.','局部瑞利频谱平移 ΔνR','Local Rayleigh spectral shift ΔνR','一轮频扫期间状态需近似不变；串行频扫降低更新速率。','Assume a nearly constant state during each scan; serial scanning reduces update rate.',['Δε=-ΔνR/[ν0(1-pe)]  (ΔT=0)','fupdate≲frep/Nν']),
      ('连续扫频光与参考光干涉，用辅助 MZI 校正扫描后转换为空间复回波。','Continuously swept light interferes with a reference; an auxiliary MZI calibrates the sweep before spatial reconstruction.','距离相关拍频与空间复回波','Distance-dependent beat and complex spatial return','与脉冲 OTDR 不同；需校准参考延迟和拍频符号，动态相位测量要求一次扫描内扰动近似不变。','Unlike pulsed OTDR, calibrate reference delay and beat sign; phase sensing assumes small changes within each sweep.',['fb=κ(τz-τref); z=c(τref+fb/κ)/(2ng)','Δzideal≈c/(2ng Δνsweep)']),
    ]
    manifest=json.loads((ROOT/'knowledge'/'atlases'/'das'/'DAS_图册说明.json').read_text(encoding='utf-8'))
    result=[]
    for i,((name,en),v) in enumerate(zip(names,descriptions),1):
        zh,eng,obs,obs_en,lim,lim_en,eqs=v;source=manifest['sources'][i-1]
        result.append(dict(id=f'DAS{i:02}',name=name,en=en,summary=zh,sum_en=eng,observable=obs,obs_en=obs_en,limits=lim,limits_en=lim_en,refs=[str(i)],steps=[dict(label='关键关系 / Key relation',equation=eq,zh='',en='') for eq in eqs],figure=f'atlases/das/figures/DAS_{i:02}.svg'))
    refs={str(v['route']):dict(title=v['reference'],url='https://doi.org/'+v['doi'],evidence='Source retained from the original DAS project; this page summarizes its representative architecture.') for v in manifest['sources']}
    return result,refs

def prepare_das_assets():
    out=ROOT/'knowledge'/'atlases';original=ROOT/'光纤传感原理'/'outputs'
    figures=out/'das'/'figures';figures.mkdir(exist_ok=True)
    archive=out/'das'/'DAS_全部单图_SVG_PNG.zip'
    for i in range(1,10):
        name=f'DAS_{i:02}.svg';target=figures/name
        if (original/name).exists():shutil.copy2(original/name,target)
        elif not target.exists():
            with zipfile.ZipFile(archive) as z:target.write_bytes(z.read(name))
    comps=json.loads((out/'shared'/'components-source.json').read_text(encoding='utf-8'))
    for v in comps:
        name=v['id']+'.png';dest=out/'shared'/name
        if not dest.exists():
            p=original/'DAS_元件实物图片'/name
            if p.exists():shutil.copy2(p,dest)
            else:
                with zipfile.ZipFile(archive) as z:dest.write_bytes(z.read('DAS_元件实物图片/'+name))
        v['asset']='shared/'+name;v['en']=v['abbr'];v['image_kind']='manufacturer_photo';v['source_url']=v['photo']['page']
    return comps

def notes_html(kind,routes,comps,references,shell,bi,esc):
    intro=INTRO[kind]
    def point(label,zh,enlabel,en):return '<li><strong>'+bi(label,enlabel)+'</strong><span>'+bi(zh,en)+'</span></li>'
    def heading(id,num,zh,en):return f'<h2 id="{id}"><small>{num}</small>'+bi(zh,en)+'</h2>'
    body='<section class="article-hero"><div class="breadcrumbs"><a href="index.html">'+bi('知识','Knowledge')+'</a> / '+kind.upper()+'</div>'+bi('分布式光纤传感 · 原理说明','DISTRIBUTED FIBER-OPTIC SENSING · PRINCIPLES',attrs='class="eyebrow"')+bi(intro['title'],intro['en'],'h1')+bi(intro['lead'],intro['lead_en'],'p','class="lede"')+'</section>'
    body+='<nav class="notes-toc" aria-label="Page contents">'+''.join(f'<a href="#{id}">'+bi(zh,en)+'</a>' for id,zh,en in [('measure','测量什么','Measurement'),('chain','测量过程','Acquisition'),('routes','实现方式','Implementations'),('components','元件作用','Components'),('limits','解释边界','Limits'),('sources','参考来源','Sources')])+'</nav><div class="point-notes">'
    body+=heading('measure','01','先理解：它测量什么','What does it measure?')+'<ul class="explanation-points">'
    for label,zh,enlabel,en in intro['points']:body+=point(label,zh,enlabel,en)
    body+='</ul>'+heading('chain','02','测量过程：从光到结果','From light to a result')+'<ol class="measurement-flow">'
    for zh,en in intro['flow']:body+='<li>'+bi(zh,en)+'</li>'
    body+='</ol>'+heading('routes','03','代表性实现方式','Representative implementations')+'<p>'+bi('每一种方式分别说明测量机制、直接观测与适用条件。光路示意和关键公式可按需展开。','Each implementation states its mechanism, observable, and conditions. Expand schematics and key equations as needed.')+'</p><nav class="route-index" aria-label="Implementations">'
    for r in routes:body+=f'<a href="#{r["id"]}"><span>{r["id"][-2:]}</span>'+bi(r['name'],r['en'])+'</a>'
    body+='</nav>'
    for r in routes:
        body+=f'<article class="point-route" id="{r["id"]}"><h3><small>{r["id"][-2:]}</small>'+bi(r['name'],r['en'])+'</h3><ul class="explanation-points">'+point('工作方式',r['summary'],'How it works',r['sum_en'])+point('直接观测',r['observable'],'Observable',r['obs_en'])+point('适用条件与局限',r['limits'],'Conditions and limits',r['limits_en'])+'</ul>'
        fig=r.get('figure',f'atlases/{kind}/figures/{r["id"]}.svg')
        body+='<details class="note-detail"><summary>'+bi('代表性光路与关键公式','Representative path & key equations')+'</summary><figure class="route-figure"><img src="'+fig+'" alt="'+esc(r['name'])+'" data-alt-zh="'+esc(r['name'])+'" data-alt-en="'+esc(r['en'])+'" loading="lazy"><figcaption>'+bi('概念示意，非按比例、非实测数据。','Conceptual, not to scale, not measured data.')+'</figcaption></figure><ol class="point-formulas">'
        for s in r['steps']:
            body+='<li><strong>'+esc(s['label'])+'</strong><div class="equation">'+esc(s['equation'])+'</div>'
            if s['zh']:body+=bi(s['zh'],s['en'],'p')
            body+='</li>'
        body+='</ol></details><p class="point-source">'+bi('依据：','Sources: ')
        for k in r['refs']:body+='<a href="'+esc(references[k]['url'])+'" target="_blank" rel="noopener noreferrer">'+esc(references[k]['title'].split('. ')[0])+'</a> '
        body+='</p></article>'
    body+=heading('components','04','主要元件：各自起什么作用','What the components do')+'<ul class="explanation-points">'
    groups=[('光源与发射控制','激光器提供光；调制器产生脉冲、频移或扫频；驱动与偏置控制决定实际发射波形。','Source and launch','Lasers supply light; modulators create pulses, shifts, or sweeps. Drivers and bias controls shape the actual launch.'),('光路与光纤','耦合器分光或混频，环形器区分发射与回波，光纤提供分布式散射；光学滤波按谱带选型。','Optical path and fiber','Couplers split/mix, circulators route launch/return, and fiber provides distributed scattering. Select filters by optical band.'),('接收与采集','探测器把光信号转为电信号，采集卡或时间标记器记录信号；带宽、增益和同步均需校准。','Reception and acquisition','Detectors convert light to electrical signals, recorded by digitizers or time taggers. Calibrate bandwidth, gain, and timing.'),('处理与标定','上位机完成比值、谱拟合或相关解调，再用参考温度、应变灵敏度和安装信息赋予物理量。','Processing and calibration','Compute ratios, fits, or correlations, then calibrate with reference temperatures, strain sensitivities, and installation information.')]
    for label,zh,enlabel,en in groups:body+=point(label,zh,enlabel,en)
    body+='</ul><details class="note-detail"><summary>'+bi('逐项查看元件、作用和图片','Component-by-component descriptions and images')+'</summary><div class="point-components">'
    for v in comps:
        isphoto=v['image_kind']=='manufacturer_photo'
        body+='<article><h3>'+v['id']+' · '+bi(v['name'],v.get('en',v['abbr']))+'</h3><img loading="lazy" src="atlases/'+v['asset']+'" alt="'+esc(v['name'])+'"><ul><li>'+bi(v['role'],v.get('role_en','Role in the representative optical branch.'))+'</li>'
        if v.get('eq') and not ('\\' in v['eq']):body+='<li class="component-equation">'+esc(v['eq'])+'</li>'
        body+='</ul><small>'+bi('厂家外观示例；须核对实际规格。' if isphoto else '原创功能示意，不是实物照片。','Manufacturer appearance example; check actual specifications.' if isphoto else 'Original functional schematic, not a product photo.')+'</small>'
        if v.get('source_url'):body+='<a href="'+esc(v['source_url'])+'" target="_blank" rel="noopener noreferrer">'+bi('厂家来源 ↗','Manufacturer source ↗')+'</a>'
        body+='</article>'
    body+='</div></details>'+heading('limits','05','解释时需要区分什么','Interpretation limits')+'<ul class="explanation-points">'
    limits=[('空间尺度','空间分辨率、应变标距与输出采样间距分别定义；密集输出点不代表更高的真实分辨率。','Spatial scales','Resolution, gauge length, and output sample spacing are distinct; dense samples do not establish finer true resolution.'),('交叉敏感','温度、应变与机械耦合可能同时影响读数。先确认仪器的直接观测，再讨论目标物理过程。','Cross-sensitivity','Temperature, strain, and coupling can affect readings together. Establish the instrument observable before interpreting the target process.'),('验证层次','这些光路与关系式用于原理说明；代数校验不等于仪器性能验证，也不等于现场解释成立。','Validation','These paths and relations teach principles; algebra checks are not instrument-performance or field-interpretation validation.')]
    if kind=='das':limits.insert(1,('相位与应变','采用原项目的 exp(+iωt) 约定和远端减近端相位差时，Δεavg=-Δφg/(Kε Lg)，Kε=4πneff(1-pe)/λ。端口顺序、温度变化和解调符号需校准。','Phase to strain','Under the original exp(+iωt) and far-minus-near phase convention, Δεavg=-Δφg/(Kε Lg), with Kε=4πneff(1-pe)/λ. Calibrate port order, temperature, and signs.'))
    for label,zh,enlabel,en in limits:body+=point(label,zh,enlabel,en)
    body+='</ul>'+heading('sources','06','参考来源','Sources')+'<ol class="references">'
    for k in dict.fromkeys(k for r in routes for k in r['refs']):body+='<li><a href="'+esc(references[k]['url'])+'" target="_blank" rel="noopener noreferrer">'+esc(references[k]['title'])+'</a></li>'
    body+='</ol><div class="notes-related">'+bi('继续阅读：','Continue: ')+''.join('<a href="'+k+'-optical-atlas.html">'+k.upper()+'</a>' for k in ['das','dts','dss'] if k!=kind)+'</div></div>'
    return shell(intro['title'],intro['en'],body)

def refresh_notes():
    from build_sensing_atlases import shell,bi,esc,OUT,make_components
    from atlas_content import DTS,DSS,REFERENCES
    comps=make_components()
    for kind,routes in [('dts',DTS),('dss',DSS)]:
        used=[v for v in comps if any(v['key'] in r['components'] for r in routes)]
        page=notes_html(kind,routes,used,REFERENCES,shell,bi,esc)
        (ROOT/'knowledge'/(kind+'-optical-atlas.html')).write_text(page,encoding='utf-8')
    routes,refs=das_routes();dcomps=prepare_das_assets()
    (ROOT/'knowledge'/'das-optical-atlas.html').write_text(notes_html('das',routes,dcomps,refs,shell,bi,esc),encoding='utf-8')
    topics=json.loads((ROOT/'knowledge'/'topics.json').read_text(encoding='utf-8'))
    for t in topics:
        kind=t['slug'].split('-')[0]
        if kind in INTRO:
            t['title']={'zh':INTRO[kind]['title'],'en':INTRO[kind]['en']}
            t['summary']={'zh':INTRO[kind]['lead'],'en':INTRO[kind]['lead_en']}
    (ROOT/'knowledge'/'topics.json').write_text(json.dumps(topics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name in ['index.html','knowledge/index.html','knowledge/dfos-principles.html']:
        p=ROOT/name;s=p.read_text(encoding='utf-8')
        replaces={'DAS 光路与原理图册':INTRO['das']['title'],'DAS optical-path and principles atlas':INTRO['das']['en'],'DTS 温度传感原理图册':INTRO['dts']['title'],'DTS temperature-sensing atlas':INTRO['dts']['en'],'DSS 应变传感原理图册':INTRO['dss']['title'],'DSS strain-sensing atlas':INTRO['dss']['en'],'35 类元件、九类光路与逐支路公式，配套交互图册和 PDF。':INTRO['das']['lead'],'35 components, nine paths, and branch equations, with an interactive atlas and PDF.':INTRO['das']['lead_en'],'仪器原理图册':'仪器原理说明','原理图册':'原理说明','principles atlases':'principles notes','DSS atlases':'DSS notes','atlases 05 → 07':'notes 05 → 07'}
        for old,new in replaces.items():s=s.replace(old,new)
        p.write_text(s,encoding='utf-8')
    print('Updated point-by-point DAS/DTS/DSS Knowledge pages; no PDF or package entry links.')

if __name__=='__main__':refresh_notes()
