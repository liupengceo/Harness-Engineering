---
title: Harness 核心约束
inclusion: always
---

# Harness 核心约束

> **所有任务都要读这一份。** 本文件是 `/AGENTS.md` 的具体化:把 "humans steer, agents execute" 落到每天的动作上。

## 1. 公式

```
Agent = Model + Harness
```

你(agent)是 **Model** 的一部分,**Harness** 是你周围的一切:本仓库的工具、AGENTS.md、steering、测试、CI、review persona、沙箱、记忆三件套……

**限制你表现上限的,不是你的模型大小,是 harness 的形状。**
这意味着:你遇到反复出错的场景时,**第一反应应当是:harness 里少了什么**,而不是"再换一个 prompt 试试"。

## 2. 四条铁律

### R1 · 先 Plan,再 Code

- 任何触及代码的任务**必须先出 ExecPlan**(见 `templates/ExecPlan.md`)。
- Plan 必须包含:目标 / 影响面(impact map)/ 步骤 / 验收标准 / 回滚方案。
- Plan 放入 PR 的**第一个 commit**。
- **人类 plan checkpoint 未通过前,不得开工**(小任务可由人类显式跳过,但必须在 PR 里留痕)。

**理由**:在 3 行 plan 上抓错,比在 800 行 PR 里抓错便宜一个数量级。
**退役条件**:本条长期有效。

### R2 · Repo 是唯一真相源

- 所有决策、约定、接口契约 → **沉到仓库里的 markdown / schema / 类型定义**。
- 藏在 Slack、Google Docs、脑子里的知识 = 对你不存在。
- 发现"我不知道这件事怎么做"时,正确顺序:
  1. `grep`
  2. 读 `docs/`
  3. 读 `.kiro/steering/`
  4. 读 `AGENTS.md`
  5. 仍查不到 → **停下来提问**,不要猜。

**理由**:agent legibility 的前提是"信息真的在你看得见的地方"。
**退役条件**:长期有效。

### R3 · 修 Harness,不修输出

- 任何一类错误**第二次出现**,触发 harness 改动:加 schema / 加 lint / 加测试 / 加 steering / 加 persona / 加工具……或者**减**工具。
- 禁止:换一个 prompt 压下同类错误,不做任何结构性改动。
- harness 改动走独立 PR,标 `harness-change` 标签。

**理由**:打补丁会让同一类失败在后续任务反复付出 token + 注意力成本。
**退役条件**:长期有效。

### R4 · 工具减法优先

- 工具默认清单见 `/AGENTS.md` § 4.1,其余都默认禁用。
- 新增工具必须同时写明"**删掉它会造成什么损失**"。
- 每季度一次"减法复审":当前模型已经不需要哪些工具?

**理由**:工具越多,agent 分心越多,约束悖论反复验证"少即是准"。
**退役条件**:长期有效。

## 3. 五层反馈结构

| 层 | 频率 | 谁负责 | 产物 |
|---|---|---|---|
| 单任务内 | 秒/分 | 你自己 | 本地 test / lint / type 跑通 |
| ExecPlan | 分 | 你 + plan checkpoint | `ExecPlan.md` + 人类 OK |
| PR 评审 | 分 | review persona + CI | `/review` 报告 + 绿灯 |
| Acceptance | 小时 | 人类 + rubric | 合入 |
| 生产 | 天/周 | 团队 + 监控 | harness PR(必要时) |

**所有失败信号必须满足**:结构化、可归因、可回放。

## 4. 上下文经济

- Context window 是稀缺资源。**不要塞一个巨大的 system prompt**;按任务按需注入。
- 一次只做一个 feature / 一个 plan step,不跨 feature 拼进一次对话。
- 不会做的事优先 `grep`,不是"大胆猜然后让测试告诉我"。
- 路径、名字、API 签名 → **以真实仓库为准**,永远不许凭印象写。

## 5. 长任务的三件套

(仅当任务被标为"长任务":跨 session / 跨天)

- **必读**(session 开始前):
  - `plan/PROGRESS.md`
  - `plan/HANDOFF.md`(或最近一条 `plan/sessions/<N>.md`)
- **必写**(session 结束前):
  - 更新 `plan/PROGRESS.md` 的完成状态
  - 新写 `plan/HANDOFF.md`,字段:做了什么 / 仓库是否 green / 下一步该做什么 / 遇到的坑 / 待决问题
- 不写 HANDOFF = 这次 session 不能合入长任务主分支。

## 6. 反模式(任何一条都要立刻停止)

| 反模式 | 为什么要停 | 正确姿势 |
|---|---|---|
| 跳过 plan checkpoint | 成本失控 | 先出 ExecPlan |
| 猜测文件路径 | 幻觉注入 | grep,找不到就问 |
| 用自然语言替代 schema | agent 可读性差 | 能类型化就类型化 |
| 把 "harness 改动" 和 "业务改动" 塞进同一 PR | 难 review,难回滚 | 拆成两个 PR |
| 新加工具不写"删掉的代价" | 工具越堆越多,最终失控 | 不写就不加 |
| 失败了就换个 prompt 再试 | 错误不会沉淀 | 改 harness 或提问 |
| 长任务靠 conversation history 记状态 | 下次 session 必然失忆 | 写 HANDOFF |
| 为了 PR 合入缩减测试范围 | 把质量债藏进自己仓库 | 修代码,不修测试 |

## 7. 与其他 steering 的关系

- `code-style.md`:每次写代码前匹配风格。
- `testing.md`:每个 plan step 对应一组可执行的验收(不只是功能测试)。
- `security.md`:随时应用。触发红线立即停。
- `docs.md`:接口 / 行为 / 架构变更必须同步更新文档。
- `git-workflow.md`:Git 和 PR 的具体规范。
- `DEPRECATION.md`:每增/改一条 harness,登记一下。

## 8. 自检触发器(agent 必答)

每开始一个任务时,默念一遍:

- [ ] 这次任务属于**短任务**还是**长任务**?
- [ ] 读过 `/AGENTS.md` 的 § 3、§ 4 没?
- [ ] 读过 `harness.md`、任务相关主题的 steering 没?
- [ ] 有 ExecPlan 吗?人类审过了吗?
- [ ] worktree / 沙箱是否隔离?
- [ ] 长任务:`PROGRESS.md` + 最近 `HANDOFF.md` 读过了?
- [ ] 本次任务会触及的"重复痛点",已知的 harness 应对在哪条 steering 里?

任何一条"否",先把它变成"是"再继续。

## 9. 延伸阅读

- `docs/harness-engineering/06-methodology.md` — 方法论骨架
- `docs/harness-engineering/07-practice-checklist.md` — 落地清单
- `docs/harness-engineering/01-openai-harness.md` — OpenAI 博客精读
- `docs/harness-engineering/02-anthropic-harness.md` — Anthropic 三篇
