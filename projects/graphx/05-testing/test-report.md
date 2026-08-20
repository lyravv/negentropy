---
title: 测试报告 — Graph 删除（GX-APP-012）+ 推送组织库（GX-APP-013）
role: test-engineer
status: APPROVED
version: 0.1
updated: 2026-08-20
upstream: [05-testing/test-plan.md, 05-testing/defect-log.md]
downstream: [devops-engineer, orchestrator]
---

# 测试报告 — 阶段 5（GX-APP-012/013 合规测试 + 全量回归）

## 交接说明
- **给谁**：devops-engineer / orchestrator
- **一句话**：**可发布** —— GX-APP-012/013 的 9 条合规用例全绿、全量回归 126 passed + 12 subtests 全绿、GX-APP-014 画布测试通过、无阻塞/严重缺陷；遗留风险均为非阻塞（范围外能力 / 部署项 / 1 条契约措辞待裁定）。
- **关键决策**：
  1. 结论为**可发布**（二选一，明确）。
  2. 合规测试为接口级（TestClient + 临时 SQLite），级联删除与组织库快照经直接查 DB 断言。
  3. 未发现实现缺陷；`confirmed` 缺失分支 422 vs 409 的措辞差异记为 Q-001（契约澄清，非缺陷）。
- **需要下游注意**：
  - **Postgres 部署需补 `CREATE TABLE org_library_graphs` 迁移**（SQLite 由 `create_all` 自动建表，Postgres 不会）——devops 部署前必须执行。
  - 组织库 Add/删除端点、重复推送去重本轮未实现，前端 Add 弹窗为只读展示。
  - Q-001（`confirmed` 缺失状态码）待 architect 裁定，不阻塞发布。
- **未决问题**：Q-001（等待 architect，非阻塞）

## 1. 结论
> **可发布**

理由：GX-APP-012/013 的 9 条 P0/P1 合规用例 100% 通过，全量回归 126 passed + 12 subtests 全绿（无破坏），GX-APP-014 画布合规测试��过，且无阻塞/严重缺陷遗留。所有遗留风险均为非阻塞（范围外能力、部署迁移项、1 条契约措辞待裁定），不影响本轮交付的删除/推送功能正确性。

## 2. 执行概况
| 指标 | 数值 |
|------|------|
| 合规用例总数（TC-001…TC-009） | 9 |
| 通过 | 9 |
| 失败 | 0 |
| 阻塞 | 0 |
| 合规用例通过率 | 100% |
| 全量回归最终计数 | **126 passed + 12 subtests passed**（基线 117 + 新增 9） |
| GX-APP-014 画布测试 `test_canvas_renders_typed_hypergraph` | 通过 |
| 执行命令 | `UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest -q` |

### 合规用例明细
| 用例 | 函数 | 结果 |
|------|------|------|
| TC-001 | `test_delete_mine_graph_removes_related_records` | ✅ 通过 |
| TC-002 | `test_delete_system_graph_rejected` | ✅ 通过 |
| TC-003 | `test_delete_requires_confirmation` | ✅ 通过 |
| TC-004 | `test_delete_nonexistent_graph_404` | ✅ 通过 |
| TC-005 | `test_push_mine_graph_creates_org_library_entry` | ✅ 通过 |
| TC-006 | `test_push_system_graph_rejected` | ✅ 通过 |
| TC-007 | `test_push_requires_confirmation` | ✅ 通过 |
| TC-008 | `test_push_nonexistent_graph_404` | ✅ 通过 |
| TC-009 | `test_bootstrap_exposes_org_library` | ✅ 通过 |

## 3. 缺陷概况
| 严重级 | 发现 | 已修复 | 遗留 |
|--------|------|--------|------|
| 阻塞 | 0 | 0 | 0 |
| 严重 | 0 | 0 | 0 |
| 一般 | 0 | 0 | 0 |
| 轻微 | 0 | 0 | 0 |

**本轮无缺陷**（详见 `defect-log.md`）。唯一记录项为 Q-001（契约措辞差异，非缺陷，待 architect 裁定）。

## 4. 遗留风险
> 均为**非阻塞**，不影响本轮删除/推送功能发布；列出供 devops / 后续迭代知悉。

1. **Postgres 迁移（部署项，devops）**：新表 `org_library_graphs` 在 SQLite 由 `Base.metadata.create_all` 自动建表，但**生产 Postgres 需手动执行 `CREATE TABLE org_library_graphs`**（字段见 backend-notes 第 2 节）。未执行则 Postgres 环境推送/`bootstrap.org_library` 会失败。
2. **组织库无 Add/删除/更新端点（范围外）**：从组织库"添加只读副本"、删除/更新组织库条目本轮未实现；前端 Add 弹窗仅**只读展示** `bootstrap.org_library`（backend-notes 限制 1/3，frontend-notes 限制 5）。
3. **重复推送不去重（契约未定义）**：同一 Graph 多次推送产生多行 `org_library_graphs`（每行独立 `org-*` id）；如需"最新一次为准"需走 C-xxx 变更（backend-notes 限制 2）。
4. **删除不可逆（符合契约）**：无回收站/软删除，连接密钥文件 unlink 后不可恢复（符合 GX-APP-012 "Delete is irreversible"，backend-notes 限制 4）。
5. **画布合规测试为源码级（非 DOM 视觉验证）**：`test_canvas_renders_typed_hypergraph` 断言 `App.tsx` 文本关键标识，能锁定渲染实现不回退，但不能替代 DOM 级视觉验证；画布等价重构（改类名）会使该测试失败并提示重新对齐（frontend-notes 限制 3）。
6. **`confirmed` 缺失分支状态码待裁定（Q-001）**：实现缺失 `confirmed` 返回 422、`confirmed=false` 返回 409；任务规格措辞为"均 409"。核心拒绝行为一致，待 architect 裁定后对齐契约/测试（非阻塞）。
7. **删除后工作台回退未单独断言**：GX-APP-012 "删除 active Graph 后回退到另一 loaded Graph" 由 backend 自测覆盖（`bootstrap` 选图逻辑），本轮合规测试未单独写用例；前端 `refresh()` 不带 `graph_id` 依赖该后端行为（frontend-notes 自测项，联调时建议手工走一遍）。
8. **推送后本地副本归属为产品决策**：spec/07-open-questions 记录"推送后本地副本是否转 System·read-only"为产品决策；本轮按契约假设本地保持 `Mine·editable`（TC-005 已断言 ownership 不变），若产品决策相反需改前端确认文案与菜单可见性（frontend-notes 限制 2）。

## 5. 建议
- **devops**：Postgres 部署清单加入 `CREATE TABLE org_library_graphs` 迁移（风险 1），并在联调环境手工走一遍"Mine Graph 菜单 → Push → Add 弹窗出现条目 → 删除 → 回退到另一 Graph"（风险 7）。
- **architect**：裁定 Q-001（`confirmed` 缺失分支 409 vs 422），据此对齐 spec/11 错误表与合规测试 TC-003。
- **product-manager**：确认"推送后本地副本归属"产品决策（风险 8）与"重复推送去重"语义（风险 3），如需变更走 C-xxx。
- **后续迭代**：组织库 Add 只读副本端点（含副本 ownership=`system` 只读与 source 绑定语义）作为独立需求排期。
