---
title: AI Manage 交互与技术可行性草案
role: architect
status: APPROVED
version: 0.4
updated: 2026-09-14
upstream: [用户本轮个人产品与先设计后需求指令, 用户2026-09-14无默认最终决定, projects/graphx/STATE.md, graphx/spec/]
downstream: [product-manager, frontend-engineer, backend-engineer, test-engineer]
artifact_type: architecture
source_revision: WORKTREE
reviewers: [product-manager, frontend-engineer, backend-engineer, test-engineer]
approver: architect
approval_evidence: 2026-09-14 architect 依据用户“没有默认；每条消息发送时选哪个模型就用哪个”的最终决定收口
---

## 交接说明

给 product-manager、frontend/backend/test：正式方向是个人多配置库、逐消息显式选择、整树快照、逐请求用量和复用任务 Trace。不得实现隐式默认。主要未决项只剩 pinned DSH 的逐请求观测完整性；Q-AIM-002 未关闭前 usage 必须诚实显示 unavailable/partial。

## 0. v0.3 覆盖性决定

本节覆盖本文其余仍提及“单一默认配置”的早期探索文字：系统不存在 default/active 指针；配置列表、列表第一项、最近一次选择和部署配置均不是用户本次选择。AI Manage 页面可为编辑方便选中第一条配置，但该编辑态与 composer 的消息选择态必须隔离。composer 每次根消息完成发送后应回到“未选择”，下一条消息再次显式选择；缺失选择时前后端均不得发送/接受任务。派生任务不是新根消息，必须继承根快照而不再次选择。

## 1. 范围与决定来源

用户已决定：先设计 → 需求 → 开发 → 验收；优先 AI Manage，覆盖模型配置、用量统计、日志；Applications 仅一级占位；GraphX 是个人产品，不新增 tenant、组织或 RBAC 平台。日志展示真实公共助手输出及工具参数/结果，不用概括文案代替原始内容。三个 tab 是本文的布局建议，不是用户明确决定。

布局、字段、接口分工与实施顺序已按 v0.3 收口。模型按角色覆盖、价格/成本、预算限制、自动清理/日志删除、导出、扩展运行参数编辑及自动模型发现均不在本轮；如需要，由产品角色单列取舍，不能借实现扩展范围。已有内部 tenant 字段的迁移不属本轮。

## 2. 最低充分交互

一级导航保留 Graphs、Resources，加入 AI Manage、Applications。AI Manage 不依赖当前选中 Graph；三个 tab 为“模型 / 用量 / 日志”。Applications 打开静态“尚未开放”占位页，无创建、发布、应用运行或后端接口。

| 页面 | 建议首屏与操作 | 反馈与异常 |
|---|---|---|
| 模型 | 多配置条目库：名称、兼容路由、Base URL、模型 ID、凭据状态；每条保存与测试连接独立；显示条目版本 | AI Manage 的编辑选中不传播到 composer；保存不能显示成已验证成功；字段错误原位提示；保存失败保留非秘密输入 |
| 用量 | 时间范围（建议默认近 7 日）；已观测请求数、重试请求数、已知输入/输出 token、未知用量请求数；按时间列请求明细，支持 Graph/模型/状态筛选 | 完全无记录与旧任务未采集分开；unknown 显示“未知”，不能作 0；部分数据明确标“已知小计”；加载失败可重试 |
| 日志 | 跨 Graph 任务列表：时间、Graph、角色、任务状态、模型快照；时间/Graph/状态筛选；点击打开执行轨迹 | 历史缺模型显示“未记录”；任务不存在显示不可用；运行任务可刷新，错误不清空已加载轨迹 |

### 2.1 视觉与 composer 收口

- 模型页是纯配置库。左侧选中条目只表达编辑焦点；页面标题、列表项、详情字段、提示和保存/测试反馈不得生成“当前在用”“激活”“默认”语义。配置名按用户保存值原样展示，系统不附加状态后缀。
- Graphs 收起后直接复用 peer navigation card primitive：可用宽度 100%、最小高度 54px、白色背景、1px `gray-200` 边框、11px 圆角、水平 14px 内边距、图标文字 8–10px 间隔，兄弟卡 9px 间距；inactive 不保留 Graph 列表的白底内层、粉色边框或额外 padding。active 状态与其他入口共同使用 pink-50 背景和 pink 边框/文字。
- composer 采用单一大边框容器，最小高度 96px。文本输入区在上，起始可见约三行；底部是同一容器内工具栏。模型选择靠右、发送按钮最右，紧凑显示配置名称和 chevron，宽度受限时单行省略。附件及其他工具靠左。选择菜单在入口上方向上展开，名称为主信息，provider/model 为次信息，并提供“管理模型配置”。
- 空配置库时，composer 的模型位置显示可操作的“配置模型”入口；有配置但本条未选时显示“选择模型”。配置页编辑选中与 composer 状态完全隔离，发送成功后清空本条选择。

