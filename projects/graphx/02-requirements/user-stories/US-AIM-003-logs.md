---
title: US-AIM-003 全局日志查阅
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

给架构/实现/测试：首版只读日志索引复用 Trace；删除/清理仍后置待确认，范围见 Q-AIM-001。

## 故事陈述

作为个人用户，我想跨 Graph 找到任务并查看真实执行记录，以便定位模型输出和工具调用问题。

## 验收标准

- [ ] AC1：可按时间/Graph/状态筛选并分页，列表显示时间、Graph、角色、任务状态及历史模型快照；旧任务无模型显示“未记录”，不得显示当前默认模型。
- [ ] AC2：打开任务复用现有 Trace，能查到已保存的公共助手文本与工具参数/结果原文；不以摘要报告替代，不展示隐藏思维或 secret；已脱敏/截断/历史缺原文均明确标记。
- [ ] AC3：运行中刷新可见新事件，同秒事件次序稳定且重复通知不重复成行；返回列表保留筛选和位置，加载错误保留已有记录并可重试，任务不可用给出明确反馈。

## 交互/数据要点、边界与异常

索引与 Graph 内入口打开同一任务的同一 Trace；无记录有空态。没有删除、自动清理、导出入口，也不恢复旧摘要报告页。

优先级：Must；依赖快照及现有 Trace 契约，时间估算待开发拆分。
