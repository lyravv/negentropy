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
| W-APP-001 | 后端：Chat 生命周期门禁 + 多轮 Build + 非 Build 真实智能体对话 + 空工作台 bootstrap（GX-APP-015/016/017/018） | DONE | backend-engineer | implement | graphx `db3d118` | `src/graphx_alpha/service.py`、`src/graphx_alpha/harness_executor.py`、`spec/03`、`spec/11`、`spec/06`、`spec/conformance/requirements.json`、`spec/manifest.yaml`、`docs/architecture/frontend-backend-api-contract.md`、`tests/`（单测+4 合规） | 与 W-APP-002 无文件重叠（前端仅 `apps/web/src`） | 2026-08-21 | 2026-08-21T22:30+08:00 | 全量 154 passed + 12 subtests；4 条新需求合规用例通过；`git diff --check` 干净 | graphx WORKTREE（待提交）；4 条需求已同步规范/契约/测试 |
| W-APP-002 | 前端：未使用 Chat 禁建 + 空工作台状态 + 删除失败可见性 | DONE | frontend-engineer | implement | graphx `db3d118` | `apps/web/src/App.tsx`、`apps/web/src/api.ts`、`apps/web/src/styles.css` | 与 W-APP-001 无文件重叠（后端仅 `src/`+`spec/`+`tests/`） | 2026-08-21 | 2026-08-21T22:30+08:00 | `tsc -b`+`vite build` 零错误；空工作台/禁建/删除错误三态可验证 | graphx WORKTREE（待提交）；`dist/` 已构建（gitignore）；遗留：`pushGraph`/`send` 失败 toast 同样被 `refresh` 清除（后续项） |
| W-TEST-002 | GX-APP-015/016/017/018 合规测试 + 全量回归 + 测试报告 | DONE | test-engineer | implement | graphx `db3d118` | `tests/conformance/`、`05-testing/{test-plan,defect-log,test-report}.md` | 依赖 W-APP-001、W-APP-002 完成 | 2026-08-21 | 2026-08-21T23:59+08:00 | 全量回归绿；4 条需求合规用例通过；测试报告结论明确 | 全量 154 passed + 12 subtests（exit 0）；4 合规用例全过；无新缺陷；测试报告 v0.3 APPROVED 可发布 |
| W-OPS-001 | 前端构建 + 重新部署 8001 + 清空全部现有 Graph（用户授权）+ 部署后验证 | IN_PROGRESS | devops-engineer | publish | graphx `db3d118` | `apps/web/dist`（已构建）、`scripts/redeploy_alpha.sh`、运行库数据 | 依赖 W-TEST-002 通过 | 2026-08-21 | 2026-08-22T01:00+08:00 | 8001 跑新代码；`DELETE /graphs/{id}` 返回 200；清空后 bootstrap 200 空态；5 条反馈逐项可复验 | 前端已构建；`scripts/redeploy_alpha.sh` 已就绪；已在 8002 临时实例验证 5 条行为全过；**待用户在宿主机执行 `scripts/redeploy_alpha.sh --clear-graphs`**（agent 沙箱无法 signal 宿主机进程） |

## 冲突与集成说明

- 当前集成者：未指定；本次团队迁移只维护 negentropy 定义。
- 受保护的既有修改：开始新任务时以两个仓库的实时 `git status` 为准；本表不缓存已结束工作树状态。
- 并发和 lease 规则：`team/concurrency.md`。
