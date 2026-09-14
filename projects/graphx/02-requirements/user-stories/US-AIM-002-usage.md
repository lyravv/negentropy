---
title: US-AIM-002 逐请求用量
role: product-manager
status: APPROVED
version: 0.1
updated: 2026-09-14
upstream: [projects/graphx/02-requirements/ai-manage-requirements.md]
downstream: [architect, frontend-engineer, backend-engineer, test-engineer]
artifact_type: requirements
source_revision: WORKTREE
reviewers: [architect, test-engineer]
approver: product-owner
approval_evidence: 用户在首版范围说明后于2026-09-14明确要求继续开发；架构与独立测试需求评审无阻塞
---

## 交接说明

给架构/实现/测试：请求数不是任务数，unknown 不是 0；Q-AIM-002 未验证，不能宣称 pinned SDK 已支持完整观测。

## 故事陈述

作为个人用户，我想查看模型请求及 token 消耗，以便了解各任务和模型的实际用量与数据缺口。

## 验收标准

- [ ] AC1：一次任务发生两轮 LLM 请求、第二轮真实重试一次，显示 3 个 attempt 和 1 次重试；仅计划但未发出的重试不增计数。重复/乱序通知不翻倍，终态后的有效 usage 可合并。
- [ ] AC2：分别注入完整 usage、明确 0、全缺失、仅输入已知四类结果：0 保留为 0，缺失显示未知；按字段汇总已知小计并显示缺口，不把未知输出补零，不重复相加 provider 已包含的明细。未知请求数按输入/输出任一字段缺失计每个 attempt 一次，并分别显示输入、输出已知覆盖请求数（显式 0 属已知）。
- [ ] AC3：已发出后失败/超时/取消且缺 usage 仍计 attempt 并标未知；老任务无采集或请求边界不完整时显示未采集/覆盖不完整，不能伪造请求数或完整总量。
- [ ] AC4：时间/Graph/模型/状态筛选同时作用于汇总和分页明细；显示实际任务/角色/模型快照及结果；默认近 7 日并明确时区与区间。普通任务与连接测试可分开查看，业务汇总默认不混入测试。
- [ ] AC5：确定性 pinned runtime 探针覆盖成功、多轮、工具循环、失败、重试、取消与重复；缺公开请求边界时阻止完整逐请求统计验收，不能用本地 upstream 推测代替证据。

## 交互/数据要点、边界与异常

展示已观测请求数、真实重试数、输入/输出已知小计和未知请求数；空记录、历史未采集、加载失败可区分。连接测试无 Graph 归属仍可查；分页顺序稳定。用量关联来自服务端任务身份。

优先级：Must；依赖配置快照与 Q-AIM-002，时间估算待开发拆分。
