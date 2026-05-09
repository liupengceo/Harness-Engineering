# 07 · 实践清单:从零搭一套最小可用 Harness

> 这一章是"**明天就能开始做的事**"。假设你是一个 3–10 人的工程团队,想把 agent 引进来做"主要劳动力"。

---

## 阶段 0:确认前提

1. 有一个 git 仓库,CI 能跑单测和 lint。
2. 团队统一一种 coding agent 工具(Codex CLI、Claude Code、Cursor、Kiro 等)。
3. 至少有一个**机器可跑的 acceptance 信号**——不一定完美,但不能纯靠"人眼觉得还行"。

如果 3 不成立:**先补这条,比上 agent 优先级高 10 倍**。

---

## 阶段 1:仓库搭骨架(1 天)

在仓库根建立:

```
AGENTS.md                         # agent 约束基线
.kiro/steering/
  ├─ harness.md                  # harness 工作方式
  ├─ code-style.md               # 代码风格
  ├─ testing.md                  # 测试约定
  └─ security.md                 # 安全/权限红线
templates/
  ├─ ExecPlan.md                 # 执行计划模板
  └─ review-personas/            # review agent persona 套装
.github/
  ├─ pull_request_template.md    # PR 必填格式
  └─ ISSUE_TEMPLATE/
      └─ task.md                 # 任务 issue 模板
plan/                             # 长任务的记忆(按需)
  ├─ PROGRESS.md
  └─ sessions/
docs/harness-engineering/         # 你现在在看的这个目录
```

**验收**:
- [ ] 新来一个工程师(或一个 agent)能**10 分钟内**看完这些文件,就知道在这里干活的约定。
- [ ] 任何时候,"我们的规矩在哪?" 这个问题只有一个答案:**上面的文件**。

---

## 阶段 2:统一任务流(2–3 天)

每个任务走同一个流水线:

```
   Issue(意图 + acceptance)
         ↓
   ExecPlan.md(structured plan)
         ↓
   人类 plan checkpoint(看 plan diff)
         ↓
   agent 实现 + 测试
         ↓
   agent-based review(persona)
         ↓
   CI 门禁(lint / type / test)
         ↓
   人类 acceptance checkpoint(看 rubric,不是逐行代码)
         ↓
   Merge
```

**硬规定**:
- 无 ExecPlan 的 PR 一律不合。
- 无 acceptance 的 issue 一律回退。
- 同一类问题**第二次发生**,触发 "harness 修改" PR,不得再次打补丁。

---

## 阶段 3:工具减法(持续)

给 agent 的工具集做"**能不能去掉**"复审,每月至少一次。

**先减后加**原则:

- 默认只给 4 件套:`bash`、`fs`(read/write)、`grep`、`run_tests`。
- 其他工具一律需要"添加理由说明"才能进工具集。
- 每多一件工具,必须写上 "**删除它会造成什么问题**"。
- 每删一件工具,把对应的 "prompt 补丁" 一并清走。

---

## 阶段 4:每任务 worktree / devbox(1 周)

- 每个任务开一个独立 git worktree。
- 观测(logs、metrics、tracing)跟着 worktree 启停。
- 如果有条件,使用 ephemeral devbox(参考 Stripe 10 秒启动基准)。
- 禁止"多任务共用一个工作目录"——这是并行最大的坑。

**验收**:
- [ ] 工程师能**同时**带 3 个以上 agent 任务,互不干扰。
- [ ] 任务失败时,能**完整保留**失败现场(worktree + logs + 最后的 prompt)以便复盘。

---

## 阶段 5:Review Persona(1 周)

把 "code review" 按关注面拆成多个 persona,每个 persona 是一个**小 agent + rubric**:

| Persona | 关注 |
|---|---|
| **Security Reviewer** | 密钥泄露、注入、越权、依赖漏洞 |
| **Performance Reviewer** | 关键路径、N+1、锁、同步阻塞 |
| **API Design Reviewer** | 接口稳定性、命名、向后兼容 |
| **Testing Reviewer** | 覆盖、等价类、边界、断言强度 |
| **Observability Reviewer** | 日志、指标、trace 可定位 |
| **Docs Reviewer** | README、ADR、AGENTS.md 是否同步更新 |

人类只在**多 persona 冲突**或**高风险变更**时介入。Persona 模板放在 `templates/review-personas/`。

---

## 阶段 6:长任务三件套(按需)

长任务(跨多 session / 跨多天)在 `plan/` 目录下维护:

