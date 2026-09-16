---
title: 代码审查意见
role: reviewer
status: DRAFT
version: 0.1
updated: YYYY-MM-DD
upstream: [04-implementation/frontend-notes.md, 04-implementation/backend-notes.md]
downstream: [frontend-engineer, backend-engineer, test-engineer, orchestrator]
source_revision: WORKTREE
---

# 代码审查意见

## 交接说明
- **给谁**：orchestrator（路由）/ 实现角色（整改）/ 需要参考的人
- **一句话**：<本次审查范围、结论一句话>
- **关键决策**：<审查的取舍，例如只审 diff 不审全仓>
- **需要下游注意**：<哪些是"本次变更引入的、建议整改"，哪些是"历史遗留、只提醒不擅删">
- **未决问题**：无 / Q-xxx

## 1. 审查范围
- 触发方式：`on-demand`（用户/编排者明确要求）
- 被审对象：<文件 / 目录 / diff 范围>
- 依据 revision：<commit SHA / WORKTREE>
- 基准：<契约/需求，用于溯源>

## 2. 结论
> **通过 / 有条件通过 / 需整改**（三选一，无模糊表述）

<结论简述，一条即可>

## 3. 问题项
> 每条：严重性（阻塞 / 严重 / 一般 / 建议）+ 证据（文件:行号）+ 建议。

### 本次变更引入
| 严重性 | 位置 | 问题 | 建议 |
|--------|------|------|------|
| | `path:line` | | |

### 历史遗留（只提醒，不擅删）
| 位置 | 现象 | 是否疑似可删 |
|------|------|--------------|
| | | |

## 4. 通过标准核对
- [ ] 本次变更的边缘已逐行溯源到请求
- [ ] 没有把不可核实的"感觉"当作证据
- [ ] 没有擅自改动任何代码 / 文档（本文件除外）

## 5. 下次快速复审项
<整改后需要快速复审的增量范围，若无不填>