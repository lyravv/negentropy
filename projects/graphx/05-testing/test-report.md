---
title: 测试报告 — GX-INGEST-006
role: test-engineer
status: APPROVED
version: 0.2
updated: 2026-08-21
upstream: [05-testing/test-plan.md, 05-testing/defect-log.md]
downstream: [backend-engineer, orchestrator, devops-engineer]
---

# 测试报告 — GX-INGEST-006

## 交接说明
- **给谁**：backend-engineer / orchestrator / devops-engineer
- **一句话**：**可发布** —— BUG-001～004 均已回归，目标组 30/30 通过且无新严重缺陷。
- **关键决策**：不可信 manifest 路径/role、空集合、CLI symlink 与私有输出安全均纳入自动化回归。
- **需要下游注意**：OQ-016 仍阻塞真实 Harness 私有语料运行。
- **未决问题**：无；OQ-016 是后续真实 Harness 运行门禁，不影响本次输入计划工具发布。

## 1. 结论

> **可发布**

BUG-001～004 均已修复并回归通过。目标测试 30/30 通过，未发现新的阻塞或严重缺陷；GX-INGEST-006 输入计划工具可发布。该结论不授权启动真实私有 Harness 会话，OQ-016 仍须先关闭。

## 2. 执行结果

| 项目 | 结果 |
|---|---|
| 目标测试 | 30 passed，2.54 秒，退出码 0 |
| 私有输出原子 0600 测试 | 通过 |
| 外部三份 JSON 权限 | 3/3 为 0600 |
| backend-notes 私有 hash 模式 | 0 |
| CLI stdout hash | 目标测试确认无 `sha256:` |
| 外部 JSON 结构 | 3/3 runtime model 校验通过；未输出 hash/正文 |
| table Bundle | 13 table nodes、0 edge、0 hyperedge、224 fields |
| manifest | 45 accepted、8 exclusions，分类计数符合预期 |
| Builder plan | 13 table sources、23 business evidence，manifest/base 绑定通过 |
| 对抗验证 | absolute/`..`/反斜杠/重复分隔符/secret/golden/cache/pyc/role-suffix 错配/嵌套 SQL 均拒绝；空 SQL/base 拒绝；CLI 输入 symlink 拒绝 |

此前分组证据为 73 passed + 12 subtests；本轮按编排者要求只做 GX-INGEST-006 最终定向回归，未运行长时全量。

## 3. 规范一致性与下一轮

- 正常路径满足 table-only、SQL ref 集合绑定、schema 正向验证与 content-free 输出。
- GX-INGEST-006 的 exact allowlist 已在不可信 manifest 边界执行，runtime 最小基数与 schema 一致。
- 后续常规发布回归仍应处理既有 TestClient 环境超时并完成全量分组；该项不是本次定向回归新缺陷。
- OQ-016 未关闭前不得启动真实 Builder/Reviewer/Tester 私有语料会话。
