---
title: AI Manage 首版 API 与运行数据契约
role: architect
status: APPROVED
version: 0.3
updated: 2026-09-14
upstream: [projects/graphx/02-requirements/ai-manage-requirements.md v0.3, projects/graphx/02-requirements/user-stories/US-AIM-005-multimodel-config.md v0.2, 用户2026-09-14无默认最终决定]
downstream: [backend-engineer, frontend-engineer, test-engineer]
artifact_type: api-contract
source_revision: WORKTREE
reviewers: [backend-engineer, frontend-engineer, test-engineer]
approver: architect
approval_evidence: 2026-09-14 architect 按用户最终“无默认、逐消息选择”决定收口 v0.3；批准多配置/快照/日志 A 边界及 B DTO，Q-AIM-002 未关闭前禁止验收真实逐请求采集
---

## 交接说明

首版采用个人多配置条目库、逐根消息显式选择、整树快照、独立连接测试、用量和只读日志；Applications 仅静态页。系统没有默认模型，任何隐式首项/最近选择/deployment fallback 都不得创建新根任务。A（配置、日志、导航、连接测试）及 B 的 DTO 已批准；B 的真实逐请求采集仍受 Q-AIM-002 pinned runtime 探针门禁约束。

## 1. 通用约定与切片

Base 为 `/api/v1/alpha/ai`，沿用 FastAPI 直接 JSON 对象与现有 `detail: {code,message}` 错误格式。API 在当前个人部署的既有访问边界内，不新增 actor/tenant 参数。所有时间为带时区 RFC3339 UTC；ID 为服务端不透明字符串。请求拒绝额外字段。字符串不接受控制字符。响应永远不包含 secret、秘密位置或 SDK 原始错误。

业务错误用当前 ProductError 规则：不存在 404，其余冲突 409；输入错误 422。AI 接口错误顶层增加 `schema_version:"graphx-ai-error/v1"`，保留 detail 格式。AI 接口必须净化 FastAPI validation 错误，不能回显含凭据的 input/context；422 返回 `{schema_version:"graphx-ai-error/v1",detail:{code:"AI_INPUT_INVALID",message:"配置或查询参数无效"}}`，允许额外安全 field_errors（仅 field/code）。

| 方法/路径 | 故事 | 返回 | 切片 |
|---|---|---|---|
| GET `/config` | 001 | ConfigView | A：只读兼容别名；非默认、不得用于任务选择 |
| POST `/config/test` | 001/002 | ConnectionTestResult | A；统计完整性属 B |
| GET `/configs` | 001/005 | ConfigList | A：条目库 |
| POST `/configs` | 001/005 | ConfigView | A：新增条目 |
| PUT `/configs/{config_id}` | 001/005 | ConfigView | A：新增条目版本 |
| DELETE `/configs/{config_id}` | 005 | 204 | A：停止该条目后续选择；不破坏冻结快照 |
| GET `/logs` | 003 | LogPage | A：日志/导航 |
| GET `/usage` | 002 | UsagePage（含同过滤汇总） | B：探针后采集验收 |
| GET `/tasks/{id}/trace`（现有 alpha 路径） | 003 | 现有 TaskTraceData | A；无替换 |

A 可先批准开工，不得宣称 B 已满足。B 未启用时 `/usage` 返回 `collection_state:"unavailable"` 与明确覆盖缺口；页面显示尚未开始完整采集，不伪造 0 请求完整统计。连接测试此时仍建立独立测试运行记录，usage 无观测则未知。

## 2. 配置 DTO

```ts
type Route = "local" | "deepseek-official";
type ConfigView = {
  schema_version: "graphx-ai-config/v1";
  config_id: string | null; // null 只允许 GET /config 的部署兼容视图
  version: number; // 每个 config_id 内递增；部署兼容视图为 0
  source: "deployment" | "saved" | "live";
  name: string;
  provider: Route;
  base_url: string;
  model: string;
  auth_mode: "none" | "api_key";
  credential_configured: boolean;
  updated_at: string | null;
};
type ConfigInput = {
  schema_version?: "graphx-ai-config-input/v1"; // 兼容既有 alpha 输入风格，可省略
  expected_version: number;
  provider: Route;
  base_url: string;
  model: string;
  auth_mode: "none" | "api_key";
  api_key?: string; // 仅写入；省略或空字符串按保留规则
};
type ConfigCreate = Omit<ConfigInput,"expected_version"> & {name:string};
type ConfigList = {schema_version:"graphx-ai-config-list/v1";items:ConfigView[]};
```

