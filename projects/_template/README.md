# 项目工作区模板（_template）

> 开新项目时：`cp -r projects/_template projects/<project-name>`，然后删掉本文件。
> 本目录是项目工作区的骨架，阶段目录按 `team/workflow.md` 编号。

## 目录约定
```
<project-name>/
├── README.md              # 项目说明（本文件，开项目后改写）
├── STATE.md               # ★ 单一"当前状态 + 下一步"入口（跨 agent 续接靠它，编排者每轮更新）
├── WORKBOARD.md           # 写任务认领、lease、范围与集成状态
├── open-questions.md      # 全局未决问题/变更登记簿（从模板复制）
├── 00-intake/
│   └── project-brief.md   # 立项简报（编排者填）
├── 01-business/           # business-liaison 产出
├── 02-requirements/       # product-manager 产出（含 user-stories/）
├── 03-architecture/       # architect 产出
├── 04-implementation/     # frontend ∥ backend 产出（代码另放，notes 在此）
├── 05-testing/            # test-engineer 产出
├── 06-ops/                # devops-engineer 产出
└── 07-retro/              # 复盘
```

> **`STATE.md` 是续接入口，`WORKBOARD.md` 是写入互斥入口**。任何 agent 收到“继续项目”时先读两者；
> 任何写任务先按 `team/concurrency.md` 认领。

## 项目信息
- 项目名：<project-name>
- 启动日期：YYYY-MM-DD
- 当前阶段：<stage>
- 项目状态：ACTIVE / PAUSED / BLOCKED / COMPLETED / ARCHIVED
- workflow profile：full / existing-spec / feature / bugfix / spike / ops-only
