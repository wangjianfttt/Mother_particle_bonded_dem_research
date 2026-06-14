# 创新边界与差异化分析

## 1. 已有研究类型

### A. 单颗粒 Li4SiO4 bonded sub-ball DEM

2024 年已有研究针对 Li4SiO4 pebbles 建立了单颗粒 DEM 模型，使用 sub-ball 和 parallel bond 描述压碎行为，并引入 random sub-ball removal 表征固有缺陷。该方向已经覆盖：

- 单颗粒尺寸效应；
- 单颗粒压碎模式；
- Weibull 强度离散性；
- 缺陷对 crush load 的影响。

因此，本课题如果只做“单颗粒 bonded sphere 标定”，创新性不足。单颗粒模型必须作为球床研究的标定基础，而不是最终目标。

### B. 预设破碎比例或 crush-probability 球床 DEM

已有球床 DEM 工作常采用两种简化方式：

- 预先设定一定比例的破碎颗粒；
- 用 DEM 接触力和单颗粒 crush-load 分布计算破碎概率。

这类方法可以研究破碎对球床宏观力学响应的影响，但破碎通常不是由颗粒内部裂纹或 bond 断裂自然产生，因此难以直接输出碎片形成、碎片重排和局部断裂路径。

### C. 球床尺度 crushable DEM

最新 crushable DEM 研究开始在球床尺度引入 Weibull、fractal theory、tensile strength assignment、crush detection 和 sub-particle insertion，能够追踪球床破碎演化和破碎热区。

这类研究已经接近本课题目标，因此本课题需要明确差异：

- 使用 LIGGGHTS-INL cohesive bond 直接构造可破碎 bonded-particle 模板；
- 每个母颗粒内部有真实 bond 网络，断裂由 bond stress 触发；
- 碎片由原有子颗粒网络自然断开形成，而不是检测到破碎后再插入替代子颗粒；
- 可直接统计 bond-level failure、fragment topology、fragment size distribution 和 force-chain-triggered breakage。

## 2. 本课题建议创新点

### 创新点 1：Li4SiO4 单颗粒 BPM 多目标标定

不是只匹配平均 crush load，而是同时约束：

- 弹性段刚度；
- 平均 crush load；
- crush load 离散性；
- 破碎模式；
- 碎片粒径分布；
- 子颗粒分辨率收敛性。

### 创新点 2：可破碎模板注入球床

将标定后的 bonded Li4SiO4 母颗粒作为模板注入球床，直接模拟压缩过程中：

- 局部力链形成；
- 母颗粒内部 bond 应力集中；
- bond 断裂；
- 碎片形成；
- 碎片重排和填隙；
- 球床宏观刚度和孔隙率改变。

### 创新点 3：从 bond 断裂到球床宏观性质的统计桥接

建立以下映射：

```text
contact force network
    -> bond stress concentration
    -> bond breakage clusters
    -> mother-particle fragmentation
    -> fragment migration and void filling
    -> stress-strain / porosity / coordination evolution
```

这条链路是本课题区别于“单颗粒破碎 DEM”和“球床破碎概率模型”的核心。

## 3. 第一篇论文建议边界

第一篇论文不建议加入热-流-固全耦合，也不建议直接做完整 HCCB 包层几何。建议聚焦：

> Bonded-particle DEM calibration of Li4SiO4 ceramic breeder pebbles and compression-induced fragmentation evolution in pebble beds

中文表述：

> 基于 bonded-particle DEM 的 Li4SiO4 陶瓷增殖球单颗粒压碎标定及球床压缩破碎演化

## 4. 必须避免的薄弱写法

- 只说“用 500 个小颗粒组成一个大颗粒”，但没有说明为什么 500 足够。
- 只匹配一个 crush load 均值，不匹配强度离散性。
- 球床里只展示漂亮破碎图片，不做统计指标。
- 没有和不可破碎 DEM、预设破碎比例 DEM、crush-probability DEM 对照。
- 没有讨论计算成本和尺度扩展问题。

## 5. 最小发表闭环

1. 单颗粒实验数据整理。
2. 单颗粒 BPM 标定。
3. 单颗粒分辨率和随机性验证。
4. 小规模球床可破碎压缩。
5. 中等规模球床统计。
6. 三组对照：不可破碎、预设破碎、真实 BPM。
7. 输出断键-碎片-宏观响应的因果链。

