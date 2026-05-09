<!--
Short PR 模板(默认)
=====================

这是面向**小改动**的精简模板(bug fix / typo / 文档微调 / 局部 refactor)。

如果你的改动更复杂,请用更长的模板:
  - 新功能 / 行为变更 / 跨模块接口变化:?template=standard.md
  - 改 AGENTS / steering / templates / scripts / workflows:?template=harness_change.md

填不动 short 版的字段 ≠ 跳过。"只是 typo" 也请一句话说清 What。
-->

## What & Why

<!-- 1-3 句。这个 PR 做了什么?为什么现在做? -->

## Type

- [ ] fix · bug
- [ ] docs · 文档微调 / typo
- [ ] chore / build / ci
- [ ] refactor · 等价重构(如果有行为变化请切 standard)
- [ ] perf · 小幅性能微调(若有基准对比请切 standard)
- [ ] test · 仅加测试
- [ ] **如果你选中了 feat / security / harness-change,请切到 `?template=standard.md` 或 `?template=harness_change.md`**

## How tested

<!-- 说清楚你怎么验证的。可以是"本地跑 foo test"或"手工点了一遍 X 流程"。 -->

## Blast radius

<!-- 1 行。最坏情况影响谁?回滚 = `git revert`?如果不是,请切 standard。 -->

## Rollback

<!-- 1 行。通常 `git revert <sha>`。 -->

## 自检

- [ ] 没 force push
- [ ] 没引入 secret
- [ ] 本地 pre-commit 跑过
- [ ] 真的属于 "short" 范畴(而不是想偷懒)
- [ ] 关联的 issue / 上下文在描述里有链接
