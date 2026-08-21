---
title: 测试方案 — GX-INGEST-006
role: test-engineer
status: APPROVED
version: 0.2
updated: 2026-08-21
upstream: [graphx/spec/03-domain-invariants.md, graphx/spec/09-sql-only-acceptance-profile.md, graphx/spec/contracts/builder-input-v1.schema.json, graphx/spec/conformance/requirements.json, 04-implementation/backend-notes.md]
downstream: [backend-engineer, orchestrator]
---

# 测试方案 — GX-INGEST-006

## 交接说明
- **给谁**：backend-engineer / orchestrator
- **一句话**：验证 table-only base、SQL ref 精确绑定、最小 business Markdown allowlist、路径安全和私有产物写入。
- **关键决策**：CLI manifest 按不可信输入测试；覆盖伪造 role、绝对路径、`..`、symlink、secret/cache/golden 和空 SQL/base。
- **需要下游注意**：不得读取/打印 golden、connection_info 或私有正文；Git 外 JSON 仅检查结构、计数、分类、绑定和权限。
- **未决问题**：无；BUG-001～004 均已回归通过。

## 用例与门槛

| 用例 | 验证 | 优先级 |
|---|---|---|
| TC-001 | base 只含 table，拒绝 edge/hyperedge/其他 node type | P0 |
| TC-002 | 每个 table 恰好一个 SQL ref，集合与 manifest SQL 精确相等 | P0 |
| TC-003 | allowlist 仅含 `sql_templates/*.sql` 和 `hyperedges/**/*.md` | P0 |
| TC-004 | 拒绝绝对路径、`..`、symlink、伪造 role、secret/cache/golden | P0 |
| TC-005 | 空 SQL/base 不得生成违反 schema `minItems` 的 plan | P0 |
| TC-006 | 私有 JSON 原子 0600 写入，stdout/Git 文档不含私有 hash | P0 |
| TC-007 | runtime payload/schema/spec/requirements 一致 | P1 |

通过标准：P0/P1 100%，无阻塞/严重缺陷，私有产物无 group/other 权限，目标回归在 30 秒硬超时内通过。否则结论为“不可发布”。

## 安全执行

```bash
timeout --signal=TERM --kill-after=5s 30s .venv/bin/pytest -q \
  tests/test_corpus_manifest.py tests/test_corpus_contract_schema.py \
  tests/test_private_corpus_cli.py tests/test_sql_ingestion.py tests/test_spec_contract.py
```

所有攻击用例使用合成临时数据；测试角色不修改后端实现。
