---
title: GraphX 全仓最低充分代码审查
role: reviewer
status: IN_REVIEW
version: 0.3
updated: 2026-09-12
upstream: [/home/wangling/develop_team/graphx/spec/, /home/wangling/develop_team/graphx/AGENTS.md]
downstream: [orchestrator, frontend-engineer, backend-engineer, test-engineer]
source_revision: 76d9220c9fc1ffc982ccb6f8a00b166a764a7169
---

# 代码审查意见

## 交接说明

- **给谁**：orchestrator 路由给 frontend/backend/test 实现整改；产品行为冲突由 product-owner 确认。
- **一句话**：全仓抽样与高复杂度路径审查结论为 **需整改**；当前最先应修的是 Resource Manager 绕过 GraphX observation、角色按钮残留双 mention，以及启动期逐连接访问外部 API。
- **关键决策**：按用户要求审查全仓，但只保留高影响、可证实且可用小改动消除的问题；不逐行评论格式，不把历史代码债务冒充本轮回归。
- **需要下游注意**：R-001～R-003 是近期资源/角色变更暴露或引入的问题；H-001～H-002 是历史遗留。审查工作已完成，文档状态为 `IN_REVIEW`；Reviewer 只给意见，不代表批准或发布门禁。
- **未决问题**：删除历史业务 Profile 前需 product-owner 决定其作为冻结评测资产的保留位置；不应继续留在通用 GraphX prompt。

## 1. 审查范围

- 触发方式：`on-demand`，用户明确要求使用 negentropy reviewer 对 GraphX 整体 review 并优化。
- 被审对象：`src/`、`apps/web/src/`、`config/`、`scripts/`、`tests/`，以及与问题对应的 `spec/`、Git history。
- 依据 revision：GraphX `76d9220c9fc1ffc982ccb6f8a00b166a764a7169`；审查开始时 GraphX worktree clean。
- 基准：`AGENTS.md`；`spec/02-architecture.md`；`spec/03-domain-invariants.md`；`spec/05-harness-adapter.md`；`spec/11-workbench-application.md`；`spec/conformance/requirements.json`。
- 审查方法：最大文件/函数统计、精确引用搜索、`git blame/log` 溯源、Python compile、三组相关定向测试；未运行高成本全量测试。

## 2. 结论

> **需整改**

代码的安全边界、类型化 Artifact、权限清单和规范映射总体清楚，近期提交也普遍同步了 spec/test；但存在一项当前规范的直接失配、一个可复现的角色选择缺陷，以及会把外部服务延迟放大成应用启动延迟的迁移实现。另有约 620 行确定不可达的旧流水线和无法稳定审计的动态 Prompt Profile，继续迭代前应收敛。

## 3. 问题项

### 本次/近期变更引入或暴露

#### R-001 · Resource Manager 终态被特判为不触发 GraphX observation

| 字段 | 内容 |
|---|---|
| 严重性 | **严重** |
| 位置 | `/home/wangling/develop_team/graphx/src/graphx_alpha/service.py:3606`；规范 `/home/wangling/develop_team/graphx/spec/11-workbench-application.md:347` |
| 证据 | 所有独立角色先执行 `_finish_role_task`，但 `service.py:3608-3609` 对 `AgentRole.RESOURCE_MANAGER` 直接返回；Builder/Reviewer/Tester 才进入 `_record_graphx_observation`。GX-APP-026 明确要求“a role task reaching a terminal state MUST enqueue a new GraphX observation turn”。`git blame -L 3606,3612` 显示该例外由 `3e60697` 引入。现有测试 `test_role_terminal_event_creates_graphx_observation_dag_node` 只覆盖 Tester，因此 14 项相关测试仍通过但没有保护 Resource Manager。
| 影响 | Resource Manager 成为唯一不把结果交回 GraphX 的角色，破坏“角色独立、GraphX 统一负责人”的心智；Resource Manager 完成 Draft/表单请求或失败后，GraphX 无法基于根目标决定后续动作或审计 silent finish。
| 最小修改建议 | 删除两行 Resource Manager 早退，统一进入已有 `_record_graphx_observation`；将 observation conformance test 参数化覆盖四个非 GraphX 角色，并允许 observation 选择 silent finish，避免多余气泡。不要增加 Resource Manager 专用 pipeline。

