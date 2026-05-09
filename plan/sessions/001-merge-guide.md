# Session 001 · Merge Guide for PR #1–#11

> **用途**:一份给 human reviewer(即你)的 runbook。11 个 open PR 的 merge 顺序、每个 PR 的 review 重点、预期的 CI 行为、rollback 代价。
>
> **为什么存在这份文档**:这份 guide 代替了"知识只活在对话历史里"这种不可持续的状态。任何人(或 agent)在后续 session 合这批 PR 时都可以直接按表走。参见 `.kiro/steering/harness.md` R2 · repo-as-source-of-truth。
>
> **不是权威判断**:每个 PR 的最终 approve/merge 是你的决定。这份 guide 只告诉你**我对这个 PR 的心理模型**,以便你的 review 更快地聚焦在关键差异上。

---

## 0. TL;DR 时间预算

- **分 3 批合**。每批之间停一下看 CI 行为。
- 总时间预估:2–3 小时(含 review + 观察 CI)。
- **关键决策点只有 1 个**:合 #3 之后,去 GitHub 把 #6 的 base 从 `ci/review-personas-workflow` 改成 `main`(GitHub PR 页面 Edit → base branch)。

---

## 1. 依赖图(合成 DAG)

```
                            main
                             │
                             ▼
                   ┌─────────┴─────────┐
                   │     Batch A       │
                   │  (Foundation)     │
                   │   #1, #5          │
                   └─────────┬─────────┘
                             ▼
     ┌───────────────────────┼─────────────────────────┐
     │       Batch B         │      Batch C            │
     │  (Infrastructure,     │  (Harness pipes,        │
     │   any order)          │   串行)                  │
     │  #2, #4, #7           │  #3 → #6                │
     └───────────────────────┴──────────────────┬──────┘
                                                │
                                                ▼
                           ┌─────────────────────────────┐
                           │         Batch D             │
                           │     (Governance,            │
                           │    合 Batch B/C 后进行)      │
                           │  #8, #9, #10, #11           │
                           └─────────────────────────────┘
```

---

## 2. Batch A · Foundation(先合这两个)

### PR #1 · harness-engineering-setup-v2 → main