日志详情沿用现有 Trace 的助手/调用/结果行与展开原文能力，保留任务入口返回位置。排序采用服务端事件顺序与稳定 ID，不仅凭同秒时间。大列表分页；详情复用组件和 API，不另造第二套摘要日志。详情中保留脱敏/截断/历史原文缺失标识；“原文”指公共内容的受控保存版本，不承诺未裁剪 SDK dump。

只有规范化后的 Base URL 与路由均未变化时，空凭据才保留旧值；改目标必须重新提供凭据或明确选择无凭据，测试也不能将旧 secret 自动发送到新目标。首版不提供凭据删除管理。GET/保存响应仅返回 configured/source，不返回 secret、secret path、secret reference 或掩码原值；前端不在 localStorage 保存凭据。离开未保存表单提示丢弃；保存/测试期间禁用重复提交；并发版本冲突提示重新载入，避免静默覆盖。

手动测试连接使用当前表单的临时配置发出一次小请求，经相同 SDK/Cordis 路径验证 endpoint/model/认证；执行前显示“可能消耗 tokens”。测试不保存或激活配置，不调用业务工具。成功只对应本次表单值，编辑后清除成功标识。服务端创建独立测试关联 ID，用量标为 connection_test、无 Graph 归属，业务任务汇总默认排除；测试分页明细仍遵循实际 attempt/unknown 语义。测试临时凭据只在服务端请求作用域使用，不进入持久化日志。

## 3. 已有实现与真实缺口

以下路径相对 `/home/wangling/develop_team`，均为本轮只读代码证据；没有读取 secret 文件、运行真实模型或验证运行中的服务。

| 证据 | 当前事实及影响 |
|---|---|
| `graphx/src/graphx_alpha/config.py:17`、`:58` | Settings 是启动时 frozen 配置，provider/model 来自环境；新增 UI 仅写配置表而不接执行链不会生效 |
| `graphx/src/graphx_alpha/harness_executor.py:562`、`:700`、`:865` | 多条执行路径把 Settings 模型传给 WorkerConfig；需要统一解析，覆盖 GraphX、Resource Manager、Builder、Reviewer、Tester 和保留入口 |
| `graphx/config/harness/graphx-cordis.yml:27`、`graphx/scripts/deepseek_harness_worker.py:448`、`:532`、`:600` | local route 的 endpoint/model 由 Cordis 模板提供；local 使用固定非秘密占位 key，official 分支有另一套凭据加载。UI 改 model 名不等于 endpoint/认证改变，必须让快照同时驱动 Cordis 和 worker |
| `graphx/tests/test_model_runtime_config.py:12` | `config/model-runtime.json` 是现有配置验证/说明资产；没有据此证明它是动态运行时权威。旧默认与无 max_tokens cap 行为应保留 |
| `graphx/src/graphx_core/deepseek_adapter.py:68`、`:84` | 当前 progress allowlist 没有 usage；WorkerConfig 没有完整动态 endpoint/credential 契约，需要新增明确投影 |
| `graphx/src/graphx_core/runtime.py:16` | canonical 枚举已有 `usage.recorded`，但枚举存在不等于采集、持久化、聚合已经实现 |
| `graphx/scripts/deepseek_harness_worker.py:168`、`:181`、`:204` | `assistant/message` 只取 text blocks；工具事件已有 original 参数/结果；step/start 产生的 thinking_summary 是程序状态描述，不能冒充模型思考 |
| `graphx/src/graphx_alpha/service.py:694`、`:1292`；`graphx/apps/web/src/TaskTrace.tsx:27` | 公共事件已有白名单，Trace 已显示 original 并跳过 status/thinking_summary；API 为 `/api/v1/alpha/tasks/{task_id}/trace`（`api.py:320`） |
| `graphx/src/graphx_alpha/entities.py:246`、`:302` | TaskActivity、PublicActivityEvent 可用于任务索引与轨迹复用；无需复制一套原始 Harness session 存储 |

