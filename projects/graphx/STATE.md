---
title: GraphX 项目当前状态与下一步（STATE · 项目内容）
role: orchestrator(维护)
status: ACTIVE
version: 8.5
updated: 2026-09-16
upstream: [graphx/spec/06-testing-and-handoff.md]
downstream: [任何被要求"继续 graphx 开发"的 agent]
---

# GraphX · 当前状态与下一步（STATE）

## 2026-09-16 最新同步：统一 GraphX Supervisor

本节优先于下方历史记录。GraphX 提交 `89f6f96`，分支 `feat/trusted-build-core`。
用户授权同步进度并提交、推送；本次不部署，不修改线上数据。

- Graphs 移除 Build Mode，统一完整构建能力；旧请求字段继续兼容但不再切换工作模式。
- 删除 `GRAPHX_READ_ONLY` 与 Harness `chat()`；所有 GraphX 模型任务统一 Supervisor，离线回复保持确定性。
- Resource Manager 不再兼任其他角色的只读入口；数据库/API 明确先请求安全配置表单。
- 提示词补充中文审阅注释；版本绑定的 Candidate 缺少当前 Review 时不允许提前结束协调。
- System Graph 保护、工具授权、Candidate 校验与用户 Apply 确认保留。Applications 仍仅占位，后续限制由服务端能力控制。
- 本次复验：Harness/入口/路由/聊天 UI/前端契约 45 passed，Web production build 通过。
  上轮扩大回归合计 47 passed、9 failed；9 项位于 dynamic-agent-task-graph，因旧测试未传 `config_id`
  报 `AI_CONFIG_REQUIRED`，尚未进入角色执行。不得据此宣称全量验收通过。
- 下一步：修复上述测试夹具（不弱化产品模型选择要求），重跑任务 DAG 与 Candidate Review/Apply 回归；
  然后部署并用真实资源配置、构图、审查、Apply 场景验收。LLM 完整用量采集仍沿用既有未完成状态。


## 2026-09-14 当前迭代：个人工作台 AI Manage

本节优先于下方历史计划。用户明确 GraphX 是个人产品，不是多租户平台；
历史 W-PLATFORM-001 的 tenant/org 平台路线不再是本产品下一步，不据其启动开发。
本轮用户要求 Negentropy 团队按“设计 → 需求 → 开发 → 验收”推进，先落地 AI Manage，
Applications 仅一级导航占位，不做应用构建、运行或发布。Graphs / Resources 保持现有能力。

- profile：`feature`；用户明确的前置交互设计先于需求整理，正式技术契约仍在需求评审后冻结。
- 权威代码：`graphx` 分支 `feat/trusted-build-core`，HEAD `bd15e9886a6180519f2912881ce28c297d4aead9`；接手时 clean。
- 规范仍以 `graphx/spec/` 为准；新设计尚未批准，不能将设计意图宣称为已实现。
- 用户/产品批准者：`project-owner=user`、`product-owner=user`。用户已确定模块范围；新增细节由需求稿明确提交确认，不伪造批准。
- 设计：`03-architecture/ai-manage-design.md` v0.3（APPROVED）。
- 需求：`02-requirements/ai-manage-requirements.md` v0.3、`ai-manage-iteration-plan.md` v0.2 及五个 US-AIM 用户故事（APPROVED）。
- AI Manage 聚焦模型配置、LLM 用量统计、执行日志；复用任务 Trace，不另做一套摘要报告。
- 当前工作授权为 scoped implementation，设计阶段仅文档；未获本轮提交、部署、push 授权，不改线上数据和密钥。
- 2026-09-14 验证：`UV_CACHE_DIR=/tmp/graphx-uv-cache uv sync --offline` 成功；
  `UV_CACHE_DIR=/tmp/graphx-uv-cache uv run --offline python -m unittest discover -s tests -v` 输出 12 tests OK，
  但执行会话尚未返回退出码；仅记录测试输出，不声称该进程已正常退出。
  `python scripts/validate_team.py --project graphx`：0 errors、6 项历史 warnings；未执行新功能验收或重新核验部署状态。
- 设计及需求已交付 v0.1 IN_REVIEW；独立测试角色只读评审结论为无阻塞提交用户确认，
  不是新功能测试通过。评审要求明确测试凭据复用/新目标保护、部分 usage 的未知计数与字段覆盖率。
- 用户随后要求“继续吧”，Q-AIM-001 范围已确认推进；需求已记录批准证据。下一步由架构角色冻结正式契约，
  后端/前端开发、测试角色独立验收。Q-AIM-002 为 pinned DSH 请求观测技术门禁，实施时必须有真实证据。
