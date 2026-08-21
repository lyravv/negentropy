# negentropy · 负熵开发团队

negentropy 是一个正在真实项目中使用的、文档可移植且带机器校验护栏的软件开发团队定义。它把模糊诉求逐步变成有批准者、有 revision、有测试证据、可续接的软件交付。

团队遵循[“最低充分秩序”](team/philosophy.md)：不追求最多角色、最厚文档或最严审批，而以最低持续成本抑制关键漂移。任何流程扩张都应先证明它防止的失败值得其维护成本。

## 当前能力（0.3.0）

- 8 个正式角色：orchestrator、业务、产品、架构、前端、后端、测试、运维；
- 协议 `v1.1-docs`：文档 + 审批/revision/并发证据；
- 六种 workflow profile，允许已有规范项目、feature、bugfix、spike 和运维任务按需裁剪；目前 `existing-spec` 已经 GraphX 验证，其余为 beta/experimental；
- `STATE.md` 负责项目快照，`WORKBOARD.md` 负责写任务认领和 lease；
- `team.yaml` 是枚举与审批策略的机器权威来源，`team/governance.md` 解释其语义；
- `python scripts/validate_team.py` 在工作前后检查结构与活跃项目。

团队定义是 Markdown + YAML，不绑定特定 Agent 框架。`team.yaml` 是受校验的清单和未来编排输入，但 0.3.0 不宣称仅解析 YAML 就能安全自治；实际执行还必须读取治理、项目规则和用户授权。

## 目录

```text
negentropy/
├── team.yaml
├── team/
│   ├── governance.md          # 审批矩阵、状态、action mode
│   ├── philosophy.md          # 最低充分秩序与团队设计取舍
│   ├── concurrency.md         # 认领、lease、文件范围、集成
│   ├── workflow.md
│   ├── workflow-profiles.md
│   ├── orchestration.md
│   ├── handoff.md
│   ├── protocols/CURRENT.md
│   ├── roles/<role-id>/{AGENT.md,skills.md}
│   └── templates/
├── projects/<project>/{STATE.md,WORKBOARD.md,open-questions.md}
├── scripts/validate_team.py
└── evolution/{CHANGELOG.md,roadmap.md}
```

## 开始新项目

1. 复制 `projects/_template`。
2. 在 STATE 选择 workflow profile，登记每类权威来源和 revision。
3. 初始化 WORKBOARD；任何写任务先认领。
4. 按 `team/handoff.md` bootstrap，运行校验。
5. 按治理矩阵评审/批准；实现完成不自动意味着可以 push 或部署。

## 继续已有项目

一句话要求继续项目时：先读 `projects/<project>/STATE.md` 和 `WORKBOARD.md`，再读 `team/handoff.md`。STATE 提供“在哪和下一步”，WORKBOARD 保护“谁正在改什么”。

### 真实项目示例：GraphX

当前 GraphX 项目使用 `existing-spec` profile：阶段 1–3 由其外部规范事实源替代，不在 negentropy 中复制规范。实际仓库位置、规范路径和 revision 只登记在项目入口 [`projects/graphx/STATE.md`](projects/graphx/STATE.md) 中；这不是 negentropy 的通用路径约束。

## 角色入队

角色必须读取：

1. 自己的 `AGENT.md` 与 `skills.md`；
2. `protocols/CURRENT.md` 指向的协议；
3. philosophy、governance、concurrency；
4. 项目 STATE/WORKBOARD、项目规则和本工作项的权威输入。

任务提示必须包含 action mode、base revision、写入范围、依赖和验收命令，见 `team/orchestration.md`。

## 校验

```bash
# 在 negentropy 仓库根目录执行
python scripts/validate_team.py
python scripts/validate_team.py --project <project-name>
```

例如，校验当前 GraphX 项目：

```bash
python scripts/validate_team.py --project graphx
```

校验依赖列在 `scripts/requirements-validation.txt`；当前开发环境已具备。校验器即使缺少 `jsonschema` 仍执行内建结构检查并给 warning，`PyYAML` 是读取 `team.yaml` 的必需依赖。

error 表示团队无法可靠运行，必须修复；warning 表示历史文档迁移或易漂移信息，允许在不相关任务中暂缓，但下一次触碰该文档时处理。

## 演进原则

团队能力写入 `team/`，项目事实写入项目权威来源和 STATE/WORKBOARD。结构变化记 CHANGELOG；只有经过项目验证或明确通用的经验才进入稳定技能，避免过拟合单次任务。
