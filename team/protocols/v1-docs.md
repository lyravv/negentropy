# 协作协议 v1 · 纯文档协作（当前生效）

> **版本**：v1-docs　**状态**：ACTIVE
> 本协议定义团队在**没有外部协同工具**时如何协作：一切沟通通过项目工作区里的 Markdown 文档完成，git 是单一事实源。
> 升级到 v2（yapi/jira）时，本协议保留备查，见 `v2-tools.md`。

## 1. 核心原则

1. **文档即沟通**：角色之间不"口头"交接，所有交接都落成文档。
2. **单一事实源**：同一信息只在一处定义，其他地方引用，不复制。
3. **显式优于隐式**：假设、决策、未决项都要写下来，不靠"大家都知道"。
4. **契约先行**：前后端以 `api-spec.md` 为契约；改契约必须走变更流程。

## 2. 文档规范

### 2.1 文档头部（每份文档必须有）

```markdown
---
title: <文档标题>
role: <产出角色 id>
status: DRAFT | IN_REVIEW | APPROVED | DONE | BLOCKED
version: 0.1
updated: YYYY-MM-DD
upstream: [<依赖的上游文档路径>]
downstream: [<消费本文档的下游角色>]
---
```

### 2.2 Handoff Note（交接说明）

每份文档正文开头放一个"交接说明"块，让下游 30 秒内抓住重点：

```markdown
## 交接说明
- **给谁**：<下游角色>
- **一句话**：<本文档的核心结论/交付物>
- **关键决策**：<列出 3-5 条最重要的决策>
- **需要下游注意**：<坑、约束、未决项>
- **未决问题**：<见 open-questions.md 的编号，或"无">
```

### 2.3 未决问题（open-questions.md）

每个项目工作区根目录维护一份 `open-questions.md`，全局唯一编号：

```markdown
| 编号 | 提出角色 | 问题 | 等待谁 | 状态 | 解决记录 |
|------|---------|------|--------|------|---------|
| Q-001 | architect | 用户量级决定要不要分库？ | business-liaison | OPEN | |
```

- 任何角色都可以提问题，但**只有被等待的角色**能关闭它。
- 阻塞性未决问题会让相关文档进入 `BLOCKED` 状态。

## 3. 交接流程

```
上游角色产出文档 → 置为 IN_REVIEW → 编排者路由给下游
→ 下游阅读，有问题则写 open-questions / 打回
→ 无问题则下游置为 APPROVED 并开工
```

- **编排者（orchestrator）**负责路由：把 `IN_REVIEW` 的文档交给正确的下游角色。
- 角色**只读**上游的 `APPROVED` 文档作为正式输入；`IN_REVIEW` 的只能参考。

## 4. 变更流程

已 `APPROVED` 的文档要改时：
1. 提出变更的角色在 `open-questions.md` 记录变更请求（编号 `C-xxx`）。
2. 原产出角色评估影响，修订文档，`version` +0.1，`status` 回到 `IN_REVIEW`。
3. 受影响的下游角色重新确认。
4. 契约类文档（`api-spec.md`、`data-model.md`）的变更**必须**经 architect 确认。

## 5. 命名与位置

- 项目工作区：`projects/<project-name>/`
- 阶段目录：`00-intake/` `01-business/` `02-requirements/` `03-architecture/` `04-implementation/` `05-testing/` `06-ops/` `07-retro/`
- 文档名：kebab-case，见 `team/templates/` 各模板。
- 用户故事：`02-requirements/user-stories/US-<nnn>-<slug>.md`

## 6. 提交规范（git）

- 每个阶段完成提交一次，commit message 格式：
  `[<project>] <stage>: <简述> (role: <role-id>)`
  例：`[demo-api] architecture: 完成接口与数据模型 (role: architect)`
- 团队定义文件（`team/`、`evolution/`）的变更单独提交：
  `team: <简述>` 或 `evolution: <简述>`
