---
title: GraphX 项目当前状态与下一步（STATE · 项目内容）
role: orchestrator(维护)
status: ACTIVE
version: 4.0
updated: 2026-09-02
upstream: [graphx/spec/06-testing-and-handoff.md]
downstream: [任何被要求"继续 graphx 开发"的 agent]
---

# GraphX · 当前状态与下一步（STATE）

> **本文件只放"项目内容"**（我们在哪 + 下一步 + 项目专属约束）。
> **团队能力**（Bootstrap 顺序 / 收尾清单 / 团队级约束 / STATE.md 约定）的单一事实源在
> **`team/handoff.md`**，本文件不重复——只留指针（见文末「续接指针」）。
> 任何 agent（DSH / Claude Code / Cursor / 自研引擎）收到
> **「使用 /home/wangling/develop_team/negentropy 定义的多agent角色，继续 graphx 的开发工作」**
> 时，**先读本文件**，再顺指针读 `team/handoff.md` 按 Bootstrap 顺序接手，**无需额外背景或进度信息**。
> 本文件由编排者（orchestrator）在每轮收尾时更新，是"我们在哪 + 下一步做什么"的权威快照。

## 30 秒速览

| 项 | 值 |
|---|---|
| 项目 | GraphX（Graph-first 可追溯超图工作台），产品版本 **0.5.7** |
| 代码仓库 | `/home/wangling/develop_team/graphx`（分支 `feat/trusted-build-core`，已部署 HEAD `cb18047`） |
| 规范事实源 | `/home/wangling/develop_team/graphx/spec/`（APPROVED，**单一事实源**，覆盖一切历史聊天/原型） |
| 工作流 | `existing-spec`（阶段 1–3 由 `graphx/spec/` 的精确 revision 替代） |
| 团队 | negentropy（8 角色，协议 `v1.1-docs`），定义在 `/home/wangling/develop_team/negentropy` |
| 当前阶段 | **首个完整超图场景已闭环**：销售订单履约追踪已完成资源、构图、关系验证、Review/Test、用户 Apply、重启与查询验收 |
| 测试状态 | 角色隔离/关系计划/目录迁移相关 74+60 项定向测试及新增迁移用例通过；此前基线 **262 passed + 13 subtests**；未伪称新全量通过 |
| 真实运行证据 | Reviewer/Tester 实际工具面无 skill/job/bash；公开消息为类型化短摘要；source_ref 迁移已 Apply，重启后 Revision 5 查询成功 |
| 运行应用 | `cb18047` 已部署到 8001，重启后 PID `1089814`，健康；正式 Active Graph 为 Revision 5 |
| 下一步 | W-POLISH-001/W-META-001 已闭环；选择第二个完整业务场景，验证构图团队的跨场景泛化 |

## 项目批准者

| Principal | 实际负责人/稳定 ID | 说明 |
|---|---|---|
| project-owner | user | 范围、残余风险和发布授权 |
| product-owner | user | GraphX 产品行为与优先级 |
| business-owner | user | 业务语义与材料使用边界 |

> 批准者不可用时保持 BLOCKED 并请求决定；等待时间不自动转换为授权。

## 当前状态（按 `team/workflow.md` 阶段）

| 阶段 | 负责角色 | 状态 | 说明 |
|---|---|---|---|
| 0 立项 | orchestrator | DONE | `00-intake/project-brief.md` APPROVED |
| 1 业务 | business-liaison | SKIPPED（existing-spec） | 替代事实源：`spec/01` 产品范围；revision 跟随当前 graphx WORKTREE |
| 2 需求 | product-manager | SKIPPED（existing-spec） | 替代事实源：`spec/01/09/10/12`；revision 跟随当前 graphx WORKTREE |
| 3 架构 | architect | SKIPPED（existing-spec） | 替代事实源：`spec/02/05/08` + `spec/contracts`；revision 跟随当前 graphx WORKTREE |
| 4 实现 | frontend ∥ backend | **ACTIVE** | 当前主线为完整场景所需资源目录、语义超边和关系验证工具 |
| 5 测试 | test-engineer | **ACTIVE** | 建立“销售订单履约追踪”完整团队 E2E，而非继续扩大孤立查询样本 |
| 6 发布 | devops-engineer | **DONE（当前里程碑）** | `9bea7fe` 已部署，宿主 health/OpenAPI/diagnostics/bootstrap 与数据保留检查通过 |
| 7 复盘 | orchestrator | **DONE** | 2026-08-31 完成项目目标/完成度/不可用断点复盘；用户确认 SQL 验证应前置 |

> 说明：阶段 1–3 按 `existing-spec` 合法裁剪为 `SKIPPED`，由 `graphx/spec/` 的当前 revision 替代
> （`spec/` 是单一事实源）。本工作区只承载团队协作文档（notes/测试三件套/问题登记），不复制规范。

