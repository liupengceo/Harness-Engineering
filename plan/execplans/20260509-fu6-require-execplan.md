# ExecPlan · FU-6 · ci(require-execplan)

- **任务 ID**:FU-6 (self-review P1 #5)
- **分类**:`ci` + `harness-change`
- **规模**:S
- **base**:`harness-engineering-setup-v2`
- **版本**:v1

## 1. 目标

用 CI 机械地执行 `AGENTS.md § 3.1` 的 **"任何触及代码的任务必须先出 ExecPlan"** 规定:PR 如果改了生产代码但**没有** ExecPlan(既不在 `plan/execplans/` 新增,也不在 PR 描述中包含 ExecPlan block),则标红。

## 2. 动机

`AGENTS.md` 说 "没 ExecPlan 的 PR 一律不合",但此前没有自动化。结果:**我自己开的 PR #1–#4 都是违反的**(self-review P0 #1)。没有机械检查,规则会**继续**被绕过。

## 3. 非目标

- 不强制所有 PR 都要 plan(small 模板明确接受 micro-plan 在 commit body)。
- 不检查 plan 的**质量**(太主观)。
- 不阻断 merge(只 flag,人类决定)——FU-7 可能会把它升级。

## 4. 影响面

| 路径 | 动作 |
|---|---|
| `.github/workflows/require-execplan.yml` | 新增 |
| `scripts/check_pr_has_execplan.py` | 新增 |
| `.kiro/steering/DEPRECATION.md § 9` | 登记 |

## 5. 方案

### 5.1 策略

检查以下条件,**任一满足**即通过:

1. 本 PR 的 diff 中新增了至少一个 `plan/execplans/*.md` 文件。
2. PR body 中包含一段以 `<!-- ExecPlan -->` 或 `## ExecPlan` 或 `## 执行计划` 标记的 block。
3. PR body 中引用了 `plan/execplans/` 路径(作为"我用了已有的 plan")。
4. **豁免分类**:PR 属于 `docs` / `chore(typo|deps|readme)` / `ci` 类型,通过 commit subject 或 label 识别。
5. **规模豁免**:diff ≤ 10 行(typo / 1 行 fix)。

### 5.2 识别 "触及代码" 的方式

"生产代码"定义为:`src/` / `lib/` / `pkg/` / 任何 `*.py` `*.ts` `*.js` `*.go` `*.rs` `*.java` `*.rb` `*.rb` `*.c` `*.cpp` 等。

**排除**:`plan/` `docs/` `.github/` `.kiro/` `templates/` `tests/` 下的改动,它们有自己的 ExecPlan 判断(harness-change 走独立 gate)。

对当前仓库:生产代码目录**还不存在**。本 workflow 现阶段仅给 warning + 准备好未来;一旦第一个业务代码目录出现,它自动生效。

### 5.3 Workflow 设计

- Event:`pull_request`,`types: [opened, synchronize, edited, reopened, labeled, unlabeled]`
- Jobs:
  - `check` · 跑 `scripts/check_pr_has_execplan.py`,以 PR body + changed files 为输入
  - 失败时在 PR 留 sticky comment
- 不阻断 merge(只是一个 status check);由 branch protection 决定是否必须绿

## 6. 步骤

- [ ] S1 · 写 `scripts/check_pr_has_execplan.py`
- [ ] S2 · 写 `.github/workflows/require-execplan.yml`
- [ ] S3 · 本地用 stub 测试 3 场景(有 plan file / PR body 含 block / typo 豁免)
- [ ] S4 · DEPRECATION.md § 9 登记

## 7. 验收

- [ ] `check_pr_has_execplan.py` 对 3 种输入给出正确决策
- [ ] Workflow YAML `yamllint` 通过
- [ ] 描述清楚"豁免规则"以免新人误判

## 8-15

简化,参照 FU-5。
