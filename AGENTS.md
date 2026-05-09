# AGENTS.md · 本仓库对 Agent 的约束基线

> 本文件是本仓库的 **Harness 契约**。任何在这个仓库里工作的 AI coding agent(Codex、Claude Code、Cursor、Kiro、自研 agent……)都应当先读完本文件,再动手。
>
> **本文件的权威性等同于代码本身**:对它的修改必须走 PR、被 review、被记账。

---

## 0. 一句话说清楚

> **Humans steer. Agents execute.**
>
> 人设计环境、声明意图、搭反馈回路;你(agent)负责写代码、写测试、写文档、跑 CI,并把失败信号以可消费的形式回传给人。

---

## 1. 文件的优先级与阅读顺序

1. **本文件(`/AGENTS.md`)**——全局基线。最高优先级。
2. **`/.kiro/steering/*.md`**——按主题拆分的 steering 规则。细化本文件。
3. **任务上 ExecPlan(`templates/ExecPlan.md` 产出的 plan 文件)**——任务粒度的意图。
4. **`plan/PROGRESS.md` + 最近一条 `plan/HANDOFF.md`**(仅限长任务)——跨 session 交班记录。
5. **目标文件附近的 `AGENTS.md`** 或目录级 README——模块局部约定,最细粒度。

**冲突解决**:粒度细的胜出(目录级 > 全局);**但任何关于"安全 / 权限 / 不可越界"的规则,最严的那条永远胜出**。

---

## 2. 人与 Agent 的职责分界

| 你应该做(agent) | 不应该做(agent) |
|---|---|
| 写代码 / 写测试 / 写文档 / 写 migration | 代表人类做**产品决策** |
| 先出 ExecPlan,再动手 | 跳过 plan 直接改代码 |
| 按 steering 里的风格与约定写代码 | 为了"更美观"违反约定 |
| 同类错误第二次出现时,**建议 harness 改动** | 默默打补丁、再犯再补 |
| 交付前自己跑一遍测试 / lint / 类型检查 | 让人去跑你能跑的命令 |
| 写清楚每个 PR 的"为什么" | 在 commit / PR 里只写"fix bug" |
| 在不确定时**停下来问** | 在不确定时自行发明需求 |

### 人负责的"四个 checkpoint"
1. **Intent**:issue 的意图与 acceptance。
2. **Plan**:ExecPlan 的结构性 review(plan diff,而非 code diff)。
3. **Acceptance**:合入前对照 rubric 做验收。
4. **Harness change**:对 `AGENTS.md` / steering / 工具注册表的改动做 review。

---

## 3. 标准任务流程

**所有任务都走这条流水线。**

```
  Issue (意图 + acceptance)
        ↓
  /plan  →  templates/ExecPlan.md 填好的草稿
        ↓
  人类 plan checkpoint(必要)
        ↓
  worktree + 独立沙箱启动
        ↓
  按 plan 写代码 + 写测试
        ↓
  本地自动化:lint / type / test / harness 检查
        ↓
  /review  →  逐一调用 review personas
        ↓
  agent 根据 persona 反馈修补
        ↓
  PR(必须使用 /.github/pull_request_template.md)
        ↓
  CI 门禁
        ↓
  人类 acceptance checkpoint(对照 rubric)
        ↓
  Merge
```

### 3.1 开工前必须做的 3 件事
1. 读 `/AGENTS.md` + `/.kiro/steering/*.md` 里**与任务相关**的条目。
2. 产出 `ExecPlan.md`,放到 PR 的第一个 commit。
3. 如果是长任务,先读 `plan/PROGRESS.md` + 最近一条 `plan/HANDOFF.md`。

### 3.2 写码过程中必须做的事
- **小步前进**:一次 plan step = 一次可独立回滚的 commit。
- **测试先行或并行**:不允许"先写代码再补测试"。
- **随时同步文档**:改了接口必须改 README / ADR / 相关 steering 文件。

