# 06 · 方法论:把 harness engineering 拆到骨头

> 这一章把 00 / 01 / 02 / 03 / 05 各章里出现的方法论提取并结构化,便于作为**团队内部讲义**或**架构评审参考**。

---

## 1. 公式:Agent = Model + Harness

| 组件 | 负责 |
|---|---|
| **Model** | token → token 的推理;最小单位的"认知" |
| **Harness** | 其他**全部**:工具、权限、上下文、反馈、观测、评审、记忆、编排 |

**推论**:

- 模型没变,harness 变了,性能就变了 → 所以 harness 是产品的杠杆点。
- Harness 是**可版本化的工程资产**:应该像代码一样进 PR、被 review、被测试。

---

## 2. 五个控制杆(Harness 的可调项)

| 杆 | 问题 | 工具与约束 |
|---|---|---|
| **工具层 Tools** | agent 能触达什么? | 工具注册表、MCP、自定义 CLI、严格 schema |
| **上下文层 Context** | 给它什么信号? | AGENTS.md、.kiro/steering/、impact map、少量高质量样本 |
| **错误层 Errors** | 出错怎么说? | 结构化错误 + 下一步建议 + 稳定 error code |
| **验证层 Verification** | 怎么证明"好了"? | 测试、类型、lint、CI、auto-review agent、acceptance rubric |
| **权限/范围层 Scope** | 能动到哪里? | devbox、文件系统白名单、网络白名单、凭证 scope、write gate |

**约束悖论(constraint paradox)**:更严的约束、更少的工具、越窄的权限,**常常带来更高的成功率**。先做减法,再考虑加项。

---

## 3. 任务模式光谱

把"agent 做什么任务"画在一张光谱上,不同位置适合不同 harness 策略:

```
  有界 / 高频            <───────────────────>            无界 / 少而复杂
  (Minions 风格)                                           (长任务 harness)

  - ticket → one-shot PR        - 复杂 feature / 重构 / 新产品
  - 升级依赖、修 flaky test      - 需要多 session 的长项目
  - 模板化生成样板代码            - 需要跨 feature 决策
  - Blueprint + deterministic     - planner / generator / evaluator
    控制 agent 每一步              - HANDOFF.md / PROGRESS.md
```

**不要把长任务的 harness 套用到高频短任务上**,反之亦然——这一点最容易出错。

---

## 4. 三层反馈回路(Stripe Minions 提法的一般化)

| 层 | 频率 | 谁负责 | 作用 |
|---|---|---|---|
| **单任务内** | 秒级 ~ 分级 | agent 自己 | 写 → 测 → 修;直到绿 |
| **PR 门禁** | 分钟级 | CI + review persona | 一道自动化质检;人工仅看被标红处 |
| **生产** | 天级 ~ 周级 | 团队 | 失败信号倒流:改 harness,而非改某次输出 |

每条反馈都要满足三个条件:
1. **结构化**:agent 能直接消费,不是堆栈文本。
2. **可归因**:能指回哪次改动 / 哪条规则。
3. **可回放**:能用这条信号本地重跑一遍。

---

## 5. 长任务的"记忆三件套"

来自 Anthropic《Effective Harnesses》,落地到仓库里就是这三件东西:

| 文件 | 职责 |
|---|---|
| `plan/PROGRESS.md` | 全局 feature list + 完成状态。每次 session 开始先读它。 |
| `plan/sessions/<n>.md` 或 `plan/HANDOFF.md` | 每次 session 的**交班记录**:做了什么、下次该做什么、坑在哪里。 |
| `plan/decisions/*.md`(或 ADR) | 长效决策。跨 session 长期有效。 |

**约定**:
- **Session 开始**:agent 必须先读 `PROGRESS.md` + 最近一条 `HANDOFF.md`,才能动手。
- **Session 结束**:必须写**下一个** `HANDOFF.md`,否则 PR 不能合并。

---

## 6. 复杂任务的"三 agent 架构"

来自 Anthropic《Harness design》:

```
  ┌───────────┐      tractable chunks       ┌───────────┐
  │  Planner  │ ──────────────────────────▶ │ Generator │
  │   agent   │                             │   agent   │
  └─────┬─────┘                             └─────┬─────┘
        │                                         │
        │ acceptance rubric                       │ code + tests
        │                                         ▼
        │                                  ┌───────────┐
        │                                  │ Evaluator │
        │                                  │   agent   │
        │                                  └─────┬─────┘
        │                                        │ feedback
        │                                        ▼
        └────────────── (loop until pass) ───────┘
```

**关键设计**:

- Evaluator 的第一步是**把模糊判断翻译成具体可打分维度**。否则它就是"觉得挺好"的复读机。
- Planner 的 chunk 粒度要**刚好能让 Generator 一次做完**——太小浪费 context,太大退化回"单 agent"。

