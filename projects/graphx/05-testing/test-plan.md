---
title: 测试方案 — Graph 删除（GX-APP-012）+ 推送组织库（GX-APP-013）
role: test-engineer
status: APPROVED
version: 0.1
updated: 2026-08-20
upstream: [graphx/spec/11-workbench-application.md, graphx/spec/03-domain-invariants.md, 04-implementation/backend-notes.md, 04-implementation/frontend-notes.md]
downstream: [test-engineer(执行), orchestrator, devops-engineer]
---

# 测试方案 — Graph 删除（GX-APP-012）+ 推送组织库（GX-APP-013）

## 交接说明
- **给谁**：自己（执行）/ orchestrator / devops-engineer
- **一句话**：为阶段 4 新增的 `DELETE /api/v1/alpha/graphs/{id}` 与 `POST /api/v1/alpha/graphs/{id}/push` 编写接口级合规测试（9 条用例，全部可追溯到 GX-APP-012/013 的 MUST 或接口错误码），并执行全量回归；P0/P1 全绿且无阻塞/严重缺陷即"可发布"。
- **关键决策**：
  1. 测试层级为**接口级（TestClient + 临时 SQLite）**，风格对齐 `tests/test_alpha_app.py`；级联删除与组织库快照通过**直接查 DB** 断言（API 不暴露这些内部行）。
  2. 共享 `settings`/`client` 助手抽到 `tests/conformance/conftest.py`（pytest fixture），两个合规文件复用，避免重复。
  3. 候选级联（BuildRun/Candidate/CandidateReview）无独立创建端点，按任务要求**直接往 DB 插行**覆盖。
  4. 推送"保留版本历史"通过**直接插入 number=2 的 GraphRevision**（合法小 bundle + `bundle_hash`）并置为当前版本来验证。
  5. GX-APP-014 画布合规测试由 frontend-engineer 交付（`test_canvas_renders_typed_hypergraph`），本轮**只确认其通过，���重写**。
- **需要下游注意**：
  - 删除端点 `confirmed` 缺失时实现返回 **422**（必填 query 参数），仅 `confirmed=false` 返回 409 `DELETE_CONFIRMATION_REQUIRED`；与任务测试规格"缺失也 409"存在措辞差异，已记 **Q-001** 待 architect 裁定（非阻塞，核心拒绝行为一致）。
  - 组织库 Add/删除/更新端点、重复推送去重、Postgres 迁移均**不在本轮范围**（见 test-report 遗留风险）。
- **未决问题**：Q-001（`confirmed` 缺失分支状态码 409 vs 422，等待 architect）

## 1. 测试范围

### 测什么（本轮范围）
- **GX-APP-012 删除 Mine Graph**（`DELETE /api/v1/alpha/graphs/{graph_id}?confirmed=`）：
  - Mine Graph 经显式确认可删除，且级联清除 revisions / Candidates / Chats / Connections 及连接密钥文件；
  - System（非 mine）Graph 不可删除（409 `GRAPH_READ_ONLY`）；
  - 未确认（`confirmed=false` / 缺失 `confirmed`）被拒绝，Graph 保留；
  - 不存在的 graph_id → 404 `GRAPH_NOT_FOUND`。
- **GX-APP-013 推送组织库**（`POST /api/v1/alpha/graphs/{graph_id}/push`）：
  - Mine Graph 经 `actor=user` + `confirmed=true` 可推送，生成 `org_library_graphs` 快照（当前 revision bundle + 全量 revision 历史，按 number 升序）；
  - 推送后本地 Graph 保持 `mine` 可编辑（ownership 不变）；
  - System Graph 不可推送（409 `GRAPH_READ_ONLY`）；
  - 非 user actor 或未确认 → 409 `PUSH_CONFIRMATION_REQUIRED`；
  - 不存在的 graph_id → 404 `GRAPH_NOT_FOUND`；
  - `bootstrap` 响应新增 `org_library` 字段，推送后可见该条目（字段齐全）。

