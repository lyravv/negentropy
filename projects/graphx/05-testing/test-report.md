---
title: 测试报告 — GX-APP-015/016/017/018
role: test-engineer
status: APPROVED
version: 0.3
updated: 2026-08-21
upstream: [05-testing/test-plan.md, 05-testing/defect-log.md]
downstream: [backend-engineer, orchestrator, devops-engineer]
---

# 测试报告 — GX-APP-015/016/017/018

> 本报告取代 v0.2（GX-INGEST-006）测试报告；旧报告结论已并入缺陷日志回归结论。

## 交接说明
- **给谁**：backend-engineer / orchestrator / devops-engineer
- **一句话**：**可发布** —— 全量回归 154 passed + 12 subtests（7.51s，退出码 0），四个新工作台行为 conformance 4/4 通过，无新缺陷。
- **关键决策**：GX-APP-015/016/017/018 均以确定性 fake harness 做 conformance 测试，mock 运行时无需 LLM key/网络（AGENTS.md 铁律）。
- **需要下游注意**：8001 线上服务仍运行旧代码，需 devops 重新部署（W-OPS-001）后本轮修复才生效。
- **未决问题**：OQ-016（凭据隔离）仍阻塞真实私有语料 Harness 会话；真实 provider 端到端为后续项。

## 1. 结论

> **可发布**

全量回归 `154 passed, 12 subtests passed in 7.51s`（退出码 0），与预期一致；GX-APP-015/016/017/018 四个 conformance 测试全部通过，未发现新的阻塞或严重缺陷。四个工作台行为（Chat 生命周期门禁、多轮 Build、非构建模式真实智能体对话、空工作台 bootstrap）可发布。该结论不授权启动真实私有 Harness 会话，OQ-016 仍须先关闭。

## 2. 执行结果

| 项目 | 结果 |
|---|---|
| 全量回归 | 154 passed + 12 subtests passed，7.51 秒，退出码 0 |
| GX-APP-015 `test_chat_lifecycle.py::test_create_chat_rejected_when_unused_chat_exists` | 通过 |
| GX-APP-016 `test_multi_round_build.py::test_second_build_round_produces_candidate` | 通过 |
| GX-APP-017 `test_agent_chat.py::test_non_business_question_uses_agent` | 通过 |
| GX-APP-018 `test_empty_workbench.py::test_bootstrap_empty_when_no_graphs` | 通过 |
| 四个 conformance 定向运行 | 4 passed，0.49 秒，退出码 0 |

## 3. 规范一致性与下一轮

- 四个需求已在 spec/11-workbench-application.md、spec/03-domain-invariants.md、spec/06-testing-and-handoff.md、spec/conformance/requirements.json（均 `implemented` 并绑定 conformance 测试）、spec/manifest.yaml（conformance 指向 requirements.json）与 docs/architecture/frontend-backend-api-contract.md 间同步一致。
- 确定性回退保持 mock 运行时无 LLM key/网络可用（AGENTS.md 铁律）：GX-APP-017 harness 关闭/失败回退确定性上下文感知回复；GX-APP-016 确定性模式后续轮次 409 `BUILD_REQUIRES_HARNESS` 失败关闭。
- 下一轮 / 需要下游注意：
  1. 8001 线上服务仍运行旧代码，必须重新部署（devops W-OPS-001）后本轮修复才生效。
  2. GX-APP-017（真实智能体对话）与 GX-APP-016（多轮设计模式 Build）本轮以确定性 fake harness 验证；真实 DeepSeek Harness 路径由既有 harness 集成测试覆盖，真实 provider 的 live 端到端运行为后续项。
  3. OQ-016（凭据隔离）未关闭前不得启动真实私有语料 Harness 会话。
