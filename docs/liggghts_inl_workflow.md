# LIGGGHTS-INL 工作流草案

## 1. 当前软件状态

命令行 PATH 中暂未发现 `liggghts`、`lmp` 或 `lmp_serial`。本项目已在 `external/LIGGGHTS-INL/src/` 下编译出本地测试可执行文件：

```text
external/LIGGGHTS-INL/src/lmp_mpi_no_vtk
```

该版本为 no-VTK 构建，可用于文本输出和核心 DEM 验证。

推荐顺序：

1. 获取 LIGGGHTS-INL 源码；已完成。
2. 编译 no-VTK MPI 版本；已完成。
3. 确认 bond 相关模型是否编译可用；已完成。
4. 跑通本项目 SP-001 smoke test；已完成。
5. 跑通 mesh 压板 SP-002 smoke test；已完成。
6. 后续如需 ParaView/VTK 输出，再单独编译 VTK 版本。

本地构建额外加入了一个 contact-model 白名单项：

```text
GRAN_MODEL(HERTZ, TANGENTIAL_HISTORY, COHESION_BOND, ROLLING_OFF, SURFACE_DEFAULT)
```

否则 `fix wall/gran ... cohesion bond mesh ...` 会在创建 wall contact implementation 时失败。

## 2. 已确认的 LIGGGHTS-INL bonded-particle 路线

源码和官方示例中已经确认，适合本课题的路线是：

```lammps
atom_style granular
pair_style gran model hertz tangential history cohesion bond stressBreak on createBondAlways off
fix clump all particletemplate/multiplespheres ... spheres file data/li4sio4_sp_500.multisphere scale 1.0 bonded yes
create_particles clump single 0.0 0.0 0.0 velocity 0.0 0.0 0.0
compute bond_status all bond/counter
compute bond_force all pair/gran/local/bond
```

这条路线来自 LIGGGHTS-INL 的 `examples/LIGGGHTS/INL/cohesive_bond` 和 `cohesive_bond_nonlinear_tension` 示例。它比传统 `bond_style` 更适合颗粒破碎，因为 cohesive bond 是 granular pair model 的一部分，可以和颗粒接触、墙面接触、断键统计和 VTK bond 输出自然结合。

### 关键材料参数

需要通过 `fix property/global` 定义：

- `radiusMultiplierBond`
- `normalBondStiffnessPerUnitArea`
- `tangentialBondStiffnessPerUnitArea`
- `maxSigmaBond`
- `maxTauBond`
- `dampingNormalForceBond`
- `dampingTangentialForceBond`
- `dampingNormalTorqueBond`
- `dampingTangentialTorqueBond`
- `tsCreateBond`
- `createDistanceBond`

其中 `stressBreak on` 时，bond 根据最大法向/切向应力断裂；若不用应力断裂，则可用 `maxDistanceBond` 控制过拉伸断裂。

## 3. 单颗粒压缩最小算例结构

建议第一个 LIGGGHTS-INL 单颗粒算例包含：

- `in.single_pebble_compression`: 主输入脚本；
- `data.single_pebble`: 子颗粒和 bond 拓扑；
- `mesh` 或 wall 定义：上下刚性压板；
- `dump`: 输出颗粒坐标、速度、受力和 bond 断裂状态；
- `post`: 后处理力-位移曲线和 bond 断裂曲线。

## 4. 几何模板

当前已经生成第一版模板：

- 路径：`simulations/single_pebble/templates/sp_500_d1mm/`
- 子颗粒数：500
- 母颗粒直径：1.0 mm
- bond 数：6248
- 平均 bond 配位数：约 25

模板文件：

- `particles.csv`: 子颗粒坐标和半径；
- `bonds.csv`: bond 两端子颗粒和初始长度；
- `summary.md`: 模板摘要。
- `simulations/single_pebble/SP-001/data/li4sio4_sp_500.multisphere`: LIGGGHTS-INL `particletemplate/multiplespheres` 文件，单位 m。
- `simulations/single_pebble/SP-001/data/li4sio4_sp_500_nooverlap.multisphere`: 当前默认使用的无初始重叠模板，单位 m。

## 5. 需要继续确认的 LIGGGHTS-INL 技术点

1. bond 断裂后碎片之间是否自动转为普通颗粒接触。
2. 是否需要在压缩前进行几何松弛，以消除模板初始重叠或不合理内应力。
3. 正式单颗粒压缩应使用 mesh plate、servo wall 还是端部子颗粒分组调试。当前 SP-002 已跑通恒速 mesh plate。
4. 如何稳定输出 bond 断裂事件、断裂时间和断裂位置。
5. 是否需要编译 VTK 版本以输出 `local/gran/vtk` bond 可视化。

## 6. 第一版模拟工况

### SP-001

- 母颗粒直径：1.0 mm；
- 子颗粒数：500；
- 压缩方式：上下刚性板，底板固定，上板恒定速度下压；
- 温度：室温；
- 目标：跑通力-位移曲线和 bond 断裂输出。
- 当前状态：已建立并跑通 `simulations/single_pebble/SP-001/in.single_pebble_compression.lmp` smoke test。

### SP-002

- 压缩方式：上下 `mesh/surface/stress` 刚性压板，底板固定，上板 `move/mesh` 恒速下压；
- 当前状态：已跑通 1000 步 smoke test，500 atoms，6723 intact bonds，0 broken bonds；
- 输出方式：暂时从 `log.liggghts` 的 thermo 表提取载荷曲线；当前组合中 `fix print` 会触发 MPI abort；
- 下一步：缩小初始板距或提高调试加载速度，使上板实际接触颗粒并形成非零反力。

### SP-003

- 在 SP-001 基础上改变 bond stiffness；
- 目标：建立初始刚度对 bond stiffness 的响应曲线。

### SP-004

- 在 SP-001 基础上引入 bond strength 随机分布；
- 目标：模拟 crush load 离散性。
