# ExecPlan · FU-3 · docs(repo): LICENSE + CODEOWNERS + CONTRIBUTING + .env.example

- **任务 ID**:FU-3 (self-review P0 #10 + P1 #11)
- **负责人**:@repo-owner
- **执行者**:kiro agent
- **分类**:`docs`(table-stakes 补齐;零代码改动)
- **规模**:S
- **base**:`harness-engineering-setup-v2`
- **Plan 版本**:v1

## 1. 目标

补齐一个"**对外可见**的 starter kit"应有的 table-stakes 文件,确保**别人实际可以复用**这个仓库:

- `LICENSE` — 没它,严格意义上没人能合法 fork/use 这个 kit。
- `CODEOWNERS` — 把"harness 改动必须经 steward 审"从约定升级为 GitHub 原生保护。
- `CONTRIBUTING.md` — 给第一次来的人一个入口(不是所有人都知道 `AGENTS.md` 是什么)。
- `CODE_OF_CONDUCT.md` — 社区默认期望。
- `.env.example` — 让 secret 管理流程(`security.md § 5`)有一个占位符起点。
- `SECURITY.md` — 漏洞披露流程。

## 2. 动机

self-review P0 #10 + P1 #11:

- 仓库 `README.md` 用 "starter kit" 自称,但缺 LICENSE —— 这是**合规硬伤**。
- `.gitignore` 里写了 `!.env.example`(允许入库)但文件不存在 —— 死路径。
- `AGENTS.md § 8` 讲红线,但 `SECURITY.md` 缺失让**外部**报告漏洞者找不到入口。
- 对一个希望被 fork 的 starter kit,CONTRIBUTING 缺失会让外部贡献者直接放弃。

## 3. 非目标

- 不起一个复杂的 issue triage 流程(现有 issue 模板够用)。
- 不改 `AGENTS.md` 的内容(CONTRIBUTING 只是 "go read AGENTS.md" 的桥梁)。
- 不引入真实依赖管理 / SBOM / security scanning(那需要真实代码)。

## 4. 影响面

### 4.1 文件

| 路径 | 动作 | 风险 |
|---|---|---|
| `LICENSE` | 新增(Apache-2.0) | 低(法律兜底,不影响代码) |
| `CODEOWNERS` | 新增 | 低(保护 harness 改动) |
| `CONTRIBUTING.md` | 新增 | 低 |
| `CODE_OF_CONDUCT.md` | 新增(Contributor Covenant v2.1 节选) | 低 |
| `SECURITY.md` | 新增 | 低 |
| `.env.example` | 新增(占位) | 低 |
| `README.md` | 追加"License"与"Contributing"两节 | 低 |
| `.kiro/steering/DEPRECATION.md` | 不需要改(这些不是"对抗模型缺陷的约束") | — |

### 4.2 下游

- Fork 可以**合法**使用本 kit。
- GitHub 默认从 CODEOWNERS 要求 reviewer,首次合入可能卡住。在 CODEOWNERS 里我**只标记"建议",不强制**(用软关键字),依靠 branch protection 决定是否硬阻断。

### 4.3 Blast radius

- 几乎零 —— 全是新文件 + README 追加。revert 1 分钟。

## 5. 方案

### 5.1 License 选择:**Apache-2.0**

理由:

- 这个仓库的价值**在文档/脚本/模板**;用户可能把它**直接复制**进自己的 proprietary 仓库。
- MIT 太宽松(无专利授予);GPL 会污染下游 fork 的 license。
- Apache-2.0 给用户显式专利授予,同时允许他们在 proprietary 项目中使用。

### 5.2 CODEOWNERS 策略

- 所有**harness 相关路径**(`AGENTS.md`, `.kiro/steering/`, `templates/review-personas/`, `scripts/check_*`, `.github/workflows/`, `docs/adr/`, `docs/harness-engineering/`)→ owner = `@liupengceo`(可以加团队)。
- 普通路径不设 owner。

### 5.3 CONTRIBUTING 内容

- 1 段式 "hello, start here"
- 把人引到:`README.md` → `AGENTS.md` → `docs/harness-engineering/` → ExecPlan 模板
- 明确"这个仓库是**你自己仓库的模板**,你大概率想 fork 而不是直接 PR 来加你的业务规则"

### 5.4 CODE_OF_CONDUCT

引用 Contributor Covenant 2.1,不重新发明。

### 5.5 SECURITY.md

- 漏洞报告入口(private security advisory 或 email)
- 范围:脚本 / 工作流的安全问题;不覆盖 "fork 后你自己项目的问题"

### 5.6 .env.example

- 只列**本仓库**会用到的 env:
  - `REVIEW_RUNNER` (abstain / codex / claude-code / custom)
  - `REVIEW_MODEL` (optional)
  - `CUSTOM_REVIEW_CMD` (custom 模式下)

## 6. 步骤

- [ ] **S1** · 起草 LICENSE(Apache-2.0 原文,版权 holder 留占位)
- [ ] **S2** · 起草 CODEOWNERS,引用路径
- [ ] **S3** · 起草 CONTRIBUTING.md,3 段式入门
- [ ] **S4** · 起草 CODE_OF_CONDUCT.md(CC 2.1 节选 + 本仓库联系方式)
- [ ] **S5** · 起草 SECURITY.md(报告流程 + 范围)
- [ ] **S6** · 起草 .env.example
- [ ] **S7** · 在 `README.md` 追加 "License" + "Contributing" + "Security" 三节
- [ ] **S8** · 本地自检:`scripts/check_cross_refs.py`(如果存在) + 手工 grep 所有新路径被正确引用

## 7. 验收

### 7.1 机器可验证

- [ ] 6 个新文件存在且非空
- [ ] `LICENSE` 头部包含 "Apache License, Version 2.0"
- [ ] `CODEOWNERS` 语法合法(每行 `<pattern> @<user>`)
- [ ] `README.md` 含 "License" / "Contributing" / "Security" section 标题
- [ ] 本 PR 所有新文件都**没有**真实 secret / 真实邮箱(用占位符 `security@<domain>`)

### 7.2 rubric

| 维度 | 权重 | 标准 |
|---|---|---|
| 合规完备 | 40 | License / CoC / Security / Contributing 齐 |
| 可用性 | 30 | 外部贡献者读完一圈能开工 |
| 一致性 | 20 | 术语、链接与既有 AGENTS/steering 对齐 |
| 可回滚 | 10 | 全新文件,revert 0 副作用 |

**≥ 85 合入。**

## 8. 回滚

`git revert`。

## 9. 观测

无。

## 10. 文档

本 PR **就是**文档。

## 11. Harness 改动

**边缘情况**。CODEOWNERS 对 harness 路径加强保护,算弱 harness-change。但**不**改 AGENTS.md / steering 内容,不加 tool,不改 persona。标 `harness-change` 过度,但在 PR 描述里显式说明 CODEOWNERS 的保护范围。

## 12. 未解决

- [ ] **Q1**:License 选 Apache-2.0 vs MIT?
  - 倾向:Apache-2.0(专利条款 + 允许 proprietary 使用)。
  - Fallback:48h 无回应,按倾向。
- [ ] **Q2**:CODEOWNERS 的 owner 用个人账号 `@liupengceo` 还是建一个 team?
  - 倾向:个人(仓库规模小)。
  - Fallback:按个人。
- [ ] **Q3**:SECURITY.md 的报告入口:GitHub Private Vuln Report vs email?
  - 倾向:Private Vuln Report(零运维成本)。
  - Fallback:按倾向。

## 13. 时间

~30 分钟 agent;~5 分钟 human review。

## 14. Checkpoint

- [ ] Plan:__
- [ ] Review:local grep of cross-refs
- [ ] Acceptance:__

## 15. 变更历史

| v | date | who | change |
|---|---|---|---|
| v1 | 2026-05-09 | kiro | 初版 |
