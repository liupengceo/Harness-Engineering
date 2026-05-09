---
title: Harness 退役台账
inclusion: manual
---

# Harness 退役台账(Deprecation Ledger)

> 这是本仓库**对抗 harness 老化**的中央台账。
>
> 每条 harness 约束——不管是一条工具、一条 steering 条目、一条 CI 规则、一条 review persona 规则,**只要它是为了应对当前模型的某种失败模式,都必须登记在这里**。
>
> **没登记 = 默认永久。** 永久的东西会在几代模型之后变成负担。
> 登记 = 给它一个"退役条件",让未来的 agent / 工程师有机会干净利落地拆掉它。

---

## 1. 使用方式

### 新增一条

当你(或 agent)在 `AGENTS.md` / `.kiro/steering/*.md` / 工具注册表 / CI 里**加了一条新约束**,且这条约束的动机是:

- 对抗某个模型版本的具体失败模式(比如"模型会幻觉 API 签名,所以强制 schema")
- 临时压制某类输出偏差
- 对某个当前暴露的 bug 做 guardrail

→ **必须**在本文件下方追加一条登记,格式见 § 3。

### 不需要登记的情况

以下**不必**登记(它们是永久性工程实践):

- 通用最佳实践(TDD、SemVer、SOLID……)
- 安全红线(`security.md` 里的 § 1)
- 格式 / 命名 / 语言社区惯例
- 本仓库的根本性架构决策(这种走 ADR)

### 复审节奏

- **每季度**一次整体复审(由 harness steward / on-call / staff eng 主持)。
- 模型版本大升级后一周内,额外**临时复审**一次。

---

## 2. 复审流程

对每条登记项,问 5 个问题:

1. 触发这条规则的失败模式,在当前模型下**还会发生吗**?
2. 有没有**更宽松**的写法能达成同样效果?
3. 删掉它会造成什么**新的失败**?有可量化的信号吗(CI 数据、incident 数、review 打回率)?
4. 如果保留,**收紧**或**扩展**它有没有价值?
5. 如果替代它,替代方案是什么?

如果答案是"不需要了"→ 发 `harness-change` PR 删除,同时在本文件把对应条目改为 `状态: Retired`,**不删除历史记录**(留下学习价值)。

---

## 3. 登记条目格式

```markdown
### <序号>. <一句话标题>

- **状态**:Active | Retired | Escalated(更严了)| Widened(放宽了)
- **登记日期**:YYYY-MM-DD
- **登记人**:@someone(可以是 agent + 复核人)
- **约束位置**:
  - [ ] `AGENTS.md` § ?
  - [ ] `.kiro/steering/<file>.md` § ?
  - [ ] 工具注册表(具体工具名)
  - [ ] CI (`.github/workflows/<file>.yml` step 名)
  - [ ] 其他(具体)

- **约束内容**(原文引用或扼要):
  > (例:禁止 agent 使用 `any`,强制 `unknown as X` + 守卫)

- **针对的模型 / 版本 / 现象**:
  - 模型: `gpt-5-codex-max` / `claude-opus-4.6` / ...
  - 现象: (例:在 TS 项目里频繁用 `any` 逃避类型错误,导致 review 被反复打回)
  - 可量化信号: (例:2026 年 4 月有 23% 的 PR 因为 `any` 被 review flag)

- **触发复审的信号**:
  - (例:连续 2 个月相关 review flag 率 < 5% → 复审放宽的可行性)
  - (例:模型升级到 `gpt-6` 且官方 release note 说明已解决类型逃避 → 立刻复审)

- **首次复审时间**:YYYY-MM-DD

- **注释 / 历史**:
  - YYYY-MM-DD · (复审结果 / 状态变化 / 背景补充)
```

---

## 4. 登记示例(模板已填,方便抄)

> 下面是示例条目——本仓库现在并没有真的加这些约束。**上线真实条目时请删除示例**或改为 `状态: Retired - example`。

### 0. [示例] 禁用 `any`,要求 `unknown as X` + 守卫

- **状态**:Active (示例)
- **登记日期**:2026-05-09
- **登记人**:@repo-owner + codex
- **约束位置**:
  - [x] `.kiro/steering/code-style.md` § 10 · TypeScript / JavaScript
- **约束内容**:
  > 在 TS / JS 代码中禁用 `any`;需要时用 `unknown` 并在边界做类型守卫。
- **针对的模型 / 版本 / 现象**:
  - 模型:`gpt-5-codex-max`、`claude-opus-4.6`
  - 现象:这一代模型在面对复杂泛型时有时会用 `any` 逃避,导致接口被悄悄弱化。
  - 可量化信号:review flag 样本、PR 打回率。
- **触发复审的信号**:
  - 当某个模型版本连续 30 天的相关 flag 率 < 5%,复审是否可以改回 "warn" 级别。
  - 或者:引入更强的类型推断插件后复审。
- **首次复审时间**:2026-08-09
- **注释 / 历史**:
  - 2026-05-09 · 初始登记,示例用途。

---

### 1. [示例] 强制"先 ExecPlan 再写代码"

- **状态**:Active (示例)
- **登记日期**:2026-05-09
- **登记人**:@repo-owner
- **约束位置**:
  - [x] `AGENTS.md` § 3.1
  - [x] `.kiro/steering/harness.md` § 2 R1
- **约束内容**:
  > 任何触及代码的任务必须先出 ExecPlan,plan 放入 PR 第一个 commit。
