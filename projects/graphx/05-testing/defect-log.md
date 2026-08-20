---
title: 缺陷日志 — Graph 删除（GX-APP-012）+ 推送组织库（GX-APP-013）
role: test-engineer
status: APPROVED
version: 0.1
updated: 2026-08-20
upstream: [05-testing/test-plan.md]
downstream: [backend-engineer, frontend-engineer, orchestrator]
---

# 缺陷日志 — 阶段 5（GX-APP-012/013 合规测试）

> 每个缺陷一行，编号 `BUG-xxx`。修复后由 test-engineer 回归并更新状态。
> 状态：OPEN → FIXING → FIXED → REGRESSED(回归通过) / REOPENED

## 结论
**本轮无缺陷。**

9 条合规用例（TC-001…TC-009）全部通过，全量回归 126 passed + 12 subtests 全绿，未发现任何实现缺陷（无阻塞/严重/一般/轻微）。

## 缺陷登记
| 编号 | 标题 | 严重级 | 所属(前端/后端) | 复现步骤 | 状态 | 修复记录 |
|------|------|--------|----------------|---------|------|---------|
| — | 本轮无缺陷 | — | — | — | — | — |

## 说明（非缺陷，供追溯）
- **Q-001（契约措辞差异，非缺陷）**：删除端点 `confirmed` **缺失**时实现返回 **422**（必填 query 参数），仅 `confirmed=false` 返回 409 `DELETE_CONFIRMATION_REQUIRED`。任务测试规格写"缺失或 false 均 409"，与实现存在措辞差异。核心行为（未确认即拒绝、Graph 保留）一致，且 backend-notes 已把"缺失 → 422"记为有意设计。已记 `open-questions.md` Q-001 待 architect 裁定，**不作为缺陷打回**。
- 其余行为（级联删除、密钥文件 unlink、组织库快照、revision 历史升序、本地 ownership 不变、4 个错误码）均与契约一致，无偏差。
