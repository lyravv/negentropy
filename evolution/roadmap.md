# 团队演进路线图（Roadmap）

> 团队"接下来要变成什么样"的规划。
> 来源：项目复盘的行动项、使用中的痛点、外部工具成熟度。
> 每项落地后，移入 `CHANGELOG.md` 并在此标记完成。

## 状态图例
`PLANNED` 规划中 · `IN_PROGRESS` 进行中 · `DONE` 已完成

## 近期（提升日常效率）

| 项 | 类型 | 状态 | 说明 |
|----|------|------|------|
| 用真实项目跑通 v1.1 全流程 | workflow | IN_PROGRESS | GraphX 已验证 existing-spec 的实现/测试/续接；尚未验证完整生产发布和复盘 |
| 沉淀各角色首批 skills | skill | PLANNED | 前 1-2 个项目后，把通用偏好写进各 skills.md |
| 模板瘦身/增补 | template | PLANNED | 根据实际使用删减冗余字段、补充缺失模板 |
| 多编排者并发协调协议 | workflow | DONE | 已落地 `concurrency.md`、WORKBOARD、lease、scope/base revision、冲突与集成门禁；后续用 GraphX 多入口实践校准 lease 时长 |
| 最低充分秩序哲学与审视准则 | workflow | DONE | 已落地 `team/philosophy.md`，后续团队建议必须说明风险、成本、轻量替代和删除条件 |

## 中期（引入协同工具，协议 v2）

| 项 | 类型 | 状态 | 说明 |
|----|------|------|------|
| 引入 YApi 管理接口 | protocol | PLANNED | 见 `protocols/v2-tools.md`；接口 >10 个或多前端消费时启动 |
| 引入 Jira 跟踪任务/缺陷 | protocol | PLANNED | 见 `protocols/v2-tools.md`；多项目并行、需看板时启动 |
| 协议 v2 试运行并切换 | protocol | PLANNED | 按 v2-tools.md 的升级检查清单执行 |

## 远期（规模化与自动化）

| 项 | 类型 | 状态 | 说明 |
|----|------|------|------|
| 角色细分（如拆出 DBA / 安全 / 数据） | role | PLANNED | 当某角色职责过重或项目需要专项能力时 |
| 编排自动化（解析 team.yaml 驱动） | other | IN_PROGRESS | 已有 manifest/schema/校验器；自动派活仍需显式授权模型与持久 lease 实现，不能仅凭 YAML 自治 |
| 团队知识库（跨项目经验沉淀） | other | PLANNED | 把多项目复盘中反复出现的经验提炼为团队级知识 |

## 演进原则
1. **小步快跑**：一次只改一处，验证后再改下一处。
2. **可回退**：协议/流程变更保留旧版本，能降级。
3. **复盘驱动**：没有复盘依据的"我觉得应该改"不进入 roadmap。
4. **记录结构性决定**：团队能力变更进 CHANGELOG；不保存没有长期价值的过程噪声。
