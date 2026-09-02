---
title: 测试报告 — GX-APP-015/016/017/018/021..025
role: test-engineer
status: APPROVED
version: 1.6
updated: 2026-09-02
artifact_type: test-report
source_revision: graphx@cb18047
approver: test-engineer
approval_evidence: W-FLOW-006 formal Chat complete team run; focused guard regression 31 passed; prior W-FLOW-005 73 tests + 13 subtests
upstream: [05-testing/test-plan.md, 05-testing/defect-log.md]
downstream: [backend-engineer, orchestrator, devops-engineer]
---

## 2026-09-02 W-POLISH-001 / W-META-001 · APPROVED / APPLY PENDING

- GraphX `5e3526e`/`71dc019` 关闭 Cordis spine 的 workspace/skill/bash/job/goal 工具，并逐次将
  provider request/header 工具名与 server grant 比对；兼容 Harness schema-object header。
- Reviewer/Tester 公开消息改为类型化报告的确定性短摘要，不再复制模型 final prose、finding/check
  payload 或业务计数。真实 Reviewer 工具清单无 native tool。
- GraphX `0bf3e48` 从精确 Candidate Preview 生成四条有序关系计划；真实 Tester 仅调用
  `candidate_get`、四次 `graph_relation_check`、`test_run`，四份 receipt 与 TestReport 均 passed。
- GraphX `cb18047` 修复历史 SourceTable 主键/连接 upsert；五表目录 alias 已统一到 connection namespace。
  Query authorization 使用精确 connection/schema/table，目录刷新后 Revision 4 只读查询仍成功。
- Candidate `candidate:agent-task-e4363b2e8043479c8bd2185d430474b8` 仅含两个 node update；与
  Revision 4 的差异字段都且只有 `source_refs`。Review/Test passed，正式 Revision 仍为 4，等待用户 Apply。

## 2026-09-01 W-FLOW-006 · TEAM E2E APPROVED / APPLY PENDING

- GraphX `3d39eeb` 约束每个 Supervisor run 只接受一个权威 decision；`bd2c53f` 将无变化保护限定为
  同一 root task lineage 的连续 Builder Artifact hash，历史等价 Candidate 不再阻断新用户目标。
- 两项修复均已推送，`bd2c53f` 部署到 8001（PID 3889276）；相关动态任务图、Supervisor、规范、
  Compiler/Harness 共 31 项测试通过。
- 正式 Chat `thread-1960563b5c264656bda7be3ac593e4ff` 由一次用户目标动态完成
  GraphX→Builder→Reviewer→Tester→GraphX；未使用固定流水线，未自动 Apply。
- Candidate `candidate:agent-task-75bfc1872f41407eb273c5ca28632f8a` 为 ready：Preview 为
  5 node + 4 relation + 1 hyperedge；Reviewer passed；Tester 四条 Candidate-bound relation receipt
  均为 20/capped，权威 TestReport 已持久化且 passed。
- 正式 Graph Revision 仍为 3。E2E 团队链验收通过；W-FLOW-006 仅剩用户逐次确认 Apply、重启持久性
  与随机订单查询验证，因此不得标记完整发布 DONE。

### Apply 后补充验收 · APPROVED

- Product owner 已显式 Apply；Candidate 状态 `applied`，正式 Graph 从 Revision 3 升为 Revision 4
  (`revision-a16a8569e53943ecb291ea1704dd268b`)。
- GraphX 重启到 PID 3917230 后，Bootstrap 仍为 Revision 4，结构仍精确为 5 node + 4 edge +
  1 hyperedge，证明正式图持久化成功。
- Apply 后只读 Chat 任务 `agent-task-0c5ff470895b4dd1a010558dcf0f238c` 通过
  `graph_sql_query` 在语义节点 `sales-order` 返回 1 条有界结果；QueryReceipt 绑定精确 Revision 4、
  candidate_id 为空，并完整通过五项 Gateway 检查。W-FLOW-006 发布闭环 APPROVED。

