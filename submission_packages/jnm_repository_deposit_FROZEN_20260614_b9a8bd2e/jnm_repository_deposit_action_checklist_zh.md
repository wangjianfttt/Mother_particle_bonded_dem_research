# JNM 可复现包仓库上传中文操作单

这份清单用于完成 Journal of Nuclear Materials 投稿前的最后一个外部步骤：把公开可复现包上传到 Zenodo、Figshare 或机构数据仓库，获得 DOI 或稳定 URL，然后回填到论文和投稿材料中。

## 1. 当前状态

- 本地论文、图件、补充材料、投稿包和可复现包已经通过自动检查。
- 当前 gate 状态应为 `BLOCKED_EXTERNAL`，不是因为本地文件失败，而是因为还没有仓库 DOI 或稳定 URL。
- 当前 JNM 投稿工作区内没有正在运行的 DEM/LIGGGHTS 计算；其他项目目录中的外部算例不作为本稿件的投稿 gate 阻塞项。

## 2. 上传哪个文件

优先上传这个公开可复现包：

- `submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip`

建议同时保存或上传校验文件：

- `submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip.sha256`

不要把下面这个内部投稿支持包作为公开数据仓库记录上传：

- `submission_packages/journal_of_nuclear_materials_submission_package.zip`

原因是内部投稿支持包包含 cover letter、declarations、reviewer-risk prebuttal 等投稿管理材料；公开仓库只需要可复现数据、脚本、图件、代表性输入和审计文件。

## 3. 仓库元数据

可直接使用：

- `submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_repository_metadata_zenodo.json`
- `submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_repository_metadata_readme.md`

建议填写：

- 类型：dataset
- 版本：`1.0`
- 访问权限：open
- 许可证：`CC BY 4.0`，除非通讯作者或单位要求其他兼容许可证
- 标题：`Reduced reproducibility package for acceptance-gated bonded-template DEM of Li4SiO4 breeder-bed fracture sequences`
- 关键词：Li4SiO4; ceramic breeder; fusion blanket; pebble bed; bonded-particle DEM; fracture-event sequence; native force network; Journal of Nuclear Materials

发布前请人工确认作者姓名、单位、ORCID、基金和仓库 community。

## 4. 上传前本地检查

在项目根目录运行：

```bash
python3 scripts/check_jnm_public_repro_package.py
python3 scripts/check_jnm_repository_deposit_staging.py
python3 scripts/check_jnm_submission_gate.py
```

同时在 frozen 上传目录内核对公开可复现包的 SHA256：

```bash
cd submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e
shasum -a 256 -c journal_of_nuclear_materials_reproducibility_package.zip.sha256
cd -
```

预期结果：

- public reproducibility package: `PASS`
- repository-deposit staging: `PASS`
- final submission gate: `BLOCKED_EXTERNAL`，且只有 repository DOI/stable URL 这一项阻塞

## 5. DOI 或稳定 URL 生成后

先预览要改哪些文件：

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run
```

确认无误后执行：

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild
```

这个脚本会自动更新数据可用性声明、TeX、cover letter、declarations、证据矩阵、上传矩阵、仓库 README、最终行动摘要和主线状态文件，并重新生成 PDF、flat source、投稿包、公开可复现包、中文 deposit handoff、仓库暂存目录和最终 gate 报告。仓库暂存目录会在 handoff 更新后再次刷新，确保公开包 SHA256 和 handoff 文字一致。

不要手动改 `manuscript/journal_of_nuclear_materials_submission.tex`，因为它是由 Markdown 草稿自动生成的。

## 6. DOI 回填后的预期结果

运行：

```bash
python3 scripts/check_jnm_submission_gate.py
```

预期最终状态：

- `overall_status=PASS`
- `0 FAIL`
- `0 BLOCKED_EXTERNAL`

如果仍然是 `BLOCKED_EXTERNAL`，打开：

- `docs/jnm_final_submission_gate_report.md`

按报告里列出的剩余文件继续用 DOI 插入脚本处理，不要手工只改单个文件。

## 7. 论文上传前最后确认

- 作者顺序、单位、通讯作者邮箱和 CRediT 贡献是否确认。
- 基金、利益冲突、AI 使用声明是否确认。
- Data availability 中 DOI 或稳定 URL 是否真实可打开。
- 论文仍保持保守表述：单颗粒模板是 calibration candidate；100 母球床结果是 event-sequence evidence；不声称收敛破碎概率；不声称最终 Li4SiO4 材料本构；不声称已完成热-流-力耦合预测。
