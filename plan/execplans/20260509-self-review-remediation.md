# ExecPlan · Self-review remediation (P0)

- **任务 ID / Issue**:self-review-20260509(由对话提起,未单独建 issue —— 将在开始前补一个)
- **负责人**:@repo-owner
- **执行者**:kiro agent + 人类 acceptance
- **分类**:`harness-change` (多 PR bundle)
- **规模**:L (3-5 天 worth,分多次 session 完成)
- **长任务?**:Yes → 同步 `plan/PROGRESS.md` + 每 session 写 `plan/sessions/<N>.md`
- **Plan 版本**:v1

---

## 1. 目标(Goal)

让本仓库的 harness starter kit **从"优秀的文档骨架"升级为"会真正执行自己规矩的工作仓库"** —— 具体到:

- 本仓库**自己**的 PR 走本仓库自己的流程(ExecPlan + 模板 + pre-commit)。
- 自动化补齐缺口(ExecPlan 存在性检查、cross-ref 检查、季度复审自动 issue)。
- 消除 P0 级别的自相矛盾(`abstain` verdict 误导、PR 模板过长、命令表空头支票)。
- 补齐对外可见仓库的 table stakes(LICENSE / CODEOWNERS / CONTRIBUTING)。

简言之:**关掉"说教型 harness"的债**。

## 2. 动机与背景(Why)

- 自检(见对话 "这个项目有哪些地方需要完善") 暴露了 24 条问题,其中 10 条 P0/P1。
- 其中最严重的一条是:我开出的 4 个 PR 自己都没走 ExecPlan / PR 模板。
- Anthropic《Managed Agents》明确警告:**harness 会老化;说教型 harness 老化得最快**。不把规矩变成机械检查,6 个月后这个仓库会沦为"讲道理的仓库"。

关联:
- `docs/harness-engineering/02-anthropic-harness.md § Managed Agents`
- `AGENTS.md § 3`、`§ 9`、`§ 10`
- `.kiro/steering/DEPRECATION.md § 复审节奏`

## 3. 非目标(Non-goals)

明确**本次不做**:

- 不真正接入某个 agent 平台(Codex/Claude/Cursor)做 review — 留给 ADR-0002。
- 不改 ExecPlan 模板本身 — 先让模板**有人用**再讨论该不该瘦身。
- 不改 review persona 文本 — 先把机械管道做对。
- 不做 GitLab / Gitea 抽象 — 先把 GitHub 路径做对,留 ADR-0003。
- 不追溯补齐精读库 10 章的 `last_reviewed` — 单独一个小 PR 做。

## 4. 影响面 / Impact Map

### 4.1 会被触及的文件

| 路径 | 改动类型 | 风险 |
|---|---|---|
| `plan/execplans/*.md`(此文件 + 后续 4 份) | 新增 | 无 |
| `plan/sessions/001.md` | 新增 | 无 |
| `plan/PROGRESS.md` | 修改 | 无 |
| `scripts/run_review_persona.sh` | 修改 verdict 语义 | 中:影响所有用过本 adapter 的 fork |
| `scripts/aggregate_reviews.py` | 支持 `abstain` verdict + banner | 中:聚合 YAML 格式新增 |
| `templates/review-personas/README.md` | verdict 枚举 + YAML 输出契约 | 中:契约变更 |
| `.github/pull_request_template.md` | 拆成 short / full | 低 |
| `.github/PULL_REQUEST_TEMPLATE/*.md` | 新建 | 低 |
| `.github/workflows/require-execplan.yml` | 新增 | 低 |
| `scripts/check_cross_refs.py` | 新增 | 低 |
| `.pre-commit-config.yaml` | 加入 cross-refs hook | 低 |
| `.github/workflows/quarterly-harness-review.yml` | 新增 schedule | 低 |
| `LICENSE` / `CONTRIBUTING.md` / `CODEOWNERS` / `.env.example` | 新增 | 低 |
| `AGENTS.md § 14` | 命令表加警示 | 低 |
| `.kiro/steering/docs.md § 9 双语` | 放宽到"术语表中英必备,其他文件按情况" | 低 |
| `.kiro/steering/DEPRECATION.md` | 登记本轮每一条 | 低 |

### 4.2 下游影响

