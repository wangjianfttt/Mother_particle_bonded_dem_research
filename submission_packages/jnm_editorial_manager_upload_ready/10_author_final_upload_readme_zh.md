# Journal of Nuclear Materials 最终投稿上传说明

这份说明给对应作者在 Elsevier Editorial Manager 中逐项上传和复制粘贴使用。当前本地文件已经通过自动 gate；真正投稿前仍需先完成公开数据仓库 DOI 或稳定 URL。

## 1. 先做公开复现包沉积

优先使用已经冻结的上传目录，不要临时重新打包：

`submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/`

上传这个文件到 Zenodo、Figshare 或机构数据仓库：

`submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip`

冻结版 SHA256：

`b9a8bd2e16ea84ed874e31bac701fb0a45b22fe9435b3a2c898306c518a28a30`

上传前可运行：

```bash
submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/VERIFY_BEFORE_UPLOAD.sh
```

当前公开复现包已经校验为 125 个文件。staging 目录仍保留为生成/审计目录，但正式上传以 frozen 目录为准。

同时保留校验文件：

`submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip.sha256`

仓库元数据可从以下文件复制：

`submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_repository_metadata_zenodo.json`

最终逐项上传清单在这里，按它区分公开数据仓库文件、Editorial Manager 文件和本地支持包：

- `docs/jnm_final_upload_manifest.md`
- `docs/jnm_final_upload_manifest.csv`

拿到 DOI 或稳定 URL 后，在项目根目录执行：

```bash
python3 scripts/insert_jnm_repository_identifier.py https://doi.org/10.5281/zenodo.20687351 --dry-run
python3 scripts/insert_jnm_repository_identifier.py https://doi.org/10.5281/zenodo.20687351 --apply --rebuild
```

如果插入后 gate 显示 `PASS`，再进入 Editorial Manager 正式投稿。

## 2. Editorial Manager 主要上传文件

| 系统字段或文件类型 | 使用文件 | 备注 |
| --- | --- | --- |
| Manuscript | `manuscript/journal_of_nuclear_materials_submission.pdf` | DOI 插入后重新生成的 PDF |
| Source files | `submission_packages/journal_of_nuclear_materials_flat_source.zip` | 如果系统要求 LaTeX 源文件，上传这个扁平源文件包 |
| Highlights | `manuscript/journal_of_nuclear_materials_highlights.md` | 复制 5 条 highlights |
| Cover letter | `manuscript/journal_of_nuclear_materials_cover_letter_draft.md` | 对应作者最终检查后上传或粘贴 |
| Graphical abstract | `figures/main/journal_of_nuclear_materials_graphical_abstract.png` 或 `.tiff` | 系统允许时单独上传 |
| Supplementary material | `manuscript/journal_of_nuclear_materials_supplementary.pdf` | 作为 supporting information 上传 |
| Declarations | `manuscript/journal_of_nuclear_materials_elsevier_declarations.md` | 按系统字段分别复制 |
| Data/code availability | DOI 插入后的 manuscript 和 paste fields | 使用真实 DOI：`https://doi.org/10.5281/zenodo.20687351`；不要保留 DOI 占位符 |

投稿用总包在这里：

`submission_packages/journal_of_nuclear_materials_submission_package.zip`

这个总包是本地备份和协作者审阅包，不要作为公开数据仓库记录上传。上传时以系统要求的单项文件和 `docs/jnm_final_upload_manifest.md` 为准。

## 3. 复制粘贴字段

优先从下面这个文件复制标题、摘要、关键词、Highlights、Data availability、Code availability、Funding、CRediT 和 AI 声明：

`manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md`

作者顺序和单位从下面两个文件核对：

- `manuscript/journal_of_nuclear_materials_author_metadata.csv`
- `manuscript/journal_of_nuclear_materials_author_declaration_checklist.md`

对应作者：

Jian Wang, `wjfttt@mail.ustc.edu.cn`

## 4. 投稿前最后确认

必须满足以下条件后再点击 Submit：

- `python3 scripts/check_jnm_submission_gate.py` 输出 `overall_status=PASS`。
- `python3 scripts/check_jnm_final_upload_manifest.py` 输出 `PASS final upload manifest`。
- Data availability 中已经是真实 DOI 或稳定 URL。
- PDF 首页作者、单位、摘要、关键词无错。
- 8 位作者均确认作者顺序、单位、基金、CRediT、利益冲突和 AI 声明。
- 不上传内部 reviewer-risk prebuttal，除非编辑部明确要求。
- 不把本地大体积 restart、完整 local-bond dump 当成常规补充文件上传；公开包中已经包含可审查的 processed data、代表性输入、图表源数据和脚本。

## 5. 当前证据边界

投稿时保持论文现有保守表述：

- 单球弱面模板是当前校准候选，不是最终 Li4SiO4 本构律。
- 100 个母球的床层结果是断裂事件序列和敏感性证据，不是收敛的失效概率统计。
- 文章主张的是可审计的断裂事件诊断流程，以及局部键断裂、宏观载荷响应和原生力网络重组之间的机制联系。
- 不声称已经完成寿命预测、循环载荷退化、热流固耦合或 ITER/CFETR 设计裕度定量评估。
