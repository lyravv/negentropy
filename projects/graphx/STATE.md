---
title: GraphX 项目当前状态与下一步（单一入口 / STATE）
role: orchestrator(维护)
status: LIVE
version: 1.0
updated: 2026-08-20
upstream: [graphx/spec/06-testing-and-handoff.md]
downstream: [任何被要求"继续 graphx 开发"的 agent]
---

# GraphX · 当前状态与下一步（STATE）

> **这是"继续 graphx 开发"的单一入口。**
> 任何 agent（DSH / Claude Code / Cursor / 自研引擎）收到
> **「使用 /home/wangling/develop_team/negentropy 定义的多agent角色，继续 graphx 的开发工作」**
> 时，**先读本文件**，按下方「Bootstrap 顺序」执行即可，**无需额外背景或进度信息**。
> 本文件由编排者（orchestrator）在每轮收尾时更新，是"我们在哪 + 下一步做什么"的权威快照。

## 30 秒速览

| 项 | 值 |
|---|---|
| 项目 | GraphX（Graph-first 超图工作台），产品版本 **0.5.7** |
| 代码仓库 | `/home/wangling/develop_team/graphx`（分支 `feat/trusted-build-core`，已推送 origin） |
| 规范事实源 | `/home/wangling/develop_team/graphx/spec/`（APPROVED，**单一事实源**，覆盖一切历史聊天/原型） |
| 团队 | negentropy（7 角色，协议 `v1-docs`），定义在 `/home/wangling/develop_team/negentropy` |
| 当前阶段 | 阶段 4（实现）+ 阶段 5（测试）已交付 GX-APP-012/013/014 |
| 测试状态 | **126 passed + 12 subtests 全绿**（`uv run pytest -q`） |
| 运行应用 | `http://10.54.56.113:8001/`（**跑的是旧代码**，新特性生效需重启/重新部署，见阶段 6） |
| 下一步 | 用私有语料跑 Builder 提议关系与语义超边（见「下一步动作」第 1 条） |

## Bootstrap 顺序（新 agent 照此执行，逐步）

1. 读本文件（`STATE.md`）——拿到"在哪 + 下一步 + 约束"。
2. 读团队入口 `/home/wangling/develop_team/negentropy/README.md` 与
   `team/orchestration.md`——如何把任务派给角色 sub-agent（标准 prompt 结构）。
3. 读代码仓库 `/home/wangling/develop_team/graphx/AGENTS.md`——工程铁律 + 变更协议。
4. 读规范事实源 `/home/wangling/develop_team/graphx/spec/README.md`，**按其指定顺序**读相关规范。
5. 读 `/home/wangling/develop_team/graphx/spec/06-testing-and-handoff.md` 的
   **「Continue in this order」**——权威下一步清单（本文件「下一步动作」是它的摘要）。
6. 跑基线确认全绿：
   `cd /home/wangling/develop_team/graphx && UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest -q`
7. 按「下一步动作」派对应角色 sub-agent（用 `orchestration.md` 的标准 prompt 结构；
   阶段 4 前后端可并行，阶段 5 测试在实现完成后）。
8. 收尾：按「收尾清单」更新本文件 + `spec/06` + 提交推送。

## 当前状态（按 `team/workflow.md` 阶段）

| 阶段 | 负责角色 | 状态 | 说明 |
|---|---|---|---|
| 0 立项 | orchestrator | DONE | `00-intake/project-brief.md` APPROVED |
| 1 业务 | business-liaison | DONE（由 graphx/spec 固化） | `spec/01` 产品范围 |
| 2 需求 | product-manager | DONE（由 graphx/spec 固化） | `spec/01/09/10/12` |
| 3 架构 | architect | DONE（由 graphx/spec 固化） | `spec/02/05/08` + `spec/contracts` |
| 4 实现 | frontend ∥ backend | **部分完成** | GX-APP-012/013/014 已交付；**私有语料 Builder 构图未做** |
| 5 测试 | test-engineer | **部分完成** | GX-APP-012/013/014 合规测试通过；**30 条盲评未跑** |
| 6 发布 | devops-engineer | 未开始 | 需重启/重新部署 `10.54.56.113:8001`；Postgres 迁移 |
| 7 复盘 | orchestrator | 未开始 | |

> 说明：阶段 1–3 的"业务/需求/架构"文档不在本工作区，而是由 `graphx/spec/` 固化并 APPROVED
> （`spec/` 是单一事实源）。本工作区只承载团队协作文档（notes/测试三件套/问题登记），不复制规范。

