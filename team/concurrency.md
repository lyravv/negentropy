---
title: 并发与工作认领协议
role: orchestrator
status: APPROVED
version: 1.0
updated: 2026-08-21
upstream: [team/governance.md]
downstream: [projects/*/WORKBOARD.md, team/orchestration.md]
artifact_type: team-definition
source_revision: WORKTREE
reviewers: [orchestrator, implementation-roles]
approver: team-owner
approval_evidence: 用户要求对正在使用的团队做稳定、实际的全面优化，2026-08-21
---

# 并发与工作认领协议

## 核心规则

1. 任何写入任务先在项目 `WORKBOARD.md` 建工作项并认领；只读检查无需认领。
2. 工作项必须写清 `base_revision`、action mode、owner、写入范围、依赖、验收命令和 lease 截止时间。
3. 两个活动工作项不得覆盖同一文件/数据/契约；有重叠时由 orchestrator 拆分或串行化。
4. 前后端并行必须以已批准契约为共同 base；契约修改单独建工作项，并阻塞依赖项直到重新批准。
5. Agent 开始和交付前都检查目标仓库 worktree。发现未知修改时停止覆盖，缩小范围或请求协调。
6. 集成者基于各工作项记录的 revision 合并、运行全量验证，并对最终状态负责。

## Lease

- `CLAIMED/IN_PROGRESS` 必须有 `claimed_at` 与 `lease_until`。
- 建议单轮 lease 为 2 小时；长任务在到期前续租并更新心跳。
- lease 过期不代表可直接覆盖其文件。orchestrator 先确认没有活跃进程/新提交，再将其标为 `BLOCKED` 或重新认领，并记录原因。
- 同一 work item 同时只有一个 owner；协作者写入互斥区域时拆成子项。

## 最小工作项字段

`id / title / status / owner / action_mode / base_revision / scope / dependencies / claimed_at / lease_until / acceptance / result_revision / notes`

## 集成门禁

- 所有依赖项处于 `DONE`，或被批准者明确豁免；
- worktree 未覆盖用户既有修改；
- 契约、实现、测试、交接指向同一行为版本；
- scoped tests 与项目 baseline 通过；
- `git diff --check` 通过；
- push/部署另有 `publish` 授权，不能由“集成完成”推导。

## 冲突处理

优先保留用户修改，其次保留已批准契约；不要自动选择某一 Agent 的版本。冲突工作项置 `BLOCKED`，记录双方 base/result revision、冲突文件和需要谁裁决。
