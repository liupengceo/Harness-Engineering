# 01 · OpenAI《Harness engineering: leveraging Codex in an agent-first world》精读

> 原文:[https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)
> 配套姊妹篇:[《Unrolling the Codex agent loop》](https://openai.com/index/unrolling-the-codex-agent-loop/)、[《Unlocking the Codex harness》](https://openai.com/index/unlocking-the-codex-harness/)

## 1. 实验背景

- **时间**:2025 年 8 月下旬起,5 个月。
- **团队**:Frontier Product Exploration 团队,3 人起步,扩到 7 人;演讲人 Ryan Lopopolo。
- **任务**:从空 git 仓库起,做一个面向内部 daily user + 外部 alpha 用户的 **Electron 桌面产品**。
- **硬约束**:**0 行手写代码**。连目录结构、CI、lint、包管理器、AGENTS.md 自身都由 Codex 生成。

## 2. 关键数字

| 指标 | 数值 |
|---|---|
| 总代码 | 约 100 万行 |
| 合入 PR | 约 1,500 |
| 人效 | 平均 3.5 PR/人/天,峰值 5–10 |
| 日 tokens | 约 10 亿 |
| 人效估算 | 约为手写的 10× |
| 团队变化 | 3 → 7,吞吐**随人数线性甚至超线性增长** |

## 3. 中心论点

### 3.1 Humans steer, agents execute

团队把"人做什么、agent 做什么"彻底颠倒:
- 人不再写代码,也不再逐行 review。
- 人**设计环境、声明意图、搭反馈回路**。
- Agent 负责全部代码——应用逻辑、测试、CI、文档、观测、内部工具全是 Codex 写的。

### 3.2 真正稀缺的资源是人的时间与注意力

Harness 的目标就是围绕这个稀缺资源做最大化:
- 不要让人做 agent 能做的事(写样板代码、查文档、跑命令)。
- **让 agent 做能做的所有事**,把人的注意力聚焦在不可替代处:意图澄清、架构决策、关键评审节点。

### 3.3 "修 harness,不是修产物"

这是文章被反复引用的一句反射动作:

> 当 agent 犯错,不要自己上手改这一次。
> 问:**缺了什么能力? 怎么让这件事对 agent 变得 legible + enforceable?**
> 然后把修复沉淀回 harness。

## 4. 七个在文章里反复出现的工程实践

> 下面各条综合了原文与多篇高质量转述([akillness](https://akillness.github.io/posts/harness-engineering/)、[alexlavaee](https://alexlavaee.me/blog/openai-agent-first-codebase-learnings)、[ignorance.ai](https://www.ignorance.ai/p/the-emerging-harness-engineering)、[daily.dev 摘录](https://app.daily.dev/posts/harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan-lopopolo-openai-bspqkijzd))。

### 4.1 Repo-as-Source-of-Truth

- 所有决策 → 沉到仓库的 markdown / schema / execution plan。
- 藏在 Slack、Google Docs、脑子里的知识对 agent **不存在**。
- 连 AGENTS.md 都是 agent 自己写的——但人必须能对它做有意义的 diff review。

### 4.2 Agent Legibility(面向 agent 的可读性)

- 目录结构、命名、错误消息、注释密度,**首要读者是 agent**。
- 一个错误消息应该能直接指导 agent 下一步修什么,而不是让 agent 去反猜。
- Schema 比自由文本强:能用 JSON schema / TypeScript type 的地方都别写 "自然语言规范"。

### 4.3 Spec 先行 + ExecPlan

- 不直接丢一句 "add feature X" 让它开写。
- 先让 agent 产出 **结构化规范**(文件路径、复用模式、影响面、acceptance criteria),然后产出 **ExecPlan**(分步执行计划)。
- **人类在 plan 阶段做 checkpoint**:在 3 行 plan 上抓住错误假设,比在 800 行 PR 里抓要便宜一个数量级。

### 4.4 Just-in-Time Context

- **Context 是最稀缺的 token**。
- 一个臃肿的 system prompt 会挤掉"任务本身 + 代码 + 相关文档"的空间。
- 做法是**按任务按需拉取**:impact map、相关文件片段、相关 ADR / spec,现查现喂。

### 4.5 Parallel + Isolated Sandboxes

- 每个任务 = 一个独立的 `git worktree` + 独立沙箱。
- Logs / metrics / observability 都是**每 worktree 临时起**(ephemeral)。
- 这样多个 agent 可以并行开工,工程师变成 "staff-level orchestrator",每人同时带 3–10 个任务。

### 4.6 Agent-to-Agent Review

- 不再要求同步人工 review。
- 用**带 persona 的 review agent**(安全、性能、API 设计、可观测性…每个 persona 关注一块)做第一道评审。
- 人只在 persona 间意见冲突、或者 stakes 很高的场景介入。
- OpenAI alignment 团队的 [auto-review](https://alignment.openai.com/auto-review/) 文章是这套机制的安全论证:**单独一个 agent 批准/拒绝越界动作**,作为安全默认。

### 4.7 修 Harness 不修单次输出

- 同一类错误第二次出现时,**不是再 prompt 一遍**,而是:
  - 加 schema / 加类型约束 / 加单元测试 / 加 lint 规则 / 加一条 AGENTS.md / 加一个 review persona / 加一个工具。
- 目标:**让这类错误从源头不可能再发生**。

## 5. 流程示意(复刻版)

```
┌────────────────────────────────────────────────────────────────┐
│  Human: 提出意图  →  澄清需求  →  plan checkpoint  →  grade 最终结果 │
└──────────────▲─────────────────────────────────────▲───────────┘
               │                                     │
               │ 约束 / 规范                          │ acceptance
               ▼                                     │
┌────────────────────────────────────────────────────────────────┐
│  AGENTS.md  +  .kiro/steering/*.md                              │
│  (仓库级 harness)                                                │
└───────┬──────────────────────────────────────────────────┬─────┘
        │ 按需注入                                          │
        ▼                                                  ▼
  ┌────────────┐   impact map   ┌────────────┐    tools   ┌────────┐
  │  Planner   │ ─────────────> │  ExecPlan  │ ─────────> │ Coding │
  │   Agent    │                │ (markdown) │            │ Agent  │
  └────────────┘                └────────────┘            └───┬────┘
                                                              │
                                                              ▼
                                                        ┌───────────┐
                                                        │  Tests /  │
                                                        │   Lint /  │
                                                        │    CI     │
                                                        └─────┬─────┘
                                                              │
                                                              ▼
                                                        ┌───────────┐
                                                        │  Review   │
                                                        │  Persona  │
                                                        │  Agents   │
                                                        └─────┬─────┘
                                                              │
                                                              ▼
                                                          PR → Merge
```

每一步都可以**被一个或多个 agent** 跑。人的注意力被聚焦在图上画粗框的两处:**plan checkpoint** 与 **acceptance 验收**。

## 6. Codex 的 "Harness 即 App Server"

姊妹篇 [Unlocking the Codex harness](https://openai.com/index/unlocking-the-codex-harness/) 展示了 OpenAI 怎么把 harness 从 CLI 升到一个 App Server,让它同时支撑 CLI / VS Code / Cloud 三种 surface:

- 比 request/response 更丰富的交互模式:**workspace 探索、推理进度流式、diff emit**。
- Harness 承担 agent 与模型之间的长时编排,上层只暴露"语义事件"。

这等于把 harness 本身也做成了**可复用的基础设施**,而不是一次性脚本。

## 7. 从这篇文章直接能落地的 10 件事

1. 建仓库时先让 agent 自己写 `AGENTS.md` 草稿,再由人精读定版。
2. 任务粒度以 **"一个 PR"** 为单位,在 issue 上就写清 acceptance。
3. 所有任务必须先出 `ExecPlan.md`,PR 里带上 plan 的 diff。
4. 每个任务跑在独立 worktree / devbox 里,观测栈随之启停。
5. 给 agent 的工具"**减法优先**":能用 bash + fs + grep + run_tests 就别再加。
6. 错误消息面向 agent:机器可解析 + 给下一步建议。
7. 把 Slack/Docs 上的协议全部迁到仓库的 markdown。
8. 代码 review 用 persona 化的 agent 先过一轮,再决定要不要叫人。
9. 同类错误第二次出现 = harness 改造优先级最高的信号。
10. 给 harness 本身设**退役日志**:哪些约束是因为当前模型缺陷,未来可删。

## 来源索引

- OpenAI 原文:《Harness engineering》(https://openai.com/index/harness-engineering/)
- OpenAI 姊妹篇:《Unrolling the Codex agent loop》(https://openai.com/index/unrolling-the-codex-agent-loop/)
- OpenAI 姊妹篇:《Unlocking the Codex harness》(https://openai.com/index/unlocking-the-codex-harness/)
- OpenAI alignment:《Auto-review of agent actions》(https://alignment.openai.com/auto-review/)
- 高质量转述:
  - [akillness《5 Rules That Let Agents Ship 1M Lines》](https://akillness.github.io/posts/harness-engineering/)
  - [Alex Lavaee《OpenAI's Agent-First Codebase Learnings》](https://alexlavaee.me/blog/openai-agent-first-codebase-learnings)
  - [ignorance.ai《The Emerging Harness Engineering Playbook》](https://www.ignorance.ai/p/the-emerging-harness-engineering)
  - [The Neuron《Ship 1M Lines of Code》](https://www.theneuron.ai/explainer-articles/openais-harness-engineering-playbook-how-to-ship-1m-lines-of-code-without-writing-any/)
  - [daily.dev Lopopolo 演讲摘要](https://app.daily.dev/posts/harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan-lopopolo-openai-bspqkijzd)
  - [ZenML LLMOps 摘要](https://www.zenml.io/llmops-database/extreme-harness-engineering-building-production-software-with-zero-human-written-code)
