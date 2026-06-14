# SP-001 单颗粒压缩最小算例

目标：用 LIGGGHTS-INL 的 `particletemplate/multiplespheres` 和 `cohesion bond` 创建 500 子颗粒 Li4SiO4 bonded sphere，并建立第一个可运行的压缩算例框架。

## 文件

- `data/li4sio4_sp_500.multisphere`: 500 子颗粒 multisphere 模板，单位为 m。
- `data/li4sio4_sp_500_nooverlap.multisphere`: 无初始重叠的 500 子颗粒模板，当前 SP-001 默认使用。
- `in.single_pebble_compression.lmp`: LIGGGHTS-INL 输入脚本草案。

## 重要说明

当前已经在本机用 `external/LIGGGHTS-INL/src/lmp_mpi_no_vtk` 完成 smoke test。`mpi_no_vtk` 版本不支持 VTK dump，因此当前脚本使用文本 dump。

## 模型路线

采用 LIGGGHTS-INL cohesive bond 模型：

```lammps
pair_style gran model hertz tangential history cohesion bond stressBreak on createBondAlways off
fix clump all particletemplate/multiplespheres ... spheres file data/li4sio4_sp_500.multisphere scale 1.0 bonded yes
create_particles clump single 0.0 0.0 0.0 velocity 0.0 0.0 0.0
compute bond_status all bond/counter
compute bond_force all pair/gran/local/bond
```

第一版先保证 bonded sphere 创建、断键统计和输出链路跑通。压缩边界可以有两条路线：

1. 用上下端部子颗粒分组，固定底部并移动顶部，适合作为最小力学调试算例。
2. 用上下 mesh wall/servo wall 压缩，适合作为正式单颗粒压缩验证算例。

## 当前 smoke test 结果

命令：

```bash
../../../external/LIGGGHTS-INL/src/lmp_mpi_no_vtk -in in.single_pebble_compression.lmp -var nsteps 1001
```

结果：

- 500 atoms 创建成功；
- 第 1000 步显示 6723 条 intact particle-particle bonds；
- 0 条 bond 断裂；
- dangerous neighbor builds 为 0；
- 当前模板和建键策略可作为后续标定起点。

关键修正：

- 原始模板存在子颗粒初始重叠，会导致大量 bond 立即断裂；
- 当前默认改用 `li4sio4_sp_500_nooverlap.multisphere`；
- `tsCreateBond` 设为 1.0，使 bond 在第 1 步一次性创建；
- `createBondAlways` 保持 off，避免每一步重复建键。