## 4. 模型配置如何真正生效

保存个人级配置条目版本（非秘密字段）和对应的受保护凭据版本，不维护默认指针。现有 Settings/Cordis 只服务兼容读取和旧运行，不得替新根消息选择模型。已有 local 无认证语义保持可表达。首版仅承诺已经接通的路由类型，不在下拉框中伪装支持任意厂商协议。

在用户根任务创建事务中解析并冻结模型快照，至少包含配置版本、provider、model、endpoint 标识与实际运行参数；公开 DTO 只返回必要非秘密元数据。所有后续子任务、孙任务、协调回合和重试继承该根快照。Worker 从快照生成请求与本任务 Cordis 配置，并在服务端解析凭据版本。凭据不进入模型 prompt、上下文 pack、公共事件或运行指纹 hash 输入。任务中途保存配置不会改变整条在途任务树；重启后排队任务仍能复现其快照。旧排队任务缺快照时在首次执行补建并明确 provenance，不伪造历史配置；同一遗留活动任务树须复用首次补建版本，已结束历史任务保持未记录。

建议：同一会话下一条用户消息创建的新根任务使用当时配置，已有根任务的后续委派仍使用原快照。该整树规则替换 v0.1 的委派读取新配置建议，依据为需求草案 R-AIM-002/US-AIM-001 AC2，仍是待用户确认业务语义。

保存非秘密字段与凭据须具有一致性；写入失败不激活半份配置。服务端持有旧凭据版本直到引用它的整条活动任务树结束（包括排队/等待子任务），禁止编辑全局环境变量造成并行串用。版本冲突、参数不支持、凭据不可用分别返回可读且脱敏的错误。具体 DTO/存储实现由正式契约收口，本文不规定 ORM 或单独配置服务。

## 5. 每次 LLM 请求用量与 DSH 可行性

本地 upstream checkout `spikes/deepseek-harness-upstream@47f943859bef60e4160492346772ded9b24f765a` 的 `packages/core/agent-loop/src/agent.ts:382` 在 assistant/message data 上附带可选 usage；`packages/llm/llm/src/types.ts:135` 定义 TokenUsage，`packages/llm/llm-retry/src/index.ts:150` 区分 retry 与 retry-started。因此不能以“没有 usage.recorded 事件名”为由断言 DSH 无 usage，也不能把重试计划当成已发请求。

但当前锁定 SDK/runtime 为 `0.1.0rc6`，`graphx/config/harness-runtime.lock.json` 的 source_commit 为 null；本地 upstream 不是该二进制的等价性证据。成功 assistant/message 的 usage 也不能覆盖失败前已发生的请求。正式实现前须对 pinned runtime 做受控 mock transport/公开通知探针，确认请求边界、稳定序号、usage 字段、失败、重试、取消和重复投递；不读私有 session JSONL、不解析二进制内部事件作为产品契约，不自动升级 SDK。

最低数据语义建议：每一次实际 provider 请求 attempt 一条记录，关联 task/run、role、配置快照、逻辑请求 ID、attempt 序号、开始/结束、结果、输入/输出 token 可空、usage_source 与 completeness。网络重试是新的 attempt；同一工具循环中的下一次 LLM 请求也是新逻辑请求。缓存、reasoning token 如公开 usage 提供则作为明细且按 provider 定义处理，不能与已包含它们的 total 重复相加。

在 worker/adapter 边界只投影计数和必要关联信息为 GraphX typed usage，独立持久化；用稳定 event/request/attempt key 幂等更新，重放不能翻倍。使用服务端任务身份关联，不能相信模型提供 task ID。用量接口独立于现有公共活动白名单，不能为获取 token 放开原始事件响应。

| 情形 | 必须记录/显示 |
|---|---|
| 已发请求，返回明确 usage | 保留 provider 计数；成功与失败独立于有无用量 |
| 请求发出后报错/取消/超时，无 usage | attempt 计入请求数；token=null，unknown；不得估算为 0 |
| 重试已安排但未实际发出 | 仅重试状态，不增加实际请求数 |
| 部分 attempts 有 usage | 汇总已知 token，另报未知数量；不能宣称完整总量 |
| 老任务或缺失请求边界 | 显示未采集/覆盖不完整，不倒推聊天字数，不伪造请求数 |
| 事件重复、先结束后到达 usage | 幂等合并且保留来源；不得因任务终态丢弃迟到有效计数 |

