# DAS 元件实物图来源与作用

覆盖原编号 1–9；元件 C01–C35。所有图片版权归相应厂家。读取日期：2026-10-06。

图片直接取自厂家网站；包含产品照片及厂家外观图，未使用 AI 生成为实物替代。照片仅用于器件识别，不代表整套采购配置。

## C01 窄线宽激光器 / NLL

厂家 / 型号：Chilas；CF3 1550 nm 蝶形封装
对应路线：1, 2, 3, 4, 5, 6, 8
作用：提供高相干性的连续光，作为脉冲探测光和同源本振；线宽与频率噪声影响相位测量。
说明：裸封装需电流驱动、TEC 温控及配套安装座。

产品页：[Chilas 官方页面](https://chilasbv.com/chilas-cf3-1550-nm/)
原图：[C01 图片原始地址](https://chilasbv.com/wp-content/uploads/2025/07/Chilas-CF3-butterfly-packaged-laser.webp)
原尺寸：[768, 432]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C02 可电流调谐激光二极管 / LD

厂家 / 型号：AeroDIODE；1550 nm DFB 蝶形激光系列
对应路线：7
作用：电流调制使光频在一个脉冲内连续变化，生成 CP-φ-OTDR 所需的啁啾光。
说明：图片代表封装；啁啾斜率、线性度与动态调谐带宽需实测标定。

产品页：[AeroDIODE 官方页面](https://www.aerodiode.com/product/1550-nm-laser-diode/)
原图：[C02 图片原始地址](https://www.aerodiode.com/wp-content/uploads/2020/05/1550-nm-laser-diode-2.jpg)
原尺寸：[986, 752]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C03 扫频可调谐激光器 / TLS

厂家 / 型号：Santec；TSL-570；内置扫频控制
对应路线：9
作用：连续扫描光频；回波与参考光产生距离相关的拍频，用于相干 OFDR。
说明：扫频控制器可集成在整机中；辅助 MZI 校正实际扫频非线性。

产品页：[Santec 官方页面](https://inst.santec.com/products/test-and-measurement/tunablelaser)
原图：[C03 图片原始地址](https://santec-inst.transforms.svdcdn.com/production/product-images/Japan/TSL-570_A.png?w=363&h=242&q=80&fm=png&fit=crop&dm=1768835583&s=7b53e54b280f26da58159b5bada910e7)
原尺寸：[363, 242]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C04 光隔离器 / ISO

厂家 / 型号：DK Photonics；1550 nm 非偏振相关隔离器
对应路线：1, 2, 3, 4, 5, 6, 7, 8, 9
作用：允许指定方向传光，抑制反射光返回激光器；路线 5 的接收 ISO 也抑制干涉仪回返。
说明：有方向性；图中的箭头需与实物安装方向一致。

产品页：[DK Photonics 官方页面](https://www.dkphotonics.com/product/1550nm-polarization-insensitive-isolator.html)
原图：[C04 图片原始地址](https://www.dkphotonics.com/wp-content/uploads/ISO-1X1-bare-fiber-1024x640.png)
原尺寸：[1024, 640]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C05 1×2 分光耦合器 / OC

厂家 / 型号：AC Photonics；1×2 单模熔融耦合器
对应路线：2, 3, 4, 6, 9
作用：把同一激光分成探测/本振、两脉冲臂、延迟干涉臂或扫频辅助支路。
说明：分光比决定各支路功率；1×2 器件为三端口。

产品页：[AC Photonics 官方页面](https://acphotonics.com/1x2-and-2x2-single-mode-fused-coupler)
原图：[C05 图片原始地址](https://acphotonics.com/image/cache/catalog/product/Singlemode_Dual_Window_Couplers_54_1-500x500.png)
原尺寸：[500, 500]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C06 2×2 光纤耦合器 / 2×2 OC

厂家 / 型号：DK Photonics；1550 nm PM 熔融耦合器
对应路线：2, 5, 6, 9
作用：将两路光相干合束，或把反射干涉仪回波送至接收端；两个输出可用于平衡探测。
说明：四端口；固定端口相位需按接线约定校准。

产品页：[DK Photonics 官方页面](https://www.dkphotonics.com/product/pm-fused-coupler.html)
原图：[C06 图片原始地址](https://www.dkphotonics.com/wp-content/uploads/2x2-pm-fiber-fused-coupler-1024x640.jpg)
原尺寸：[1024, 640]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C07 3×3 光纤耦合器 / 3×3 OC

厂家 / 型号：DK Photonics；3×3 PM 熔融耦合器系列
对应路线：4
作用：让两路延迟回波产生三个相位错开的干涉输出，结合三只 PD 恢复相位。
说明：六端口；第三输入终止。实际分光比、相位差需校准。

产品页：[DK Photonics 官方页面](https://www.dkphotonics.com/product/1550nm-3x3-fused-pm-fiber-splitter.html)
原图：[C07 图片原始地址](https://www.dkphotonics.com/wp-content/uploads/3x3-pm-fiber-fused-coupler.jpg)
原尺寸：[1600, 1000]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C08 三端口光环形器 / CIR

厂家 / 型号：DK Photonics；1550 nm 3-port PIOC
对应路线：1, 2, 3, 4, 5, 6, 7, 8, 9
作用：按 1→2、2→3 路由光信号，把发射光送进感测纤，再把瑞利回波送至接收链。
说明：三个尾纤的编号需对应光路图；环形器不同于隔离器。

产品页：[DK Photonics 官方页面](https://www.dkphotonics.com/product/1550nm-3-port-polarization-insensitive-optical-circulator.html)
原图：[C08 图片原始地址](https://www.dkphotonics.com/wp-content/uploads/3-port-PIOC-fc-apc-1024x640.png)
原尺寸：[1024, 640]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C09 掺铒光纤放大器 / EDFA

厂家 / 型号：Optilab；C-band 双级台式 EDFA 系列
对应路线：1, 2, 3, 4, 5, 6, 7, 8
作用：提高探测脉冲功率，增加可用瑞利回波；同时引入 ASE，并存在增益饱和。
说明：图中表示发射放大；需要匹配峰值功率、平均功率与脉冲重复率。

产品页：[Optilab 官方页面](https://www.optilab.com/en-ca/products/dual-stage-erbium-doped-fiber-amplifier-c-band-benchtop)
原图：[C09 图片原始地址](https://www.optilab.com/cdn/shop/files/2_030882ad-dcb2-4b04-96e6-d0c4c0cce57d.png?v=1760593674)
原尺寸：[3245, 2168]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C10 光带通滤波器 / BPF

厂家 / 型号：PriTel；PM-TB-TWF 可调带通滤波器
对应路线：1, 2, 3, 4, 5, 6, 7, 8
作用：通过探测光频带并抑制 EDFA 带外 ASE；保留脉冲及频移所需的光谱宽度。
说明：不能把电学低通滤波器当作这里的光带通滤波器。

产品页：[PriTel 官方页面](https://www.pritel.com/tbtwf.html)
原图：[C10 图片原始地址](https://www.pritel.com/images/TBTWF_small.gif)
原尺寸：[533, 200]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C11 光纤声光调制器 / AOM

厂家 / 型号：AeroDIODE；1550AOM 高速封装系列
对应路线：1, 2, 4, 5, 6
作用：通过 RF 驱动控制脉冲通断，同时使所选衍射级的光频发生偏移；双脉冲方案使用两只。
说明：照片为厂家产品外观图；需要配套 RF 驱动器。

产品页：[AeroDIODE 官方页面](https://www.aerodiode.com/product/fiber-coupled-aom/)
原图：[C11 图片原始地址](https://www.aerodiode.com/wp-content/uploads/2021/07/Fiber-coupled-AOM-model-2-front.jpg)
原尺寸：[1400, 1000]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C12 电光强度调制器 / IM / MZM

厂家 / 型号：Exail；LiNbO3 强度调制器系列
对应路线：3, 8
作用：利用 Mach-Zehnder 电光干涉把连续光切成脉冲；需控制 RF 电压与直流偏置。
说明：工作点决定消光比；理想式忽略插损与残余啁啾。

产品页：[Exail 官方页面](https://www.exail.com/index.php/fr/product/linbo3-intensity-modulators-photonics)
原图：[C12 图片原始地址](https://www.exail.com/media/7912/exail-produits-linbo3-intensity-modulators_2835x975.png)
原尺寸：[2835, 975]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C13 IQ / 双平行 MZ 调制器 / SSB-EOM

厂家 / 型号：Exail；MXIQER-LN-30
对应路线：8
作用：用正交 RF 驱动和合适偏置抑制载波/一侧边带，实现光学单边带频移。
说明：SSB 是工作方式；对应实物为 IQ / DPMZM，而非一个软件盒。

产品页：[Exail 官方页面](https://www.exail.com/news/unlocking-qkd-potential-with-optical-iq-modulator)
原图：[C13 图片原始地址](https://www.exail.com/media/9005/mxiqerln30-exail_2835x553.png)
原尺寸：[2835, 553]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C14 电光相位调制器 / PM

厂家 / 型号：Exail；LiNbO3 相位调制器系列
对应路线：5
作用：在 Michelson 干涉臂上施加已知相位载频，以 PGC 谐波解调提取声波相位。
说明：反射臂会两次经过 PM；有效调制深度需包括去、回时延。

产品页：[Exail 官方页面](https://www.exail.com/product/linbo3-phase-modulators-photonics)
原图：[C14 图片原始地址](https://www.exail.com/media/10479/exail-produit-linbo3-phase-modulators_804x154.png)
原尺寸：[804, 154]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C15 半导体光放大器 / SOA

厂家 / 型号：AeroDIODE；1550SOA 蝶形封装系列
对应路线：7
作用：由脉冲电流改变增益，门控啁啾连续光并放大脉冲，保留其频率扫描信息。
说明：器件与驱动器分别展示；ASE、饱和和载流子动力学在理想式中省略。

产品页：[AeroDIODE 官方页面](https://www.aerodiode.com/product/semiconductor-optical-amplifier/)
原图：[C15 图片原始地址](https://www.aerodiode.com/wp-content/uploads/2026/08/SOA-butterfly-1550nm.jpg)
原尺寸：[768, 478]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C16 SOA 脉冲电流驱动器 / SOA driver

厂家 / 型号：AeroDIODE；SOA-std 开放式驱动系列
对应路线：7
作用：向 SOA 注入同步的短电流脉冲；设定脉宽、重复率、峰值电流与温度。
说明：图片为 SOA 与开放式驱动板组合；外部 AWG / TTL 提供触发。

产品页：[AeroDIODE 官方页面](https://www.aerodiode.com/product/soa-pulsed-driver/)
原图：[C16 图片原始地址](https://www.aerodiode.com/wp-content/uploads/2022/08/Semiconductor-optical-amplifier-SOA-std.jpg)
原尺寸：[1024, 768]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C17 偏振控制器 / PC

厂家 / 型号：DK Photonics；3PPC560 三环手动控制器
对应路线：2, 3
作用：调节本振或信号的偏振，使两路电场有充分重叠，改善相干接收干涉可见度。
说明：这里 PC 指 Polarization Controller；需把光纤绕入三环。

产品页：[DK Photonics 官方页面](https://www.dkphotonics.com/product/3-paddle-manual-polarization-controllers-56-mm-loop.html)
原图：[C17 图片原始地址](https://www.dkphotonics.com/wp-content/uploads/3-paddle-manual-polarization-controllers-56-mm-loop-2-1024x640.png)
原尺寸：[1024, 640]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C18 可变光衰减器 / VOA

厂家 / 型号：DK Photonics；1550 nm 机械式 VOA
对应路线：2, 3
作用：调节本振光功率，平衡信号与本振并避免接收器饱和；也便于调试功率预算。
说明：A_dB 为功率衰减量；场幅衰减使用 20 作分母。

产品页：[DK Photonics 官方页面](https://www.dkphotonics.com/product/1550nm-single-mode-mechanical-variable-optical-attenuator.html)
原图：[C18 图片原始地址](https://www.dkphotonics.com/wp-content/uploads/voa-standard-size-1024x640.png)
原尺寸：[1024, 640]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C19 法拉第旋转镜 / FRM

厂家 / 型号：DK Photonics；1550 nm Faraday mirror
对应路线：5
作用：反射回光并产生约 90° 的往返偏振旋转，补偿理想互易光纤臂的偏振扰动。
说明：J 为单程 Jones 矩阵，F 为理想 FRM 矩阵。两只 FRM 分别位于长、短反射臂末端。

产品页：[DK Photonics 官方页面](https://www.dkphotonics.com/product/1550nm-faraday-mirror.html)
原图：[C19 图片原始地址](https://www.dkphotonics.com/wp-content/uploads/FM-5.5x35-fp-1024x640.png)
原尺寸：[1024, 640]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C20 90° 光学混频器 / 90° hybrid

厂家 / 型号：Optoplex；90Degree Optical Hybrid
对应路线：3
作用：把回波与本振混合，得到 I+、I-、Q+、Q- 四个光学输出，供两对平衡探测。
说明：照片中硬币为厂家尺寸参照；混频器本身不等于 ADC 或数字 I/Q。

产品页：[Optoplex 官方页面](https://www.optoplex.com/Optical_Hybrid.htm)
原图：[C20 图片原始地址](https://www.optoplex.com/images/product/90Degree_Optical_Hybrid.png)
原尺寸：[396, 296]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C21 感测光纤 / 光缆 / Sensing fiber

厂家 / 型号：AFW Technologies；SMF 光纤盘产品系列
对应路线：1, 2, 3, 4, 5, 6, 7, 8, 9
作用：沿纤产生连续分布的瑞利散射；声波引起轴向应变与光程变化，编码进回波。
说明：照片展示实验室光纤盘；现场应使用合适封装与机械耦合的感测光缆。

产品页：[AFW Technologies 官方页面](https://www.afwtechnologies.com.au/delay_lines.html)
原图：[C21 图片原始地址](https://www.afwtechnologies.com.au/images/3%20Reels-1.jpg)
原尺寸：[478, 460]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C22 延迟 / 参考光纤 / Delay fiber

厂家 / 型号：AFW Technologies；SM1 光纤延迟盒系列
对应路线：4, 5, 9
作用：建立干涉臂时延差，或设置 OFDR 参考与辅助 MZI 时延；它不承担现场声波感测。
说明：ΔL 是单程物理臂长差；Michelson 往返光程差为两倍。

产品页：[AFW Technologies 官方页面](https://www.afwtechnologies.com.au/delay_lines.html)
原图：[C22 图片原始地址](https://www.afwtechnologies.com.au/images/box-1000m-smaller.jpg)
原尺寸：[472, 328]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C23 光纤跳线与连接器 / FC/APC

厂家 / 型号：AFW Technologies；FC/APC 单模跳线
对应路线：1, 2, 3, 4, 5, 6, 7, 8, 9
作用：连接器件间光路；APC 斜面端接有助于降低反射，PM 支路还需匹配偏振轴。
说明：APC 与 UPC 不应直接混接；裸尾纤方案可以熔接代替接头。

产品页：[AFW Technologies 官方页面](https://www.afwtechnologies.com.au/patchcord.html)
原图：[C23 图片原始地址](https://www.afwtechnologies.com.au/images/patchcordfca.jpg)
原尺寸：[538, 378]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C24 低反射光纤终端 / Terminator

厂家 / 型号：Fibertronics；FT-TRM-231 FC/APC
对应路线：4, 9
作用：吸收未使用端口的光，抑制额外反射和寄生干涉；感测纤末端也可采用低反射处理。
说明：不向终止输入端注入独立光场；图中终端不是 FRM。

产品页：[Fibertronics 官方页面](https://fibertronics.com/fcapc-terminator)
原图：[C24 图片原始地址](https://www.fibertronics.com/site/FT-TRM-231_00.default.png)
原尺寸：[800, 667]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C25 单通道光电接收器 / PD + TIA

厂家 / 型号：Optilab；HPR-IG InGaAs 接收器系列
对应路线：1, 4, 5, 6, 7, 8, 9
作用：将光功率转换为电流，再由跨阻放大器转换为采样电压；路线 9 用于辅助 MZI。
说明：路线 4 需要三通道同步采样；照片为厂家 HPR 产品页配图。

产品页：[Optilab 官方页面](https://www.optilab.com/products/100-mhz-high-gain-ingaas-photoreceiver-module)
原图：[C25 图片原始地址](https://www.optilab.com/cdn/shop/files/HPR.png?v=1760515607)
原尺寸：[3097, 2648]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C26 平衡光电接收器 / BPD

厂家 / 型号：Optoplex；BR-C0100B1DC
对应路线：2, 3, 9
作用：两只 PD 对两个光学输出分别探测后相减，提取干涉项并抑制共模强度成分。
说明：路线 3 的 I、Q 各需要一对；共模抑制依赖响应与增益匹配。

产品页：[Optoplex 官方页面](https://www.optoplex.com/Balanced_Photo-Receivers.htm)
原图：[C26 图片原始地址](https://www.optoplex.com/images/Balanced_PD_BR-C0100B1DC.jpg)
原尺寸：[3137, 2385]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C27 高速数据采集卡 / ADC / DAQ

厂家 / 型号：AlazarTech；ATS9440 四通道 PCIe 卡
对应路线：1, 2, 3, 4, 5, 6, 7, 8, 9
作用：把探测器电压离散采样，形成每次迹线/扫描的数据，送往计算与存储单元。
说明：照片仅作硬件识别；采样率、模拟带宽、位数和通道数需按方案确定。

产品页：[AlazarTech 官方页面](https://www.alazartech.com/en/product/ats9440/16/)
原图：[C27 图片原始地址](https://www.alazartech.com/LowCal/Resources/static/images/uploads/originals/products/16/6/6445ATS9440AlazarTech.jpg)
原尺寸：[360, 288]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C28 脉冲 / 任意波形发生器 / AWG

厂家 / 型号：RIGOL；DG5000 系列
对应路线：1, 2, 3, 4, 5, 6, 7, 8
作用：产生门控、触发、啁啾电压或 PM 载频；同步发射时序和数据采集。
说明：一个系统可由多通道 AWG / FPGA 集成实现，图中分开的电框不一定各占一台。

产品页：[RIGOL 官方页面](https://www.rigol.com/intl/products/function-arbitrary-waveform-generator/DG5000.html)
原图：[C28 图片原始地址](https://www.rigol.com/dam/jcr:6350a8e1-c348-4b0f-b9e3-fe5458293928/DG5000-front.png)
原尺寸：[600, 600]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C29 AOM 射频驱动器 / RF driver

厂家 / 型号：AeroDIODE；Fiber-coupled AOM RF driver
对应路线：1, 2, 4, 5, 6
作用：向 AOM 输出匹配频率的 RF 功率，并用 TTL 或模拟输入控制幅度，实现光门控。
说明：路线 6 两通道需要共同参考时钟和稳定相对初相。

产品页：[AeroDIODE 官方页面](https://www.aerodiode.com/product/fiber-coupled-aom/)
原图：[C29 图片原始地址](https://www.aerodiode.com/wp-content/uploads/2021/07/Fiber-coupled-AOM-RF-Driver-analog.jpg)
原尺寸：[1400, 1000]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C30 直接数字频率合成器 / DDS

厂家 / 型号：Analog Devices；AD9914 评估板
对应路线：6, 8
作用：产生可控频率和相位的 RF 信号；路线 8 用频率步进驱动 SSB，路线 6 可用作相干 RF 基准。
说明：评估板需要时钟、控制与供电；不等同于完整配套 AOM 功率驱动。

产品页：[Analog Devices 官方页面](https://wiki.analog.com/resources/eval/ad9914-user-guide)
原图：[C30 图片原始地址](https://wiki.analog.com/_media/resources/eval/user-guides/ad9914/figure1_ad9914_evb.png?w=700&tok=01fb86)
原尺寸：[700, 347]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C31 激光电流与温控驱动 / LD driver / TEC

厂家 / 型号：AeroDIODE；CCS-CW 电流 / TEC 封装
对应路线：7
作用：稳定 LD 偏置电流与温度；高速电流调制输入改变瞬时光频，为啁啾提供电学控制。
说明：照片代表偏置/温控硬件；图示 CCS-CW 本身不能保证快啁啾，需独立高速端。

产品页：[AeroDIODE 官方页面](https://www.aerodiode.com/product/laser-diode-driver/)
原图：[C31 图片原始地址](https://www.aerodiode.com/wp-content/uploads/2019/12/Laser-Driver-01-1-600x450.jpg)
原尺寸：[600, 450]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C32 电光调制器电压驱动 / EOM RF driver

厂家 / 型号：Exail；DR-AN 模拟驱动系列
对应路线：3, 5, 8
作用：将波形源电压放大到所需调制幅度，驱动 IM、PM 或 IQ 的 RF 端。
说明：图片展示射频封装；PGC 低频载波可使用合适的低频电压驱动。

产品页：[Exail 官方页面](https://www.exail.com/product/analog-drivers-photonics)
原图：[C32 图片原始地址](https://www.exail.com/media/10413/exail-produit-analog-drivers_804x530.png)
原尺寸：[804, 530]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C33 MZ / IQ 偏置控制器 / MBC

厂家 / 型号：Exail；MBC-IQ-LAB；IQ 偏置控制
对应路线：3, 8
作用：锁定调制器直流工作点；IM 保持所需消光点，IQ 保持载波与边带抑制条件。
说明：图片为 IQ 专用控制器；路线 3 应选 MZ 适用型号，或采用手动稳定偏置。

产品页：[Exail 官方页面](https://www.exail.com/product/digital-iq-modulators-bias-controller-photonics)
原图：[C33 图片原始地址](https://www.exail.com/media/11975/exail-product-digital-iq-modulators-bias-controller_1000x700.png)
原尺寸：[1000, 700]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C34 实时数字处理硬件 / FPGA / DSP

厂家 / 型号：Digilent；Genesys 2 Kintex-7 开发板
对应路线：1, 2, 3, 4, 5, 6, 7, 8, 9
作用：实现触发控制、数字下变频、I/Q、三相位/PGC 解调、相关与 FFT 等实时处理。
说明：PGC、数字 I/Q、相关与 FFT 是算法；开发板需编程及数据接口适配。

产品页：[Digilent 官方页面](https://digilent.com/shop/genesys-2-amd-kintex-7-fpga-development-board/)
原图：[C34 图片原始地址](https://cdn11.bigcommerce.com/s-7gavg/images/stencil/1280x1280/products/460/5643/15998876535_127d3780ec_o__76232.1602872655.386.513__24606.1749764241.png?c=2)
原尺寸：[386, 343]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。

## C35 上位机与计算存储 / Host PC

厂家 / 型号：Dell；Dell Pro 14 笔记本外观示例
对应路线：1, 2, 3, 4, 5, 6, 7, 8, 9
作用：配置仪器、接收与存储数据，运行离线/部分在线解调，显示声波时空图与谱分析。
说明：此处 PC 指计算机；PCIe 采集卡通常需要兼容台式机或服务器。

产品页：[Dell 官方页面](https://www.dell.com/en-us/shop/laptops/sf/latitude-laptops)
原图：[C35 图片原始地址](https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/dell-pro/pc14250/media-gallery/notebook-dell-pro-pc14250-hd-fhd-gy-gallery-1.psd?fmt=png-alpha&pscan=auto&scl=1&hei=804&wid=1062&qlt=100,0&resMode=sharp2&size=1062,804)
原尺寸：[1062, 804]；显示处理：PNG 格式；透明背景铺白；仅裁去近白边缘；保留厂家标记；必要时等比例缩小。