#### R-002 · 角色按钮切换不会清除已有 `@Resource Manager`

| 字段 | 内容 |
|---|---|
| 严重性 | **严重** |
| 位置 | `/home/wangling/develop_team/graphx/apps/web/src/App.tsx:832`；对照 `/home/wangling/develop_team/graphx/apps/web/src/api.ts:204` |
| 证据 | `ROLE_CHOICES` 已含 `resource_manager`，解析器 `ENTRY_MENTION` 也接受 `ResourceManager|Resource Manager`；但 `selectEntryRole` 的清理正则仍只有 `GraphX|Builder|Reviewer|Tester`。用户先选 Resource Manager、再选其他角色时会得到两个 leading mentions，`parseEntryMention` 将其判为 ambiguous。当前 `test_supervisor_chat_ui.py` 只断言源码字符串存在，没有模拟角色切换。
| 影响 | 正常 UI 操作会生成前后端主动拒绝的模糊消息；角色越多，这种复制枚举的漂移会重复发生。
| 最小修改建议 | 不在 `App.tsx` 维护第二份角色正则。由 `api.ts` 导出一个 `stripEntryMention`（与 `parseEntryMention` 共用同一规范化表），按钮切换调用该函数；补一个行为测试覆盖 `Resource Manager → Builder → GraphX`，断言始终只有一个 mention。

#### R-003 · API 兼容回填把逐连接外部网络访问放进同步应用启动

| 字段 | 内容 |
|---|---|
| 严重性 | **严重** |
| 位置 | `/home/wangling/develop_team/graphx/src/graphx_alpha/service.py:156`、`:414`；`/home/wangling/develop_team/graphx/src/graphx_alpha/source.py:68`；`/home/wangling/develop_team/graphx/src/graphx_alpha/api.py:41` |
| 证据 | `create_app()` 在返回 FastAPI 实例前同步调用 `service.initialize()`；初始化遍历每个空目录 API 连接并调用 OpenAPI rescan。每个连接最多尝试两个候选地址，每次 `urlopen(..., timeout=8)`；连接数量没有全局上限，最坏启动延迟约为 `连接数 × 16 秒`。异常虽被转成 `SourceConfigurationError` 后忽略，但等待本身仍阻塞启动。该路径由 `db5b5dd` 引入。
| 影响 | 一个或多个已下线的旧 API 能让健康检查和重启长时间不可用；“fail soft”目前只覆盖最终异常，不覆盖可用性和可观测性。失败也无持久状态，重启会重复等待。
| 最小修改建议 | 初始化只做本地、幂等的数据标记；把 rescan 变成受总预算约束的后台/管理迁移任务，记录 `pending/last_attempt/error_code`，成功后原子写目录。若产品坚持兼容初始化时扫描，至少增加整个 backfill 的全局时间/数量预算和结构化 warning，并补多连接超时测试。该调整会触及 GX-APP-075，需先同步规范语义。

### 历史遗留（只提醒，不擅删）

#### H-001 · 两条已退休流水线保留约 620 行不可达实现

| 字段 | 内容 |
|---|---|
| 严重性 | **一般（高收益清理）** |
| 位置 | `/home/wangling/develop_team/graphx/src/graphx_alpha/service.py:4660`、`:5260` |
| 证据 | `_legacy_qa_pipeline` 在 `4662` 无条件抛错，其后约 230 行不可达；`_legacy_build_pipeline` 约 382 行，仓库搜索只有定义、无调用。它仍编码 QuestionRun intent 检测和固定 Builder→Reviewer 活动，并依赖 `ALLOWED_TABLES`、`BusinessQuestionExecutor`、`DeterministicReviewer`。AST 统计两函数分别为 238/382 行；`rg -n '_legacy_qa_pipeline|_legacy_build_pipeline'` 未发现调用方。
| 是否疑似可删 | **是**。保留简短兼容入口 `qa()`/`build()` 即可；迁移考古应由 Git history 承担，不应把不可执行实现留在生产模块。
| 最小修改建议 | 先用 tests/部署脚本搜索确认没有反射调用，再整体删除两个私有函数的历史 body；随之删除只服务旧路径的构造参数/import/测试，或把冻结业务评测 executor 移到明确的离线 evaluation 模块。删除后跑统一 chat、Candidate、canvas review 和冻结评测回归。

