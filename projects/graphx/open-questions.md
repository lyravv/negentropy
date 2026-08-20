---
title: 未决问题与变更请求
role: orchestrator(维护) / 全员(提出)
status: DRAFT
version: 0.1
updated: YYYY-MM-DD
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

## 变更请求（Change Requests）
| 编号 | 提出角色 | 目标文档 | 变更内容 | 影响评估 | 状态 |
|------|---------|---------|---------|---------|------|
| C-001 | | | | | PENDING / APPROVED / REJECTED |
