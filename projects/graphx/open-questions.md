---
title: 未决问题与变更请求
role: orchestrator(维护) / 全员(提出)
status: DRAFT
version: 0.4
updated: 2026-08-21
upstream: []
downstream: [全员]
---

# 未决问题与变更请求（Open Questions & Change Requests）

> 项目工作区根目录的**全局**问题/变更登记簿。
> - 问题编号 `Q-xxx`，变更请求编号 `C-xxx`。
> - 任何角色可提出；**只有"等待谁"那一列的角色**能关闭它。
> - 阻塞性问题会让相关文档进入 `BLOCKED`。

## 未决问题（Questions）
| 编号 | 提出角色 | 问题 | 等待谁 | 状态 | 解决记录 |
|------|---------|------|--------|------|---------|
| Q-001 | test-engineer | GX-APP-012 删除端点 `confirmed` 缺失时的状态码：契约（spec/11 + 任务后端契约）写"confirmed 非 true → 409 DELETE_CONFIRMATION_REQUIRED"，但实现把 `confirmed` 设为必填 query 参数，缺失时 FastAPI 返回 **422**（仅 `confirmed=false` 才 409）。核心行为（未确认即拒绝、Graph 保留）一致，仅缺失分支的状态码/错误码不同。请裁定缺失分支应为 409 还是 422，以对齐契约/实现/测试。非阻塞。 | architect | RESOLVED | 2026-08-20 编排者裁定：**缺失或非 true 一律 409 DELETE_CONFIRMATION_REQUIRED**。理由：删除只能经"显式、已确认"的用户动作触发（GX-APP-012），缺失确认即"未显式确认"，应与 `confirmed=false` 统一为业务拒绝（409），错误表更干净。落地：`api.py` 将 `confirmed` 改为 `Query(False)`（缺失→False→409）；`test_graph_delete.py::test_delete_requires_confirmation` 断言缺失与 false 均 409；backend-notes 同步。 |
| Q-002 | backend-engineer | OQ-016 阻塞私有 corpus 的真实 Builder 执行：当前 DeepSeek Harness worker 与 bundled Bash 同 UID，provider Token 仍映射进 worker 环境，无法证明 Agent 不可读 Token。已完成 GX-INGEST-006 的 hash-bound 最小权限 Builder input plan，并在 Git 外对当前 corpus 生成 13 个 table source + 23 个 business-document evidence 的计划；该计划不构成真实会话授权。需要实现并验证 out-of-sandbox credential broker（或等价 UID/mount 隔离），且证明真实 Token 对 Agent/Bash 不可读后，才能装载私有语料。 | devops-engineer | OPEN | 阻塞真实 Builder/Reviewer 会话；不阻塞确定性输入准备。不得以路径权限或 0600 文件冒充安全边界。 |

## 变更请求（Change Requests）
| 编号 | 提出角色 | 目标文档 | 变更内容 | 影响评估 | 状态 |
|------|---------|---------|---------|---------|------|
| C-001 | product-manager(另一 agent 提出) | spec/01,05,07 + decisions | 可验证的自定义模型供应商：DeepSeek 保持默认，允许运营者显式选择经无业务数据探测通过的内网 OpenAI-compatible qwen3.6-27b 备选（US-001，9 条 AC）。与 Phase 1 窄冲突（model routing 原为非范围）。 | 产品负责人（用户）2026-08-21 决定**砍掉该需求**：US-001 已删除，不进入架构评估/实现。DeepSeek 维持唯一绑定（PD-020/OQ-003 不变）。如未来重启需重新立项。 | REJECTED |