Base URL 长度 1..2048，绝对 http/https URL，禁止 userinfo、query、fragment；保留 path，规范化 scheme/host、默认端口及尾部 slash 后比对完整目标。模型长度 1..256，trim 后非空；key 最大 8192 字符，不 trim 非空 key 内容。仅上述两条已适配路由；local 走 OpenAI completions 兼容路径，official 走既有受支持路径。保存必须校验路由确可配置相应 endpoint，否则拒绝，不能保存后静默忽略。无认证仅 local 允许；official 必须 api_key。

`expected_version` 不等该条目最新版本返回 `AI_CONFIG_CONFLICT`，不执行网络请求或写入新版本。只有 provider 与规范化完整 base_url 都相同，才允许省略/空 key 保留；模型 ID 变化不改变凭据目标。目标改变而 api_key 模式为空返回 `AI_CREDENTIAL_REQUIRED`。local 明确 auth_mode=none 可建立无凭据新版本，不复用旧 key；该动作不是删除旧版本秘密。所有安全解析在保存与测试共用，不能仅依赖前端判断。

`GET /configs` 只列用户保存且未删除条目的最新版本，不注入部署默认。`GET /config` 仅为旧消费者保留：无条目时可返回 `config_id:null,version:0,source:deployment`；有条目时可返回确定性的兼容视图，但它不具有 default/active 语义，composer 和任务创建不得消费它。写入只使用 collection 接口；`PUT /config` 和 set-default 接口不属于 v0.3 契约。保存原子追加该条目的新版本并返回安全视图；无网络测试隐式副作用。请求失败保留非秘密输入，前端清理不再使用的 key；不在 URL、浏览器持久存储或调试日志放 key。

## 3. 测试连接

POST 接收 ConfigInput；相同版本、认证目标保留规则；使用当前表单临时值，不保存或修改任何配置条目。服务端分配 test_id 并创建 purpose=connection_test 的运行记录（task_id/graph_id=null）。经正常 worker/SDK/Cordis 发小请求，业务工具关闭，不包含用户图/聊天。总超时建议 30 秒，限制测试输出至 16 tokens；该上限仅测试使用，不能改变真实任务原有无显式 max_tokens cap。

```ts
type ConnectionTestResult = {
  schema_version: "graphx-ai-connection-test/v1";
  test_id: string;
  status: "succeeded" | "failed";
  tested_at: string;
  duration_ms: number;
  provider: Route;
  model: string;
  error: { code: string; message: string } | null;
};
```

已执行测试的 provider 错误以 HTTP200/status=failed 返回，error.code 仅 `AI_TEST_AUTH_FAILED|AI_TEST_UNREACHABLE|AI_TEST_TIMEOUT|AI_TEST_FAILED`，消息固定安全文案；参数/版本错误用 422/409，不创建虚假已发请求。返回不含模型原文或 key。客户端执行前显示可能消耗 tokens，成功只对应该次字段值，编辑后失效；请求期间禁止重复点击。统计每个实际 attempt，可能由 runtime 重试导致多次，不能把点击次数作请求数。

## 4. 持久数据与快照

复用当前 SQLAlchemy/Database 生命周期。最低新增事实：配置版本、任务模型快照关联、测试运行、请求 attempt；TaskActivity/PublicActivityEvent 不复制。配置版本一行保存 config_id、条目内 version、名称、非秘密 provider/base_url/model/auth_mode、时间和服务端 credential_version_ref；不存在 active/default 指针。秘密保存在现有风格的服务端受限文件存储（目录0700、文件0600、Git外），配置表只存内部版本引用。先写完整秘密再提交配置版本；失败不能半写入。不得删除已有秘密或改写旧版本。

根用户消息必须携带用户本次明确选择的 `ChatRequest.config_id`；服务端在接受消息并创建根任务的同一事务中解析该条目最新版本并绑定不可变 snapshot_id。快照存 config_id/config_version/source/provider/base_url/model/auth_mode、有效 max_tokens/timeout 和内部 credential_version_ref。子任务、孙任务、GraphX协调回合与 retries 使用根 snapshot_id，不再读取配置库。服务端 root_task_id 为关联权威，不能由模型提供。缺少/空 config_id 返回 `AI_CONFIG_REQUIRED`，不存在或已删除返回 `AI_CONFIG_NOT_FOUND`，不得回退第一条、上一条或部署配置。等待/排队/重启恢复及任务派生均保留快照；旧秘密至少保持到整树不再可能派生任务，本轮不做自动清理。

