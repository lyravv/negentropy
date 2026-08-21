---
title: 工作流配置档
role: orchestrator
status: APPROVED
version: 1.0
updated: 2026-08-21
upstream: [team/workflow.md, team/governance.md]
downstream: [projects/*/STATE.md]
artifact_type: team-definition
source_revision: WORKTREE
reviewers: [orchestrator, all-stage-owners]
approver: team-owner
approval_evidence: 用户要求完全按评估建议优化团队，2026-08-21
---

# 工作流配置档（Profiles）

项目必须在 `STATE.md` 选择 profile。`SKIPPED` 不是忽略质量，而是用已登记的权威输入替代某阶段产物。

| Profile | 成熟度 | 使用场景 | 必经阶段 | 可替代阶段 |
|---|---|---|---|---|
| `full` | beta | 新产品/需求模糊 | 0→1→2→3→4→5→6→7 | 无 |
| `existing-spec` | stable | 已有批准规范和架构，例如 GraphX | 0→4→5；发布时 6 | 1–3 可由外部规范替代 |
| `feature` | experimental | 已有产品中开发功能 | 2/3 影响检查→4→5；发布时 6 | 无影响阶段可 SKIPPED |
| `bugfix` | experimental | 行为缺陷 | 缺陷复现→4→5；发布时 6 | 1–3 通常引用既有事实源 |
| `spike` | experimental | 调研/技术验证 | 0→3(结论/ADR)→7 | 不形成产品实现承诺 |
| `ops-only` | experimental | 部署、迁移、事故 | 5(证据)→6→7 | 1–4 引用已发布 revision |

成熟度的机器权威来源是 `team.yaml#workflow.profile_maturity`。`experimental` 表示结构已定义但未被真实项目完整验证，不应被宣传为稳定能力。

## 裁剪门禁

阶段只能在以下条件下标为 `SKIPPED`：

1. `STATE.md` 写明替代事实源及精确 revision；
2. orchestrator 验证其可读且适用于当前 scope；
3. 受影响角色确认没有缺失输入；
4. 不得用 `SKIPPED` 绕过测试、发布授权或安全门禁。

工作进行中可切换 profile，但必须记录原因、影响阶段和批准者。默认 `full`；已有规范项目优先 `existing-spec`。
