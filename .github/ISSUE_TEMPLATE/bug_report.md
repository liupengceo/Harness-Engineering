---
name: Bug report · 报告一个 bug
about: 说清楚"期望行为"与"实际行为",方便 agent 一次做对
title: "[Bug] <一句话现象>"
labels: ["bug"]
---

## 1. 现象(What happened)

清晰描述你看到了什么。截图 / 日志片段 / 报错堆栈都欢迎。

## 2. 期望(What you expected)

## 3. 复现步骤

1.
2.
3.

## 4. 环境

- 版本 / commit SHA:
- 浏览器 / OS / 运行时:
- 配置 / feature flag 状态:

## 5. 严重性

- [ ] P0 · 生产宕机 / 数据损坏 / 安全
- [ ] P1 · 核心路径出错,影响一部分用户
- [ ] P2 · 边缘路径 / 可绕开
- [ ] P3 · 小瑕疵 / 打磨

## 6. 是否触发 security 红线?

- [ ] 是 · 看 `.kiro/steering/security.md` § 1,请立即 assign 给 on-call。
- [ ] 否

## 7. 提示 / 已调查(Optional)

- 可能的原因:
- 已经看过的文件 / 日志:
- 相关 issue / PR:

## 8. 希望怎么修?

- [ ] 只要修复本次现象
- [ ] 希望同时修 harness(让这类 bug 不再发生)
- [ ] 其他:

<!--
Agent 看到 bug issue 时的默认动作:
1. 先写一条能稳定复现该 bug 的失败测试(对应 testing.md § 3 "先复现,再修")
2. 产出 ExecPlan
3. Plan checkpoint 后修复
4. 如果是"第二次出现的同类 bug",同步提议 harness 改动(独立 PR)
-->
