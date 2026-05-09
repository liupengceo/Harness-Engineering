# ExecPlan · FU-2 · fix(review): abstain verdict + banner

- **任务 ID**:FU-2 (self-review P0 #3)
- **负责人**:@repo-owner
- **执行者**:kiro agent
- **分类**:`fix` + `harness-change`(修 review schema,属于 harness)
- **规模**:S(半天)
- **base 分支**:`ci/review-personas-workflow`(本 PR 依赖 PR #3 引入的 script,必须基于它)
- **长任务?**:本 PR 是 self-review 长任务的第 2 个 PR
- **Plan 版本**:v2(v1 曾想 base 在 `harness-engineering-setup-v2`;实际文件在 #3 分支才有,已修正)

## 1. 目标

把 `scripts/run_review_persona.sh` 在 `REVIEW_RUNNER=abstain` 时的输出从**误导性的 `verdict: approve`** 改为**语义明确的 `verdict: abstain`**,并让 `scripts/aggregate_reviews.py` 在整份聚合为 abstain 时**在 PR 评论顶部打显眼横幅**,阻止"反正 bot 过了"的懒惰习惯。

## 2. 动机

self-review P0 #3:现有 #3 合入后,所有 PR 评论顶部会写 `Overall verdict: approve`,即使**根本没有任何 agent 做过评审**。这养成"bot 绿 = 万事大吉"的反射,与 `.kiro/steering/harness.md § 7 "verified" 的新定义`冲突。

## 3. 非目标

- 不接入任何真实 agent 平台(留给 ADR-0002)
- 不改 6 个 persona 的 rubric 文本
- 不改 `select_personas.py`

## 4. 影响面

### 4.1 文件

| 路径 | 改动类型 | 风险 |
|---|---|---|
| `scripts/run_review_persona.sh` | 改 abstain 分支 YAML + 加 validator 调用 | 中 |
| `scripts/aggregate_reviews.py` | rollup 规则 + banner + 全-abstain 路径 | 中 |
| `scripts/validate_persona_output.py` | **新增** | 低 |
| `templates/review-personas/README.md` | § 3 § 4 enum + 输出契约 | 低 |
| `.kiro/steering/DEPRECATION.md § 8` | 新增一条 abstain 语义 | 低 |

### 4.2 下游影响

- Fork 若自己已 patch 过 `aggregate_reviews.py`:收到新 `abstain` enum,需要一行兼容(加入 `VERDICT_RANK`)。**本 PR 写兼容路径**:未识别的 verdict 视作 `approve-with-changes` 并给 warning。

### 4.3 Blast radius

- 最坏:aggregate 产出 markdown 语法错,评论渲染乱。
- 回滚:`git revert`。

## 5. 方案

### 5.1

1. verdict 加枚举 `abstain`。
2. `roll_up_verdict`:**全 abstain → abstain;混合 → 跳过 abstain**。
3. `render_markdown`:
   - 全 abstain → 顶部替换为 `⚠️ **Review workflow abstained**` banner,不写 "Overall verdict"
   - 混合 → 正常 Overall verdict,但在 banner 区警示 "N persona(s) abstained"
4. `validate_persona_output.py`:必需字段 + verdict enum + 禁 code fence / 禁前后非 YAML 文本。
5. `run_review_persona.sh` 4 分支结尾都 pipe 过 validator(失败时 exit 3,CI step 失败 → orchestrator aggregate 跳过坏报告)。

### 5.2 候选(已在 ExecPlan v1 中记录;略)

## 6. 步骤

- [ ] **S1** · 更新 `templates/review-personas/README.md` § 3 enum 加 abstain;§ 3 加"adapter 必须输出 raw YAML 到 stdout,不得代码围栏包裹"条款
- [ ] **S2** · 改 `scripts/run_review_persona.sh` 的 abstain 分支文案
- [ ] **S3** · 新增 `scripts/validate_persona_output.py`
- [ ] **S4** · `run_review_persona.sh` 4 runner 分支末尾都 pipe validator
- [ ] **S5** · 改 `scripts/aggregate_reviews.py`:VERDICT_RANK 加 abstain;rollup 规则;render_markdown banner
- [ ] **S6** · 本地 smoke:模拟 3 场景(全 abstain / 全真 / 混合)
- [ ] **S7** · 登记 `.kiro/steering/DEPRECATION.md § 8`

## 7. 验收

### 7.1 机器可验证

- [ ] validator 拒绝:code fence 包裹的 YAML / 缺 persona / 缺 verdict / verdict 不在 enum
- [ ] `run_review_persona.sh` REVIEW_RUNNER=abstain 输出的 YAML 通过 validator
- [ ] aggregate 在 **全 abstain** 输入产出带 `⚠️ Review workflow abstained` banner 的 markdown
- [ ] aggregate 在 **混合**(1 abstain + 1 approve)产出包含 "1 persona abstained" 的 banner,overall = approve
- [ ] aggregate 在 **全真 review**(1 approve + 1 request-changes)产出 overall = request-changes,不含 abstain banner

### 7.2 rubric

见上文 v1,不变。

## 8. 回滚

`git revert`。

## 9. 观测

无。

## 10. 文档

- README § 3
- DEPRECATION § 8

## 11. Harness 改动

是。本 PR 仅包含 harness 改动(+ ExecPlan + DEPRECATION 登记),不混业务。

## 12. 未解决

- [ ] Q1:abstain 要 block merge 吗?倾向不 block。Fallback:不 block。

## 13. 时间

~1h agent + ~5min human review。

## 14. Checkpoint

- [ ] Plan:__
- [ ] Review:local smoke
- [ ] Acceptance:__

## 15. 变更历史

| 版本 | 日期 | 改了什么 | 谁 |
|---|---|---|---|
| v1 | 2026-05-09 | 初版(base 错) | kiro |
| v2 | 2026-05-09 | 修正 base 到 `ci/review-personas-workflow` | kiro |
