# Review Personas · 多角色评审 agent 套装

> 本目录是一组 **评审 persona**。每个 persona 都是一个"有明确关注面 + 明确 rubric + 明确边界"的小 agent 提示,可以独立调用,也可以组合调度。
>
> 目标:把传统 "一个人 review 整个 PR" 这件高耦合的工作,拆成多个**关注面清晰、可并行、可对账**的自动评审,让人类只在关键节点介入。

## 1. Persona 目录

| 文件 | Persona | 关注面 | 默认触发条件 |
|---|---|---|---|
| [security.md](./security.md) | Security Reviewer | 凭证、越权、注入、依赖漏洞、PII | 所有 PR **必跑**(可精简) |
| [testing.md](./testing.md) | Testing Reviewer | 覆盖、边界、等价类、断言强度、flakiness | 所有 PR **必跑** |
| [api-design.md](./api-design.md) | API Design Reviewer | 接口稳定性、命名、向后兼容、schema | 改公共接口时 |
| [performance.md](./performance.md) | Performance Reviewer | 关键路径、N+1、锁、IO、大数据 | 改关键路径 / 大数据 / 并发时 |
| [observability.md](./observability.md) | Observability Reviewer | log / metric / trace / 告警可定位性 | 涉及运行时行为时 |
| [docs.md](./docs.md) | Docs Reviewer | README / ADR / 术语 / 注释 why | 改行为 / 改架构 / 改协议时 |
| [harness-steward.md](./harness-steward.md) | Harness Steward | AGENTS.md / steering / 工具注册表 / CI | 所有 `harness-change` PR |
| [orchestrator.md](./orchestrator.md) | Persona Orchestrator | 调度其他 persona,整合意见 | 所有 PR(可选) |

## 2. 调用方式

每个 persona 文件是一份**完整的 agent system prompt**。调用方式取决于你的 agent 平台,常见三种:

### 方式 A:用作 CLI 命令
```bash
# 伪代码:把 persona 文件作为 system prompt,让它评审当前 PR 的 diff
$ codex review --persona=security < diff.patch
```

### 方式 B:用作 Kiro / Claude Code 子 agent
在主 agent 里调用一个 sub-agent,把对应的 persona 文件作为 system prompt,把当前 diff 作为 user message。

### 方式 C:CI bot
让 CI 在 PR 打开 / push 时自动调起几个必跑 persona,把结果粘进 PR 评论区。

## 3. 统一的输出格式

**所有 persona 都必须按这个 schema 输出**(方便下一步的 orchestrator / CI 汇总):

```yaml
persona: "security"              # persona 名
verdict: "approve"               # one of: approve | approve-with-changes | request-changes | block
summary: "一句话结论"
findings:
  - id: "SEC-001"
    severity: "critical | high | medium | low | info"
    file: "src/billing/refund.ts"
    line: 42
    summary: "一句话概括"
    detail: "多行详细说明"
    suggestion: "具体建议,最好能直接套成一个 diff"
    related_rule: ".kiro/steering/security.md § 3"
followups:
  - "Harness 改动建议(如有),独立 PR 跟进"
escalate_to_human:
  required: false                # true 时主流程必须等人类决策
  reason: ""
```

## 4. 严重性阶梯(persona 通用)

| severity | 含义 | 默认行为 |
|---|---|---|
| **critical** | 触发红线 / 安全事故 / 数据损坏风险 | `block` + escalate 人 |
| **high** | 必须修才能合入 | `request-changes` |
| **medium** | 强烈建议修 | `approve-with-changes` |
| **low** | 打磨;可在后续 PR 修 | `approve` + followup |
| **info** | 观察记录,不影响合入 | `approve` |

## 5. Persona 的硬规矩

- **只在自己的关注面内发言**。别越界。Security persona 不评论 API 命名,除非命名导致安全问题。
- **具体到行**。抽象建议 = 反模式。至少给出文件 + 大致行号 + 可直接采纳的改法。
- **给出 rule 引用**。每个 finding 引用仓库内某条 steering / ADR / RFC,不要"我觉得"。
- **可被反驳**。任何结论都要有依据;人类或其他 persona 可以用数据推翻。
- **三问**(每个 persona 在下判断前默念):
  1. 我是不是超出关注面了?
  2. 我引用的规则真实存在吗?
  3. 我的建议是否会让其他 persona(如 performance)反对?

## 6. 冲突处理

- 两个 persona 意见冲突时,**默认 escalate 给人**,不擅自决议。
- Orchestrator persona 可以尝试综合,但它的 verdict 不能**覆盖**子 persona 的 `block`。
- 人类决议后,在 PR 评论里留痕 + **考虑**是否要加一条 steering 条目来消除同类冲突。

## 7. 建议的默认调度

```
所有 PR:
  - security
  - testing
  - (orchestrator 综合)

若 PR 改 API / schema / URL:       加 api-design
若 PR 改关键路径 / 并发 / 大数据:    加 performance
若 PR 改日志 / metric / 告警:       加 observability
若 PR 改行为 / 架构 / 协议 / 流程:   加 docs
若 PR 为 harness-change:           加 harness-steward(必选)
```

## 8. Persona 的演化

- 发现某个 persona **反复 false positive** → 改其 prompt;如触及对模型的假设,登记到 `.kiro/steering/DEPRECATION.md`。
- 发现某类问题**反复被漏** → 考虑抽出新 persona。不要把所有新关注点塞进已有 persona,会变成"什么都看什么都看不好"的怪物。
- Persona 之间要**尽量正交**——如果一个 finding 可以被两个 persona 命中,优先让**更窄**的那个负责。