#### H-002 · Prompt Profile 实际哈希了每轮上下文，且通用 GraphX prompt 内嵌特定业务 Profile

| 字段 | 内容 |
|---|---|
| 严重性 | **一般（进入泛化验收前应修）** |
| 位置 | `/home/wangling/develop_team/graphx/src/graphx_alpha/harness_executor.py:251`、`:359`、`:375`、`:209`、`:491`、`:777`、`:1008`、`:1160`；`/home/wangling/develop_team/graphx/src/graphx_core/runtime.py:217` |
| 证据 | `_supervisor_prompt` 是 165 行字符串组装；通用 Supervisor 明文列出 WMS/SAP、合同履约及十余个订单域 `analysis_profile`。五个角色均用 `content_hash(rendered_prompt)` 作为 `RoleProfile.prompt_digest`，而 rendered prompt 已含当前日期、目标、Chat、资源和 Context Pack；因此相同角色/指令版本在不同任务上也会得到不同 `profile_digest`。Context Pack 和 objective 本已有独立 hash/binding，当前实现无法仅凭 profile digest 比较“提示词版本是否变化”。这些业务段来自 2026-09-02/03 的冻结问题优化，早于当前通用构图路线。
| 是否疑似可删 | 业务 Profile 本身是否继续作为冻结评测能力由 product-owner 决定；**不应继续无条件注入所有 GraphX 会话**。
| 最小修改建议 | 建立五个独立、版本化的 Prompt Profile（代码可加载、配置可审阅）；`prompt_digest` 只哈希稳定 instruction template，动态 Context Pack 继续用自己的 hash。业务 profile 目录由服务端根据当前 Graph 能力有界投影，或只在冻结 evaluation profile 中加载。先保持工具权限仍以 `policy.py` 为唯一权威，不把权限下放到 prompt 配置。

### 结构性观察（不单独阻塞）

- `GraphXService` 为 6,053 行，同时拥有 schema 迁移、Workspace Resource、Chat、Supervisor DAG、Candidate、Canvas、Merge；`App()` 从 `App.tsx:263` 延续至文件末并持有 50 余个 state/ref。它们解释了 R-001/R-002 为什么容易以局部特判和复制正则进入系统。
- 不建议一次“大重构”。完成 R-001～R-003 后，优先以现有 API 为 facade，只抽两个最清晰边界：`ResourceCatalogService`（迁移/连接/目录）与 `ChatOrchestrator`（task/observation）；前端先抽 `useChatTurn` 和 `ResourceConnectionForm`。每次抽取保持行为测试不变。

## 4. 整改顺序（收益 / 风险）

1. **R-001 + R-002（最高收益、低风险）**：都是小范围删除/去重，直接恢复统一角色心智；先补失败测试再修。
2. **R-003（高收益、中风险）**：解除重启对旧外部 API 的同步依赖；需要确认 GX-APP-075 的初始化措辞并保留可追溯重试。
3. **H-001（高收益、低至中风险）**：删除确定不可达代码，显著缩小 `service.py` 和错误认知面；以引用搜索与定向回归兜底。
4. **H-002（中长期高收益、中风险）**：先拆稳定 prompt/profile digest，不同时改角色行为；随后把业务 Profile 条件化，最后进入未见场景泛化验收。
5. **小步拆分 monolith（持续进行）**：只随触碰边界抽取，不另起全面重写项目。

## 5. 通过标准核对

- [x] 审查范围、revision 和权威基准已明确。
- [x] 每条问题有严重程度、精确文件行号、可复现证据与最小修改建议。
- [x] 已区分近期引入/暴露与历史遗留。
- [x] 没有把代码行数单独当成错误；结构性结论由具体漂移/不可达路径佐证。
- [x] 未修改 GraphX 代码、规范或测试；只新增本审查文档。
- [x] 审查工作已完成，文档状态为 `IN_REVIEW`，未冒充批准者。