- 现有 open PR(#1–#4):合并后本 follow-up 的改动才会真正生效。本 plan 假设 **PR #1 先合** 才继续推进(见 § 13)。
- 任何 fork 会感觉到 `abstain` 行为变化(从 approve → abstain);属于**向后不兼容**,但因为还没有用户,可接受。

### 4.3 Blast radius

- **最坏情况**:CI 工作流错误导致所有 PR 开起来就红。**回滚**:一次 revert 对应 PR。
- **中等**:persona schema 变更让已有 fork 的 adapter 报错 → 在 README.md § 3 打出兼容性说明 + 半年过渡期。

## 5. 方案(Approach)

### 5.1 选择的方案

**分 7 个 PR,每个独立走完整流程,全部 base 在 `harness-engineering-setup-v2`**,以便无论 #1 何时合入,本批 PR 都能跟得上。

7 个 PR 顺序(顺序=优先级):

1. **docs(plan): self-review ExecPlan + session-001 handoff**(本 PR)
2. **fix(review): abstain verdict + banner**(P0 #3)
3. **docs(repo): LICENSE + CODEOWNERS + CONTRIBUTING + .env.example**(P0 #10)
4. **chore(templates): split PR template into short + full**(P0 #4)
5. **docs(agents): mark § 14 commands as conventions, not bindings**(P0 #2)
6. **ci(require-execplan): enforce ExecPlan presence on code PRs**(P1 #5)
7. **ci(cross-refs + quarterly): 机械化两条 harness 老化防线**(P1 #6 + #9)

### 5.2 候选方案

| 方案 | 要点 | 为什么放弃 |
|---|---|---|
| A · 一个大 PR 打包所有修复 | 简单、一次过 | 违反 `git-workflow.md § 4.1` 的 400 行 / 原子 PR 原则;review 困难 |
| B · 改写已有 4 个 PR | 把 ExecPlan 塞进已有 PR | 破坏 immutable history;违反 `git-workflow.md § 2` "amend after review" 反模式 |
| **C(选中)** · 7 个独立小 PR 向前修复 | 每个守规矩 | 唯一符合自己规矩的做法 |

### 5.3 参考

- Stripe Minions 的"每 PR 一个 Blueprint"(`docs/harness-engineering/03-stripe-minions.md § 3`)
- Martin Fowler 站 Kief Morris "verified = 机械化"(`docs/harness-engineering/05-martin-fowler.md § 3`)

## 6. 步骤(Steps)

本 plan 只覆盖 **PR-1**(meta)。其余 6 个 PR 各自有自己的 ExecPlan(放 `plan/execplans/`)。

- [ ] **S1**:写本 ExecPlan(你正在读这个)。
- [ ] **S2**:写 `plan/sessions/001.md` 交班,覆盖之前 4 个 PR + 本轮 self-review。
- [ ] **S3**:刷新 `plan/PROGRESS.md`(长任务状态 + feature 清单 + next up + 开放问题)。
- [ ] **S4**:提交 meta PR,base = `harness-engineering-setup-v2`。

## 7. 验收标准

### 7.1 机器可验证

- [ ] `plan/execplans/20260509-self-review-remediation.md` 存在且非空
- [ ] `plan/sessions/001.md` 存在,含 8 段必填
- [ ] `plan/PROGRESS.md` 的 § 2 feature list 至少列出 7 个 follow-up PR 占位
- [ ] PR 分类为 `harness-change`,带 `harness-change` label(打不上没关系,label 会在首次手动加后保留)
- [ ] Pre-commit 在本 PR 内**正式首次** 跑通(本 PR 是 meta,理论上没代码改动,但仍需让 hook 不报错)

### 7.2 人类 rubric

| 维度 | 权重 | 标准 |
|---|---|---|
| 自洽性 | 40 | 本 PR 本身是否符合自己定的规矩 |
| 后续可执行 | 30 | 6 个 follow-up PR 的结构是否真的能按此 plan 推进 |
| 可回滚 | 10 | 本 PR 所有内容都是文档,revert 代价 0 |
| 可追溯 | 20 | PROGRESS / HANDOFF 能让下一次 session 30 秒内接手 |

**总分 ≥ 85 才合入。**

## 8. 回滚计划

- 本 PR 是纯文档,`git revert` 即可。
- 不引入代码路径变化,没有 migration,没有副作用。

## 9. 观测与告警

- 无(文档)。
- **自观测**:本 plan 将在 `plan/sessions/001.md` 记录 self-review 对话中提出的 24 条问题,每条标 P0/P1/P2/P3 以及是否被本轮 follow-up 覆盖。

## 10. 文档与 ADR

- 更新 `plan/PROGRESS.md`。
- 不写 ADR(本身只是"执行现有 ADR-0001")。
- 下一个 follow-up PR 如果涉及接口语义变化(例:`abstain` verdict 变更 schema),**会写 ADR-0002**。

## 11. Harness 改动

- **本 PR 不改 harness**。
- 但它是一个**明确的 bootstrap 异常**的范例:AGENTS.md 刚建立的 4 个 PR 没走 ExecPlan,本 PR 显式追认这个异常并在 § 12 提出永久的"bootstrap exception"登记方式。

## 12. 未解决问题 / 需要人类决策

- [ ] **Q1**:是否接受"过去 4 个 PR 没有 ExecPlan 是 bootstrap 异常"?
  - 查过:`AGENTS.md § 3.1`、`.kiro/steering/harness.md § 2 R1`、`DEPRECATION.md § 1 不需要登记的情况`。
  - 倾向:**接受**。写入 DEPRECATION.md 一条"bootstrap exception (retired)"条目作为历史留痕。
  - Fallback:如果 48 小时未回应,按倾向执行,在后续 PR 可被撤销。

- [ ] **Q2**:本 follow-up 是否要等 #1 合并才继续,还是让所有 PR base 在 #1 分支?
  - 查过:GitHub PR chain 模式、`git-workflow.md § 7 冲突解决`。
  - 倾向:**让所有 follow-up 都 base 在 `harness-engineering-setup-v2`**,#1 合并后一次性 rebase 到 main。这样无论 #1 何时合都不阻塞。
  - Fallback:如果 review 太复杂,切到逐个合入模式。

## 13. 时间 & 依赖

- agent 工时:meta PR ≈ 30 分钟;6 个 follow-up ≈ 2–3 小时(agent 在 session 内)
- 人类 review 时间:meta ≈ 5 分钟;每个 follow-up ≈ 10 分钟
- 依赖:无外部依赖;所有改动在仓库内。

## 14. Checkpoint 签名

- [ ] **Plan checkpoint**(人类):__ · YYYY-MM-DD · `approve / approve-with-changes / reject`
- [ ] **Review checkpoint**(personas):pre-commit 本地跑通(本 PR 无代码,仅 markdown)
- [ ] **Acceptance checkpoint**(人类):__ · YYYY-MM-DD · rubric 总分 __/100

## 15. Plan 变更历史

| 版本 | 日期 | 改了什么 | 谁 |
|---|---|---|---|
| v1 | 2026-05-09 | 初版 | kiro agent |
