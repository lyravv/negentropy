---
title: 实现说明（前端/后端通用）
role: frontend-engineer | backend-engineer
status: DRAFT
version: 0.1
updated: YYYY-MM-DD
upstream: [03-architecture/architecture.md, 03-architecture/api-spec.md, 03-architecture/data-model.md]
downstream: [test-engineer, devops-engineer]
---

# 实现说明

## 交接说明
- **给谁**：test-engineer / devops-engineer
- **一句话**：<实现了什么，怎么跑起来>
- **关键决策**：<实现层面的关键选择>
- **需要下游注意**：<怎么启动、依赖、已知限制>
- **未决问题**：无 / Q-xxx

## 1. 实现范围
<对应哪些用户故事/接口>

## 2. 代码结构
<目录结构、关键模块说明>

## 3. 如何运行
<依赖安装、启动命令、环境变量、数据库初始化>

```bash
# 示例
```

## 4. 契约偏离记录
> 若实现与 api-spec / data-model 有出入，必须在此记录并说明原因（应已走变更流程）。

| 位置 | 契约原文 | 实际实现 | 原因 | 是否已同步契约 |
|------|---------|---------|------|--------------|

## 5. 自测情况
<自己做了哪些验证>

## 6. 已知限制 / 遗留问题
<没做完的、临时方案、技术债>