- 暂未开发、提交或部署 AI Manage。本轮草案选择单默认配置、整树快照、连接测试、逐请求用量、只读日志；
  多配置/角色覆盖、费用与破坏性日志清理均是后置建议，不冒充用户已批准。
- 2026-09-14 续接（orchestrator）：AI Manage 后端（配置/快照/连接测试/日志/用量）与前端（三 tab+占位）已在
  `graphx` WORKTREE 实现并通测（`tests/conformance/test_ai_management_backend.py` 6 passed、前端 `apps/web/tests/aiManage.test.mjs` 5 passed、production build 通过）；
  用量采集按 Q-AIM-002 门禁保持诚实 `unavailable/partial`，不冒充完整统计（GX-APP-083 仍 planned）。
  已修复基线：`test_spec_contract` 曾因 GX-APP-080..084 未在 `spec/03-domain-invariants.md` 声明而 red，
  现已补充声明并为未实现项补齐 `planned_test` 说明。
  又修复 WORKTREE 前端回归：`ResourceCenter` 曾重复内联与 `GlobalWorkspaceFrame` 相同的工作台 rail
  （多出一个 `<WorkspaceGraphControl>`），导致 `test_workspace_resources_are_a_peer_page_and_graph_binding_is_separate` red；
  已改为 `ResourceCenter` 复用 `GlobalWorkspaceFrame`，删除重复 rail，并把陈旧 FE conformance 断言更新为组件化
  导航架构；`test_workbench_frontend.py` 新增通过 `test_ai_manage_and_applications_are_peer_workspace_destinations`。
  最终 `uv run --offline python -m unittest discover -s tests` 12 tests 全绿；AI 后端 conformance 6 passed、
  FE conformance 12 passed、前端 production build 通过、`git diff --check` 通过。
  GX-APP-080/081/082/084 已 conformance-wire 置 `implemented`（manifest 对应 flag 同步为 true）；
  GX-APP-083 保持 `planned`，唯一阻塞为 Q-AIM-002。
  仍为 WORKTREE（未 commit）；AI Manage 目前端已完成 `vite build` 并在用户授权下经 `redeploy_alpha.sh` 部署到 8001（未清库），
  后端 AI 四路由已验证可用；下一步可据契约 v0.2 APPROVED 由独立测试角色收口 AI Manage 验收报告。
- **2026-09-14 已交付上线：多模型配置库，无"默认"概念**。用户最终明确：**没有默认**；每条消息发送时选一个模型，就是用它跑，下一条可换。
   WORKTREE 已实现并部署（`redeploy_alpha.sh`，PID 2009718，保留数据）：
   - 后端多条目库：`GET/POST /api/v1/alpha/ai/configs`、`PUT /api/v1/alpha/ai/configs/{id}`、
     `POST .../configs/{id}/default`、`DELETE .../configs/{id}`；`/ai/config` 保持默认别名。
     每条目独立版本；删除唯一默认受阻（409 `AI_CONFIG_DELETE_DEFAULT`）；连接测试按条目版本校验、不落库；
   - 前端：AI Manage 模型页改为**配置条目列表**（新增/编辑/名称/路由/模型/Base URL/设默认/删除）；
     GraphX 输入栏增加**模型下拉**（选定→`POST default` 设为全局默认）。
     说明：新增条目**非自动默认**，需单独“设为默认”或用输入栏切换（区隔更清晰，避免静默改默认）；
   - 快照绑定 `config_id+version`；凭据仍服务端隔离、不回流浏览器。
   - 测试：AI conformance 10 passed（+3 多配置）、前端 node 9 passed、spec-contract 通过、build 通过；live 已验证创建/列表/设默认/更新版本(409)/删除保护 全通。
   GX-APP-085 新增置 `implemented`，manifest/handoff 同步；GX-APP-083 仍 planned（Q-AIM-002）。
   非本迭代回归：`test_graph_delete / workspace_resource_center / tool_first_graph_operations` 3 个在 WORKTREE 基线即因 workspace-resource 复用语义 red，与 AI 无关。

