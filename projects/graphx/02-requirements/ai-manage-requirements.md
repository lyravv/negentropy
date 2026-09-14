---
title: AI Manage 首版需求
role: product-manager
status: APPROVED
version: 0.4
updated: 2026-09-14
upstream: [用户2026-09-14明确范围指令 + 多模型配置决策, projects/graphx/03-architecture/ai-manage-design.md, projects/graphx/03-architecture/ai-multimodel-config-draft.md]
downstream: [architect, test-engineer, frontend-engineer, backend-engineer]
artifact_type: requirements
source_revision: WORKTREE
reviewers: [architect, test-engineer]
approver: product-owner
approval_evidence: 用户在2026-09-14先批准多配置库，随后明确作出覆盖性最终决定：「没有默认；每条消息发送时选哪个模型就用哪个」
---

## 交接说明

给 architect、test-engineer：交付个人级多配置库、逐请求用量、任务日志和 Applications 占位。模型配置没有默认条目；每条根用户消息必须显式携带用户本次选择的 `config_id`，派生任务树继承该条目当时的不可变版本。角色覆盖、成本/预算/自动发现等仍后置。重点评审逐消息选择、整树快照、实际请求观测、凭据保护和删除语义；未决 Q-AIM-002 见本文末。

## 1. 需求概述

用户已明确先设计 → 需求 → 开发 → 验收，优先 AI Manage（模型配置、流量统计、日志），Applications 仅占位；这是个人产品，不新增多租户平台。本轮将“流量”建议定义为实际模型请求与 token 用量，不包含网络字节或费用。以下细节已按本轮用户继续指令确认，批准来源见文档头。
代码参考基线为 `graphx@bd15e9886a6180519f2912881ce28c297d4aead9`；无新增业务简报/术语表获批，用户明确范围作为本草案事实输入，其余不能视作已有规范替代。本草案不宣称任何新功能已实现或验证。

## 2. 需求清单

| 编号 | 需求 | MoSCoW | 故事 |
|---|---|---|---|
| R-AIM-001 | 个人多配置条目库：名称、兼容路由、Base URL、模型 ID、凭据；每条独立保存、测试和版本化，不设默认条目 | Must | US-AIM-001/005 |
| R-AIM-002 | 每条根用户消息必须显式选择一个配置条目；接受消息时冻结 `config_id` 与版本，整条任务树、子任务与重试继承根快照 | Must | US-AIM-001/005 |
| R-AIM-003 | 按真实请求 attempt 采集用量，重试独立、重复通知幂等、未知不记零 | Must | US-AIM-002 |
| R-AIM-004 | 用量时间/Graph/模型/状态筛选、同条件汇总与分页明细；连接测试单独分类 | Must | US-AIM-002 |
| R-AIM-005 | 跨 Graph 日志筛选查阅、复用现有 Trace 展示公共助手文本与工具原文 | Must | US-AIM-003 |
| R-AIM-006 | Graphs、Resources、AI Manage、Applications 四导航；最后一项仅静态占位 | Must | US-AIM-004 |
| R-AIM-007 | 多配置库可新增、编辑、测试和删除；GraphX 输入框旁提供逐消息模型选择。选择只作用于本次根消息，不修改任何全局状态；页面加载、配置新增、列表刷新或上一条消息的选择均不得隐式替用户选择 | Must | US-AIM-005 |
| R-AIM-008 | 日志删除、自动清理、导出、Applications 后端实体及运行/发布 | Won't this iteration | 后置 |
| R-AIM-009 | 角色覆盖、价格/计费/预算、自动模型发现、扩展运行参数编辑，以及“默认模型/最近选择自动沿用” | Won't this iteration | 后置 |
| R-AIM-010 | AI Manage 的模型页只维护配置条目，不展示或暗示“当前在用/已激活/默认”；Graph 聊天的逐消息模型选择属于 composer，而不是配置页状态 | Must | US-AIM-001/005 |
| R-AIM-011 | 四个一级导航卡在 Graphs 收起时使用同一宽度、背景、边框、圆角、内边距、图标/文字对齐和卡间距；不得因 Graphs 可展开而出现另一套收起外观 | Must | US-AIM-004 |
| R-AIM-012 | 逐消息模型选择位于增高后的 composer 内部底部工具栏右侧，以紧凑模型名和下拉入口呈现；不得作为输入框上方的独立胶囊或悬浮卡 | Must | US-AIM-005 |

