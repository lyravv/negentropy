# 团队变更日志（CHANGELOG）

> 记录 **negentropy 团队自身**的所有结构性变更（不是项目变更）。
> 项目变更记在各项目工作区；这里只记"团队怎么变的"。
> 格式：日期 · 类型 · 变更 · 原因。类型：`role` 角色 / `workflow` 流程 / `protocol` 协议 / `template` 模板 / `skill` 技能 / `other`。

## [0.3.0] - 2026-08-21
### Added
- `workflow`：新增 `team/philosophy.md`，确立“最低充分秩序”、按风险唤醒角色、边界对齐、治理强度随不可逆性提升，以及治理建议的成本/删除审查。
- `role`：把 orchestrator 升为第 8 个正式角色，增加章程、技能、职责边界和 DoD。
- `workflow`：增加 `full/existing-spec/feature/bugfix/spike/ops-only` 六种 profile；GraphX 正式使用 `existing-spec`。
- `workflow`：增加 `WORKBOARD.md`、工作认领、base revision、写入 scope、lease、冲突处理和集成门禁。
- `protocol`：增加统一治理矩阵，区分作者/reviewer/approver/orchestrator；拆分文档、项目、阶段、工作项、Q/C 状态。
- `protocol`：增加 inspect/draft/implement/integrate/publish action mode，明确实现不自动授权 commit/push/deploy。
- `other`：增加 `team.schema.json` 和 `scripts/validate_team.py`，检查协议指针、角色、owner、状态、frontmatter 与项目控制文件。
- `other`：profile 增加 stable/beta/experimental 成熟度；高风险 artifact 的最小审批策略进入 `team.yaml`。

### Changed
- 当前协议升级到 `v1.1-docs`，旧 v1 兼容读取；新增 revision、审批和验证证据字段。
- “git 是全部事实的单一来源”调整为“每类事实有唯一权威来源”，跨仓引用必须带 revision。
- handoff 收尾取消强制 commit/push，外部副作用只在明确 publish 授权下执行。
- 模板补充审批字段；STATE 与 WORKBOARD 分离项目快照和并发认领。
- `team.yaml` 成为状态、action mode、profile 成熟度和审批策略的结构化权威来源；Markdown 只解释语义。
- 校验器按表头解析 WORKBOARD/open-questions，畸形行不再静默通过；schema 增加角色目录、阶段归属、profile 和审批策略检查。

### Migration
- GraphX 的现有未提交代码/文档变更全部视为受保护 worktree；迁移不覆盖其内容。
- 历史文档缺新 frontmatter 字段只产生 warning，下次实质修改时补齐，避免活跃项目一次性断裂。

## [0.2.2] - 2026-08-21
### Changed
- `workflow`：**明确复盘节奏**（阶段 7）。默认**项目结束**做一次完整复盘；**不做自动增量复盘**
  （避免过拟合单个项目）；但**用户/编排者可随时主动触发一次"按需复盘"**（针对具体问题/切片），
  流程同上、范围限定在触发点，回写 `skills.md`/`CHANGELOG.md` 并在 `07-retro/` 留带日期记录。
- 原因：长期项目若只等"结束"才复盘，团队成长滞后；但自动增量又易过拟合。折中为"默认项目结束 + 按需手动触发"。

## [0.2.1] - 2026-08-21
### Changed
- `workflow`/`template`：**把"交接/续接机制"收敛为团队能力单一事实源 `team/handoff.md`**，
  落实"团队能力沉淀到团队、项目内容用机制在项目同步"的原则。
  - 新增 `team/handoff.md`：核心原则（团队能力 vs 项目内容）+ STATE.md 约定 + Bootstrap 顺序(模式)
    + 收尾清单(模式) + 团队级约束 + 新/接手两条路径。
  - `team/orchestration.md` Resume 节、`README.md` Continue 节 → 缩成**入口指针**，指向 `handoff.md`，不再重复流程。
  - `projects/_template/STATE.md` 与 `projects/graphx/STATE.md` → **纯化**为"项目内容 + 续接指针"，
    删除原先重复的 Bootstrap 顺序 / 收尾清单 / 团队级约束。
- 原因：此前 Bootstrap/收尾/团队级约束在 orchestration、模板、各项目 STATE.md 三处重复，
  改一处需同步多处。收敛后改团队流程只改 `handoff.md`，所有项目经指针自动生效。

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