- **2026-09-14 再修正（最终语义，覆盖上方默认实现）：移除全部"默认"概念并重新部署 8001（PID 2277393）**。用户要求：没有默认；每条消息发送时选哪个模型就用哪个。
   - 后端移除 `POST /configs/{id}/default`、`PUT /config`、`active/default` 及删除默认保护逻辑；删除 API 改为普通删除。`GET /ai/config` 保留旧别名（仅回退部署值，不含 default）。
   - 发送消息在 `ChatRequest.config_id` 显式带所选模型，根任务快照绑该 config_id+version（source=user_selected）、子树继承；未选模型拒发（AI_CONFIG_REQUIRED）。
   - 前端：AI Manage 模型页=条目库（新增/编辑/删除/测试，无"默认"徽标）；GraphX 输入栏模型下拉=本消息所选，未选不能发送。
   - 已从 live 删除预置"部署默认"条目（库现为空，由用户新增）。测试全绿（AI 10 / node 9 / spec-contract / workbench 12），e2e 验证 无config拒发、带config接受并绑快照。GX-APP-085 语义改为"逐消息选模型，无默认"。
   - 2026-09-14 架构收口：需求 v0.3、US-AIM-005 v0.2、设计/契约 v0.3 和 GraphX GX-APP-081/085 已统一为该最终语义；旧多模型默认方案标记 SUPERSEDED。发现当前前端仍在加载列表时自动选中第一条作为 composer 模型，此行为等价于隐式默认，违反 v0.3，进入实现修复与独立验收门禁。

- **2026-09-14 独立验收收口（优先于本节上方过程记录）**：A 切片已通过，报告为
  `05-testing/ai-manage-test-report.md` v0.1 APPROVED。已修复并复验 composer 隐式首选、非空 SQLite
  迁移、活动旧任务树 `legacy_recovery`、worker 凭据协议和跨目标凭据隔离。常规 pytest 48 项、
  pinned DSH rc6 本机回环真实路径 1 项、Web 9 项及 production build 均通过；所选 Base URL、
  model、Bearer Authorization 已在真实路径生效且不泄漏 secret。当前 WORKTREE 未提交、未部署，
  8001 现未监听。A 切片可进入本地体验；真实逐请求/token 用量仍受 Q-AIM-002 阻塞，
  `llm_request_usage_accounting` 保持 false，不得描述为完整首版可发布。

- **2026-09-14 UX 追加收口**：模型配置页已移除“当前在用”运行语义；Graph 非 active 卡与
  其他一级入口统一为 54px 视觉 primitive；模型选择迁入增高 composer 内部底栏右侧，
  无配置时保留“配置模型”入口。Web 9 项及 production build、GraphX 前端/规范 pytest
  13 项、diff check 均通过。详见独立验收报告 v0.2。仍为 WORKTREE，未提交、未部署。

- **2026-09-14 最终交付状态（覆盖上述过程记录）**：AI Manage A 切片、Applications 占位、
  逐消息显式模型选择、原始 Task Trace 及本地 OpenAI-compatible 连接路径已完成。
  凭据目录已移出代码仓并支持旧路径迁移；重新部署不再从旧进程继承代理或硬编码模型主机，
  仅使用当前服务器环境的 proxy/no_proxy。用户配置的 `qwen3.6-27b` 连接测试已实际成功。
  最终回归：Python 49 passed，Web 9 passed，production build 通过，`git diff --check` 通过。
  8001 当前为 `graphx-alpha.service` active/running（PID 2709544）。LLM usage 仍按契约返回
  `unavailable/partial`，不虚报完整 token 统计。本轮已获用户“整理并提交”授权。

## 2026-09-13 最新续接：应用后业务验收

用户已应用合同候选，正式图revision 2、15节点。异常保存终态与页面状态同步已修复，
部署PID 2699771，保留数据；43项专项测试、12项基线与前端构建通过。
首题最初失败源于模型参数不合法，不是已证实数据库故障。Supervisor profile v4明确
查询参数形状及错误解释后，同题复测返回2条记录，与human_label一致。
这是已有 `contract_material_fulfillment/v1` 分析工具的验证，不是泛化能力证明。
下一步选取不同履约分支的问题继续验收；保留0行合同查询及口径冲突为后续核查项。
详见 `graphx/docs/handoff/user-scenario-contract-20260912.md`，本节优先于历史状态。

## 2026-09-12 最新续接：真实合同履约场景候选恢复

本节优先于下方历史快照。用户暂停隔离实验，当前先验收真实产品场景。
已修复继续聊天隐式丢弃候选、跨轮候选缺失、续派继承旧候选和关系收据错用正式图校验。
8001 已重新部署（PID 1961912），未清数据。26 项专项回归、12 项 unittest 基线及前端构建通过。
`合同履约全链路 · 用户场景验证` 最新候选为15节点、13关系、2超边，状态 ready；
针对同版本 Reviewer passed，Tester 完成12条关系检查和2项确定性检查。
已进一步修复 GraphX 把读入的 Tester 收据重复发布的问题，真实收尾返回200；
前两次失败遗留的协调任务已通过取消API结束，当前活动任务为0。
尚未用户 Apply，正式图为空不等于候选未生成；右侧应显示“候选预览 · 未应用”。
下一步由用户确认应用，再验证真实业务问题；不能把结构检查等同于完整业务验收。
细节与剩余问题：`graphx/docs/handoff/user-scenario-contract-20260912.md`。

