# 参数映射与标定目标

## 1. 实验量到模型量

| 实验/文献量 | DEM 输出量 | 主要控制参数 | 用途 |
|---|---|---|---|
| 单颗粒初始刚度 | 力-位移曲线弹性段斜率 | `normalBondStiffnessPerUnitArea`, `tangentialBondStiffnessPerUnitArea`, `radiusMultiplierBond` | 弹性标定 |
| 平均 crush load | 峰值载荷 | `maxSigmaBond`, `maxTauBond`, `radiusMultiplierBond` | 强度标定 |
| crush load 离散性 | 多随机样本峰值载荷分布 | bond strength 随机分布、缺陷分布 | Weibull 标定 |
| 破碎模式 | 断键空间分布、碎片拓扑 | bond 网络、强度非均质性、加载边界 | 机制验证 |
| 碎片粒径分布 | fragment size distribution | bond 网络密度、强度分布、子颗粒数 | 破碎后验证 |
| 球床应力-应变曲线 | 压板反力/截面积 vs 压缩应变 | 单颗粒强度、摩擦、填充率 | 宏观验证 |
| 孔隙率演化 | 床层体积与颗粒/碎片体积 | 破碎、重排、摩擦 | 功能性质推断 |
| 破碎概率 | 破碎母颗粒数/总母颗粒数 | contact force network、强度分布 | 对照 crush-probability 模型 |

## 2. LIGGGHTS-INL cohesive bond 参数

当前 SP-001 使用以下占位参数，后续必须通过文献和模拟标定更新：

| 参数 | 当前占位值 | 含义 | 标定方向 |
|---|---:|---|---|
| `radiusMultiplierBond` | 1.0 | bond 半径系数 | 影响刚度和强度 |
| `normalBondStiffnessPerUnitArea` | 1.0e14 | 法向 bond 刚度/面积 | 控制弹性段刚度 |
| `tangentialBondStiffnessPerUnitArea` | 5.0e13 | 切向 bond 刚度/面积 | 控制剪切和弯曲响应 |
| `maxSigmaBond` | 5.0e7 | 最大法向应力 | 控制拉/压断裂 |
| `maxTauBond` | 5.0e7 | 最大切向应力 | 控制剪切断裂 |
| `createDistanceBond` | 1.90e-4 m | 初始建键距离 | 控制 bond 网络密度 |

## 3. 第一批参数扫描

### SP-K：刚度扫描

- 固定 `maxSigmaBond` 和 `maxTauBond`；
- 扫描 `normalBondStiffnessPerUnitArea` 和 `tangentialBondStiffnessPerUnitArea`；
- 目标：匹配实验初始刚度。

### SP-S：强度扫描

- 固定已标定刚度；
- 扫描 `maxSigmaBond` 和 `maxTauBond`；
- 目标：匹配平均 crush load。

### SP-R：bond 网络扫描

- 扫描 `createDistanceBond` 或几何脚本中的 `bond-factor`；
- 目标：研究 bond 配位数对刚度、强度和破碎模式的影响。

### SP-W：随机性扫描

- 给 bond strength 加 Weibull 或分组随机系数；
- 每组至少 30 个随机样本；
- 目标：匹配实验 crush load 分布。

