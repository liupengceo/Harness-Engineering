# 贡献指南 / Contributing

> **This repository is a starter kit.** If you want to apply its ideas to your own project, the right move is usually to **fork it and adapt**, not to PR your business rules back here.
>
> 这个仓库是**起步套件**。如果你想把它的想法用到你自己的项目上,正确的姿势通常是**先 fork 再改**,而不是把你的业务规则 PR 回来。

## 谁适合来 PR

这里**接受**:

- 修 bug(脚本、模板、CI、文档中的事实错误)
- 补齐 starter kit 本身的缺失(例如 "少了一种 review runner adapter")
- 扩展精读库中外部来源的准确性(新增权威资料 / 修正误传)
- 改进 workflow 的正交性 / 减少启发式规则的误报
- 翻译、改错字、排版

这里**不接受**(请在你自己的 fork 做):

- 你业务项目特有的 steering 条目
- 你团队特有的 review persona
- 改成你团队偏好的 git / PR 工作流
- 把某条"强制"改成"可选"因为你自己不喜欢

## 开工前先做两件事

1. **读 [AGENTS.md](./AGENTS.md)**。这是整个仓库的 agent / 人类共同契约。如果你觉得繁琐:本 kit **就是**关于"把繁琐的东西系统化"的。
2. **读 [docs/harness-engineering/README.md](./docs/harness-engineering/README.md)**。至少扫一遍 `00-overview.md` 与 `07-practice-checklist.md`,你会理解为什么我们坚持这么多看起来多余的 checkpoint。

## 开始一次改动的标准姿势

这也是 **[AGENTS.md § 3](./AGENTS.md) 的流程** —— 不是为你发明的,是整个仓库的默认。

```
  1. 起一个 Task issue  (用 .github/ISSUE_TEMPLATE/task.md)
  2. 复制 templates/ExecPlan.md 填好,放到 plan/execplans/<date>-<slug>.md
     或者 PR 的第一个 commit
  3. 等 plan checkpoint  (人类 review plan diff,不是 code diff)
  4. 开 worktree 写代码 + 测试
  5. 本地跑 pre-commit (见下文)
  6. 开 PR,用 .github/pull_request_template.md
  7. 等 CI + 人类 acceptance
```

**硬规定(摘录,权威在 AGENTS.md):**

- 没 ExecPlan 的 PR **一律不合**。
- 没 acceptance 标准的 issue **一律回退**。
- Harness 改动(`AGENTS.md` / `.kiro/steering/` / `templates/` / `scripts/`)**必须**独立 PR,标 `harness-change` label。
- **永远**不要 `git push --force` 到 `main`/`master`,不要用 `--no-verify` 绕 hook。
- 触发 `.kiro/steering/security.md § 1` 的红线 → **立即停手,等人**。

## 本地开发环境

```bash
pip install pre-commit pyyaml
pre-commit install
pre-commit install --hook-type commit-msg
```

一次性跑全量:

```bash
pre-commit run --all-files
```

CI 工作流(`.github/workflows/lint.yml`)会跑**同一套** hooks。本地过 = CI 过。

## Review 流程

- CI 的 `review-personas` 工作流会根据 diff 自动调度若干 review persona(security / testing / api-design / performance / observability / docs / harness-steward)。
- 默认 `REVIEW_RUNNER=abstain`,意味着没有真实 agent 评审过你的 PR — bot 评论里会有 **:warning:** 横幅提示你这不是"approve"。
- 在 fork 里,你可以把 repo variable `REVIEW_RUNNER` 改成 `codex` / `claude-code` / `custom` 接入真实 agent。
- 详见 [templates/review-personas/README.md](./templates/review-personas/README.md)。

## 行为规范

本项目采用 [Contributor Covenant v2.1](./CODE_OF_CONDUCT.md) 作为行为规范。任何形式的骚扰 / 歧视 / 人身攻击不被接受;报告入口见该文件。

## 安全问题

**不要**在公开 issue 里报告安全漏洞。见 [SECURITY.md](./SECURITY.md)。

## 授权

你提交的改动以 [Apache License 2.0](./LICENSE) 授权。提交 PR 即视为同意这一点。

## 问题 / 建议

- 想法、讨论、"可以这样做吗" → GitHub Discussions(不要开 issue)
- 具体任务 → 用 [Task issue template](./.github/ISSUE_TEMPLATE/task.md)
- Bug 报告 → 用 [Bug report template](./.github/ISSUE_TEMPLATE/bug_report.md)
- Harness 改动提议 → 用 [Harness change template](./.github/ISSUE_TEMPLATE/harness_change.md)

---

If this is your first time working in an "agents steer execution" repo, please take the time to read AGENTS.md carefully — it will save you and the reviewers hours of back-and-forth.