若 pinned 的公共接口无法覆盖实际请求边界，必须选择受支持的公开 LLM adapter instrumentation，并单独评审该扩展；在此之前可交付其他切片，但逐请求统计不得标完成。成本估算不在本轮默认范围，不能用 token 数乘未经批准的单价展示费用。

## 6. 最小接口分工与实施切片

待需求/消费者确认的新增边界只有：个人模型配置读取/版本化保存及独立连接测试；按时间、用途与过滤条件分页的请求用量查询（同口径汇总）；跨 Graph 的任务日志索引。任务详情继续用现有 task trace。时间范围使用明确时区和半开区间，排序加稳定 ID；不新增 Application API 或组织权限接口。正式参数、字段、错误码和 schema 在批准后的规范中成为唯一事实源，不复制到三套全项目架构文档。

1. **需求与可行性闭环**：产品角色确认布局、字段、快照继承规则和验收标准；前后端/测试评审；用 pinned runtime 的受控探针决定 usage 接入边界。用户批准方案和需求后再开发。
2. **配置生效**：持久化版本及凭据、旧配置 fallback、整树快照、所有执行入口消费；用受控目标验证保存 A→创建根任务→保存 B 后旧树后续委派与重试仍用 A、新根任务用 B，重启后也成立。核对实际 SDK/Cordis 请求中的 endpoint/model/认证，仅 worker 回显不算通过；连接测试不激活配置且分类记录，全部读取/异常/日志响应不含假测试密钥。
3. **用量采集与页面**：先落每请求记录和幂等，再做聚合/明细 UI；验证多轮、工具循环、重试、失败、缺 usage、重复、取消及旧任务，不以任务数代替请求数。
4. **日志与导航**：增加 AI Manage 和 Applications 占位，日志索引复用 TaskTrace；验证原始公共文本和 tool args/results 的可达性、缺失/截断提示、运行刷新与分页；不出现伪 thinking。
5. **验收**：测试角色核对规范、契约、实现同一 revision；相关确定性测试与前端构建完成后，再按授权做真实模型 smoke。当前没有执行上述测试，不宣称功能或部署完成。

## 7. 交给产品与消费者的未决点

- **D-01（backend/test）**：pinned SDK 的公开 request/usage/retry 覆盖证据；未确认前阻塞“逐请求完整统计”完成判定，不阻塞需求编写。
- **D-02（product/user，RESOLVED）**：确认多配置无默认、逐根消息选择、现有支持字段、根任务整树继承、独立小请求连接测试及用途分类；以需求 v0.3 Q-AIM-001 为准。
- **D-03（frontend/backend/test）**：确认列表过滤/分页、公共原文裁剪标识、历史缺字段兼容及凭据保存异常路径，在正式契约冻结时收口。
- **D-04（product/user）**：角色覆盖、成本、清理等扩展仅候选，不纳入默认开发验收。

本文件提交 IN_REVIEW 等待需求与受影响消费者评审；无用户批准证据，无代码、规范、STATE/WORKBOARD 写入，无 commit/push/deploy。

### 2026-09-14 技术评审记录

续接：用户随后要求继续，编排者登记为首版范围推进确认；需求批准证据由需求作者/编排者同步。本文保留前置设计历史，开发以 `ai-manage-contract.md` 经消费者评审的具体契约为准，不能将本文历史“待确认”表述推翻最新用户授权。

已只读评审 `02-requirements/ai-manage-requirements.md`、`ai-manage-iteration-plan.md` 及 US-AIM-001～004（均 v0.1/IN_REVIEW）。范围与验收可映射当前执行链/公共 Trace；v0.2 已收敛快照和连接测试差异，没有新增阻碍用户范围评审的矛盾。Q-AIM-002 仍是逐请求统计实现与验收的技术门禁；正式契约须明确 usage 按字段缺口、失败 attempt 已知 usage 保留及严格 worker schema 扩展。此结论是技术 review，不是需求或架构批准，也不替代消费者对最终接口的评审。
