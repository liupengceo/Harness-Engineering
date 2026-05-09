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

## 7. 机器化守卫 · Pre-commit hooks

> 把可机械化的 steering 做成 hook,是对抗老化的第一线——hook 在模型进化前后**一致生效**,不会被新 agent 的"新解读"拐走。

当前本仓库安装的 hooks(定义在 `.pre-commit-config.yaml`):

| hook | 出处 steering | 严重性 |
|---|---|---|
| `trailing-whitespace` / `end-of-file-fixer` / `mixed-line-ending` | `code-style.md` | 非致命(自动修) |
| `check-merge-conflict` | `git-workflow.md § 7` | 致命 |
| `check-added-large-files` (>512KB) | `code-style.md § 6 依赖管理` | 致命 |
| `detect-private-key` / `gitleaks` | `security.md § 5 密钥管理` | 致命 |
| `no-commit-to-branch main/master` | `git-workflow.md § 1` | 致命 |
| `markdownlint` | `docs.md` | 致命 |
| `yamllint` | `code-style.md` / `docs.md` | 致命 |
| `shellcheck` | `code-style.md` / `security.md § 3` | 致命 |
| `harness-steering-format` | `.kiro/steering/README.md` | 致命 |
| `harness-todo-format` | `code-style.md § 8` | 致命 |
| `harness-commit-msg` | `git-workflow.md § 2` | 致命 |
| `harness-deprecation-link` | `harness.md R3` + 本文件 | **advisory** |

**放宽的原因记录**:

- `MD013`(行长)在 `.markdownlint.yaml` 被关闭——本仓库长链接大量出现,硬 wrap 反而损害 diff 可读性。将来若有工具能智能 wrap,可回开。
- `detect-secrets` 未启用,由 gitleaks 覆盖(单一密钥扫描工具,减少噪音)。
- `harness-deprecation-link` 为 advisory 而非 blocking——打字错误修复会被误伤。若社区忘写频繁,可升级为 blocking + 在本文件新登记一条"已收紧"。

---

## 8. 维护者

- 本台账的 steward:`@repo-owner`(请替换为实际 owner)。
- Steward 不负责写每一条,但负责:
  - 复审节奏
  - 审查 `harness-change` PR 时检查是否登记
  - 每季度 reporting:多少 Active / 多少 Retired / 模型升级后删了哪些
