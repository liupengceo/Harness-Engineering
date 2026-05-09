# 02 · Anthropic 的三篇 harness 文章精读

Anthropic 在 2025 年底 ~ 2026 年初,沿着 harness 这条主线连续发了至少三篇工程文章,合起来几乎就是"长任务 agent"的完整方法论。

| 文章 | 链接 | 问的问题 |
|---|---|---|
| Effective harnesses for long-running agents | https://anthropic.com/engineering/effective-harnesses-for-long-running-agents | 长任务里每次 session 都"失忆",怎么办? |
| Harness design for long-running application development | https://www.anthropic.com/engineering/harness-design-long-running-apps | 单 agent 不够,多 agent 怎么搭出更好的产物? |
| Managed Agents(Decoupling the brain from the hands) | https://www.anthropic.com/engineering/managed-agents | Harness 会随模型进化而"老化",怎么防? |

---

## 1. Effective Harnesses for Long-Running Agents

### 1.1 问题比喻

Anthropic 用的画面感很强:**一个项目由多班轮替的工程师维护,每班人一上班都没有上一班的记忆**。这就是长任务 agent 的处境——受限于 context window,每次 session 都是新的一盘棋。

### 1.2 二元结构

他们给 Claude Agent SDK 做了一个**双 agent** 解决方案:

- **Initializer Agent**(初始化员)
  - 只跑第一次。
  - 搭好环境:feature list、git 仓库、进度跟踪文件、约定的目录结构。
  - 输出是后续所有 session 都能直接读的"环境契约"。

- **Coding Agent**(值班员)
  - 每次 session 做一小步增量。
  - 强制要求保持仓库 clean 状态(编译通过、测试不退化)。
  - 结束前**显式写下"交班记录"**:这次做了什么、下次该做什么、哪里有坑。

### 1.3 社区整理的 7 个模式

