# Architecture Decision Records (ADR)

> 本目录收录本仓库的**长期架构/技术决策**。每个 ADR 记录一个**一次性成形、日后可能被替代**的选择,以及它的上下文、取舍、后果与退役条件。

## 文件命名

```
NNNN-short-title.md
```

- `NNNN` — 单调递增的 4 位数字编号,不重用。
- `short-title` — 英文 / 中文皆可;以可搜索、可 grep 为原则。

## 格式

严格按 `.kiro/steering/docs.md § 3` 的 7 字段模板:

1. **状态**(Proposed / Accepted / Superseded by … / Deprecated)
2. **日期**
3. **作者**
4. **上下文**
5. **决策**
6. **候选方案**
7. **取舍理由**
8. **后果**(正向、负向、监控信号)
9. **退役条件**

## 索引

| # | 标题 | 状态 | 日期 |
|---|---|---|---|
| [0001](./0001-adopt-harness-engineering-starter-kit.md) | Adopt Harness Engineering starter kit | Accepted | 2026-05-09 |

## 什么时候必须写 ADR

见 `.kiro/steering/docs.md § 2`。粗略地:

- 改变**架构 / 模块边界 / 依赖关系**。
- 做出**长期影响**的技术选型(数据库、消息、协议、框架)。
- 改变**跨团队契约**(事件 schema、错误模型、版本化策略)。
- **引入或移除**一整套工程方法论(本 ADR-0001 就是典型例子)。

不需要 ADR:

- 单个 bug fix。
- 局部重命名 / 重构。
- 配置调参。
- UI / 文案。

## 何时更新状态

- 一个 ADR 被**后续 ADR 替代**时,改其状态为 `Superseded by ADR-XXXX`,**不要删除**。
- 不再适用时改为 `Deprecated`,并标注"从哪天起不再生效"。
- 永远保留历史。ADR 的价值在"决策链"。