## 2026-09-12 用户试用后：统一聊天角色逻辑

用户已确认设计并要求实施，当前优先于泛化实验。设计说明：
`graphx/docs/product/chat-role-coordination.md`。
入口由每条消息的 @ 决定；默认 GraphX；Add resource 仅增加开场白。
角色充分回答后 GraphX 静默结束，后台协调保留 Trace。Build Mode 控制变更工具，
不再禁止只读角色会话；委派继承权限。此轮已部署到 8001（PID 1467662），
3 个 Graph ID 与 2 个 Workspace 资源保留。74 项专项测试、3 项前端测试及构建通过；
真实模型专项 `chat-finish-check-fc846e2f8d` 返回 finish + silent=true。
验收关注 Resource Manager 回答不重复、关闭模式只读角色可用、变更工具被拒绝。

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
| 项目 | GraphX（Graph-first 可追溯超图工作台），产品版本 **0.5.9 WORKTREE** |
| 代码仓库 | `/home/wangling/develop_team/graphx`（分支 `feat/trusted-build-core`，HEAD `76d9220` + Reviewer 全部整改 WORKTREE；未提交、未部署） |
| 规范事实源 | `/home/wangling/develop_team/graphx/spec/`（APPROVED，**单一事实源**，覆盖一切历史聊天/原型） |
| 历史工作流 | existing-spec（历史阶段 1–3 由 `graphx/spec/` 替代；当前迭代以顶部 feature 说明为准） |
| 团队 | negentropy（9 角色，含独立 Reviewer，协议 `v1.1-docs`），定义在 `/home/wangling/develop_team/negentropy` |
| 当前阶段 | **W-GENERALIZE-001 IN_PROGRESS**：Reviewer 整改与防回归增强已完成；全新设备维保场景及评分口径已冻结，确定性通用能力 preflight 通过，下一阶段运行真实角色 runtime |
| 测试状态 | Node tests 1 file/3 cases passed；前端 production build 通过；Python 核心 46 passed + 14 subtests、runtime/spec 28 passed，新增专项组合 27 passed；仓库规约 unittest baseline 12 passed；compile、requirements JSON、diff check 通过。更宽旧 pytest 集合仍有既有后台等待卡住，不声明全量通过 |
| 真实运行证据 | 两个完整语义场景已通过团队构建并 Apply；30 问题隔离运行 30/30 HTTP 完成，最终三个编排缺陷已定向修复；仍有 2 个 Graph 覆盖缺口、2 个历史 golden 漂移、2 个代理/数据质量限制。**W-GENERIC-SEM-001F 已无清库部署到 8001（main PID 1320551）并验证**：旧连接/准入自动提升为 WorkspaceResource+Binding（connection_id 保持），active `123` 5 节点仍可解析；临时 Graph 上 HTTP 闭环 create→test→bind→unbind→delete-protect→delete 全部通过，生产 3 Graph 无损 |
| 运行应用 | AI Manage 已部署到 8001（`redeploy_alpha.sh`，2026-09-14，用户授权 publish）并已验证：`/api/v1/alpha/ai/{config,config/test,logs,usage}` 全部可用；`config` 返回真实部署配置（local / `DeepSeek-V4-Flash-0731` / none）、`logs` 返回近 7 日跨 Graph 任务分页索引、`usage` 按 Q-AIM-002 诚实返回 `unavailable`。保留既有 Graph/数据，未清库。其余 reviewer/泛化整改仍为本地 WORKTREE、未 commit |
| 下一步 | 对冻结的 `equipment-maintenance-v1` 执行隔离真实角色 runtime：先由 GraphX 根据目标动态派工，再按实际产物触发所需独立角色；统计工具/返工/澄清与 Candidate 得分。不得预排固定 pipeline 或现场改 fixture/prompt；commit/deploy 仍需另行授权 |

## 2026-09-12 · W-GENERALIZE-001 Phase 1 已冻结

- 无需用户真实数据，采用全合成 `equipment-maintenance-v1`：设备台账、维保工单、维保技术人员、
  维保班组、备件消耗记录五个目录资源；预先冻结四条仅由字段元数据支持的 association 与四个代表问题。
- fixture 明确排除订单、客服、WMS、SAP Profile 和 model-visible connection identity；运行前已经固定，后续
  失败只能分类记录，不能为提高成绩现场修改场景或增加 Python handler。
- Phase 1 确定性 preflight 证明：`semantic_scenarios=()` 时仍能投影字段角色和四条关联线索，语义操作
  可以编译五节点四关系 Candidate，模型侧只使用语义名称，服务端再绑定 opaque provenance。
