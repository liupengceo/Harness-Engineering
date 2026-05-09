# Security Policy · kiro.dev

> 这是一个 **starter kit** 仓库。这里的代码/脚本/工作流本身可能存在安全问题;你基于它 fork 的仓库有自己独立的安全策略。

## 支持的版本

`main` 分支是唯一的受支持版本。`kiro.dev` 暂无 tagged release。

## 报告漏洞

**请不要在公开 issue / discussion 里报告安全漏洞。**

请使用 GitHub 的 **[Private Vulnerability Reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)**:

1. 打开本仓库的 **Security** tab
2. 点 **Report a vulnerability**
3. 附上:
   - 影响的文件 / 路径
   - 最小复现步骤
   - 你认为的严重性(critical / high / medium / low)
   - 建议的修复(可选)

如果 Private Vulnerability Reporting 未启用或你无法访问,请通过邮件联系 `security@<维护者域名>`(请先在 GitHub 上 @ 维护者以便私信)。

## 响应时间目标

| 严重性 | 首次回复 | 初步修复 |
|---|---|---|
| critical | 24 小时内 | 7 天内 |
| high     | 3 天内   | 30 天内 |
| medium   | 7 天内   | 90 天内 |
| low      | best effort | best effort |

本仓库是业余维护的 starter kit,上述时间为**目标**,不保证。

## 范围

**在范围内**(欢迎报告):

- 本仓库的 `scripts/` 下任何脚本的安全问题
- `.github/workflows/*.yml` 的权限过宽、secret 泄露等
- `.pre-commit-config.yaml` / hooks 的安全问题
- AGENTS.md / steering 中的**安全建议**本身有错导致下游 fork 的风险
- 精读库 `docs/harness-engineering/*.md` 中的事实错误导致误导读者采纳不安全做法

**不在范围**(请报告给原项目):

- 你 fork 本仓库后在**你的**代码里引入的漏洞
- OpenAI / Anthropic / Stripe / Shopify / GitHub 自身的问题
- 精读库引用的第三方博客 / 论文本身的问题

## 已知的 harness 相关风险

- **Prompt injection**:`scripts/aggregate_reviews.py` 在生成 PR 评论 markdown 时会消费 persona 输出。如果 persona adapter 被入侵,可以注入 markdown。本仓库通过 `scripts/validate_persona_output.py` 做了一道 schema 校验,但**不保证**覆盖所有注入向量。见 self-review P3 #23。
- **`run_review_persona.sh` custom runner**:通过 env 变量 `CUSTOM_REVIEW_CMD` 直接 exec 命令,属于信任 repo variable 的攻击面。不要让未受信的人改 repository variables。

## 致谢

报告有效漏洞的人会被列入 `docs/security-credits.md`(如果你愿意公开)。
