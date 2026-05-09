# Harness Engineering 中文精读库

> 面向 **agent-first 软件开发**的中文知识库。内容综合 OpenAI、Anthropic、Stripe、Shopify、Martin Fowler 站等多方公开资料,整理为可工程落地的笔记、方法论与实践清单。

## 这是什么

**Harness Engineering(马具工程)** 是 2026 年前后在 OpenAI、Anthropic、Stripe、Shopify 等公司内部几乎同时出现的一个新工程学科。它的核心判断是:

> **Agent = Model + Harness**
>
> 决定一个 AI coding agent 在生产环境能不能稳定干活的,不是模型本身,而是**模型外面那一整套脚手架**——工具注册表、沙箱、权限、上下文生命周期、反馈回路、文档基建、架构不变式、观测与评测循环。

把"马具"(harness)做好,一个普通模型也能在长任务里跑出高质量结果;马具缺位,再强的模型也会在真实代码库里翻车。

## 目录

| # | 文件 | 主题 |
|---|---|---|
| 00 | [overview.md](./00-overview.md) | 总览:Harness Engineering 是什么 / 为什么 / 关键数据 |
| 01 | [openai-harness.md](./01-openai-harness.md) | OpenAI《Harness engineering: leveraging Codex in an agent-first world》精读 |
| 02 | [anthropic-harness.md](./02-anthropic-harness.md) | Anthropic 三篇:Harness design / Effective harnesses / Managed Agents |
| 03 | [stripe-minions.md](./03-stripe-minions.md) | Stripe Minions:one-shot end-to-end coding agents |
| 04 | [shopify-roast.md](./04-shopify-roast.md) | Shopify Roast:约定优先的 AI 工作流编排 |
| 05 | [martin-fowler.md](./05-martin-fowler.md) | Martin Fowler 站:harness engineering + on-the-loop |
| 06 | [methodology.md](./06-methodology.md) | 方法论:Agent=Model+Harness、5 个控制杆、约束悖论、harness 老化 |
| 07 | [practice-checklist.md](./07-practice-checklist.md) | 实践清单:从零开始搭一套最小可用 harness |
| 08 | [glossary.md](./08-glossary.md) | 术语表(中英对照) |
| 09 | [references.md](./09-references.md) | 参考文献与延伸阅读 |

## 如何使用这份精读库

- **只有 30 分钟**:读 [00-overview](./00-overview.md)。
- **想落地到团队**:读 [07-practice-checklist](./07-practice-checklist.md) + [06-methodology](./06-methodology.md),然后结合本仓库根目录下的 `AGENTS.md` 与 `.kiro/steering/` 配置。
- **给一线工程师宣讲**:顺序读 00 → 01 → 05 → 06 → 07。
- **给基础设施/平台团队**:顺序读 00 → 01 → 02 → 03 → 06。
- **写文章/内部纪要做引用**:从 [09-references](./09-references.md) 反查原文链接。

## 使用约定

- 所有条目**以改写/总结为主**,单一来源的逐字引用控制在 30 词以内。
- 每份笔记末尾都给出 **来源链接**,以便你自行回查原文。
- 数字(行数、PR 数、成本等)均以公开资料为准,且标注来源。
- 本库不是原文的替代品,是"**跨源交叉整理**"过的脚手架。