## 2026-09-01 W-FLOW-005 · APPROVED

- GraphX commit：`15878ba feat: guide complete fulfillment builds`，已推送并部署（PID 3870656）。
- `graphx-semantic-scenario/v1` 在五表资源全部 server-bound 时向 Builder 暴露，在精确 Candidate Preview
  含五表时向 Reviewer/Tester 暴露；不做关键词路由，不固定角色流水线，不含 ID/秘密/业务行。
- `update_table_relation` 允许用语义旧端点纠正方向/端点/结构化 join；Compiler 保持 edge ID、注入
  precondition，并解析同一提案前序节点改名，解决正式图反向旧边无法收敛的问题。
- 73 项定向/规范/Compiler/Harness 测试及 13 subtests 通过。
- 真实隔离 runner `fulfillment-team-20260901-v1`：一次用户目标由 Builder 生成 10-operation Candidate，
  Preview 精确为 5 node + 4 relation + 1 hyperedge；独立 Reviewer passed；Tester 四条关系各生成
  Candidate-bound receipt（均 20/capped），TestReport passed；Candidate 保持 unapplied，零业务行/秘密日志。

## 2026-09-01 W-FLOW-004 · APPROVED

- GraphX commit：`5791c04 feat: validate candidate relations safely`，已推送并部署（PID 3847889）。
- `graph_relation_check` 仅接受两个语义节点名、1–4 个字段对和上限 20；服务端绑定精确
  Revision/Candidate hash、解析字段和同库连接、执行 read-only timeout join，仅返回聚合计数。
- `graphx-relation-check-receipt/v1`、ADR-013、GX-QUERY-007、role-tools、Harness 协议、Tester prompt
  与持久 TypedAgentArtifact 输出已同步；跨连接关系明确 fail closed。
- 63 项定向/规范/角色/桥接/运行时测试及 13 个 subtests 通过。
- 真实隔离 Harness `relation-20260901-v2` 仅调用 `candidate_get → graph_relation_check → test_run`；
  `sales-order.sales_order_code = shipment-application.sales_order_code` 返回 `20/capped=true`，六项网关
  检查与静态 TestReport 通过；Candidate 保持 proposed/unapplied，未输出业务行、SQL 或连接秘密。
- 大范围 pytest 仍会在既有 HTTP/Chat 路径长时间等待且无本切片失败栈；已中止并保持如实记录。

## 2026-09-01 W-FLOW-003 · APPROVED

- GraphX commit：`4415c30 feat: compile semantic hyperedges`，已推送并部署（PID 3589737）。
- `semantic-change/v1-draft`、Pydantic DTO、静态 JSON Schema、Builder tool catalog/prompt、ADR-012、
  GX-SEM-005 与 manifest 已同步。
- 41 项 semantic/compiler/bridge/executor/gateway/spec 定向测试通过；create/update 超边均验证 server-owned
  identity、precondition、evidence 和同提案 node dependencies。
- 真实隔离 Harness smoke `plugin-20260901-fulfillment-hyperedge` 通过：模型仅调用一次
  `graph_semantic_context_get` 和一次 `graph_propose_changes`；Candidate 含 5 node + 4 edge + 1 hyperedge，
  五个成员角色与三条业务规则完整；未访问数据库、未加载私有业务文档、未 Apply。
- 全量 265 项回归在既有 `tests/conformance/test_agent_chat.py::test_non_business_question_uses_agent`
  长时间等待且无失败栈，已中止并作为独立运行时测试问题保留；不据此伪称全量通过。

# 测试报告 — GX-APP-015/016/017/018/021..025

## 2026-09-01 W-EVAL-002 · APPROVED

- versioned 6-case/7-turn suite 覆盖直接、礼貌、口语查询，缺失节点，Build-off 读写混合和
  会话纠错；隔离 metadata 副本，真实数据连接只读，不暴露/调用 Apply。
