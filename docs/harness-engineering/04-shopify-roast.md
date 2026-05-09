# 04 · Shopify Roast:约定优先的 AI 工作流编排

> 原文:[Shopify Engineering《Introducing Roast》](http://shopify.engineering/introducing-roast)
> 仓库:[Shopify/roast](https://github.com/Shopify/roast)
> 外部解读:[tessl.io](https://tessl.io/blog/roast-shopify-ai-workflow/) · [Ry Walker 研究](https://rywalker.com/research/shopify-roast) · [MindStudio Stripe vs Shopify](https://www.mindstudio.ai/blog/stripe-minions-vs-shopify-roast-ai-coding-harnesses)

## 1. Roast 是什么

由 Shopify Augmented Engineering 团队维护的 **Ruby gem**,**不是一个完整 agent**,而是一个"**约定优先的 AI 工作流编排框架**"。

定位非常明确:**你继续用你原有的工程流水线,我负责把 LLM 调用整整齐齐嵌进去**。

## 2. 三个核心原语

来自 [tessl.io 的整理](https://tessl.io/blog/roast-shopify-ai-workflow/):

| 原语 | 角色 |
|---|---|
| **Step** | 单个工作单元。可以是普通 Ruby 代码,可以是 LLM 调用,可以是 shell 命令,可以是调用一个 coding agent。 |
| **Plan** | 一串 step 的**固定顺序**,带配置。 |
| **Run** | 带状态的一次执行。产出日志、中间 artifact、最终结果。 |

这意味着你**不用**为 AI 重新发明一套编排框架;你用已经习惯的"step/plan"抽象,把 AI 当成一种可插拔 executor 就行。

## 3. 关键判断:交织,而不是"AI 负责全部"

> Roast 的原话被多处引用为:**convention-oriented workflow orchestration framework designed specifically for creating structured AI workflows that interleave non-deterministic AI behavior with normal non-AI code execution.**

翻译过来的关键词:

- **convention-oriented**:靠约定(目录、文件名、配置键)而不是大而全的 API。
- **interleave**:AI 步骤和非 AI 步骤**混编**,不是"AI 包圆"。
- **structured**:流程可读、可重入、可审计。

## 4. 典型用法

[dblock.org 的例子](https://code.dblock.org/2025/05/10/executing-structured-ai-workflows-with-shopify-roast.html) 显示 Roast 常被用于内部开发者生产力场景:

- **flaky test 自动修**:找出最近不稳定的测试 → LLM 给方案 → 跑补丁 → 复测 → 开 PR。
- **低测试覆盖改善**:扫描高风险文件 → LLM 写测试 → 运行 → 合并。
- **代码 review 辅助**:LLM 做初评 → 真人仅看被标红处。
- **架构扫描**:LLM 扫某个目录并输出架构摘要。

共同模式都是:**agent 是水管里的一段 valve,不是水源**。

## 5. 与 Stripe Minions 的并列对比

[MindStudio《Stripe Minions vs Shopify Roast》](https://www.mindstudio.ai/blog/stripe-minions-vs-shopify-roast-ai-coding-harnesses) 把两者放一起做了对比,总结如下(有我自己的改写):

| 维度 | Stripe Minions | Shopify Roast |
|---|---|---|
| 粒度 | 端到端产出 PR | 某个工作流里的一段 step |
| 核心目的 | 单任务"人最少介入"的最大吞吐 | 把 AI **嵌进既有流水线**,不改变工作方式 |
| 形态 | 内部产品 + SRE 级基础设施 | 开源 Ruby gem |
| 典型用户 | Stripe 内部 eng | 任何一个想把 LLM 编进 CI 的团队 |
| 约束风格 | Blueprint = 控制 agent 的状态机 | Plan = step 有序组合,每个 step 自治 |

一个团队其实**两种都可以存在**:顶层是 "Roast 式" 编排,低层某些节点是 "Minion 式" one-shot agent。

## 6. 从 Roast 学到的可直接搬的 3 件事

1. **先声明 step,再决定用不用 LLM**
   - 每个 step 都应该能被替换成 "非 LLM 实现"。
   - 如果不能,说明你把 agent 用在了不该用的地方。
2. **约定 > 配置**
   - Roast 式的文件布局(`workflows/`, `steps/`, `plans/`)意味着 agent 读代码 30 秒就能参与。
   - 不要把工作流塞成一个 YAML 大泥球。
3. **state is not conversation**
   - Run 的状态要显式写进 artifact,不依赖 conversation history。
   - 这样任何一个 agent 都能随时接手一个 Run,而不需要翻前文。

## 7. 两个可引用的启示

- **Harness engineering 不等于"造一个新 framework"**,很多时候是**把 LLM 装进已有 framework 的对应位置**——这可能比"自研 agent 框架"成本低一个数量级。
- **Ruby / Rails / Django / Spring 这些成熟生态的 convention over configuration 思想,对 agent-first 开发仍然适用**。在这个意义上,Roast 是对"造概念"派的一个温和修正。

## 来源索引

- Shopify:《Introducing Roast》(http://shopify.engineering/introducing-roast)
- 仓库:[Shopify/roast](https://github.com/Shopify/roast)
- [tessl.io《Roast-ing AI workflows with Ruby》](https://tessl.io/blog/roast-shopify-ai-workflow/)
- [Ry Walker《Shopify Roast 研究》](https://rywalker.com/research/shopify-roast)
- [MindStudio《Stripe Minions vs Shopify Roast》](https://www.mindstudio.ai/blog/stripe-minions-vs-shopify-roast-ai-coding-harnesses)
- [dblock.org《Executing Structured A.I. Workflows with Shopify Roast》](https://code.dblock.org/2025/05/10/executing-structured-ai-workflows-with-shopify-roast.html)
- [Defmethod Podcast EP 4](https://www.defmethod.com/podcast/episode-4-roasting-ruby-ai-workflows-with-obie-fernandez)
- [ZenML《Shopify Structured AI Workflow Orchestration》](http://www.zenml.io/llmops-database/structured-ai-workflow-orchestration-for-developer-productivity-at-scale)
