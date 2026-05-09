<!--
PR 模板(本仓库)
================

- 本模板适用于**所有 PR**。Draft PR 也请尽量填,写得越早,人类 plan checkpoint 越有用。
- 不适用的字段写 `N/A`,**不要整段删除**——保留空字段让 reviewer 一眼看到这项"被考虑过"。
- 相关文件:
  - /AGENTS.md
  - .kiro/steering/git-workflow.md
  - templates/ExecPlan.md
-->

## 概要 / What & Why

<!-- 一两句话概括:这个 PR 做了什么?为什么要现在做? -->

## 类型

- [ ] feat · 新功能
- [ ] fix · bug 修复
- [ ] refactor · 等价重构
- [ ] perf · 性能
- [ ] docs · 文档
- [ ] test · 测试
- [ ] chore / build / ci · 工程杂项
- [ ] **harness-change** · 修改 `AGENTS.md` / `.kiro/steering/` / 工具注册表 / agent 约束
- [ ] security · 安全相关(触发 `security` persona 强制 review)

## 关联

- Issue:`Closes #___` / `Refs #___`
- ExecPlan:`plan/execplans/<date>-<slug>.md` 或**在本 PR 第一个 commit 中**
- 相关 ADR:`docs/adr/NNNN-...md`(如适用)
- 前置 / 后续 PR:`#___`

## 影响面 / Impact Map

<!--
粗粒度列出会被触及的模块、接口、数据、用户流程。格式自由。
不写影响面的 PR 视为不合格,哪怕 diff 很小。
-->

- **模块**:
- **接口**:
- **数据 / migration**:
- **用户可见行为**:
- **Blast radius**(最坏情况影响面 + 回滚难度):

## 做了什么(How)

<!--
不必复述 diff,但要点出关键选择与非明显的取舍。
推荐格式:带项目列表,每条 1-2 行。
-->

-
-
-

## 验证 / How tested

- [ ] 本地运行了相关单元测试
- [ ] 本地运行了相关集成测试
- [ ] Lint / type-check 通过
- [ ] 新增了回归测试(命名三段式)
- [ ] 手工验证步骤(若适用):
  1.
  2.

## 回滚方案

<!--
出事怎么办?关 feature flag?revert commit?数据要不要补?
高风险 PR 必填。
-->

-

## 观测与告警

- 新增 log / metric / trace:
- 新增告警(或已有告警的调整):

## 文档更新

- [ ] README / 模块 README
- [ ] `docs/` 下相关页
- [ ] ADR(如适用)
- [ ] CHANGELOG (`Unreleased`)
- [ ] `.kiro/steering/DEPRECATION.md`(如本次涉及 harness 新增/收紧)

## Review Persona 调度

> 请**至少**勾选 2 项。对 security / api / performance 的改动,对应 persona 必选。

- [ ] `security` — 涉及 auth / 凭证 / 输入 / 权限 / 网络出入?
- [ ] `testing` — 涉及测试策略 / 覆盖 / flakiness?
- [ ] `api-design` — 涉及公开接口 / SDK / URL / 契约?
- [ ] `performance` — 涉及关键路径 / 大数据 / 锁 / IO?
- [ ] `observability` — 涉及 log / metric / trace / 告警?
- [ ] `docs` — 涉及文档、术语、API 描述?
- [ ] `harness-steward` — 涉及 `AGENTS.md` / steering / 工具注册表 / CI?

**选中的 persona 的报告**(直接贴 `/review <persona>` 的结论,或者链接):

- <persona>:...

## 自检(必填;任何一项未勾选请在下面说明)

- [ ] 我遵循了 `AGENTS.md § 3` 的流程。
- [ ] 我读过与本 PR 相关主题的 steering 文件。
- [ ] 本 PR diff ≤ 400 行(或者有合理拆分说明)。
- [ ] 本 PR 没有把 "harness 改动" 和 "业务改动" 混在一起。
- [ ] 本 PR 没有引入新 `any` / `@ts-ignore` / `# type: ignore`(如有,下述理由)。
- [ ] 本 PR 没有 `skip` / `xfail` 任何测试(如有,下述理由)。
- [ ] 本 PR 没有在日志或 commit 中引入真实 secret。
- [ ] 本 PR 没有 `--no-verify` 绕过 pre-commit。
- [ ] 本 PR 没有 force push 到保护分支。

如某项未勾选,请在这里写清楚为何:

<!-- 写在这里 -->

## Agent 备注(可选)

<!--
如果这个 PR 由 agent 执笔完成,可以在这里记下:
- 本次 agent 主要使用的工具
- 出现过的反复失败模式(考虑沉到 steering)
- 建议加入的 harness 改动(独立 PR 跟进)
-->
