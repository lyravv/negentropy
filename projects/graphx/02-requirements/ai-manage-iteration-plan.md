---
title: AI Manage 首版迭代计划
role: product-manager
status: APPROVED
version: 0.2
updated: 2026-09-14
upstream: [projects/graphx/02-requirements/ai-manage-requirements.md]
downstream: [architect, orchestrator, test-engineer]
artifact_type: requirements
source_revision: WORKTREE
reviewers: [architect, test-engineer]
approver: product-owner
approval_evidence: 用户在首版范围说明后于2026-09-14明确要求继续开发；架构与独立测试需求评审无阻塞
---

## 交接说明

给 architect/orchestrator：按设计 → 需求 → 开发 → 验收交付五个 Must 故事；需求与无默认多配置契约已批准。当前进入实现差异修复和独立验收；Q-AIM-002 仍单独阻塞真实 usage 采集。

## 1. 迭代目标

个人用户可配置真实生效的模型，查看不虚报的逐请求用量，并从全局日志回到原有 Trace；Applications 可见但不可执行。开发前将参考设计与批准需求的差异同步为正式契约。

## 2. 里程碑

| 里程碑 | 出口门禁 | 计划时点 | 当前状态 |
|---|---|---|---|
| M1 前置设计 | 交互/可行性设计与最终产品决定一致 | 已产出 v0.3 | DONE |
| M2 需求与契约 | 无默认多配置、逐消息选择、快照和消费者接口冻结 | 已产出 v0.3 | DONE |
| M3 开发与自检 | US-AIM-001..005；实现与 v0.3 契约一致；usage 保持诚实不可用 | M2 后 | IN_PROGRESS |
| M4 独立验收 | P0 全通过、P1 导航通过；测试报告绑定最终 revision，无伪造运行证据 | M3 后 | NOT_STARTED |

## 3. 排期（按用户故事）

| 故事 | 优先级 | 阶段/顺序 | 依赖 |
|---|---|---|---|
| US-AIM-001 | Must | 开发 1 | M2；真实配置路径核验 |
| US-AIM-002 | Must | 开发 2 | 快照；Q-AIM-002 观测证据 |
| US-AIM-003 | Must | 开发 3 | 快照；现有 Trace 契约 |
| US-AIM-004 | Must | 开发 3 | M2；全局页面入口 |
| US-AIM-005 | Must | 开发 1 | M2；无默认逐消息选择契约 |

## 4. 风险与缓冲

pinned runtime 探针与集成验收单独留出验证阶段，不承诺日期。观测边界不满足时重新评审，不静默降级 Must；可推进无依赖切片，但本迭代不可宣告全部完成。原有脏工作树按认领保护，部署和真实模型付费请求按实际授权范围执行。

## 5. 迭代出口标准

Must 故事 AC 全部可追溯到最终规范/契约/实现与测试 revision；P0 覆盖实际 SDK+Cordis 参数生效、整树快照不漂移、缺 usage/显式 0/部分 usage、真实 retry 与重复通知、secret 全出口保护、旧 Trace 不套当前模型；P1 验证四导航一致及占位无执行入口。相关确定性测试、前端构建、`git diff --check` 通过；未运行的真实模型 smoke 单独记录，不能称已验证。验收完成不等于提交、推送或部署。
