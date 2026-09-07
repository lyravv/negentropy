---
title: 未决问题与变更请求
role: orchestrator(维护) / 全员(提出)
status: DRAFT
version: 0.8
updated: 2026-09-07
upstream: []
downstream: [全员]
---

# 未决问题与变更请求（Open Questions & Change Requests）

> 项目工作区根目录的**全局**问题/变更登记簿。
> - 问题编号 `Q-xxx`，变更请求编号 `C-xxx`。
> - 任何角色可提出；“等待谁”负责回答，提出者或 test-engineer 验证落地后关闭。
> - 阻塞性问题会让相关文档进入 `BLOCKED`。

## 未决问题（Questions）
| 编号 | 提出角色 | 问题 | 等待谁 | 状态 | 决定来源 | 验证者 | 解决记录 |
|------|---------|------|--------|------|---------|-------|---------|
| Q-001 | test-engineer | GX-APP-012 删除端点 `confirmed` 缺失时的状态码：契约（spec/11 + 任务后端契约）写"confirmed 非 true → 409 DELETE_CONFIRMATION_REQUIRED"，但实现把 `confirmed` 设为必填 query 参数，缺失时 FastAPI 返回 **422**（仅 `confirmed=false` 才 409）。核心行为（未确认即拒绝、Graph 保留）一致，仅缺失分支的状态码/错误码不同。请裁定缺失分支应为 409 还是 422，以对齐契约/实现/测试。非阻塞。 | architect | RESOLVED | orchestrator（legacy，治理矩阵建立前） | test-engineer（实现与测试已落地） | 2026-08-20：缺失或非 true 一律 409 `DELETE_CONFIRMATION_REQUIRED`。`api.py`、合规测试和 backend-notes 已同步。 |
| Q-002 | backend-engineer | OQ-016 阻塞私有 corpus 的真实 Builder 执行：当前 DeepSeek Harness worker 与 bundled Bash 同 UID，provider Token 仍映射进 worker 环境，无法证明 Agent 不可读 Token。已完成 GX-INGEST-006 的 hash-bound 最小权限 Builder input plan，并在 Git 外对当前 corpus 生成 13 个 table source + 23 个 business-document evidence 的计划；该计划不构成真实会话授权。需要实现并验证 out-of-sandbox credential broker（或等价 UID/mount 隔离），且证明真实 Token 对 Agent/Bash 不可读后，才能装载私有语料。 | devops-engineer | OPEN | | | 阻塞真实 Builder/Reviewer 会话；不阻塞确定性输入准备。不得以路径权限或 0600 文件冒充安全边界。 |
| Q-003 | test-engineer | 已被当前 Revision 或开放 Candidate 的 `extensions.connection_id` 引用的 GraphConnection 目前仍可直接删除，会让正式节点立即变为不可查询。应拒绝删除，还是生成受控解绑 Candidate？ | product-owner + architect | RESOLVED | product-owner（user） | test-engineer（实现后验证） | 2026-08-31：被正式 Revision 或开放 Candidate 引用的连接禁止直接删除；必须先通过 Candidate 迁移或解绑引用节点。实现与 E2E 验证纳入 W-USABLE-003/004。 |
| Q-004 | test-engineer | 首轮 deterministic Build 在同 Graph 有多个 connected database 时当前选最早连接，而 SourceTable 没有 GraphConnection 归属；是否要求用户显式选择连接，并建立 SourceTable→Connection 映射？ | product-owner + architect | RESOLVED | product-owner（user） | test-engineer（实现后验证） | 2026-08-31 修正：连接及资源目录是 Graph 的构建输入；SourceTable/API resource 必须保留 connection_id，Builder 据此构图，节点记录构建后的可执行来源。只有目录来源不唯一或冲突时才澄清；不得要求用户常规逐节点点名连接，也不得按创建时间/默认连接猜测。实现纳入 W-USABLE-003。 |
| Q-005 | orchestrator（基于 W001F 使用反馈） | Workspace Resource Center 的 `New resource` 目前只能创建 `database` / `api`（后端 `CreateWorkspaceResourceRequest.kind: Literal["database","api"]`）；`document` / `ontology` 只能作为部署托管（Deployment 注册表 / `managed=True`）资源进入，用户无法自行添加。用户希望知道：用户侧 Document/Ontology 导入范围？ | product-owner + architect | OPEN | | | 已登记为 W-GENERIC-SEM-001G（前端 type 扩到 4 类 + 后端放开 kind + doc_execute/ontology_execute 适配；认证 broker 仍属后续）。ADR-021 原文：user-owned Document/Ontology 导入是 later adapter。 |

