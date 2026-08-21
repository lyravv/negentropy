---
title: 团队治理、状态与审批
role: orchestrator
status: APPROVED
version: 1.0
updated: 2026-08-21
upstream: [team.yaml]
downstream: [team/workflow.md, team/orchestration.md, team/protocols/v1.1-docs.md]
artifact_type: team-definition
source_revision: WORKTREE
reviewers: [orchestrator, all-role-charters]
approver: team-owner
approval_evidence: 用户要求完全按评估建议优化团队，2026-08-21
---

# 团队治理、状态与审批

本文件解释权限、状态和授权边界的语义；团队设计取舍先遵循 `team/philosophy.md`。状态枚举、action mode 和机器审批策略以 `team.yaml` 为结构化权威来源，本文不形成第二份机器事实。角色章程若与本文冲突，以本文语义和 `team.yaml` 数据为准并登记修订。

## 1. 四条不可混淆的职责

- **作者（Author）**：创建和修订交付物，对内容真实性负责。
- **审查者（Reviewer）**：提出意见并留下 review evidence；不能代替批准者。
- **批准者（Approver）**：对该类事实有决策权，唯一可把文档从 `IN_REVIEW` 置为 `APPROVED`。
- **编排者（Orchestrator）**：检查流程和证据、路由工作、维护状态；除非本身就是该项批准者或得到用户明确委托，否则不能代替业务/技术批准者。

## 2. 批准矩阵

| 交付物/决策 | 作者 | 必须审查 | 批准者 |
|---|---|---|---|
| project brief、范围、需求优先级 | orchestrator / product-manager | business-liaison、相关技术角色 | 用户/项目负责人；明确委托时可由 orchestrator 代理 |
| business brief、业务规则、术语 | business-liaison | product-manager | 业务负责人；无法联系则 `BLOCKED` |
| requirements、user story、验收标准 | product-manager | architect、test-engineer | 用户/产品负责人 |
| architecture | architect | 实现、测试、运维中受影响角色 | architect（技术责任人） |
| API/data contract 及其变更 | architect | 所有受影响消费者 | architect；业务行为变化还需 product-manager |
| implementation notes | 实现角色 | test-engineer；必要时 architect | 产出角色对事实签署，测试门禁另由 test report 决定 |
| test plan | test-engineer | 受测角色；必要时 architect | test-engineer 自检；不设独立正式审批门禁 |
| test report | test-engineer | 受测角色；必要时 architect | test-engineer（质量结论） |
| deployment plan | devops-engineer | backend、test-engineer | devops-engineer；生产发布另需用户/项目负责人授权 |
| release / rollback | devops-engineer | test-engineer、orchestrator | 用户/项目负责人；紧急回滚可由 devops 按预授权执行 |
| 团队定义 | orchestrator | 受影响角色 | 用户/团队负责人 |

只有 `team.yaml#approval_policies` 中的门禁型交付物强制批准证据：`approver` 必须匹配策略，`APPROVED` 时必须有 `source_revision` 与 `approval_evidence`。普通 notes/日志不为形式完整而填审批字段；旧门禁文档按触碰原则迁移。

`team-owner / project-owner / business-owner / product-owner` 是稳定职责 ID，不是姓名。每个项目在 STATE 的“项目批准者”中把它们解析为实际负责人或 `user`；联系方式不必进入 Git。批准者不可用时保持 `BLOCKED` 并请求决定，不能因等待超时自动获得授权。

## 3. 状态空间

不同对象使用不同状态，禁止混用。以下是 `team.yaml#statuses` 的人类可读投影；增删枚举只改 `team.yaml`，本文仅在语义变化时更新：

- 文档：`DRAFT / IN_REVIEW / APPROVED / BLOCKED / SUPERSEDED / ARCHIVED`
- 项目：`ACTIVE / PAUSED / BLOCKED / COMPLETED / ARCHIVED`
- 阶段：`NOT_STARTED / READY / IN_PROGRESS / IN_REVIEW / DONE / BLOCKED / SKIPPED`
- 工作项：`READY / CLAIMED / IN_PROGRESS / IN_REVIEW / BLOCKED / DONE / CANCELLED`
- 问题：`OPEN / RESOLVED / DEFERRED`
- 变更：`PENDING / APPROVED / REJECTED / IMPLEMENTED / SUPERSEDED`

兼容规则：0.3.0 以前 `STATE.md` 的 `LIVE` 只作为项目状态 `ACTIVE` 的旧别名读取；新写入必须用 `ACTIVE`。

## 4. 状态转换

文档正常路径为 `DRAFT → IN_REVIEW → APPROVED`。作者提交评审，批准者批准；编排者只验证流程证据。已批准文档变更时回到 `IN_REVIEW`，版本递增，原批准证据保留在变更记录中。阻塞解除后回到阻塞前状态。

阶段 `DONE` 表示其 profile 规定的出口证据已存在，不等于所有项目工作已经完成。阶段被 profile 合法裁剪时用 `SKIPPED`，必须给出替代权威来源。

## 5. 问题和变更的关闭权

- Q 项由“等待谁”回答；提出者或 test-engineer 验证回答已落地后置 `RESOLVED`。
- C 项由目标事实的批准者决定 `APPROVED/REJECTED`；完成代码、规范、测试同步后由 orchestrator 核验并置 `IMPLEMENTED`。
- orchestrator 可以催办、路由和核验证据，不能凭流程身份代替领域裁决。
- 用户的明确决定优先级最高，必须在解决记录中注明日期和决定来源。

## 6. 行为授权模式

每个工作项必须声明一种 action mode。下表解释 `team.yaml#action_modes`，可执行值以 YAML 为准：

| 模式 | 允许范围 |
|---|---|
| `inspect` | 只读诊断和汇报 |
| `draft` | 仅修改指定文档，不提交、不发布 |
| `implement` | 修改认领范围并验证，不默认提交 |
| `integrate` | 在明确请求或项目政策允许时提交，不推送/部署 |
| `publish` | 只有明确授权才允许推送、部署、外部写入或通知 |

用户要求“实现/优化”不自动授权 push、部署、生产迁移或向外部系统写入。破坏性操作仍需单独确认。

## 7. 每类事实的权威来源

不再笼统声称一个仓库包含全部事实。每个项目在 `STATE.md` 登记：代码、规范、当前状态、工作认领、测试证据、发布状态各自的权威来源及 revision。跨仓交接至少包含仓库路径、分支、commit SHA（未提交则写 `WORKTREE`）、更新时间和验证命令。