旧已结束任务 snapshot=null，API 返回 model_snapshot=null，禁止用当前配置补历史。旧活动树首次恢复时原子补建一份 source=legacy_recovery 的快照并整树共享；保存补建时间且不称其原始启动配置。不能因补快照修改旧公共输出。

公开快照统一为 `{config_id:string|null,config_version:number,provider:string,model:string,source:"user_selected"|"legacy_recovery"}`，不回 endpoint 或 credential refs；日志/usage 可用该 DTO。历史已结束任务仍可为 null；配置页允许显示用户配置的非秘密 endpoint。

## 5. Worker 边界（A）

读取证据：`graphx_alpha/config.py:17` frozen Settings；`harness_executor.py:562,700,865` 多条 WorkerConfig 构造；`deepseek_adapter.py:190` request/v1；`deepseek_harness_worker.py:300` 请求校验、`:448` Cordis渲染、`:532` 凭据路由、`:600` SDK创建。

不修改进程全局 Settings 作为热更新。executor 各入口以可选快照参数扩展，统一生成 WorkerConfig，旧 fake/mock 调用不要求新参数。无快照保持 request/v1 路径；提供快照的新请求使用 `graphx-dsh-worker-request/v2`，新增：

```ts
runtime_model: {
  snapshot_id: string;
  provider: "local" | "deepseek-official";
  base_url: string;
  model: string;
  auth_mode: "none" | "api_key";
  credential_file: string | null; // 内部受限绝对路径，只在worker请求内
}
purpose: "task" | "connection_test"
```

其余既有 prompt/session/workspace/plugin/max_tokens/timeout 字段保持；重复的顶层 provider/model 若为兼容暂留必须与 runtime_model 一致，否则拒绝。v1 请求兼容原部署逻辑；v2 缺 runtime_model 拒绝，不能 fallback 悄悄切模型。credential_file 只允许服务端生成并通过既有 allowed_root/secret位置校验，不接受模型或浏览器路径。

worker 从快照渲染每次运行独立 Cordis endpoint/model/凭据环境变量；api_key 模式不再覆盖成 local 占位 key；none 保留现有非秘密占位行为。秘密只进入隔离 worker 子进程环境，禁止命令行参数/全局父进程环境，finally 清理引用；URL 重定向不得把认证带往新 origin。测试和任务使用相同路由解析及 SDK 调用边界。

已有 success/progress v1 在 A 保留，不往 strict extra=forbid 类型任意塞 usage。所有 argv/stdout/stderr/validation 错误出口不得输出 credential_file/key。验证必须检查受控 HTTP 目标实际收到 endpoint/model/认证，不能只比较 WorkerConfig 回显。

## 6. 列表、日志与 Trace

GET logs 查询：`from`/`to` 可省略（服务端默认最近7日并回显），RFC3339，from<to，时间区间 `[from,to)`；`graph_id?`、`status?`、`limit=50`（1..100）、`cursor?`。status 为 queued/running/waiting/completed/failed/cancel_requested/cancelled，按既有任务状态投影，不另建状态机。筛选 graph 不存在返回空集合；格式非法422。

```ts
type LogRow = {
  task_id:string; graph_id:string; graph_name:string | null;
  role:string; status:string; created_at:string; ended_at:string | null;
  model_snapshot:PublicModelSnapshot | null;
};
type LogPage = {
  schema_version:"graphx-ai-log-page/v1";
  items:LogRow[]; next_cursor:string | null;
  range:{from:string,to:string};
};
```

按 `(created_at DESC, task_id DESC)` keyset 分页；cursor 绑定筛选与首次查询截止时间（不允许翻页中改变筛选），非法/不匹配422；新增任务通过刷新首页可见。cursor 长度上限4096，在现有 service 内解析与构造 SQL 查询即可，无新增分页服务。task status 仍可实时更新，不承诺跨页事务快照。

日志详情调用现有 `/api/v1/alpha/tasks/{task_id}/trace`，返回结构保持；如补 model_snapshot 必须可选，旧组件可忽略。展示 public assistant_output.original、tool_call.original、tool_result.original；排序沿既有 agent/sequence 稳定关系，关联 call_id；同秒不依赖时间独排。保持 `thinking_summary` 不显示成思维链。已有红线：只允许公共text block，不公开 private reasoning/system prompt/raw session。