- **尺寸**:~5000 行(超出 `git-workflow.md § 4.1` 的 400 行硬规定,属于 **bootstrap 豁免**,已在 DEPRECATION.md § 8 登记)
- **review 重点**:
  - 目录结构是否合理(`AGENTS.md`、`.kiro/steering/`、`templates/`、`docs/harness-engineering/`、`plan/` 的拓扑)
  - 是否有任何真实 secret / 真实邮箱误入
  - `AGENTS.md § 8 安全红线` 是否足够严格
  - 你的名字 `@liupengceo` 是否应该出现在 CODEOWNERS(留给 #7 处理)
- **不要**逐字读完 —— 它太大了。重点看 4 个文件:
  - `AGENTS.md`(权威契约)
  - `.kiro/steering/harness.md`(4 条铁律)
  - `.kiro/steering/security.md § 1`(红线)
  - `templates/ExecPlan.md`(模板)
- **合后 CI 行为**:没有 workflow 会跑(CI 文件还在 #2 里)。
- **Rollback 代价**:**不可能** —— 合掉就是 main。所以 review 要做对一次。
- **建议动作**:approve & squash merge。确保 merge commit message 清晰(GitHub 会用 PR title,已经是 "Install Harness Engineering starter kit")。

---

### PR #5 · docs/plan-self-review-001 → main

- **尺寸**:~900 行(包括本 guide,因为是我追加的那个 commit)
- **review 重点**:
  - `plan/execplans/20260509-self-review-remediation.md` § 12 的 3 个 Open questions(Q1 bootstrap 异常 / Q2 base 策略 / Q3 双语放宽)—— 你现在应该**显式回答**,否则 fallback 会被触发
  - `plan/sessions/001.md § 2.2` 的 24 条 self-review 问题清单 —— 这是未来 follow-up 的 backlog 锚点,value 集中在这里
  - 本 merge-guide.md(你正在读)
- **注意**:此 PR 的存在就是"我们开始认真执行 harness 的标志"。合它象征性地 retire 了 bootstrap 豁免。
- **合后 CI 行为**:无。
- **Rollback 代价**:低 —— 纯文档,`git revert` 0 副作用。但 revert 会把 session 记忆链打断,所以**事实上**不会回滚。
- **建议动作**:review 3 个 open questions 并在 PR 评论里明确回答(哪怕只是 "Q1: yes, Q2: keep base on v2, Q3: yes relax"),然后 merge。

---

### ⏸ 停一下

Batch A 合完后,`main` 应该有这个结构。在开 Batch B 前:

- 确认本地 `git pull origin main` 能拿到所有文件
- `ls -la` 大致看一遍目录,**感受一下**仓库的形状
- 无需跑任何测试(还没有)

---

## 3. Batch B · Infrastructure(任意顺序,可并行)

这 3 个 PR 互不依赖,可以并行合入。GitHub 会自动为后合的 PR 提示 rebase。

### PR #2 · chore/pre-commit-guards → harness-engineering-setup-v2

- **尺寸**:~700 行(pre-commit 配置 + 4 个 Python 守卫 + 2 个 lint 配置 + 1 个 CI workflow)
- **review 重点**:
  - `.pre-commit-config.yaml` —— 9 类 hook,问自己"每一条我都同意它生效吗?"
  - 4 个 `scripts/check_*.py` —— 每个都有 docstring 说明对抗的 steering 条目
  - `.github/workflows/lint.yml` —— 在 CI 上跑同一套 hooks
- **Base 注意**:base 是 `harness-engineering-setup-v2`,#1 合入 main 后,GitHub 会提示把 base 改为 main。**照做**。
- **合后 CI 行为**:
  - 所有后续 PR 的 `lint` workflow 开始生效
  - **很可能**会在 #3 / #4 / #6 等其他未合 PR 上标红(markdownlint、trailing whitespace、yamllint)
  - **那些红是好事** —— 守卫生效了。跟进 PR 里修一下即可
  - 注意:我本次所有 commit 都用了 `--no-verify`(因为本地没 pre-commit runtime)。合 #2 之后,这些未合 PR 里的 commit 会**在 CI 上**被 hooks 检查,可能现出问题
- **预期的 "good red"**(不要惊慌):
  - trailing whitespace / 缺尾部换行符
  - shellcheck 对 `run_review_persona.sh` 的小警告
  - markdownlint 对某些 table / heading 的 warn
- **预期的 "bad red"**(需要我跟进修):
  - gitleaks 标出任何真实 secret(应该没有;如果有告诉我)
  - `check_steering_headers.py` 说某个 steering front-matter 不合法
  - `check_commit_msg.py` 说某个 commit subject 不合规
- **Rollback 代价**:中。Revert 本 PR 会让 CI 的 lint job 消失,后续 PR 表面变绿,但守卫失效。除非你发现 hook 本身有 bug,否则不要 revert。
- **建议动作**:approve & merge;然后**等 CI 在其他 PR 上跑完一轮**,回来看我列的 "good red" 清单。

---

### PR #4 · docs/adr-0001-adopt-harness-starter → harness-engineering-setup-v2

- **尺寸**:~200 行(ADR + ADR README)
- **review 重点**:
  - ADR-0001 § 候选方案:看我放弃 A/B/C 的理由是否站得住脚
  - ADR-0001 § 退役条件:未来什么情况下这个 ADR 应被替换
  - § 监控信号:承诺的 5 个指标 —— **目前未落地**,P2 #16 跟进
- **Base 注意**:同 #2,合入后改 base 到 main。
- **合后 CI 行为**:lint workflow(由 #2 提供)会跑,可能有 markdownlint warn。
- **Rollback 代价**:低 —— ADR 合了也可以改状态为 `Superseded`,不必 revert。
- **建议动作**:approve & merge。如果你觉得候选方案 B/C 讨论不够细,可以评论留 followup。

---

### PR #7 · docs/table-stakes → harness-engineering-setup-v2

- **尺寸**:~515 行(LICENSE 200 行标准文本占大头)
- **review 重点**:
  - `LICENSE` 是 Apache-2.0 标准文本,**不要逐行读**,看"Copyright 2026 The kiro.dev Contributors"这行替换是否合你期望
  - `CODEOWNERS` —— 确认 `@liupengceo` 是你的账号;否则改掉
  - `CONTRIBUTING.md` —— 有中英混排,如果你倾向全中文或全英文,说一声
  - `SECURITY.md` —— 邮件占位 `security@<维护者域名>`,如果你有真邮箱可以在合入前改
  - `.env.example` 的 3 个变量名 `REVIEW_RUNNER` / `REVIEW_MODEL` / `CUSTOM_REVIEW_CMD`
- **Base 注意**:同 #2,合入后改 base 到 main。
- **合后 CI 行为**:
  - CODEOWNERS 生效,之后任何改 harness 路径的 PR 会**自动**请求 `@liupengceo` review(可能是你自己)
  - GitHub 默认的 "auto request reviews" 行为取决于 repo 设置
  - 建议你到仓库 Settings → Branches → 给 main 加 "Require review from Code Owners"
- **Rollback 代价**:中 —— LICENSE 一旦合入再删除有法律层面的微妙影响(后续 fork 已在 Apache-2.0 下)。建议**选择一次,不回头**。
- **建议动作**:
  1. 先改 CODEOWNERS 里的 `@liupengceo` 如果不对
  2. 改 SECURITY.md 里的邮箱如果想填真实的
  3. 然后 merge
  4. **合入后**去 GitHub Settings 把 CODEOWNERS 启用为必需 reviewer(可选但推荐)

---

### ⏸ 停一下

Batch B 合完后:

- `main` 上应该有 pre-commit / lint CI / LICENSE / CODEOWNERS
- **所有未合 PR 会在 CI 上跑 lint**,你会看到一批绿或红
- 如果有 "good red"(格式类),我来跟进
- 如果有 "bad red"(safety / schema 类),**不要继续合**,先让我修

---

## 4. Batch C · Harness pipes(必须串行)

### PR #3 · ci/review-personas-workflow → harness-engineering-setup-v2

- **尺寸**:~700 行(workflow + 3 个 script + review.yml)
- **review 重点**:
  - `.github/workflows/review.yml` 3 stage(plan → run personas → aggregate)
  - `scripts/select_personas.py` 的规则表 —— 这是 self-review P2 #13 承认的启发式规则,**会有 false positive**
  - `scripts/run_review_persona.sh` 的 `abstain` 分支 —— **这是 P0 #3 的 bug 源头**,但本 PR 留 bug,#6 修它
- **Base 注意**:合入后改 base 到 main。
- **合后 CI 行为**:
  - `review-personas` workflow 开始在每个 PR 上跑
  - **每个 PR 评论区会出现一个 sticky comment**,内容是 "Overall verdict: approve"(因为 `abstain` 被错误地赋为 `approve`)
  - **这正是 P0 #3 会误导你的原因** —— 如果你合 #3 但暂不合 #6,所有 PR 评论都会假装有 bot 批准了
- **!! 重要顺序 !!**:
  - **合完 #3 立刻去处理 #6 的 base**
  - GitHub PR 页面:打开 #6 → Edit → base branch 从 `ci/review-personas-workflow` 改为 `main`
  - GitHub 会自动重新计算 #6 的 diff,把 #3 已合部分移除,只留 #6 自己的改动
- **Rollback 代价**:高 —— review workflow 是 #8 / #10 / #11 部分假设的基础设施。revert #3 会让它们的 workflow 出错。
- **建议动作**:
  1. Merge #3
  2. **立刻** 改 #6 的 base 到 main
  3. 观察 #6 的 diff:应该只剩 abstain fix 相关文件(6 个 左右),不应包含 #3 的 workflow / script
  4. 如果 #6 diff 看起来包含了 #3 的内容 → 告诉我,我需要手动 rebase

---

### PR #6 · fix/review-abstain-verdict-v2 → [先改 base 再 review]

- **尺寸**(#3 合入 + base 改好后):~400 行(新增 validate_persona_output.py + run_review_persona.sh 改动 + aggregate 改动 + README § 3 改动 + DEPRECATION § 7 登记)
- **review 重点**:
  - `scripts/validate_persona_output.py` 的 4 条规则(见文件 docstring)
  - `scripts/aggregate_reviews.py` 的 `roll_up_verdict` 新逻辑 —— **关键:verify 它不把 abstain 当 approve**
  - `templates/review-personas/README.md § 3.1` 的 verdict 枚举(新加 `abstain`)和 § 3.2 输出契约(禁 code fence)
  - `scripts/run_review_persona.sh` 的 `abstain` 分支新 summary —— "Do NOT treat this as approval"
- **Rebase 风险**:如果合 #3 后 `ci/review-personas-workflow` 分支在 main 上已不存在,改 base 到 main 时 GitHub 会提示 "no changes" 或 "rebase required"。如果提示 rebase,让我来做(告诉我"需要 rebase #6")。
- **合后 CI 行为**:
  - 所有 PR 评论的 sticky 变成 "All N persona(s) abstained... Do not interpret this as approval" 大横幅
  - 如果你之前合了 #3 看到了"approve"误导,合 #6 后立即修正
- **Rollback 代价**:中 —— revert 会让误导回来。不建议。
- **建议动作**:approve & merge。

---

### ⏸ 停一下

Batch C 合完后:

- Review workflow 运作,但所有 verdict 都是 `abstain`(因为没接真 runner)
- **这是正确的** —— 你应该看到大横幅
- 如果合完之后发现横幅没出现 / 出现 "approve" 字样 / banner 格式乱,告诉我,P0 修复

---

## 5. Batch D · Governance(合 Batch B/C 后)

这 4 个 PR 依赖 Batch B 的 CI 基础设施。

### PR #8 · chore/pr-template-split → harness-engineering-setup-v2

- **尺寸**:~330 行
- **review 重点**:
  - 3 个 PR 模板(short / standard / harness_change)的字段差
  - `.github/pull_request_template.md`(short 版)是否**真的短**,≤ 50 行
  - `harness_change.md` 是否**真的严**,含 11 处 DEPRECATION 引用
- **Base 注意**:合入后改 base 到 main。
- **测试**:合完后你开一个 **dummy 小改动 PR**(比如改 README 的一个 typo),看默认模板是否是 short 版,**并且**你能通过在 URL 后加 `?template=standard.md` 切换到 standard 版。
- **合后 CI 行为**:下个 PR 自动用新 short 模板。
- **建议动作**:approve & merge。

---

### PR #9 · docs/agents-commands-clarify → harness-engineering-setup-v2

- **尺寸**:~210 行(AGENTS § 14 重写 + 新 docs/agent-commands.md)
- **review 重点**:
  - AGENTS.md § 14 标题 **"语义约定(**不是** API 契约)"** 是否足够醒目
  - docs/agent-commands.md 里 6 条命令的 "手动等价" 是否每条都真的可行
- **Base 注意**:合入后改 base 到 main。
- **Rollback 代价**:极低 —— 纯文档。
- **建议动作**:approve & merge。可选 followup:如果你把仓库对接到具体 agent 平台(Kiro / Codex CLI),在 docs/agent-commands.md 里补真实 skill 文件路径。

---

### PR #10 · ci/require-execplan → harness-engineering-setup-v2

- **尺寸**:~395 行
- **review 重点**:
  - `scripts/check_pr_has_execplan.py` 里的 `EXEMPT_COMMIT_TYPES` 和 `TYPO_LOC_THRESHOLD` 是否合你期望
  - `.github/workflows/require-execplan.yml` 的 triggers(`opened / synchronize / edited / reopened / labeled / unlabeled / ready_for_review`)
  - 6 条本地 smoke test 场景(在 commit message 里列出)
- **Base 注意**:合入后改 base 到 main。
- **合后 CI 行为**:
  - 任何新 PR 如果**触及代码 + 无 ExecPlan + 无豁免**,会收到 sticky comment + status 红
  - **不自动阻断 merge**,除非你到 Settings → Branches 把 `require-execplan / check` 设为 required
- **第一次验证**:合完后开一个故意违规的 dummy PR(改 `src/foo.py`,无 ExecPlan,无豁免 label),确认 workflow 标红并留评论。
- **Rollback 代价**:低 —— revert workflow 会让守卫消失,不损坏其他东西。
- **建议动作**:approve & merge,然后**做一次 dummy PR 验证**。

---

### PR #11 · ci/cross-refs-and-quarterly → harness-engineering-setup-v2

- **尺寸**:~400 行(cross_refs.py + 2 个 workflow + DEPRECATION § 7/8)
- **review 重点**:
  - `scripts/check_cross_refs.py` 的 `REF_RE` 正则 —— 保守 vs 过严的权衡
  - `scripts/check_cross_refs.py` 的 `resolve_ref_path` 3 层候选
  - `.github/workflows/quarterly-harness-review.yml` cron 表达式 `'0 10 1 2,5,8,11 *'`
- **Base 注意**:合入后改 base 到 main。
- **合后 CI 行为**:
  - cross-refs workflow 在每个 PR 上跑,**会立刻扫出问题**(我本地跑过 0 个 false positive,但 CI 上可能有编码差异)
  - quarterly-harness-review 不会立刻跑(下次触发是 Aug 1 / Nov 1),但你可以 workflow_dispatch 手动跑一次做 dry-run
- **第一次验证**:合入后到 Actions tab 手动 dispatch `quarterly-harness-review` with `dry_run=true`,看 body.md 生成是否合理。
- **Rollback 代价**:低。
- **建议动作**:
  1. approve & merge
  2. Actions tab → quarterly-harness-review → Run workflow → `dry_run=true` → 看日志
  3. 如果日志看起来对,以后每季度它会自动开 issue

---

## 6. 合完之后

全部 11 个合入 main 后:

- 仓库是 main-only(所有 feature branch 合并)
- 所有 workflow 生效
- 你手上有一个**真正会执行自己规矩**的 starter kit

### 回来找我做什么

- 如果遇到任何 "bad red"(见上文分类)
- 如果某个 workflow 误报 / 漏报
- 如果准备走 **Path A**(接真 `REVIEW_RUNNER`,需要告诉我三件事,见 session-001.md § 6 Q3 上面那一段)
- 如果准备走 **Path B**(pytest 覆盖 9 个脚本)
- 或者新任务

在那之前,我什么都不做。

---

## 7. 预期的"好红"清单(Batch B 合入后会看到)

我在本次 session 所有 commit 都用了 `--no-verify`。我预期 pre-commit / lint.yml 可能在其他未合 PR 上标出:

| PR | 可能的 flag | 原因 | 谁 fix |
|---|---|---|---|
| #3 | shellcheck warns on `run_review_persona.sh` | 我可能漏了一些 quoting | 我(追加 commit 到 #3) |
| #3 / #6 | markdownlint on README.md / persona files | 长行 / heading 风格 | 按 flag 具体内容决定 |
| #6 | gitleaks 误报 `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` 字符串 | 文档里出现了 env 名 | 看 gitleaks 是否真的把它当 secret;通常不会 |
| #9 | markdownlint on AGENTS.md / docs/agent-commands.md | 中英混排的 punctuation | 放宽 rule 或改文档 |
| #10 | yamllint on require-execplan.yml | 缩进或长行 | 跟进修 |
| #11 | yamllint on quarterly workflow 的 heredoc YAML | heredoc 里的 markdown 被误认为 YAML | 跟进修 |

**没出现就是 bonus**;出现了是守卫正在起作用。告诉我哪一条红,我来 fix(不新建 PR,追加 commit 到对应分支)。

---

## 8. 预期的"坏红"清单(需要我立刻 fix)

这些不应该出现;出现了说明我的守卫本身有 bug:

| 症状 | 可能原因 | 我的责任 |
|---|---|---|
| gitleaks 找到真实 secret | 我误把示例当真 | 立刻撤销 + 清历史 + 轮换 |
| cross-refs 扫出不应该红的条目 | 我的 regex 过严 | 放宽 regex + 登记 DEPRECATION |
| require-execplan 误标 docs-only PR 为 fail | `is_code_file` 有 bug | 修规则 + 加测试用例 |
| review-personas workflow 根本不跑 | matrix / trigger 配置错 | 修 workflow + 本地验证 |
| CODEOWNERS 要求不存在的用户 | `@liupengceo` 拼错 | 检查仓库 owner username |

---

## 9. 签名

- **agent**:kiro — 2026-05-09
- **human checkpoint**:@liupengceo — `[ ]` guide 有用 / `[ ]` guide 冗余
- **guide 变更历史**:
  - 2026-05-09 · v1 · 初版,11 个 PR 的 runbook
