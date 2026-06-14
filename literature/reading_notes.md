# 阅读笔记

## 2024 Li4SiO4 单颗粒尺寸效应 DEM

主题：Li4SiO4 ceramic pebble 单颗粒压缩，使用 bonded sub-ball 思路模拟尺寸效应和破碎。

初步记录：

- 论文题名：Investigation of the size-dependent crushing behavior of Li4SiO4 pebbles via discrete element method
- 期刊：Fusion Engineering and Design
- 年份：2024
- 卷/文章号：Volume 199, 114105
- DOI：10.1016/j.fusengdes.2023.114105
- 与本课题关系：非常近邻。该文已经针对 Li4SiO4 单颗粒压缩建立 bonded sub-ball DEM，需要重点对照其 sub-ball 数量、parallel bond 参数、缺陷/Weibull 处理和尺寸效应结论。
- 对本课题的启发：
  - 单颗粒标定必须包含尺寸效应和强度离散性，不应只标定一个平均 crush load。
  - 该文使用 random sub-ball removal scheme 表征固有缺陷，并识别 splitting、progressive fracturing、explosive 三类破坏模式。
  - 可以借鉴其缺陷引入方法，但本课题的差异应放在“单颗粒模板注入球床后，bond 断裂、真实碎片与球床宏观演化的耦合”。
  - 文章若使用 PFC 或通用 DEM，而本课题使用 LIGGGHTS-INL，则需要突出开源可复现和球床尺度扩展。

待提取：

- sub-ball 数量；
- parallel bond stiffness、strength、bond radius；
- Li4SiO4 单颗粒实验 crush load；
- Weibull 参数；
- 破碎模式；
- 与粒径相关的标定关系。

## 2026 Crushable DEM pebble bed crushing evolution

主题：基于理论 crushing model 的球床 crushable DEM，关注 HCCB 包层球床破碎演化。

初步记录：

- 论文题名：Crushing evolution in pebble bed based on a novel method: A crushable DEM study
- 期刊：Nuclear Science and Techniques
- 年份：2026，在线发表 2025-12-05
- DOI：10.1007/s41365-025-01806-0
- 与本课题关系：最新近邻球床尺度研究。它使用 Weibull、fractal theory、tensile strength assignment、crush detection 和 sub-particle insertion 描述球床破碎演化。
- 对本课题的启发：
  - 它是“球床尺度简化可破碎 DEM”的强对照。
  - 本课题可以强调 LIGGGHTS-INL bonded-particle 模板的优势：破碎从颗粒内部 bond 失效和碎片形成自然产生，而不是基于单个球的 stress criterion 后再替换/插入子颗粒。
  - 后处理可以借鉴其 crushing hot zone、径向/轴向分层统计和破碎位置演化。

待提取：

- 球床几何；
- 应变范围；
- 破碎判据；
- 子颗粒插入策略；
- 破碎空间统计；
- 与 2021 crushable pebble bed DEM 的关系。

## 2024 破碎球床压降实验

主题：particle crushing 对 helium purge gas pressure drop 的影响。

初步记录：

- 论文题名：Experimental study on the pressure drop of helium purge gas in particle crushing pebble beds
- 期刊：Fusion Engineering and Design
- 年份：2024
- 卷/文章号：Volume 207, 114631
- DOI：10.1016/j.fusengdes.2024.114631
- 与本课题关系：说明颗粒破碎不只是力学问题，还会显著影响 purge gas 压降。可以作为论文引言中“为什么破碎重要”的最新支撑，也可作为后续拓展到孔隙率/渗透性/流动阻力的依据。

待提取：

- 破碎率定义；
- 压降与破碎率关系；
- 球床填充率变化；
- 是否使用 Li4SiO4 或类似 ceramic breeder pebbles；
- 可否与本课题的破碎后孔隙率/碎片粒径分布对应。

## 2021 Li4SiO4 颗粒结构性能初步研究

主题：Li4SiO4 pebbles structural performance，含单颗粒压碎数据。

初步记录：

- 论文题名：Preliminary investigation of Li4SiO4 pebbles structural performance
- 期刊：Fusion Engineering and Design
- 年份：2021
- 文章号：112677
- DOI：10.1016/j.fusengdes.2021.112677
- 与本课题关系：单颗粒 crush load 标定的首选实验来源之一。

待提取：

- 样品制备方法；
- 粒径范围；
- crush load 均值和离散性；
- 压缩实验边界条件；
- 是否报告力-位移曲线。

## 2021 Crushable ceramic pebble bed 一维压缩 DEM

主题：crushable ceramic pebble bed 一维压缩 DEM。

初步记录：

- 论文题名：DEM simulation of mechanical behavior in one-dimensional compression of crushable ceramic pebble bed
- 期刊：Fusion Engineering and Design
- 年份：2021
- 文章号：112783
- DOI：10.1016/j.fusengdes.2021.112783
- 与本课题关系：球床压缩对照文献。该类研究通常将破碎颗粒比例预设为参数，而本课题希望用 bond 断裂自然产生破碎。

待提取：

- 球床几何尺寸；
- 颗粒尺寸和数量；
- 预设破碎比例；
- 压缩应变范围；
- 宏观应力-应变曲线；
- DEM 接触参数。

## 2011 Crush probability analysis

主题：ceramic breeder pebble beds 在机械应力下的破碎概率。

初步记录：

- 论文题名：Crush probability analysis of ceramic breeder pebble beds under mechanical stresses
- 期刊：Journal of Nuclear Materials
- 年份：2011
- DOI：10.1016/j.jnucmat.2010.12.078
- 与本课题关系：可以作为简化统计模型对照。它把 DEM 接触力与单颗粒 crush-load 分布耦合，估算球床破碎概率。

待提取：

- crush probability 定义；
- 接触力统计方式；
- 单颗粒强度分布；
- 球床压缩边界条件；
- 可用于对照的破碎概率曲线。

## LIGGGHTS-INL

主题：LIGGGHTS-INL 的 bonded-particle model 能力。

初步记录：

- 软件页：Idaho National Laboratory LIGGGHTS-INL
- GitHub：https://github.com/idaholab/LIGGGHTS-INL
- 与本课题关系：主模拟平台。需要确认可用 atom style、bond style、bond 断裂输出和 data 文件格式。

待确认：

- `bond_style` 是否包含适合颗粒破碎的模型；
- 是否有 `bond/gran` 或 cohesion bond 断裂；
- 是否有官方 examples；
- data 文件 Atoms/Bonds sections 的准确格式。
# Fang et al. (2026): Li4SiO4 bed crushing and purge-gas pressure drop

- Published in *Fusion Engineering and Design* 224, 115604; DOI: 10.1016/j.fusengdes.2025.115604.
- Uniaxial cyclic-compression experiments were performed on Li4SiO4 breeder pebble beds under different stress and temperature conditions.
- Breakage ratio and fragment-size distribution were measured by sieving. Higher stress and temperature increased breakage and the mass fraction of small fragments.
- Reconstructed crushed beds with 3-15% breakage were used for helium pressure-drop tests. Pressure drop increased with breakage ratio; the reported Ergun-equation deviation remained within 10.6% at the most fragmented condition.
- Use in the present manuscript: external evidence that mechanically generated fragments have a functional purge-flow consequence. The present DEM event database supplies mother-pebble-resolved initiation and propagation information that the bulk experiment does not resolve.
- Claim boundary: cite the published experiment for qualitative consequence and trend only; do not describe the present room-temperature screening curves as a quantitative reproduction of its cyclic and temperature-dependent tests.
