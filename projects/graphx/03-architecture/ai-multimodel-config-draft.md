---
title: AI Manage 多模型配置 · 设计/契约提案（草稿）
role: architect
status: SUPERSEDED
version: 0.1
updated: 2026-09-14
upstream: [projects/graphx/03-architecture/ai-manage-contract.md, projects/graphx/03-architecture/ai-manage-design.md, projects/graphx/02-requirements/ai-manage-requirements.md]
downstream: [product-manager, frontend-engineer, backend-engineer, test-engineer]
artifact_type: api-contract
source_revision: WORKTREE
approver: architect
approval_evidence: 2026-09-14 用户最终决定改为无默认、逐消息显式选择；正式语义见 ai-manage-contract.md v0.3
---

## 交接说明

给 product-manager、frontend/backend/test：这是把「多模型配置」（R-AIM-007）从 Won't 提前的**设计/契约草案**，供你评审是否就是所需的多模型能力。**不改代码、不改现有契约/需求/规范**；批准后才进入正式需求与契约更新，并由各角色履约。

> 状态：**已被替代（SUPERSEDED）**。本文的默认指针、set-default 和删除默认保护均不再有效；正式语义见 `ai-manage-contract.md` v0.3 与 US-AIM-005 v0.2。

## 1. 你要的到底是什么（先对齐）

你提到「新增模型配置，如我在使用你的时候」。我把这解读为另一种**多模型配置档案**：不只是把唯一的默认配置换掉，而是能**新增并保有多个模型配置条目**，例如：
- `local / DeepSeek-V4-Flash-0731`
- `deepseek-official / deepseek-chat`
- 另一个 OpenAI-compatible 端点 / 别的模型

每条都能独立**保存、测试连接、设为默认**，若干条同时存在，随时切默认。任务仍走「默认配置→根任务整树快照」。

### 不属于本草案（仍为 Won't）
价格/成本换算、预算、自动模型发现、高级运行参数编辑、按角色覆盖配置、组织/多租户。若你以后也要这些，单独提。

## 2. 现有契约如何升级（兼容性优先）

现状：单一配置，靠「全局唯一 `version` + `active` 位」实现覆盖。旧 DTO：
```ts
type ConfigView = {
  schema_version: "graphx-ai-config/v1";
  version: number;             // 全局唯一，覆盖递增
  source: "deployment"|"saved";
  provider: Route; base_url: string; model: string;
  auth_mode: "none"|"api_key"; credential_configured: boolean;
  updated_at: string|null;
};
```

升级为「**配置条目** + 每条自己的版本历史（version 从全局唯一变为每条内唯一）」：

- 每个配置条目有自己的 `id`（不透明，如 `ai-config-…`）。
- 同一条目内 `version` 自增（乐观锁，`expected_version` 依旧用于冲突检测）。
- 「当前默认」= 指向某一条的某个版本（不是把其它配置的 active 清零）。旧逻辑 `active` 仍是默认标识。
- 现有 `GET/PUT /config` 保留为「默认配置」的**便捷别名**，避免破坏已部署前端与已有调用；新增的是 collection 端点。

### 图示：从单例到多条目
```
【现状】  config.version = n (全局唯一), active → 唯一
【多模型】 configs:
   ai-config-aaa (默认) { version:3, provider:local,   model:V4-Flash },
   ai-config-bbb            { version:1, provider:official, model:chat },
   ai-config-ccc (version:0, source:deployment)  ← 无覆盖时的部署 fallback 条目
```

## 3. 建议接口（草案）

Base 仍为 `/api/v1/alpha/ai`，沿用既有错误格式/安全净化。**现阶段只列新增与变更，按你的反馈调整**。

| 方法/路径 | 作用 | 说明 |
|---|---|---|
| `GET /api/v1/alpha/ai/configs` | 列出所有条目（非秘密最新版本）+ `default_id` | 现有 `GET config` 可保留等价于取 default |
| `POST /api/v1/alpha/ai/configs` | 新增一个条目（body ≈ ConfigInput，无 expected_version）→ 返回新 ConfigView | 新条目，不在创建时启动为默认 |
| `GET /api/v1/alpha/ai/configs/{id}` | 某一条目的最新非秘密视图 | |
| `PUT /api/v1/alpha/ai/configs/{id}` | 保存该条目的新版本（body 带 `expected_version`，逻辑同现在单条） | 乐观锁冲突返回 `AI_CONFIG_CONFLICT` |
| `POST /api/v1/alpha/ai/configs/{id}/test` | 用该条目当前表单值连接测试 | 沿用现行为，不保存不激活 |
| `POST /api/v1/alpha/ai/configs/{id}/default` | 把它设为当前默认 | 高度乐观锁；旧的默认条目不再 active 但保留历史 |
| `DELETE /api/v1/alpha/ai/configs/{id}` | 删除条目 | 有规则：若它是默认，需先切走；被活动/排队任务引用的版本不删（保留历史），仅删将来不用的条目 |

> `version`「全局→每条」的变化会影响现有 `GET /config` 返回的 `version`（现为部署时 0，保存后 1/2/…）。迁移后，`version` 表示**该条目的版本**。你的已有前端在 deploy 后会读到新语义。需要一并处理。

## 4. 关键兼容与边界（沿用现有诚实规则）

- **凭据**：仍是服务端受限文件、目标变化须重输、目标隔离沿用现有规则。**每条配置独有凭据版本引用**，不得互相串用。
- **usage / 日志 / Trace 的 `model_snapshot`**：升级为同时携带 `configs/{id}/v{version}`，用 `{config_version, provider, model, source}` 保持现有 DTO 兼容（新增 `config_id`），旧任务 `null` 不伪造。
- **Q-AIM-002 门禁不变**：本草案是「多配置条目」，不改变「能否逐请求采集」的结论。usage 在门禁未关前仍为 `unavailable`，和配置多少无关。
- **任务整树快照**：根任务把「默认条目 + 版本」与现有运行参数一起冻结；子/孙/重试继承。切换默认不影响在途任务树。
- **不破坏现有 `/config`**：保持后端和已部署前端可用；多配置是**加性扩展**。

## 5. 前端交互（建议，供你确认）

模型 tab 从「单条表单」改为：
- 左侧：配置条目列表（名称/来源/当前 default 标记）
- 右侧：选中条目的表单 + 保存 / 测试连接 / 设为默认 / 删除
- 「+ 新增配置」按钮新建空白条目

## 6. 需要你决定

- **A.** 是否这就是你要的「新增模型」？还是你要的是别的（例如单个配置里加多个 model 下拉、或按角色/Graph 用不同模型等）——先澄清避免做错。
- **B.** 若走多条目：**是否需要「删除」能力**，还是先保留只增不删？
- **C.** 默认逻辑：新条目是否可立即设默认，还是要二次确认（涉及路由/凭据切换）。

确认后，我会把它转成正式需求（R-AIM-007 提前）与正式契约更新，再由各角色按 negentropy 流程开发。当前**未改代码、未部署、未 commit**。
