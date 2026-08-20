---
title: 实现说明（后端）— Graph 删除 + 推送组织库
role: backend-engineer
status: APPROVED
version: 0.2
updated: 2026-08-20
upstream: [graphx/spec/11-workbench-application.md, graphx/spec/03-domain-invariants.md, graphx/spec/08-hgt-protocol-v0.1.md]
downstream: [test-engineer, devops-engineer]
---

# 实现说明（后端）— 阶段 4：Graph 删除（GX-APP-012）+ 推送组织库（GX-APP-013）

## 交接说明
- **给谁**：test-engineer / devops-engineer
- **一句话**：新增 `DELETE /api/v1/alpha/graphs/{graph_id}`（级联删除 Mine Graph）与 `POST /api/v1/alpha/graphs/{graph_id}/push`（推送快照到组织库），并在 `bootstrap` 响应新增 `org_library` 字段；全部按 APPROVED 契约实现，现有 116 个测试保持全绿。
- **关键决策**：
  1. 错误检查顺序按契约错误表顺序执行：先 404 `GRAPH_NOT_FOUND`，再 409 `GRAPH_READ_ONLY`，最后 409 确认类错误（`DELETE_CONFIRMATION_REQUIRED` / `PUSH_CONFIRMATION_REQUIRED`）。
  2. `PushGraphRequest` 的 `actor`/`confirmed` 用普通 `str`/`bool`（不用 `Literal`），使非法 actor / 未确认请求落到服务层返回 409 而非 FastAPI 422。
  3. 删除在单个事务内按"先子后父"顺序级联删除（ChatMessage → BuildRun → QuestionRun → CandidateReview → Candidate → GraphRevision → GraphConnection → ChatThread → Graph）；连接密钥文件在事务提交后 `unlink(missing_ok=True)`。
  4. 推送只新增 `org_library_graphs` 行（当前 revision 的 bundle + 全量 revision 历史），不修改本地 Graph/Revision，本地保持 `mine` 可编辑。
  5. `bootstrap.org_library` 按 `pushed_at` 升序（`id` 作稳定次级排序键），无条目时为空 list。
- **需要下游注意**：
  - 新表 `org_library_graphs` 由 `Base.metadata.create_all` 自动建表（SQLite 开发库首次启动即生效）；Postgres 部署需执行 `CREATE TABLE org_library_graphs`（字段见第 2 节）。
  - 删除/推送端点暂无合规测试（`spec/conformance/requirements.json` 中 GX-APP-012/013 仍为 `planned`，`planned_test` 指向 `tests/conformance/test_graph_delete.py` / `test_graph_push.py`），由 test-engineer 补齐。
  - 本轮**不实现**"从组织库添加只读副本"的 Add 端点（见第 6 节已知限制）。
- **未决问题**：无（契约问题见 open-questions.md，本轮未新增）

## 1. 实现范围
对应 `spec/11-workbench-application.md` 的 GX-APP-012 / GX-APP-013 与 `spec/03-domain-invariants.md` 同名不变量：

| 契约项 | 实现 |
|--------|------|
| `DELETE /api/v1/alpha/graphs/{graph_id}?confirmed=`（GX-APP-012） | `api.delete_graph` → `GraphXService.delete_graph` |
| 删除级联：revisions / Candidates / Chats / Connections + 密钥文件 | 单事务先子后父删除 + 提交后 unlink |
| `POST /api/v1/alpha/graphs/{graph_id}/push`（GX-APP-013） | `api.push_graph` → `GraphXService.push_graph` |
| 推送保留内容与 revision 历史 | `OrgLibraryGraph` 快照（bundle + 全量历史） |
| 推送后"available in the organization library"可验证 | `bootstrap` 响应新增 `org_library` 列表 |
| 错误码 `GRAPH_NOT_FOUND` / `GRAPH_READ_ONLY` / `DELETE_CONFIRMATION_REQUIRED` / `PUSH_CONFIRMATION_REQUIRED` | 全部实现，经既有 `ProductError` 处理器映射 404/409 |

不在本轮范围：从组织库 Add 只读副本端点（后续项，见第 6 节）。

## 2. 代码结构
只改动 4 个后端文件（`/home/wangling/develop_team/graphx/src/graphx_alpha/`）：

- **entities.py** — 新增 `OrgLibraryGraph`（表 `org_library_graphs`）：
  `id` String(64) PK（值 `org-{uuid4().hex}`）、`source_graph_id` String(64)、`name` String(200)、`description` Text 默认 `""`、`bundle_json` JSON（当前 revision 的 bundle）、`revision_number` Integer、`content_hash` String(80)、`revision_history_json` JSON（`[{id, number, content_hash, created_by, created_at}]` 按 number 升序，`created_at` 存 ISO 字符串）、`pushed_at` DateTime(timezone=True) 默认 now。
- **schemas.py** — 新增 `PushGraphRequest`：`actor: str`、`confirmed: bool`（`extra="forbid"` 继承自 `APIModel`）。
- **service.py** — 新增 `delete_graph(graph_id, *, confirmed)` 与 `push_graph(graph_id, *, actor, confirmed)`；`bootstrap` 查询 `OrgLibraryGraph` 并在响应 `graphs` 之后新增 `org_library` 字段（每项 `{id, name, source_graph_id, revision, content_hash, pushed_at}`，按 `pushed_at` 升序）。
- **api.py** — 新增两个路由（删除端点 `confirmed` 为 `Query(False)`：缺失即视为"未显式确认"，与服务层 `confirmed=false` 统一返回 409 `DELETE_CONFIRMATION_REQUIRED`，而非 422——Q-001 裁定）；错误响应沿用既有 `ProductError` 处理器（`*_NOT_FOUND` → 404，其余 → 409，包裹格式 `{"detail": {"code", "message"}}` 不变）。

