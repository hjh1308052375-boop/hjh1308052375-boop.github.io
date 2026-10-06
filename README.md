# 胡俊昊的个人学术主页

中英文静态网站，使用原生 HTML、CSS 和 JavaScript，由 GitHub Pages 托管。

## 知识栏目

基础原理、井下布设、井生命周期、水泥水化监测，以及三类仪器的分点原理说明：

- `knowledge/das-optical-atlas.html`：DAS 测量机制与 9 类代表性实现方式。
- `knowledge/dts-optical-atlas.html`：DTS 测量、标定与 6 类代表性路线。
- `knowledge/dss-optical-atlas.html`：DSS 测量、温度补偿与 7 类代表性路线。

页面按“测量什么、测量过程、实现方式、元件作用、解释边界、参考来源”分点阅读。每条路线直接说明工作方式、观测量及局限；光路、公式和完整元件列表可按需展开。保留中英文切换和页内目录，不提供 PDF 图册或资料包下载入口。页面 URL 保留以兼容已有链接。

元件照片有厂家来源；X 编号明确为原创功能示意，不冒充实物照片。

## 编辑和构建

修改 `tools/atlas_content.py` 中的内容，运行：

```powershell
python tools/sensing_notes.py
python tools/verify_sensing_atlases.py
python -m http.server 8765 --bind 127.0.0.1
```

内容在 `tools/atlas_content.py`，分点呈现在 `tools/sensing_notes.py`。原图件构建工具保留用于维护可编辑图片，运行后也会更新分点知识页。构建工具需要 Python 的 ReportLab、Pillow，以及本机 Microsoft YaHei 字体；验证工具还使用 NumPy、pypdf。网页本身不需要第三方 CDN。

页面插图和来源缓存保存在 `knowledge/atlases/`；此前生成的 PDF、ZIP 和原项目文件作为本地维护资料保留，不作为知识页的阅读入口。

本地复制的 `光纤传感原理/` 保留原始项目和历史版本，工作记录在 `work/atlas-qa/`，两者不纳入网站 Git 版本。不要将历史构建目录当作网站入口。

## 验证范围

已进行本地链接、ZIP 完整性、PDF 内容、光路布局，以及拉曼校正、布里渊补偿、瑞利谱移符号的独立数值自检。浏览器检查包括语言切换、路线/元件筛选、放大和移动端布局。

图示为概念架构，非按比例、非实测数据。结构和代数校验不能证明仪器性能；温度与应变灵敏度、机械耦合和现场解释须另行标定与验证。厂家图像版权归原权利人。
