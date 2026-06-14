# JNM 数据仓库上传最终交接单

本文件用于作者实际上传 Zenodo、Figshare 或机构数据仓库时核对。它由 `scripts/build_jnm_repository_deposit_handoff.py` 从当前 staging manifest 和最终 gate 报告自动生成；正式上传路径使用已冻结的 repository-deposit 目录。

## 只上传这个公开复现包

- 上传文件：`submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip`
- 文件大小：9.32 MiB
- SHA256：`0fdb62931aad30d170345800eb00888a4a12a4ecf1ee70713a372ec13e38bbd5`

建议同时上传或在仓库描述中记录校验文件：

- 校验文件：`submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip.sha256`
- 校验文件 SHA256：`9ac83f3ab778b286be8066e1637d204ce1ba3e1bb9a48b9a4118a27be0992c89`

上传前建议在 frozen 目录内执行一次校验，并保留 staging 检查作为生成一致性审计：

```bash
cd submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e
shasum -a 256 -c journal_of_nuclear_materials_reproducibility_package.zip.sha256
cd -
python3 scripts/check_jnm_repository_deposit_staging.py
```

不要把 `journal_of_nuclear_materials_submission_package.zip` 当作公开数据仓库记录上传；它是本地 Editorial Manager 投稿支持包，包含内部投稿辅助材料。

## 当前本地 gate 状态

- overall_status：`FAIL`
- PASS/WARN/BLOCKED_EXTERNAL/FAIL：`83/0/0/2`
- 当前外部 blocker：无

这个状态是正常的：在真实 DOI 或稳定 URL 插入前，本地 gate 应保持 `BLOCKED_EXTERNAL`，且不应有 `FAIL`。

## 推荐上传顺序

1. 打开 Zenodo、Figshare 或机构数据仓库。
2. 新建公开记录，上传上面的公开复现包 zip。
3. 复制 `journal_of_nuclear_materials_repository_metadata_zenodo.json` 中的标题、摘要、关键词、作者和许可证信息。
4. 记录或上传 `.sha256` 校验文件。
5. 仓库生成 DOI 或稳定 URL 后，回到项目根目录执行下面两条命令。

```bash
python3 scripts/insert_jnm_repository_identifier.py <真实DOI或URL> --dry-run
python3 scripts/insert_jnm_repository_identifier.py <真实DOI或URL> --apply --rebuild
```

## DOI 插入后的预期结果

DOI 或稳定 URL 插入并重建后，预期最终 gate 为：

```text
overall_status=PASS
83 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL
```

该闭环已经在轻量隔离副本中用测试 DOI URL 完整演练通过；主工作区没有写入测试 DOI。
