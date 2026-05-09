# ADR-0001 · 以 Harness Engineering 起步套件作为本仓库的协作基线

- **状态**:Accepted
- **日期**:2026-05-09
- **作者**:@repo-owner + kiro agent(起草)

---

## 上下文

本仓库的目的,是把 2026 年前后在 OpenAI、Anthropic、Stripe、Shopify、Martin Fowler 站等来源共同浮现的 **"Harness Engineering"** 一类实践,沉淀为一个**可复用的起步套件**(starter kit),方便我们自己和他人在 agent-first 的方式下开展软件工程。

我们面临的约束:

- 这是一个新工作方式,团队里没有人"**这么干过三年**"的肌肉记忆。
- 模型迭代速度快,任何 harness 都有老化风险(Anthropic《Managed Agents》已明确警告)。
- 团队希望"**人类 on the loop**" —— 管**环本身**,而不是每一条 artifact 都亲手审。
- 我们不想被任何单一 agent 平台(Codex / Claude Code / Cursor / Kiro / 自研)锁死。
- 新人(或新 agent)应当在**30 分钟内**理解"在这个仓库里该怎么干活"。

同时,我们从多方资料(见 `docs/harness-engineering/09-references.md`)抽出几条共同结论:

1. **Agent = Model + Harness**,限制产出质量上限的几乎总是 harness,不是模型。
2. **Repo is source of truth**;藏在其他地方的知识对 agent 不存在。
3. **Fix the harness, not the output**;同类错误第二次出现就触发结构性改动。
4. **Tool subtraction > tool addition**;约束悖论反复被验证。
5. **Long-running agents lose memory**;必须显式的"轮班 handoff"。
6. **Harnesses encode assumptions that age**;必须设计退役路径。

---

## 决策

在本仓库**正式采纳**以下一整套工程基线,作为所有任务的默认 harness:

1. 仓库根的 `AGENTS.md` 为 agent 行为契约的**最高基线**。
2. `.kiro/steering/` 作为 AGENTS.md 的按主题细化(harness / code-style / testing / security / docs / git-workflow / DEPRECATION)。
3. `docs/harness-engineering/` 的中文精读库作为**共享的知识底座**。
4. `templates/ExecPlan.md` + `.github/pull_request_template.md` 作为**任务流程的两道 checkpoint**(plan + PR)。
5. `templates/review-personas/` 的 8 个 review persona 作为**代码评审的默认调度集**。
6. `plan/PROGRESS.md` + `plan/HANDOFF.md` + `plan/sessions/` + `plan/decisions/` 作为**长任务的记忆三件套**。
7. `.kiro/steering/DEPRECATION.md` 作为 **harness 老化对抗台账**——每一条为对抗当前模型缺陷而加的约束都要在这里登记退役条件。
8. Pre-commit + CI 上的 hooks 作为**机器可验证的 steering**,让 harness 的关键点**不依赖 agent 是否记住**。
9. `.github/workflows/review.yml` + persona 适配器(`REVIEW_RUNNER` 抽象层)作为**persona 自动调度**的实现,不绑定任何模型厂商。

**人类的工作模式由此确定为 "on the loop"**:
- 做目标、acceptance、plan checkpoint、final acceptance、harness-change review。
- **不做**逐行代码审阅、琐碎工具调用、机器可验证的 lint。

---

## 候选方案

### A · 完全不搭 harness,靠 prompt 对话式协作

- **优点**:零前期成本;起步快。
- **缺点**:
  - 任务扩大时,同类错误反复出现,成本复利。
  - 不同 agent session / 不同人用 agent 习惯不一致,互相踩坑。
  - 无法解决长任务的"失忆"问题。
  - 审计轨迹差:合规与 postmortem 代价高。
- **放弃理由**:这等于"**赌每一次对话都完美**",与 harness engineering 的论点直接冲突。

### B · 采用某个现成平台的默认"skill / 规则"(如 Claude Code skills、Cursor rules)

- **优点**:上手快,有社区支持。
- **缺点**:
  - 绑定特定 agent 平台,跨团队协作时摩擦高。
  - 平台抽象层在快速变化,容易踩版本升级的坑。
  - 不易把"业务特定"的 steering 做到精细。
- **放弃理由**:我们希望**平台无关**,只在适配器层(`REVIEW_RUNNER`)接入具体平台。

### C · 自研一套完整的工作流 DSL / orchestration 框架(类似 Shopify Roast)