## 3. 用户故事索引

| 故事 | 文件 | 优先级 | 状态 |
|---|---|---|---|
| US-AIM-001 | [配置与快照](user-stories/US-AIM-001-model-config.md) | Must | APPROVED |
| US-AIM-002 | [用量统计](user-stories/US-AIM-002-usage.md) | Must | APPROVED |
| US-AIM-003 | [日志查阅](user-stories/US-AIM-003-logs.md) | Must | APPROVED |
| US-AIM-004 | [导航与占位](user-stories/US-AIM-004-navigation.md) | Must | APPROVED |
| US-AIM-005 | [多模型配置库](user-stories/US-AIM-005-multimodel-config.md) | Must | APPROVED |

## 4. 非功能需求

凭据仅在服务端受保护使用，读回/保存响应、异常、Trace、提示词和浏览器持久存储均不得泄漏原值或秘密定位信息。缺失历史模型/usage 标明未记录；不得套用当前配置。列表分页、稳定排序；刷新失败保留已加载内容。保留现有无显式输出 token 上限行为，不静默引入新 cap；真实参数生效须有实际 SDK 与 Cordis 执行路径证据。

## 5. 范围外（明确不做）

多配置的「角色覆盖、价格/成本、预算、自动模型发现、扩展运行参数编辑」及日志删除/自动清理/导出、Applications 后端实体仍后置（R-AIM-008/009 部分）；不新增 tenant、组织、RBAC，不迁移已有内部 tenant 字段，不恢复旧摘要报告 UI。首版日志管理明确只覆盖筛选查阅；删除和自动清理尚未批准，不宣称完整日志生命周期已满足。公共原文不包含隐藏思维链或 secret，沿用受控脱敏/截断并明确标记。

## 6. 依赖、风险与集中待确认

- Q-AIM-001（RESOLVED，product-owner=user）：用户最终选择多配置库、无默认、逐根消息显式选择；同时推进手动小请求连接测试、整树快照、逐请求/token 统计、只读日志、四导航与 Applications 占位；采用三个 tab 与近 7 日默认查询范围。正式技术契约 v0.3 已由 architect 批准。
- 相对设计 v0.1 第 4 节，本需求确定后续委派也继承根快照，避免协调中途切模型；同一会话中下一条用户消息创建的新根任务采用当时新配置。连接测试由设计候选确认为 Must，执行前明确可能消耗 tokens，测试本身不激活配置。
- **多配置最终决策（2026-09-14）**：用户先确认把「多配置条目库」和删除能力提前到本轮，随后明确用「没有默认；每条消息发送时选哪个模型就用哪个」覆盖此前“新条目设默认”的选择。正式契约 v0.3 仅保留 `/configs` collection 作为写入契约；`GET /config` 只能作为非权威兼容读取，不能被 UI、任务创建或后台逻辑解释为默认配置。
- **交互收口（2026-09-14）**：模型配置页只回答“有哪些配置以及如何维护”，不回答“现在使用哪个”。因此列表、详情标题、说明、状态和操作反馈均不得生成“当前在用/激活/默认”语义。逐消息选择只在 Graph composer 出现，并采用输入框内部底部工具栏布局。Graphs 收起态与其他一级导航卡使用同一视觉 primitive。
- Q-AIM-002（OPEN，等待 architect/backend/test）：pinned DSH `0.1.0rc6` 的公开边界需确定性探针覆盖真实 attempt、失败、重试、取消、usage 和重复通知；上游源码不能替代锁定运行时证据。若无法完整观测，评审支持的接入方案，禁止把“已知小计”包装成完整统计。该门禁与配置条目多少无关，多配置不改变用量完整性结论。
- 本工作项无 `open-questions.md` 写权限，Q 项暂集中于本文，交编排者路由登记；需求已批准；正式技术契约及 Q-AIM-002 仍待收口。
