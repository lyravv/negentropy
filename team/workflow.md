# 工作流（Workflow）

> 定义一个项目从立项到发布的流水线：每个阶段的**负责人、准入（DoR）、产出、准出（DoD）**，
> 以及阶段间的**并行**与**反馈回路**。
> 编排者（orchestrator，通常是主 agent）按本文件驱动各角色 sub-agent。

## 阶段总览

```
[0 立项] → [1 业务] → [2 需求] → [3 架构] → [4 实现(前端∥后端)] → [5 测试] → [6 发布] → [7 复盘]
                              ↑__________|  反馈回路（见下）
```

| 阶段 | ID | 负责角色 | 产出（相对项目工作区） |
|------|----|---------|----------------------|
| 0 立项 | `intake` | orchestrator | 项目工作区、`00-intake/project-brief.md` |
| 1 业务 | `business` | business-liaison | `01-business/business-brief.md`、`01-business/glossary.md` |
| 2 需求 | `requirements` | product-manager | `02-requirements/requirements.md`、`02-requirements/user-stories/`、`02-requirements/iteration-plan.md` |
| 3 架构 | `architecture` | architect | `03-architecture/architecture.md`、`03-architecture/api-spec.md`、`03-architecture/data-model.md` |
| 4 实现 | `implementation` | frontend-engineer ∥ backend-engineer | 代码 + `04-implementation/frontend-notes.md`、`04-implementation/backend-notes.md` |
| 5 测试 | `testing` | test-engineer | `05-testing/test-plan.md`、`05-testing/defect-log.md`、`05-testing/test-report.md` |
| 6 发布 | `release` | devops-engineer | `06-ops/deployment.md`、`06-ops/release-notes.md` |
| 7 复盘 | `retrospective` | orchestrator | `07-retro/retrospective.md` + 回写各角色 `skills.md` |

## 各阶段细则

### 阶段 0 · 立项（orchestrator）
- **DoR**：有明确的项目诉求（一句话即可，允许模糊）。
- **动作**：`cp -r projects/_template projects/<name>`；填写 `00-intake/project-brief.md`（背景、目标、干系人、约束）。
- **DoD**：项目工作区建立，`project-brief.md` 状态为 `APPROVED`。

### 阶段 1 · 业务澄清（business-liaison）
- **DoR**：`project-brief.md` 已 APPROVED。
- **动作**：澄清业务背景、领域术语、核心流程、外部依赖（第三方系统/合规/数据）。
- **DoD**：`business-brief.md` 与 `glossary.md` 完成，关键业务问题无未决项（或已显式标注为"待业务方确认"并列出）。

### 阶段 2 · 需求（product-manager）
- **DoR**：`business-brief.md` 已 APPROVED。
- **动作**：把业务诉求转成需求清单、用户故事（含验收标准）、迭代计划（优先级 + 里程碑）。
- **DoD**：`requirements.md`、`user-stories/`、`iteration-plan.md` 完成；每个用户故事都有可验证的验收标准。

### 阶段 3 · 架构（architect）
- **DoR**：`requirements.md` 已 APPROVED。
- **动作**：技术选型、系统架构、接口设计（api-spec）、数据模型。
- **DoD**：三份文档完成；接口与数据模型覆盖所有用户故事；选型有理由记录。

### 阶段 4 · 实现（frontend-engineer ∥ backend-engineer，**并行**）
- **DoR**：`architecture.md`、`api-spec.md`、`data-model.md` 已 APPROVED。
- **动作**：
  - 后端：服务、数据库、权限、接口实现。
  - 前端：界面、交互、前端测试。
  - 两者以 `api-spec.md` 为契约并行开发；契约变更必须回到 architect 走变更流程。
- **DoD**：功能按用户故事实现完成；各自 `*-notes.md` 记录实现决策、偏离契约之处、遗留问题。

### 阶段 5 · 测试（test-engineer）
- **DoR**：阶段 4 的 DoD 达成（或达到可测的最小集）。
- **动作**：测试方案、自动化测试、执行、缺陷记录与回归。
- **DoD**：`test-plan.md`、`defect-log.md`、`test-report.md` 完成；阻塞性/严重缺陷已修复并回归通过；测试报告给出"可发布/不可发布"结论。

### 阶段 6 · 发布（devops-engineer）
- **DoR**：`test-report.md` 结论为"可发布"。
- **动作**：环境、部署、监控、备份、发布。
- **DoD**：`deployment.md`、`release-notes.md` 完成；系统上线且监控/备份就绪。

### 阶段 7 · 复盘（orchestrator）
- **DoR**：阶段 6 完成（或项目终止）。
- **动作**：填写 `07-retro/retrospective.md`（做得好/待改进/行动项）；把可复用的经验**回写**到相关角色的 `skills.md`；结构性变更记入 `evolution/CHANGELOG.md`。
- **DoD**：复盘文档完成，行动项有归属。
- **节奏**：默认**项目结束**做一次完整复盘；**不做自动增量复盘**（避免过拟合单个项目）。
  但**用户/编排者可随时主动触发一次"按需复盘"**（针对某个具体问题/切片）：流程同上、范围限定在触发点，
  同样回写 `skills.md`/`CHANGELOG.md`，并在 `07-retro/` 留一份带日期的复盘记录（如 `retrospective-YYYYMMDD-<主题>.md`）。

## 反馈回路（Feedback Loops）

下游发现上游问题时，**不擅自改上游文档**，而是：
1. 在自己的文档中记录问题（引用上游文档的具体位置）；
2. 通过 `open-questions.md` 或 handoff note 打回给上游角色；
3. 上游角色修订后，重新走该阶段的 DoD。

| 从 | 到 | 触发条件 |
|----|----|---------|
| architect | product-manager | 需求不可实现 / 存在歧义 |
| product-manager | business-liaison | 业务背景不足 / 术语冲突 |
| test-engineer | backend-engineer | 后端缺陷 |
| test-engineer | frontend-engineer | 前端缺陷 |
| devops-engineer | backend-engineer | 部署阻塞 / 配置缺失 |

## 状态标记（所有文档通用）

每份文档头部必须有状态：

| 状态 | 含义 |
|------|------|
| `DRAFT` | 起草中 |
| `IN_REVIEW` | 待评审（交给下游/编排者） |
| `APPROVED` | 已批准，可作为下游输入 |
| `DONE` | 阶段完成，归档 |
| `BLOCKED` | 被阻塞（必须写明阻塞原因和等待谁） |

> 只有 `APPROVED` 的文档才能作为下游阶段的正式输入。
