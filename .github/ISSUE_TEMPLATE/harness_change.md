---
name: Harness Change · 改 AGENTS.md / steering / 工具 / CI
about: 提议一次"对 agent 的约束系统"的修改;独立于业务 PR
title: "[Harness] <一句话改动>"
labels: ["harness-change"]
---

<!--
用这个 issue 来提议修改:
- /AGENTS.md
- .kiro/steering/*.md
- 工具注册表
- CI 规则(本仓库 .github/workflows/)
- PR / issue / plan 模板

业务代码改动不要用这个模板。
-->

## 1. 要改的位置

- [ ] `AGENTS.md` § <section>
- [ ] `.kiro/steering/<file>.md` § <section>
- [ ] 工具注册表(工具名:<name>)
- [ ] CI(`.github/workflows/<file>.yml`)
- [ ] 模板(`templates/<...>` / `.github/<...>`)

## 2. 现状与问题

描述:
- 当前的规则是什么?
- 反复出现的痛点是什么?
- 这个痛点出现过几次?影响了多少任务?
- 有没有量化信号(review flag 率 / CI 失败率 / incident 次数)?

> **只出现过一次的偶发问题,不应该成为 harness 改动。**

## 3. 提议的改动

- 新增 / 删除 / 收紧 / 放宽 的内容(原文粘贴 + 建议的版本)。
- 是否与已有 steering 条目冲突?

## 4. 替代方案

至少讨论 1 个放弃的方案,以及为什么放弃。

## 5. 退役条件(Deprecation Criteria)

> 填这一项是为了**对抗 harness 老化**。不填 = 默认永久。

- [ ] 本条**长期有效**(永久性工程原则,不针对任何特定模型)
- [ ] 针对当前模型的临时补丁:
  - 针对模型版本:
  - 退役条件:(例:升级到 XXX 且连续 30 天相关 flag 率 < 5%)
  - 首次复审时间:YYYY-MM-DD

对应的 `.kiro/steering/DEPRECATION.md` 登记条目会在 PR 中同时添加 / 修改。

## 6. 风险与反向影响

- 这次改动会让哪类任务**变难**?
- 是否有可能把一个真实 bug 归咎于新规则?
- 回滚这次 harness 改动的步骤?

## 7. Review Persona 调度

- [ ] `harness-steward`(必选)
- [ ] `security`(如涉及权限/工具/网络)
- [ ] `docs`(如涉及模板)

## 8. 自检

- [ ] 我至少用过 / 见过**两次**这类痛点才提议。
- [ ] 我读过 `.kiro/steering/DEPRECATION.md` 的使用说明。
- [ ] 我准备把这次改动**独立**成 PR,不混业务代码。