### 3.3 提交前必须通过的机械检查
在 PR 打开前,agent 必须本地跑一遍:
- 代码格式化(项目约定的 formatter)
- Lint
- 类型检查(如果项目支持)
- 单元测试 + 相关集成测试
- 所有受影响模块的 smoke test

**没跑通就先别开 PR。**

### 3.4 提交时必须做的事
- **选对 PR 模板**(FU-4 改动起生效):
  - 默认 `?` → short 版(fix / docs / chore / 小改)
  - `?template=standard.md` → 新功能 / 行为变更 / 跨模块接口变化
  - `?template=harness_change.md` → 改 AGENTS.md / steering / templates / scripts / workflows / 工具注册表
  - **选错模板 = 重开 PR**(不要硬填)
- PR 的第一个 commit 必须包含 `ExecPlan`(short 版 PR 可以在 commit body 写 micro-plan,但 standard/harness-change **必须**有文件级 ExecPlan)。
- 在 PR 里**显式列出对 AGENTS.md / steering / 工具注册表 的改动**,如果有。
- 如果这次改动是因为某次错误反思而做的 harness 改动,标注 `harness-change` 标签 + 用 harness_change 模板。

### 3.5 合入后必须做的事(长任务)
- 更新 `plan/PROGRESS.md`。
- 写一条 `plan/HANDOFF.md` 或 `plan/sessions/<N>.md`。

---

## 4. 工具约束(**减法优先**)

### 4.1 默认工具清单

任何 agent 在本仓库默认可用:
- `bash`(受沙箱限制)
- 文件读写(限本仓库 worktree)
- `grep` / 代码搜索
- 跑测试(`run_tests`、`pytest`、`npm test` 等项目约定)
- Git(读操作无限制,写操作受 3.4 / 3.5 约束)

### 4.2 默认禁用(除非 PR 中显式获批)

- 访问外网(抓包、拉取任意 URL)
- 写入 `.git/config`、`.gitignore` 以外的系统配置
- 直接修改 CI 上的 secret
- 绕过 hook 的 git 操作(禁止 `--no-verify`)
- 交互式命令(`-i`、会阻塞等待输入)
- 破坏性命令(`push --force`、`reset --hard`、`clean -fd`、`branch -D`),除非人类显式要求

### 4.3 新增工具的规则

向 agent 的工具集添加一个工具,**必须**在 PR 里写清楚:

- 这个工具解决的是哪种重复出现的痛点?
- 它取代的是哪条 prompt 补丁?
- **删掉它将造成什么具体问题?** (没有这条不得合入)
- 它的权限边界?
- 这条工具是为了对抗当前模型的哪个失败模式?(登记到 `/.kiro/steering/DEPRECATION.md`)

---

## 5. 上下文注入规则

> **Context 是本项目最稀缺的资源**。

- **不要**试图塞一个"大而全"的 system prompt。
- 任务级的上下文按需注入:impact map、最相关的文件片段、最相关的 ADR、最相关的历史 PR。
- 如果你不知道一个概念在本仓库里怎么实现,先 `grep`,再读 `docs/`,再读 `.kiro/steering/`——**只有穷尽这三步之后才允许去猜**。
- 永远不要猜测文件路径。**路径必须是真实存在的**;不存在就先 `grep` / `ls`,找不到就问。

---

## 6. 错误处理与"失败倒流"

### 6.1 错误信息的要求

你写的错误信息必须满足三个条件:

1. **机器可解析**(有稳定 code / key,不是自由文本拼字符串)。
2. **面向下一个读者(agent 或人)给下一步建议**。
3. **可重放**:带上最小复现条件。

### 6.2 你出错了怎么办

顺序执行:

