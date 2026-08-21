---
title: 交接与续接机制（Handoff / 团队能力）
role: orchestrator(维护)
status: APPROVED
version: 1.0
updated: 2026-08-21
upstream: [team/workflow.md, team/orchestration.md]
downstream: [每个项目的 STATE.md, 任何接手项目的 agent]
---

# 交接与续接机制（Handoff）

> **这是 negentropy 团队的一项正式能力**：让**任意项目**（从头开始或中途接手）、
> 由**任意 agent 框架**（DSH / Claude Code / Cursor / 自研）在**只有一句话、不带进度/背景**
> 的指令下，都能自举接手并持续开发。
> 本文件是该机制的**单一事实源**（团队能力）。各项目的 `STATE.md` 只承载**项目内容**，
> 并指向本文件，**不重复**本文件里的流程与团队级约束。

## 0. 核心原则：团队能力 vs 项目内容

> **团队能力 → 沉淀到团队（本文件 + `team/` 其他文档）；项目内容 → 用机制在项目 `STATE.md` 同步。**

| 类别 | 归属 | 例子 |
|---|---|---|
| **团队能力**（怎么开发/怎么续接/怎么收尾，对所有项目通用） | **团队**（本文件、`workflow.md`、`orchestration.md`、`_template/`） | Bootstrap 顺序、收尾清单、团队级约束、STATE.md 约定、派活 prompt 结构、角色章程 |
| **项目内容**（这个项目的状态/下一步/专属约束） | **项目**（`projects/<name>/STATE.md` + 项目工作区 + 规范仓库） | 当前阶段、精确下一步、代码仓库路径、规范事实源、基线命令、项目专属约束、已知遗留 |

判定口诀：**"换一个项目还成立吗？"** 成立 → 团队能力（放团队）；不成立、只对这个项目成立 → 项目内容（放 STATE.md）。

## 1. STATE.md 约定（每个项目工作区根目录必须有）

`STATE.md` 是该项目**单一"当前状态 + 下一步"入口**，由编排者每轮收尾更新。它是"可续接"的标志。
**只放项目内容**，流程与团队级约束指向本文件。必备章节：

| 章节 | 内容（项目内容） |
|---|---|
| 30 秒速览 | 项目一句话、代码仓库(路径+分支)、规范事实源(路径)、当前阶段、测试状态(计数+命令)、下一步一句话 |
| 当前状态 | 按 `team/workflow.md` 阶段的状态表（哪些 DONE / 部分完成 / 未开始） |
| 下一步动作 | **精确**的下一步：做什么、派哪个(些)角色、输入/前置/排除项；权威完整清单指向规范仓库的交接文档 |
| 本轮已交付 | 本轮各角色产出 + 对应提交 |
| 项目专属约束 | **只列这个项目特有的**约束（如 graphx 的变更协议、工程铁律、产品形态）；团队级约束见本文件 §4 |
| 已知遗留 | 非阻塞的遗留风险 |
| 续接指针 | 一行：「Bootstrap 顺序 / 收尾清单 / 团队级约束见 `team/handoff.md`」+ 本项目基线命令 |

> 不要在 STATE.md 里重复 Bootstrap 顺序 / 收尾清单 / 团队级约束——那是团队能力，改一处即全局生效。

## 2. Bootstrap 顺序（团队能力 · 接手项目的固定步骤）

> 触发：收到「使用 negentropy 定义的多agent角色，继续 `<project>` 的开发工作」这类单句指令。
> 下面是**通用模式**；具体路径/命令由项目 `STATE.md` 提供。

1. 读 `projects/<project>/STATE.md`——拿到"在哪 + 下一步 + 项目专属约束 + 基线命令"。
2. 读团队入口：`README.md` + 本文件（`team/handoff.md`）+ `team/orchestration.md`（如何派角色）。
3. 读代码仓库的 `AGENTS.md`（工程铁律 + 变更协议）——路径见 STATE.md。
4. 读规范事实源（按其 `README.md` 指定顺序读相关规范）——路径见 STATE.md。
5. 读规范仓库里权威的"下一步清单"（如 graphx `spec/06`「Continue in this order」）。
6. 跑基线测试确认全绿——命令见 STATE.md（含所需环境变量）。
7. 按 STATE.md「下一步动作」派对应角色 sub-agent（用 `orchestration.md` 的标准 prompt 结构；
   阶段 4 前后端可并行，阶段 5 测试在实现完成后）。
8. 收尾：按本文件 §3 收尾清单执行。

## 3. 收尾清单（团队能力 · 每轮结束编排者执行）

1. 更新项目 `STATE.md`（当前状态 + 下一步）+ 规范仓库的交接文档（两者保持一致）。
2. 更新需求状态（如 `requirements.json`）+ 版本清单（如 `manifest.yaml`）。
3. 跑全量测试 + `git diff --check`（必须全绿、无空白错误）。
4. 提交代码仓库（`type:scope` 小提交）+ 推送 origin。
5. 提交 negentropy 项目工作区变更（`projects/<project>/`）。
6. 最终交接留下**分支/提交 + 精确下一步**。

## 4. 团队级约束（对所有项目通用，违反即停）

- **机密**：Token / 数据库连接 / 代理配置**不得**打印、写入 Git、进入项目数据/提示/Trace/日志。
- **不覆盖**：动手前 `git status` 检查，不覆盖用户已有未提交修改。
- **范围**：所有工作材料只放在受控开发目录下（graphx 为 `/home/wangling/develop_team`）。
- **变更协议**：任何行为修改必须**同一变更**内同步 规范 + 测试 + 交接（具体协议见各项目 `AGENTS.md`）。
- **不重新设计产品形态**：按各项目规范既定的产品心智模型推进，不擅自扩张 UI/流程。
- **环境**：用项目指定的包管理器/缓存（graphx 为 uv + `UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv`，
  系统 uv 缓存只读）。

> 项目**专属**约束（如 graphx 的"Agent 不得直接写正式 Graph revision""Apply 永不作为 Agent 工具"等）
> 写在该项目 `STATE.md` 的「项目专属约束」，不写在这里。

## 5. 两条路径

### 从头开始（New）
1. `cp -r projects/_template projects/<name>`（模板已含 `STATE.md` 骨架）。
2. 填 `STATE.md`（项目内容）+ `00-intake/project-brief.md`（APPROVED）。
3. 按 `team/workflow.md` 阶段推进，每阶段派对应角色（`orchestration.md` 标准 prompt）。
4. 每轮收尾按 §3 更新 `STATE.md`。

### 接手继续（Resume）
按 §2 Bootstrap 顺序执行。`STATE.md` 是入口，本文件是流程，规范仓库是事实源。

## 6. 演进

- 本机制是团队能力，变更记入 `evolution/CHANGELOG.md`（类型 `workflow`/`template`）。
- 改 Bootstrap/收尾/团队级约束 → 只改本文件，所有项目经指针自动生效（不逐个改 STATE.md）。
- 改某项目的状态/下一步 → 只改该项目 `STATE.md`（项目内容）。
