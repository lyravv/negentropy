---
title: 实现说明（前端）
role: frontend-engineer
status: APPROVED
version: 0.2
updated: 2026-08-20
upstream: [spec/11-workbench-application.md, spec/03-domain-invariants.md]
downstream: [test-engineer, devops-engineer]
---

# 实现说明

## 交接说明
- **给谁**：test-engineer / devops-engineer
- **一句话**：阶段 4 前端完成——Graph 列表菜单新增「Push to 组织库 / 删除 Graph」两个确认式动作（仅 Mine·editable 可见），Add 弹窗改为组织库只读列表，并新增 GX-APP-014 画布合规测试 `test_canvas_renders_typed_hypergraph`；`pnpm build` 与全量 pytest 均通过。
- **关键决策**：
  1. 删除/推送严格按任务给定的后端契约调用（`DELETE /api/v1/alpha/graphs/{id}?confirmed=true`、`POST /api/v1/alpha/graphs/{id}/push` body `{actor:"user",confirmed:true}`），不依赖后端实际进度；
  2. 两个菜单项仅在 `graph.editable === true` 时渲染，System 只读 Graph 不显示（满足 GX-APP-012/013 的"仅 Mine 可删/可推"）；
  3. 删除成功后 `refresh()` 不带 `graph_id`，让后端回退到另一个已加载 Graph（GX-APP-012 回退要求）；
  4. 画布渲染代码（GraphCanvas / NODE_TYPE_COLORS / nodeColor / hyperedgeNodeIds / convexHull / padHull）为既有未提交实现，本次**零改动**，合规测试以源码断言方式锁定其四个 MUST；
  5. 合规测试对 `edge-label` 的断言使用带引号形式 `'"edge-label"'`，避免误伤合法的 `hyperedge-label` 类（超边标题标签是 spec 允许的）。
- **需要下游注意**：
  - 删除/推送的**后端接口尚未实现**（backend-engineer 并行开发中），前端已按契约就绪，联调前这两个动作会 404/405；
  - 删除/推送的合规测试（`tests/conformance/test_graph_delete.py`、`test_graph_push.py`）由 test-engineer 负责，本次未写；
  - 画布合规测试是**源码级**断言（读 App.tsx 文本），不是 DOM 级渲染测试；
  - 构建用 `corepack pnpm build`（环境无全局 pnpm，packageManager 锁定 pnpm@11.9.0）。
- **未决问题**：无（契约按任务给定执行，无偏离；spec 中"推送后本地副本是否转 System 只读"本就是 07-open-questions 记录的产品决策，不影响本次前端实现）。

## 1. 实现范围

| 需求 | 来源 | 实现位置 |
|------|------|---------|
| GX-APP-012 删除 Mine Graph（显式确认、不可逆、非 Agent 工具） | spec/11 + spec/03 | `App.tsx` 菜单项「删除 Graph」+ `api.deleteGraph` |
| GX-APP-013 推送 Mine Graph 到组织库（显式确认、保留内容与版本历史、非 Agent 工具） | spec/11 + spec/03 | `App.tsx` 菜单项「Push to 组织库」+ `api.pushGraph` |
| bootstrap 新增 `org_library` 字段的前端消费 | 任务契约 | `api.ts` `OrgLibraryEntry` 类型 + `Bootstrap.org_library?` |
| Add 弹窗展示组织库只读列表 | 任务要求 | `App.tsx` `modal === "add"` 分支 |
| GX-APP-014 画布类型化超图渲染合规测试 | spec/11 + spec/03 | `tests/test_workbench_frontend.py::test_canvas_renders_typed_hypergraph` |

未实现（边界外）：删除/推送的后端接口、删除/推送的合规测试、"从组织库添加只读副本"（spec 明确为后续能力，UI 仅只读展示 + 说明文案）。

## 2. 代码结构

```
apps/web/src/
├── api.ts        # +OrgLibraryEntry 类型；+Bootstrap.org_library?；+api.deleteGraph / api.pushGraph
├── App.tsx       # +pushGraph()/deleteGraph() 动作函数（确认→调用→notice/error→refresh）
│                 # +context-menu 两个菜单项（graph.editable 条件渲染，删除项带 danger 类）
│                 # +Add 弹窗组织库只读列表（name · v{revision} · pushed_at 本地化时间）
└── styles.css    # +.context-menu button.danger（沿用 danger-button 红系配色）
                  # +.org-library-list / .org-library-item / .org-library-glyph / .org-library-copy
tests/
└── test_workbench_frontend.py  # +test_canvas_renders_typed_hypergraph（源码级断言，4 个 MUST）
```