当事件有 original 时继续使用受控原文；新增可选 `original_meta:{redacted:boolean,truncated:boolean}` 随公共投影返回以标注新采集情况；旧事件无该字段显示“历史记录，脱敏/截断标记未记录”，无 original 则“该历史事件未保存原文”。不重新从摘要生成原文。新标记在实际净化/裁剪点生成，不能臆测。Graph内与AI日志复用同一 TaskTrace 组件。

## 7. Usage DTO 与独立门禁（B）

查询复用 logs 时间/cursor/limit，增加 `purpose=task|connection_test|all`（默认task）、`model?`（精确值）、`status=running|succeeded|failed|cancelled|timed_out|unknown`；graph_id 只匹配实际 task 的图。汇总和明细用完全相同过滤，按 `(started_at DESC, id DESC)` 分页；汇总始终覆盖全部匹配记录，不仅本页。

```ts
type UsageRow = {
  id:string; logical_request_id:string; attempt:number; purpose:string;
  task_id:string|null; test_id:string|null; graph_id:string|null; role:string|null;
  model_snapshot:PublicModelSnapshot|null;
  started_at:string; ended_at:string|null; status:string; is_retry:boolean;
  input_tokens:number|null; output_tokens:number|null;
  usage_source:"provider"|"unavailable";
};
type UsagePage = {
  schema_version:"graphx-ai-usage-page/v1";
  items:UsageRow[]; next_cursor:string|null; range:{from:string,to:string};
  collection_state:"available"|"partial"|"unavailable";
  coverage:{request_boundaries_complete:boolean; historical_gap:boolean};
  summary:{
    observed_requests:number; retry_requests:number;
    input_tokens_known:number; output_tokens_known:number;
    input_known_requests:number; output_known_requests:number;
    unknown_usage_requests:number;
  };
};
```

token 只接受非负整数或null；显式0计入 known_requests。unknown_usage_requests 指输入或输出任一缺失的已观测请求数；两个字段 known coverage 分别计算。历史未知请求数量不可计算时用 coverage 标志，不虚构分母。没有边界证据时 observed_requests=0 只表示未观测，collection_state/coverage 必须同时显示，不能称零实际消耗。失败 attempt 的已知用量必须保留。

新增 attempt 唯一键 `(run_id, logical_request_id, attempt)`；每次真实 provider 发出单独 attempt。scheduled retry 不新增。通知和最终结果使用同 key 幂等合并；已知值与冲突值不能随意相加，冲突记不完整并保留诊断，不覆盖为0。token 明细如cache/reasoning已有包含关系，本轮不新增总费用或重复 total。

在锁定 rc6 的公开通知边界得到确定性证据后，再冻结 GraphX typed usage progress/result v2 的映射；至少白名单投影 request_started/request_finished 及可选计数、稳定attempt key。GraphX内部 ID 由适配层绑定，不接受模型自报。该 runtime 映射尚未批准，不能解析私有session补数；探针不足时暂停B验收并提交受支持adapter instrumentation选择。UI DTO 可据此实现，不能先宣称采集完整。

探针输入约束：不能把 request/header 或 step/start 当成实际 HTTP 请求；retry-started 仍需核对是否真的发送。公开通知按 sessionId/seq 去重并隔离 descendant；usage chunk 和 assistant/message.usage 不重复入账。输入 token 是否包含缓存须根据 pinned provider adapter 实测后定义归一化，不能直接把上游 inputTokens 误当全输入。失败 usage 优先保留已观测计数。

## 8. 批准前消费者确认与验收

Frontend：ConfigView/Input、测试反馈、跨目标凭据提示、LogPage/UsagePage、旧 Trace 可选字段与分页；Backend：全入口快照、原子版本、隔离秘密及 v1/v2兼容；Test：受控目标参数生效、整树重启、假密钥所有出口、旧原文、用量null/0/partial/retry/重复等。

A 通过相关确定性测试、构建和diff check后可交付本地实现；B须先关闭Q-AIM-002再验收逐请求完整性。消费者意见在本节或工作项记录后由architect批准A/B相应边界；本文当前IN_REVIEW。产品运行规范、requirement ID、schema及manifest同步由后续获认领实现任务完成，本文件不越权写入代码规范。无commit/deploy授权扩展。
