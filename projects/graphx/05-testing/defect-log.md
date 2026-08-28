---
title: 缺陷日志 — GraphX Alpha 用户反馈轮
role: test-engineer
status: APPROVED
version: 0.9
updated: 2026-08-28
upstream: [05-testing/test-plan.md]
downstream: [backend-engineer, orchestrator]
---

# 缺陷日志 — GraphX Alpha 用户反馈轮

## 交接说明
- **给谁**：backend-engineer / orchestrator
- **一句话**：本轮（GX-APP-015/016/017/018）全量回归通过，5 项用户反馈均已处理，未发现新缺陷；BUG-001～004 保持 REGRESSED。
- **关键决策**：content-free plan 仍是安全边界，不能信任调用者提供的 manifest role/path。
- **需要下游注意**：保留反序列化入口的路径/role 负向用例，防止最小 allowlist 回退。
- **未决问题**：无。

## 缺陷登记

| 编号 | 标题 | 严重级 | 所属 | 证据 | 状态 |
|---|---|---|---|---|---|
| BUG-001 | 私有 JSON 为 0664，CLI 非原子写入 | 严重 | 后端 | 已改为同目录临时文件、fsync、atomic replace、最终 0600；3 个外部产物均复核为 0600 | REGRESSED |
| BUG-002 | CLI/stdout 与 Git notes 披露私有 hash | 严重 | 后端 | CLI stdout 已移除 hash；backend-notes 私有 hash 模式计数为 0；目标测试验证 stdout 无 `sha256:` | REGRESSED |
| BUG-003 | 伪造 manifest 可绕过 evidence 路径/role allowlist | 严重 | 后端 | 已加入 canonical relative path、role/path/suffix、forbidden path 校验及 CLI 输入 symlink 拒绝；13 组路径/role 负向用例通过 | REGRESSED |
| BUG-004 | 空 SQL manifest + 空 base 可生成 schema-invalid plan | 严重 | 后端 | 函数拒绝无 SQL/无 table；runtime model 对 table/evidence sources 增加最小基数；负向用例通过 | REGRESSED |
| BUG-005 | 活动任务卡首次渲染默认展开，违反 compact-by-default | 一般 | 前端 | 已改为 `useState(false)`；紧凑摘要展示任意 Agent 名称与六态标签，active→terminal 边沿折叠不覆盖 active 期间的用户展开。复验 `npm run build` 与 `git diff --check` 均通过 | FIXED |
| BUG-006 | 受控查询仅识别固定业务表，且首次泛化修复在多表歧义路径空引用查询计划 | 严重 | 后端 | 初验发现 planner 仅硬编码销售订单/发货申请；首次修复后 service 在 `plan=None` 时访问 `.table`。现已从当前 HGT 动态解析任意 DB 表，并在歧义/未匹配时生成净化失败回执与 GraphX final；新增第三表、planner 歧义及 service-level 歧义回归。专项最终 `23 passed` | FIXED |
| BUG-007 | 部署后的 user service 丢失代理，Builder/GraphX Harness 均以 TRANSPORT 失败 | 严重 | DevOps/后端 | 干净 Graph 复现；Harness 原始会话三次 TRANSPORT；宿主机 provider probe 成功但 unit Environment 为空。部署脚本现以 persistent transient user service 显式注入 allowlisted proxy；真实 Harness smoke `completed` | FIXED |
| BUG-008 | GraphX observation 失败被伪造 completed，且卡片排在父 Builder 前 | 严重 | 后端/前端 | 删除 silent-finish 异常兜底，失败写真实 terminal code/final；observation 以 parent final message 锚定；专项覆盖失败状态与源码顺序 | FIXED |
| BUG-009 | GraphX observation 未结束即显示 Candidate Apply，且无 Review 也标记通过 | 严重 | 后端/前端 | Builder Candidate 改为 `proposed`；Reviewer typed report 更新状态；UI 同时校验 lineage 无活动/未解决失败与同哈希 Review passed，其他状态只显示真实等待/失败门禁 | FIXED |
| BUG-010 | Harness 实际步骤未进入任务卡，GraphX max-token 被泛化错误码 | 严重 | Harness/后端/前端 | 公开 SDK `on_notification` → 净化 JSONL → Adapter callback → durable activity；卡片事件区可滚动；丢弃 raw args/results/chunks/CoT；`max-tokens` 映射 `HARNESS_MAX_TOKENS`，role-completion 立即 typed decision | FIXED |
| BUG-011 | 新 Builder 尚未产出 Candidate 时显示上一轮“协调失败”，耗时从 480 分钟开始 | 严重 | 前端 | Candidate 投影先检测比旧候选更新的 active Builder 并隐藏旧卡；API 的无 offset 时间按 UTC 正规化后再计算耗时/显示；工具回执缺 call ID 时按 pending call 安全关联工具名 | FIXED |
| BUG-012 | GraphX 已生成 Supervisor 决策却立即显示“协调失败” | 严重 | Adapter | Bridge 已支持 `supervisor_decision`，但 Worker result Adapter 的 artifact receipt 枚举漏项，成功回执被误报 `WORKER_PROTOCOL_SCHEMA`；现已统一枚举并增加端到端 receipt 回归 | FIXED |
| BUG-013 | 本地模型配置使用桌面端缺失插件，Cordis 初始化超时且不发模型请求 | 严重 | Harness/配置 | rc6 SDK 不包含 `settings-file` / `credentials-local`；改由 bundled `llm-pi-ai` 直接声明 local route，注入固定非敏感占位 key；纯 SDK 与 plugin smoke 通过 | FIXED |
| BUG-014 | Candidate 跨 Chat 泄漏，Apply 后又回退显示历史失败卡片 | 严重 | 后端/前端 | GX-APP-034 以 BuildRun.thread_id 限定 Bootstrap；GX-APP-035 只认最新 Candidate，Apply/继续发言关闭未决提案，late Reviewer 不重开终态；8 项卡片合规测试与前端 build 通过 | FIXED |
| BUG-015 | 简单构图多次产生工具参数 Schema 错误与 30 秒桥接超时 | 严重 | 本地模型/Harness | 最近一次真实构图前两轮 `BUILDER_FAILED`；回执含 `TOOL_ARGUMENT_SCHEMA`，提交调用多次精确 30 秒超时；成功轮仍有重复校验与 120 秒非必要 Bash | OPEN |

