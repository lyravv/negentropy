---
title: <project> 项目当前状态与下一步（STATE · 项目内容）
role: orchestrator(维护)
status: LIVE
version: 0.1
updated: YYYY-MM-DD
upstream: [<规范仓库的交接文档，如 graphx/spec/06-testing-and-handoff.md>]
downstream: [任何被要求"继续 <project> 开发"的 agent]
---

# <project> · 当前状态与下一步（STATE）

> **本文件只放"项目内容"**（我们在哪 + 下一步 + 项目专属约束）。
> **团队能力**（Bootstrap 顺序 / 收尾清单 / 团队级约束 / STATE.md 约定）的单一事实源在
> **`team/handoff.md`**，本文件不重复——只留一行指针（见文末「续接指针」）。
> 任何 agent 收到「使用 negentropy 定义的多agent角色，继续 <project> 的开发工作」时，
> 先读本文件，再顺指针读 `team/handoff.md` 按 Bootstrap 顺序接手，无需额外背景。

## 30 秒速览

| 项 | 值 |
|---|---|
| 项目 | <一句话> |
| 代码仓库 | <绝对路径>（分支 <branch>） |
| 规范事实源 | <绝对路径，APPROVED 单一事实源> |
| 团队 | negentropy（7 角色，协议 v1-docs） |
| 当前阶段 | <workflow 阶段 + 简述> |
| 测试状态 | <N passed 全绿> |
| 下一步 | <一句话> |

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

1. **（当前）** <精确的下一步：做什么、派哪个(些)角色、输入/前置/排除项>
2. <…>

## 本轮已交付

| 角色 | 产出 | 状态 |
|---|---|---|
| | | |

## 项目专属约束（只列本项目特有的；团队级约束见 `team/handoff.md` §4）

- <本项目特有的约束，如变更协议、工程铁律、产品形态、环境/缓存等>

## 已知遗留（非阻塞）

- <…>

## 续接指针

- **Bootstrap 顺序 / 收尾清单 / 团队级约束 / STATE.md 约定**：见 `team/handoff.md`（团队能力单一事实源）。
- **本项目基线命令**：<确切命令 + 所需环境变量，如 `cd <repo> && UV_CACHE_DIR=... uv run pytest -q`>
