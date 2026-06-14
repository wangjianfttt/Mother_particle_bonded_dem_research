# 下一步行动清单

## 立即任务

1. 精读并补全第一批核心文献矩阵。
2. 从单颗粒实验文献中建立 `data/raw/single_pebble_experimental_data.csv`。
3. 确认本机 LIGGGHTS-INL 是否已安装，记录版本和可用 bond 模型。
4. 写一个脚本生成 500+ 子颗粒 bonded sphere 几何模板。已完成第一版。
5. 搭建第一个单颗粒上下板压缩 LIGGGHTS 算例。已完成 SP-001、SP-002 smoke test 和第一版强度扫描。

## 第一批数据表字段

建议实验数据表包含：

- `source`
- `material`
- `diameter_mm`
- `plate_material`
- `loading_rate_mm_min`
- `mean_crush_load_N`
- `std_crush_load_N`
- `weibull_modulus`
- `sample_count`
- `temperature_C`
- `notes`

## 第一批模拟参数表字段

建议模拟参数表包含：

- `case_id`
- `subparticle_count`
- `mother_diameter_mm`
- `subparticle_diameter_mean_mm`
- `bond_normal_stiffness`
- `bond_shear_stiffness`
- `bond_tensile_strength`
- `bond_shear_strength`
- `bond_radius_multiplier`
- `friction_particle_particle`
- `friction_particle_wall`
- `loading_rate`
- `peak_load_N`
- `initial_stiffness_N_mm`
- `broken_bond_count_at_peak`
- `fragment_count`

## 本机软件状态

当前尚未在命令行 PATH 中发现 `liggghts`、`lmp` 或 `lmp_serial` 可执行文件，但已经在项目本地源码目录编译出：

```text
external/LIGGGHTS-INL/src/lmp_mpi_no_vtk
```

已用该可执行文件跑通 SP-001 smoke test。

## 当前已经完成

- 生成 500 子颗粒、1.0 mm 母颗粒 bonded sphere CSV 模板。
- 导出 LIGGGHTS-INL `particletemplate/multiplespheres` 模板文件。
- 建立 SP-001 单颗粒压缩输入脚本草案。
- 确认 LIGGGHTS-INL cohesive bond 路线：`pair_style gran model hertz tangential history cohesion bond`。
- 编译 LIGGGHTS-INL no-VTK 版本。
- 跑通 SP-001 smoke test：500 atoms，6723 intact bonds，0 broken bonds，dangerous builds 为 0。
- 跑通 SP-002 mesh 压板 smoke test：500 atoms，6723 intact bonds，0 broken bonds，thermo 已抽取到 `data/processed/SP-002_plate_smoke_thermo.csv`。
- 跑通 SP-002 快速加载强度扫描：25/50/100 MPa 三组，峰值上板载荷分别约 3.99/6.67/16.47 N，最终断键数分别为 242/193/123。
- 跑通 SP-002 50 MPa 加载速度敏感性：1.0/0.5/0.25/0.1 m/s 四组，最终断键数分别为 193/123/105/106；阶段性结果记录见 `docs/sp002_preliminary_results.md`。
- 跑通 PB-003 分阶段球床初始化诊断：先远距离造内部键，再按 atom-id 组平移到致密床；1.02 mm 目标间距和底板 `z = -1.506 mm` 的 supported 版本在压缩前保持全部 `80676` 根内部键，且在压缩中产生底板支撑反力和断键演化。
- 跑通 PB-006 第一套 500 颗粒随机床生产算例：proxy 球先在重力下沉积，之后替换成 500 个 SP-002-CAL1 bonded templates，共 `250000` 个子颗粒和 `2938000` 根内部键。压缩前断键为 0；压缩到 0.1975 mm 的最后 local bond dump 时，可定位 271 根内部键断裂，集中在最高两层，涉及 5 个母颗粒。
- 完成 PB-006 seed02：第二套 500 proxy 随机沉积床高约 4.08 mm；bonded-template 初始化检查通过，压缩前保持 `2938000` 根内部键和 0 断键；0.20 mm 生产压缩后定位到 246 根内部断键、9 个断裂事件和 4 个破碎母颗粒。
- 完成 PB-006 seed03：第三套 500 proxy 随机沉积床高约 3.82 mm；0.20 mm 生产压缩后定位到 559 根内部断键、22 个断裂事件和 7 个破碎母颗粒。seed01、seed02 和 seed03 都在 0.0725 mm 位移由最高层 500 号母颗粒首破，但 seed03 的后续顶层扩展更强。
- 完成三套 PB-006 随机床 packing descriptors：seed03 的床高最低、顶层颗粒数最多、顶层平均几何接触度最高，并对应最高断键数和最高终端上板力。结果已汇总到 `tables/pb006_three_seed_packing_descriptors_cutoff1p02mm.csv`、`tables/pb006_packing_descriptor_cutoff_sensitivity.csv` 和 `figures/pb006/pb006_three_seed_packing_breakage.svg`。
- 测试了 PB-006 生产输入中的 contact-local 输出路线，但当前 LIGGGHTS-INL 要求 `pair/gran/local` 和 `wall/gran/local` 在第一次 `run` 前定义，这与 PB-006 “先成内部键、再整体平移模板”的初始化流程冲突。生产输入已恢复为稳定 bond-local 路线；原生接触力链需要后续单独设计 restart/rerun 工作流。
- 完成 seed02/seed03 的 overlap-derived force-path proxy：从已保存的 particle dump 中重建跨母颗粒重叠网络和顶板重叠代理。结果显示 seed03 在相同位移下有更多顶板加载母颗粒和更多上部母颗粒间接触边，支持“更宽的上部载荷路径触发更强破碎级联”的解释。结果见 `figures/pb006/pb006_seed02_seed03_overlap_force_proxy.svg`。
- 完成 PB-006 1000 颗粒尺度初始化检查：1000 proxy 随机沉积床高 7.912 mm；转换为 1000 个 SP-002-CAL1 bonded templates 后共有 500000 个子颗粒，轻量 initcheck 报告 `5876000 = 1000 x 5876` 根内部键且 0 断键。结果见 `tables/pb006_1000_proxy_packing_summary.csv` 和 `data/processed/PB-006-bonded-randompack-1000-seed01-initcheck-light_thermo.csv`。
- 完成 PB-006 1000 颗粒短压缩首破扫描：`PB-006-bonded-randompack-1000-seed01-prod-0p10mm-thermoonly` 压缩到 0.10 mm，首个累计断键出现在 0.0675 mm；终点累计 53 根断键，最终 bond-local dump 将 53 根断键全部定位到最高母颗粒 1000，且损伤仍在顶层高度 bin。结果见 `tables/pb006_1000_short_compression_summary.csv` 和 `figures/pb006/pb006_500_vs_1000_short_comparison.svg`。
- 完成 PB-006 1000 颗粒 targeted local-dump rerun：前 0.0575 mm 不写局部键文件，之后每 1000 步输出一次 local bond dump 到 0.10 mm。解析得到 6 个母颗粒断裂事件，位移分别为 0.0675、0.0700、0.0775、0.0900、0.0925 和 0.0950 mm，事件断键数为 15、8、20、6、2 和 2；所有 53 根断键均属于最高母颗粒 1000 和最高高度 bin。结果见 `tables/pb006_1000_targeted_window_summary.csv`、`tables/pb006_500_vs_1000_onset_comparison.csv` 和 `figures/pb006/pb006_1000_targeted_window_event_sequence.svg`。
- 完成 PB-006 主线证据边界审计：0.20 mm thermo-only 深压缩和 0.15 mm late targeted-window 深压缩均未产生可解释的后续 local bond 数据，已归档为诊断而非物理结果。0.15 mm 算例实际已进入早期压缩段，但被终止在 local-dump window 前。因此当前 1000 颗粒证据只支持 0.10 mm early-onset scale-up check，不能声称 0.15-0.20 mm 后续传播。状态见 `docs/pb006_mainline_status.md`。
- 新增 1000 颗粒 restartable targeted-window 路线：`simulations/pebble_bed/PB-006/in.pb006_bonded_compression_targeted_window_restartable.lmp` 和 `scripts/run_pb006_bonded_compression_targeted_window_restartable.sh`，加入 flushed thermo 和周期 restart，避免长段压缩中断后完全重算。
- 新增运行监控脚本：`scripts/monitor_pb006_restartable_run.sh`，用于查看 detached screen、LIGGGHTS 进程、最新 thermo 行、restart/local dump 文件。
- 完成主线文献-主张映射和审稿风险审计：新增 `docs/literature_claim_support.md` 和 `docs/manuscript_reviewer_risk_audit.md`，将 HCPB 球床背景、陶瓷球床 DEM、crush probability、Li4SiO4 破碎传播和 bonded-particle 方法文献对应到具体稿件主张。

