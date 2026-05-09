# 08 · 术语表(中英对照)

> 按字母顺序。每条给出中文常见译法、英文定义要点、代表出处。

| 英文 | 常见译法 | 含义与出处 |
|---|---|---|
| **Acceptance Criteria** | 验收标准 | 机器可验证、或有明确 rubric 的通过条件。Stripe Minions / Verdent 都强调这是 ExecPlan 的必需字段。 |
| **Agent** | 智能体 | 一个能感知环境、选择动作、产生副作用的系统。工程上常写作 "Agent = Model + Harness"。 |
| **Agent Legibility** | 面向 agent 的可读性 | 代码与文档的首要读者是 agent,而非只是人类。OpenAI 博客反复强调。 |
| **AGENTS.md** | 仓库级 agent 约束 | 放在仓库根的规则文件,告诉任何来访 agent "在这里该怎么干活"。OpenAI Codex 默认识别这个文件。 |
| **Artifact** | 中间产物 | 代码、测试、文档、plan、handoff 都算 artifact。Kief Morris 在 "how loop" 里强调它们是"手段",不是目的。 |
| **Auto-review** | 自动评审 | 用一个独立 agent 批准/拒绝另一个 agent 的越界动作。来自 OpenAI alignment 博客。 |
| **Blueprint** | 蓝图(Stripe 语境下) | Stripe Minions 用来编排 "deterministic + agentic 节点" 的状态机式结构。 |
| **Brain ↔ Hands Decoupling** | 脑—手解耦 | 把模型(brain)与工具执行(hands)分离,让 harness 在模型迭代中保持接口稳定。Anthropic《Managed Agents》。 |
| **Context Engineering** | 上下文工程 | 决定**哪些 token 何时进 prompt**。位于 prompt engineering 和 harness engineering 之间。 |
| **Context Window** | 上下文窗口 | 模型一次调用能看到的 token 上限。长任务失忆的根本原因。 |
| **Constraint Paradox** | 约束悖论 | 更严的约束、更少的工具往往带来**更高**的成功率。来自 Build This Now handbook 的观察。 |
| **Deprecation List** | 退役清单 | 标注 "哪些 harness 约束只是为了对抗当前模型的缺陷",便于未来删除。 |
| **Devbox** | 开发沙箱 | Ephemeral VM / container,每任务一盘"干净电脑"。Stripe 基准是 10 秒启动。 |
| **Determinism Layer** | 确定性层 | Blueprint 里写死的、非 LLM 节点。保证流水线的可审计性。 |
| **ExecPlan** | 执行计划 | 在写代码前先产出的结构化 plan:impact map、步骤、验收标准。 |
| **Evaluator Agent** | 评估智能体 | 三分法架构中的一员,专门"把模糊判断翻译成可打分维度"。Anthropic《Harness design》。 |
| **Feedback Loop** | 反馈回路 | 单任务内 / PR 门禁 / 生产三层。所有 harness 文献的共同关注点。 |
| **Generator Agent** | 生成智能体 | 三分法中的实现者。一次只做一个 chunk。 |
| **Handoff Note** | 交班记录 | 长任务 session 之间的显式状态传递。对应 `HANDOFF.md`。 |
| **Harness** | 马具 / 脚手架 | 模型外围的一整套系统(工具、沙箱、记忆、反馈、观测、评测、编排)。来自 OpenAI 2026-02 博客。 |
| **Harness Engineering** | 马具工程 | 上述 harness 的设计与迭代工作。是新的工程学科。 |
| **Human-in-the-loop** | 人在环内 | 人参与每一条 artifact 的审核。Martin Fowler 站认为这是被窄化的说法。 |
| **Human-on-the-loop** | 人在环上 | 人构造并管理循环本身,而非逐条审查产物。Kief Morris 的提法。 |
| **Impact Map** | 影响面图 | 在 ExecPlan 里列出"这次改动会动到哪些文件/符号/接口"。Verdent 强调为第 1 步。 |
| **Initializer Agent** | 初始化智能体 | Anthropic《Effective Harnesses》中的角色:只在第一次 session 搭环境,不参与后续增量开发。 |
| **Legibility** | 可读性 | 这里指"对 agent 的可读性",不同于传统 human readability。 |
| **Long-running Agent** | 长任务智能体 | 跨多 session、可能几天甚至几周的 agent。需要 "记忆三件套"。 |
| **Managed Agents** | 托管智能体 | Anthropic 的平台化方案,通过稳定接口对抗 harness 老化。 |
| **Minion** | 迷你工(Stripe 语境下) | Stripe 的 one-shot end-to-end coding agent;每周产出 ~1,300 PR。 |
| **One-shot Agent** | 一击式智能体 | 单次 LLM 调用完成端到端任务;靠 context engineering,不靠 loop。 |
| **On-the-loop** | 在环上 | 见 Human-on-the-loop。 |
| **Persona (Review Persona)** | 评审人设 | 评审 agent 扮演的关注面角色:Security / Performance / API / Testing / Observability / Docs…… |
| **Planner Agent** | 规划智能体 | 三分法中的任务分解者。输出 feature 列表 + acceptance。 |
| **Plan Checkpoint** | Plan 审查点 | 人类在代码生成前先审 ExecPlan。比 PR 级审查便宜一个数量级。 |
| **Prompt Engineering** | 提示工程 | 对单次 LLM 调用的 prompt 做优化。Harness engineering 的子集。 |
| **Repo-as-Source-of-Truth** | 仓库即真相源 | 所有决策沉到仓库内的文件,藏在其他地方的知识 = 不存在。 |
| **Retire / Deprecation** | 退役 | Harness 条目的生命周期管理。 |
| **Roast** | Shopify 开源工作流编排 Ruby gem。 |
| **Sandbox** | 沙箱 | 隔离的执行环境。与 devbox 常被互换使用。 |
| **Session** | 会话 | 长任务 agent 的一次独立执行上下文。每次 session 是一盘新棋。 |
| **Spec** | 规范 | ExecPlan 的上游物:需求、接口、acceptance 的结构化表达。 |
| **Steering** | 指引 | 像 Kiro / AGENTS.md 那样,给 agent 提供"这里怎么干"的永久性规则。对应 `.kiro/steering/`。 |
| **Tool Registry** | 工具注册表 | 可调用工具的清单 + 签名 + 权限。 |
| **Trust Barrier** | 信任障碍 | 人类与 AI 代码之间的天然屏障。Harness 存在的理由。Martin Fowler 站。 |
| **Verified** | 已验证 | Martin Fowler 2026 版新定义:**被测试 / 被类型 / 被自动门禁 / 或在你判断最值钱处被你读过**。不再等于"我读过了"。 |
| **Why loop / How loop** | 为什么循环 / 怎么做循环 | Kief Morris 的两层循环模型。Why 由人驱动,How 由 agent 执行。 |
| **Worktree** | 工作树(git) | 每任务一个 worktree,为并行隔离服务。OpenAI 博客强调。 |

## 几个易混概念的快速对比

- **Prompt engineering vs Context engineering vs Harness engineering**
  - Prompt:一次对话的文字。
  - Context:对话里喂了哪些 token,什么时候喂。
  - Harness:整套系统。
  - 三者包含关系: harness ⊃ context ⊃ prompt。

- **One-shot Agent vs Long-running Agent**
  - One-shot:1 次调用搞定,靠 context。
  - Long-running:多 session,靠记忆三件套。
  - 同一团队里两者可共存。

- **Human-in-the-loop vs Human-on-the-loop**
  - In-the-loop:人审核每一条 artifact。
  - On-the-loop:人管循环本身(目标、规范、验收、harness)。

- **Deterministic Node vs Agent Node**(Blueprint 语境)
  - Deterministic:写死代码,100% 可预测。
  - Agent:LLM 调用,概率性。
  - 混编出来的流水线是可控 agentic workflow。