### 不测什么（本轮范围外）
- **GX-APP-014 画布渲染**：已由 frontend-engineer 的 `tests/test_workbench_frontend.py::test_canvas_renders_typed_hypergraph` 覆盖（源码级断言），本轮仅确认其通过，不重写、不扩展。
- **从组织库 Add 只读副本端点**：本轮未实现（backend-notes 已知限制 1），无端点可测。
- **组织库删除/更新端点**：本轮未实现（backend-notes 已知限制 3）。
- **重复推送去重/覆盖语义**：契约未定义（backend-notes 已知限制 2），不测幂等。
- **Postgres 迁移**：devops 部署项（backend-notes 已知限制 5），本轮仅 SQLite。
- **删除后工作台回退到另一 Graph**：属工作台/前端行为，后端 `bootstrap` 的选图逻辑由 backend 自测覆盖；本轮合规测试不单独断言（列入遗留风险）。
- **"Delete/Push MUST NOT be an Agent 工具"**：架构约束，经代码审查确认（两端点为用户侧 HTTP 端点，未注册为 Agent 工具），不写自动化用例。

## 2. 测试策略
| 层级 | 方法 | 覆盖目标 |
|------|------|---------|
| 接口（主） | `TestClient(create_app(...))` + 临时 SQLite（`tmp_path`），断言 `status_code` 与 `json()["detail"]["code"]` | GX-APP-012/013 全部 MUST + 4 个错误码（`GRAPH_NOT_FOUND`/`GRAPH_READ_ONLY`/`DELETE_CONFIRMATION_REQUIRED`/`PUSH_CONFIRMATION_REQUIRED`）的正常/异常/边界路径 |
| 数据（辅助） | 直接经 `service.database.sessions` 查/插 DB 行 | 级联删除的 8 类从属行清空、连接密钥文件 unlink、`org_library_graphs` 快照字段、revision 历史升序、本地 ownership 不变 |
| 回归 | `uv run pytest -q` 全量 | 不破坏既有 117 个测试 + 12 subtests |

## 3. 测试用例
| 用例ID | 函数名 | 对应 MUST / 接口 | 前置 | 步骤 | 预期 | 优先级 |
|--------|--------|-----------------|------|------|------|--------|
| TC-001 | `test_delete_mine_graph_removes_related_records` | GX-APP-012「Mine 可删 + 删除清除 revisions/Candidates/Chats/Connections」 | 新建 Mine Graph + 1 Chat + 1 数据连接（probe 打桩 True）+ DB 直插 BuildRun/Candidate/CandidateReview | `DELETE ?confirmed=true` | 200 `{"status":"deleted","graph_id"}`；Graph/GraphRevision/ChatThread/ChatMessage/GraphConnection/BuildRun/Candidate/CandidateReview 行全清空；密钥文件 `connections/<id>.json` 被删 | P0 |
| TC-002 | `test_delete_system_graph_rejected` | GX-APP-012「System 不可删」+ GX-GRAPH-003 | 新建 Graph 后 DB 置 `ownership="system"` | `DELETE ?confirmed=true` | 409 `GRAPH_READ_ONLY`；Graph 仍存在 | P0 |
| TC-003 | `test_delete_requires_confirmation` | GX-APP-012「仅显式确认可删」 | 新建 Mine Graph | ① `DELETE`（缺 `confirmed`）② `DELETE ?confirmed=false` | ① 422（必填参数缺失）② 409 `DELETE_CONFIRMATION_REQUIRED`；两种情况 Graph 均保留（缺失分支 409/422 措辞差异见 Q-001） | P0 |
| TC-004 | `test_delete_nonexistent_graph_404` | 接口错误码 `GRAPH_NOT_FOUND` | — | `DELETE /graphs/graph-does-not-exist?confirmed=true` | 404 `GRAPH_NOT_FOUND` | P1 |
| TC-005 | `test_push_mine_graph_creates_org_library_entry` | GX-APP-013「Mine 可推 + 保留内容与版本历史」 | 新建 Mine Graph（rev1 空 bundle）+ DB 直插 number=2 合法 revision 并置为当前 | `POST push {actor:user,confirmed:true}` | 200 `status=pushed`、`revision=2`、`org_library_id` 前缀 `org-`；`org_library_graphs` 行 `revision_number=2`、`content_hash`/`bundle_json` 等于当前 revision、`revision_history_json` 2 条按 number 升序 [1,2]；本地 Graph `ownership` 仍 `mine` | P0 |
| TC-006 | `test_push_system_graph_rejected` | GX-APP-013（仅 Mine 可推）+ GX-GRAPH-003 | 新建 Graph 后 DB 置 `ownership="system"` | `POST push {actor:user,confirmed:true}` | 409 `GRAPH_READ_ONLY`；`org_library_graphs` 无残留行 | P0 |
| TC-007 | `test_push_requires_confirmation` | GX-APP-013「仅 user 显式确认可推」 | 新建 Mine Graph | ① `POST push {actor:agent,confirmed:true}` ② `POST push {actor:user,confirmed:false}` | 均 409 `PUSH_CONFIRMATION_REQUIRED`；`org_library_graphs` 无残留行 | P0 |
| TC-008 | `test_push_nonexistent_graph_404` | 接口错误码 `GRAPH_NOT_FOUND` | — | `POST /graphs/graph-does-not-exist/push {actor:user,confirmed:true}` | 404 `GRAPH_NOT_FOUND` | P1 |
| TC-009 | `test_bootstrap_exposes_org_library` | GX-APP-013「推送后可在组织库看到」 | 新建 Mine Graph 并成功 push | `GET /api/v1/alpha/bootstrap` | `org_library` 非空且含该条目，字段恰为 `{id,name,source_graph_id,revision,content_hash,pushed_at}` | P0 |

