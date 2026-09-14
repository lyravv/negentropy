---
title: US-AIM-004 四导航与 Applications 占位
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

给架构/实现/测试：四个一级入口保持一致；Applications 仅占位是用户明确范围，tab 布局已随 Q-AIM-001 确认。

## 故事陈述

作为个人用户，我想从全局入口管理 AI 并看见未来应用入口，以便理解当前产品能力及尚未开放的部分。

## 验收标准

- [ ] AC1：Graphs、Resources、AI Manage、Applications 四入口在各页面名称/顺序/选中反馈一致；AI Manage 建议包含模型/用量/日志三 tab，无选中 Graph 时仍可打开使用。
- [ ] AC2：Applications 打开静态“尚未开放”，无创建、发布、运行或其他可执行入口；不新增 Application 后端实体/API，不触发模型或修改 Graph/Resource。
- [ ] AC3：切换导航保留既有 Graphs/Resources 入口行为；空工作区和已有工作区均可打开 AI Manage/Applications，不要求 tenant/组织选择或新权限设置。
- [ ] AC4：Graphs 收起为一级入口时，与 Resources、AI Manage、Applications 的外框宽度、54px 高度、背景、边框、圆角、水平内边距及卡间 9px 间距一致；图标和文字使用同一基线。仅 active 状态允许统一的粉色反馈，Graphs 不得保留列表背景、额外上下空白或不同灰阶。

## 交互/数据要点、边界与异常

占位页面只有说明，无需后端应用数据。导航切换遇到未保存模型表单遵循 US-AIM-001 丢弃提示。

优先级：Must；依赖范围批准和全局入口，时间估算待开发拆分。