## 下一步动作（权威完整清单在 `graphx/spec/06`「Continue in this order」）

### 2026-09-01 · 语义构图边界重构（已交付）

产品负责人已确认：**模型只看语义层；所有技术 ID、hash、Revision/连接绑定和
并发前提由工具与 Patch Compiler 管理。** HGT Patch 继续作为系统内部正式协议，
但不再作为 Builder 直接填写的参数。

目标链路：

```text
用户业务表述
  → Builder: create/update/connect table semantic operations
  → server-bound Graph/Revision/resource resolver
  → deterministic HGT Patch Compiler
  → Candidate / Review / Test / user Apply
```

首版严格收窄到 `create_table_node`、`update_table_node`、`connect_table_nodes`。
模型只提供节点名称、描述、语义 selector、`connection_name? / schema_name /
table_name` 和 rationale；不得提供 graph/revision/candidate/patch/connection/entity
ID 或 content/precondition hash。连接名称只是人类可读消歧条件，Compiler 根据
Graph-owned catalog 注入真正的 connection binding 和 evidence。

交付结果：

1. **W-SEM-001..003 DONE**：ADR-009、GX-SEM-001..004/GX-APP-038、窄 DTO、
   Resolver/Compiler 和 `graph_propose_changes` 已在 GraphX `6603899` 交付；Builder
   模型目录只剩语义 Context 与语义变更两个工具，raw Patch 保留为系统内部协议。
2. **W-SEM-004 DONE**：脱敏 root-cause 链已持久化；真实 update Candidate 在两次工具
   调用内成功。真实运行又发现 Supervisor 会复制坏 artifact hash，已由 `829ddd5`
   改为服务端绑定协调身份，第二轮 Reviewer→Tester→GraphX finish 完整通过。
3. **W-USABLE-004 DONE**：ADR-010/PD-042 取代“保留 Bash”的旧决定；产品
   Cordis composition 移除 Bash/subprocess/local-file，RoleProfile `native_tools=()`；Tester
   获得 exact Candidate ID/hash 的受控 SQL binding，服务端重算 artifact hash、应用 persisted
   Patch 得到 Preview 并复验 connector scope。真实 Tester 已在隔离元数据、未 Apply Candidate
   Preview 上完成受控 count 查询与 `test_run`，全程无业务行/连接秘密输出。

### 2026-09-01 · 当前执行切片

1. **W-USABLE-004a DONE**：真实 Candidate Preview `graph_sql_query` 使用 exact hash binding，
   工具序列 `candidate_get→graph_sql_query→test_run`，Candidate 最终仍为 `proposed`。
2. **W-TEST-DEBT-001 DONE**：8 个旧入口测试已迁移到统一 Chat message + structured
   mention/Build capability；删除死 Alpha `BuildRequest`，完整回归 252 passed + 13 subtests。
   迁移还修复了独立角色同步失败响应缺少净化 `terminal_code`（GX-APP-040）。
3. **W-USABLE-005 DONE**：10/10 真实模型轮次均只调用
   `graph_semantic_context_get→graph_propose_changes`，精确响应成功；无业务源、数据库或 Apply。
4. **GX-APP-041 DONE**：`graph_sql_query` 的模型参数由 `node_id` 改为 `node_name`；服务端在
   exact Revision/Preview 内按名称/声明 alias 唯一解析，缺失或重名时 fail closed。
5. **GX-QUERY-006 DONE**：成功的 `graph_sql_query` 自动生成 immutable、hash-bound
   `graphx-query-receipt/v1`；包含语义请求、精确 Revision/Candidate、受限脱敏结果、五项网关检查
   与 producer run。统一 Agent Task 同时持久化 QueryReceipt 和 SupervisorDecision；旧
   prose detector→QuestionRun 固定管线已从产品入口移除，不恢复关键词路由。
6. **W-OBS-001 DONE**：精确 Task 诊断和 Graph 范围 status/trace 索引从持久
   Task/Agent/public event/Artifact 事实重建；不暴露 prompt、业务行、连接材料、raw stderr 或
   hidden reasoning。旧空 trace 已安全回填 task ID；真实重启后两个 Graph 的近期失败均可查。
7. **W-EVAL-002 DONE**：versioned 6-case/7-turn 真实查询评测覆盖直接/礼貌/口语查询、
   缺失节点、Build-off 读写混合和会话纠错。首轮发现缺失节点被替换为现有节点；Supervisor
   收紧为显式资源缺失时禁止 nearest-node fallback、单资源最多一次查询。定向与完整复验最终
   6/6 通过，且无 Apply、Graph/Candidate 变更、业务行/模型正文/raw stderr/秘密日志。