Ahmed Nadar 基于这篇原文,整理了 [7 patterns](https://ahmednadar.com/7-patterns-for-long-running-agent-harnesses/),并给出一个值得记住的观察:

> 前 4 条大家都自然做对,**后 3 条才是 agent 悄悄翻车的地方**。

| # | 模式 | 关键点 |
|---|---|---|
| 1 | 稳定的任务入口 | 一条命令/一个 issue 就能启动新 session,不依赖人类手工 onboarding |
| 2 | 清晰的 feature/TODO 列表 | 长任务的 "全局目标" 在仓库里以结构化形式存在 |
| 3 | 增量 commit + 干净仓库 | 每次 session 结束,仓库必须是可编译、可测、可部署的 |
| 4 | 工具使用节制 | 工具越少越好,少到只留"必须的" |
| 5 | 会话之间的交班记录 | 显式 handoff note,而不是把"状态"藏在 conversation history 里 |
| 6 | 自检与自我反思 | Session 结束前 agent 自己打一轮分,标红可疑点 |
| 7 | 可被第三方校验的 artifact | 交付物能脱离当前 agent 独立验证:测试、schema、类型、文档 |

### 1.4 可直接抄的工程结构

- `PROGRESS.md` 或 `plan/` 目录:feature list + 完成状态。
- `HANDOFF.md` 或 `sessions/<n>.md`:每次 session 的交班记录。
- 约定: **每次 session 开始时先读 `HANDOFF.md` 的最后一条,再开始干活**。
- 约定: **仓库 main 必须永远 green**;红就先修 red,再开新任务。

---

## 2. Harness Design for Long-Running Application Development

### 2.1 为什么单 agent 不够

团队发现:对"**既要主观品味(设计好不好看)又要可验证正确性(功能能不能跑)**"的任务,单 agent 自己评价自己会陷在局部最优——它倾向于告诉你"我觉得挺好"。

### 2.2 三分法:Planner → Generator → Evaluator

借鉴 **GAN (Generative Adversarial Networks)** 的思路,换成三个专业化 agent:

- **Planner Agent**
  - 把 product spec 拆成**可处理的小块任务**(tractable chunks)。
  - 输出: feature 列表 + 每 feature 的执行步骤 + 可验证的验收标准。

- **Generator Agent**
  - 实现某个 feature。只写这一块代码 + 对应测试。
  - 每次会话只做一件事,避免跨 feature context 污染。

- **Evaluator Agent**
  - 独立打分。
  - 关键:**先把"好不好"翻译成具体可打分的维度**(配色?可达性?API 设计?错误处理?),避免陷入模糊评价。
  - Evaluator 给出的反馈会被 Generator 拿去修改,直到通过。

### 2.3 两条可迁移的老经验

Anthropic 强调这是延续它之前 harness 工作的两条老经验:

- **把任务分解成 tractable chunks**(planner 做这件事)。
- **用结构化 artifact 在 session 之间传递上下文**(与 Effective Harnesses 一脉相承)。

### 2.4 16 个 Claude 并行做 C 编译器

[Anthropic blog](https://anthropic.com/engineering/building-c-compiler) + [Ars Technica](https://arstechnica.com/ai/2026/02/sixteen-claude-ai-agents-working-together-created-a-new-c-compiler/) 报道的实验,是这套方法论的放大版:

- 16 个 Claude Opus 4.6 并行 agent,跑 2 周。
- 自定义 harness 负责**任务协调、测试、冲突解决**。
- 产出:10 万行 Rust 写的 C 编译器,能编 Linux 6.9 内核,支持 x86 / ARM / RISC-V。
- 总开销 ≈ $20,000。
- 仓库:[anthropics/claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler)。

结论:**harness 足够强时,任务复杂度可以近似"加 agent 就加吞吐"**。

---

## 3. Managed Agents:Decoupling the Brain from the Hands

这是 Anthropic 对 harness engineering **最重要的一次自我警告**。

### 3.1 核心观察

> Harness 会把模型的"当前缺陷"固化成结构。模型升级后,它反而可能变成拖后腿的枷锁。

换句话说:**为 Sonnet 4.5 精心打磨的 harness,用在 Opus 4.6 上可能更差**。[Practice Overflow 的复盘](https://practiceoverflow.substack.com/p/the-harness-got-simpler-and-the-agents) 专门讲过这一幕。

### 3.2 对应的工程解法:把 brain 和 hands 解耦

- **Brain 侧**:模型 + agent loop。随模型换代。
- **Hands 侧**:对外稳定的**接口**——工具注册、权限、上下文协议、artifact 协议。
- **Managed Agents** 给用户暴露的就是这层稳定接口,harness 内部怎么换都行。

### 3.3 对应的新能力("dreaming / outcomes / multi-agent orchestration")

[kenhuangus 的解读](https://kenhuangus.substack.com/p/claude-agents-can-now-dream-how-ai) 总结了 Anthropic 在这个方向上正在做的三件事:

- **Dreaming**:agent 跨 session 归纳经验,沉淀成可复用的"skill / heuristic"。
- **Outcomes**:用户用一个 rubric 定义 "done",**独立的 grader agent 反复修**,直到达标。
- **Multi-agent orchestration**:lead agent 分派给 specialist sub-agent,每个 specialist 有自己的 context、工具、prompt、模型。

这三者其实都是 harness 层的功能,不是模型层。

### 3.4 对团队的启示

- **不要把模型的缺陷焊进 harness**(比如"模型不会用 X,所以我们全局禁止 X"这种补丁)。
- 为 harness 维护一份 **"退役清单"**:哪些约束是为了当前模型?未来可删除?
- 优先做稳定的抽象层(工具签名、权限模型、artifact schema),而不是硬编码流水线。

---

## 4. 三篇合起来看的方法论

1. **Effective Harnesses** 解决**时间维度**:长任务怎么在多 session 之间不失忆。
2. **Harness Design** 解决**结构维度**:复杂任务怎么靠多 agent 分工做得更好。
3. **Managed Agents** 解决**演化维度**:harness 本身如何不老化。

落到一个团队的日常操作:

- 时间维度 → 每个长任务仓库里都有 `plan/`、`sessions/`、`HANDOFF.md`。
- 结构维度 → 重要 feature 默认"planner + generator + evaluator"三件套,哪怕 evaluator 只是一个简短 rubric。
- 演化维度 → 工具、权限、artifact schema 在**独立目录**里维护(如 `.kiro/steering/`),harness 的变化走 PR,留得下审计轨迹。

## 来源索引

- Anthropic:
  - 《Effective harnesses for long-running agents》(https://anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  - 《Harness design for long-running application development》(https://www.anthropic.com/engineering/harness-design-long-running-apps)
  - 《Managed Agents》(https://www.anthropic.com/engineering/managed-agents)
  - 《Long-running Claude for scientific computing》(https://www.anthropic.com/research/long-running-Claude)
  - 《Building a C compiler with a team of parallel Claudes》(https://anthropic.com/engineering/building-c-compiler)
  - 仓库 [anthropics/claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler)
- 第三方:
  - [Ahmed Nadar《7 Patterns》](https://ahmednadar.com/7-patterns-for-long-running-agent-harnesses/)
  - [astromvp《Why Multi-Agent Systems Beat Solo AI Coding》](https://www.astromvp.com/blog/claude-harness-design-long-running-apps)
  - [Practice Overflow《The Harness Got Simpler》](https://practiceoverflow.substack.com/p/the-harness-got-simpler-and-the-agents)
  - [kenhuangus《Claude Agents Can Now Dream》](https://kenhuangus.substack.com/p/claude-agents-can-now-dream-how-ai)
  - [Ars Technica《16 Claude agents C compiler》](https://arstechnica.com/ai/2026/02/sixteen-claude-ai-agents-working-together-created-a-new-c-compiler/)
  - [Anthropic Managed Agents docs](https://platform.claude.com/docs/en/managed-agents/overview)
