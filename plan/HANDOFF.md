# HANDOFF · 最新一次交班

> **读**:每次 session 开始前,agent 必须读这份文件的全部。
> **写**:每次 session 结束前,agent 必须**新建**一份 `sessions/<N>.md` 作为该次交班的归档,并把这份 `HANDOFF.md` **覆写**为最新一次的副本(以便下次一眼看到)。
>
> 非长任务不使用本文件。

## 硬格式(8 个必填段)

每一次交班严格按这 8 段写,缺一不可。

---

## 1. 本次 session 摘要

- **Session 编号**:`<N>`
- **日期**:`YYYY-MM-DD`
- **执行 agent**:`<agent 标识>`
- **人类共驾**:`@someone`
- **对应 ExecPlan**:`plan/execplans/<date>-<slug>.md`
- **持续时长**:`<小时>`

## 2. 本次做了什么

> 只列可归因的事实,不列心得感想。

- 完成 PROGRESS.md feature #2 的 S1–S3 步
- PR:#456 已合(squash)
- 修了 #463 的 bug(并加复现测试 `refund_when_double_submit_*`)
- 新增 ADR:`docs/adr/0023-refund-notification-via-events.md`
- 触发 harness 改动 PR #478(独立):加 `.kiro/steering/caching.md`

## 3. 仓库当前状态

- **main 状态**:`green` / `red`(如果 red,见 § 4)
- **未合 PR**:
  - #478 · harness-change: caching steering(等 human review)
- **未解决 TODO 里最紧的一条**:`src/billing/queue.ts:88 · 需要确认 dead letter topic 名`

**关键命令(本次环境的最后跑通姿态)**:

```bash
pnpm install
pnpm test            # 全绿
pnpm test:integration   # 需要 docker-compose up -d
pnpm build
```

## 4. 遇到的坑 / 已处理未处理

- **P1** · migration `0025_add_refund_email.sql` 在 staging 有 15s lag。已加 `--online` 注释,待 DBA 审批。
- **P2** · `mailer.test.ts` flaky — 本次没修,加了 `.kiro/steering/testing.md § 9` 的引用注释。
- **P3** · `grep` 全仓发现 `user_id` 与 `userId` 并存,未统一。建议下次做个小 chore PR。

## 5. 下一个 session 该做什么

**第一句:先读什么**
1. 读本 `HANDOFF.md` 的 § 4 + § 7。
2. 读 `plan/PROGRESS.md` 的 § 3 "下一步"。
3. 读相关 ExecPlan(若仍在 WIP)。

**然后按优先级:**
1. 推进 PROGRESS.md Feature #2 的 S4(集成测试 + 重试队列)
2. 如果 DBA 审批过了,部署 migration
3. 拿时间的话,起 chore PR 统一 `user_id` 命名

## 6. 待决问题(给人类)

> 这一节是 session 结束时**必须**滚动检查的。如果人类上次的回答已经收到,移除相应条目。

- [ ] **Q1** · 是否允许对 alpha 用户先启用 Feature 2?
  - 我的查询:PR #456 评论 Thread-2。
  - 倾向:可以,但只对 `tenant_id IN (...)` 的显式白名单。
  - Fallback:如果 48h 未回应,不启用,继续做 Feature 3。

## 7. 对 harness 的建议

> 这一节是 harness 的反哺通道。**每次 session** 至少想一条,没有就写 "none + 原因"。

- 建议:把 `grep` 出来的 `userId/user_id` 不一致沉到 `.kiro/steering/code-style.md § 2`,加一条机器化检查脚本。
  - 信号:本次任务反复因此被 review 打回。
  - 行动:**独立 harness-change PR** 在下次 session 提。
- 已提过的 harness 改动:PR #478(见 § 2)。

## 8. 签名

- **agent**:`<agent 标识>` — `YYYY-MM-DD HH:MM`
- **人类复核**:`@owner` — 复核 `[ ]` done / `[ ]` pending

---

> **禁止**:没有本文件或本文件字段不全就开始下一个 session。
> 如果在长任务里发现本文件已过时(某人直接操作了仓库),agent 必须**先写一份 sessions/<N>.md 追认历史**,再继续。
