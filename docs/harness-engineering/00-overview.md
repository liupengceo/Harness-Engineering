# 00 · 总览:Harness Engineering 是什么

> 这是精读库的主篇,后续每一章都是对这里某个段落的放大。

## 1. 一个公式 + 一个判断

**公式**:

```
Agent = Model + Harness
```

- **Model**:大模型本身(GPT-5.x、Claude Opus、Gemini…),负责 token 级的推理。
- **Harness**:除模型以外的一切——工具注册表、沙箱、权限、上下文管理、反馈回路、文档、评审 agent、观测、评测。

**判断**(在 OpenAI、Anthropic、Build This Now handbook、Martin Fowler 站等多篇文章里反复出现):

> 真正决定 agent 在生产环境表现的,是 harness,不是模型。

一个典型反例(来自 [Build This Now](https://www.buildthisnow.com/blog/guide/agents/agent-harness-engineering) 的整理):
同一个模型下,**把 agent 能用的工具从 15 个砍到 1 个 bash**,准确率从 80% 跳到 100%,token 消耗还下降 37%。模型没变,是 harness 变了。

## 2. 名字怎么来的

"Harness" 原本是**测试脚手架**(test harness)的术语——输入夹具、输出捕获、断言、前置/后置条件,围绕被测对象做一整套控制。

把同一个词迁到 agent 上:**模型是被"夹住"的那一部分,harness 是夹它的那套东西**。

OpenAI 在 [Harness engineering](https://openai.com/index/harness-engineering/) 里把这个名字正式带进行业词汇。它还在姊妹篇 [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) 里把 agent 的 loop 本身就直接叫"harness",强调它是 "model ↔ tools ↔ user" 三方编排的核心。

## 3. OpenAI 五个月实验的关键数字

来源:[OpenAI 原文](https://openai.com/index/harness-engineering/) 与 [ZenML 总结](https://www.zenml.io/llmops-database/extreme-harness-engineering-building-production-software-with-zero-human-written-code)。

| 指标 | 数值 |
|---|---|
| 周期 | 约 5 个月(2025-08 末到 2026-02) |
| 团队规模 | 3 人 → 7 人(变大后吞吐**不减反增**) |
| 产出代码 | 约 100 万行 |
| 合入 PR | 约 1,500 个 |
| 每人每天 PR | 3.5 个(部分场景 5–10) |
| 每日 token 消耗 | 约 10 亿 |
| 人工编码比值 | 估算约为手工的 1/10 |
| 手写代码 | **0 行**(包括脚手架、CI、AGENTS.md) |

## 4. 核心心法

来自多篇文章的共同表述,改写整理:

- **Humans steer. Agents execute.**
  人类设计环境、声明意图、搭反馈回路;agent 负责动手写代码。
- **Fix the harness, not the output.**
  当 agent 犯错,不是去改它那一次的产物,而是问:harness 里缺了什么?然后把修复沉淀回 harness。
- **Agent legibility > human readability.**
  代码结构优化给 agent 看(命名、目录、错误消息、schema),而不只是给人看。
- **Repo is the single source of truth.**
  藏在 Slack、Google Docs、人脑里的知识对 agent 不可见 = 不存在。所有决策落地成 markdown、schema、执行计划。
- **On the loop, not in the loop.**
  ([Kief Morris / Martin Fowler 站](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html)) 人类不是每一条 artifact 都读,是**构造并管理那个循环**。

## 5. Harness 的五个控制杆

综合 [Build This Now](https://www.buildthisnow.com/blog/guide/agents/agent-harness-engineering)、[tianpan.co](https://tianpan.co/blog/2026-02-17-harness-engineering-agent-first-software-development) 以及 OpenAI/Anthropic 的论述,可以把 harness 拆成五类可调项:

1. **工具层(Tools)**:agent 能触达什么工具?工具签名、权限、返回结构是否清晰?
2. **上下文层(Context)**:给它塞什么、怎么塞?是按任务按需注入,还是塞一个大而全的 system prompt?
3. **错误层(Errors)**:失败信号以什么形式回传?是面向人类的堆栈,还是 agent 可直接消费的结构化信号?
4. **验证层(Verification)**:输出怎么被检查?测试、类型、lint、CI、runtime metrics、auto-review agent 都是这一层。
5. **权限/范围层(Permissions)**:agent 能触达哪些资源?文件系统、网络、凭证、外部 API?

配一条经验性反直觉的观察:**约束悖论(constraint paradox)** —— 更严的约束、更少的工具,往往带来**更高**的成功率,不是更低。

## 6. 核心架构模式一览

不同玩家在做同一件事,可以放在一张表里对照:

| 玩家 | 形态 | 关键词 |
|---|---|---|
| OpenAI | 长任务编排 + 每任务 worktree + 每日十亿 tokens | "Harness engineering" / AGENTS.md / ExecPlan |
| Anthropic(长任务) | initializer → coding(每 session 增量,写 handoff) | 交班记录 / artifact 持久化 |
| Anthropic(复杂任务) | planner → generator → evaluator 三分法 | GAN 式 generator / evaluator |
| Anthropic(平台) | Managed Agents:brain ↔ hands 解耦 | 接口稳,harness 内部可迭代 |
| Stripe | Minions:ticket → one-shot → PR | 确定性 + agentic 节点混编 / devbox 10 秒启动 |
| Shopify | Roast:step/plan/run 三原语,LLM 与工具都是可插拔 executor | 约定优先的工作流编排 |
| Martin Fowler 站 | why loop / how loop / on-the-loop | 人类治理循环本身 |

详见第 01–05 章。

## 7. 反例与警告

来自 Anthropic 的自我复盘([《Managed Agents》](https://www.anthropic.com/engineering/managed-agents) + [Practice Overflow 复盘](https://practiceoverflow.substack.com/p/the-harness-got-simpler-and-the-agents)):

> Harness 会把模型"此刻的缺陷"烤硬进自己的结构。模型升级后,它可能反而变成瓶颈。

所以高阶建议是:
- **把 harness 做成稳定接口,而不是硬编码流程**(brain ↔ hands 解耦)。
- 为 harness 设"退役路径":哪些限制是为了当前模型的,模型升级后应当删掉哪些。
- 不要把 prompt 补丁当 harness 的主体。

## 8. 这份文档库之后的展开

- 想看每家的具体做法 → 01–05 章。
- 想理解底层方法论 → 06 章。
- 想在自己项目里落地一份最小可用版 → 07 章 + 仓库根的 `AGENTS.md`、`.kiro/steering/harness.md`、`templates/ExecPlan.md`。

## 来源索引

- OpenAI:《Harness engineering》(https://openai.com/index/harness-engineering/),《Unrolling the Codex agent loop》(https://openai.com/index/unrolling-the-codex-agent-loop/),《Unlocking the Codex harness》(https://openai.com/index/unlocking-the-codex-harness/)
- Anthropic:《Harness design for long-running application development》(https://www.anthropic.com/engineering/harness-design-long-running-apps),《Effective harnesses for long-running agents》(https://anthropic.com/engineering/effective-harnesses-for-long-running-agents),《Managed Agents》(https://www.anthropic.com/engineering/managed-agents)
- Stripe:《Minions》Part 1/2(https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
- Shopify:《Introducing Roast》(http://shopify.engineering/introducing-roast)
- Martin Fowler 站:《Harness Engineering - first thoughts》(https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html),《Humans and Agents in Software Engineering Loops》(https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html)
- 第三方综合:[Build This Now](https://www.buildthisnow.com/blog/guide/agents/agent-harness-engineering),[ZenML LLMOps](https://www.zenml.io/llmops-database/extreme-harness-engineering-building-production-software-with-zero-human-written-code),[Tian Pan](https://tianpan.co/blog/2026-02-17-harness-engineering-agent-first-software-development),[Naoko Reeves Cheat Sheet](https://naoko.github.io/posts/2026-04-28-harness-engineering-overview/)
