---
title: 未决问题与变更请求
role: orchestrator(维护) / 全员(提出)
status: DRAFT
version: 0.5
updated: 2026-08-31
upstream: []
downstream: [全员]
---

# 未决问题与变更请求（Open Questions & Change Requests）

> 项目工作区根目录的**全局**问题/变更登记簿。
> - 问题编号 `Q-xxx`，变更请求编号 `C-xxx`。
> - 任何角色可提出；“等待谁”负责回答，提出者或 test-engineer 验证落地后关闭。
> - 阻塞性问题会让相关文档进入 `BLOCKED`。

## 未决问题（Questions）
| 编号 | 提出角色 | 问题 | 等待谁 | 状态 | 决定来源 | 验证者 | 解决记录 |
|------|---------|------|--------|------|---------|-------|---------|
| Q-001 | test-engineer | GX-APP-012 删除端点 `confirmed` 缺失时的状态码：契约（spec/11 + 任务后端契约）写"confirmed 非 true → 409 DELETE_CONFIRMATION_REQUIRED"，但实现把 `confirmed` 设为必填 query 参数，缺失时 FastAPI 返回 **422**（仅 `confirmed=false` 才 409）。核心行为（未确认即拒绝、Graph 保留）一致，仅缺失分支的状态码/错误码不同。请裁定缺失分支应为 409 还是 422，以对齐契约/实现/测试。非阻塞。 | architect | RESOLVED | orchestrator（legacy，治理矩阵建立前） | test-engineer（实现与测试已落地） | 2026-08-20：缺失或非 true 一律 409 `DELETE_CONFIRMATION_REQUIRED`。`api.py`、合规测试和 backend-notes 已同步。 |
| Q-002 | backend-engineer | OQ-016 阻塞私有 corpus 的真实 Builder 执行：当前 DeepSeek Harness worker 与 bundled Bash 同 UID，provider Token 仍映射进 worker 环境，无法证明 Agent 不可读 Token。已完成 GX-INGEST-006 的 hash-bound 最小权限 Builder input plan，并在 Git 外对当前 corpus 生成 13 个 table source + 23 个 business-document evidence 的计划；该计划不构成真实会话授权。需要实现并验证 out-of-sandbox credential broker（或等价 UID/mount 隔离），且证明真实 Token 对 Agent/Bash 不可读后，才能装载私有语料。 | devops-engineer | OPEN | | | 阻塞真实 Builder/Reviewer 会话；不阻塞确定性输入准备。不得以路径权限或 0600 文件冒充安全边界。 |
| Q-003 | test-engineer | 已被当前 Revision 或开放 Candidate 的 `extensions.connection_id` 引用的 GraphConnection 目前仍可直接删除，会让正式节点立即变为不可查询。应拒绝删除，还是生成受控解绑 Candidate？ | product-owner + architect | RESOLVED | product-owner（user） | test-engineer（实现后验证） | 2026-08-31：被正式 Revision 或开放 Candidate 引用的连接禁止直接删除；必须先通过 Candidate 迁移或解绑引用节点。实现与 E2E 验证纳入 W-USABLE-003/004。 |
| Q-004 | test-engineer | 首轮 deterministic Build 在同 Graph 有多个 connected database 时当前选最早连接，而 SourceTable 没有 GraphConnection 归属；是否要求用户显式选择连接，并建立 SourceTable→Connection 映射？ | product-owner + architect | RESOLVED | product-owner（user） | test-engineer（实现后验证） | 2026-08-31 修正：连接及资源目录是 Graph 的构建输入；SourceTable/API resource 必须保留 connection_id，Builder 据此构图，节点记录构建后的可执行来源。只有目录来源不唯一或冲突时才澄清；不得要求用户常规逐节点点名连接，也不得按创建时间/默认连接猜测。实现纳入 W-USABLE-003。 |

## 变更请求（Change Requests）
| 编号 | 提出角色 | 目标事实 | 批准者 | 变更内容 | 影响评估 | 状态 | 实施证据 |
|------|---------|---------|---------|---------|---------|------|---------|
| C-001 | product-manager(另一 agent 提出) | spec/01,05,07 + decisions | product-owner（user） | 可验证的自定义模型供应商：DeepSeek 保持默认，允许运营者显式选择经无业务数据探测通过的内网 OpenAI-compatible qwen3.6-27b 备选（US-001，9 条 AC）。与 Phase 1 窄冲突（model routing 原为非范围）。 | 产品负责人 2026-08-21 决定砍掉；DeepSeek 维持唯一绑定。 | REJECTED | US-001 已删除；如未来重启需重新立项。 |
| C-002 | orchestrator（基于用户复盘） | spec/01,02,03,06,11,12 + GX-APP-025/030/036 | product-owner（user） | 将“数据源显式绑定 + 受控 SQL 查询验证”提升为当前可用性里程碑的基础门禁；一个 `table` 节点不能只结构合法，必须绑定同 Graph 已连接数据源并能经服务端限权查询验证。 | 与原 Phase 1 “数据库 connector 非范围”存在冲突；需修正 GraphX 产品范围/交接文档，并将 SQL backend 从 Supervisor 局部装配提升为角色最小权限共享基础设施。 | APPROVED | 2026-08-31 用户明确：SQL 应尽早提供，否则无法验证所构建的图；当前不可用感的根本是节点未连接数据源。 |
