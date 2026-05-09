---
title: 代码风格与命名
inclusion: fileMatch
fileMatchPattern: "**/*.{ts,tsx,js,jsx,py,rb,go,rs,java,kt,swift,cs,cpp,c,h,hpp,php,sh,md,sql,yaml,yml,toml,json}"
---

# 代码风格与命名

> 所有写代码的任务都读这份。具体语言 formatter 由项目 CI 执行——本文件规定的是**高于 formatter 的**约定。

## 1. 首要读者是 agent

这是本仓库最重要的一条风格:

- **首要读者是 agent,其次才是人。**
- 这意味着:
  - 变量名、函数名要可**grep**。别起那种换个单复数就同名冲突的名字。
  - 错误、边界条件**显式化**,不要靠约定 / 隐式 nil。
  - 一个文件一个主要概念;避免"全能工具类"。
  - 注释以"下一个接手者(可能是 agent)需要知道什么"为标准,不是"解释语言特性"。

## 2. 命名

| 类别 | 约定 |
|---|---|
| 变量 / 函数 | 语言社区惯例(`snake_case` for py/rb,`camelCase` for ts/js/java…) |
| 类型 / 类 | `PascalCase` |
| 常量 | `SCREAMING_SNAKE_CASE` |
| 文件 | 语言社区惯例;不混大小写风格 |
| 测试文件 | 与被测文件同名加后缀(`foo_test.go`、`foo.test.ts`、`test_foo.py`) |
| Feature flag | `FLAG_<AREA>_<NAME>`,值为布尔或枚举 |

**永远不要**:
- ❌ 一个字母 / 两个字母的变量名,除了循环 index 和坐标 `x/y/z`。
- ❌ 既叫 `userID` 又叫 `user_id` 又叫 `uid`(同一仓库内必须统一)。
- ❌ "helper / util / misc" 命名的文件——这是反模式。

## 3. 文件与目录

- 一个文件导出的公共符号 **≤ 7 个**。超过就拆文件。
- 超过 **400 行**的文件必须有充分理由(如 generated code)。
- 目录层级**不超过 5 层**。
- 测试文件与被测文件**同目录**或镜像目录(`__tests__/`、`tests/`)。

## 4. 函数

- 优先选**短、纯、显式**。
- 单个函数 **≤ 50 行** 是硬目标;≤ 30 行是软目标。
- 副作用集中在函数的前部或后部,不要散落在中间。
- 函数签名里**禁止**出现 `any / interface{} / void*`,除非有书面理由。
- 返回值多于 3 个 → 用具名结构体 / 对象 / tuple 类型。

## 5. 错误处理

- 错误信息**三要素**:
  1. **What**:发生了什么。
  2. **Where**:哪个模块 / 操作。
  3. **Next**:下一步建议(重试?联系谁?读哪个 doc?)。
- 用项目约定的错误类型体系(而不是随手 `throw new Error("xxx")`)。
- **严禁**:吞错误、把错误序列化成字符串然后再当错误处理、用 print 代替结构化日志。

## 6. 日志与观测

- 日志格式必须**机器可解析**(优先 JSON / logfmt)。
- 关键事件有稳定 `event_id`(便于 grep 和告警)。
- 敏感字段(token / key / PII)永远不进日志。触发 `security.md` 的红线。

## 7. 注释

- 注释写的是 **why**,不是 **what**。
- 反模式:`// increment i by 1`。
- 推荐:`// 这里故意用 atomic inc 而非 mutex,因为 §性能文档 第 3 节`。
- 对"看起来可以删但其实不能删"的代码,加 **不可省略**的注释,指明"删掉会破坏什么"。

## 8. TODO / FIXME

- `TODO:` 必须写**负责人 / 任务链接 / 截止条件**。裸 `TODO:` 不合入。
  - ✅ `TODO(@alice, PROJ-412, 2026-Q3): 替换为 foo service 后删除。`
  - ❌ `TODO: 以后再说。`
- `FIXME:` 只用在"知道错了,但为了赶上线暂时保留"的情形,并必须关联 bug issue。
- `HACK:` 必须写明 "是为了绕过什么",以及 "什么条件下可以拆掉"。

## 9. 类型化优先

- 能加类型的地方都加(TS、Python type hints、Rust 全面;动态语言优先 dataclass / Struct / TypedDict 等)。
- 对 JSON / HTTP payload 用 schema(JSON Schema / pydantic / zod),不要靠自由字典。
- 对外接口**禁止裸 dict / map** 作为公共参数或返回。

## 10. 语言特定(节选)

### TypeScript / JavaScript

- 禁用 `any`。需要时用 `unknown` 并在边界处做类型守卫。
- 严格模式打开(`"strict": true`)。
- 优先 `const`,少量 `let`,禁用 `var`。
- 函数参数 **≥ 3 个**时用对象解构 `({ a, b, c }: FooArgs)`。
- 异步优先 `async/await`;除非性能路径需要手写 Promise 组合。

### Python

- 全量 type hints(包括内部函数)。
- 用 `dataclass` / `attrs` / `pydantic`,避免 `dict` 作为强类型载体。
- `print` 只用于 CLI 工具;库代码用 `logging` / 结构化日志。
- `try/except` 只抓需要处理的异常,不抓 `Exception`(顶层除外)。

### Go

- 错误用 `errors.Is / As` + sentinel / wrap,避免字符串比较。
- 不用全局 `var`(除非是 logger / config 的单例 initializer)。
- 包名小写,短;`util / misc / common` 不是包名。
- 并发里 **绝不泄漏 goroutine**;`context` 永远作为第一参数。

### Rust

- `unwrap` 只允许出现在:测试 / main 的顶层 / 有显式 SAFETY 注释的地方。
- 公共 API 避免直接暴露具体类型,优先用 trait object 或泛型 + where 约束。
- `#[must_use]` 用在任何"返回了却被忽略就必然出 bug"的函数上。

## 11. 提交前自检

- [ ] 运行了 formatter 和 lint?
- [ ] 类型检查通过?
- [ ] 没有新增 `any` / `unknown as X` / `@ts-ignore` / `# type: ignore`?
- [ ] 没有裸 TODO?
- [ ] 没有一次性超过 400 行的文件?
- [ ] 单函数没超过 50 行?
- [ ] 错误信息三要素齐全?

## 12. 理由合集(抽取)

- 命名可 grep → agent legibility 第一位。
- 类型优先 → 把"机器能验证"的事交给机器,这是 §harness 7 "verified" 的落地。
- 文件 / 函数限长 → LLM 一次能稳定推理的窗口有限,块小更利于增量 diff。
- 注释 why → agent 接手时最缺的是"为什么这里不能改动"的信息。
