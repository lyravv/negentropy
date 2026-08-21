---
title: 缺陷日志 — GX-APP-015/016/017/018
role: test-engineer
status: APPROVED
version: 0.3
updated: 2026-08-21
upstream: [05-testing/test-plan.md]
downstream: [backend-engineer, orchestrator]
---

# 缺陷日志 — GX-APP-015/016/017/018

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

## 回归结论

- 上一轮（GX-INGEST-006）：目标组 `30 passed in 2.54s`。BUG-001～004 全部为 `REGRESSED`，无 OPEN 缺陷。
- 本轮（GX-APP-015/016/017/018）：全量回归 `154 passed, 12 subtests passed in 7.51s`（退出码 0），5 项用户反馈均已处理，未发现新缺陷。