1. **自检**:本次失败是哪类? (类型 / 测试 / 风格 / 语义 / 权限)
2. **定位**:失败信号指向哪一 plan step?
3. **决定**:回退这一 step,修改,再推进;还是回到 plan 重写?
4. **反思**:这类错误之前出现过吗?
   - 如果**是**,直接提议 harness 改动(新加测试 / 新加 lint 规则 / 新加 steering 条目 / 新加 review persona)。
   - 如果**否**,继续这次任务,但在 PR 里记一笔"可观察到的新失败模式"。

**禁止**的姿势:默默 retry 同一 prompt、手写 hack 绕过、屏蔽报警、缩小测试范围。

---

## 7. 验证(Verification)

借用 Martin Fowler 站 2026 版的新定义:

> **"Verified" = 被测试 / 被类型 / 被自动门禁 / 或在你判断最值钱处被你读过。**

不算 verified 的情况:
- "我读过了,看起来对"
- "单跑一下是过的"(不写进自动化)
- "先合进去,后面再补测试"

### 7.1 本仓库的验证层(从下往上)

1. **代码层**:formatter、lint、type check。
2. **单元测试**:相关模块 + 新增代码。
3. **集成测试**:涉及跨模块的。
4. **Review Persona**:至少 `security` + `testing` + 与变更相关的 1~2 个。
5. **CI**:所有绿灯才能合。
6. **人类 acceptance**:按 rubric。

### 7.2 Review Persona 调度规则
- 每个 PR **至少**调度:`security`、`testing`。
- 涉及接口/协议的 PR 加:`api-design`。
- 涉及性能敏感路径的 PR 加:`performance`。
- 涉及日志/监控的 PR 加:`observability`。
- 涉及 harness 自身的 PR 加:`harness-steward`。
- Persona 冲突时,**默认 escalate 给人**,不擅自决议。

---

## 8. 安全红线(不可跨越)

以下任何一条触发,立即停止并呼叫人类:

- 发现真实 secret(凭证、token、key)被写入仓库或日志。
- 任何会**修改生产数据**的操作。
- 任何会**对外产生副作用**的网络请求(支付、发邮件、发消息、调用第三方带副作用的 API)。
- 任何会**绕过身份验证 / 授权**的改动。
- 任何**监控 / 收集个人隐私数据**的改动(未经显式许可)。
- 任何**擦除或重写 git 历史**的改动。
- 任何改动 CI 或仓库权限配置的改动(除非明确任务就是做这件事)。

触发规则:**先停手,再 PR 留评论 /issue 说明,再等人来决策**。

---

## 9. Harness 老化对抗

(参见 `docs/harness-engineering/02-anthropic-harness.md`。)

- 本仓库维护一份 `/.kiro/steering/DEPRECATION.md`。
- 所有"为了对抗当前模型某个缺陷"而加入的约束,**必须**在 DEPRECATION.md 里登记:
  - 约束内容
  - 针对的模型版本
  - 触发的具体现象
  - 何时可复审(至少每季度一次)
- 模型升级后,第一优先级是**复审 DEPRECATION.md**,删除不再必要的约束。

---

## 10. 长任务特例

(参见 `docs/harness-engineering/02-anthropic-harness.md` 的 "记忆三件套"。)

如果本次任务被标为长任务(跨 session / 跨天),在 `plan/` 下维护:

- `plan/PROGRESS.md`:全局 feature 列表 + 完成状态 + 下一步。
- `plan/HANDOFF.md` 或 `plan/sessions/<N>.md`:本 session 的**交班记录**。必须包括:
  - 本次做了什么(附 PR 链接)
  - 仓库当前是否 green
  - 下一次 session 应该从哪一步接手
  - 已发现但未解决的坑
  - 任何"需要人类决策"的悬而未决问题
- `plan/decisions/*.md`:长期 ADR。

**硬规定**:
- Session 开始前必须 `cat` 这三处的最新内容。
- Session 结束时必须写下一次 HANDOFF——**没写就不许合入长任务分支**。

---

## 11. 提问规则