## 下一步动作（权威完整清单在 `graphx/spec/06`「Continue in this order」）

1. **（当前）** 用私有语料跑 Builder 提议 table-table 关系与语义超边；**不直接抄历史 demo 对象**。
   - 角色：backend-engineer（驱动 Builder 执行）+ test-engineer（验证）。
   - 私有语料（Git 外）：`/home/wangling/develop_team/graph_poc_doc/`
     （`sql_templates/` 13 个 SQL 模板、`hyperedges/` 业务证据、`selected_30_questions.csv`、
     `connection_info.md.txt` 为**排除项**，内容不得读/哈希/入 manifest）。
   - 业务问题盲评套件：`/home/wangling/develop_team/runtime/graphx-eval/`（Git 外）。
2. 独立 Reviewer 检查 join key、数量/状态语义、红蓝记账规则、证据覆盖、缺失员工源。
3. 把确定性静态套件绑到 `test_run`，跑完 30 条盲评用例，**冻结 Tester 输出**后评估者才读 golden。
4. 通过原生插件提交真实 ReviewReport / TestReport，冻结其脱敏验证 trace。
5. 加 SELECT-only 数据库工具，对 golden 标签做执行验证。
6. 把 provider 认证移出 Agent/Bash 安全域，再摄取不可信第三方代码/文档，并证明真实 Token 不可读。
7. 用业务材料验证可运行工作台旅程，按用户反馈细化 graph/file/chat/merge 行为。
8. 用原生 Harness 角色会话替换轻量 Build 执行器（保持 Candidate Apply 用户可控）。
9. 把应用投影变更迁移到可执行 HGT Patch，实现规范持久 Graph store、授权、审批、outbox、原子 Apply。
10. 组织库后续：只读"从组织库添加"端点、可选推送去重、Postgres `org_library_graphs` 迁移。

## 关键约束（任何 agent 必须遵守，违反即停）

- **uv 环境**：依赖 `uv sync` 管理；**必须带 `UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv`**
  （系统 uv 缓存 `/home/wangling/.cache/uv` 只读，不带会报 Read-only file system）。
- **机密**：Token、数据库连接、代理配置**不得**打印、写入 Git 或进入 Graph 数据/提示/Trace/日志。
- **不覆盖**：动手前 `git status` 检查，不覆盖用户已有未提交修改。
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

## 本轮已交付（阶段 4–5，GX-APP-012/013/014）

| 角色 | 产出 | 状态 |
|---|---|---|
| backend-engineer | `04-implementation/backend-notes.md`（删除 + 推送 + `bootstrap.org_library`） | APPROVED |
| frontend-engineer | `04-implementation/frontend-notes.md`（菜单动作 + Add 弹窗 + 画布合规测试） | APPROVED |
| test-engineer | `05-testing/{test-plan,defect-log,test-report}.md`（9 条合规用例，结论**可发布**） | APPROVED |
| orchestrator | `open-questions.md`（Q-001 已 RESOLVED：删除 `confirmed` 缺失/非 true 一律 409） | — |

对应 graphx 提交（`feat/trusted-build-core`，已推送）：
`c84cef6` 后端 / `7a7741e` 前端+画布 / `00b95c9` 合规测试 / `475bb87` 规范+交接。

## 收尾清单（每轮结束，编排者执行）

1. 更新本文件（当前状态 + 下一步）与 `graphx/spec/06`（delivered / limitations / continue）。
2. 更新 `spec/conformance/requirements.json` 状态 + `spec/manifest.yaml`。
3. 跑全量测试 + `git diff --check`（必须全绿、无空白错误）。
4. 提交 graphx 仓库（`type:scope` 小提交，如 `feat:`/`test:`/`docs:`）+ 推送 origin。
5. 提交 negentropy 项目工作区变更（本目录）。
6. 在最终交接里留下**分支/提交 + 精确下一步**。

## 已知遗留（非阻塞，详见 `05-testing/test-report.md` 第 4 节）

- Postgres 需补 `org_library_graphs` 建表迁移（SQLite 由 `create_all` 自动建表）。
- 组织库无 Add/删除/更新端点（Add 弹窗仅只读展示）；重复推送不去重。
- 画布合规测试为源码级断言（锁定渲染形态不回退），非 DOM 级视觉验证。
- 推送后本地副本归属为产品决策（`spec/07` OQ-017，默认保持 `Mine · editable`）。
- 应用 `10.54.56.113:8001` 跑旧代码，删除/推送生效需重启/重新部署（阶段 6，devops）。