## 6. 验证证据

```text
cd /home/wangling/develop_team/graphx
.venv/bin/python -m pytest -q tests/conformance/test_dynamic_agent_task_graph.py tests/conformance/test_supervisor_chat_ui.py tests/test_role_policy.py
# 14 passed, 14 subtests passed in 3.98s

.venv/bin/python -m compileall -q src scripts
git diff --check
# passed

rg -n "_legacy_qa_pipeline|_legacy_build_pipeline" src tests scripts apps/web/src
# only the two definitions

git blame -L 3606,3612 src/graphx_alpha/service.py
git blame -L 414,474 src/graphx_alpha/service.py
git blame -L 329,410 src/graphx_alpha/harness_executor.py
# respectively identifies 3e60697, db5b5dd and the historical profile commits
```

说明：相关现有测试全部通过恰好证明 R-001/R-002 是覆盖缺口，不代表问题不存在；本轮未运行高成本全量 suite。

## 7. 下次快速复审项

- `service.py:3606-3612` 与 observation test 是否覆盖 Resource Manager/Builder/Reviewer/Tester。
- mention 规范化是否只剩一份实现，并有真实字符串转换测试而非源码包含断言。
- 应用启动是否不再按旧 API 连接数量线性等待外部网络。
- 两条 legacy pipeline 是否完整删除且统一入口与冻结评测仍通过。
- Role Profile digest 是否在动态 Chat/目标变化时保持稳定、在 instruction template 变化时改变。

## 8. 2026-09-12 WORKTREE 增量复审

### 8.1 复审范围与基线

- 基线仍为 GraphX `76d9220c9fc1ffc982ccb6f8a00b166a764a7169`；被审对象为该 HEAD 上尚未提交的 `W-CODE-OPT-001/002` WORKTREE，复审时共 `217 insertions / 1026 deletions`。
- 本次只核对 R-001、R-002、R-003、H-001、H-002 的关闭证据，并检查新增 `prompt_profiles.py`、显式 API 修复路径及 spec/test 一致性；未扩大到新的全仓风格审查。
- 最终结论：**仍需整改**。R-001、R-003 已关闭；R-002 实现已关闭但行为回归测试仍弱；H-001 主体已关闭但留下无调用构造依赖；H-002 的实现方向正确，但新建的 `GX-HARNESS-012` 未登记到权威 invariant 清单，导致 spec contract 测试确定失败。因此文档继续保持 `IN_REVIEW`，本结论是 Reviewer 意见，不代表批准。

### 8.2 原问题逐项状态

#### R-001 — 已关闭

- **代码证据**：`/home/wangling/develop_team/graphx/src/graphx_alpha/service.py:3621-3625` 已删除 Resource Manager 早退，所有非 GraphX 独立角色都在 `_finish_role_task` 后统一调用 `_record_graphx_observation`。
- **测试证据**：`/home/wangling/develop_team/graphx/tests/conformance/test_dynamic_agent_task_graph.py:75-111` 将终态 observation 测试参数化覆盖 Resource Manager、Builder、Reviewer、Tester；定向测试通过。
- **额外核对**：`service.py:4658-4660` 去掉 observation turn 对原触发用户消息的重复回显，恢复统一观察机制的同时没有制造第二个用户气泡。

#### R-002 — 实现已关闭，测试保护部分关闭

- **代码证据**：`/home/wangling/develop_team/graphx/apps/web/src/api.ts:204-220` 由同一 `ENTRY_MENTION` 同时驱动 `stripEntryMention` 与 `parseEntryMention`；`/home/wangling/develop_team/graphx/apps/web/src/App.tsx:832-837` 切换角色时调用共享清理函数，不再复制缺少 Resource Manager 的正则。
- **验证**：前端 `npm run build` 通过。
- **残余风险（一般）**：`/home/wangling/develop_team/graphx/tests/conformance/test_supervisor_chat_ui.py:13-34` 仍主要通过源码字符串断言验证该修复，没有执行 `Resource Manager → Builder → GraphX` 的实际字符串转换。最小补强是对 `stripEntryMention` 增加可执行 TypeScript 单元测试，断言连续切换后始终只有一个 leading mention；这不否定当前实现修复，但尚未完全达到原审查建议的回归保护强度。

