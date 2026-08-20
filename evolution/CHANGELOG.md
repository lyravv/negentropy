# 团队变更日志（CHANGELOG）

> 记录 **negentropy 团队自身**的所有结构性变更（不是项目变更）。
> 项目变更记在各项目工作区；这里只记"团队怎么变的"。
> 格式：日期 · 类型 · 变更 · 原因。类型：`role` 角色 / `workflow` 流程 / `protocol` 协议 / `template` 模板 / `skill` 技能 / `other`。

## [0.2.0] - 2026-08-20
### Added
- `workflow`/`template`：**跨 agent 续接入口 `STATE.md`**。每个项目工作区根目录新增 `STATE.md`
  （单一"当前状态 + 下一步"入口），由编排者每轮收尾更新。任何 agent 收到"继续 <project> 开发"的
  一句话指令（不带进度/背景）时，直接读 `projects/<project>/STATE.md` 即可接手。
  - `team/orchestration.md` 新增「继续一个已有项目（Resume / 跨 agent 互通）」章节（固定接手步骤 + 约定）。
  - `README.md` 新增「如何"继续"一个已有项目（Continue）」章节 + 目录结构标注。
  - `projects/_template/` 新增 `STATE.md` 模板 + 目录约定说明（新项目天生可续接）。
  - 首个实例：`projects/graphx/STATE.md`（GraphX，含 Bootstrap 顺序 / 当前阶段 / 下一步 / 约束 / 收尾清单）。
- 原因：让"使用 negentropy 定义的多agent角色，继续 graphx 的开发工作"这类**单句、无上下文**指令
  在**任意 agent 框架**中都能自举接手，无需人工再提供进度/背景。

## [0.1.0] - 2025-01-01
### Added
- 团队初始构成：7 个角色（business-liaison, product-manager, architect, frontend-engineer, backend-engineer, test-engineer, devops-engineer）。
- 工作流 `team/workflow.md`：8 阶段流水线 + 反馈回路 + 状态标记。
- 协作协议 v1-docs（纯文档协作），`protocols/CURRENT.md` 指向它。
- 文档模板集 `team/templates/`。
- 编排指南 `team/orchestration.md`。
- 演进机制：本 CHANGELOG + `roadmap.md` + 各角色 `skills.md`。
