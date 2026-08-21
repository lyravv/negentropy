# 编排指南（Orchestration）

编排者是 control plane，不是全领域批准者。先遵循 `philosophy.md` 的最低充分秩序；完整职责见 `roles/orchestrator/AGENT.md`，权限见 `governance.md`，并发见 `concurrency.md`。

## 接手顺序

1. 读项目 `STATE.md`，确认 profile、权威来源、revision、下一步和基线。
2. 读 `WORKBOARD.md`，识别活动 lease、冲突范围和可认领项。
3. 读团队哲学、当前协议、治理、并发规则和项目代码仓 `AGENTS.md`。
4. 检查所有相关仓库 worktree；保留已有修改。
5. 运行团队校验；再按项目风险决定是否运行基线测试。
6. 写任务先认领，读任务可直接执行；按角色章程派活。

## 标准派活 Prompt

```text
【角色】negentropy/<role-id>；完整阅读该角色 AGENT.md、skills.md 与当前协议。
【项目】<workspace>；profile=<profile>；STATE/WORKBOARD=<paths>。
【授权】action_mode=<mode>；授权来源=<user request/project policy>。
【基线】base_revision=<sha|WORKTREE>；当前 worktree=<clean|列出需保护的修改>。
【输入】只列权威输入及精确 revision；说明哪些阶段由 existing spec 替代。
【任务】一个可验收目标。
【范围】允许写入文件/目录；明确禁止范围；与其他工作项的依赖。
【产出】目标文件、状态、审批者、交接字段。
【验证】必须运行的 scoped 命令；全量命令由集成者运行。
【完成】更新工作项结果；报告 revision/WORKTREE、验证、风险；不默认 commit/push/deploy。
```

## 编排循环

1. **分类**：确定 action mode 和 workflow profile。
2. **盘点**：读取权威事实、检查 worktree 和活动任务。
3. **拆分**：按契约和文件所有权拆成无重叠工作项，写依赖图。
4. **认领**：记录 owner、base、scope、lease、验收；然后启动角色。
5. **评审**：内容由治理矩阵中的 reviewer/approver 处理；orchestrator 检查证据。
6. **集成**：核对 revision，运行 scoped + baseline 验证，处理冲突。
7. **交接**：更新 WORKBOARD 与 STATE；只有 publish 授权才执行外部副作用。

## 并行判定

满足以下全部条件才并行：写入集合不重叠；没有未决契约；共享输入 revision 相同；任务间无产出依赖；集成责任人明确。否则串行。首次实现与后续修复都遵循同一规则，不能仅因角色不同就假定安全。

## 评审门禁

- frontmatter 与状态类型正确；
- approver 符合治理矩阵且 evidence 可追溯；
- source revision 与实际工作一致；
- DoR/DoD、契约覆盖和未决项完整；
- 不越权、不覆盖用户修改、不扩大外部副作用；
- 测试结论对应被测 revision，而非旧报告数字。

## 兼任角色

无法或无需启动独立角色时，主 agent 可以兼任，但 WORKBOARD 的 owner 写 `orchestrator as <role>`，审批仍遵循职责分离；高风险变更不能由同一身份同时作者、唯一 reviewer 和业务/发布批准者。