## 3. 如何运行
```bash
cd /home/wangling/develop_team/graphx
UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv sync
# 全量测试（含 spec-contract）
UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest -q
# 启动服务（默认 SQLite：runtime/alpha/graphx.db，首次启动自动建表含 org_library_graphs）
UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run python -m graphx_alpha.api
```
环境变量与既有端点一致（`GRAPHX_APP_DATABASE_URL`、`GRAPHX_PORT` 等），本轮无新增环境变量。

手工验证示例：
```bash
curl -X DELETE "http://127.0.0.1:8001/api/v1/alpha/graphs/<graph_id>?confirmed=true"
curl -X POST "http://127.0.0.1:8001/api/v1/alpha/graphs/<graph_id>/push" \
  -H 'Content-Type: application/json' -d '{"actor":"user","confirmed":true}'
curl "http://127.0.0.1:8001/api/v1/alpha/bootstrap" | jq .org_library
```

## 4. 契约偏离记录
> 无偏离。以下为按契约实现时做出的、契约未显式规定的实现选择（已按"最合理理解"落地并在此显式记录）：

| 位置 | 契约原文 | 实际实现 | 原因 | 是否已同步契约 |
|------|---------|---------|------|--------------|
| 删除/推送错误检查顺序 | 错误表列出 404 → 409 READ_ONLY → 409 确认 | 按该顺序检查（Graph 不存在时即使 confirmed 缺失也返回 404） | 契约未规定多错误同时成立时的优先级，按错误表列出顺序实现 | 否（非偏离，建议 test-engineer 按此顺序设计用例） |
| `OrgLibraryGraph.description` | 字段 `description (Text, 默认 "")` | 恒存 `""` | `Graph` 实体无 description 字段，无来源可复制 | 否 |
| 重复推送同一 Graph | 未规定幂等/覆盖语义 | 每次推送新增一行 `org_library_graphs` | 契约只要求"推送后可在组织库看到"，未定义去重/覆盖 | 否（见第 6 节已知限制） |
| `revision_history_json.created_at` | 未规定序列化格式 | ISO 8601 字符串 | JSON 列不能直接存 datetime（与既有 `mode="json"` 惯例一致） | 否 |

## 5. 自测情况
- 全量回归：`uv run pytest -q` → **116 passed + 12 subtests**（与改动前基线一致，无破坏；注：并行前端工程师同期新增 1 个前端源码级测试，合库后为 117 passed，亦全绿）。
- 临时自测脚本（12 个用例，覆盖正常 + 全部错误路径，自测后已删除，未留在仓库）：
  - bootstrap 初始 `org_library == []`；
  - push 成功：200 且 `status/org_library_id/graph_id/revision` 字段齐全，`org_library_id` 前缀 `org-`；bootstrap `org_library` 条目字段集合与契约一致；
  - push 保留全量 revision 历史（构造 2 个 revision 后推送，`revision_history_json` 按 number 升序为 [1, 2]，`revision_number=2`）；
  - push 拒绝 `actor=agent` / `confirmed=false` / 两者皆错 → 409 `PUSH_CONFIRMATION_REQUIRED`，且组织库无残留行；
  - push 不存在 Graph → 404 `GRAPH_NOT_FOUND`；push System Graph → 409 `GRAPH_READ_ONLY`；
  - push 后本地 Graph 仍 `mine`、revision 不变（可编辑性保持）；
  - delete `confirmed=false` 或缺 `confirmed` 参数 → 均 409 `DELETE_CONFIRMATION_REQUIRED`（Q-001 裁定：缺失=未显式确认，统一 409）；Graph 仍在；
  - delete 不存在 Graph → 404 `GRAPH_NOT_FOUND`；delete System Graph → 409 `GRAPH_READ_ONLY`；
  - delete 成功：200 `{"status":"deleted","graph_id":...}`，9 类从属行（ChatMessage/BuildRun/QuestionRun/CandidateReview/Candidate/GraphRevision/GraphConnection/ChatThread/Graph）全部清空，连接密钥文件（0600）被 unlink；
  - 删除默认 Graph 后 bootstrap 回退到剩余 Graph（`active_graph` 为备用 Graph）。

## 6. 已知限制 / 遗留问题
1. **Add 端点未实现（本轮范围外）**：从组织库"添加只读副本"的端点未实现，前端 Add 弹窗本轮只读展示 `bootstrap.org_library`；后续需定义副本的 ownership（`system` 只读）与 source 绑定语义。
2. **重复推送不去重**：同一 Graph 多次推送产生多行 `org_library_graphs`（每行一个 `org-*` id）；契约未定义覆盖/幂等语义，如需"最新一次为准"需走 C-xxx 变更。
3. **组织库无删除/更新端点**：`org_library_graphs` 行一旦写入不可变（与 revision 不可变原则一致），但也没有管理端点；属后续产品决策。
4. **删除为不可逆操作**：无回收站/软删除；密钥文件 unlink 后不可恢复（符合 GX-APP-012 "Delete is irreversible"）。
5. **Postgres 迁移**：开发用 SQLite 由 `create_all` 自动建表；生产 Postgres 需补一条 `CREATE TABLE org_library_graphs` 迁移（字段见第 2 节），由 devops-engineer 在部署时执行。
6. **错误优先级假设**：多错误同时成立时按"404 → READ_ONLY → 确认"顺序返回（见第 4 节），如 test-engineer 认为应不同，请提 open question 由 architect 裁定。
