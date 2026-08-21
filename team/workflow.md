# 工作流（Workflow）

工作流由阶段模型和可裁剪 profile 组成。默认 profile 是 `full`；已有批准规范的 GraphX 使用 `existing-spec`。profile 的 stable/beta/experimental 成熟度以 `team.yaml` 为准，实验性表示结构已定义但尚未被真实项目完整验证。详细裁剪规则见 `workflow-profiles.md`，状态和批准权见 `governance.md`，取舍遵循 `philosophy.md`。

## 阶段模型

| 阶段 | ID | 负责人 | 最小出口证据 |
|---|---|---|---|
| 0 立项 | `intake` | orchestrator | STATE、WORKBOARD、项目简报、profile 与事实源 revision |
| 1 业务 | `business` | business-liaison | 已批准业务规则和术语，或经登记的替代事实源 |
| 2 需求 | `requirements` | product-manager | 已批准需求/验收标准，或经登记的替代事实源 |
| 3 架构 | `architecture` | architect | 已批准架构/契约/数据模型，或经登记的替代事实源 |
| 4 实现 | `implementation` | frontend ∥ backend | scoped 实现、说明、自测及行为同步证据 |
| 5 测试 | `testing` | test-engineer | 可追溯测试、缺陷状态、带 revision 的质量结论 |
| 6 发布 | `release` | devops-engineer | 经授权的部署、冒烟、监控、回滚证据 |
| 7 复盘 | `retrospective` | orchestrator | 复盘和有依据的团队改进行动 |

## 通用 DoR

阶段进入 `IN_PROGRESS` 前必须满足：

- 项目为 `ACTIVE`，profile 已登记；
- 工作项已认领，action mode、base revision、scope、lease 明确；
- 上游是匹配当前 scope/revision 的 `APPROVED` 输入，或 profile 合法登记的替代事实源；
- 目标 worktree 已检查，未知用户修改不会被覆盖；
- 阻塞性 Q/C 已解决或明确隔离在本 scope 外。

## 通用 DoD

- profile 要求的产出与批准证据齐全；
- 规范、契约、实现、测试和交接没有行为矛盾；
- scoped 验证通过；全量验证无法运行时明确原因和风险；
- `git diff --check` 通过；
- WORKBOARD 工作项记录 result revision/`WORKTREE`、验证和遗留；
- STATE 只更新当前事实和精确下一步，不复制完整报告；
- 未经 publish 授权没有 push、部署或外部写入。

## 阶段细则

### 0 立项

选择 profile，登记各类权威来源，创建 STATE/WORKBOARD/open-questions，记录授权模式与基线。新项目的范围由用户/项目负责人批准。

### 1–3 业务、需求、架构

`full` 按顺序产出；`existing-spec/feature/bugfix` 可引用已有规范。替代输入必须精确到 revision，受影响角色确认够用，阶段记 `SKIPPED` 而不是伪造 `DONE` 文档。

### 4 实现

前后端只有在写入范围无重叠、共同契约已批准且依赖独立时并行。行为变化必须在同一工作项/集成批次同步规范、契约、测试与交接；契约疑义先提 C/Q，不在实现里私下约定。

### 5 测试

先验证测试计划，再执行。报告必须记录被测 revision、命令、日期、结果和未覆盖风险。质量结论由 test-engineer 批准；发布接受残余风险由用户/项目负责人决定。

### 6 发布

仅在质量结论允许、发布计划和回滚方案就绪且取得 `publish` 授权后执行。部署与 push 不是实现阶段的默认收尾动作。生产事故按已批准回滚条件先止血，再记录与升级。

### 7 复盘

默认项目/里程碑结束执行；用户可按需触发。只有被多次验证或明确具有通用价值的经验才回写稳定技能；结构性变更进 CHANGELOG。

## 反馈回路

下游引用证据登记 Q/BUG/C，由 orchestrator 路由给事实负责人。关闭和批准按 governance 执行。修订后受影响下游只需重跑影响范围与必要回归，不机械重走无关阶段。