#### R-003 — 已关闭

- **代码证据**：`/home/wangling/develop_team/graphx/src/graphx_alpha/service.py:154-180` 的 `initialize()` 不再调用外部 OpenAPI 回填；`service.py:411-485` 将兼容扫描保留为可按 `resource_id` 约束的幂等修复；`service.py:1805-1843` 只在用户显式测试且 API 可用时触发该资源的空目录修复。
- **可达性证据**：`/home/wangling/develop_team/graphx/src/graphx_alpha/api.py:100-102` 暴露显式 test endpoint，前端 `/home/wangling/develop_team/graphx/apps/web/src/api.ts:428-430` 使用该入口。
- **测试证据**：`/home/wangling/develop_team/graphx/tests/conformance/test_api_connection_catalog.py:286-311` 证明初始化零扫描及重复回填不重复；`:314-378` 证明显式资源测试只修复其绑定目录且第二次不重扫。相关测试通过。
- **规范证据**：GX-APP-075 已在 `spec/03-domain-invariants.md:190-193`、`spec/06-testing-and-handoff.md:202-207`、`spec/11-workbench-application.md:725-737` 和 PD-079 同步为“初始化本地化、显式测试修复”。

#### H-001 — 主体关闭，残余清理未完成

- **关闭证据**：`_legacy_qa_pipeline` 与 `_legacy_build_pipeline` 已从 `service.py` 删除；本次该文件净删约 715 行，`rg -n '_legacy_qa_pipeline|_legacy_build_pipeline' src tests scripts apps/web/src` 无结果。
- **残余风险（一般）**：`/home/wangling/develop_team/graphx/src/graphx_alpha/service.py:141-152` 仍接收并实例化 `question_executor`、`reviewer`，但 `rg -n 'self\\.question_executor|self\\.reviewer' src/graphx_alpha/service.py` 除这两处赋值外无消费方；相应 import 与大量 fixture 注入因此仍表现为已删除流水线的生产构造残留。`controlled_query_executor` 与 `generic_reviewer` 仍有真实调用，不应一起删除。
- **最小建议**：只删除无调用的两个字段、构造参数/import，并机械清理测试 fixture 的同名注入；`question_executor.py`/`reviewer.py` 中仍被离线测试或其他模块使用的冻结能力可独立保留，不要顺手扩大删除范围。

#### H-002 — 实现基本关闭，但规范闭环失败

- **实现证据**：新增 `/home/wangling/develop_team/graphx/src/graphx_alpha/prompt_profiles.py:9-37` 定义不可变、具名、版本化 profile，`prompt_digest` 只哈希稳定元数据与 instructions；`:40-196` 覆盖 GraphX、Resource Manager、Builder、Reviewer、Tester。`/home/wangling/develop_team/graphx/src/graphx_alpha/harness_executor.py:215-229`、`:356-377`、`:622-691`、`:807-856`、`:930-955` 均先选择 profile，再追加每轮上下文。通用 GraphX instructions 已移除无条件 WMS/SAP 与订单分析 profiles。
- **测试证据**：`/home/wangling/develop_team/graphx/tests/test_harness_executor.py:189-206` 检查通用提示词无订单域内容，并检查 profile 角色覆盖、digest 唯一及 runtime digest 来源；相关 harness 测试通过。
- **阻塞问题（严重）**：`/home/wangling/develop_team/graphx/spec/conformance/requirements.json:715-719` 把 `GX-HARNESS-012` 标记为 implemented，但 `/home/wangling/develop_team/graphx/spec/03-domain-invariants.md` 没有声明该 ID。`/home/wangling/develop_team/graphx/tests/test_spec_contract.py:16-25` 要求 requirements ID 集合与 invariant 声明严格相等，因此定向 suite 当前稳定失败：`Items in the first set but not the second: 'GX-HARNESS-012'`。
- **最小修复**：在 `spec/03-domain-invariants.md` 的 Harness invariant 区加入与 `spec/05-harness-adapter.md:348-356` 一致的 `GX-HARNESS-012` 声明，然后重跑 `tests/test_spec_contract.py`。同时建议把当前源码包含型 profile test 补成行为断言：不同 objective/history 生成不同 rendered prompt，但 `runtime_profile().prompt_digest` 不变；修改 profile instructions/version 后 digest 改变。