- 这只是运行前资格检查，不冒充泛化结果。Phase 2 必须让真实 GraphX/独立角色 runtime 面对不变 fixture，
  记录动态派工、澄清、工具调用、返工、Candidate、Review/Test 与问答评分。

## 2026-09-12 · W-REVIEW-HARDEN-001 已完成

- Prompt Profile 增加性质测试：改变 objective/history 会改变渲染后的每轮 prompt，但不改变稳定
  `prompt_digest`；改变稳定 instructions 或 version 必须改变 digest。
- 前端角色 ID、显示 label、mention aliases、解析器和 UI 角色按钮由 `entryMention.ts` 的同一份
  `ROLE_DEFINITIONS` 派生；新增角色不再同时维护 TypeScript union、正则、显示映射和按钮数组。
- GX-APP-075 的旧 API catalog 修复加入单 Service 临界区；同一资源并发显式 test 不会重复扫描、
  重复写入确定性 operation ID 或向用户暴露事务冲突。规范、manifest 与映射测试保持闭环。
- 该短前置没有改变角色心智、资源授权、Candidate/Apply 或 wire contract。下一主任务直接进入
  `W-GENERALIZE-001`，结构性拆分继续保持渐进式后置。

## 2026-09-12 · Negentropy Reviewer 整改收口与下一步

- Reviewer 首轮识别的五项问题已经全部处理：四个独立角色统一回交 GraphX observation；入口 mention
  解析/清理由单一运行时模块负责并有真实连续切换测试；应用初始化不再扫描外部 OpenAPI；两条不可达
  legacy pipeline 及其无调用 Service 构造依赖删除；五角色 Prompt Profile 具名、版本化，稳定 digest 与
  动态任务上下文分离，通用 GraphX prompt 不再无条件注入订单/WMS/SAP 场景。
- `04-implementation/code-review.md` v0.3 是 Negentropy Reviewer 的独立复核记录，结论为
  **原审查项全部关闭、复审通过、无阻塞发现**。文档按角色协议保持 `IN_REVIEW`，不冒充产品批准或发布授权。
- 下一工程切片 `W-REVIEW-HARDEN-001` 已完成三项防回归增强：Prompt digest 性质测试、前端角色定义
  单源化、API catalog 并发幂等测试；未扩大为产品重构。
- 随后的主线是用一个全新、未见的中等复杂场景验证 GraphX 的动态派工、资源使用、Candidate →
  独立 Review/Test → 用户 Apply 与问答闭环。失败按产品能力分类，不现场增加场景专属 handler。
- `ResourceCatalogService`、`ChatOrchestrator`、`useChatTurn`、`ResourceConnectionForm` 的渐进抽取仍是结构性建议；
  只在后续触碰对应边界时小步实施，不以一次性 monolith 重写阻塞泛化验收。

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
| 4 实现 | frontend ∥ backend | **IN_PROGRESS** | Resource Manager role/skills、Graph-local/Workspace scope 与显式发布已在 WORKTREE；本轮修复资源菜单裁剪并将 Database 授权收敛到配置 Schema |
| 5 测试 | test-engineer | **READY** | 当前 30 问题冻结为回归资产；下一质量门禁使用全新未见场景检验泛化 |
| 6 发布 | devops-engineer | **DONE（当前里程碑）** | `fa351ce` 已本地提交并 **push** `origin/feat/trusted-build-core`；8001 已无清库重部署、迁移与 HTTP 闭环验证通过 |
| 7 复盘 | orchestrator | **DONE** | 2026-09-03 完成第二次项目级复盘：从场景正确率优化转向通用构图产品化 |

> 历史说明：阶段 1–3 当时按 existing-spec 合法裁剪为 `SKIPPED`，由 `graphx/spec/` 的当前 revision 替代
> （`spec/` 是单一事实源）。本工作区只承载团队协作文档（notes/测试三件套/问题登记），不复制规范。

## 当前产品判断与新路线（2026-09-03）

### 产品目标

GraphX 不是一个针对固定问题集编写查询函数的问答应用。它的核心产品是：让用户把受控数据源交给
一个可审计的 Agent team，由模型只表达业务语义，服务端 Resolver/Compiler 管理技术身份与并发，
经 Candidate、独立 Review/Test 和用户 Apply 形成可执行的不可变超图；之后 GraphX 通过该图回答问题，
并把证据绑定到精确 Revision。

### 当前完成度

