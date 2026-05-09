---
title: 文档与 ADR 标准
inclusion: fileMatch
fileMatchPattern: "**/*.{md,rst,mdx,adr}"
---

# 文档与 ADR 标准

> 本仓库奉行 **repo-as-source-of-truth**:藏在 Slack / 文档系统 / 脑子里的知识对 agent 不存在。
>
> 这份 steering 定义"什么时候必须写文档,写成什么样"。

## 1. 三类文档(定义边界)

| 类别 | 住在哪里 | 用途 | 谁读 |
|---|---|---|---|
| **讲解型(Docs)** | `docs/` | 对外对内讲清楚"这是什么、为什么、怎么用" | 新人、agent、用户 |
| **决策型(ADR)** | `docs/adr/` 或 `plan/decisions/` | 记录长期影响的架构 / 技术决策 | 未来的自己、新 agent |
| **记忆型(Plan)** | `plan/` | 长任务的 PROGRESS / HANDOFF / 会话交班 | 下一次 session |

**不要混**。把决策写进 README、把讲解塞进 ADR,都是反模式。

## 2. 什么改动**必须**同 PR 更新文档

触发任何一条 → 改动必须同步相应文档,否则 PR 不合入:

- 改了**公共接口**(HTTP / RPC / CLI / SDK signature)→ 更新 API / SDK 说明。
- 改了**用户可见行为**(UI flow、CLI 输出、错误消息含义)→ 更新用户文档。
- 改了**架构 / 模块边界 / 依赖关系** → 写一份 ADR。
- 改了**构建 / 部署 / 配置**流程 → 更新 README / ops 文档。
- 改了 **AGENTS.md** / **steering** / **工具注册表** → 同 PR 做 harness-change 登记。
- 改了 **schema / migration / feature flag** → 写迁移说明(含 rollback 步骤)。

## 3. ADR 的最低格式

放在 `docs/adr/NNNN-title.md`,必含 7 字段:

```markdown
# ADR-NNNN · <一句话结论>

- **状态**:Proposed | Accepted | Superseded by ADR-XXXX | Deprecated
- **日期**:YYYY-MM-DD
- **作者**:@author(可以是 agent + 复核人)

## 上下文

我们在什么情况下面对什么问题。这个问题的**约束条件**是什么。

## 决策

我们选择了什么。**一句话能说清就不要展开**。

## 候选方案

- 方案 A:<描述>。优点 <...>。缺点 <...>。
- 方案 B:<...>
- 方案 C:<...>(如果有)

## 取舍理由

为什么选了当前这个方案,放弃了其他。

## 后果

- **正向**:<...>
- **负向**:<...>(必填,空白是红旗)
- **监控信号**:我们用什么指标判断这个决策是对的?

## 退役条件

什么条件下这个 ADR 应该被重新审视?
```

ADR 编号单调递增,不重复;被替代的 ADR 不删,改状态为 `Superseded by ADR-XXXX`。

## 4. 讲解型文档(Docs)的规范

- 每个主目录都应有 `README.md`,回答三件事:**这是什么 / 它为什么存在 / 怎么用 / 怎么改**。
- 代码示例**必须可运行**(哪怕是伪代码,也要标明 "pseudocode")。
- 链接用相对路径;外部链接写清楚域名和发布时间(便于几年后判断是否过期)。
- 大于 500 行的 doc 一定要有目录(TOC)。

## 5. 注释与代码内 docstring(与 `code-style.md` 互补)

- 文件顶部用一段 **≤10 行** 的注释说明:这个文件做什么、主要出入口、依赖谁。
- 公开函数 / 类必须有 docstring,内容:**输入、输出、side effect、错误、典型用法**。
- 内部复杂函数的 docstring 里必须有 "**哪些改动会破坏它**" 一行。

## 6. 面向 agent 的可读性

- 术语统一——同一概念在整个仓库里**只用一种命名**。发现两种并存:立刻起一个 `docs/glossary.md` 标准化。
- 尽量**用表格和列表**表达约束、枚举、对比——比自然语言段落好 grep。
- **每段 / 每节**都应该可以独立成块被拉进 context。避免"必须从头读到尾才能理解第 7 节"的叙事结构。
- 使用**稳定的锚点**(section heading 不要随便改;要改时保留旧锚点作为跳转 alias)。

## 7. 图与流程

- 优先用 **mermaid / plantuml** 文本图,而不是图片。
- 图要**能被 grep**(写标签、不要全是线)。
- 关键流程一张总览 + 按场景拆 3~5 张细图,而不是一张巨图。

## 8. "写文档"常见反模式

| 反模式 | 为什么坏 | 正确姿势 |
|---|---|---|
| 写"当前项目进度" | 过半年必定陈旧 | 进度放 issue tracker / PROGRESS.md |
| 一个 README 5000 行 | 没人读 | 拆目录 |
| 复制粘贴的"Quick Start" | 版本不一 | 链接到单一 source |
| 描述性文字代替表格 / 枚举 | 难 grep | 用表格 / 列表 |
| 决策藏在 PR 评论里 | agent 读不到 | 写 ADR |
| 文档里 hardcode 环境 URL / port | 迁移就死 | 用占位符 + 配置说明 |
| 拼音 / 半英文术语 | 不一致 | 统一术语表 |

## 9. 翻译 / 多语言

- 本仓库默认主语言:**简体中文**(与 `docs/harness-engineering/` 一致)。
- 新增英文文档必须同时保持中文版(`README.md` + `README.en.md` 模式)。
- 术语翻译以 `docs/harness-engineering/08-glossary.md` 为准。
- 只写英文 / 只写中文 = 合入时 `docs` persona review 会 flag。

## 10. 自检清单

- [ ] 我改了接口/行为/架构,是否同步了相应文档?
- [ ] 我做了一项长期决策,是否写了 ADR?
- [ ] 我的 README / docstring / 注释是否给出 "why" 而不只是 "what"?
- [ ] 我新增的术语是否入了 glossary?
- [ ] 我的大文档有没有目录?
- [ ] 我的 PR 里是否显式列出了"文档改动"一节?

## 11. 推荐布局

```
docs/
├── README.md                       # 项目讲解入口
├── architecture/                   # 组件与数据流
├── adr/                            # 历次架构决策
│   ├── 0001-initial-architecture.md
│   └── 0002-...
├── runbooks/                       # 运行 / 故障排查
├── glossary.md                     # 全局术语
└── harness-engineering/            # 本仓库的 harness 精读库
```

`plan/`(长任务用)的典型布局:

```
plan/
├── PROGRESS.md                     # 全局 feature 列表 + 状态
├── HANDOFF.md                      # 最新一次交班
├── sessions/                       # 历次交班归档
│   ├── 001.md
│   └── 002.md
└── decisions/                      # 长任务内的 ADR(可选,或并入 docs/adr/)
```