- **优点**:灵活、彻底,针对本仓库量身定做。
- **缺点**:
  - 极重的前期投入(3-6 人月起)。
  - 抽象过早,容易做出 "over-engineered" 的怪物。
  - Harness 本身会老化,还没等它成熟可能就要翻新。
- **放弃理由**:当前阶段投入产出比差。等到 8 节 "后果" 的监控信号告诉我们"**约束力不够**"时,可以起 ADR-0002 走 B / C 方向。

### D · 本 ADR 的选择:轻量"脚手架 + 约定"

- 只做**文档、模板、脚本**——三类 artifact 都原生属于 git 仓库,没有运行时依赖。
- 约定用**抽象适配层**(`REVIEW_RUNNER` / `AGENTS.md` 本身)解耦具体 agent 平台。
- 把**可机器化**的部分(pre-commit / CI)落成代码;剩下的留给人类注意力。

---

## 取舍理由

- **与公共实践保持可迁移**:我们想让任何看过 OpenAI/Anthropic/Stripe/Shopify/Martin Fowler 材料的人都能在这个仓库里**立刻上手**。方案 D 的词汇、结构、命名直接从这些公共资料对齐。
- **演化成本最低**:方案 D 可以向 A(放弃)、B(绑定某平台)、C(自研 DSL)任一方向演化,没有沉没成本。
- **压力测试**:我们用 kiro.dev 自身作为"吃自己的狗粮"场:本仓库的每一个 PR 都走这套流程,让 harness 的问题尽早暴露。

---

## 后果

### 正向

- 新贡献者(人或 agent)在 30 分钟内获得"本仓库怎么干活"的共同语言。
- 所有任务强制 plan checkpoint,把错误代价左移。
- Harness-change 独立 PR + DEPRECATION.md 登记,使"为对抗当前模型缺陷打的补丁"可见、可退役。
- Pre-commit + CI 复用同一套规则,避免"CI 绿 + 本地红"的不对称。

### 负向

- 起步成本比 "直接开干" 高:第一次任务要读 AGENTS.md + harness.md + ExecPlan 模板。
- 新开发者可能觉得 PR 模板"填字段填得累"。
- DEPRECATION 台账需要**人持续复审**;若无人复审,本决策的对抗老化效力退化。
- Review persona 套装**有噪音风险**——若 persona 过度 false positive,PR 作者会学会忽略评论,整套自动评审失效。

### 监控信号(每季度复审一次)

| 信号 | 解读 | 应对 |
|---|---|---|
| PR 作者抱怨"模板太繁" | 模板与真实需要脱节 | 裁剪 / 拆分 / 改为可选字段 |
| `DEPRECATION.md` 条目无新增 / 无退役 | 台账被遗忘 | 指定 steward + 加入季度回顾 |
| Persona 评论里的 finding **持续** 被忽略 | 噪音过高 | 关闭对应 persona 或改规则 |
| "harness-change" 标签 PR 超过总 PR 20% | 我们在加补丁,不是做结构 | 警示:不是每次失败都值得 harness 改动 |
| 任意 PR 绕过 plan checkpoint 直接开 PR | 流程破窗 | 强化 steering + review persona |

---

## 退役条件

本 ADR 在满足下列任一条件时**应当复审**:

1. **模型跨代升级后**(例:整个平台从 GPT-5/Claude-4 系列跳到 GPT-6/Claude-5+):
   - 首要动作:复审 `.kiro/steering/DEPRECATION.md`,删除不再必要的约束。
   - 评估本 ADR 的各子项是否还需要保留。
2. **出现了公认优于"starter kit"的新范式**:
   - 例如某平台(Codex App Server、Anthropic Managed Agents、其他)把本仓库的绝大部分 harness 内化为基础设施,我们只需留本地化的 steering。
   - 此时应写 `ADR-XXXX superseding ADR-0001`。
3. **度量说"成本大于收益"**:
   - 连续 2 个季度的 "PR throughput / 人 / 天" 显著低于同规模对照(如果我们有)。
   - 或"harness-change PR 占比" 长期过高(>20%)。
4. **所有 Follow-up(pre-commit / review.yml / 本 ADR)**都稳定运行后,2027-Q2 起每半年做一次主观+量化评估,决定继续、收紧、放宽。

---

## 相关

- `AGENTS.md`
- `.kiro/steering/harness.md`
- `.kiro/steering/DEPRECATION.md`
- `docs/harness-engineering/06-methodology.md`
- `docs/harness-engineering/07-practice-checklist.md`
- `templates/ExecPlan.md`
- `templates/review-personas/README.md`