8. **方向修正（C-004）**：W-DIAG-UI-001/W-EVAL-003 不作为下一阶段主线。产品负责人要求
   优先让完整超图构建 team 变得丝滑，并以一个真实完整场景驱动提示词和工具改进。

### 2026-09-01 · 完整场景：销售订单履约追踪

目标不是再生成一张两节点图，而是构建可执行的五节点履约超图：

```text
销售订单 sales_order
  → BPM 发货申请 shipping_applications
  → SAP 发货申请 sap_shipping_applications
  → SAP 销售出库 financial_sales_outbound
  → WMS 销售出库 wms_outbound_records
```

一条“订单履约追踪”语义超边同时表达：订单行、发货申请、SAP 同步、SAP/WMS 实际出库；
关键关联采用 `sales_order_code/config_material_code` 与
`application_code=delivery_request_code`；数量统一遵守蓝字 `+ABS`、红字 `-ABS`，且不得把
SAP 发货申请与实际销售出库混为同一概念。

当前事实与缺口：

1. 数据库 information_schema 已确认 5 张表真实存在；但 Graph-owned SourceTable 目录只登记
   `sales_order`、`shipping_applications`，因为 `ALLOWED_TABLES` 仍是早期两表切片。
2. 当前正式 Revision 只有两张表节点、零语义超边；语义工具只支持 create/update table 与
   connect table，Builder 无法创建 `HGTHyperedge`。
3. `graph_sql_query` 只能验证单节点读，不能验证 join key 是否在真实数据上连通；Tester 只能
   证明“表能读”，不能证明“关系可执行”。
4. 因此实施顺序必须是：目录补齐 → semantic hyperedge Compiler → relation/join check →
   Builder/Reviewer/Tester prompts → 隔离真实完整 E2E → 用户确认后 Apply。
5. **W-FLOW-002 DONE**：GraphX `369c7ff` 将五张真实表纳入 bounded catalog；发现操作读取
   明确选择的 GraphConnection 私有配置，不再读取 process-wide DSN 后重新贴连接标签；每项
   保留 connection ID/source provenance 与真实列结构。全量 262 passed + 13 subtests；部署后
   正式 Active Graph 目录已包含全部五表，Revision/Candidate 数量均未变化。
6. **W-FLOW-003 DONE**：GraphX `4415c30` 扩展 `semantic-change/v1-draft`，Builder 可用语义
   selector、成员业务角色和规则 create/update semantic hyperedge；Compiler 负责 member IDs、超边 ID、
   evidence/hash/precondition 与同提案依赖。真实隔离 Builder 用一次 `graph_propose_changes` 生成五节点、
   四关系和“订单履约追踪”五成员超边 Candidate，未访问数据库/私有文档且未 Apply。41 项定向/规范测试通过；
   全量 suite 另在既有 `test_non_business_question_uses_agent` 处等待，无本切片失败栈，需独立定位。
7. **W-FLOW-004 DONE**：GraphX `5791c04` 增加 `graph_relation_check` 和
   `graphx-relation-check-receipt/v1`。模型只提交两个语义节点名和 1–4 个字段对；服务端在精确
   Revision/Candidate Preview 上解析节点/字段/连接并执行同库只读 bounded join，公开结果只有
   `match_count/capped`。真实隔离 Tester 对 `sales-order → shipment-application` 的
   `sales_order_code` 得到 20/capped，六项确定性网关检查及 test_run 均通过，Candidate 未 Apply。
8. **W-FLOW-005 DONE**：GraphX `15878ba` 增加 checked-in
   `graphx-semantic-scenario/v1`、资源完整性门控和 `update_table_relation`。Builder 能按资源复用/重命名
   两个旧节点、纠正反向旧边并只创建三项缺失资源；Reviewer/Tester 共享相同五表/四关系/超边/规则验收。
   真实隔离 team runner 一次用户目标生成 10-operation Candidate，最终 5 节点、4 关系、1 五成员超边；
   Reviewer passed，Tester 四个 relation receipt 均 20/capped 且 TestReport passed，未 Apply。
9. **W-FLOW-006 正式团队链已通过，等待用户 Apply**：正式 Chat
   `thread-1960563b5c264656bda7be3ac593e4ff` 从一次 `@GraphX` 目标动态完成
   GraphX→Builder→Reviewer→Tester→GraphX。Candidate
   `candidate:agent-task-75bfc1872f41407eb273c5ca28632f8a` 的 Preview 为 5 节点、4 关系、1 超边；
   Reviewer passed；Tester 四条 bounded join 均为 20/capped，权威 TestReport 已持久化并 passed；
   Candidate 状态 ready，正式 Revision 保持 3。运行中发现并修复两个控制面缺陷：`3d39eeb` 保证每个
   Supervisor run 只有一个权威决策；`bd2c53f` 将 Candidate no-change guard 收紧到同一 root task
   lineage，避免历史等价 Candidate 阻断新目标。当前仅等待 product-owner 的逐次 Apply 授权。
