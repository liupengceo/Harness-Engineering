# PROGRESS · 长任务全局进度

> **这份文件是长任务的"全局仪表盘"**。
> 每次 session 开始前,agent 必须读它;每次 session 结束前,agent 必须更新它。
>
> 读取优先级:仅次于 `AGENTS.md` / `.kiro/steering/harness.md` 与最近一条 `HANDOFF.md`。
>
> 非长任务(XS/S/M 规模),不使用这个文件——它们走 issue + 单 PR 即可。

## 如何使用

1. **新建长任务**:复制本文件到对应分支 / 子目录(或就在 main 上维护),填 § 1 ~ § 4。
2. **日常维护**:每次 session 结束,刷新 § 2 的完成状态、§ 3 的"下一步"、§ 4 的"已发现的坑"。
3. **交班**:写**一份新** `HANDOFF.md`(或 `sessions/<N>.md`),别直接覆写历史。

---

## 0. 元信息

- **长任务名称**:`<e.g. 建立 billing v2 模块>`
- **创建日期**:`YYYY-MM-DD`
- **owner**:`@human-owner`
- **主要执行 agent**:`<agent 标识>`
- **预计持续**:`<周 / 月>`
- **相关 issues / 分支**:`#... / feature/...`

## 1. 目标(Goal)

用 3~5 句话说清"做完这件事时,系统会是什么样子"。**不要**列步骤,**不要**写成 todo。

## 2. Feature List + 状态

| # | Feature / 子目标 | 状态 | 负责 session | PR | 备注 |
|---|---|---|---|---|---|
| 1 | `<e.g. 建立新的 refund schema>` | Done | #001 | #412 | 已合并 |
| 2 | `<...>` | In progress | #003 | #456 | 卡在 migration 审批 |
| 3 | `<...>` | Todo | - | - | - |
| 4 | `<...>` | Blocked | - | - | 等 ops 迁 redis |

状态取值:`Todo` / `In progress` / `Blocked` / `Done` / `Dropped`。

## 3. 下一步(Next up)

按优先级列 1~3 件:

- [ ] **#1 · <小标题>**:接下来要做什么具体事情 + 涉及的 feature
- [ ] **#2 · ...**
- [ ] **#3 · ...**

## 4. 已发现但未解决的坑(Known issues)

| # | 现象 | 触发条件 | 当前对策 | 长期方案 |
|---|---|---|---|---|
| 1 | `<e.g. 并发退款时偶发 duplicate key>` | 压测 > 200 qps | 退避重试 | 数据层加 idempotency token |
| 2 | ... | | | |

## 5. 架构/接口 关键决策索引(ADR)

- ADR-0023 · 退款通知走事件总线 → `docs/adr/0023-...md`
- ADR-0024 · 新 schema 命名与旧字段映射 → `docs/adr/0024-...md`

## 6. 指标 / 可观察性

- 量化目标(做到什么才算"成功达成"):
  - `<e.g. refund 通知送达率 ≥ 99.9% within 24h>`
- 当前指标(从 dashboard 抓,填快照):
  - ...

## 7. 人类决策悬而未决(Open questions)

列出需要人类拍板但 agent 无法自决的事:

- [ ] **Q1** · ...(见 `sessions/<N>.md` § 12)

## 8. Session 摘要索引

> 最新在上。每次 session 结束后,把对应的交班文件追加到这里。

- `sessions/003.md` · YYYY-MM-DD · 做了 #2,卡在 migration
- `sessions/002.md` · YYYY-MM-DD · 完成 #1 并合入
- `sessions/001.md` · YYYY-MM-DD · 初始化仓库,写本文件 v1

---

## 示例(参考,不要留在实际任务里)

> 下面是一个示例,便于初次使用的 agent / 人类理解格式。真实长任务启动时请把这段删除。

- Feature 1:建立新的 `refunds.v2` schema → **Done** (PR #412)
- Feature 2:通知走 event bus → **In progress**,卡在 ops 审批
- Feature 3:retry 队列 + dead letter → **Todo**
- Feature 4:旧客户端兼容层 → **Todo**,依赖 Feature 2

Next up:
- [ ] 推进 Feature 2 的 ops 审批(owner 已 ping)
- [ ] 并行起 Feature 3 的 plan 草稿

已发现的坑:
- 事件总线在多 region 下的 ordering 不保证 → 临时按 refund_id 分片

Open questions:
- [ ] Q1:是否允许对 alpha 用户先启用 Feature 2?(影响合规评估)