- 首次有效运行 5/6：纠错场景第一轮把不存在的“客户退款单”替换成现有节点并查询；这是
  真实语义错误，不以工具成功掩盖。Supervisor 随后增加 exact name/alias 缺失禁止替代及
  单资源最多一次查询约束。
- 定向纠错复验 1/1，完整复验最终 6/6；每个成功查询恰好 1 QueryReceipt，缺失节点 0 查询，
  纠正后恢复，全部场景无 Graph/Candidate 变化。
- 安全报告 Schema 验证通过，且 `model_content_logged/business_rows_logged/
  runtime_stderr_logged/connection_secrets_logged/apply_exposed_or_called` 均为 false。
- 宿主完整回归 `261 passed, 13 subtests passed in 32.31s`；GraphX `9bea7fe` 已部署到
  8001（PID 3470963），health、20-path OpenAPI 与数据保留检查通过。

限制：6/6 是首轮针对性样本，不代表全部业务表达或数据库故障已覆盖；W-EVAL-003 扩展
timeout、permission、redaction、dialect、多源歧义和更宽 paraphrase。

## 2026-09-01 W-OBS-001 · APPROVED

- 宿主完整回归：`259 passed, 13 subtests passed in 33.20s`。
- 新增 exact Task diagnostic 与 Graph-scoped status/trace index；诊断由持久 Task、Agent、
  allowlisted public event 和 opaque Artifact metadata 重建，不依赖当前 Chat 或活跃 Harness。
- conformance 证明失败 root cause 在重启后仍可检索，私有异常文本不进入响应；JSON Schema、
  OpenAPI 路径、非法状态/查询边界均由服务端约束。
- `AgentActivity` 启动即分配服务端 trace ID；旧空 trace 幂等回填 task ID。部署后两个现有
  Graph 分别检索到 5/3 条近期失败，全部带 trace。
- GraphX `cbcac13` 已部署到 8001（PID 3443710）；health、20-path OpenAPI、2 Graph、
  1 connection、5 Candidate 数据保留检查通过。

限制：早期失败只持久化了 `BUILDER_FAILED/GRAPHX_SUPERVISOR_FAILED` 时，系统不会从已丢弃的
私有 stderr 伪造 tool root cause；新运行按现有结构化 failure receipt 保留安全 cause。

## 2026-09-01 W-QUERY-006 · APPROVED

- 宿主完整回归：`257 passed, 13 subtests passed in 35.67s`；QueryReceipt/Harness 定向复验
  `16 passed`。
- `graph_sql_query` 成功后自动生成 immutable `graphx-query-receipt/v1`，服务端验证精确
  Graph/Revision、可选 Candidate ID/hash、语义节点、producer run、受限脱敏结果和五项网关检查。
- 统一 Agent Task 同时持久化 typed QueryReceipt 与 SupervisorDecision；公开工具回执只含
  opaque artifact ID/hash，不暴露业务行、连接配置或秘密。
- 真实隔离 Candidate Preview 查询通过：`candidate_get → graph_sql_query → test_run`；
  QueryReceipt 与 Candidate/Revision/语义节点/producer/public hash 全部精确一致，Candidate
  保持 `proposed`，未 Apply。
- GraphX `a14a049` 已部署到 8001（PID 3419561）；health、18-path OpenAPI、Bootstrap
  数据保留检查通过（2 Graph、1 connection、5 Candidate、Active Graph 正常）。

残余范围：本轮证明 typed 查询证据和真实受控查询链路，不代表开放式用户表达、歧义澄清和
失败恢复质量已充分覆盖；由 W-EVAL-002 验证。日志跨重启检索和失败聚类由 W-OBS-001 收敛。

## 2026-09-01 W-USABLE-004/005 · APPROVED

- 宿主完整回归：`255 passed, 13 subtests passed in 32.09s`。
- 真实 Candidate Preview：Tester 仅通过 typed catalog 调用
  `candidate_get → graph_sql_query → test_run`；exact Candidate ID/hash 与 connector scope
  均由服务端绑定；确定性 suite passed，隔离 Candidate 保持 `proposed`，未 Apply。