10. **W-FLOW-006 DONE**：product-owner 已确认 Apply，Candidate 状态为 `applied`，正式 Graph 升为
    Revision 4（`revision-a16a8569e53943ecb291ea1704dd268b`）。服务重启到 PID 3917230 后仍保持
    5 节点、4 关系、1 超边；Apply 后只读验收任务通过语义节点 `sales-order` 在精确 Revision 4 上
    返回 1 条有界结果，五项 Query Gateway 检查完整，未绑定 Candidate、未回退默认连接。

Remove、API/document 和 proposal-local alias 仍不进入当前语义契约，后续按真实需求扩展 schema。

### 2026-08-31 · 可用性收敛里程碑

产品近期唯一主旅程收缩为：

```text
建立并验证数据连接
  → Builder 产生显式绑定 connection_id/schema/table 的 Candidate
  → 对 Candidate preview 和 Apply 后 Revision 执行同一受控查询验证
  → Reviewer/TestReport 绑定精确 Candidate hash
  → 用户 Apply
  → 重启后仍可查询
```

产品决策：**SQL 工具是节点可用性验证的基础设施，不是后续增强。**
`table` 节点只有在当前 Revision 中显式绑定同 Graph、`connected`、
`database` 连接，并能通过服务端限权查询时，才能被宣称为可用节点。

多数据连接是正常产品场景：连接及其资源目录归 Graph 所有，是构建输入；
SourceTable/API resource 必须保留 `connection_id`。Builder 根据目录来源创建节点，
节点再记录构建后的可执行来源。只有目录缺失归属、来源冲突或无法唯一匹配时
才请求澄清；不能把常规逐节点选连接的负担推给用户，也禁止按创建时间、
所谓“默认连接”或任意顺序猜测。
被正式 Revision 或开放 Candidate 引用的连接禁止直接删除，必须先经 Candidate
迁移或解绑引用节点。

实施顺序：

1. **W-USABLE-001 · 绑定不变量收口**：审查、补齐并提交当前 GX-APP-036/GX-CANVAS-002 未提交工作；统一 Bundle/Patch/应用层的连接字段契约。
2. **W-USABLE-002 · Builder Patch 可构造性**：实体 hash、完整 Schema、脱敏字段错误和重试/预算门禁已提供，但真实运行证明 raw Patch 本身仍是错误抽象；由 W-SEM 系列取代其“模型手写 Patch”目标。
3. **W-USABLE-003 · Graph 资源目录与 Query 验证前置**：建立 GraphConnection→SourceTable/API resource 目录归属，Builder 依目录构图并让节点保留来源绑定，目录歧义才澄清；拒绝删除仍被 Revision/Candidate 引用的连接；为 GraphX、Builder、Reviewer、Tester 按最小权限装配同一 `graph_sql_query` backend；支持 Candidate preview 和正式 Revision 绑定；保持结构化 SELECT-only、字段允许列表、超时、行/字节上限和脱敏。
4. **W-USABLE-004 · 固定 E2E 门禁**：以销售订单+发货申请两表建立自动 smoke，验收 Candidate 查询、Review/Test、Apply、Revision 查询和重启持久性；解决 TestClient/全量测试挂起。
5. **W-USABLE-005 · 部署与真实试用**：仅在 001–004 通过后发布；连续执行 10 次主旅程无人工修补，记录脱敏 trace 和成功率。

暂停：新 Agent 角色、Supervisor 扩展、组织库、Canvas 新交互、新 HGT 节点类型、图/向量数据库选型。

### 2026-08-28 · W-LOCAL-001 / W-CAND-001 本地模型与 Candidate 决策生命周期

GraphX 已切换到内网 OpenAI-compatible `/models/DeepSeek-V4-Flash-0731`，不发送
`max_tokens`。固定 rc6 SDK 未打包桌面端 `settings-file` / `credentials-local` 插件，原装
挂载方案会在 Cordis 初始化阶段超时；当前通过 bundled `llm-pi-ai` 直接声明 `local` route，
worker 仅注入无鉴权端点所需的固定非敏感占位值。纯 SDK 返回 `LOCAL_OK`，完整 GraphX
plugin smoke 完成并产生类型化工具回执；架构决策记录在 GraphX `ADR-008`。

Candidate 投影先以 GX-APP-034 绑定 originating `BuildRun.thread_id`，杜绝跨 Chat 卡片泄漏；
GX-APP-035 进一步把审批卡定义为一次性待处理决策：Apply 后关闭，同一 Chat 未 Apply 而
继续发送消息时，服务端在接收新 turn 的事务中把所有开放 Candidate 标为 `rejected`；前端
只读取最新 Candidate，不再回退到旧 `proposed`，晚到 Reviewer 也不能重开终态。实现、
规范、测试已提交并推送为 GraphX `280d0ef`。

