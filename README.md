# negentropy · 负熵开发团队

> **负熵（negentropy）**：从混沌中建立秩序。
> 这个团队的存在，就是把"模糊的业务诉求"这个高熵状态，一步步降熵成"可运行、可验收、可发布的软件"。
> 每个角色负责消除一类不确定性——业务熵、需求熵、设计熵、实现熵、质量熵、运维熵。

negentropy 是一个**以文档为协作介质、以 git 为单一事实源**的软件开发团队。团队由 7 个角色（sub-agent）组成，
它们的定义、协作协议、技能偏好全部记录在本仓库中——**仓库即团队**。

## 为什么这样设计

| 设计目标 | 做法 |
|---------|------|
| **可移植**（任何地方都能用） | 团队定义是纯 Markdown + YAML，不绑定任何 agent 框架。任何能读文件的 agent（DSH / Claude Code / Cursor / 自研引擎）都能"入队"。 |
| **可演进**（技能偏好逐步调整） | 每个角色有独立的 `skills.md`，随项目复盘持续更新；所有团队变更记入 `evolution/CHANGELOG.md`。 |
| **协作可升级**（文档 → yapi/jira） | 协作协议**版本化**：当前是 `v1-docs`（纯文档），未来可平滑升级到 `v2-tools`（yapi 管接口、jira 管任务），旧版本保留备查。 |
| **机器可读**（可被任意引擎驱动） | `team.yaml` 是结构化的团队清单（角色/阶段/反馈回路）。未来无论用什么语言写编排引擎，解析它即可自动驱动团队；今天没有引擎，人读 Markdown 也能直接跑。 |

## 团队构成

| 角色 | ID | 消除的熵 | 一句话使命 |
|------|----|---------|-----------|
| 业务对接员 | `business-liaison` | 业务熵 | 澄清业务背景、术语、流程及外部依赖 |
| 产品经理 | `product-manager` | 需求熵 | 整理需求、用户故事、验收标准和迭代计划 |
| 架构工程师 | `architect` | 设计熵 | 技术选型、系统设计、接口和数据模型 |
| 前端工程师 | `frontend-engineer` | 实现熵(界面) | 界面、交互与前端测试 |
| 后端工程师 | `backend-engineer` | 实现熵(服务) | 服务、数据库、权限和接口 |
| 测试工程师 | `test-engineer` | 质量熵 | 测试方案、自动化测试、缺陷与回归 |
| 运维工程师 | `devops-engineer` | 运维熵 | 环境、部署、监控、备份和发布 |

每个角色的完整定义在 [`team/roles/<id>/AGENT.md`](team/roles/)，
可演进的技能偏好在同目录的 `skills.md`。

## 目录结构

```
negentropy/
├── README.md                  # 本文件：团队入口
├── team.yaml                  # 机器可读的团队清单（角色/阶段/协议）
├── team/
│   ├── roles/                 # 7 个角色，每个一个目录
│   │   └── <role-id>/
│   │       ├── AGENT.md       # 角色章程：使命/职责/输入输出/决策权/质量标准
│   │       └── skills.md      # 可演进的技能与偏好（随复盘更新）
│   ├── workflow.md            # 流水线：阶段、准入准出、并行与反馈回路
│   ├── protocols/             # 协作协议（版本化）
│   │   ├── CURRENT.md         # 指向当前生效的协议版本
│   │   ├── v1-docs.md         # 当前：纯文档协作
│   │   └── v2-tools.md        # 规划：yapi / jira 集成
│   ├── templates/             # 各交付物的文档模板
│   ├── orchestration.md       # 如何用 sub-agent 实际跑起这个团队
│   └── handoff.md             # ★ 交接/续接机制（团队能力单一事实源：Bootstrap/收尾/团队级约束/STATE.md 约定）
├── projects/                  # 每个项目一个工作区（根目录必有 STATE.md = 续接入口）
│   ├── graphx/                # GraphX 项目（STATE.md 见其根目录）
│   └── _template/             # 项目骨架（开新项目时复制，含 STATE.md 模板）
├── evolution/                 # 团队演进
│   ├── CHANGELOG.md           # 团队变更日志
│   └── roadmap.md             # 规划中的升级
└── .gitignore
```

## 如何开始一个项目

1. 复制项目骨架：`cp -r projects/_template projects/<project-name>`
2. 按 [`team/workflow.md`](team/workflow.md) 的阶段推进，每个阶段由对应角色产出文档
3. 用 [`team/orchestration.md`](team/orchestration.md) 中的方法，把每个阶段派给对应角色的 sub-agent
4. 项目结束后做复盘，把学到的东西写回各角色的 `skills.md`，并在 `evolution/CHANGELOG.md` 记一笔

## 如何"继续"一个已有项目（Continue）

> **这是跨 agent 互通的关键入口。** 任何 agent 收到
> 「使用 `/home/wangling/develop_team/negentropy` 定义的多agent角色，继续 `<project>` 的开发工作」
> 这类**只有一句话、不带进度/背景**的指令时，**直接读 `projects/<project>/STATE.md`**。

分工（**团队能力 vs 项目内容**）：
- **`projects/<project>/STATE.md`** = **项目内容**：代码仓库位置、规范事实源、当前阶段、
  **精确的下一步动作**、项目专属约束、基线命令。由编排者每轮收尾更新。
- **`team/handoff.md`** = **团队能力**（��一事实源）：Bootstrap 顺序、收尾清单、团队级约束、
  STATE.md 约定。对所有项目通用，改一处全局生效。

新 agent 读 `STATE.md`（项目内容）→ 顺指针读 `team/handoff.md`（团队能力）→ 按 Bootstrap 顺序接手，
无需额外上下文。

- 现有项目：`projects/graphx/STATE.md`（GraphX，Graph-first 超图工作台）。
- 约定：每个项目工作区根目录**必须**有 `STATE.md`；编排者每轮收尾必须更新它（见
  `team/handoff.md`）。没有 `STATE.md` 的项目视为未建立可续接状态。

## 如何"入队"（对任何 agent 框架）

任何 agent 想扮演某个角色，只需：
1. 读取 `team/roles/<role-id>/AGENT.md`（章程）和 `skills.md`（技能偏好）
2. 读取 `team/protocols/CURRENT.md` 指向的协作协议
3. 按章程的"输入"读取上游文档，按"输出"产出文档到项目工作区

不需要任何额外配置。仓库就是全部。

## 演进机制

- **技能演进**：每个角色的 `skills.md` 带变更记录，复盘后追加。
- **协议演进**：`protocols/` 下版本化，`CURRENT.md` 是开关。升级协议 = 写新版本 + 改指针。
- **团队演进**：所有结构性变更（加角色、改流程、换协议）记入 `evolution/CHANGELOG.md`，规划写 `evolution/roadmap.md`。

详见 [`evolution/roadmap.md`](evolution/roadmap.md)。
