# SP-002 刚性压板单颗粒压缩

SP-002 在 SP-001 的基础上，将端部子颗粒移动调试边界替换为上下刚性 mesh 压板。

## 目标

- 使用 `mesh/surface/stress` 记录上下压板总反力；
- 使用 `move/mesh` 让上压板恒速下压；
- 通过 `thermo_style` 输出力-位移和 bond 统计，用后处理脚本抽取曲线；
- 保持 bonded sphere 初始稳定，避免初始重叠导致非物理断键。

## 当前状态

该算例使用：

- `data/li4sio4_sp_500_nooverlap.multisphere`
- `meshes/bottom_plate.stl`
- `meshes/top_plate.stl`
- `in.plate_compression.lmp`

已完成 1000 步 smoke test 和第一版快速加载强度扫描。

### Smoke test

- 500 atoms；
- 6723 created/intact bonds；
- 0 broken bonds；
- 上板位移 `5e-10 m`；
- 当前压板间距为 `z = +/-0.70 mm`，该 smoke test 尚未进入接触加载阶段；
- thermo CSV：`../../../data/processed/SP-002_plate_smoke_thermo.csv`。

运行方式：

```bash
../../../external/LIGGGHTS-INL/src/lmp_mpi_no_vtk -in in.plate_compression.lmp -var nsteps 1000
```

注意：`fix print` 在当前 LIGGGHTS-INL bonded mesh-wall 组合中会触发 MPI abort，因此暂时只从 `log.liggghts` 的 thermo 表抽取载荷曲线。

### 快速加载强度扫描

运行脚本：

```bash
../../../scripts/run_sp002_plate_case.sh SP-002-strength-50MPa 30000 -1.0 5.0e7 5.0e7 1.0e-6 1.0e-4 7.9460215e-6
../../../scripts/analyze_sp002_curve.py ../../../data/processed/SP-002-strength-50MPa_thermo.csv \
  --summary ../../../data/processed/SP-002-strength-50MPa_summary.csv \
  --plot ../../../data/processed/SP-002-strength-50MPa_curve.svg
```

第一版调试扫描采用上板速度 `1 m/s`，用于快速验证破碎趋势，不作为最终准静态标定结果。

| bond strength | peak top force | first break displacement | final broken bonds |
| --- | ---: | ---: | ---: |
| 25 MPa | 3.99 N | 0.105 mm | 242 |
| 50 MPa | 6.67 N | 0.105 mm | 193 |
| 100 MPa | 16.47 N | 0.110 mm | 123 |

汇总表：`../../../data/processed/SP-002-strength-scan_summary.csv`。
