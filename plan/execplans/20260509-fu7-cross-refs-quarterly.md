# ExecPlan · FU-7 · ci: cross-refs check + quarterly-harness-review

- **任务 ID**:FU-7 (self-review P1 #6 + P1 #9)
- **分类**:`ci` + `harness-change`
- **规模**:S-M
- **base**:`harness-engineering-setup-v2`
- **版本**:v1

## 1. 目标

两条机械化守卫合一个 PR(它们都属于"对 harness 老化的被动防线"):

**A. Cross-reference check**(P1 #6):扫 repo 内所有 markdown 里形如 `AGENTS.md § 3.1`、`.kiro/steering/foo.md § 5` 的引用,确认目标 **section anchor 真的存在**。预防重命名 section 时旧引用悄悄失效,让 agent 读到"指向虚空的规则"。

**B. Quarterly harness review automation**(P1 #9):每季度自动在仓库开一个 issue,附当前 `DEPRECATION.md` 的 Active 条目清单,催促人类 review。防止 DEPRECATION 台账自己老化。

## 2. 动机

- A:`AGENTS.md` + 本仓库的 steering + 精读库里**每段**都可能引用其他 section。一次无意重命名会静默破坏这种引用,而 agent 读到失效引用会放弃或幻觉。
- B:`DEPRECATION.md § 1` 说 "每季度一次整体复审",但**没人**会自动记得。半年后台账变装饰。

## 3. 非目标

- A 不扫**外链死链**(那是 P1 #7,单独 PR)。
- B 不自动 retire 条目(只提醒)。

## 4. 影响面

| 路径 | 动作 |
|---|---|
| `scripts/check_cross_refs.py` | 新增 |
| `.github/workflows/cross-refs.yml` 或合入 `lint.yml` | 新增/改 |
| `.pre-commit-config.yaml` | 加入 cross-refs hook(本地快速反馈) |
| `.github/workflows/quarterly-harness-review.yml` | 新增(cron) |
| `.kiro/steering/DEPRECATION.md` | 加两条登记 |

## 5. 方案

### 5.A Cross-refs

- 扫 markdown 文件。
- 正则匹配形如:
  - `` `some/file.md` § N `` / `` `some/file.md` § N.M ``
  - `some/file.md § N` (in body text)
  - `AGENTS.md § N` / `AGENTS.md § N.M`
  - `.kiro/steering/<name>.md § N`
  - `templates/review-personas/<name>.md § N`
  - `docs/harness-engineering/NN-foo.md § N`
- 解析目标文件(若存在),把 `section ID` (形如 `## 3. foo` / `### 3.1 foo`)抽出。
- 如果引用号不存在 → 报错。
- 正则先保守,允许 false negative;宁可漏也不要 false positive 误杀合法文本。

### 5.B Quarterly

- Scheduled workflow: `cron: '0 10 1 2,5,8,11 *'`(每季度第 1 天 10:00 UTC)。
- Job 用 `actions/github-script`:
  - 读 `DEPRECATION.md`,提取**所有 Active 条目的标题**(简单 regex)
  - 用 `gh issue create` 开一个新 issue,标签 `harness-review`,body 含:
    - 上次 review 的日期(从最近一个带相同 label 的 closed issue 推)
    - Active 条目清单
    - 复审 checklist(5 条问题,来自 DEPRECATION.md § 2)
  - assignee = CODEOWNERS 里的 harness-steward

## 6. 步骤

- [ ] S1 · `check_cross_refs.py` + 5 场景本地测试
- [ ] S2 · 加入 `.pre-commit-config.yaml` 作为 local hook
- [ ] S3 · 合入 `.github/workflows/lint.yml`(PR 时跑)
- [ ] S4 · `quarterly-harness-review.yml`(cron 工作流)
- [ ] S5 · DEPRECATION.md § 7/8 新登记

## 7. 验收

- [ ] cross-refs 扫当前仓库 **0 个 false positive**
- [ ] cross-refs 故意断一条引用 → 正确报错
- [ ] quarterly 工作流 `actionlint` 合法
- [ ] DEPRECATION 两条新登记到位

## 8-15

简化,参照 FU-6。