| 层级 | 结论 | 已有证据 |
|---|---|---|
| HGT 与控制面 | 基本成型 | Bundle/Patch、不可变 Revision、Candidate、Review/Test、用户 Apply、typed receipts、诊断与权限门禁均已实现 |
| Agent 构图团队 | 已跑通 Alpha | GraphX/Resource Manager/Builder/Reviewer/Tester 独立 Harness、语义工具、动态任务图、关系验证和两次正式场景 Apply 已验证；GraphX 负责任务分派，不存在写死 pipeline |
| 数据可执行性 | 已跨过“空壳图”阶段 | Graph-owned connection/catalog、节点来源绑定、Candidate Preview/Revision 受控 SQL 与 relation check 可用 |
| 工作台体验 | 已具备大图基础 | 超边实体、力导向拖拽、全屏/小地图、搜索聚焦、一跳高亮和可扩展成员选择已交付 |
| 业务问答 | 当前场景可用，但尚未证明通用 | 30/30 HTTP 完成，关键语义缺陷已修复；部分能力依赖 `question_executor.py` 的服务端确定性 Profile |
| 生产平台 | 未完成 | 多租户授权、生产 Graph store/原子 outbox、对象存储、OS 级隔离、凭据 broker 与组织库生命周期仍是后续工程 |

### 暂停项

- 暂停继续修 q021/q029 golden 漂移、q028 供应商归因和当前 30 问题的逐题优化；保留为冻结回归/数据治理事项。
- 失败诊断详情 UI、超时/方言/广泛脱敏评测继续保持 deferred，不抢占构图主线。
- 不把新的业务问题继续固化成 Python `profile_name -> handler` 分支；已有 Profile 作为基线与迁移样本。

### W-ALIGN-001 对齐结果

- 入口 README 和 SPEC 已改为当前 GraphX/Builder/Reviewer/Tester、语义 Compiler、数据连接与受控查询主链；
  早期“只有 Builder/两张表”表述已删除。
- manifest 进入 `generalizable-semantic-construction` 阶段，30 问题明确为冻结回归，
  `graph_owned_executable_semantics` 明确为尚未完成。
- `spec/06` 现在先给出唯一的当前继续顺序，时间累积内容降为历史交付记录。
- 14 个 planned requirement 已逐项核查：8 个凭现有或新增直接测试转为 implemented；6 个真实缺口保持 planned，
  分别是投影重建、golden OS 隔离、原子 Apply/outbox、完整运行指纹、提示注入防护和全链路脱敏。

### W-JOURNEY-001A 通用资源目录（已交付到 WORKTREE）

- PostgreSQL 连接现在保留用户配置的 Schema；新 `scan` 路径只读 `information_schema`，最多返回
  200 张表及字段元数据，预览不会写入 SourceTable。
- 新 `import` 路径只接受用户明确选择的 `(schema_name, table_name)`；服务端会重新扫描并拒绝重复、
  伪造或过期选择，只把获批资源及其 connection provenance 写入当前 Graph catalog。
- 工作台在新增 Database 连接后打开可搜索资源选择器，连接列表也可再次进入；支持过滤结果批量选择、
  显式 selected count 和逐项增删，不读取业务行、不把连接秘密交给模型。
- ADR-017 与 GX-APP-056 已记录。旧 13 表发现仅保留兼容，不再是通用构图目标。

### W-JOURNEY-001B 通用 Builder 语义投影（已交付到 WORKTREE）

- `graph_semantic_context_get` 现在为任何用户批准的目录资源生成有界、确定性的字段角色摘要，
  不读取业务行，也不要求命中 checked-in scenario。
- 服务端只从精确且类型兼容的标识字段生成最多 100 条关系线索；线索只能支持
  `association`，明确声明不是数据库外键、血缘或业务方向。无证据则不输出关系线索。
- Builder prompt 要求保留元数据字段对与理由；没有用户陈述、scenario 或 hint 支持时只构建
  有依据的节点，并指出关系含义/连接证据仍需澄清。
- 冻结的客服领域 fixture（客户账户、客服工单、客服排班）证明：无内置场景时可编译三节点和
  一条有依据的账户—工单 association，且不会把无依据的排班表强行连入。
- GX-APP-057 已登记；相关核心组合 62 项、资源目录独立 3 项通过。未提交、未部署、未 Apply。

### W-JOURNEY-001C 通用黄金旅程门禁（已交付到 WORKTREE）

- 同一冻结客服 fixture 从空 Mine Graph 生成语义 Candidate；Reviewer 读取精确 diff 并提交独立
  ReviewReport，Tester 对同一 Candidate 提交独立 TestReport，期间正式 Graph 不变。
- 非 user actor 的 Apply 被拒绝；显式 user Apply 创建不可变 Revision 2；随后受控查询产生绑定该
  Revision 的 QueryReceipt。全程 `semantic_scenarios=()`，没有业务专属 handler。
- GX-APP-058 已登记，最终专项 4 passed；W-JOURNEY-001 达到当前 Alpha 验收并转为 DONE。

