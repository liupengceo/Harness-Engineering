---
title: Git / PR / 提交规范
inclusion: always
---

# Git / PR / 提交规范

> 所有任务都适用。具体 CI 门禁由 `.github/workflows/` 定义,这份 steering 规定 **比 CI 严格** 的行为约束(agent 要把一些 CI 还没写的规矩内化)。

## 1. 分支策略

- `main`(或 `master`):永远保持 **green**(lint / type / test 全绿),任何时刻可部署。
- `harness-engineering-setup`、`feature/<short-name>`、`fix/<short-name>`、`chore/<...>`、`harness-change/<...>`:功能分支。
- **禁止**直接推 `main`:走 PR → review → merge。
- **禁止** `push --force` 到 `main` / `master`。对其他分支除非必要不 force-push;若必要,用 `--force-with-lease`,并在 PR 里留痕。
- 分支命名**只用**英文 + `-` + 数字。

## 2. Commit Message 规范

- **格式**: `<type>(<scope>): <subject>`,例如:
  - `feat(api): add pagination to /users`
  - `fix(auth): refresh token expiry check`
  - `docs(harness): add stripe minions chapter`
  - `chore(deps): bump ts to 5.4`
  - `refactor(core): extract plan runner`
  - `test(billing): cover partial refund edge case`
  - `perf(core): cache impact map`
  - `harness(agents): tighten tool list`
- **type** 允许值:
  - `feat` / `fix` / `docs` / `style` / `refactor` / `perf` / `test` / `chore` / `build` / `ci` / **`harness`**(本仓库特有,用于 agent/harness 基线的修改)
- **subject**:祈使句、≤ 72 字符、结尾无句号。
- **body**(可选):
  - 写 **why**,不写 what(diff 能看)。
  - 引用 issue:`Closes #123` / `Refs #456`。
  - 大改必须有 body。
- **尾部**:不要手动加 `Signed-off-by` / `Co-authored-by`(除非真实协作),不要伪造。

### 禁止
- ❌ `fix bug`
- ❌ `update`
- ❌ `WIP`
- ❌ `Merge branch 'main' into ...` 作为单独 commit(用 rebase 保持历史干净;合并 commit 交给 GitHub)。

## 3. 原子提交(Atomic Commits)

- 一个 commit 对应**一件事**,可以独立 revert 而不破坏仓库。
- 自动化产物(formatter / generated code)单独 commit,不和业务改动混在一起。
- 手写 / agent 写的**公共代码 + 生成代码 + lockfile**分为 2~3 个 commit。
- **重命名**或**大移动**单独 commit:`refactor: move foo from a/ to b/`。

## 4. PR 规范(细节)

> 完整结构见 `.github/pull_request_template.md`。这里是行为约束。

### 4.1 大小

- **每个 PR ≤ 400 行 diff**(不含 generated / lockfile / snapshot)。超了拆。
- 实在拆不动 → PR 描述里**显式写明理由 + 预告下一个相关 PR**。

### 4.2 必填

- 意图 / 动机(why)。
- 影响面(impact map)。
- 关联 issue / ExecPlan。
- 验证方式(测试命令、手动步骤、截图)。
- 回滚方案。
- **Harness 变更**(如果动了 AGENTS.md / steering / 工具注册表,必须**勾选**并在正文描述)。

### 4.3 合并

- 合并方式:默认 **squash merge**(保持 `main` 线性)。
- Commit 标题 = PR 标题(符合 § 2)。
- 合并前**所有 CI 必须绿**。
- 合并前**至少一个 human approve**;高风险领域(auth / payment / infra)需 **2 个** approvers,且一个来自领域 owner。

### 4.4 Draft / WIP

- 未准备好 review → **Draft PR**。
- 不要在非 Draft PR 里不断 push 大改:每次大改视为请求重新 review。

## 5. Agent 行为约束

### 5.1 允许
- 自由创建功能分支。
- 自由 rebase 功能分支、自由 force-with-lease 推功能分支。
- 自由 open PR、自由 close 自己的 PR。
- 自由运行 `git log` / `git diff` / `git blame`。

### 5.2 需要人类明示才能做
- 合并到 `main` / `master`。
- 打 tag / release。
- `git push --force-with-lease` 到别人的功能分支。
- 改 `.git/hooks/` 或跳过 hook(`--no-verify`)。
- 修改 `.gitignore` 去掩盖意外提交的文件(应先清历史)。

### 5.3 绝对禁止
- 改 `git config user.*`。
- `push --force` 到保护分支。
- `filter-branch` / `git-filter-repo` 重写公共历史。
- 任何删除分支 + force push 的组合动作,除非在 PR 里被明确要求。

## 6. Pre-commit hooks(推荐)

本仓库建议在 `.pre-commit-config.yaml` 里挂:
- `end-of-file-fixer` / `trailing-whitespace`
- 语言对应的 formatter + linter
- `detect-secrets` / gitleaks
- `markdownlint`(docs)
- `shellcheck`(sh)
- 自定义:检查 PR/commit 是否符合 § 2 规范

Agent 应当始终让 hook 运行;遇到 hook 失败 → 修代码或修配置,**不要 `--no-verify`**。

## 7. 冲突解决

- 冲突发生 → **rebase**,不是 merge(保持线性)。
- 复杂冲突 → 把冲突文件内容以注释化形式列在 PR 评论里,请求人类指引。
- 冲突后**必须重新跑全测试**,不得假设"冲突的行没动就没事"。

## 8. Release / Tag

- Tag 格式:`vMAJOR.MINOR.PATCH`(SemVer)。
- 预发布:`vX.Y.Z-rc.N`、`vX.Y.Z-beta.N`。
- CHANGELOG:**Keep a Changelog** 风格;每次 tag 前更新 `Unreleased` 段。
- Tag 必须在 `main` 上打,且 CI 已绿。

## 9. 自检清单(PR 打开前)

- [ ] 分支名符合规范。
- [ ] Commit 规范(type/scope/subject)。
- [ ] PR ≤ 400 行 diff,或有合理拆分说明。
- [ ] CI 在本地已跑通(test / lint / type)。
- [ ] 引用了 issue / ExecPlan。
- [ ] 标注了 harness-change(如适用)。
- [ ] 没有 force push 过保护分支。
- [ ] 没有 `--no-verify` 绕过 hook。
- [ ] 没有 commit 进仓库的 secret。

## 10. 反模式速查

| 反模式 | 正确姿势 |
|---|---|
| `Merge main` 作为 PR 的最后一个 commit | rebase,保持线性 |
| 一个 PR 混 "重构 + 新功能 + 格式化 + lockfile 更新" | 拆成 2~4 个 PR 或至少拆 commit |
| 直接往 `main` 推 | 所有改动走 PR |
| PR 说明只写 "fix bug" | 写 why + 影响面 + 验证 |
| 把 `.env` 加进 `.gitignore` 来"掩盖"已 commit 的 secret | 撤销凭证 + 清历史 + 改 harness |
| 大改动硬塞进一个 PR "因为要一起上线" | 拆小 + feature flag |
| 改 AGENTS.md 塞在业务 PR 里不声明 | 标 `harness-change`,最好独立 PR |
