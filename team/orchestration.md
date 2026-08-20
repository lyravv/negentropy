# 编排指南（Orchestration）

> 本文件回答：**如何用一个主 agent（编排者）+ 多个角色 sub-agent 实际跑起 negentropy 团队。**
> 适用于任何支持 sub-agent 的 agent 框架（DSH、Claude Code 等）。核心思想：**编排者只负责路由与把关，角色 sub-agent 负责产出。**

## 角色分工

- **编排者（orchestrator）= 主 agent**：
  - 不亲自写业务文档，只负责：立项、按 `workflow.md` 推进阶段、把任务派给正确的角色 sub-agent、评审产出、路由 handoff、管理 `open-questions`、主持复盘。
  - 是**唯一**能改 `team/` 和 `evolution/` 的角色（团队自身演进）。
- **角色 sub-agent**：每次按需启动，扮演一个角色，读章程 + 上游文档，产出本角色文档，然后结束。

## 继续一个已有项目（Resume / 跨 agent 互通）

> 团队不仅支持"从零立项"，也支持**任意 agent 在任意时刻接手继续**。这是跨 agent 互通的核心。

**触发**：收到「使用 negentropy 定义的多agent角色，继续 `<project>` 的开发工作」这类
**只有一句话、不带进度/背景**的指令。

**编排者接手步骤（固定）**：
1. 读 `projects/<project>/STATE.md`——该项目的**单一"当前状态 + 下一步"入口**。
   它给出：��码仓库位置、规范事实源、当前阶段、**精确下一步动作**、关键约束、Bootstrap 顺序。
2. 按 `STATE.md` 的「Bootstrap 顺序」读团队入口、代码仓库 `AGENTS.md`、规范事实源、
   以及规范里的权威"下一步清单"（如 graphx 的 `spec/06`「Continue in this order」）。
3. 跑基线测试确认全绿（`STATE.md` 会给出确切命令与环境变量）。
4. 按「下一步动作」派对应角色 sub-agent（用下方"派活的标准 Prompt 结构"）。
5. 收尾时**必须更新 `STATE.md`**（当前状态 + 下一步）+ 规范里的交接文档 + 提交推送。

**约定**：
- 每个项目工作区根目录**必须**有 `STATE.md`；它是"可续接"的标志。
- `STATE.md` 由编排者维护，是"我们在哪 + 下一步"的权威快照；规范仓库里的交接文档
  （如 graphx `spec/06`）是产品级细节，两者需保持一致（`STATE.md` 是摘要 + 指针）。
- 角色 sub-agent **不需要**看到整个项目历史，只需要：章程 + 技能 + 协议 + 上游 APPROVED 文档
  + `STATE.md` 指派的本次任务。这样任何 agent 都能以小上下文、可并行地接手。

## 派活的标准 Prompt 结构

给某个角色 sub-agent 的任务提示，固定包含以下部分（编排者照此拼装）：

```
【角色】你是 negentropy 团队的 <角色名>（<role-id>）。
【章程】先完整阅读并遵守：<repo>/team/roles/<role-id>/AGENT.md
【技能】再阅读你的技能与偏好：<repo>/team/roles/<role-id>/skills.md
【协议】遵守协作协议：<repo>/team/protocols/<CURRENT 指向的版本>.md
【项目】项目工作区：<repo>/projects/<project>/
【输入】你的上游输入（已 APPROVED）：<列出文档路径>
【任务】<本次具体要做什么，对应 workflow.md 的哪个阶段>
【产出】把结果写到：<目标文档路径>，文档头部按协议填好 status/version/upstream/downstream，
       正文开头写"交接说明"块。
【边界】只产出你职责内的文档；发现问题写 open-questions.md 并打回，不要擅自改上游文档。
【完成标准】满足 AGENT.md 中本阶段的 Definition of Done 后，汇报产出路径与关键决策。
```

## 阶段驱动（对应 workflow.md）

```
编排者
  │  阶段0 立项：建项目工作区，写 project-brief.md
  ▼
启动 business-liaison sub-agent  → 产出 01-business/*
  │  编排者评审 → APPROVED
  ▼
启动 product-manager sub-agent   → 产出 02-requirements/*
  │  评审 → APPROVED
  ▼
启动 architect sub-agent         → 产出 03-architecture/*
  │  评审 → APPROVED
  ▼
并行启动 frontend-engineer ∥ backend-engineer sub-agent  → 代码 + 04-implementation/*
  │  两者都完成 → 评审
  ▼
启动 test-engineer sub-agent     → 产出 05-testing/*
  │  有缺陷 → 打回对应实现角色（可多轮）
  │  无阻塞缺陷 → APPROVED
  ▼
启动 devops-engineer sub-agent   → 产出 06-ops/*
  ▼
编排者主持复盘 → 07-retro/* + 回写 skills.md + evolution/CHANGELOG.md
```

## 并行与反馈

- **并行**：阶段 4 的前后端 sub-agent **同时启动**（互不依赖，以 `api-spec.md` 为契约）。
  其他阶段默认串行（下游依赖上游 APPROVED）。
- **反馈回路**：下游 sub-agent 发现问题时，不直接改上游，而是写 `open-questions.md` 并汇报给编排者；
  编排者据此**重新启动**上游角色 sub-agent 做修订。
- **多轮**：测试→修复→回归可能多轮，每轮都是"启动实现角色 sub-agent 修缺陷 → 启动测试角色 sub-agent 回归"。

## 评审（编排者的把关）

编排者收到角色产出后，按该角色 `AGENT.md` 的"质量标准"检查：
- 文档头部字段齐全、状态正确？
- 交接说明块清晰？
- 是否满足 Definition of Done？
- 是否越界（改了不该改的文档）？
- 未决问题是否都进了 `open-questions.md`？

不达标 → 打回该角色 sub-agent 重做（附上具体问题）；达标 → 置 `APPROVED`，进入下一阶段。

## 上下文管理（重要）

- 角色 sub-agent **不需要**看到整个项目历史，只需要：章程 + 技能 + 协议 + 上游 APPROVED 文档 + 本次任务。
  这样每个 sub-agent 上下文小、专注、可并行。
- 编排者维护全局视图（哪些文档什么状态、有哪些 open questions），是团队的"记忆中枢"。
- 若框架支持，优先用**继承上下文的 fork** 给需要"接着上次改"的角色（如缺陷修复轮），
  用**全新 sub-agent** 给首次执行某阶段的角色。

## 一次最小完整运行（示例）

```
1. 编排者：cp -r projects/_template projects/demo-api；写 project-brief.md（APPROVED）
2. 编排者 → business-liaison：产出 business-brief.md + glossary.md
3. 编排者评审 → APPROVED
4. 编排者 → product-manager：产出 requirements.md + user-stories/ + iteration-plan.md
5. 编排者评审 → APPROVED
6. 编排者 → architect：产出 architecture.md + api-spec.md + data-model.md
7. 编排者评审 → APPROVED
8. 编排者 → [frontend ∥ backend]：实现 + 各自 notes
9. 编排者评审 → APPROVED
10. 编排者 → test-engineer：test-plan + 执行 + defect-log + test-report
11. （若有缺陷）编排者 → 对应实现角色修复 → 回到 10 回归
12. 编排者 → devops-engineer：deployment.md + release-notes.md
13. 编排者：复盘，回写 skills.md，记 evolution/CHANGELOG.md
```
