# ExecPlan · FU-4 · chore(templates): split PR template into short + full

- **任务 ID**:FU-4 (self-review P0 #4)
- **分类**:`chore` + `harness-change`(PR template 是 harness 的一部分)
- **规模**:S
- **base**:`harness-engineering-setup-v2`
- **版本**:v1

## 1. 目标

把当前 ~120 行、18 字段的 PR 模板拆成 **short / standard / harness-change** 三档,让小任务不再被迫填"影响面 / 观测与告警 / 回滚"这些对 typo 修复毫无意义的字段。

## 2. 动机

self-review P0 #4:真实团队遇到过度规范化的模板会**选择性填写**,一旦选择性填写,"必填"就失效。
`AGENTS.md § 3.4` 要求用模板,但模板不区分规模 —— XS 任务填全套 = 人类拒绝,失效传染到所有 PR。

## 3. 非目标

- 不减损 harness-change 类 PR 的审查深度(full 模板不瘦身)。
- 不自动检测 PR 类型(那是 FU-6 `require-execplan.yml` 的潜在演化方向)。
- 不改 `AGENTS.md § 3.4` 的强制性。

## 4. 影响面

| 路径 | 动作 | 风险 |
|---|---|---|
| `.github/pull_request_template.md` | 替换为 short 版(默认) | 中:所有新 PR 体验变 |
| `.github/PULL_REQUEST_TEMPLATE/standard.md` | 新增(长版) | 低 |
| `.github/PULL_REQUEST_TEMPLATE/harness_change.md` | 新增(最长版,带 DEPRECATION 检查) | 低 |
| `AGENTS.md § 3.4` | 加一段"如何选模板" | 低 |
| `CONTRIBUTING.md` | 顺带指一下 | 低 |

GitHub 支持 `?template=<name>.md` query param;当文件放在 `.github/PULL_REQUEST_TEMPLATE/` 子目录时,默认 fallback 仍是根级 `pull_request_template.md`。

## 5. 方案

### 5.1 三档

| 档 | 触发 | 字段数 |
|---|---|---|
| **short**(默认) | 无 label / typo / bug fix / 小改 | 6 |
| **standard** | `feature` / `refactor` / 任何改了行为的改动 | ~12 |
| **harness-change** | 改 AGENTS / steering / templates / scripts / workflows / tools | ~16(含 DEPRECATION 登记勾选) |

### 5.2 Short 版字段(必填 6)

1. What & Why(1-3 句)
2. Type(radio)
3. How tested
4. Blast radius(单行)
5. Rollback(单行)
6. 自检(5 条复选)

短到"改 typo 不会想跳过"的程度。

### 5.3 Standard 版字段(~12)

保留当前模板的**大部分**字段,但标明哪些是"必填"哪些是"如适用"。

### 5.4 Harness-change 版字段(~16)

在 standard 基础上加:

- **为什么是 harness 改动,不是 prompt 补丁?**
- **DEPRECATION.md 登记 ID 或退役条件**
- **模型版本范围**(如果针对特定模型缺陷)
- **harness-steward persona 结论**占位

## 6. 步骤

- [ ] S1 · 备份当前 `.github/pull_request_template.md` 内容作为 standard 版种子
- [ ] S2 · 新建 `.github/PULL_REQUEST_TEMPLATE/` 目录 + standard.md / harness_change.md
- [ ] S3 · 重写根级 `.github/pull_request_template.md` 为 short 版
- [ ] S4 · 在 short 版顶部写"如果你的改动改了行为/架构/harness,用 `?template=...` 切换到对应模板"
- [ ] S5 · 更新 `AGENTS.md § 3.4` 说明三档
- [ ] S6 · `CONTRIBUTING.md` 加一句指引

## 7. 验收

### 7.1 机器可验证

- [ ] 3 个模板文件存在且非空
- [ ] Short 版 <= 40 行(硬指标)
- [ ] Standard 版保持原有字段的**语义**(不能悄悄丢必填项)
- [ ] Harness-change 版至少包含 "DEPRECATION.md 登记" 字段
- [ ] markdownlint 通过

### 7.2 rubric

| 维度 | 权重 | 标准 |
|---|---|---|
| Short 版真的短 | 30 | ≤ 40 行,6 字段 |
| 覆盖度不丢 | 30 | harness-change 路径的严格度不降 |
| 引导清晰 | 20 | 用户能一眼选到正确模板 |
| 可回滚 | 20 | 单文件替换,revert 简单 |

## 8. 回滚

`git revert`。

## 9. 观测

无。

## 10. 文档

AGENTS.md § 3.4 + CONTRIBUTING.md + 本 ExecPlan。

## 11. Harness 改动

**是**。但**不**登记 DEPRECATION(这是流程松紧的调整,不是对抗模型缺陷)。参考 DEPRECATION § 1 "不需要登记的情况"。

## 12. 未解决

- [ ] Q1:默认模板要选 short 还是 standard?
  - 倾向:**short**(fallback 到最小阻力)。认真的改动作者会自己切换。
  - Fallback:按倾向。

## 13. 时间

~45 分钟 agent + ~5 分钟 human review。

## 14. Checkpoint

- [ ] Plan
- [ ] Review: local markdownlint
- [ ] Acceptance

## 15. 变更历史

| v | date | who | change |
|---|---|---|---|
| v1 | 2026-05-09 | kiro | init |
