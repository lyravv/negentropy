---
title: US-AIM-001 模型配置与任务快照
role: product-manager
status: APPROVED
version: 0.2
updated: 2026-09-14
upstream: [projects/graphx/02-requirements/ai-manage-requirements.md]
downstream: [architect, frontend-engineer, backend-engineer, test-engineer]
artifact_type: requirements
source_revision: WORKTREE
reviewers: [architect, test-engineer]
approver: product-owner
approval_evidence: 用户2026-09-14最终明确多配置无默认、逐消息选择；本版按该决定覆盖旧单配置语义
---

## 交接说明

给架构/实现/测试：配置须实际生效且整树稳定；Q-AIM-001 已解决，整树继承替换参考设计的委派新配置建议。

## 故事陈述

作为个人用户，我想管理多个模型配置、独立测试连接，并为每条根消息明确选择模型，以便本次任务树使用所选模型且在途协作不漂移。

## 验收标准

- [ ] AC1：保存合法名称/路由/Base URL/模型 ID/凭据后重启仍可从配置库读到该条目的非秘密最新版本；不得提示连接已成功；不支持的路由拒绝保存。配置库为空时不注入部署默认。
- [ ] AC2：根消息显式选择配置 A 后，其任务、子/孙任务和重试均使用 A 的发送时版本；之后编辑 A、创建 B、删除 A 或为下一条消息选择 B，均不改变该在途树。包括排队重启恢复；覆盖 GraphX、Resource Manager、Builder、Reviewer、Tester 与保留入口。
- [ ] AC3：通过实际 SDK 与 Cordis 对受控目标的请求验证 endpoint/model/认证及原有运行参数生效；仅断言 worker 配置 echo 不算通过。历史缺快照不得编造旧模型，旧排队任务补快照的来源须明确。
- [ ] AC4：模型配置页只展示配置条目的名称、路由、模型 ID、Base URL、认证状态、版本及维护操作；系统不得增加“当前在用”“已激活”“默认”等徽标、后缀、说明或成功反馈，也不得在该页提供切换当前模型的动作。
- [ ] AC4：点击测试前可见“小请求可能消耗 tokens”；以表单当前值测试且不保存/激活，成功只代表该次连接测试；失败给出脱敏原因。测试请求独立分类，编辑字段后旧成功状态不代表新值已验证。路由和 Base URL 均未变时，测试与保存的空凭据语义一致：使用已存凭据版本，无已存版本则无凭据。
- [ ] AC5：路由或 Base URL 改变时，保存和测试均须重新输入凭据或明确选择无凭据（路由支持时），不得隐式沿用并外发旧凭据；未改变时空输入保留旧值。保存失败不激活半份配置、保留非秘密输入；并发版本冲突提示重载。读回/保存响应、异常、公共 Trace/提示词均不泄漏 secret 或秘密定位信息；前端不持久化凭据。

## 交互/数据要点、边界与异常

配置条目编辑、保存与测试独立；未保存离开提示丢弃，保存/测试中防重复。无凭据路由可表达，需凭据但缺失时明确报错；在途任务仍可访问旧凭据版本。AI Manage 的编辑选中仅表示“正在编辑这一条”，不得写入 composer 或解释为运行状态；composer 每条根消息必须重新明确选择。首版不提供删除凭据或高级参数编辑。

优先级：Must；依赖批准范围和执行路径契约，时间估算待开发拆分。
