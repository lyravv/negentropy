---
title: <project> 项目当前状态与下一步（单一入口 / STATE）
role: orchestrator(维护)
status: LIVE
version: 0.1
updated: YYYY-MM-DD
upstream: [<规范仓库的交接文档，如 graphx/spec/06-testing-and-handoff.md>]
downstream: [任何被要求"继续 <project> 开发"的 agent]
---

# <project> · 当前状态与下一步（STATE）

> **这是"继续 <project> 开发"的单一入口。**
> 任何 agent 收到「使用 negentropy 定义的多agent角色，继续 <project> 的开发工作」时，
> **先读本文件**，按「Bootstrap 顺序」执行即可，**无需额外背景或进度信息**。
> 本文件由编排者每轮收尾时更新，是"我们在哪 + 下一步做什么"的权威快照。

## 30 秒速览

| 项 | 值 |
|---|---|
| 项目 | <一句话> |
| 代码仓库 | <绝对路径>（分支 <branch>） |
| 规范事实源 | <绝对路径，APPROVED 单一事实源> |
| 团队 | negentropy（7 角色，协议 v1-docs） |
| 当前阶段 | <workflow 阶段 + 简述> |
| 测试状态 | <N passed 全绿 / 命令> |
| 下一步 | <一句话> |

## Bootstrap 顺序（新 agent 照此执行，逐步）

1. 读本文件（`STATE.md`）。
2. 读团队入口 `negentropy/README.md` 与 `team/orchestration.md`（如何派角色）。
3. 读代码仓库 `<repo>/AGENTS.md`（工程铁律 + 变更协议）。
4. 读规范事实源 `<repo>/spec/README.md`，按其指定顺序读相关规范。
5. 读规范里的权威"下一步清单"（如 `<repo>/spec/06`「Continue in this order」）。
6. 跑基线测试确认全绿（给出确切命令与环境变量）。
7. 按「下一步动作」派对应角色 sub-agent（用 `orchestration.md` ��准 prompt 结构）。
8. 收尾：更新本文件 + 规范交接文档 + 提交推送。

## 当前状态（按 `team/workflow.md` 阶段）

| 阶段 | 负责角色 | 状态 | 说明 |
|---|---|---|---|
| 0 立项 | orchestrator | | |
| 1 业务 | business-liaison | | |
| 2 需求 | product-manager | | |
| 3 架构 | architect | | |
| 4 实现 | frontend ∥ backend | | |
| 5 测试 | test-engineer | | |
| 6 发布 | devops-engineer | | |
| 7 复盘 | orchestrator | | |

## 下一步动作（权威完整清单在 <规范交接文档>）

1. **（当前）** <精确的下一步，含角色、输入、前置>
2. <…>

## 关键约束（任何 agent 必须遵守，违反即停）

- <环境/依赖/缓存等>
- <机密：Token/连接/代理 不得打印、入 Git、入 Graph 数据>
- <不覆盖用户已有未提交修改>
- <变更协议：行为修改须同步 规范+测试+交接>
- <产品形态/范围约束>

## 本轮已交付

| 角色 | 产出 | 状态 |
|---|---|---|
| | | |

## 收尾清单（每轮结束，编排者执行）

1. 更新本文件（当前状态 + 下一步）+ 规范交接文档。
2. 更新需求状态 + manifest。
3. 跑全量测试 + `git diff --check`。
4. 提交代码仓库 + 推送。
5. 提交 negentropy 项目工作区变更。
6. 最终交接留下分支/提交 + 精确下一步。

## 已知遗留（非阻塞）

- <…>