---

## 7. Harness 会老化:三种对抗姿势

核心警告:**harness 把模型此刻的缺陷焊成了结构,模型进化会让 harness 变成负担**。
对抗姿势:

1. **解耦(Brain ↔ Hands)**
   - 对外只暴露稳定的"动作接口"(工具签名、权限、artifact schema)。
   - 内部 harness 实现可以随模型换代而整改。
   - Anthropic Managed Agents 就是这种模式。

2. **退役清单(Deprecation List)**
   - 每增加一条 harness 约束,标注它**是为了对抗当前模型的哪种失败模式**。
   - 定期问:模型升级后,这条还需要吗?
   - 把这个清单当成**技术债台账**来管。

3. **最简主义(Minimalism)**
   - 不轻易加工具、不轻易加 persona、不轻易加 prompt。
   - 每加一项,都要写清**去掉它的代价**是什么。
   - 越少的 harness = 越小的老化风险。

---

## 8. Harness 架构的 "七件套" 参考

从所有文献里抽出可复用的模块清单。你不一定都要有,但看着这张表可以自检漏了啥:

| 模块 | 问题 | 最小实现 |
|---|---|---|
| **Intent 捕获** | 人怎么告诉 agent 想要什么 | issue 模板 + acceptance 字段 |
| **Spec / ExecPlan** | 开工前的结构化蓝图 | `templates/ExecPlan.md` |
| **Context 注入** | 按任务喂相关文件 | impact map 脚本 + symbol search |
| **工具注册表** | agent 能做什么 | 工具 schema + 权限矩阵 |
| **沙箱 / worktree** | 在哪里做 | 每任务独立 worktree / devbox |
| **测试 + 自动评审** | 做完以后怎么验 | CI + review persona |
| **长任务记忆** | 跨 session 怎么接 | `PROGRESS.md` / `HANDOFF.md` |
| **观测 + 评测** | 整体健康度 | 失败倒流 + harness change audit |
| **退役机制** | 老化怎么治 | deprecation list + harness ADR |

---

## 9. Harness 和 Prompt / Context Engineering 的关系

不要被这几个词搞混:

- **Prompt engineering**:对**单次调用**的 prompt 做优化。
- **Context engineering**:决定**哪些 token 该进 prompt**,以及**什么时候**进。
- **Harness engineering**:决定**整个系统(agent loop、工具、验证、记忆、权限)**长什么样。

三者包含关系:**harness ⊃ context ⊃ prompt**。一个成熟团队的精力分配大致是 **70/25/5**——花在 harness 上的时间远远多于花在 prompt 本身上的。

---

## 10. 落地清单(可直接贴到内部 wiki)

- [ ] 仓库根有 `AGENTS.md`,由人类精读定版。
- [ ] `.kiro/steering/` 有按主题拆分的 steering 文件。
- [ ] 任务必须先出 `ExecPlan.md`,再写代码。
- [ ] 每个长任务有 `PROGRESS.md` + 最新 `HANDOFF.md`。
- [ ] PR 模板强制包含:意图、plan 链接、验证清单。
- [ ] CI 有至少一个 auto-review agent,持 persona 做初评。
- [ ] 工具清单显式列出,且定期"减法复审"。
- [ ] 每次 agent 犯错,工程师问的第一个问题是 "harness 怎么改"。
- [ ] Harness 的修改走独立 PR,保留 audit trail。
- [ ] 有一张 deprecation list,登记"为当前模型打的补丁"。

---

## 来源索引

- OpenAI《Harness engineering》:https://openai.com/index/harness-engineering/
- OpenAI《Unrolling the Codex agent loop》:https://openai.com/index/unrolling-the-codex-agent-loop/
- Anthropic《Harness design for long-running application development》:https://www.anthropic.com/engineering/harness-design-long-running-apps
- Anthropic《Effective harnesses for long-running agents》:https://anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic《Managed Agents》:https://www.anthropic.com/engineering/managed-agents
- Stripe《Minions》:https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
- Shopify《Introducing Roast》:http://shopify.engineering/introducing-roast
- Martin Fowler 站《Harness Engineering》:https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html
- Martin Fowler 站《Humans and Agents》:https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html
- [Build This Now 《Agent Harness Engineering》](https://www.buildthisnow.com/blog/guide/agents/agent-harness-engineering)
- [Tian Pan 《Harness Engineering》](https://tianpan.co/blog/2026-02-17-harness-engineering-agent-first-software-development)
- [Naoko Reeves《Harness Engineering Cheat Sheet》](https://naoko.github.io/posts/2026-04-28-harness-engineering-overview/)
