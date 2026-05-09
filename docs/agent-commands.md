# Agent Commands · 语义约定参考

> 本文件是 `AGENTS.md § 14` 的详细版。它不实现任何命令;它**定义**每条命令想表达的语义,并为不同 agent 平台给出对接建议。

## 原则

本仓库**不**绑定任何具体 agent runtime。`/plan`、`/review` 这类字符串只是团队共同语言,用于把"我要做 X"压缩成一句话。真正落地的**永远是 artifact**:

- 一份合格的 `ExecPlan.md`
- 一份合格的 review persona YAML
- 一份合格的 `sessions/<N>.md` 交班记录
- 一个带对应标签 + 模板的 PR

如果你达成了这些 artifact,**无论你是不是真的输了 `/plan`,都算遵守了语义**。

## Commands

### `/plan <issue-or-desc>`

**Semantics**
为指定 issue(或自由描述)产出填好的 `ExecPlan`,放到 PR 的第一个 commit。

**Expected artifact**
- `plan/execplans/<YYYYMMDD>-<short-slug>.md`,遵循 [`templates/ExecPlan.md`](../templates/ExecPlan.md) 的 15 节结构
- OR(对 short 规模):PR 描述里的 micro-plan(What / Why / 3 steps / rollback)

**Manual equivalent**
1. 读 issue 的 acceptance(若缺,先 `AGENTS.md § 11` 停下来问)
2. `cp templates/ExecPlan.md plan/execplans/<date>-<slug>.md`
3. 逐节填(§ 1 goal、§ 4 impact、§ 6 steps、§ 7 acceptance 至少必填)
4. `git add` + `git commit -m "docs(plan): ExecPlan for ..."`
5. **不要开 PR,等 plan checkpoint**

**Per-platform suggestions**
- **Codex CLI**:把 `.codex/skills/plan.md` 设为工作流;让 `codex plan <issue-url>` 走上述流程。
- **Claude Code**:定义一个 sub-agent(`general-task-execution`)带 system prompt "按 templates/ExecPlan.md 产出 plan"。
- **Cursor**:在 Rules 里加"开始任务前先写 ExecPlan"。
- **Kiro(本工具)**:使用内置 spec / plan 能力。

**Anti-patterns**
- ❌ 一边写代码一边"顺手"写 plan。plan 必须**先**。
- ❌ Plan 里只有 steps,没有 impact map / rollback。那不是 plan,是 checklist。
- ❌ Plan 长度 < 10 行且不是 short 规模。

---

### `/context <path-or-symbol>`

**Semantics**
把 `<path>` 相关的"影响面 + 已有决策"注入当前对话,避免盲改。

**Expected artifact**
Just-in-time 上下文片段(不需要落盘;如果任务是 L+,可选地落入 plan 的 § 4)。

**Manual equivalent**
1. `grep -rn '<key>' . --include='*.ts' --include='*.py'` 找调用点
2. `ls docs/adr/` 挑 1–3 篇最相关
3. `grep -l '<topic>' .kiro/steering/` 找相关 steering
4. 挑最相关的 40–60 行塞进对话,**不要**塞全文

**Per-platform**
- 大多数 agent 平台有"**read file / grep**"工具组合,用那个。
- Kiro 有专门的 context-gatherer sub-agent,可以委派。

**Anti-patterns**
- ❌ 把整个 `docs/` 塞进 prompt。那是 context bloat,见 `harness.md § 4`。
- ❌ 跳过这一步"我记得大概怎么写"。猜测 = 幻觉。

---

### `/review <persona|all>`

**Semantics**
用 `templates/review-personas/<persona>.md` 作为 system prompt,对当前 PR diff 产出**符合 `templates/review-personas/README.md § 3` schema 的 YAML**。

**Expected artifact**
`review-<persona>.yaml`,内容见 schema。**必须**是 raw YAML(不带 markdown code fence)。

**Manual equivalent**
1. `git diff <base>...HEAD > pr.diff`
2. 读 `templates/review-personas/<persona>.md`,当作 system prompt
3. 请一个 LLM 用该 system prompt 评审 `pr.diff`
4. 产出 YAML 并通过 `python3 scripts/validate_persona_output.py --persona <persona> --input review-<persona>.yaml`

**Per-platform**
- CI 会自动做这件事(`.github/workflows/review.yml` + `scripts/run_review_persona.sh`)。
- 本地使用时,本 CLI 路径依赖 `REVIEW_RUNNER` 变量(见 `.env.example`)。

