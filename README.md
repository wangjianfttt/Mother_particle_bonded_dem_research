# Li4SiO4 Pebble Breakage DEM Research

本项目用于组织聚变堆包层 Li4SiO4 硅酸锂球床颗粒破碎研究。当前研究路线以 LIGGGHTS-INL 为主要 DEM 平台，采用 bonded-particle model 将一个陶瓷球表示为 500 个以上 bonded 小颗粒，先完成单颗粒压碎标定，再将可破碎颗粒模板注入球床，研究压缩载荷下的 bond 断裂、颗粒破碎和球床宏观性质演化。

## Repository and DOI

This repository hosts the code, processed data products, representative inputs, manuscript figures and submission-support materials for the Journal of Nuclear Materials manuscript:

**Acceptance-gated bonded-template DEM reveals localized fracture sequences in Li4SiO4 ceramic breeder beds**

The citable archived reproducibility package uses the same Zenodo DOI:

https://doi.org/10.5281/zenodo.20687351

The live GitHub repository is:

https://github.com/wangjianfttt/Mother_particle_bonded_dem_research

Very large DEM restart files and complete raw local-bond dump histories are not tracked in this repository; they are retained as local audit archives and can be assembled separately if needed.

## Project Structure

- `docs/`: 研究计划、技术路线、模型标定方案。
- `literature/`: 文献矩阵、检索式、阅读笔记。
- `simulations/single_pebble/`: 单颗粒压缩与 BPM 标定算例。
- `simulations/pebble_bed/`: 球床压缩与破碎演化算例。
- `data/`: 实验数据、文献数据、模拟后处理数据。
- `scripts/`: 生成颗粒模板、后处理、绘图脚本。
- `figures/`: 论文和汇报图。
- `submission_packages/`: JNM 投稿包、Editorial Manager 上传包和缩减复现包。

## Current Milestone

第一阶段目标是完成单颗粒 BPM 标定：

1. 从文献提取 Li4SiO4 单颗粒压缩实验数据。
2. 建立 500-1500 子颗粒组成的 bonded sphere 模板。
3. 标定 bond 刚度、强度和非均质参数，使模拟复现实验 crush load、初始刚度和破碎模式。
4. 做分辨率、加载速率、摩擦系数和 bond strength 分布敏感性分析。
