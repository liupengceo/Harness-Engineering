<!--
Harness-change PR 模板
=======================

- 使用条件:本 PR 改动 `AGENTS.md` / `.kiro/steering/` / `templates/` /
  `templates/review-personas/` / `scripts/check_*` / `scripts/run_review_*` /
  `scripts/aggregate_*` / `.github/workflows/` / `.pre-commit-config.yaml` /
  工具注册表,或**定义**新的约束、persona、工具、审查规则。
- 访问方式:`?template=harness_change.md`
- 本模板比 standard.md 多两节:**为什么是 harness 改动** 与 **DEPRECATION 登记**。
- 本模板是`.kiro/steering/DEPRECATION.md` 机制的入口之一 —— 请**不要**跳过第 3、4 节。
-->

## 概要 / What & Why

<!-- 1-3 句。务必回答:这个 harness 改动**在我不做**的情况下会出什么问题? -->

## 为什么这是 Harness 改动而不是 prompt 补丁?

<!--
Harness 改动的标准(来自 .kiro/steering/harness.md R3):

  - 同一类错误出现过 **≥ 2 次**(不是第一次见到)
  - 改 prompt 无法根治 —— 需要 schema / lint / CI / 审查人设 / 工具减法
  - 影响的是**结构**,不是个别输出

如果以上不成立,应该是 bug fix 或 docs PR,不要标 harness-change。
-->

- 重复出现次数 / 证据:
- 为什么 prompt 补丁不够:
- 预期消除的失败模式:

## 类型

- [x] **harness-change**
- [ ] 同时是 `security`(触 security.md § 1)—— 必须 `security` persona + human approve
- [ ] 同时是破坏性变更(adapter / schema / workflow shape)

## 关联

- Issue: `Closes #___` / `Refs #___`
- ExecPlan: `plan/execplans/<date>-<slug>.md` 或**本 PR 第一个 commit**
- 关联 ADR: `docs/adr/NNNN-...md`(harness-change 通常**需要** ADR,除非是小调整)
- 前置 / 后续 PR:

## 影响面 / Impact Map

- **改了哪些 harness 路径**:
  - [ ] `AGENTS.md`
  - [ ] `.kiro/steering/<file>`
  - [ ] `templates/<file>`
  - [ ] `templates/review-personas/<file>`
  - [ ] `scripts/<file>`
  - [ ] `.github/workflows/<file>`
  - [ ] `.pre-commit-config.yaml`
  - [ ] 工具注册表
  - [ ] 其他:
- **agent 或 contributor 的日常改变**:
- **Blast radius**(最坏情况 + 回滚难度):

## DEPRECATION 登记(**必填**)

见 `.kiro/steering/DEPRECATION.md § 3` 登记格式。

- [ ] **A · 永久性**:通用工程最佳实践 / 安全红线 / 根本性工程决策 → DEPRECATION.md **不**登记(§ 1 的豁免情况)。
- [ ] **B · 针对当前模型缺陷**:已在 `DEPRECATION.md § 7 / § 8 / § (新章节)` 登记,条目 ID / 节号:`____`
- [ ] **C · 临时收紧/放宽一条已有条目**:修改了 DEPRECATION.md 的 `§ 5` / `§ 6`,条目 ID:`____`

**如果选 B 或 C,请在此处粘贴你新增 / 修改的 DEPRECATION 条目的摘要**:

<!-- 粘贴条目摘要 -->

**退役条件 / 复审触发**(必填):

-

## 替代方案(Considered alternatives)

<!-- 至少列 1 条放弃的方案 + 放弃理由。"没考虑过"不是有效答案。 -->

- A · <方案> — 放弃理由:
- B · <方案> — 放弃理由:

## 验证 / How tested

- [ ] 本地运行了相关单元测试
- [ ] Pre-commit 本地跑通(lint / type / 自定义 hooks)
- [ ] 模拟了 harness 改动**生效后**的 3 个代表性场景(并在下方列出)
- [ ] 没造成 `scripts/check_*.py` / `scripts/validate_persona_output.py` 等已有守卫的回归

场景 1:
场景 2:
场景 3:

## 回滚方案

<!-- Harness 改动的回滚要特别小心:已合入的 PR 里可能已经依赖新行为。 -->

- Git-level revert:
- 需要反向迁移吗:
- 其他 PR 是否在依赖本改动:

## 观测与告警

- 新增 log / metric / PR 评论结构变化:
- 退役后检查的信号(如何知道这条约束不再必要?):

## 文档更新

- [ ] `AGENTS.md` 若涉及 —— 同 PR 改
- [ ] 相关 steering 文件若涉及 —— 同 PR 改
- [ ] `docs/harness-engineering/` 精读库若涉及事实变动 —— 同 PR 改
- [ ] `.kiro/steering/DEPRECATION.md` — 上面已勾选
- [ ] ADR(如涉及架构性决定)
- [ ] `CHANGELOG.md`(starter kit 发布后启用)

## Review Persona 调度

- [x] **`harness-steward`**(必选,对 harness-change PR 无例外)
- [ ] `security` — 涉及 auth / 凭证 / 输入 / 权限 / 网络出入?
- [ ] `testing` — 涉及测试策略 / flakiness / 守卫脚本?
- [ ] `api-design` — 改了接口 / schema / 契约?
- [ ] `performance` — 改了关键路径 / 工作流 concurrency?
- [ ] `observability` — 改了 log / metric / trace / 告警?
- [ ] `docs` — 改了文档基础?

**Persona 报告**(必须粘贴 harness-steward 的结论):

- `harness-steward`:
- 其他:

## 自检(全填;任何一项未勾选请解释)

- [ ] 我遵循了 `AGENTS.md § 3` 的流程
- [ ] ExecPlan 是本 PR 的**第一个 commit**
- [ ] 我读过 `.kiro/steering/harness.md` + `.kiro/steering/DEPRECATION.md` + 本次改动涉及主题的 steering 文件
- [ ] 本 PR **没有**同时包含业务改动(harness-change 必须独立)
- [ ] 本 PR **没有** `any` / `@ts-ignore` / `# type: ignore`
- [ ] 本 PR **没有** `skip` / `xfail` 测试
- [ ] 本 PR **没有** 引入 secret
- [ ] 本 PR **没有** `--no-verify`;若有,解释理由
- [ ] 本 PR **没有** force push 到保护分支
- [ ] 我已在 DEPRECATION.md 登记 / 更新了对应条目(若适用)

未勾选的解释:

<!-- 写在这里 -->

## Agent 备注

<!--
- 本 PR 主要使用的工具
- 发现的新失败模式(如果这本身是反思触发的)
- 对**后续** harness 改动的建议
-->
