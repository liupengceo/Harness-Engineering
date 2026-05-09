# 05 · Martin Fowler 站:harness engineering + on-the-loop

Martin Fowler 和他带的 Thoughtworks 团队在 [Exploring Generative AI](https://martinfowler.com/articles/exploring-gen-ai.html) 这个专栏下,从 2025 年起陆续发了一串 memo,从理论层面给 harness engineering 定了位。这一章挑出四篇最值得读的,做系统整理。

---

## 1.《Harness Engineering – first thoughts》(2026-02-17)

- 原文:https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html

### 核心判断

- Harness 的作用是**把人类工程师的经验显性化、外部化**。
- 但 harness 不可能完全取代人——能做的是**把人的输入引导到最重要的位置**(比如 plan checkpoint、关键架构决策、acceptance 验收)。
- 这句值得记下来:**好 harness 不以"消灭人"为目标,以"优化人的注意力分配"为目标**。

这和 OpenAI 那句 "humans steer, agents execute" 是同一个意思的两种表述。

### 对团队的操作化含义

- 不要把"我们家 agent 全自动化了"当 KPI。
- 要把"**人的时间省在了哪些环节、花在了哪些环节**"当 KPI。

---

## 2.《Humans and Agents in Software Engineering Loops》by Kief Morris(2026-03-04)

- 原文:https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html

### 关键概念:why loop / how loop / on-the-loop

把软件开发拆成两层循环:

- **Why loop(为什么循环)**
  - 迭代的是**想法 ↔ 可工作的软件**。
  - "我们到底想要什么" 这个问题,天然由人类驱动——直到 AI 起义那天。
- **How loop(怎么做循环)**
  - 迭代的是**构建软件过程中的中间 artifact**:代码、测试、工具、基础设施、技术设计、ADR。
  - 是多层嵌套的:最外层是 "交付可工作软件" 的 outer loop,最内层是 "生成 + 跑测试" 的 inner loop,中间是各级任务分解。
  - 这一层**绝大部分工作可以由 agent 接管**。

### 人该站在哪里:on the loop

- 传统讲 human-in-the-loop(在环内)——人要审每一个 artifact。
- Kief Morris 建议:**human-on-the-loop**(在环上)——人**构造并管理这个循环本身**。
- 不是放手不管,也不是微观管产物;是**管循环的结构**:目标、输入规范、验收标准、反馈通道。

### 直接搬来用的姿势

| 工种 | 传统做法 | On-the-loop 做法 |
|---|---|---|
| 产品 | 写需求,等工程交付 | 维护 why loop 的高质量信号:用户反馈、指标、验收标准 |
| 架构师 | 画图 / 做评审 | 维护 how loop 的结构:模块边界、ADR 模板、质量门 |
| 工程师 | 写代码 / review PR | 维护 harness:工具、steering、review persona、测试框架 |
| EM / staff | 管排期 | 管**循环本身的吞吐与信号质量** |

---

## 3.《Harness engineering for coding agent users》(2026-03)

- 原文:https://martinfowler.com/articles/harness-engineering.html

### 切入角度

不是面向"造 harness 的基础设施团队",而是面向**每天用 coding agent 写业务代码的普通工程师**。

### 核心痛点

> 我们和 AI 生成代码之间天然有**信任障碍**(trust barrier)——LLM 非确定、不懂我们的语境、"思考"的是 token 而不是语义。

所以:**要减少对 agent 的监督,就必须提高对它输出的信任**。这就是 harness engineering 存在的意义。

### 作者建议的信任建立路径(改写整理)

1. **缩小任务粒度**:每次让 agent 做"小到容易验证"的一块。
2. **建立 guardrail**:类型、lint、测试、schema、契约。
3. **疯狂文档化**:让 agent 读着文档就能推理出上下文,而不是在意图之间猜。
4. **强制验证**:verified ≠ "我读了",而是 "被某个机械或结构化机制检查过"。

这条"verified"的重新定义在他 2026-04-29 的 [Fragments](https://martinfowler.com/fragments/2026-04-29.html) 被再次强调:

> 当 agent 吞吐这么大时,"verified" 必须是**被测试、被类型、被自动门禁、或在你判断最值钱的地方被你读过**。

---

## 4. 相关系列 memo

一并列在这里,方便你扩展阅读:

- 《LLMs and the what/how loop》(https://www.martinfowler.com/articles/convo-what-how.html)
  - 点名否定 "human-in-the-loop" 这种窄化表述。
  - 指出把"把需求翻译成代码"当软件开发本质是一种误解——真正的本质是**造一个在变化中存活的系统**。
- 《LLMs bring new nature of abstraction》(https://martinfowler.com/articles/2025-nature-abstraction.html)
  - LLM 带来了一种新的抽象方式:从精确 code 到模糊意图。
  - 这种抽象不是更差,只是**另一种**;harness 的职责就是在两种抽象之间搭桥。
- 《How far can we push AI autonomy in code generation?》(http://martinfowler.com/articles/pushing-ai-autonomy.html)
  - Thoughtworks 做过一系列实验,试试看 LLM 能在无人值守下走多远。
  - 实验结论是和 Stripe / OpenAI 一致的:**不是模型极限,是 harness 极限**。
- 《Fragments 2026-04-29》(https://martinfowler.com/fragments/2026-04-29.html)
  - 重申:改动要小、要有 guardrail、要无情地文档化、每次改动都要被验证。

---

## 5. 整合起来的思考框架

把这几篇文章串起来,可以得出一个**给人类工程师**的认知地图:

```
           ┌─────────────────────────┐
  Why loop │  用户 ↔ 指标 ↔ 验收标准   │   ← 人驱动
           └───────────┬─────────────┘
                       │ 目标 / 约束 / 接受度
                       ▼
           ┌─────────────────────────┐
  How loop │  任务分解 → ExecPlan →   │
           │  生成 → 测 → review →   │   ← agent 执行,人类 on-the-loop
           │  修 → 合并               │
           └───────────┬─────────────┘
                       │ 反馈信号
                       ▼
           ┌─────────────────────────┐
  Harness  │  工具 / steering / 验证  │   ← 人设计、agent 自动化运行
           │  / 观测 / persona        │
           └─────────────────────────┘
```

- 人做**目标与约束**,做**harness 设计**。
- Agent 做**how loop** 里 artifact 的生成、组合、测试、评审。
- Harness 是把这两者缝起来的"**针线**"。

## 6. 关于"on-the-loop"的具体工程暗示

从 Kief Morris 的文章落地到日常工作,有几条比较硬的操作建议:

- **要有 plan checkpoint**:在 agent 开动前看 plan 的 diff,远比看 PR 的 diff 便宜。
- **要有 acceptance checkpoint**:在 merge 前,拿 rubric 对照产出,**不是逐行读代码**。
- **要有 harness-change audit**:对 `AGENTS.md`、`.kiro/steering/` 的改动要像对生产代码一样 review。
- **人类注意力要是稀缺的、宝贵的、不可挤占的**:不要让 agent 把"琐事"倒灌回人类手上。

## 来源索引

- Martin Fowler 站:
  - [Harness Engineering – first thoughts](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html)
  - [Humans and Agents in Software Engineering Loops](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html)
  - [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)
  - [LLMs and the what/how loop](https://www.martinfowler.com/articles/convo-what-how.html)
  - [LLMs bring new nature of abstraction](https://martinfowler.com/articles/2025-nature-abstraction.html)
  - [How far can we push AI autonomy in code generation?](http://martinfowler.com/articles/pushing-ai-autonomy.html)
  - [Fragments 2026-04-29](https://martinfowler.com/fragments/2026-04-29.html)
- 配合阅读:[InfoQ《Where Do Humans Fit in AI-Assisted Software Development?》](http://infoq.com/news/2026/03/mf-aiassisted-dev/)
