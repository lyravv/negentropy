---
title: AI Manage 首版独立验收报告
role: test-engineer
status: APPROVED
version: 0.2
updated: 2026-09-14
upstream: [projects/graphx/02-requirements/ai-manage-requirements.md v0.3, projects/graphx/03-architecture/ai-manage-contract.md v0.3, graphx/spec/11-workbench-application.md]
downstream: [orchestrator, devops-engineer, backend-engineer, frontend-engineer]
artifact_type: test-report
source_revision: graphx@bd15e9886a6180519f2912881ce28c297d4aead9+WORKTREE
reviewers: [backend-engineer, frontend-engineer, architect]
approver: test-engineer
approval_evidence: 2026-09-14 独立执行确定性后端、前端和 pinned DSH rc6 本机回环验收；结果见本文
---

# AI Manage 首版独立验收报告

## 交接说明

- **给谁**：orchestrator / devops-engineer / 实现角色
- **一句话**：完整 AI Manage 首版当前不可发布；A 切片（模型配置、快照、连接测试、日志、导航与 Applications 占位）已通过独立验收，可供本地用户体验；B 切片真实逐请求用量仍受 Q-AIM-002 阻塞。
- **关键决策**：以已批准 requirements/contract v0.3 的“多配置、无默认、每条根消息显式选择”作为验收基线；usage `unavailable` 是当前唯一诚实结果，不把 0 伪装成完整统计。
- **需要下游注意**：不得把 A 切片通过描述为完整 AI Manage 发布；不得开启 `llm_request_usage_accounting`。
- **未决问题**：Q-AIM-002（真实 attempt/失败/重试/取消/usage/重复通知的公开观测边界）。

## 1. 结论

> **不可发布**（指 R-AIM-001～007 的完整首版范围）

R-AIM-003/004 是 Must，但真实请求 attempt 与 token 采集尚未实现，且 Q-AIM-002 未关闭。其余 A 切片已通过回归，可在不宣称用量统计完成的前提下进入本地用户体验。

## 2. 执行概况

| 验证组 | 结果 | 证据 |
|---|---:|---|
| 后端、适配器、worker 配置、前端规范与 spec | 48 passed | `.venv/bin/pytest -q tests/conformance/test_ai_management_backend.py tests/test_deepseek_adapter.py tests/test_deepseek_worker_config.py tests/test_workbench_frontend.py tests/test_spec_contract.py` |
| pinned DSH rc6 真实执行路径（本机回环假 OpenAI） | 1 passed | `.venv/bin/pytest -q tests/conformance/test_ai_management_runtime_path.py`；目标实际收到 `/v1/chat/completions`、所选 model 与 Bearer token |
| Web 行为测试 | 9 passed | `cd apps/web && npm test` |
| Web production build | passed | `cd apps/web && npm run build` |

自动化断言合计 58 项通过，构建通过。错误地从 GraphX 仓库根运行 npm 曾得到无 `package.json` 的 ENOENT；在实际 Web 工程目录重跑通过，不是产品缺陷。

## 3. 验收矩阵

| 范围 | 结果 | 说明 |
|---|---|---|
| 多配置库，无默认 | PASS | 列表不含 `default_id`；页面加载/刷新不隐式选首项 |
| 每条消息显式选择 | PASS | 无选择禁止发送；成功接受后立即清空，下一条需重选；失败保留选择便于重试 |
| 根任务树不可变快照 | PASS | 根任务绑定 `config_id+version`；子任务继承同一 snapshot |
| 遗留活动树恢复 | PASS | 旧活动任务原子补 `legacy_recovery` 并由活动后代共享；已结束历史保持 null |
| 配置真实生效 | PASS | pinned DSH rc6 通过 Cordis 向选择的 Base URL 发请求，请求 model/auth 匹配；非 WorkerConfig 回显测试 |
| 凭据保护 | PASS | 0600 env 文件；worker 可读格式；跨 endpoint/provider 不复用；测试临时凭据 finally 删除；响应/进程输出不含 secret |
| 非空旧表迁移 | PASS | SQLite 老配置与快照表补列并保留数据；迁移失败不再静默吞掉 |
| 跨 Graph 日志与 Trace | PASS | 稳定 agent/sequence/event 排序；展示公共 assistant/tool call/tool result 原文与标记；过滤 status/thinking_summary |
| Usage 诚实性 | PASS（降级态） | 返回 `collection_state=unavailable`、coverage=false/historical_gap=true，不把 0 说成实际零消耗 |
| 真实逐请求用量 | BLOCKED | 没有 attempt 持久化/幂等合并/失败与 retry 证据；Q-AIM-002 未关闭 |
| 四导航与 Applications 占位 | PASS | Applications 无后端创建/运行能力 |

## 4. 缺陷与回归

验收期间发现并由实现角色修复、随后回归通过：

1. **P0 凭据格式不兼容**：保存端原写裸 token，worker 只读 `TOKEN_DEEPSEEK=`；已统一并拒绝换行注入。
2. **P0 跨目标复用部署凭据**：连接测试曾可能把部署 secret 发往不同 endpoint；现仅 provider 与规范化 Base URL 完全一致时允许复用。
3. **P0 legacy recovery 缺失**：旧活动任务曾回落当前部署配置且无显式 provenance；现补建 `legacy_recovery` 快照。
4. **P0 非空旧表无迁移**：旧实现会吞异常并留下不可用表；现已验证保留数据升级。
5. **P1 隐式选择首项**：配置清单曾被前端当成用户选择；现加载/刷新保持 null，且每次已接受消息后清空。
6. **设计门禁冲突**：旧默认配置语义与实现不一致；需求、故事、设计、契约和 GraphX 规范已统一至 v0.3 无默认语义，旧方案标记 SUPERSEDED。

当前没有未修复的 A 切片 P0/P1。B 切片为明确未实现门禁，不登记为伪回归通过。

## 5. 遗留风险

- 回环测试证明成功请求路径的 endpoint/model/auth 生效，但不证明 rc6 对失败、取消、重试调度与重复 usage 通知具有足够公开观测能力。
- 当前 usage 页只能作为“尚未采集”的诚实占位；不能用于流量审计或容量判断。
- 本次未连接真实外部模型、未产生真实模型费用、未部署、未提交。

## 6. 建议

1. 将 A 切片状态记录为可本地体验，保持 `llm_request_usage_accounting: false`。
2. 下一工作项先完成 Q-AIM-002 的受控失败/重试/取消/重复通知探针；公开边界不足时走受支持 adapter instrumentation 评审。
3. 有了真实 attempt 事实后，再实现持久化、幂等、聚合与 Usage 页面，最后重新执行完整首版发布验收。

## 7. 交互收口复验（2026-09-14）

- 模型页仅表达配置库，不显示“当前在用 / 默认 / 激活”；历史名称中的状态后缀仅在读取时清理。
- Graph 非 active 卡与其他一级入口统一为 54px 高度、宽度、边框、圆角、背景和导航间距。
- 模型入口位于增高 composer 的内部底栏右侧，菜单向上展开；textarea 初始三行，容器最小高度
  112px。无配置时仍展示“配置模型”入口；成功发送后清空选择，失败保留以便重试。

复验：Web 9 passed、production build passed；GraphX 前端/规范 pytest 13 passed，
`git diff --check` passed。该 UX 切片没有未关闭 P0/P1。
