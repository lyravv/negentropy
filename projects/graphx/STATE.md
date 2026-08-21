---
title: GraphX 项目当前状态与下一步（STATE · 项目内容）
role: orchestrator(维护)
status: ACTIVE
version: 2.0
updated: 2026-08-21
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
| 项目 | GraphX（Graph-first 超图工作台），产品版本 **0.5.7** |
| 代码仓库 | `/home/wangling/develop_team/graphx`（分支 `feat/trusted-build-core`，base `cf7f9e0` + **WORKTREE**；现有修改受保护，未声明已推送） |
| 规范事实源 | `/home/wangling/develop_team/graphx/spec/`（APPROVED，**单一事实源**，覆盖一切历史聊天/原型） |
| 工作流 | `existing-spec`（阶段 1–3 由 `graphx/spec/` 的精确 revision 替代） |
| 团队 | negentropy（8 角色，协议 `v1.1-docs`），定义在 `/home/wangling/develop_team/negentropy` |
| 当前阶段 | 阶段 4（实现）+ 阶段 5（测试）已交付用户反馈修复轮（GX-APP-015/016/017/018）；阶段 6（发布）待用户在宿主机执行重新部署 |
| 测试状态 | **全量 154 passed + 12 subtests 全绿**（2026-08-21 重跑，含 GX-APP-015/016/017/018 4 条合规用例） |
| 运行应用 | `http://10.54.56.113:8001/`（**跑的是旧代码**，本轮 5 条修复生效需用户在宿主机执行 `scripts/redeploy_alpha.sh --clear-graphs`，见阶段 6） |
| 下一步 | ① 用户在宿主机执行 `scripts/redeploy_alpha.sh --clear-graphs`（重新部署 + 清空全部现有 Graph，用户已授权）② 部署后复验 5 条反馈 ③ 关闭 Q-002/OQ-016 凭据隔离门禁（Builder 实跑前置）④ 用已绑定套件执行 30 条盲评并冻结 Tester 输出 |

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
| 4 实现 | frontend ∥ backend | **部分完成** | 用户反馈修复轮（GX-APP-015/016/017/018）已交付；真实 Builder 会话被 OQ-016 阻塞 |
| 5 测试 | test-engineer | **部分完成** | 本轮 4 条合规用例 + 全量 154 passed 通过；**30 条业务盲评运行时执行 + 输出冻结未做** |
| 6 发布 | devops-engineer | **进行中** | `scripts/redeploy_alpha.sh` 已就绪，已在 8002 临时实例验证 5 条行为；**待用户在宿主机执行 `--clear-graphs`**（沙箱无法 signal 宿主机进程）；Postgres 迁移未做 |
| 7 复盘 | orchestrator | 未开始 | |

> 说明：阶段 1–3 按 `existing-spec` 合法裁剪为 `SKIPPED`，由 `graphx/spec/` 的当前 revision 替代
> （`spec/` 是单一事实源）。本工作区只承载团队协作文档（notes/测试三件套/问题登记），不复制规范。

## 下一步动作（权威完整清单在 `graphx/spec/06`「Continue in this order」）

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
- 应用 `10.54.56.113:8001` 跑旧代码，本轮 5 条修复生效需用户在宿主机执行 `scripts/redeploy_alpha.sh --clear-graphs`（阶段 6，devops）。
- 前端 `pushGraph`/`send` 失败路径的 toast 同样会被后续 `refresh()` 清除（与本轮已修复的 `deleteGraph` 同型），留作后续项。
- 真实 provider 的 agent-chat（GX-APP-017）与多轮 design Build（GX-APP-016）本轮以确定性 fake harness 验证；真实 DeepSeek Harness 端到端为后续项。

## 续接指针

- **Bootstrap 顺序 / 收尾清单 / 团队级约束 / STATE.md 约定**：见 `team/handoff.md`（团队能力单一事实源）。
- **工作认领 / lease / 写入范围**：见 `projects/graphx/WORKBOARD.md`；开始下一项写任务前先认领。
- **本项目基线命令**：`cd /home/wangling/develop_team/graphx && UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest -q`（当前 **154 passed + 12 subtests**，2026-08-21 验证，base `db3d118` + 本轮 WORKTREE）。
