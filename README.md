# kiro.dev · Harness Engineering 起步仓库

> 这个仓库是一个**"Harness Engineering 起步套件"**。它**本身**就是一份可直接复用的脚手架,用来把 OpenAI、Anthropic、Stripe、Shopify、Martin Fowler 站的 harness engineering 实践落到一个真实的工程仓库里。
>
> 如果你是 agent:先读 [`AGENTS.md`](./AGENTS.md),然后读 [`.kiro/steering/harness.md`](./.kiro/steering/harness.md)。
>
> 如果你是人类工程师:先读 [`docs/harness-engineering/README.md`](./docs/harness-engineering/README.md)。

---

## 目录结构

```
.
├── README.md                              # 你现在在读的文件
├── AGENTS.md                              # 仓库根级 agent 约束基线
├── .kiro/
│   └── steering/                          # 按主题拆分的 steering 规则
│       ├── README.md
│       ├── harness.md                     # Harness 核心约束(所有 agent 必读)
│       ├── code-style.md                  # 代码风格与命名
│       ├── testing.md                     # 测试约定
│       ├── security.md                    # 安全红线(最高优先级)
│       ├── docs.md                        # 文档 / ADR / 注释
│       ├── git-workflow.md                # Git / PR / 提交规范
│       └── DEPRECATION.md                 # Harness 老化对抗台账
├── docs/
│   └── harness-engineering/               # 中文精读库
│       ├── README.md
│       ├── 00-overview.md                 # 一页总览
│       ├── 01-openai-harness.md           # OpenAI 精读
│       ├── 02-anthropic-harness.md        # Anthropic 三篇
│       ├── 03-stripe-minions.md           # Stripe Minions
│       ├── 04-shopify-roast.md            # Shopify Roast
│       ├── 05-martin-fowler.md            # Martin Fowler / on-the-loop
│       ├── 06-methodology.md              # 方法论骨架
│       ├── 07-practice-checklist.md       # 明天就能干的事
│       ├── 08-glossary.md                 # 术语表
│       └── 09-references.md               # 参考文献
├── templates/
│   ├── ExecPlan.md                        # 执行计划模板(任务必用)
│   └── review-personas/                   # 评审 persona 套装(8 份)
│       ├── README.md
│       ├── harness-steward.md
│       ├── security.md
│       ├── testing.md
│       ├── api-design.md
│       ├── performance.md
│       ├── observability.md
│       ├── docs.md
│       └── orchestrator.md
├── plan/                                  # 长任务记忆三件套
│   ├── PROGRESS.md                        # 全局 feature 列表 + 状态
│   ├── HANDOFF.md                         # 最新一次交班(session 结束写)
│   ├── execplans/                         # 每任务 ExecPlan 归档
│   │   └── .gitkeep
│   ├── sessions/                          # 历次会话交班归档
│   │   └── .gitkeep
│   └── decisions/                         # 长任务内的 ADR(可选)
│       └── .gitkeep
└── .github/
    ├── pull_request_template.md           # PR 模板(必填项)
    └── ISSUE_TEMPLATE/
        ├── config.yml
        ├── task.md                        # 交给 agent 的任务
        ├── bug_report.md
        └── harness_change.md
```

## 六个核心文件(按重要性排)

1. **[AGENTS.md](./AGENTS.md)** — 仓库对 agent 的契约。
2. **[.kiro/steering/harness.md](./.kiro/steering/harness.md)** — Harness 四条铁律。
3. **[.kiro/steering/security.md](./.kiro/steering/security.md)** — 安全红线(永远最高优先级)。
4. **[templates/ExecPlan.md](./templates/ExecPlan.md)** — 所有任务开工前的结构化计划模板。
5. **[.github/pull_request_template.md](./.github/pull_request_template.md)** — 没填这份 PR 不合入。
6. **[docs/harness-engineering/07-practice-checklist.md](./docs/harness-engineering/07-practice-checklist.md)** — 从 0 到跑通的落地清单。

## 三分钟入门

1. Agent 第一次进来 → 读 `AGENTS.md` + `.kiro/steering/harness.md`。
2. 接到任务 → 产出 `templates/ExecPlan.md` 的填好版本(或放入 `plan/execplans/`)。
3. Plan checkpoint 通过 → 开工,按步骤 commit,走完本地 test/lint/type。
4. 开 PR → 用 `pull_request_template.md`,勾好要调度的 review persona。
5. Persona + CI 全绿 → 人类做 acceptance checkpoint。
6. 合入 → 如果是长任务,同步 `plan/PROGRESS.md` + 写 `plan/HANDOFF.md`。

## 本仓库的硬规定(摘录)

- **没 ExecPlan 的 PR,一律不合。**
- **没 acceptance 的 issue,一律回退。**
- **同类错误第二次出现,触发 harness 改动 PR。**
- **harness 改动 独立 PR**,标 `harness-change` 标签,登记 `DEPRECATION.md`。
- **安全红线(`security.md § 1`)触发 → 立即停手,等人。**

## 方法论一句话

> **Agent = Model + Harness.**
> **Humans steer. Agents execute.**
> **Fix the harness, not the output.**

## 来源与致谢

- OpenAI《Harness engineering: leveraging Codex in an agent-first world》
- Anthropic《Harness design for long-running application development》
- Anthropic《Effective harnesses for long-running agents》
- Stripe《Minions》Part 1 & 2
- Shopify《Introducing Roast》
- Martin Fowler 站《Harness Engineering — first thoughts》、《Humans and Agents in Software Engineering Loops》

详细来源见 [docs/harness-engineering/09-references.md](./docs/harness-engineering/09-references.md)。

## Contributing

贡献指南见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

关键要点:

- 这个仓库是 starter kit,通常你**应该 fork 后改**,而不是把业务规则 PR 回来。
- 所有改动走 `AGENTS.md § 3` 的标准流程(ExecPlan → plan checkpoint → code → review persona → CI → human acceptance)。
- Harness 改动(`AGENTS.md` / `.kiro/steering/` / `templates/` / `scripts/` / `.github/workflows/`)要独立 PR,带 `harness-change` label。

## 行为规范

本项目采用 [Contributor Covenant v2.1](./CODE_OF_CONDUCT.md)。

## 安全

**不要**在公开 issue 里报漏洞。见 [SECURITY.md](./SECURITY.md)。

## License

本仓库采用 [Apache License, Version 2.0](./LICENSE)。

核心意思(不构成法律意见):

- 你可以**免费**使用、修改、再分发本仓库内容,包括用在 proprietary 项目里。
- 你的 fork 必须保留 LICENSE + 显著标注你对文件的修改。
- 本仓库给予你专利 grant,但如果你为此发起专利诉讼,grant 自动终止。
- **本仓库按 "AS IS" 提供,无任何明示或暗示的担保。**