最近真实构图最终成功生成 2 节点、45 字段、1 条边并 Apply 到 v2，但此前两次 Builder
失败的回执显示本地模型多次产生 `TOOL_ARGUMENT_SCHEMA`，并触发多次精确 30 秒 bridge
timeout；成功轮仍有重复校验和一次 120 秒非必要 Bash。该效率/可靠性问题尚未修复，列为
下一轮运行时收敛项。

### 2026-08-25 · W-FIX-002 Candidate 时序与真实执行步骤

复现确认 Builder 已提交 Candidate 后，GraphX observation 仍运行时前端提前显示了可 Apply
按钮；随后 observation 因 `max-tokens` 被泛化为 `HARNESS_FINISH_UNSUPPORTED`。同时 worker
只在结束时返回汇总，SDK 的实时 notification 未进入任务卡。现已交付：Builder Candidate
先持久化为 `proposed`；必须等待任务谱系收敛且同哈希 Reviewer 报告 passed 才启用 Apply；
worker 使用公开 `on_notification` 回调流式输出版本化净化 JSONL，Adapter 校验后实时持久化
`thinking_summary/tool_call/tool_result`；展开卡片独立滚动；工具参数、原始结果、assistant
chunk 和隐藏推理全部丢弃；GraphX role-completion prompt 要求立即提交一次 typed decision，
预算增至 4096，`max-tokens` 映射为 `HARNESS_MAX_TOKENS`。8001 已重部署并保留现有数据。
后续试用发现新 Builder 启动时全局 Candidate 区仍读取上一轮失败候选，且 SQLite UTC
naive 时间被浏览器按本地时间计算为 480 分钟；现已追加轮次隔离和 UTC 正规化修复并部署。
真实试用进一步确认 Builder 已成功提交 Candidate，而后置 GraphX 已调用
`supervisor_decide` 生成 typed decision；Adapter 的 artifact receipt 枚举却漏掉
`supervisor_decision`，导致完成结果在协议校验阶段被误报为 `WORKER_PROTOCOL_SCHEMA`。
现已统一 Bridge/Adapter 契约、增加 Supervisor receipt 回归并再次部署 8001。

### 2026-08-25 · W-FIX-001 Builder 运行时与卡片因果顺序修复

干净 Graph/重连数据源后复现证明旧消息不是原因。Harness 私有会话显示 Builder 与
后置 GraphX 均因 DeepSeek `TRANSPORT` 在重试后失败；手工创建的 systemd transient
unit 未携带代理环境。现已交付：部署脚本显式传递 allowlisted GraphX/proxy 环境并使用
持久 user service；worker/Adapter 将 `TRANSPORT` 净化为 `HARNESS_TRANSPORT`；GraphX
observation 失败不再伪造成静默 completed；前端将 observation 锚定到父角色 final 后；
统一入口取消时在 Candidate 持久化前执行 execution-version fence。部署后真实 Harness
rc6 冒烟 `completed`，服务保留 Graph `111` 和 1 个连接。

### 2026-08-25 · 当前最高优先级：Supervisor + 动态多 Agent 重构

用户已批准以下不可变边界：

1. GraphX 是无 mention 时的唯一默认入口；不使用关键词/意图枚举预路由到固定 pipeline。
2. Build Mode 仅是能力授权：关闭时只能激活 GraphX，不能创建其他角色会话、Candidate 或修改 Graph；开启时才允许 GraphX/用户激活 Builder、Reviewer、Tester。
3. 用户可在群聊中 `@GraphX`、`@Builder`、`@Reviewer`、`@Tester`；指定角色完成后触发一次 GraphX Supervisor turn，由 GraphX 决定静默结束、汇总、澄清或继续委派。
4. Builder、Reviewer、Tester 是目的和工具权限不同的独立 Agent，不是固定阶段；允许 Builder↔Reviewer 返工循环、Tester 先审计当前 Graph 后触发 Builder、并行任务等动态任务图。
5. 上下文采用 Harness/Codex 风格的共享任务上下文 + 独立角色 session/workspace/checkpoint；角色间只共享公开消息、受控 Context Pack 与 typed artifact，不共享隐藏推理或私有 session。
6. SQL/Graph/File/外部系统能力全部作为 Harness plugin 或 MCP 风格工具进入统一 Tool Gateway；删除主链路上的 SQL 问句识别和关键词 route。
7. Apply 永远由用户明确确认；动态 Agent 也不得直接写正式 Graph revision。

