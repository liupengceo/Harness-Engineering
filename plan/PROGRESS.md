# PROGRESS · 长任务全局进度

> 本仓库的**长任务主线**:构建一份可被外部复用的 Harness Engineering starter kit,并持续吃自己的狗粮。

## 0. 元信息

- **长任务名称**:Harness Engineering starter kit for `kiro.dev`
- **创建日期**:2026-05-09
- **owner**:@repo-owner
- **主要执行 agent**:kiro(Vibe mode)
- **预计持续**:持续维护,不封板
- **相关 issues / 分支**:`harness-engineering-setup-v2`、`main`

## 1. 目标

让任何人(或 agent)打开本仓库,**30 分钟内**就能把 OpenAI / Anthropic / Stripe / Shopify / Martin Fowler 的 harness engineering 实践**直接用在自己的项目里**。
同时,本仓库**自身**要作为"会真正执行 harness engineering 的工程仓库"的示范——而不是"只会讲 harness engineering 的仓库"。

## 2. Feature List + 状态

| # | Feature / 子目标 | 状态 | 负责 session | PR | 备注 |
|---|---|---|---|---|---|
| 1 | Bootstrap:AGENTS + steering + docs + templates + plan 骨架 | Done | 001(bootstrap 段) | [#1](https://github.com/liupengceo/kiro.dev/pull/1) | 追认 bootstrap 豁免 |
| 2 | Pre-commit hooks + CI + 4 守卫脚本 | Done | 001(bootstrap 段) | [#2](https://github.com/liupengceo/kiro.dev/pull/2) | |
| 3 | Review persona dispatch workflow + adapter | Done | 001(bootstrap 段) | [#3](https://github.com/liupengceo/kiro.dev/pull/3) | abstain verdict 有缺陷,FU-2 修 |
| 4 | ADR-0001 采纳 | Done | 001(bootstrap 段) | [#4](https://github.com/liupengceo/kiro.dev/pull/4) | |
| 5 | **Self-review meta PR**(ExecPlan + session-001) | In progress | 001 | (本 PR) | 为 FU-2~FU-7 做准备 |
| 6 | FU-2 · fix(review): abstain verdict + banner | Todo | 001 | - | P0 #3 |
| 7 | FU-3 · docs(repo): LICENSE + CODEOWNERS + CONTRIBUTING + .env.example | Todo | 001 | - | P0 #10 / P1 #11 |
| 8 | FU-4 · chore(templates): split PR template short/full | Todo | 001 | - | P0 #4 |
| 9 | FU-5 · docs(agents): mark § 14 commands as conventions | Todo | 001 | - | P0 #2 |
| 10 | FU-6 · ci(require-execplan) | Todo | 001 | - | P1 #5 + 部分 #8 |
| 11 | FU-7 · ci: cross-refs check + quarterly-harness-review | Todo | 001 | - | P1 #6 + #9 |
| 12 | P2 批次:脚本测试、精读库 last_reviewed、双语规则修订 | Backlog | 未排期 | - | 单独一轮 |
| 13 | P3 批次:ExecPlan micro/standard 分档、AGENTS.md digest、GitHub 抽象 | Backlog | 未排期 | 需先写 ADR-0002 | |

状态取值:`Todo` / `In progress` / `Blocked` / `Done` / `Dropped` / `Backlog`。

## 3. 下一步(Next up)

- [ ] **#1 · 合 meta PR**(当前在做),base `harness-engineering-setup-v2`
- [ ] **#2 · 开 FU-2**:`fix(review): abstain verdict + banner`
- [ ] **#3 · 并行开 FU-3**:LICENSE 等 table-stakes 文件

## 4. 已发现但未解决的坑(Known issues)

| # | 现象 | 触发条件 | 当前对策 | 长期方案 |
|---|---|---|---|---|
| 1 | Sandbox 无法 `pip install pyyaml` | 本地开发 | 所有真实机械验证在 CI | `.github/workflows/lint.yml` 已覆盖 |
| 2 | `abstain` adapter 产出 verdict=approve | 现有 #3 | FU-2 修 schema + banner | Schema 改动,半年过渡 |
| 3 | PR 模板过长 | 所有真实 PR | FU-4 拆 short/full | 基于 PR 类型自动选择 |
| 4 | `AGENTS.md § 14` 命令是空头支票 | Agent 试图用 slash 命令 | FU-5 加警示文字 | 后续 ADR-0002 真正实现 |
| 5 | CI 没检查 ExecPlan 存在 | feat/fix PR 可混过 | FU-6 `require-execplan.yml` | |
| 6 | Cross-reference 可能失效 | 文档 section 重命名 | FU-7 `check_cross_refs.py` | |
| 7 | DEPRECATION.md 没季度提醒机制 | 时间流逝 | FU-7 `quarterly-harness-review.yml` | |
| 8 | 脚本 0 测试覆盖 | 脚本回归 | Backlog P2 批次 | |
| 9 | 精读库无 last_reviewed | 外部资料变化 | Backlog P2 批次 | |
| 10 | Persona YAML 输出混有 code fence 的风险 | Adapter 作者不规范 | FU-2 顺手规范 | `scripts/validate_persona_output.py`(P2) |

## 5. 架构/接口 关键决策索引(ADR)

- [ADR-0001](../docs/adr/0001-adopt-harness-engineering-starter-kit.md) · 采纳 Harness Engineering 起步套件 → Accepted
- (将来)ADR-0002 · Adopt a specific review runner(Codex / Claude / 自研) → 未起
- (将来)ADR-0003 · CI abstraction for GitLab/Gitea → 未起

## 6. 指标 / 可观察性

**目标(ADR-0001 承诺):**

- PR/人/天 吞吐(OpenAI 参考值 3.5)
- PR 首次通过 CI 比例
- 人类 review 平均时长
- 同类错误复现次数
- Harness 变更 PR 比例(警戒线:< 20%)
- 工具数量

**当前状态**:**未落地**。Backlog P2 #16(ADR-0001 指标)。
在实际有度量之前,本 § 是目标声明,不是 dashboard。

## 7. 人类决策悬而未决(Open questions)

- [ ] **Q1** · 接受 bootstrap 异常?(见 session-001 § 6 Q1)
- [ ] **Q2** · 6 个 follow-up 的 base 策略?(见 session-001 § 6 Q2)
- [ ] **Q3** · 双语规则放宽?(见 session-001 § 6 Q3)

## 8. Session 摘要索引

- [sessions/001.md](./sessions/001.md) · 2026-05-09 · Bootstrap 追认 + Self-review + 规划 6 个 follow-up
