<!--
  ExecPlan.md · 执行计划模板
  ================================

  用法:
  1. 每个任务开始前,复制这份模板到:
       plan/execplans/<YYYYMMDD>-<short-slug>.md
       (如果是一次性小任务,直接贴在 PR 描述的第一个段落也可以。)
  2. 填满所有 **必填** 字段。带有 [optional] 的字段按需。
  3. 把这份 plan 放进 PR 的第一个 commit(commit 信息:
       `chore(plan): ExecPlan for <slug>`)。
  4. **人类在 plan checkpoint 通过前,不得开工。**

  这份 plan 的读者优先级:未来的自己 ≥ 接手的 agent ≥ review 人。
  - 写给"三周后忘了这事的自己"能读懂。
  - 不要隐藏已知问题:ExecPlan 的价值就在于暴露。

  相关文件:
  - /AGENTS.md                § 3 任务流程
  - .kiro/steering/harness.md § 2 四条铁律
  - templates/review-personas 多 persona 模板
-->

# ExecPlan · `<任务一句话标题>`

- **任务 ID / Issue**:`<#123 或 JIRA-KEY 或 link>`
- **负责人**:`<@human-owner>` (最终对结果负责的人)
- **执行者**:`<agent 标识 + 人类共驾者>`
- **分类**:`[feature | fix | refactor | perf | chore | harness-change | docs | security]`
- **规模**:`[XS(<1h) | S(半天) | M(1~2天) | L(3~5天) | XL(长任务,走 plan/ 三件套)]`
- **长任务?**:`Yes / No`(如果 Yes,在 `plan/PROGRESS.md` 和 `plan/HANDOFF.md` 也要同步)
- **Plan 版本**:v1(如果 plan 本身迭代过,追加 v2/v3,并在文末记录变更)

---

## 1. 目标(Goal)

一句话说清**要达到什么状态**(面向用户/系统/agent,而非面向代码)。

> 例:"当订单退款时,用户能在 24 小时内收到邮件通知,且邮件内容可审计"。

**不**写成:"在 OrderService 里加一个方法"(那是步骤不是目标)。

---

## 2. 动机与背景(Why)

- 为什么现在做?
- 这个问题的代价是什么?(business cost / engineering cost / risk)
- 关联的讨论 / 历史 PR / incident 编号(最多 5 条,最相关的)。

---

## 3. 非目标(Non-goals)

明确列出 **这次不做** 的事,以免 scope creep。

> 例:
> - 不做邮件模板的 i18n(留给 PR-4567)。
> - 不改变退款审批流程本身。

---

## 4. 影响面 / Impact Map

### 4.1 会被触及的文件 / 模块

| 路径 | 改动类型 | 风险 |
|---|---|---|
| `src/billing/refund.ts` | 修改 | 中:退款核心路径 |
| `src/notifications/mailer.ts` | 新增调用 | 低 |
| `migrations/0025_add_refund_email.sql` | 新增 migration | 中:prod schema |

### 4.2 下游影响(谁会感觉到这次改动)

- 用户 / 调用方 / 客服流程 / 运维 / SDK 用户 / 其他 agent 的假设?

### 4.3 上游依赖(做这件事需要谁)

- 新依赖?第三方服务?feature flag?secret?

### 4.4 Blast radius 评估

- 如果**最坏情况**这次改动全错了,影响范围 = ?
- 回滚难度 = ?(分钟 / 小时 / 天 / 不可回滚)

---

## 5. 方案(Approach)

### 5.1 选择的方案

用 5–15 行写清楚**怎么做**。伪代码/接口签名/数据流图都可以。

### 5.2 候选方案(Considered Alternatives)

至少列 1–2 个放弃的方案 + 放弃理由。

| 方案 | 要点 | 为什么放弃 |
|---|---|---|
| A · 同步发邮件 | 简单 | 阻塞退款主路径,延迟 |
| B · 用 cron 扫未通知退款 | 解耦 | 延迟 > 24h 场景难保证 |
| **C(选中)** · 事件总线 + 重试队列 | 解耦 + SLA 可控 | 为选中理由 |

### 5.3 类比 / 抄参考

- 仓库内已有类似模式?(grep 结果贴一行文件路径 + 简评)
- 外部参考?

---

## 6. 步骤(Steps)

> 每一步都应该是**一个可独立 commit、可独立跑测试**的粒度。
> 建议 3~8 步之间;超过 10 步考虑拆任务。

- [ ] **S1 · 建立 migration 与 feature flag(关闭状态)**
  - 文件:`migrations/0025_*.sql`、`config/flags.ts`
  - 验证:本地跑 `db:migrate:up` / `db:migrate:down` 均 OK
  - 风险:prod 上线需要 DBA 审核窗口

- [ ] **S2 · 在 billing domain 引入 `RefundNotified` 事件**
  - 文件:`src/billing/events.ts`、`src/billing/refund.ts`
  - 验证:单测 `refund.test.ts` 新增 2 条用例
  - 风险:低

