# ExecPlan · FU-5 · docs(agents): mark § 14 commands as conventions

- **任务 ID**:FU-5 (self-review P0 #2)
- **分类**:`docs`
- **规模**:XS
- **base**:`harness-engineering-setup-v2`
- **版本**:v1

## 1. 目标

把 `AGENTS.md § 14` 的命令表(`/plan`、`/review`、`/context`、`/handoff`、`/harness-change`、`/acceptance check`)从**伪装成"API"**改成**明确为"语义约定"**,避免 agent 照着念:
> "我没有这个命令怎么办?"

并给出:每个语义约定的 **(1) 它到底想要什么结果;(2) 如何用现有工具手动对应完成;(3) 可选的,在特定 agent 平台里建议的实现**。

## 2. 动机

self-review P0 #2:§ 14 列了 6 条"推荐命令",但没有实现,也没绑定任何平台。agent 实际到仓库里会困惑 —— 这是最典型的"harness 说 agent 做 A,agent 照做但 A 不存在"类型的失效。

## 3. 非目标

- 不**实现**这些命令(留给 ADR-0002 决定接入哪个平台时再补)。
- 不改本仓库的工作流(命令只是"希望表达的意图")。

## 4. 影响面

| 路径 | 动作 |
|---|---|
| `AGENTS.md § 14` | 重写 |
| 新增 `docs/agent-commands.md`(可选) | 给每条命令写"语义 + 手动等价" |

## 5. 方案

### 5.1 AGENTS.md § 14 重写

- 加醒目标题:**"Semantic conventions, not bindings"**
- 对每条命令:一句话描述**期望结果**,注明"这不是一条具体语法,是你(agent)需要达成的效果"。
- 提供"手动等价"的一行描述(例:`/plan <issue>` → 读 issue + 复制 `templates/ExecPlan.md` 填好 + 放到 `plan/execplans/`)。
- 加一段"如果你的 agent 平台支持 slash command,建议把它们映射成本仓库的这些语义"。

### 5.2 docs/agent-commands.md

详细版 —— 每条命令一页:

- 语义
- 期望的输入 / 输出 artifact
- 手动等价流程(纯文本步骤)
- 跨平台实现建议(Codex / Claude Code / Cursor / Kiro)
- Anti-pattern("不要做 X")

## 6. 步骤

- [ ] S1 · 重写 AGENTS.md § 14
- [ ] S2 · 新建 `docs/agent-commands.md`
- [ ] S3 · README.md 目录提一句

## 7. 验收

- [ ] § 14 不再看起来像 API;任何 agent 读到会理解"这是语义"
- [ ] `docs/agent-commands.md` 对 6 条命令每条给出 4 个字段(语义 / 手动 / 平台建议 / anti-pattern)
- [ ] 本 PR 不改 workflow / script

## 8. 回滚

`git revert`。

## 9-15

短 plan,略;遵循 FU-4 的简化风格。

| v | date | who | change |
|---|---|---|---|
| v1 | 2026-05-09 | kiro | init |
