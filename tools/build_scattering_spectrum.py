"""Original teaching schematic: optical frequency vs illustrative relative intensity.
Peak positions/order are physical; profiles and heights are deliberately schematic.
No instrument data, PDF output, or image generation is used.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'knowledge'/'diagrams'
FONT=FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
plt.rcParams.update({'svg.fonttype':'path','font.size':13,'axes.linewidth':1.15})
BLUE='#1765ad'; ORANGE='#c36524'; PURPLE='#7b4db1'; INK='#122d40'; MUTED='#566b79'

def draw(lang):
    zh=lang=='zh'
    fig,axes=plt.subplots(1,3,figsize=(12.5,6.7),gridspec_kw={'width_ratios':[1,.95,1]},sharey=True)
    fig.subplots_adjust(left=.095,right=.97,bottom=.255,top=.70,wspace=.065)
    # Frequency offsets in THz, used only to preserve the GHz/THz scale separation.
    # Arbitrary Gaussian profiles/linewidths do not model an actual silica spectrum.
    domains=[(-19,-5),(-.035,.035),(5,19)]
    xleft=np.linspace(*domains[0],1000);xmid=np.linspace(*domains[1],3000);xright=np.linspace(*domains[2],1000)
    curves=[[(xleft,.38*np.exp(-.5*((xleft+13)/1.7)**2),PURPLE)],
            [(xmid,.99*np.exp(-.5*(xmid/.00075)**2),BLUE),(xmid,.53*np.exp(-.5*((xmid+.011)/.001)**2)+.53*np.exp(-.5*((xmid-.011)/.001)**2),ORANGE)],
            [(xright,.20*np.exp(-.5*((xright-13)/1.7)**2),PURPLE)]]
    for ax,domain,parts in zip(axes,domains,curves):
        ax.set_xlim(*domain);ax.set_ylim(0,1.15)
        ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False)
        ax.tick_params(colors=INK,labelsize=12,direction='out',length=5)
        for x,y,color in parts:
            ax.fill_between(x,0,y,color=color,alpha=.075)
            ax.plot(x,y,color=color,lw=2.6)
    axes[1].spines['left'].set_visible(False);axes[2].spines['left'].set_visible(False)
    axes[1].tick_params(axis='y',left=False);axes[2].tick_params(axis='y',left=False)
    axes[0].set_yticks([0]);axes[0].set_ylabel('相对散射强度（示意）' if zh else 'Relative scattered intensity (schematic)',fontproperties=FONT,fontsize=15,labelpad=16,color=INK)
    axes[0].set_xticks([-13],[r'$\nu_0-\nu_R$']);axes[1].set_xticks([-.011,0,.011],[r'$\nu_0-\nu_B$',r'$\nu_0$',r'$\nu_0+\nu_B$']);axes[2].set_xticks([13],[r'$\nu_0+\nu_R$'])
    for ax in axes:
        for label in ax.get_xticklabels():label.set_fontproperties(FONT)
    # Conventional axis-break marks distinguish the middle GHz band from Raman THz wings.
    d=.018
    for left,right in [(axes[0],axes[1]),(axes[1],axes[2])]:
        left.plot((1-d,1+d),(-d,d),transform=left.transAxes,color=INK,lw=1.3,clip_on=False)
        right.plot((-d,d),(-d,d),transform=right.transAxes,color=INK,lw=1.3,clip_on=False)
    axes[0].text(-13,.445,'拉曼 / Raman' if zh else 'Raman',ha='center',fontproperties=FONT,fontsize=15,color=PURPLE)
    axes[2].text(13,.265,'拉曼 / Raman' if zh else 'Raman',ha='center',fontproperties=FONT,fontsize=15,color=PURPLE)
    axes[1].text(0,1.04,'瑞利 / Rayleigh' if zh else 'Rayleigh',ha='center',fontproperties=FONT,fontsize=15,color=BLUE)
    for peak in [-.011,.011]:
        axes[1].text(peak,.59,'布里渊\nBrillouin' if zh else 'Brillouin',ha='center',fontproperties=FONT,fontsize=10.5,color=ORANGE,linespacing=1.3)
    fig.text(.095,.93,'三类散射在光频轴上的位置' if zh else 'Where the three scattering mechanisms appear',fontproperties=FONT,fontsize=22,color=INK)
    fig.text(.095,.865,'Stokes：低频、长波长' if zh else 'Stokes: lower frequency, longer wavelength',fontproperties=FONT,fontsize=14,color=MUTED)
    fig.text(.97,.865,'anti-Stokes：高频、短波长' if zh else 'anti-Stokes: higher frequency, shorter wavelength',ha='right',fontproperties=FONT,fontsize=14,color=MUTED)
    for ax,title in zip(axes,['THz 级频移' if zh else 'THz-scale shifts','GHz 级频移' if zh else 'GHz-scale shifts','THz 级频移' if zh else 'THz-scale shifts']):
        ax.set_title(title,fontproperties=FONT,fontsize=12,color=MUTED,pad=18)
    fig.text(.535,.16,'光频 ν  →  增大' if zh else 'Optical frequency ν  →  increasing',ha='center',fontproperties=FONT,fontsize=16,color=INK)
    fig.text(.095,.082,'断轴区分 GHz / THz 尺度；峰高与线宽仅作示意，不代表实测或真实强度比。' if zh else 'Axis breaks separate GHz / THz scales; heights and linewidths are illustrative, not measured ratios.',fontproperties=FONT,fontsize=11,color=MUTED)
    fig.text(.095,.034,r'$\nu_0$：入射光频率  ·  $\nu_B$：布里渊频移  ·  $\nu_R$：拉曼频移' if zh else r'$\nu_0$: incident frequency  ·  $\nu_B$: Brillouin shift  ·  $\nu_R$: Raman shift',fontproperties=FONT,fontsize=11,color=MUTED)
    dest=OUT/('scattering-spectrum-'+lang)
    fig.savefig(dest.with_suffix('.svg'),facecolor='white')
    fig.savefig(dest.with_suffix('.png'),dpi=170,facecolor='white')
    plt.close(fig)

def install():
    p=ROOT/'knowledge'/'dfos-principles.html';s=p.read_text(encoding='utf-8')
    marker='<!-- scattering-spectrum -->'
    figure=marker+'''<figure class="concept-figure scattering-spectrum" id="scattering-spectrum">
<img data-lang="zh" lang="zh-CN" src="diagrams/scattering-spectrum-zh.svg" width="1250" height="670" alt="三类背散射示意频谱：中央瑞利峰，近旁布里渊双峰，远侧拉曼双带；左为低频 Stokes，右为高频 anti-Stokes。" loading="lazy">
<img data-lang="en" lang="en" src="diagrams/scattering-spectrum-en.svg" width="1250" height="670" alt="Schematic backscatter spectrum: central Rayleigh peak, nearby Brillouin pair, distant Raman bands; Stokes on the low-frequency left and anti-Stokes on the high-frequency right." loading="lazy" hidden>
<figcaption><span data-zh="图：沿光频 ν 展示三类散射。瑞利位于入射频率 ν₀，布里渊在 ν₀±νB，拉曼在 ν₀±νR。断轴区分 GHz 与 THz 级频移；峰高、宽度和 Stokes/anti-Stokes 高度差均为教学示意，不代表定量谱或固定强度比。" data-en="Three scattering mechanisms along optical frequency ν: Rayleigh at ν₀, Brillouin at ν₀±νB, Raman at ν₀±νR. Axis breaks separate GHz and THz shifts. Peak heights, widths, and Stokes/anti-Stokes asymmetry are illustrative, not a quantitative spectrum or fixed intensity ratio.">图：沿光频 ν 展示三类散射。瑞利位于入射频率 ν₀，布里渊在 ν₀±νB，拉曼在 ν₀±νR。断轴区分 GHz 与 THz 级频移；峰高、宽度和 Stokes/anti-Stokes 高度差均为教学示意，不代表定量谱或固定强度比。</span> <a class="citation-link" href="#ref-5" aria-label="Reference 5">[5]</a> <a data-lang="zh" href="diagrams/scattering-spectrum-zh.svg" target="_blank" rel="noopener">查看大图 ↗</a><a data-lang="en" href="diagrams/scattering-spectrum-en.svg" target="_blank" rel="noopener" hidden>Open full-size diagram ↗</a></figcaption>
</figure><div data-lang="zh" lang="zh-CN"><ul><li><strong>先看频率位置：</strong>瑞利为近似弹性散射；布里渊侧带离入射光很近，拉曼侧带远得多。</li><li><strong>再看方向：</strong>横轴是频率，因此左边 Stokes 光子能量更低、波长更长；右边 anti-Stokes 光子能量更高、波长更短。若横轴换成波长，左右顺序会反转。</li><li><strong>最后看测量方式：</strong>DAS 常读取相干瑞利回波的相位变化；拉曼 DTS 读取经校准的两谱带强度比；布里渊 DSS/测温读取频移，并处理温度与应变交叉敏感。</li></ul></div>
<div data-lang="en" lang="en" hidden><ul><li><strong>Frequency position:</strong> Rayleigh is approximately elastic; Brillouin sidebands sit close to the incident light, while Raman bands lie much farther away.</li><li><strong>Direction:</strong> Frequency increases to the right: Stokes photons have lower energy and longer wavelength; anti-Stokes photons have higher energy and shorter wavelength. A wavelength axis reverses this order.</li><li><strong>Measurement:</strong> DAS often reads coherent Rayleigh phase changes; Raman DTS reads a calibrated band-intensity ratio; Brillouin strain/temperature sensing reads frequency shifts and addresses cross-sensitivity.</li></ul></div>
<!-- /scattering-spectrum -->'''
    if marker in s:
        start=s.index(marker);end=s.index('<!-- /scattering-spectrum -->',start)+len('<!-- /scattering-spectrum -->');s=s[:start]+figure+s[end:]
    else:
        section=s.index('<section class="topic-section" id="scattering">');pos=s.index('</h2>',section)+5;s=s[:pos]+figure+s[pos:]
    if 'id="ref-5"' not in s:
        ref='<li id="ref-5"><a href="https://doi.org/10.3390/s120708601" target="_blank" rel="noopener noreferrer">Bao, X. &amp; Chen, L. (2012) · Recent Progress in Distributed Fiber Optic Sensors</a><span class="source-type" data-zh="散射谱与传感机制综述；本文频谱为原创教学示意，未复制原图。" data-en="Review of scattering spectra and sensing mechanisms; the spectrum here is an original teaching schematic, not a copied figure.">散射谱与传感机制综述；本文频谱为原创教学示意，未复制原图。</span></li>'
        pos=s.index('</ol>',s.index('<ol class="references">'));s=s[:pos]+ref+s[pos:]
    p.write_text(s,encoding='utf-8')
    record={'purpose':'Teach the positions of Rayleigh, Brillouin and Raman scattering on an increasing optical-frequency axis','type':'original conceptual spectrum, no measured data','x_axis':'optical frequency ν; three frequency-offset windows with explicit breaks','y_axis':'illustrative relative intensity; heights independently schematic, no inferred physical ratios','profiles':'Gaussian teaching profiles, not measured line shapes','frequency_windows_THz_relative_to_nu0':[[-19,-5],[-.035,.035],[5,19]],'illustrative_centers_THz':[-13,-.011,0,.011,13],'height_and_linewidth_policy':'not quantitative; Stokes/anti-Stokes asymmetry only illustrates possible thermal asymmetry, not fixed ratio','source':'tools/build_scattering_spectrum.py','outputs':['scattering-spectrum-zh.svg','scattering-spectrum-en.svg','scattering-spectrum-zh.png','scattering-spectrum-en.png'],'references':['https://doi.org/10.3390/s120708601','https://www.epfl.ch/labs/gfo/page-60916-en-html/page-61501-en-html/distributed-brillouin-fibre-sensing/'],'dead_water_alignment':'checked/not required: no field data','date':'2026-10-06'}
    (OUT/'scattering-spectrum.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    for language in ['zh','en']:draw(language)
    install()
    print('Generated bilingual schematic spectra and inserted into #scattering.')