上一轮 W-FBK 的 Task/Event、Stop、execution-version fence、typed artifacts、Harness plugin
和 Graph-bound SQL 安全执行层保留为基础设施；关键词分类主链、固定 route enum、公开旧
`/build` API 与固定 Builder→Python Reviewer 编排已经由 W-SUP-001..008 替换。

### 2026-08-24 · 当前最高优先级：任务运行体验第二轮

1. **任务停止**：运行中提供 Stop；服务端持久化取消请求并尽快终止/跳过尚未完成阶段，Candidate/正式 Graph 不得因取消而写入。
2. **逐 Agent 过程卡**：Builder、Reviewer、GraphX 各自在自己的消息位置下展示安全公开的工作摘要、工具调用名/状态与净化回执；最终结论仍用普通气泡。不得暴露隐藏推理链、系统 prompt、token、secret 或原始工具 payload。
3. **统一意图路由**：Build Mode 表示允许图变更，不表示每条消息强制 Build；图上问答在任一模式均可进入只读 GraphX，只有明确变更意图才进入 Builder/Reviewer。
4. **受控 SQL 查询**：普通问答支持对 Graph 已绑定数据源/表执行只读、限时、限行 SQL，并把净化后的工具过程呈现在 GraphX 过程卡；不得允许任意数据源、写 SQL 或秘密外泄。
5. **顺序**：产品/架构契约 → 取消与运行事件 → 意图路由 → SQL 工具 → 前端整合 → 独立回归；发布仍需单独 `publish` 授权。

交付状态：上述 1–4 已实现并包含在 graphx `280d0ef`；GX-APP-021..025 登记为
`implemented`。独立测试专项 23 passed、前端生产构建通过，BUG-006（查询表硬编码及
歧义空计划运行时错误）已修复。全量 pytest 因当前环境 3 分钟仅推进 5 项而中止，
不计通过或失败。该轮曾按用户明确授权部署到 8001，健康检查、bootstrap、取消/消息
OpenAPI 路由和前端资源冒烟通过；最新部署状态以本页 30 秒速览为准。

1. **（当前门禁）** 实现 out-of-sandbox credential broker（或等价 UID/mount 隔离），证明真实 provider Token 对 Agent/Bash 不可读，关闭 Q-002/OQ-016。
   - 角色：devops-engineer（隔离实现）+ architect（安全边界确认）+ test-engineer（对抗验证）。
   - 禁止：不得以 0600 文件、目录约定或同 UID 子进程作为凭据边界；门禁关闭前不得装载私有语料到真实角色会话。
2. **门禁关闭后**用私有语料跑 Builder 提议 table-table 关系与语义超边；**不直接抄历史 demo 对象**。
   - 角色：backend-engineer（驱动 Builder 执行）+ test-engineer（验证）。
   - 私有语料（Git 外）：`/home/wangling/develop_team/graph_poc_doc/`
     （`sql_templates/` 13 个 SQL 模板、`hyperedges/` 业务证据、`selected_30_questions.csv`、
     `connection_info.md.txt` 为**排除项**，内容不得读/哈希/入 manifest）。
   - 业务问题盲评套件：`/home/wangling/develop_team/runtime/graphx-eval/`（Git 外）。
3. 独立 Reviewer 检查 join key、数量/状态语义、红蓝记账规则、证据覆盖、缺失员工源。
4. 确定性静态套件绑到 `test_run` **已交付**（GX-TEST-001，`db3d118`）；剩余：用已绑定套件**执行 30 条盲评用例**并**冻结 Tester 输出**后评估者才读 golden（运行时操作，需访问 Git 外私有 question suite，不读 golden）。
5. 通过原生插件提交真实 ReviewReport / TestReport，冻结其脱敏验证 trace。
6. 加 SELECT-only 数据库工具，对 golden 标签做执行验证。
7. 用业务材料验证可运行工作台旅程，按用户反馈细化 graph/file/chat/merge 行为。
8. 用原生 Harness 角色会话替换轻量 Build 执行器（保持 Candidate Apply 用户可控）。
9. 把应用投影变更迁移到可执行 HGT Patch，实现规范持久 Graph store、授权、审批、outbox、原子 Apply。
10. 组织库后续：只读"从组织库添加"端点、可选推送去重、Postgres `org_library_graphs` 迁移。

## 项目专属约束（只列 graphx 特有的；团队级约束见 `team/handoff.md` §4）

- **uv 环境**：依赖 `uv sync` 管理；**必须带 `UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv`**
  （系统 uv 缓存 `/home/wangling/.cache/uv` 只读，不带会报 Read-only file system）。
- **变更协议**（graphx `AGENTS.md`）：任何行为修改必须**同一变更**内更新
  ① `spec/conformance/requirements.json` 稳定需求 ID ② 规范 ③ 契约/schema（若 wire 变）
  ④ 合规/单测 ⑤ `spec/manifest.yaml`（破坏性决策加 ADR）⑥ `spec/06` 交接状态。
