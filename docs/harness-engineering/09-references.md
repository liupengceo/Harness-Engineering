# 09 · 参考文献与延伸阅读

> 按来源分组。每条尽量给出发布时间与一句话摘要(改写)。实际链接以原站为准。

---

## A. OpenAI 官方

- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — 2026-02 · 本库主篇引用来源。5 个月、100 万行、零手写代码的内部实验报告。
- [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) — 2026-02 · 把 Codex CLI 的 agent loop 当作 "harness" 的具体形态讲清楚。
- [Unlocking the Codex harness: how we built the App Server](https://openai.com/index/unlocking-the-codex-harness/) — 2026 · 把 harness 做成可复用 App Server,同时支撑 CLI / VS Code / Cloud。
- [Introducing Codex](https://openai.com/index/introducing-codex/) — 2025 · Codex 产品首次公开。
- [Building more with GPT-5.1-Codex-Max](https://openai.com/index/gpt-5-1-codex-max/) — 2025 · 背后的模型。
- [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) — 2026 · model-native harness + native sandbox 对外开放。
- [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) — 模式、编排、安全的官方参考。
- [Auto-review of agent actions without synchronous human oversight](https://alignment.openai.com/auto-review/) — OpenAI alignment · auto-review agent 的安全论证。
- [A Practical Approach to Verifying Code at Scale](https://alignment.openai.com/scaling-code-verification/) — 行为监测、激活监测、纵深防御。

---

## B. Anthropic 官方

- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — 2026 · planner / generator / evaluator 三分法。
- [Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents) — 2025 · initializer + coding agent,7 模式。
- [Managed Agents (Decoupling the brain from the hands)](https://www.anthropic.com/engineering/managed-agents) — 2026 · 对 harness 老化的自我警告。
- [Long-running Claude for scientific computing](https://www.anthropic.com/research/long-running-Claude) — 2026 · 把长任务范式迁到科研计算。
- [Building a C compiler with a team of parallel Claudes](https://anthropic.com/engineering/building-c-compiler) — 2026 · 16 个 Claude 并行,2 周,10 万行 Rust C 编译器。
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 2025 · context engineering 的系统论述。
- [Claude Managed Agents docs](https://platform.claude.com/docs/en/managed-agents/overview) — 产品文档。
- 仓库:[anthropics/claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler),[anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript)

---

## C. Stripe

- [Minions: Stripe's one-shot, end-to-end coding agents — Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
- [Minions Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)

---

## D. Shopify

- [Introducing Roast: Structured AI workflows made easy](http://shopify.engineering/introducing-roast)
- 仓库:[Shopify/roast](https://github.com/Shopify/roast)

---

## E. Martin Fowler 站 & Thoughtworks

- [Exploring Generative AI(专栏)](https://martinfowler.com/articles/exploring-gen-ai.html)
- [Harness Engineering — first thoughts](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html) — 2026-02-17
- [Humans and Agents in Software Engineering Loops](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html) — 2026-03-04 · Kief Morris
- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)
- [LLMs and the what/how loop](https://www.martinfowler.com/articles/convo-what-how.html)
- [LLMs bring new nature of abstraction](https://martinfowler.com/articles/2025-nature-abstraction.html)
- [How far can we push AI autonomy in code generation?](http://martinfowler.com/articles/pushing-ai-autonomy.html)
- [Fragments 2026-04-29](https://martinfowler.com/fragments/2026-04-29.html)
- [InfoQ 对该系列的转述《Where Do Humans Fit in AI-Assisted Software Development?》](http://infoq.com/news/2026/03/mf-aiassisted-dev/)

---

## F. 高质量第三方综述与实践

### F.1 方法论 / 综述

- [Tian Pan《The Discipline That Determines Whether Your AI Agents Actually Work》](https://tianpan.co/blog/2026-02-17-harness-engineering-agent-first-software-development)
- [Build This Now《Agent Harness Engineering》](https://www.buildthisnow.com/blog/guide/agents/agent-harness-engineering) — 五控制杆 + 约束悖论。
- [Naoko Reeves《The Harness Engineering Cheat Sheet》](https://naoko.github.io/posts/2026-04-28-harness-engineering-overview/) — 跨 OpenAI / Anthropic / Google / Microsoft / Shopify / Stripe 对比。
- [Cobus Greyling《The Rise of AI Harness Engineering》](https://cobusgreyling.substack.com/p/the-rise-of-ai-harness-engineering)
- [Mohamed Hendawy《From Prompts to Harnesses》](https://mohamed-hendawy.medium.com/from-prompts-to-harnesses-the-three-eras-of-ai-agent-engineering-fbd0e6168b21)
- [Wencheng Zheng《The missing mental model of harness engineering: boundary design》](https://medium.com/@wencheng.zheng_50256/the-missing-mental-model-of-harness-engineering-boundary-design-9d89ad422025)

### F.2 OpenAI 实验转述

- [ignorance.ai《The Emerging "Harness Engineering" Playbook》](https://www.ignorance.ai/p/the-emerging-harness-engineering)
- [The Neuron《Ship 1M Lines of Code w/ Agents》](https://www.theneuron.ai/explainer-articles/openais-harness-engineering-playbook-how-to-ship-1m-lines-of-code-without-writing-any/)
- [akillness《The 5 Rules That Let Agents Ship 1M Lines》](https://akillness.github.io/posts/harness-engineering/)
- [Alex Lavaee《OpenAI's Agent-First Codebase Learnings》](https://alexlavaee.me/blog/openai-agent-first-codebase-learnings)
- [ZenML LLMOps Database · Extreme Harness Engineering](https://www.zenml.io/llmops-database/extreme-harness-engineering-building-production-software-with-zero-human-written-code)
- [daily.dev · Lopopolo 演讲摘要](https://app.daily.dev/posts/harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan-lopopolo-openai-bspqkijzd)
- [Ry Walker《OpenAI Harness Engineering》](https://rywalker.com/research/openai-harness)
- [Onsite Reliability《Harness Engineering》](https://onsitereliability.com/Harness-Engineering/)
- [EQengineered《Key Takeaways》](https://www.eqengineered.com/insights/https/harness-engineering-and-continuous-ai-key-takeaways)
- [Chosun English《Humans Turn to Harness Engineering》](https://www.chosun.com/english/industry-en/2026/03/16/A4WW6USJ2BGVJEGRIPQ5VOUAYA/)
- [InfoQ《OpenAI Introduces Harness Engineering》](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/)
- [abvx substack《The Day Writing Code Became the Least Important Part of Software》](https://abvx.substack.com/p/harness-engineering-the-day-writing)
- [Zak Elfassi《Systems Engineering for the Agentic AI Age》](https://zakelfassi.com/blog/the-harness)

### F.3 Anthropic 实验转述

- [astromvp《Why Multi-Agent Systems Beat Solo AI Coding》](https://www.astromvp.com/blog/claude-harness-design-long-running-apps)
- [Ahmed Nadar《7 Patterns for long-running agent harnesses》](https://ahmednadar.com/7-patterns-for-long-running-agent-harnesses/)
- [Practice Overflow《The Harness Got Simpler and the Agents Got Worse at Teamwork》](https://practiceoverflow.substack.com/p/the-harness-got-simpler-and-the-agents)
- [kenhuangus《Claude Agents Can Now Dream》](https://kenhuangus.substack.com/p/claude-agents-can-now-dream-how-ai)
- [mejba《Anthropic's Agent Harness Design Changed How I Think》](https://www.mejba.me/blog/anthropic-long-running-agent-harness)
- [Ars Technica · 16 Claude agents C compiler](https://arstechnica.com/ai/2026/02/sixteen-claude-ai-agents-working-together-created-a-new-c-compiler/)
- [Better Stack · Multi-Agent AI Development](https://betterstack.com/community/guides/ai/anthropic-ai-agents-c-compiler/)
- [cuizhanming · Agent Teams Deep Dive](https://cuizhanming.com/anthropic-agent-teams-c-compiler/)
- [FAUN · $20,000, 16 AI Agents, and a Compiler That Builds Linux](https://www.faun.dev/co/news/devopslinks/anthropic-claudes-20000-16-ai-agents-and-a-compiler-that-builds-linux/)

### F.4 Stripe / Shopify 实验转述

- [MindStudio《Stripe Minions vs Shopify Roast》](https://www.mindstudio.ai/blog/stripe-minions-vs-shopify-roast-ai-coding-harnesses)
- [MindStudio《Stripe Minions Blueprint Architecture》](https://www.mindstudio.ai/blog/stripe-minions-blueprint-architecture-deterministic-agentic-nodes)
- [MindStudio《What Is AI Agent Harness? Stripe Minions》](https://www.mindstudio.ai/blog/what-is-ai-agent-harness-stripe-minions)
- [MindStudio《How Stripe Ships 1,300 AI PRs a Week》](https://www.mindstudio.ai/blog/what-is-harness-engineering-beyond-prompt-context-engineering)
- [jangwook.net《How a Slack Emoji Triggers 1,300 PRs a Week》](https://jangwook.net/en/blog/en/stripe-minions-autonomous-coding-agents-1300-prs/)
- [daily.dev《Deconstructing Stripe's Minions》](https://app.daily.dev/posts/deconstructing-stripe-s-minions-one-shot-agents-at-scale-lx9tazvft)
- [Geektak《Build Deterministic AI Coding Workflows》](https://www.geektak.com/blog/build-deterministic-ai-coding-workflows-stripe)
- [tessl.io《Roast-ing AI workflows with Ruby》](https://tessl.io/blog/roast-shopify-ai-workflow/)
- [dblock.org《Executing Structured A.I. Workflows with Shopify Roast》](https://code.dblock.org/2025/05/10/executing-structured-ai-workflows-with-shopify-roast.html)
- [Defmethod Podcast · Episode 4](https://www.defmethod.com/podcast/episode-4-roasting-ruby-ai-workflows-with-obie-fernandez)
- [Ry Walker《Shopify Roast 研究》](https://rywalker.com/research/shopify-roast)
- [Ry Walker《Stripe Minions 研究》](https://rywalker.com/research/stripe-minions)
- [Ry Walker《In-House Coding Agents》](https://rywalker.com/research/in-house-coding-agents)

### F.5 实践手册

- [Verdent《Harness Engineering in Practice》](https://www.verdent.ai/fr/guides/harness-engineering-ai-coding-workflow)
- [mer.vin《Harness Engineering with Codex — A Practical Beginner Guide》](https://mer.vin/2026/04/harness-engineering-with-codex-a-practical-beginner-guide-to-human-steered-agent-delivery/)
- [zeik0《Harness engineering for agent-first teams》](https://www.zeik0.com/blog/harness-engineering-openclaw-agent-first-workflows)
- [codescrum《What Is Harness Engineering?》](https://www.codescrum.com/blog/what-is-harness-engineering)
- [Wiselychen《AI Can Write Code, But It Can't Ship to Production on Its Own》](https://en.wiselychen.com/en/harness-engineering-architecture-overview-ai-code-production-guardrails/)
- [Innobu《Agentic Harness Engineering》](https://innobu.com/en/agentic-harness-engineering.html)
- [Fairmind《Harness Engineering consulting》](https://www.fairmind.ai/en/harness-engineering)
- [dsebastien.net《Harness Engineering concept》](https://concepts.dsebastien.net/concept/harness-engineering/)
- [onsitereliability《Harness Engineering》](https://onsitereliability.com/Harness-Engineering/)
- [algorithm.viblo.asia《Harness Engineering Quick Actionable Guide》](https://algorithm.viblo.asia/p/harness-engineering-quick-actionable-guide-Nj4vg86vJ6r)

### F.6 Claude Code 源泄露 & 内部拆解

- [o-mega《Inside Claude Code: Leaked Source Analysis》](https://o-mega.ai/articles/inside-claude-code-the-leaked-source-analysis)
- [apidog《How to Build Your Own Claude Code?》](https://apidog.com/blog/build-your-own-claude-code/)
- [Victor Dibia《Inside Claude Code》](https://newsletter.victordibia.com/p/inside-claude-code)
- [Generative Programmer《12 Agentic Harness Patterns from Claude Code》](https://generativeprogrammer.com/p/12-agentic-harness-patterns-from)
- [redreamality《Lessons from Claude Code's Core Loop》](https://redreamality.com/blog/inside-claude-code-agent-harness/)
- [htdocs.dev《The Claw Code Story — What's the Harness?》](https://htdocs.dev/posts/the-claw-code-story-whats-the-harness)
- [kenhuangus《Claude Code Harness Pattern 8 · Memory》](https://open.substack.com/pub/kenhuangus/p/claude-code-harness-pattern-8-memory)
- [kenhuangus《Claude Code Harness Pattern 9 · Observability》](https://kenhuangus.substack.com/p/claude-code-harness-pattern-9-observability)

### F.7 学术与开源脚手架

- [arXiv《Observability-Driven Automatic Evolution of Coding-Agent Harnesses》](https://arxiv.org/html/2604.25850v1)
- [arXiv《A Unified Review of Memory, Skills, Protocols and Harness Engineering》](https://arxiv.org/html/2604.08224)
- [arXiv《The Last Harness You'll Ever Build》](https://arxiv.org/abs/2604.21003)
- [GitHub · walkinglabs/awesome-harness-engineering](https://github.com/walkinglabs/awesome-harness-engineering)
- [GitHub · broomva/harness-engineering-skill](https://github.com/broomva/harness-engineering-skill)
- [GitHub · ZhangHanDong/harness-engineering-from-cc-to-ai-coding](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding/actions)
- [GitHub · ninjaa/openai-codex-exec-plan](https://github.com/ninjaa/openai-codex-exec-plan)
- [GitHub · OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files)
- [GitHub · HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness)
- [GitHub · keli-wen/agentic-harness-patterns-skill](https://github.com/keli-wen/agentic-harness-patterns-skill/)
- [GitHub · affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)
- [GitHub · revfactory/harness](https://github.com/revfactory/harness)
- [GitHub · deusyu/harness-engineering](https://github.com/deusyu/harness-engineering/blob/main/README.en.md)
- [Claude Plugin Hub · claude-harness-loop](https://www.claudepluginhub.com/plugins/jfk-claude-harness-loop)
- [Claude Plugin Hub · cc-harness-marketplace](https://www.claudepluginhub.com/marketplaces/jinsong-zhou-cc-harness-marketplace)

### F.8 对抗面:反思与警示

- [Salesforce《Applied AI: Why Building AI Agents Requires a New Playbook》](https://www.salesforce.com/news/stories/applied-ai-building-agents-playbook/)
- [Daniel Keller《Leading AI Is an Empowerment Problem》](https://danielkeller.com/tech/leading-ai-empowerment/)
- [Anthropic · Auto-review](https://alignment.openai.com/auto-review/)(已列)
- [Nate Newsletter · Get the Cheat Code on Long-Running AI Agents](https://natesnewsletter.substack.com/p/i-read-everything-google-anthropic)
- [The Sequence《Harness — The Operating System for Agentic Software》](https://thesequence.substack.com/p/the-sequence-opinion-844-harness)

---

## 合规说明

本精读库所有内容均为**跨源交叉整理后的改写与总结**,避免任何单一来源的大段逐字引用。如需权威原文,请以上述官方站点为准。
