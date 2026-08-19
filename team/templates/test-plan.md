---
title: 测试方案
role: test-engineer
status: DRAFT
version: 0.1
updated: YYYY-MM-DD
upstream: [02-requirements/user-stories/, 03-architecture/api-spec.md, 04-implementation/*-notes.md]
downstream: [test-engineer(执行), orchestrator]
---

# 测试方案

## 交接说明
- **给谁**：自己（执行）/ orchestrator
- **一句话**：<测什么、怎么测、测到什么程度算过>
- **关键决策**：<测试策略、范围>
- **需要下游注意**：<环境依赖>
- **未决问题**：无 / Q-xxx

## 1. 测试范围
<测什么，不测什么>

## 2. 测试策略
| 层级 | 方法 | 覆盖目标 |
|------|------|---------|
| 单元 | | 核心逻辑 |
| 接口 | | api-spec 全部接口 |
| 端到端 | | 关键用户故事 |
| 非功能 | | 性能/安全（如适用） |

## 3. 测试用例
| 用例ID | 对应故事/接口 | 前置 | 步骤 | 预期 | 优先级 |
|--------|-------------|------|------|------|--------|
| TC-001 | US-001 / API-001 | | | | P0 |

## 4. 测试数据
<需要的数据、如何准备>

## 5. 通过标准（Definition of Done for 测试）
<什么算"可发布"：P0/P1 用例通过率、缺陷等级要求>

## 6. 环境与工具
<测试环境、自动化工具>