**Anti-patterns**
- ❌ 跑了 review 但没把 YAML 交给聚合器(workflow 自动做,本地场景需手动保留)。
- ❌ 自己"裁决"冲突。Orchestrator persona 的职责是汇总而非裁决,冲突升到人。

---

### `/handoff`

**Semantics**
长任务 session 结束前,写**一份新** `plan/sessions/<N>.md` + 覆写 `plan/HANDOFF.md` 为其副本。

**Expected artifact**
- `plan/sessions/<N>.md`(新增,N = 上一编号 + 1)
- `plan/HANDOFF.md`(覆写)
- 可选:更新 `plan/PROGRESS.md` 的 feature list 状态

**Manual equivalent**
1. `ls plan/sessions/` 找最大 N
2. 按 `plan/HANDOFF.md` 的 8 段结构写 `plan/sessions/00(N+1).md`
3. `cp plan/sessions/00(N+1).md plan/HANDOFF.md`
4. 更新 PROGRESS § 2 的 feature 状态
5. commit 到长任务分支

**Anti-patterns**
- ❌ 用 `git commit --amend` 改历史 handoff。handoff 是**immutable 记录**,类似 ADR。
- ❌ 省略"**下一次 session 该做什么**"。那是整份 handoff 最重要的字段。

---

### `/harness-change <reason>`

**Semantics**
起一个**独立** PR,只包含 harness 改动,用 `?template=harness_change.md`,标 `harness-change` label,并登记 `.kiro/steering/DEPRECATION.md`(除非属于 § 1 的永久性豁免)。

**Expected artifact**
一个带完整 harness_change PR 描述的 PR(见 `.github/PULL_REQUEST_TEMPLATE/harness_change.md`),含 ≥ 1 条 DEPRECATION 登记或显式豁免。

**Manual equivalent**
见 `AGENTS.md § 3.4`。

**Anti-patterns**
- ❌ 把 harness 改动塞进业务 PR("反正都是我改的一起提")。这是最常见的降维攻击。
- ❌ 跳过 "Why is this harness and not a prompt patch" 那节("反正就是加一条 rule")。

---

### `/acceptance`

**Semantics**
对照 issue / ExecPlan § 7 的 rubric,**机器化**地对当前产物打分,把报告贴进 PR 评论。

**Expected artifact**
一段 markdown 评论,表格形式,列出每条 rubric 的 "pass / fail / N/A + 证据链接"。

**Manual equivalent**
1. 打开 issue 的 acceptance section / ExecPlan § 7
2. 逐条:对 "机器可验证" 项跑对应命令并记 output hash
3. 对 "人类 rubric" 项粘贴截图 / 具体 commit 链接作为证据
4. 产出 markdown 贴到 PR

**Per-platform**
- 目前**未**工作流化,由人类在 acceptance checkpoint 做。
- 未来可做成 `.github/workflows/acceptance.yml`,延到 ADR-0002 后。

**Anti-patterns**
- ❌ 把 "我觉得可以了" 当 acceptance。必须引用 rubric 项。
- ❌ 在没填 rubric 的 issue 上跑 acceptance。先让 issue 补上(见 `AGENTS.md § 11`)。

---

## 如何为你的平台落地

基本思路:**每个命令 = 一个 sub-agent / skill / workflow**,带对应 system prompt 指向正确的模板文件。

例子(Kiro):
- `/plan` → custom agent with system prompt pointing at `templates/ExecPlan.md`
- `/review` → use `invoke_sub_agent` with persona file as context

例子(Codex CLI):
- 在仓库放 `.codex/skills/` 目录,每个命令一个 markdown skill。

例子(Claude Code):
- 用 `.claude/commands/` 或 Agent Skills。

**无论哪种**,本仓库不关心;只关心你**产出的 artifact 是否合规**。CI + pre-commit + validator 会把关。

## 为什么不直接实现?

- 绑定某平台 = 与 starter kit 中立性违背。
- 平台本身在快速演化(Codex CLI、Claude Skills、MCP…),过早实现 = 过早老化(见 `docs/harness-engineering/02-anthropic-harness.md § Managed Agents`)。
- 真正的锚点是 **artifact schema**,不是 command syntax。

---

## 相关

- [`AGENTS.md § 14`](../AGENTS.md) — 本文件的简版入口
- [`templates/ExecPlan.md`](../templates/ExecPlan.md)
- [`templates/review-personas/README.md`](../templates/review-personas/README.md)
- [`plan/HANDOFF.md`](../plan/HANDOFF.md)
- [`.kiro/steering/DEPRECATION.md`](../.kiro/steering/DEPRECATION.md)