## 回归结论

- 上一轮（GX-INGEST-006）：目标组 `30 passed in 2.54s`。BUG-001～004 全部为 `REGRESSED`，无 OPEN 缺陷。
- 本轮（GX-APP-015/016/017/018）：全量回归 `154 passed, 12 subtests passed in 7.51s`（退出码 0），5 项用户反馈均已处理，未发现新缺陷。
- 增量轮（GX-APP-021，2026-08-24）：专项 service-direct `5 passed in 1.96s`，前端生产构建通过；发现 BUG-005（一般，OPEN），结论为 CHANGES_REQUESTED。既有 TestClient 回归组合在当前环境运行 60 秒无输出后人工中断，不计入通过率。
- BUG-005 修复复验（2026-08-24）：静态证据确认默认紧凑、六态摘要与边沿折叠行为；前端生产构建 1.14 秒通过，`git diff --check` 通过。BUG-005 转为 FIXED，GX-APP-021 结论更新为 APPROVED。
- 第二轮反馈（GX-APP-021..025，2026-08-24）：初验登记 BUG-006；两次修复后专项最终 `23 passed in 3.64s`，前端生产构建和 `git diff --check` 通过，BUG-006 转为 FIXED，结论 APPROVED。全量运行 3 分钟仅 5 个进度点后按约定中止（exit 130），不计入通过率。
- W-FIX-001（2026-08-25）：BUG-007/008 均修复；相关 Harness/Supervisor/卡片/取消专项 `30 passed in 4.98s`，前端生产构建通过，真实 Harness rc6 冒烟 `completed`。全量 TestClient 仍在既有 httpx2 路径挂起，不计全量结果。
- W-FIX-002（2026-08-25）：BUG-009/010 均修复；相关 Adapter/Executor/Activity/DAG/Cancel 专项 `22 passed in 4.54s`，前端生产构建通过，真实 Harness rc6 Builder/Reviewer/Tester 冒烟全部 `completed`。全量 TestClient 仍在既有 httpx2 路径挂起，不计全量结果。
- W-FIX-002 追加复验：BUG-011 修复；前端/Adapter专项 `13 passed in 2.33s`，production build 通过并重部署 8001。
- W-FIX-002 二次追加复验：BUG-012 修复；Adapter/Harness/DAG 专项 `16 passed in 1.25s`，重部署 8001 且 health 通过。
- W-LOCAL-001 / W-CAND-001（2026-08-28）：BUG-013/014 修复；58 个核心/运行时/合规专项、8 个 Candidate 卡专项与前端 production build 通过，本地 pi-ai SDK/plugin smoke 通过；BUG-015 保持 OPEN，最新 GX-APP-035 待重部署验证。