### 8.3 复审验证证据

```text
cd /home/wangling/develop_team/graphx
.venv/bin/python -m pytest -q \
  tests/conformance/test_dynamic_agent_task_graph.py \
  tests/conformance/test_supervisor_chat_ui.py \
  tests/conformance/test_api_connection_catalog.py \
  tests/test_harness_executor.py \
  tests/test_role_policy.py \
  tests/test_spec_contract.py
# 1 failed, 38 passed, 14 subtests passed in 8.38s
# 唯一失败：GX-HARNESS-012 未在 spec/03-domain-invariants.md 声明

cd /home/wangling/develop_team/graphx/apps/web
npm run build
# tsc -b && vite build：通过

cd /home/wangling/develop_team/graphx
.venv/bin/python -m compileall -q src scripts
git diff --check
# 通过
```

### 8.4 最小整改顺序

1. **先修 GX-HARNESS-012 invariant 登记（低风险、阻塞）**，恢复 spec contract 全绿。
2. **补 R-002 与 H-002 行为测试（低风险）**，让角色切换和稳定 digest 的真实语义可回归，而不只检查源码片段。
3. **清理 H-001 的两个无调用构造依赖（低风险）**，完成已删除旧流水线的尾部收口。

除上述事项外，本轮没有发现 R-001/R-003 修复路径的新阻塞回归；不建议在这次收口中继续扩大重构范围。

## 9. 2026-09-12 最终 WORKTREE 复核

### 9.1 最终结论

> **原审查项全部关闭；复审通过，无阻塞发现。**

本次复核对象仍为 GraphX `76d9220c9fc1ffc982ccb6f8a00b166a764a7169` 之上的未提交 WORKTREE，复核时共 `227 insertions / 1068 deletions`。v0.2 留下的 R-002 行为覆盖、H-001 构造残留、GX-HARNESS-012 invariant 登记均已补齐；结合既有 R-001/R-003/H-002 实现证据，R-001～R-003、H-001～H-002 现均判定为关闭。

审查工作已完成，文档仍保持协议要求的 `IN_REVIEW`。这里的“复审通过”仅表示 Reviewer 未发现阻塞整改项，不代表批准提交、发布或部署。

### 9.2 v0.2 遗留项关闭证据

#### R-002 — 已完全关闭

- `/home/wangling/develop_team/graphx/apps/web/src/entryMention.mjs:1-21` 现为入口 mention 解析与清理的单一运行时实现；`apps/web/src/api.ts:204` 直接复用并导出它，`apps/web/src/App.tsx:832-837` 的角色切换调用同一 `stripEntryMention`。
- `/home/wangling/develop_team/graphx/apps/web/tests/entryMention.test.mjs:11-37` 使用 Node 内置 test 执行真实行为：覆盖 `Resource Manager → Builder → GraphX` 连续切换，以及旧数据中 stacked mentions 被清理为单一 Reviewer mention。
- `apps/web/package.json:9` 已把该行为测试纳入 `npm test`；本轮实跑 `1 passed`，前端 TypeScript/Vite production build 同时通过。

#### H-001 — 已完全关闭

- `/home/wangling/develop_team/graphx/src/graphx_alpha/service.py:134-147` 的 `GraphXService` 构造器只保留仍有实际消费方的 `harness`、`generic_reviewer`、`controlled_query_executor`；`question_executor`、旧 deterministic `reviewer` 参数、实例赋值和 import 已删除。
- `rg -n 'self\\.question_executor|self\\.reviewer|def _legacy_qa_pipeline|def _legacy_build_pipeline' src tests scripts apps/web/src` 无结果；相关测试 fixture 的无效注入也已机械清理。
- `question_executor.py` 及其专门测试仍作为独立冻结能力存在，不再污染生产 Service 的依赖面；这符合 v0.2 要求的最小范围，没有误删其他仍在使用的 executor/reviewer。

