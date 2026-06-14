# 单颗粒 BPM 标定方案

## 1. 标定对象

目标是建立一个可代表 Li4SiO4 陶瓷球的 bonded-particle 模型。母颗粒直径优先取文献常见值，例如 1.0 mm 或 1.0-1.5 mm。每个母颗粒由 500 个以上子颗粒组成，子颗粒之间通过 bond 连接。

## 2. 实验标定数据

需要从文献中提取以下数据：

- 母颗粒直径；
- 压板材料；
- 加载速率；
- 初始弹性段刚度；
- 平均 crush load；
- crush load 标准差或 Weibull 参数；
- 典型破碎模式；
- 若有，碎片粒径分布。

## 3. DEM 参数组

### 子颗粒接触参数

- 密度；
- 杨氏模量；
- 泊松比；
- 颗粒-颗粒摩擦系数；
- 颗粒-压板摩擦系数；
- 阻尼系数或恢复系数。

### Bond 参数

- normal stiffness；
- tangential/shear stiffness；
- bond radius multiplier；
- tensile strength；
- shear strength；
- bond strength 分布类型；
- bond 是否允许弯矩和扭矩。

## 4. 标定顺序

1. 固定几何模板和子颗粒接触参数。
2. 调整 bond normal/shear stiffness，使力-位移曲线弹性段斜率接近实验。
3. 调整 bond tensile/shear strength，使峰值 crush load 接近实验均值。
4. 引入 bond strength 随机分布，使 crush load 离散性接近实验。
5. 调整 bond radius 或邻接阈值，使破碎模式和碎片数量合理。
6. 做 500、800、1500 子颗粒分辨率对比。
7. 做加载速率敏感性分析，确定准静态条件。

## 5. 建议输出图

- 单颗粒模板三维图；
- 压缩过程中的力-位移曲线；
- bond 断裂数量-位移曲线；
- 峰值载荷分布直方图；
- Weibull 图；
- 破碎前后碎片可视化；
- 子颗粒数对 crush load 和刚度的影响。

## 6. 判据

单颗粒模型进入球床前至少满足：

- 平均 crush load 与实验误差小于 10-15%；
- 弹性段刚度与实验处于同一量级，最好误差小于 20%；
- 多个随机样本能够再现实验强度离散性；
- 加载速率降低后峰值载荷变化不显著；
- 子颗粒数增加后主要结果收敛。