- **针对的模型 / 版本 / 现象**:
  - 模型:普适。
  - 现象:这一代 agent 在没有 plan 时倾向直接动手,导致后期 review 成本高。
  - 可量化信号:review round 次数。
- **触发复审的信号**:
  - **永久性**:这是我们对 harness 的根本约束之一,不预期退役。但每年评估一次"能否放松到'只对 ≥ X 行改动强制'"。
- **首次复审时间**:2027-05-09
- **注释 / 历史**:
  - 2026-05-09 · 初始登记。

---

### 2. [示例] 工具集默认 4 件套

- **状态**:Active (示例)
- **登记日期**:2026-05-09
- **登记人**:@repo-owner
- **约束位置**:
  - [x] `AGENTS.md` § 4.1
  - [x] `.kiro/steering/harness.md` § 2 R4
- **约束内容**:
  > 默认工具集:`bash` / 文件读写 / `grep` / `run_tests`。其他工具需要 PR 审批。
- **针对的模型 / 版本 / 现象**:
  - 现象:工具过多 → 约束悖论,agent 更易分心 + token 浪费。
- **触发复审的信号**:
  - 季度复审"是否有 3 个及以上任务因为缺工具反复失败",如有则讨论增加具体工具。
- **首次复审时间**:2026-08-09
- **注释 / 历史**:
  - 2026-05-09 · 初始登记。

---

## 5. 已退役条目(Retired)

> 留痕用。退役不删历史。

(暂无)

---

## 6. 放宽 / 收紧记录(Widened / Escalated)

> 约束变更的关键节点记录。

(暂无)

---

## 7. Review Persona 自动调度

> 2026-05-09 新增。

本仓库在 `.github/workflows/review.yml` 部署了一个 **persona 自动调度工作流**:

- `scripts/select_personas.py` 根据 PR diff 与 labels,依 `templates/review-personas/README.md § 7` 选出要跑的 persona。
- `scripts/run_review_persona.sh` 是 **agent 平台适配器**,默认 `REVIEW_RUNNER=abstain`(占位),可在 fork 里切成 `codex` / `claude-code` / `custom`。
- `scripts/aggregate_reviews.py` 聚合多个 persona 的 YAML 输出,产出一份 markdown 贴到 PR 评论。
- 工作流**不阻塞** PR;阻塞性由 required status checks 控制。

### 退役条件 / 演化

| 组件 | 当前状态 | 可放宽 | 可收紧 |
|---|---|---|---|
| `scripts/select_personas.py` 的规则表 | 与 `templates/review-personas/README.md § 7` **严格同步** | 改文档 → 改脚本(同 PR) | N/A |
| `abstain` 默认 runner | 允许裸仓库跑通 | 长期保留(为 fork 友好) | 组织内部仓库可改默认 |
| 聚合评论是 `sticky` | 避免评论风暴 | 长期保留 | N/A |
| 自动请求 changes | **未启用** | N/A | 若 persona 输出稳定度高(连续 30 天无 false positive >1/wk),可启用 auto request-changes |

### 复审触发

- 每季度:看 PR 作者是否因 persona 噪音而忽略评论;如是 → 削减 persona。
- 模型大升级后:看是否需要重跑过去 N 个 PR 做校准。

### FU-2 变更记录(2026-05-09)

| 项目 | 从 | 到 | 退役条件 |
|---|---|---|---|
| `REVIEW_RUNNER=abstain` 的默认 verdict | `approve`(误导) | `abstain`(语义独立) | 永久保留;这是对"bot 绿 = 万事大吉"的根本纠正 |
| `abstain` 在 rollup 中的行为 | (不存在) | **跳过**;全 abstain 时顶层 verdict = `abstain` | 永久 |
| aggregate 顶部的 abstain 横幅 | (不存在) | 全 abstain 时强横幅;部分 abstain 时软横幅 | 永久 |
| `scripts/validate_persona_output.py` | (不存在) | 强制 raw YAML / 必需字段 / verdict enum | 长期;当所有 adapter 稳定产出合规 YAML 超过 90 天,可考虑降级为 warning |

**为何永久**:这些改动不是对抗某个模型版本的缺陷,而是对"评审 bot 语义"的一个根本性澄清。不在 model-upgrade 后退役。

---

## 8. Bootstrap 异常(Retired)

> 2026-05-09 登记。**状态:Retired — 已追认,仅留历史**。
>
> PR #1–#4 建立了 AGENTS.md / steering / templates / ADR-0001 本身。在它们合入之前,"任何触及代码的任务必须先出 ExecPlan" 并不可能被满足(ExecPlan 的模板在 #1 里才首次出现)。这是 bootstrap 阶段的鸡生蛋,属于 `AGENTS.md § 3.1` 与 `.kiro/steering/harness.md § 2 R1` 的**一次性例外**。
>
> 从本 session(#5 meta PR)起,所有 PR 必须遵守 ExecPlan 先行规则。未来**不得**再以 bootstrap 为由豁免。
>
> 留此条目是为了避免未来的人在历史里"发现"这 4 个 PR 没 ExecPlan 而误以为"规矩本来就可以绕"。

---

## 9. 维护者

- 本台账的 steward:`@repo-owner`(请替换为实际 owner)。
- Steward 不负责写每一条,但负责:
  - 复审节奏
  - 审查 `harness-change` PR 时检查是否登记
  - 每季度 reporting:多少 Active / 多少 Retired / 模型升级后删了哪些