#### GX-HARNESS-012 / H-002 — 已完全关闭

- `/home/wangling/develop_team/graphx/spec/03-domain-invariants.md:131-135` 已正式声明 GX-HARNESS-012，与 `spec/conformance/requirements.json:715-719`、`spec/05-harness-adapter.md:348-356` 以及实现保持一致。
- 先前稳定失败的 `tests/test_spec_contract.py:16-25` 本轮通过；requirements ID 集合与权威 invariant 声明重新闭环。
- Prompt Profile 的核心实现证据未变化：`src/graphx_alpha/prompt_profiles.py:9-37` 将稳定 profile 元数据/instructions 与每轮上下文拆开；Harness 各角色选择具名 profile；通用 GraphX prompt 不再无条件嵌入订单域分析 profile。因此 H-002 不再有规范或实现阻塞。

### 9.3 全部原审查项状态

| 项目 | 最终状态 | 关键依据 |
|---|---|---|
| R-001 | **关闭** | 四个独立角色统一触发 GraphX observation，参数化 conformance 覆盖通过 |
| R-002 | **关闭** | 单一 mention 运行时实现 + Node 行为测试覆盖连续切换和历史 stacked mentions |
| R-003 | **关闭** | 初始化无外部 API I/O；显式资源测试按资源、幂等修复旧 catalog |
| H-001 | **关闭** | 两条 legacy pipeline 及其无调用 Service 构造依赖均清除 |
| H-002 | **关闭** | 稳定版本化 Prompt Profile、通用 GraphX 去业务硬编码、GX-HARNESS-012 spec registry 闭环 |

### 9.4 本轮独立验证

```text
cd /home/wangling/develop_team/graphx/apps/web
npm test
# 1 passed

npm run build
# tsc -b && vite build：通过，32 modules transformed

cd /home/wangling/develop_team/graphx
.venv/bin/python -m pytest -q \
  tests/conformance/test_dynamic_agent_task_graph.py \
  tests/conformance/test_supervisor_chat_ui.py \
  tests/conformance/test_api_connection_catalog.py \
  tests/test_harness_executor.py \
  tests/test_role_policy.py \
  tests/test_spec_contract.py
# 39 passed, 14 subtests passed in 8.76s

.venv/bin/python -m pytest -q \
  tests/test_runtime.py tests/test_role_runtime.py \
  tests/test_runtime_contract_schemas.py tests/test_model_runtime_config.py \
  tests/test_spec_contract.py
# 14 passed in 0.97s

.venv/bin/python -m compileall -q src scripts
.venv/bin/python -m json.tool spec/conformance/requirements.json >/dev/null
git diff --check
# 均通过
```

上述是 Reviewer 本轮独立复跑的子集；orchestrator 交接的更宽验证结果为相关 Python `45 passed + 14 subtests`、runtime/spec `28 passed`，与本轮结果一致，无失败证据。

### 9.5 剩余非阻塞风险与后续建议

1. **Prompt digest 行为测试仍可增强**：当前测试和代码结构足以证明实现符合 GX-HARNESS-012，但后续可增加一个直接性质测试——改变 objective/history 只改变 rendered prompt、不改变 `prompt_digest`；改变 profile version/instructions 必须改变 digest。该建议是防回归增强，不影响本次关闭 H-002。
2. **前端角色定义仍有多处类型/显示映射**：运行时正则已集中，但 `entryMention.d.mts` 的 `EntryRole`、`api.ts` 的 `AgentRole` 与 UI label 映射仍需人工同步。未来新增角色时可从一份只读角色表生成类型与匹配规则；当前 build 和行为测试均通过，不构成 R-002 复开。
3. **API catalog 可补并发幂等测试**：现有测试证明串行重复调用不重扫、不重复；若未来允许同一 Resource 的并发 test 请求，建议验证两个并发修复不会因确定性 operation ID 竞争而暴露事务错误。当前 UI 会禁用重复点击，且原 R-003 的启动阻塞已解除，因此列为后续韧性测试。

本轮没有发现需要继续修改 GraphX 的阻塞问题；建议 orchestrator 在既有验证记录完整的前提下进入后续交接，而不是继续扩大本次优化范围。
