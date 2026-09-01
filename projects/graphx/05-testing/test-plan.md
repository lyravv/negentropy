---
title: 测试方案 — GX-APP-015/016/017/018
role: test-engineer
status: APPROVED
version: 0.4
updated: 2026-08-21
upstream: [graphx/spec/11-workbench-application.md, graphx/spec/03-domain-invariants.md, graphx/spec/06-testing-and-handoff.md, graphx/spec/conformance/requirements.json, 04-implementation/backend-notes.md]
downstream: [backend-engineer, orchestrator]
---

# 测试方案 — GX-APP-015/016/017/018

## W-QUERY-006 查询凭证增量门禁

| 用例 | 验证 | 优先级 |
|---|---|---|
| TC-012 | QueryReceipt JSON Schema、确定性 hash 与篡改拒绝 | P0 |
| TC-013 | 同一 Agent Task 持久化 QueryReceipt + SupervisorDecision，精确绑定 Revision 且不写 QuestionRun | P0 |
| TC-014 | Harness 私有状态保存完整凭证，公开回执只暴露 artifact ID/hash | P0 |
| TC-015 | 真实 Candidate Preview 查询凭证精确绑定且 Candidate 保持未 Apply | P0 |

通过标准：P0 100%；全量回归通过；真实 smoke 不输出业务行、连接秘密、模型正文或原始 stderr。

## 交接说明
- **给谁**：backend-engineer / orchestrator
- **一句话**：验证 Chat 生命周期门禁、多轮 Build、非构建模式真实智能体对话与空工作台 bootstrap 四个工作台行为。
- **关键决策**：四个需求均以确定性 fake harness 做 conformance 测试，mock 运行时无需 LLM key/网络（AGENTS.md 铁律）。
- **需要下游注意**：真实 DeepSeek Harness 路径由既有 harness 集成测试覆盖；真实 provider 端到端为后续项。
- **未决问题**：OQ-016（凭据隔离）仍阻塞真实私有语料 Harness 会话。

## 本轮用例与门槛（GX-APP-015/016/017/018）

| 用例 | 验证 | 优先级 |
|---|---|---|
| TC-008 | GX-APP-015：Chat 未发消息前为 unused；`bootstrap.chats[]` 暴露 `unused`；已有 unused Chat 时 `POST /graphs/{graph_id}/chats` 返回 409 `CHAT_ALREADY_UNUSED` | P0 |
| TC-009 | GX-APP-016：非空 Graph 的后续 Build 轮次被接受；Builder 经类型化工具网关设计 HGT Patch；服务端读回并重新校验 Candidate 后才允许用户 Apply；确定性模式后续轮次 409 `BUILD_REQUIRES_HARNESS` | P0 |
| TC-010 | GX-APP-017：非业务问题由只读 Builder 角色 Harness 会话回答（基于当前 Graph + 最近对话）；智能体不提交 Candidate、不改 Graph；harness 关闭/失败回退确定性上下文感知回复 | P0 |
| TC-011 | GX-APP-018：零 Graph 时 `bootstrap` 返回 200 空投影（`active_graph: null`、`thread: null`、空列表）而非 404 | P0 |

Conformance 映射：

| 需求 | Conformance 测试 |
|---|---|
| GX-APP-015 | `tests/conformance/test_chat_lifecycle.py::test_create_chat_rejected_when_unused_chat_exists` |
| GX-APP-016 | `tests/conformance/test_multi_round_build.py::test_second_build_round_produces_candidate` |
| GX-APP-017 | `tests/conformance/test_agent_chat.py::test_non_business_question_uses_agent` |
| GX-APP-018 | `tests/conformance/test_empty_workbench.py::test_bootstrap_empty_when_no_graphs` |

通过标准：P0 100%，全量回归无阻塞/严重缺陷。否则结论为“不可发布”。

## 安全执行

```bash
UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest -q
UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest \
  tests/conformance/test_chat_lifecycle.py tests/conformance/test_multi_round_build.py \
  tests/conformance/test_agent_chat.py tests/conformance/test_empty_workbench.py -v
```

所有 conformance 用例使用合成临时数据与确定性 fake harness；测试角色不修改后端实现。

## 上一轮用例与门槛（GX-INGEST-006，已回归）

| 用例 | 验证 | 优先级 |
|---|---|---|
| TC-001 | base 只含 table，拒绝 edge/hyperedge/其他 node type | P0 |
| TC-002 | 每个 table 恰好一个 SQL ref，集合与 manifest SQL 精确相等 | P0 |
| TC-003 | allowlist 仅含 `sql_templates/*.sql` 和 `hyperedges/**/*.md` | P0 |
| TC-004 | 拒绝绝对路径、`..`、symlink、伪造 role、secret/cache/golden | P0 |
| TC-005 | 空 SQL/base 不得生成违反 schema `minItems` 的 plan | P0 |
| TC-006 | 私有 JSON 原子 0600 写入，stdout/Git 文档不含私有 hash | P0 |
| TC-007 | runtime payload/schema/spec/requirements 一致 | P1 |

通过标准：P0/P1 100%，无阻塞/严重缺陷，私有产物无 group/other 权限，目标回归在 30 秒硬超时内通过。否则结论为“不可发布”。

## 上一轮安全执行（GX-INGEST-006）

```bash
timeout --signal=TERM --kill-after=5s 30s .venv/bin/pytest -q \
  tests/test_corpus_manifest.py tests/test_corpus_contract_schema.py \
  tests/test_private_corpus_cli.py tests/test_sql_ingestion.py tests/test_spec_contract.py
```

所有攻击用例使用合成临时数据；测试角色不修改后端实现。
