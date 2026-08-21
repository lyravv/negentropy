---
title: GraphX 工作台账
role: orchestrator
status: ACTIVE
version: 0.1
updated: 2026-08-21
---

# GraphX · WORKBOARD

> 本文件在团队 0.3.0 迁移时建立。迁移时两个仓库均已有用户工作树修改，因此没有替现有任务补造 owner 或 lease；开始下一项写任务前先核对并正式认领。

| ID | 标题 | 状态 | Owner | Mode | Base revision | 写入范围 | 依赖 | Claimed at | Lease until | 验收 | Result revision / Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W-MIG-001 | negentropy 0.3.0 团队治理迁移 | DONE | orchestrator | implement | negentropy `d88ca79` + WORKTREE | `team/`, `_template/`, `scripts/`, GraphX STATE/WORKBOARD | 无 | 2026-08-21 | 2026-08-21T23:59+08:00 | 团队校验通过；不覆盖现有 GraphX 实现/测试改动 | WORKTREE；validator 0 errors，历史迁移 warnings 保留 |
| W-LEGACY-001 | 迁移前已存在的 GraphX corpus 私有输出实现 | DONE | unknown-existing-worktree | implement | graphx WORKTREE | scripts/src/tests 私有输出加固 | 不由本次迁移接管 | unknown | unknown | 全量测试绿 | graphx `1e53457`（已推送）；原任务已落库，受保护修改已由原任务提交 |
| W-TEST-001 | 确定性静态套件绑定 `test_run`（GX-TEST-001） | DONE | orchestrator（test-engineer 子代理） | implement | graphx `cf7f9e0` | `src/graphx_core/static_suite.py`、`tool_gateway.py`、`src/graphx_alpha/question_executor.py`、`tests/conformance/test_static_suite.py`、`spec/03`、`spec/06`、`spec/12`、`spec/conformance/requirements.json`、`spec/manifest.yaml` | 与 W-LEGACY-001 无文件重叠 | 2026-08-21 | 2026-08-21T23:59+08:00 | 全量 150 passed + 12 subtests；`git diff --check` 干净 | graphx `db3d118`（已推送）；30 条盲评运行时执行 + 输出冻结仍待做 |

## 冲突与集成说明

- 当前集成者：未指定；本次团队迁移只维护 negentropy 定义。
- 受保护的既有修改：开始新任务时以两个仓库的实时 `git status` 为准；本表不缓存已结束工作树状态。
- 并发和 lease 规则：`team/concurrency.md`。
