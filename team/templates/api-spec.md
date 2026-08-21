---
title: 接口规范（API Spec）
role: architect
status: DRAFT
version: 0.1
updated: YYYY-MM-DD
upstream: [03-architecture/architecture.md]
downstream: [frontend-engineer, backend-engineer, test-engineer]
artifact_type: api-contract
source_revision: N/A
reviewers: [frontend-engineer, backend-engineer, test-engineer]
approver: architect
approval_evidence:
---

# 接口规范

> **这是前后端的契约。** 任何变更必须走变更流程（见协议），并经 architect 确认。
> 前端按此实现调用，后端按此实现服务，测试按此设计用例。

## 交接说明
- **给谁**：frontend / backend / test
- **一句话**：<本系统对外提供哪些接口>
- **关键决策**：<接口风格、鉴权方式>
- **需要下游注意**：<版本策略、错误码约定>
- **未决问题**：无 / Q-xxx

## 约定
- Base URL：`/api/v1`
- 鉴权：<方式，如 Bearer Token>
- 通用响应包裹：
  ```json
  { "code": 0, "message": "ok", "data": { } }
  ```
- 错误码：`0` 成功；非 0 见错误码表
- 分页：`?page=1&size=20`，响应含 `total`

## 接口列表
| 编号 | 方法 | 路径 | 说明 | 对应故事 |
|------|------|------|------|---------|
| API-001 | GET | /users | 用户列表 | US-001 |

## 接口详情

### API-001 用户列表
- **方法/路径**：`GET /api/v1/users`
- **说明**：...
- **请求参数**：
  | 参数 | 位置 | 类型 | 必填 | 说明 |
  |------|------|------|------|------|
- **请求示例**：
- **响应示例**：
  ```json
  {}
  ```
- **错误**：
  | code | 含义 |
  |------|------|

## 错误码表
| code | 含义 | 处理建议 |
|------|------|---------|