## 下一步优先级

1. 等待当前 `pb006_1000_0p15_restart` detached screen 算例完成到 0.15 mm；当前已到 0.1125 mm，并已输出 41000-46000 步 late-window local bond dumps。
2. 算例完成后立即运行 `scripts/postprocess_pb006_1000_0p15_restartable.sh`，把 0.15 mm restartable 事件序列纳入 `tables/pb006_breakage_event_database.csv` 和 `figures/pb006/pb006_breakage_event_database.svg`。
3. 若 0.1125-0.15 mm 仍无新断键，论文中将 1000 颗粒结果表述为“首破事件簇后存在稳定平台期”；若出现新断键，则重点分析从单颗粒 1000 号向邻近上层颗粒传播的触发顺序。
4. 在深压缩策略稳定前，论文中把当前 1000 结果明确限定为 early-onset/post-onset window check；主统计证据仍采用三套 500 颗粒随机床。
5. 再做至少 1-2 个 1000 颗粒随机沉积/模板取向种子，判断首破是否总是最高颗粒控制，还是当前 seed 的几何边界效应。
6. 补齐 `docs/manuscript_gap_review.md` 中列出的单颗粒校准缺口，尤其是 1.0 mm/近 1.0 mm Li4SiO4 实验 crush-load 分布、初始刚度和 250/500/1000 子颗粒模板敏感性。
7. 建立分步加载-松弛协议或阻尼敏感性检查，减少力曲线振荡。
8. 扩展 `maxSigmaBond/maxTauBond` 强度扫描并做 bond 刚度扫描，找到同时匹配 crush load、弹性段刚度和主要碎裂形态的参数区间。
9. 若要把 force-path proxy 升级为原生 DEM 力链证据，需要设计 LIGGGHTS restart/rerun 工作流，使 `compute pair/gran/local` 能在第一次 run 前定义，同时不破坏 PB-006 的先成键再平移初始化。
