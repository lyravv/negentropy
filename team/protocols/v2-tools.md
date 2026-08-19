# 协作协议 v2 · 工具增强（规划中）

> **版本**：v2-tools　**状态**：PLANNED（未生效）
> 本协议描述团队从"纯文档"升级到"文档 + 协同工具"的路线。
> **核心不变**：git 里的 Markdown 仍是单一事实源；工具是**投影/加速器**，不是新的事实源。

## 设计原则

1. **文档为主，工具为投影**：yapi/jira 里的内容必须能追溯到 git 文档；工具里产生的新信息要回写文档。
2. **渐进引入**：一次只加一个工具，验证稳定后再加下一个。
3. **可降级**：任何工具不可用时，团队必须能退回 v1-docs 继续工作。

## 规划引入的工具

### 1. YApi（接口协作）
- **用途**：`api-spec.md` 的在线投影，支持接口调试、Mock、团队协作。
- **映射**：
  - `03-architecture/api-spec.md`（git，事实源） ⇄ YApi 项目（在线，可调试）
  - architect 在 git 改完 `api-spec.md` 后，同步到 YApi；YApi 的变更请求要回写 git。
- **引入时机**：当接口数量多到纯文档难以调试时（经验值：> 10 个接口，或多前端消费同一 API）。

### 2. Jira（任务与缺陷跟踪）
- **用途**：用户故事、任务、缺陷的状态跟踪与看板。
- **映射**：
  - `02-requirements/user-stories/US-*.md`（git，事实源） ⇄ Jira Epic/Story
  - `05-testing/defect-log.md`（git，事实源） ⇄ Jira Issue（Bug）
  - 编号对齐：Jira key 与 `US-xxx` / `Q-xxx` / 缺陷编号互相引用。
- **引入时机**：当并行项目多、需要跨人看板与历史追溯时。

## 升级检查清单

- [ ] 选定工具并完成配置（项目/空间/权限）
- [ ] 定义 git ⇄ 工具的双向同步规则（谁触发、何时同步、冲突以谁为准）
- [ ] 更新受影响角色的 `AGENT.md`（增加"工具操作"小节）
- [ ] 更新 `team/templates/`（文档头部增加工具链接字段）
- [ ] 用一个真实项目试运行
- [ ] 把本协议状态改为 `ACTIVE`，`v1-docs.md` 改为 `SUPERSEDED`
- [ ] 更新 `protocols/CURRENT.md` 指针
- [ ] 记入 `evolution/CHANGELOG.md`

## 与 v1 的关系

v2 **不替换** v1 的文档规范（头部、handoff note、open-questions、状态标记、变更流程全部沿用），
只是在其上**叠加**工具投影层。因此 v1 的所有约定在 v2 下依然有效。