- GX-APP-041：模型查询参数仅含语义 `node_name`；持久化 node ID 不在工具 schema，服务端
  对缺失/重名 fail closed。定向契约 3 passed。
- 稳定性：10/10 独立真实模型会话成功，每轮工具序列均为
  `graph_semantic_context_get → graph_propose_changes`；未加载业务源、未访问数据库、未 Apply。
- 安全日志：上述 live smoke 均未输出模型正文、runtime stderr、连接秘密或业务行。
- 发布：GraphX `5d6afe4` 已部署到 8001（PID 2848959）；health、18-path OpenAPI、统一消息
  入口和 Bootstrap 数据保留检查通过，legacy `/build` 不存在。

残余范围：10/10 属于固定工具协议稳定性，不代表开放式用户表达质量已充分覆盖；下一轮由
W-QUERY-006/W-EVAL-002 建立 tool-first 正式 Revision 查询 Artifact 与多样化评估集。

## 2026-08-28 W-LOCAL-001 / W-CAND-001 验收

> **结论：通过（APPROVED，部署待复验）**。本地 pi-ai 路由可完成真实调用，GraphX 不发送
> `max_tokens`；Candidate 已按 Chat 隔离，并成为一次性审批决策：Apply 或继续发言都会
> 关闭它，终态不会回退到历史卡片，晚到 Reviewer 不会重开。代码已推送为 `280d0ef`；
> 最新 GX-APP-035 后端仍需重新部署后做 UI/API 冒烟。

| 检查项 | 结果 |
|---|---|
| Core/Adapter/Bridge/Executor/Supervisor/Candidate 专项 | `58 passed in 7.20s` |
| Candidate 卡与决策生命周期模块 | `8 passed in 3.28s`；其中继续发言 reject、Apply 关闭旧提案 4 项核心用例 `4 passed` |
| `npm run build` | TypeScript + Vite production build 通过，28 modules transformed |
| JSON/YAML 与 diff | requirements/model/lock JSON、manifest/Cordis YAML、`git diff --check` 通过 |
| 本地模型真实 smoke | 纯 SDK 返回 `LOCAL_OK`；完整 GraphX plugin smoke passed，产生类型化回执 |
| 全量 pytest | 未重跑，不声明结果；TestClient chat-lifecycle 路径仍可在本环境长时间停滞 |

残余风险：最近真实 Builder 构图虽然最终成功并 Apply 到 v2，但两次先行失败及成功轮回执
包含多次 `TOOL_ARGUMENT_SCHEMA`、30 秒 bridge timeout、重复 HGT 校验与非必要 Bash；
本轮没有把该运行时可靠性问题声明为已修复。

## 2026-08-25 W-FIX-002 Candidate 门禁与实时 Harness 步骤验收

> **结论：通过（APPROVED）**。Candidate 在 GraphX/Reviewer 协调完成前不可 Apply；
> Harness 公开通知被实时净化为任务卡步骤，且不暴露私有推理或原始工具 payload；
> `max-tokens` 使用精确终止码，role-completion observation 被约束为立即 typed decision。

| 检查项 | 结果 |
|---|---|
| Adapter/Executor/Activity/DAG/Cancel 专项 | 22 passed，4.54 秒 |
| `npm run build` | TypeScript + Vite production build 通过 |
| 真实 DeepSeek Harness rc6 smoke | Builder/Reviewer/Tester 均 `finish_reason=completed`；新 JSONL 协议兼容 |
| 部署 | `graphx-alpha.service` active；health 通过 |
| 数据保留 | Graph `111` 与 1 个数据连接保留 |

追加复验关闭 BUG-011：新 Builder 未产出 Candidate 时不再显示历史失败候选；UTC
时间正规化后运行时长从 0 秒递增；缺少结果 call ID 时使用待处理调用安全关联公开工具名。
相关前端/Adapter专项 `13 passed in 2.33s`，production build 通过并已重部署。