- **不重新设计产品形态**：Graph 是一级对象；Build Mode 是用户与 Builder/Reviewer/Tester 的简单群聊；
  多 Agent 内部流程**不需要**复杂呈现（无独立流水线/Agent 团队/测试中心 UI）。
- **不可协商工程铁律**（graphx `AGENTS.md`）：Agent 不得直接写正式 Graph revision；不得把模型最终文本
  解析成 Candidate/ReviewReport/TestReport；Apply 永不作为 Agent 工具；System Graph 任何接口都不得变更成功；
  不得原地改 Candidate/GraphRevision 内容；mock 运行时必须确定性且无 LLM key/网络可用。
- **范围**：所有工作材料只放在 `/home/wangling/develop_team` 下；不加载私有/不可信源到真实角色会话
  （凭据隔离是前置条件，见 `spec/07` OQ-016）。

> 团队级约束（机密不得打印/入 Git/入 Graph 数据、动手前 `git status` 不覆盖未提交修改等）
> 见 `team/handoff.md` §4，对所有项目通用，此处不重复。

## 本轮已交付（阶段 4–5，GX-APP-012/013/014）

### 2026-08-24 · 连续 UI 反馈轮（GX-APP-019/020 + 栏交互）

- `0e41859`：重新部署/清理脚本 fail-closed，精确停止 8001 监听进程并验证 DELETE 路由。
- `7868da4` + `404efc7`：首条 query 生成 Chat 标题，历史 `新 Chat` 启动回填；输入框附件进入当前 Chat myspace。
- `ef3541e`：Graphs/Chats 收起交互统一，收起后整条竖栏是唯一展开区域。
- `568e63d`：附件选择器支持一次多选，批量上传后刷新 myspace 并预览最后成功文件。
- 以上均已推送 `origin/feat/trusted-build-core`；各轮 scoped pytest 与 TypeScript/Vite build 通过，未重跑全量 baseline。

### 2026-08-21 · GX-INGEST-006

- Builder input plan 只包含 table-only base Bundle、精确绑定的 SQL templates 和 business Markdown evidence；排除历史脚本、问题集、secret/cache 与预置 relation/hyperedge。
- 私有 Git 外产物使用原子 `0600` 写入；CLI/stdout 与 Git 文档不输出私有 hash。
- test-engineer 回归 **30 passed**，BUG-001–004 全部 `REGRESSED`，GX-INGEST-006 结论“可发布”。
- 未启动真实 Harness，未读 golden / `connection_info.md.txt` 正文，未提交 Candidate，未改变 Graph revision。

### 2026-08-21 · GX-TEST-001（确定性静态套件绑定 `test_run`）

- 新增 `graphx_core/static_suite.py`：纯函数确定性静态套件（`candidate_patch_applicable` → `bundle_valid` → 每个被认领 intent 的 `required_tables_bound:<intent>`），无 SQL/LLM/网络/DB/私有 golden。
- `test_run` 现在执行套件并注册 typed `TestReportArtifact`（`artifact_kind="test"`）；被认领 intent 由服务端绑定（`question_intents`），模型不可选；fail-closed 保持（无候选 → `CANDIDATE_NOT_BOUND`，二次提交 → `ARTIFACT_ALREADY_SUBMITTED`，非 Tester → `TOOL_ACCESS_DENIED`）。
- `question_executor.py` 改为从 core 导入共享 intent→table→source-ref 映射（单一事实源，行为不变）。
- 规范同步：GX-TEST-001 入 `spec/03`+`spec/12`、`requirements.json` implemented、`manifest.yaml` 标志、`spec/06` delivered/continue。
- 合规测试 `tests/conformance/test_static_suite.py`（6 条，全合成数据）；全量 **150 passed + 12 subtests**。
- 未读 golden / 私有语料，未启动真实 Harness，未改变 Graph revision。30 条盲评运行时执行 + 输出冻结仍待做。

### 2026-08-21 · 用户反馈修复轮（GX-APP-015/016/017/018）

针对用户 5 条体验反馈，新增 4 条需求并全链路交付（规范/契约/测试/前后端）：