> 追溯说明：TC-001/002/003 → GX-APP-012；TC-005/006/007/009 → GX-APP-013；TC-004/008 → 两端点的 `GRAPH_NOT_FOUND` 错误码（spec/11 HTTP API draft + 任务后端契约）。GX-APP-014 由既有 `test_canvas_renders_typed_hypergraph` 覆盖（本轮确认通过）。

## 4. 测试数据
- **环境**：`tmp_path` 下临时 SQLite（`sqlite:///<tmp>/graphx.db`），`Settings` 指向 `tmp_path` 的 `connections/`、`myspace/`、`business/` 目录；`FakeHarness` + `FakeQuestionExecutor` 打桩，无需 LLM key / 网络。
- **Mine Graph**：`POST /api/v1/alpha/graphs`（默认 revision 1，空 bundle）。
- **数据连接**：`POST .../connections`，`monkeypatch` 打桩 `service._probe_connection → True`，密钥落 `tmp_path/connections/<id>.json`（0600）。
- **候选级联行**：DB 直插 `BuildRun`（`build-run-delete-0001`）+ `Candidate`（`candidate-delete-0001`）+ `CandidateReview`（`review-delete-0001`），`base_revision_id` 指向当前 revision。
- **第二 revision**：DB 直插 `GraphRevision`（`revision-push-0002`，number=2，parent→rev1），bundle 用 `HGTBundle` + 单个 `table` 节点构造，`content_hash=bundle_hash(bundle)`，并置 `graph.current_revision_id` 指向它。
- **System Graph**：DB 直改 `Graph.ownership="system"`。

## 5. 通过标准（Definition of Done for 测试）
- **P0/P1 合规用例通过率 = 100%**（9/9：TC-001…TC-009 全绿）。
- **全量回归全绿**：`uv run pytest -q` 最终计数 ≥ 基线 117 passed + 12 subtests，且新增 9 条全过（预期 126 passed + 12 subtests）。
- **GX-APP-014 画布合规测试** `test_canvas_renders_typed_hypergraph` 通过。
- **缺陷门槛**：无阻塞/严重缺陷遗留；一般/轻微缺陷须有明确归属与处置（修复或经 orchestrator 确认接受）。
- 满足以上 → 测试报告结论为**可发布**；否则**不可发布**。

## 6. 环境与工具
- Python 3.12 + `uv`（`UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv`，系统 uv 缓存只读）。
- `pytest`（`uv run pytest`）、`fastapi.testclient.TestClient`、`sqlalchemy`（直查 DB）。
- 仓库：`/home/wangling/develop_team/graphx`，分支 `feat/trusted-build-core`，产品版本 0.5.7。
- 运行命令：
  ```bash
  cd /home/wangling/develop_team/graphx
  UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest tests/conformance/ -v   # 本轮合规
  UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest -q                     # 全量回归
  ```