- [ ] **S3 · notifications 侧消费者 + 模板**
  - 文件:`src/notifications/handlers/refund-notified.ts`
  - 验证:单测 + contract test
  - 风险:低

- [ ] **S4 · 集成测试 + 重试队列**
  - 文件:`tests/integration/refund-email.int.test.ts`
  - 验证:
    - 正常路径 × 1
    - 失败重试 × 1
    - 超过最大重试后的 dead letter × 1
  - 风险:低

- [ ] **S5 · 打开 feature flag 前的 readiness check**
  - 文件:`runbooks/refund-email-rollout.md`
  - 验证:runbook 经 ops 审读。

---

## 7. 验收标准(Acceptance Criteria)

> **机器可验证 + 人类可 rubric** 二选一,最好两者都有。

### 7.1 机器可验证

- [ ] 所有新增测试通过。
- [ ] `tests/integration/refund-email.int.test.ts` 覆盖 § 6 S4 的 3 条用例。
- [ ] Lint / type / 覆盖率门禁全绿。
- [ ] `RefundNotified` 事件 schema 纳入 `schemas/events/`,contract test 绿。

### 7.2 人类 rubric

| 维度 | 权重 | 打分标准 |
|---|---|---|
| 正确性 | 30 | 指定场景下行为与 spec 一致 |
| 可观测性 | 20 | log/metrics/trace 能定位失败 |
| 可回滚性 | 20 | 关 flag 即可,0 副作用 |
| 可维护性 | 20 | 命名清晰 / 注释 why / 文档齐全 |
| 安全 | 10 | 无 PII 泄露到 log,无权限越界 |

**总分 ≥ 85 方可合入。**

---

## 8. 回滚计划(Rollback)

- 关闭 `FLAG_BILLING_REFUND_EMAIL`。
- 如果 migration 有问题:`migrations/0025_*.sql` 提供了 down 脚本,跑 `db:migrate:down`。
- 最差情况:`git revert <commit-hash>`,重启 queue worker。
- 上线后若发现**不一致数据**,用 `scripts/refund-email-reconcile.ts` 做补发。

---

## 9. 观测与告警(Observability)

- **新增 log 事件**:
  - `refund.notified` (level: info, fields: `refund_id`, `user_id[masked]`, `template_id`)
  - `refund.notify_failed` (level: warn, fields: `refund_id`, `attempt`, `reason`)
- **新增 metric**:
  - `refund_notify_latency_seconds` (histogram)
  - `refund_notify_retry_total` (counter)
- **新增告警**(如需):
  - 重试率 5 分钟 > 5% → P3 告警
  - Dead letter 1 小时 > 10 → P2 告警

---

## 10. 文档与 ADR

- [ ] 更新 `docs/billing/refund.md` 说明通知机制。
- [ ] 如涉及架构决策,写 ADR `docs/adr/NNNN-refund-notification.md`。
- [ ] 如果改了公共接口或行为,更新 CHANGELOG `Unreleased`。

---

## 11. Harness 改动(如有)

> 如果这个任务要改 `AGENTS.md` / `.kiro/steering/` / 工具注册表 / CI,请在这里单独列出。
> **强烈建议**:把 harness 改动拆成独立 PR,不要和业务改动混合。

- [ ] 无 harness 改动。

或者:

- [ ] `AGENTS.md § X.Y` 改为 ...
- [ ] 新增 `.kiro/steering/<file>.md`:原因 ...
- [ ] 登记 `DEPRECATION.md` 条目 # ...

---

## 12. 未解决问题 / 需要人类决策

列出 **plan checkpoint 时希望人类帮忙决策** 的问题。每条给出:

- 问题
- 已经查过的资料
- 你倾向的方案
- 如果未回应,你的 fallback

> 例:
> - **Q**:`RefundNotified` 事件要不要包含商家自定义字段?
>   - 查过:`docs/billing/event-schema.md` 未明说。相关 issue #812。
>   - 倾向:**不要**,靠 `refund_id` 后续查即可,减少 event payload。
>   - Fallback:如果 48h 未决,按倾向方案实现,在 v2 plan 可追加。

---

## 13. 时间估计 & 依赖

- 估计 agent 工时:`<N 小时>`
- 估计人类 review + checkpoint:`<N 分钟>`
- 依赖:
  - DBA 审核 migration 窗口
  - ops 审 runbook
  - #billing-core 团队 owner ack

---

## 14. Checkpoint 签名

- [ ] **Plan checkpoint**(人类):`@name` · `YYYY-MM-DD` · 决议:`approve / approve-with-changes / reject`
- [ ] **Review checkpoint**(review personas):见 PR 里的 `/review` 报告
- [ ] **Acceptance checkpoint**(人类):`@name` · `YYYY-MM-DD` · rubric 总分:`__ / 100`

---

## 15. Plan 变更历史

| 版本 | 日期 | 改了什么 | 谁 |
|---|---|---|---|
| v1 | YYYY-MM-DD | 初版 | @author |
| v2 | YYYY-MM-DD | 把 S3 拆成 S3a/S3b,理由 ... | @author |