- **PROGRESS.md**:全局 feature list + 完成状态 + 下一步。
- **HANDOFF.md**(或 `sessions/<n>.md`):本 session 做了什么、下次该做什么、有什么坑。
- **decisions/**:ADR 风格的长期决策记录。

**约定**:
- Session 开始,agent 必须先 cat 这三处。
- Session 结束,agent 必须写下一次 HANDOFF。
- 没写 HANDOFF 的 PR 不合入长任务分支。

---

## 阶段 7:失败倒流(持续)

生产或 CI 里发现的问题,走这个流程:

```
incident / CI failure
        ↓
  判定:这是 agent 反复会犯的类别吗?
        ↓
    ┌── 是 ──┐           ┌── 否 ──┐
    ▼        ▼           ▼        ▼
 harness  新建测试     这一次的     这次 agent
  改动     + lint     修复 PR      再跑一遍
   PR      规则
```

**一句话总结**:只要"这类错误可能再犯",就要改 harness,不要只改代码。

---

## 阶段 8:Harness Change Audit(持续)

- 对 `AGENTS.md`、`.kiro/steering/*`、工具注册表的改动,**和生产代码一样 review**。
- 每条 steering 条目要有 "为什么存在" 的注释。
- 维护 `.kiro/steering/DEPRECATION.md`(或类似文件):
  - 哪些约束是"为了对抗当前模型的失败模式"?
  - 模型升级后应当复审?
  - 已经被某次 harness 改动替代?

---

## 阶段 9:指标与回顾(每 2 周一次)

量化 harness 的效果,跟进的是**团队级**指标,不是个人:

| 指标 | 含义 |
|---|---|
| **PR / 人 / 天** | 吞吐(OpenAI 参考值:3.5) |
| **PR 首次通过 CI 比例** | harness 质量的直接信号 |
| **人类 review 平均时长** | 是否真的"on the loop" |
| **同类错误复现次数** | harness 是否在"吸收经验" |
| **Harness 变更 PR 比例** | 团队是否在做正事 |
| **工具数量** | 做减法做得如何 |

---

## 阶段 10:对抗老化(每季度一次)

- 过一遍 `.kiro/steering/DEPRECATION.md`:哪条可以删?
- 过一遍工具注册表:哪个工具已经不需要了?
- 过一遍 `templates/review-personas/`:哪个 persona 该合并、该拆分?
- 过一遍 `AGENTS.md`:**让 agent 自己先读一遍,指出它觉得"陈旧 / 不必要 / 自相矛盾"的条款**,再由人决定。

---

## 阶段 11:进阶 · 往 Minion / 长任务两头走

等上面跑顺后,两个方向可以并行:

### A. Minion 化(针对高频任务)

- 为每类高频任务建 Blueprint:issue 模板 + ExecPlan 模板 + 固定的 step 序列。
- 让高频任务"**无人值守**":Slack 命令 / 定时任务 / webhook 触发。
- KPI:每周人类干预次数持续下降。

### B. 长任务化(针对大特性)

- 启用 planner + generator + evaluator 三件套。
- 引入 `HANDOFF.md` 约定。
- 允许 agent 跨 session 自主推进多天。

---

## 12. 反模式速查

常见翻车:

- ❌ **全靠一个巨大 system prompt** → 应该按需注入 context。
- ❌ **给 agent 越来越多工具** → 先做减法。
- ❌ **一出问题就手改** → 要修 harness。
- ❌ **plan 不 review,PR 才 review** → 太晚了。
- ❌ **长任务依赖 conversation history 记状态** → 用 `HANDOFF.md`。
- ❌ **把 harness 当一次性脚本** → 应当进 PR + audit + 退役清单。
- ❌ **用"人眼觉得还行"验收** → acceptance 必须有机械信号。

---

## 13. 推荐的起步命令集(agent 命令)

| 命令 | 作用 |
|---|---|
| `/plan <issue>` | 读 issue,产出 `templates/ExecPlan.md` 填好的草稿,贴到 PR 里 |
| `/review <persona>` | 调用某个 persona 对当前 diff 做评审 |
| `/handoff` | 产出本 session 的交班记录 |
| `/context <path>` | 按路径拉取 impact map + 相关 ADR |
| `/harness-change <reason>` | 起一个 harness 改动 PR,模板带好"为什么 / 替代方案 / 退役条件" |

这些命令不必一开始就全齐——从 `/plan` 和 `/review` 开始最划算。

---

## 来源索引

这一章是实操整理,主要参考:

- OpenAI《Harness engineering》 与 [Ryan Lopopolo 演讲摘要](https://app.daily.dev/posts/harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan-lopopolo-openai-bspqkijzd)
- Anthropic《Effective harnesses for long-running agents》
- Stripe《Minions》Part 1/2
- Shopify《Introducing Roast》
- Martin Fowler 站《Humans and Agents》
- [Verdent《Harness Engineering in Practice》](https://www.verdent.ai/fr/guides/harness-engineering-ai-coding-workflow)
- [mer.vin《Harness Engineering with Codex》](https://mer.vin/2026/04/harness-engineering-with-codex-a-practical-beginner-guide-to-human-steered-agent-delivery/)