什么时候**必须**停下来问人类,而不是继续推进:

- Acceptance 标准不清晰,且无法从已有 issue / spec / ADR 推出。
- 需要决定**接口契约**或**向后兼容策略**,而 ADR 没写。
- 发现 AGENTS.md / steering 自相矛盾。
- 存在多种都符合规范的实现选择,且方向性后果显著。
- 触发了第 8 节的任何一条红线。

提问格式:在对应 issue / PR 上留评论,包含:
- 具体问题。
- 你已经查过的资料(`grep` 结果、steering 条目、ADR 编号)。
- 你倾向的方案 + 理由。
- 如果人类 N 小时内没回应,你的**fallback 行为**是什么(通常:停手等待,不得擅自推进)。

---

## 12. 不可为之事(Don'ts)

- ❌ 跳过 ExecPlan 直接改代码。
- ❌ 自行发明 acceptance。
- ❌ 用户说"差不多就行"时真的差不多——仍按 AGENTS.md 的验证标准走。
- ❌ 为了合入 PR 而缩小测试范围 / 屏蔽失败 / 加 `skip`。
- ❌ 在一次 PR 里混入 "harness 改动 + 业务逻辑改动"。
- ❌ 把 prompt 补丁当 harness 主体(新加约束应改 AGENTS.md / steering / 工具注册表,而不是藏在某个任务的 prompt 里)。
- ❌ 修改 `.git/config`、hook 禁用、force push 到 main/master(除非明确指令)。
- ❌ 在 PR 里隐藏安全相关的变更(新增权限、新增工具、新增网络调用)。

---

## 13. 反模式速查(自检清单)

开 PR 前请默念一遍,任何一条为真就先别合:

- [ ] 我跳过了 plan checkpoint 吗?
- [ ] 我把"harness 改动"和"业务改动"混在同一 PR 里了吗?
- [ ] 我为了让测试通过缩小了测试范围吗?
- [ ] 我这次改的东西,**下次我自己都读不懂**吗?
- [ ] 我加了新工具 / 新权限但没登记在 DEPRECATION.md 吗?
- [ ] 我改了 AGENTS.md / steering 但没在 PR 标 `harness-change` 吗?
- [ ] 我在没有 acceptance 的情况下自己补了 acceptance 吗?
- [ ] 我触发了第 8 节的任何一条红线吗?

---

## 14. 推荐使用的命令集(如果 agent 平台支持)

| 命令 | 效果 |
|---|---|
| `/plan <issue>` | 基于 issue 产出 `ExecPlan.md` 草稿 |
| `/context <path>` | 拉取 `<path>` 的 impact map + 相关 ADR / steering |
| `/review <persona>` | 用指定 persona(或 `all`)对当前 diff 做评审 |
| `/handoff` | 写下一次 session 的 HANDOFF 草稿 |
| `/harness-change <reason>` | 起一个 harness 改动 PR,自动带退役条件字段 |
| `/acceptance check` | 根据 issue 上的 rubric 对当前产物做机器化验收 |

---

## 15. 延伸阅读(本仓库内)

- `docs/harness-engineering/README.md`:中文精读库总目录。
- `docs/harness-engineering/00-overview.md`:一页纸总览。
- `docs/harness-engineering/06-methodology.md`:方法论骨架。
- `docs/harness-engineering/07-practice-checklist.md`:"明天就能干的事"。
- `.kiro/steering/`:按主题拆分的 steering 规则集。
- `templates/ExecPlan.md`:执行计划模板。
- `templates/review-personas/`:评审 persona 套装。
- `.github/pull_request_template.md`:PR 必填格式。

---

## 16. 变更历史

本文件本身也要走 PR + review。任何大改需要在 `.kiro/steering/DEPRECATION.md` 登记,并写明:

- 改了什么
- 为什么改(对应哪种反复出现的失败)
- 什么条件下可以把本条删除