二次追加复验关闭 BUG-012：真实运行中 Builder Candidate 已成功产生，后置 GraphX 也已
提交 `supervisor_decision`，但 Adapter receipt 枚举漏项导致成功结果被误报协议失败。统一
契约并新增 Supervisor receipt 回归后，Adapter/Harness/DAG 专项 `16 passed in 1.25s`；
8001 已重部署且 health 通过。

全量 TestClient 套件仍复现既有 Starlette/httpx2 路径挂起，因此不声明全量结果。

## 2026-08-25 W-FIX-001 运行时修复验收

> **结论：通过（APPROVED）**。部署服务显式继承代理；Harness 的
> `TRANSPORT` 以 `HARNESS_TRANSPORT` 净化透传；GraphX observation 失败不再伪造
> completed；后置卡片按 parent final 因果排序；取消任务在 Candidate 持久化前执行
> execution-version fence。

| 检查项 | 结果 |
|---|---|
| Harness/Executor/Supervisor/Activity/Cancel 相关专项 | 30 passed，4.98 秒 |
| `npm run build` | TypeScript + Vite production build 通过 |
| 真实 DeepSeek Harness rc6 smoke | `finish_reason=completed`，预期输出哈希匹配 |
| 部署 | `graphx-alpha.service` active；代理变量脱敏核验已配置；health/bootstrap 通过 |
| 数据保留 | Graph `111` 与 1 个数据连接保留 |

全量 TestClient 套件仍在既有 Starlette/httpx2 路径停滞，因此不声明全量结果；这不
改变上述 30 个相关自动化用例和真实 Harness smoke 的通过结论。

## 2026-08-24 第二轮反馈验收 — GX-APP-021..025

> **结论：通过（APPROVED）**。Stop/持久取消与 late-result fence、逐 Agent
> 过程卡与最终气泡顺序、Build Mode 权限式路由、Graph 绑定受控只读查询和前端统一
> endpoint/poll/stop 均通过专项验收。初验发现的通用表规划限制及多表歧义异常
> （BUG-006）已修复并复验关闭。

### 执行证据

| 检查项 | 结果 |
|---|---|
| GX-APP-021..025 + Harness cancel 专项 | `23 passed in 3.64s`，退出码 0；另有 1 条既有 Starlette/httpx deprecation warning |
| `npm run build`（`apps/web`） | TypeScript + Vite 通过；28 modules transformed；1.16 秒；退出码 0 |
| `git diff --check` | 通过，无 whitespace error |
| 全量 `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -m pytest -q` | 运行 3 分钟仅输出 5 个进度点且无后续进展，按约定 Ctrl-C（退出码 130）；不计为通过或失败 |

### 独立审查结果

- GX-APP-022：取消 API 幂等；`execution_version` 与 `cancel_requested_at` 在每个晚到
  写入边界拒绝 stale 结果；取消 Build 不生成 Candidate，正式 Graph/revision 不变；
  Harness 进程按 run ID 注册，取消执行 terminate、宽限后 kill，并在完成/超时/取消后清表。
- GX-APP-021/023：Builder card → Builder final → Reviewer card → Reviewer final 的锚点
  由 `final_message_id` 保持；普通问答为 GraphX card → final。公开事件严格限于
  `thinking_summary/tool_call/tool_result/status`，projection 对 payload 二次白名单，未发现
  CoT、prompt、token、secret、credential、authorization 或 raw tool payload 泄露。
- GX-APP-024：前端统一调用 message routing endpoint；Build Mode on 仅授予 mutation
  权限，信息问答保持 read-only，混合/确认型请求澄清且不建 Candidate，off 时不改图。
- GX-APP-025：查询输入只生成结构化 server-owned plan，不接受模型 raw SQL；从当前
  HGT 动态解析任意绑定表，歧义失败关闭；连接须属于同一 Graph，表/列越权拒绝；
  read-only transaction、statement timeout、row/byte cap、敏感字段 redaction 和净化错误
  均有实现或专项证据。随机销售订单成功路径及第三张任意表规划均已覆盖。