- **GX-APP-015 Chat 生命周期门禁**：Chat 未使用（无用户消息）时禁止新建；`bootstrap.chats[]` 暴露 `unused`；`POST /graphs/{id}/chats` 已有未使用 Chat 时返回 409 `CHAT_ALREADY_UNUSED`；前端禁用"新建对话"并提示。
- **GX-APP-016 多轮 Build**：非空 Graph 的后续 Build 轮次被接受——Builder 经类型化工具网关设计 HGT Patch 并提交，服务端读回 Candidate、重校验 base 绑定与结构后 Review；确定性模式后续轮次 fail-closed（409 `BUILD_REQUIRES_HARNESS`）。
- **GX-APP-017 非 Build 真实智能体对话**：非业务问题由只读 Builder 角色 Harness 会话基于当前 Graph + 近期对话回答；Agent 不提交 Candidate、不改 Graph；Harness 关闭/失败回退确定性上下文回复（mock 运行时保持无 LLM key/网络可用）。
- **GX-APP-018 空工作台 bootstrap**：零 Graph 时 `bootstrap` 返回 200 空投影（`active_graph: null`、`thread: null`、空列表）而非 404，前端提供"创建第一个 Graph"。
- 规范同步：4 条需求入 `spec/03`+`spec/11`+`spec/06`、`requirements.json` implemented、`manifest.yaml` 4 个新标志、API 契约文档（bootstrap `unused`/空态、Create Chat 409、Build 多轮、普通问答 agent-chat）。
- 合规测试 4 条（`test_chat_lifecycle`/`test_multi_round_build`/`test_agent_chat`/`test_empty_workbench`）；全量 **154 passed + 12 subtests**，无新缺陷。
- 前端：`App.tsx`/`api.ts`/`styles.css`（禁建+提示、空工作台状态、删除失败 toast 持久化、可空性守卫）；`tsc -b`+`vite build` 零错误。
- 部署：`scripts/redeploy_alpha.sh`（保留原进程环境重启 + 可选 `--clear-graphs`）；已在 8002 临时实例验证 5 条行为全过；**待用户在宿主机执行**。
- 未读 golden / 私有语料，未改变 Graph revision；真实 provider 的 agent-chat / 多轮 design Build 为后续端到端验证项。

| 角色 | 产出 | 状态 |
|---|---|---|
| backend-engineer | `04-implementation/backend-notes.md`（删除 + 推送 + `bootstrap.org_library`） | APPROVED |
| frontend-engineer | `04-implementation/frontend-notes.md`（菜单动作 + Add 弹窗 + 画布合规测试） | APPROVED |
| test-engineer | `05-testing/{test-plan,defect-log,test-report}.md`（9 条合规用例，结论**可发布**） | APPROVED |
| orchestrator | `open-questions.md`（Q-001 已 RESOLVED：删除 `confirmed` 缺失/非 true 一律 409） | — |

对应 graphx 提交（`feat/trusted-build-core`，已推送）：
- GX-APP-012/013/014：`c84cef6` 后端 / `7a7741e` 前端+画布 / `00b95c9` 合规测试 / `475bb87` 规范+交接 / `b1a542f` manifest 日期同步。
- GX-INGEST-006：`cf7f9e0` Builder 输入计划（编排者收尾提交）。
- 私有输出加固（原 W-LEGACY-001 受保护修改）：`1e53457`（原任务落库）。
- GX-TEST-001：`db3d118` 确定性静态套件绑定 `test_run`。
- 用户反馈修复轮（GX-APP-015/016/017/018）：`f2de58f` 后端+前端+规范+合规测试+redeploy 脚本（已推送）。

## 已知遗留（非阻塞，详见 `05-testing/test-report.md` 第 4 节）

- Postgres 需补 `org_library_graphs` 建表迁移（SQLite 由 `create_all` 自动建表）。
- 组织库无 Add/删除/更新端点（Add 弹窗仅只读展示）；重复推送不去重。
- 画布合规测试为源码级断言（锁定渲染形态不回退），非 DOM 级视觉验证。
- 推送后本地副本归属为产品决策（`spec/07` OQ-017，默认保持 `Mine · editable`）。
- 前端 `pushGraph`/`send` 失败路径的 toast 同样会被后续 `refresh()` 清除（与本轮已修复的 `deleteGraph` 同型），留作后续项。
- 本地模型已可真实调用，但复杂 Builder 工具参数仍会出现 `TOOL_ARGUMENT_SCHEMA` 与
  30 秒 bridge timeout；需要完整工具 JSON Schema、运行时禁用非 GraphX 工具和更真实的
  公开错误投影。
- GraphX `280d0ef` 已推送；GX-APP-035 的最新后端行为尚待重启 8001 后验证。

## 续接指针

- **Bootstrap 顺序 / 收尾清单 / 团队级约束 / STATE.md 约定**：见 `team/handoff.md`（团队能力单一事实源）。
- **工作认领 / lease / 写入范围**：见 `projects/graphx/WORKBOARD.md`；开始下一项写任务前先认领。
- **本项目基线命令**：`cd /home/wangling/develop_team/graphx && UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest -q`。最近验证为 `280d0ef` 的 58 个核心专项、8 个 Candidate 卡专项与前端 production build；未重跑全量 baseline。
