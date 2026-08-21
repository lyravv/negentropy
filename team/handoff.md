---
title: 交接与续接机制
role: orchestrator
status: APPROVED
version: 2.0
updated: 2026-08-21
upstream: [team/governance.md, team/concurrency.md, team/orchestration.md]
downstream: [projects/*/STATE.md, projects/*/WORKBOARD.md]
artifact_type: team-definition
source_revision: WORKTREE
reviewers: []
approver: team-owner
approval_evidence: 用户要求按评估建议优化团队，2026-08-21
---

# 交接与续接机制

`STATE.md` 回答“项目在哪、下一步是什么”，`WORKBOARD.md` 回答“谁正在改什么”，权威仓库回答“事实是什么”。三者职责不同，不能互相替代。

## STATE 最小内容

- 项目状态和 workflow profile；
- 代码、规范、测试、发布等权威来源的路径、分支、revision/`WORKTREE`；
- 当前阶段状态和替代阶段依据；
- 最近验证的日期、命令、revision、结果；
- 精确下一步、项目专属约束、已知遗留；
- 指向 WORKBOARD、本文件和项目规则。

不得把长测试报告、团队通用规则或敏感配置复制进 STATE。数字无法确认时标为待验证。

## Bootstrap

1. 读 STATE 和 WORKBOARD。
2. 读本文件、当前协议、philosophy、governance、concurrency、orchestration。
3. 按 STATE 指针读代码仓规则、规范和权威交接。
4. 检查相关仓库状态；识别用户修改、活动 lease、base revision 是否失效。
5. 运行 `python scripts/validate_team.py --project <name>`；error 必须先处理，warning 按当前任务决定迁移。
6. 运行项目 baseline，或说明为何本轮只做只读/文档工作而不运行。
7. 写任务在 WORKBOARD 认领后执行。

## 收尾

1. 运行 scoped 验证、必要的 baseline 和 `git diff --check`。
2. 更新工作项状态、result revision/`WORKTREE`、验证与遗留。
3. 更新权威规范交接，再更新 STATE 的摘要和下一步；跨仓 revision 必须准确。
4. 运行团队校验，消除本轮新增 error。
5. 只有 action mode 和授权允许时才 commit；只有 `publish` 明确授权时才 push/deploy/外部写入。
6. 最终交接说明改了什么、未改什么、验证、风险和精确下一步。

## 团队级安全约束

- Token、连接信息、代理和私有数据不得输出、提交或进入提示/Trace/日志。
- 不覆盖用户或其他活动工作项的修改；不清理范围外 worktree。
- 所有写入限定在工作项 scope；行为修改同步规范、契约、测试和交接。
- 破坏性操作、生产操作、外部通知和权限扩张需要明确授权。
- 项目的包管理器、缓存路径、产品铁律和工作目录属于项目内容，只放 STATE/项目规则，不写进通用团队规则。

## 兼容策略

旧项目没有 WORKBOARD 时可以只读续接；第一次发生写任务前必须创建。旧 frontmatter 缺审批字段先 warning，触碰时迁移。旧 `LIVE` 读取为 `ACTIVE`，更新 STATE 时改成新状态。