## 变更请求（Change Requests）
| 编号 | 提出角色 | 目标事实 | 批准者 | 变更内容 | 影响评估 | 状态 | 实施证据 |
|------|---------|---------|---------|---------|---------|------|---------|
| C-001 | product-manager(另一 agent 提出) | spec/01,05,07 + decisions | product-owner（user） | 可验证的自定义模型供应商：DeepSeek 保持默认，允许运营者显式选择经无业务数据探测通过的内网 OpenAI-compatible qwen3.6-27b 备选（US-001，9 条 AC）。与 Phase 1 窄冲突（model routing 原为非范围）。 | 产品负责人 2026-08-21 决定砍掉；DeepSeek 维持唯一绑定。 | REJECTED | US-001 已删除；如未来重启需重新立项。 |
| C-002 | orchestrator（基于用户复盘） | spec/01,02,03,06,11,12 + GX-APP-025/030/036 | product-owner（user） | 将“数据源显式绑定 + 受控 SQL 查询验证”提升为当前可用性里程碑的基础门禁；一个 `table` 节点不能只结构合法，必须绑定同 Graph 已连接数据源并能经服务端限权查询验证。 | 与原 Phase 1 “数据库 connector 非范围”存在冲突；需修正 GraphX 产品范围/交接文档，并将 SQL backend 从 Supervisor 局部装配提升为角色最小权限共享基础设施。 | APPROVED | 2026-08-31 用户明确：SQL 应尽早提供，否则无法验证所构建的图；当前不可用感的根本是节点未连接数据源。 |
| C-003 | product-owner（user） | spec/03,05,06,11、semantic-change contract、ADR-009 | product-owner（user） | Agent 图变更接口从 raw HGT Patch 改为语义操作；模型不管理 Graph/Revision/Candidate/Patch/Connection/entity ID 或任何 hash，由 server-bound Resolver/Patch Compiler 注入并校验。首版只做 table create/update/connect。 | 这是 Agent 工具边界的破坏性迁移，但不改变内部 HGT Patch、Candidate、Review/Test/Apply 协议。需保留短期兼容桥，conformance 通过后从模型目录移除 raw Patch 工具。 | APPROVED | 2026-08-31 用户明确确认；GraphX `6603899` 实现，`829ddd5` 延伸到 Supervisor 协调身份；2026-09-01 真实 Builder trace 仅调用两个语义工具并生成 ready Candidate。 |
| C-004 | product-owner（user） | GraphX 下一阶段计划、semantic-change contract、Builder/Reviewer/Tester tools/prompts | product-owner（user） | 暂缓诊断 UI 和泛化故障评测；下一阶段以一个完整业务场景优化整个超图构建团队，使其能顺畅完成资源理解、节点/关系/超边构建、数据验证、Review、Test 和用户 Apply。首个场景选“销售订单履约追踪”。 | 现有语义工具只支持 table 节点与二元关系，资源目录只登记 2/5 张所需表，无法真实验收超图团队；需扩展目录、语义超边操作、关系数据验证和团队提示词，但保持模型不接触技术 ID/hash、Apply 仍只属于用户。 | APPROVED | 2026-09-01 用户明确否定 W-DIAG-UI-001/W-EVAL-003 作为下一主线；只读 information_schema 已确认 5 张场景表均真实存在。实施由 W-FLOW-001..006 跟踪。 |
| C-005 | product-owner（user） | GraphX 2026-09-03 后续路线与真实场景评测边界 | product-owner（user） | 暂停当前 30 问题真实场景的专项优化；把其冻结为回归资产。下一阶段先收敛权威叙事与通用构图黄金旅程，再将指标/状态机/比较等执行语义从服务端逐题 Profile 演进为 Graph-owned 版本化资产，并用全新未见场景验证泛化。 | 避免把“当前问题集答对”误当成“超图产品已通用”；短期会延后 q021/q029 relabel、q028 数据归因审计、诊断 UI 和广泛方言/故障评测，但直接解决场景特判与产品可迁移性风险。 | APPROVED | 2026-09-03 用户明确要求先放下真实场景优化，重新梳理进度和规划；W-RESET-002 已同步 STATE/WORKBOARD。 |
| C-006 | product-owner（user） | HGT 业务语义与 GraphX 平台边界 | product-owner（user） | GraphX 不判断数据库内容是指标、流程或其他业务类别；合同额、商机额等应作为超图中的节点、本体节点或语义超边表达。只有证明通用 HGT 原语不足并取得明确产品决定，才能新增平台级语义类型。 | 撤回 W-SEMEXEC-001/002；查询工具继续提供通用受控数据访问，不反向决定图的业务本体。 | APPROVED | 2026-09-03 用户明确纠正偏离；未提交、未部署、未 Apply 的 executable-metric 实现已撤回。C-005 中关于 Graph-owned 指标/状态机类型的推断由本决定覆盖。 |
| C-007 | product-owner（user） | API/文档/ontology 节点运行架构 | product-owner（user） | 依据既有 HGT 规范和能力预研开发三类节点支持，但适配当前产品架构：旧 MCP 仅作能力参考，正式运行能力直接实现为 DSH Harness 原生工具。 | 需要服务端注册资源与 runtime binding；模型只见语义名称/schema，不见 ID、URL、认证、artifact path/hash；文档检索与 ontology 推理保持职责分离。 | APPROVED | 2026-09-03 用户明确要求；W-GENERIC-SEM-001A/B/C 已在 GraphX WORKTREE 实现注册/执行、异构生命周期及原生目录读取，并对旧资产完成无 MCP smoke；未提交、未部署、未 Apply。 |