### W-SEMEXEC-001 错误方向试验（已撤回）

- 产品负责人指出，“合同额、商机额”等只是业务语义，GraphX 不应判断数据库内容属于指标、流程
  或其他业务门类；它们应继续使用通用节点、本体节点和语义超边表达。
- 未提交、未部署、未 Apply 的 executable-metric 代码、ADR、Schema、prompt、测试和 requirement 已从
  GraphX WORKTREE 撤回；通用资源目录、Builder 语义投影和黄金旅程成果保留。
- C-006 固化边界：未来新增平台级语义类别前，必须先证明现有 HGT 通用原语无法表达，并取得明确
  产品决策；不能从某个业务问题或查询实现反推产品本体。

### W-GENERIC-SEM-001A 注册资源节点与原生 DSH 工具（已交付到 WORKTREE）

- API、文档与 ontology 仍是 HGT 的通用节点类型，而不是 GraphX 对业务内容的分类。部署侧注册表保存
  不可变执行定义；Builder 只按 `resource_name` 和语义名称创建节点，Compiler 注入 node ID、来源证据与运行绑定。
- `graph_semantic_context_get` 只向模型投影方法/schema、文档目录/AST schema、ontology 领域/schema/支持任务等
  安全语义；URL、认证、artifact 路径、持久 ID 与 hash 均留在服务端。
- GraphX/Reviewer/Tester 通过原生 DSH `api_query`、`doc_execute`、`ontology_execute` 调用精确 Revision 中的节点；
  文档检索和 ontology 规则推理保持不同工具边界，旧 MCP server 不进入产品运行架构。
- HGT `node_refs` 增加 `ontology_nodes`，混合语义超边可同时包含 table/api/doc/graph/ontology 节点。
- 已迁移脱敏的 TPT 文档与订单履约 ontology 注册样例。API 执行支持受 schema 约束的 GET query/POST JSON；
  认证 broker 与用户可见注册入口仍属后续切片。
- GX-SEM-008、GX-HGT-008、GX-HARNESS-010、GX-APP-059 已登记为 implemented；专项验证见测试报告。

### W-GENERIC-SEM-001B 异构关系与显式解绑删除（已交付到 WORKTREE）

- 注册 API/文档/ontology 节点可通过 `update_registered_node` 修改语义名称或说明；Compiler 保留节点 ID，
  并从精确注册项重新绑定受保护运行契约，模型不能修改 URL、artifact 或 runtime。
- `connect_nodes` 根据有向端点类型推导 HGT `relation_type`，校验规范 subtype；当前覆盖 api-api、doc-doc、
  table-api、table-doc、api-doc、ontology-table、api-ontology。规范未定义的方向不会自动反转，而是要求澄清或改用超边。
- `disconnect_nodes`、`remove_semantic_hyperedge` 与 `remove_node` 提供非级联删除语义；节点仍被边或超边引用时
  返回 `SEMANTIC_NODE_IN_USE`，必须先显式解绑。Compiler 为更新/删除注入当前实体 precondition hash 与证据。
- GX-SEM-009 已登记 implemented；相关组合 82 passed，通用黄金旅程 4 passed，未提交、未部署、未 Apply。

### W-GENERIC-SEM-001C 原生文档/本体目录执行（已交付到 WORKTREE）

- 常用 `doc_execute(listdocs/search/extract_section)` 已直接读取服务端托管 Document AST；常用
  `ontology_execute(list_concepts/search_terms/get_mapping/list_rules/explain_rule/plan_evidence)` 已直接读取版本化 artifact。
- 物理路径只由隐藏的 `env:` 引用解析，路径逃逸、缺失/超大/损坏 artifact 均 fail closed；返回内容有界且不含绝对路径。
- 移除了隐式 localhost 服务假设。文档文件导出需要显式 session-workspace adapter；ontology
  `classify/validate/infer` 需要显式 reasoner adapter，未配置时返回结构化 unavailable，而不是伪造结果。
- 对用户提供的旧预研资产完成只读 smoke：8 份文档可列举，“信创”检索返回 3 条有界结果；本体读取
  16 个概念并规划出 9 个表节点。未启动 MCP/旧 HTTP 服务，未输出文档正文、业务行或物理路径。
- GX-HARNESS-011 已登记 implemented；相关组合 85 passed，黄金旅程 4 passed，前端 build 通过。

### W-GENERIC-SEM-001D Graph 级注册资源准入（已交付到 WORKTREE）

- 部署注册表现在只表示系统资源库存，不会再把全部 API、文档、本体资源自动暴露给每个 Graph。
- Mine Graph 用户通过工作台选择资源；服务端保存 Graph-scoped admission，并在 Builder 绑定、Candidate
  校验与 Apply 复验时只解析当前 Graph 已准入的资源。新 Graph 默认没有任何准入，Graph 之间不继承。