关键交互细节：
- 菜单项点击先 `setGraphMenu(null)` 关闭菜单，再走 `window.confirm` 确认；取消则不发请求。
- 确认文案与任务契约逐字一致（推送："把「name」推送到组织库？推送后组织库保留其内容与版本历史，本地副本仍可编辑。"；删除："删除「name」？其版本、候选、Chat 与数据连接都会被移除，且不可恢复。"）。
- 成功 toast：推送「已推送到组织库」、删除「Graph 已删除」；失败走统一 `setError`（`api.request` 已解析 `detail.message`，404/409 错误码信息会直接展示）。
- 动作期间 `busy=true`，禁用其他操作，防止并发。
- 组织库列表条目为纯展示（无点击行为），每条带「只读」pill；`pushed_at` 用 `toLocaleString("zh-CN")` 本地化。

## 3. 如何运行

```bash
# 前端构建（tsc -b + vite build）
cd /home/wangling/develop_team/graphx/apps/web
corepack pnpm build        # 环境无全局 pnpm，用 corepack（packageManager: pnpm@11.9.0）

# 画布合规测试
cd /home/wangling/develop_team/graphx
UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest tests/test_workbench_frontend.py -q

# 全量测试
UV_CACHE_DIR=/home/wangling/develop_team/.cache/uv uv run pytest -q
```

无新增环境变量、无新增依赖。前端与后端同进程同源（GX-APP-002），`/api/v1/alpha/*` 由应用服务器提供。

## 4. 契约偏离记录

| 位置 | 契约原文 | 实际实现 | 原因 | 是否已同步契约 |
|------|---------|---------|------|--------------|
| 无 | — | — | 删除/推送/`org_library` 均按任务给定的后端契约（与 spec/11 HTTP API draft 的 DELETE/POST 端点一致）实现，无偏离 | — |

## 5. 自测情况

| 验证项 | 方式 | 结果 |
|--------|------|------|
| TypeScript 严格模式 + Vite 生产构建 | `corepack pnpm build`（tsc -b + vite build） | ✅ 通过（28 modules，无类型错误） |
| GX-APP-014 画布合规测试 | `uv run pytest tests/test_workbench_frontend.py -q` | ✅ 3 passed（含新增 `test_canvas_renders_typed_hypergraph`） |
| 全量回归 | `uv run pytest -q` | ✅ 117 passed, 12 subtests passed |
| 菜单可见性 | 代码审查：`graph.editable &&` 条件渲染，System Graph 不出现 Push/删除项 | ✅ |
| 确认交互 | 代码审查：`window.confirm` 取消即 return，不发请求 | ✅ |
| 删除后回退 | 代码审查：`refresh()` 不带 graph_id，由后端选择回退 Graph | ✅（依赖后端行为，联调时验证） |
| 组织库空态 | 代码审查：`data.org_library?.length` 为假时保留原空态文案 | ✅ |

手工验证说明：删除/推送的真实请求路径依赖后端接口（并行开发中），本次以契约 + 构建 + 源码断言覆盖；联调时建议手工走一遍：Mine Graph 菜单 → Push → Add 弹窗出现条目 → 删除 → 回退到另一 Graph。

## 6. 已知限制 / 遗留问题

1. **后端未就绪**：`DELETE /graphs/{id}` 与 `POST /graphs/{id}/push` 由 backend-engineer 并行实现，联调前前端调用会失败（错误会经 toast 展示，不破坏页面）。
2. **推送后本地副本归属未定**：spec/11 明确"推送后本地副本是否转 System·read-only 是产品决策"（记录于 spec/07-open-questions.md）。前端按契约假设本地副本保持 Mine·editable（确认文案即按此措辞），若产品决策相反，需改确认文案与菜单可见性逻辑。
3. **画布合规测试为源码级**：断言 App.tsx 文本中的关键标识（`node-circle`、`node-type-${node.type}`、`<line … markerEnd`、`convexHull`、`polygon`、`hyperedgeNodeIds`、`dimmed`、`matchesSearch`，以及 `node-meta`/`"edge-label"` 的缺席）。它能锁定渲染实现不回退到旧形态，但不能替代 DOM 级视觉验证；若画布代码做等价重构（如改类名），测试会失败并提示重新对齐。
4. **`nodeMeta`/`nodeColor` 为既有未使用辅助函数**：属于既有画布实现的一部分，按"不修改画布代码"的边界保留未动（tsconfig 未开 noUnusedLocals，不影响构建）。
5. **组织库条目不可点击**：从组织库添加只读副本是后续能力，当前仅只读展示 + 说明文案（符合任务要求）。
