---
name: Task · 交给 agent / 自己的具体任务
about: 用这个模板开任何需要 agent 执行的任务;Plan checkpoint 的上游物
title: "[Task] <一句话目标>"
labels: ["task"]
---

<!--
使用说明:
- 本模板用来写"agent 接到就能开始"的任务 issue。
- 不要用它来讨论想法(那用 Discussion)或报 bug(用 bug_report)。
- 填好这份 issue 后,agent 才能用 `/plan <issue>` 产出 ExecPlan。
-->

## 1. 目标(Goal)

一句话,面向用户 / 系统 / agent,描述**要达到什么状态**(不是怎么做)。

## 2. 背景 / 动机(Context)

- 为什么现在做?
- 这事情之前在哪里讨论过?(链接)
- 相关 incident / user feedback / metric 变化?

## 3. 验收标准(Acceptance Criteria)

> 没有 acceptance 的 issue,agent 会退回来要。请把"怎么算做完"写到**可机器验证**的程度。

- [ ] 当 <输入>,<系统>会 <行为>,且 <指标>
- [ ] 回归测试覆盖 <场景 1/2/3>
- [ ] <其他可验证项>

## 4. 非目标(Non-goals)

避免 scope creep。

- 不做 <X>
- 不改 <Y>

## 5. 已知约束 / 提示(Hints)

- 相关文件 / 模块:
- 相关历史 PR / ADR:
- 参考实现:
- 禁止的方向:

## 6. 规模估计

- [ ] XS (< 1h)
- [ ] S (半天)
- [ ] M (1~2 天)
- [ ] L (3~5 天)
- [ ] XL (长任务,必须走 `plan/` 三件套)

## 7. 分类 & Persona

- 分类:`[feature | fix | refactor | perf | chore | harness-change | docs | security]`
- 需要触发的 review persona(至少 2 个):
  - [ ] security / testing / api-design / performance / observability / docs / harness-steward

## 8. 长任务?

- [ ] 是长任务 → 创建或更新 `plan/PROGRESS.md`,并在第一次 session 后写 `plan/HANDOFF.md`。

## 9. 自检(由 issue 发起人勾选)

- [ ] 本 issue 有机器可验证的 acceptance
- [ ] 本 issue 明确了**非目标**
- [ ] 本 issue 列出了相关文件 / 历史
- [ ] 本 issue 估计了规模与 persona

<!--
Agent 在看到本 issue 时的动作:
1. 读完这份 issue
2. 读 /AGENTS.md 和相关 steering
3. 产出 templates/ExecPlan.md 的填好版本
4. 停在 plan checkpoint 等待人类 OK
-->