- Bootstrap 仅返回不透明 key、名称、类型、说明和准入状态，不暴露 registry source ref、运行路由或物理路径。
- 当前 Revision 或开放 Candidate 仍引用注册节点时，移除准入 fail closed，要求先通过 Candidate 解绑。
- GX-APP-060 已登记 implemented；原生资源与准入专项 11 passed、production build 通过。
  TestClient 专项受既有 httpx/background wait 停滞，未计为通过；未提交、未部署、未 Apply。

### 新实施顺序

1. **W-ALIGN-001 · 权威叙事收敛（DONE）**：GraphX README、SPEC、manifest、handoff 与 conformance
   状态已对齐；W-JOURNEY-001B 后 135 项 requirement 当前为 129 implemented / 6 planned。
2. **W-JOURNEY-001 · 通用构图黄金旅程（DONE）**：空 Graph 到可查询 Revision 已由冻结非订单
   catalog 覆盖 schema/resource、语义 Candidate、diff、Review/Test、用户 Apply 和精确 Revision 查询门禁。
3. **W-GENERIC-SEM-001 · 通用业务概念建模（IN_PROGRESS）**：001A/B/C/D/E/F 已交付注册 API/文档/本体节点、
    混合超边、原生 DSH 执行、异构关系、显式解绑删除、常用目录读取、Graph 级用户准入和 **Workspace Resource Center**
    （已部署+HTTP 验证）；GX-APP-063 已在 WORKTREE 补齐 **用户材料 → Document/Ontology Draft → 显式发布**，下一切片补 DSH 丰富提炼、OCR、session-bound 导出、完整 reasoner、
    部署注册管理与认证 broker。
4. **W-GENERALIZE-001 · 未见场景泛化验证**：选择一个中等规模、此前未用于开发的场景，禁止新增场景专属
   Python handler；衡量构建成功率、澄清准确性、工具调用/返工次数、Candidate 语义正确性和 Apply 后问答正确性。
5. **W-PLATFORM-001 · 生产化门禁**：在通用性成立后再排多租户、Postgres/object store、atomic Apply/outbox、
   credential broker/隔离、组织库生命周期和扩大故障评测。

> `graphx/spec/06-testing-and-handoff.md` 当前包含大量按时间累积的旧 continuation 段落；在
> W-ALIGN-001 完成前，本节是 negentropy 的项目优先级快照，但 GraphX 行为真相仍只由其 `spec/` 和测试决定。

## 历史交付记录

### 2026-09-02 · 可扩展超图画布与关系语义（已交付）

- GraphX `960bf5f` 已将语义超边从重叠凸包改为可选择、可拖动的菱形实体，并通过
  membership springs 连接成员节点；二元边和成员边进入同一 bounded force simulation。
- 画布已提供全屏、小地图、节点/超边/关系语义搜索；搜索聚焦首个匹配项并二级高亮一跳邻域。
- 超边成员编辑改为名称/说明搜索、类型筛选、显式添加/移除、selected chips/count 与每页 40 项，
  不再为全图渲染 checkbox。
- `table-table` 新生产者契约明确 `foreign_key / lineage / semantic_similarity / association`；
  主外键必须有字段对。Canvas 客户端与服务端共同校验，Builder semantic contract 和两个场景提示均已同步。
- 旧 Revision 的无 subtype 边保持可读但不猜测语义；正式 Revision 6 未被本次部署修改。若要让四条旧边获得
  subtype 颜色和完整 Inspector 信息，应由 Builder/Canvas 生成 Candidate 后再由用户 Apply。
- 验证：60 个协议/Compiler/Harness/Canvas 专项通过，production build 通过；8001 health、前端 hash 与
  Revision 6 的 5/4/2 数据保留均通过，PID `1282835`。

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
2. Build Mode 仅是能力授权：关闭时只能激活 GraphX；开启时才允许 GraphX/用户激活 Resource Manager、Builder、Reviewer、Tester，并允许产生受控的资源或 Candidate 变更。
3. 用户可在群聊中 `@GraphX`、`@Resource Manager`、`@Builder`、`@Reviewer`、`@Tester`；没有 mention 时由 GraphX 判断交给谁。指定角色完成后统一触发一次 GraphX Supervisor observation，由 GraphX 决定静默结束、汇总、澄清或继续委派。
4. Resource Manager、Builder、Reviewer、Tester 都是目的和工具权限不同的独立 Agent，不是固定阶段或写死 pipeline；允许按目标动态派工、返工、先审计后构建或并行执行。Resource Manager 不天然从属于 Graph 构建流程。
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
