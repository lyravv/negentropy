---
title: 项目立项简报
role: orchestrator
status: APPROVED
version: 0.2
updated: 2026-08-20
upstream: []
downstream: [backend-engineer, frontend-engineer, test-engineer]
---

# 项目立项简报 · GraphX

## 交接说明
- **给谁**：backend-engineer / frontend-engineer / test-engineer
- **一句话**：继续 GraphX（Graph-first 超图工作台）的可运行工作台切片，本轮交付 Graph 删除（GX-APP-012）、推送组织库（GX-APP-013）与类型化超图画布渲染的合规测试（GX-APP-014）。
- **关键决策**：Graph 是一级对象；Build Mode 是用户与 Builder/Reviewer/Tester 的简单群聊；不重新���计产品形态；Apply/Delete/Push 永远不是 Agent 工具。
- **需要下游注意**：`/home/wangling/develop_team/graphx/spec/` 是单一事实源（已 APPROVED），本工作区只承载团队协作文档，不复制规范。
- **未决问题**：OQ-017（推送后本地副本所有权）默认"本地保持可编辑，组织库为独立只读投影"。

## 1. 背景
GraphX 是一个以 Graph/Node/Edge/Hyperedge 为一级对象的工作台。当前产品版本 0.5.7，
分支 `feat/trusted-build-core`。业务、需求、架构阶段已由 `graphx/spec/` 固化
（01 产品范围、02 架构、03 领域不变量、04 构建生命周期、05 Harness 边界、
08 HGT 协议、09 SQL 验收、10 盲评、11 工作台应用、12 图绑定业务问题）。
本轮是阶段 4（实现）的延续：完成上一轮遗留的 Graph 删除/推送与画布渲染合规测试。

## 2. 目标
- 实现 `DELETE /api/v1/alpha/graphs/{graph_id}`（GX-APP-012）与
  `POST /api/v1/alpha/graphs/{graph_id}/push`（GX-APP-013）后端端点 + 前端菜单动作。
- 为 GX-APP-014（类型化超图画布渲染）补齐合规测试。
- 三条需求从 `planned` 转为 `implemented`，全量测试通过，规范/测试/交接记录同步更新。

## 3. 非目标（Out of Scope）
- 不重新设计产品形态、不引入独立流水线/Agent 团队/测试中心 UI。
- 不实现多用户、认证、租户、对象存储、生产 Graph Store（仍为开发者 JSON/SQLite 投影）。
- 不加载私有/不可信业务源到真实角色会话（凭据隔离仍是前置条件）。
- 组织库"添加只读副本"的完整 Add 流程若超出本轮最小闭环，记为后续项，不静默扩张。

## 4. 干系人
| 角色 | 团队 | 关注点 |
|------|------|--------|
| 产品负责人 | 用户 | 产品形态、所有权语义、验收 |
| 编排者 | 主 agent | 路由、把关、规范一致性 |
| 后端/前端/测试 | negentropy 角色 sub-agent | 实现与质量 |

## 5. 约束与假设
- 使用 uv 环境；依赖通过 `uv sync` 管理（`UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv`）。
- Token、数据库连接、代理配置不得打印、写入 Git 或进入 Graph 数据。
- 任何行为修改必须同时更新规范、测试和交接记录（graphx AGENTS.md 变更协议）。
- 不覆盖用户已有未提交修改（App.tsx/styles.css 的画布渲染改动是 GX-APP-014 的既有前端实现）。
- 远程应用地址 http://10.54.56.113:8001/ ；所有工作材料只放在 /home/wangling/develop_team 下。

## 6. 成功标准
- `uv run pytest -q` 全绿（含新增合规测试与 spec-contract 测试）。
- GX-APP-012/013/014 在 `spec/conformance/requirements.json` 标记 `implemented` 且测试映射存在。
- `spec/manifest.yaml` 与 `spec/06-testing-and-handoff.md` 同步更新；提交并推送，交接记录留下分支/提交与下一步。
