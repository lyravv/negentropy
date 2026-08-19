# 当前生效的协作协议

> **ACTIVE: [v1-docs](v1-docs.md)** — 纯文档协作

## 如何切换协议版本

1. 在 `protocols/` 下写好新版本文件（如 `v2-tools.md`），状态标为 `DRAFT`。
2. 新版本验证可用后，把它的状态改为 `ACTIVE`，把旧版本改为 `SUPERSEDED`。
3. 更新本文件的 `ACTIVE` 指针。
4. 在 `evolution/CHANGELOG.md` 记一笔（协议升级属于团队结构性变更）。

> 原则：**任何时刻只有一个 ACTIVE 协议**。旧版本永远保留，用于追溯和历史项目。