### 残余风险

- 全量套件在本环境 3 分钟无进展，未取得全量通过证据；本结论基于本轮 23 个相关
  自动化用例、静态契约/实现审查、前端生产构建与 diff check。
- 受控 SQL 的真实 PostgreSQL 网络端到端未在本轮测试环境执行；执行边界以 fake
  engine/服务级用例与代码审查验证，部署后仍应对真实绑定数据源做 smoke test。

## 2026-08-24 增量验收 — GX-APP-021

### BUG-005 修复复验

> **结论：通过（APPROVED）**。`AgentActivityCard` 已改为 `useState(false)`，首次
> 渲染保持紧凑；紧凑摘要直接列出任意数量 Agent 的 `display_name` 与六态标签，
> 用户无需展开即可知道各 Agent 状态。`active → terminal` 仅在状态边沿自动折叠，
> 不会在 active 期间覆盖用户主动展开。复验执行 `npm run build`：TypeScript + Vite
> 通过，28 modules transformed，1.14 秒，退出码 0；`git diff --check` 通过。
> BUG-005 已关闭，GX-APP-021 本轮可交付。

> **初验结论（已由上述复验取代）：需修改（CHANGES_REQUESTED）**。后端活动状态机与前端生产构建通过，
> 但活动任务首次渲染时被默认展开，不满足 GX-APP-021“卡片 MUST compact by
> default”的明确要求；见 BUG-005。

### 执行证据

| 检查项 | 结果 |
|---|---|
| `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -m pytest -q tests/conformance/test_agent_activity_card.py` | 5 passed，1.96 秒，退出码 0；另有 1 条既有 Starlette/httpx deprecation warning |
| `npm run build`（`apps/web`） | TypeScript + Vite 通过，退出码 0；28 modules transformed |
| `git diff --check` | 通过，无 whitespace error |
| 既有 TestClient 相关回归组合 | 运行 60 秒无输出，人工中断（退出码 130）；不计为通过或失败 |

### 独立审查结果

- 通过：`TaskActivity` 以 `trigger_message_id` 锚定 user message，React 在该 message
  的 `message-group` 内紧邻插入卡片；后端在阻塞 Harness 前的独立事务提交 Builder
  `running` / Reviewer `queued` 初态。
- 通过：公开模型和前端组件均为任意 Agent 数组；专项测试实际注入并观察 Builder
  与 Tester 同时 `running`。六态类型/合同完整，Builder、Reviewer 成功、Builder
  失败与 Reviewer 失败均闭合；`changes_requested` 正确视为 Reviewer 执行完成。
- 通过：Bootstrap 按所选 `thread_id` 隔离，倒序取最近 20 条后恢复正序；公开 payload
  采用字段白名单；Graph 删除顺序先清 AgentActivity/TaskActivity；Trace ID 仅在对应
  阶段可读后写入。
- 通过：轮询为串行 await 的单飞 Bootstrap，请求间隔 750 ms；Graph/Chat 切换和卸载
  通过 token 取消旧循环，请求序号防止旧 Bootstrap 覆盖新选择，Build resolve/reject
  后执行最终刷新。
- 不通过：`AgentActivityCard` 使用 `useState(active)`，新活动任务 `active=true` 时首次
  渲染即展开详情，与 GX-APP-021“compact by default”冲突；终态自动折叠本身正确。

### 测试质量与残余风险

新增 5 个 service-direct 用例覆盖主状态转换、多 running、失败净化、
`changes_requested` 与空工作台，质量可接受但不足以独立防回归：尚无自动化断言覆盖
前端“紧邻触发消息 / 默认折叠 / 750 ms 单飞与取消”，也未用专项测试直接断言
thread 隔离、最近 20 条和删除后的子表计数。上述后端项本轮以代码审查确认；前端
默认折叠已因此漏测并形成 BUG-005。修复后至少应增加可执行的前端组件/轮询测试，
再将本轮结论改为 APPROVED。

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
