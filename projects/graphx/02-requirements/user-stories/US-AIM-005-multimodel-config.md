---
title: US-AIM-005 多模型配置库
role: product-manager
status: APPROVED
version: 0.2
updated: 2026-09-14
upstream: [projects/graphx/02-requirements/ai-manage-requirements.md R-AIM-007/009, projects/graphx/03-architecture/ai-multimodel-config-draft.md]
downstream: [architect, frontend-engineer, backend-engineer, test-engineer]
artifact_type: requirements
source_revision: WORKTREE
reviewers: [architect, test-engineer]
approver: product-owner
approval_evidence: 用户 2026-09-14 明确最终语义：「没有默认；每条消息发送时选哪个模型就用哪个」，覆盖此前设默认方案
---

## 交接说明

给架构/实现/测试：以无默认的多配置条目库替代单默认配置。每条根消息显式选择，选择结果冻结到该任务树；不得用第一条、最近一次或部署配置代替用户选择。多配置与 usage 独立性无关——Q-002 门禁仍约束逐请求采集。

## 故事陈述

作为个人用户，我想同时保有多个模型配置条目，并在发送每条消息时明确选择这次使用的模型，以便不同任务自由切换且系统不会暗中替我决定模型。

## 验收标准

- [ ] AC1：可新增多个配置条目；每条含 provider、Base URL、模型 ID、凭据（可选），保存成功返回该条目的非秘密视图与自身版本号。
- [ ] AC2：每条配置有独立版本历史与乐观锁；并发覆盖冲突返回 `AI_CONFIG_CONFLICT`，同现有单条语义。
- [ ] AC3：GraphX composer 为每条消息提供明确选择；未选择时拒绝发送并返回/显示 `AI_CONFIG_REQUIRED`。加载配置列表不得自动选中第一条，新增配置不得自动选中为发送模型，上一条消息的选择也不得静默沿用到下一条根消息。
- [ ] AC4：发送时把本次所选 `config_id` 交给服务端；根任务冻结「条目+版本+运行参数」，子/孙/重试继承。之后的选择、编辑或删除不影响在途任务树。
- [ ] AC5：删除条目不受“默认保护”约束；历史配置版本和已冻结任务快照仍须足以恢复在途任务，删除不能令活动/排队任务漂移或失去凭据。
- [ ] AC6：凭据沿用服务端受限文件与目标隔离规则；每条配置有独立凭据版本引用，不得互相串用；读回/异常/公共事件不泄漏 secret。
- [ ] AC7：`usage / logs / Trace` 的 `model_snapshot` 升级为携带配置条目标识（`config_id` + 版本），历史缺失任务 `null` 不伪造；usage 采集完整性仍受 Q-002 门禁约束。
- [ ] AC8：Graph composer 的模型入口位于 composer 边框内部的底部工具栏靠右区域，与附件/工作模式等工具同层；收起态仅显示所选配置名称（空间不足时省略）和下拉箭头，不展示独立的“模型”前缀胶囊或悬浮在输入框上方。菜单向上展开，逐条显示配置名称及 provider/model 辅助信息，并保留“管理模型配置”入口。
- [ ] AC9：composer 默认可容纳约三行输入，整体最小高度 96px，文本区在工具栏上方独立占位且可继续自动增高，最大高度后内部滚动；发送按钮位于内部底部工具栏最右侧。未选择模型时入口显示“选择模型”，发送仍按 AC3 阻止并给出明确提示。

## 边界与异常

多配置只增加条目库和逐消息选择；不增加默认指针。角色覆盖、价格/成本、预算、自动模型发现、扩展运行参数编辑仍不纳入本轮。AI Manage 页面为便于编辑而选中列表首项不等于 composer 选择；两种状态必须分离。前端不持久化凭据，离开未保存表单提示丢弃。
