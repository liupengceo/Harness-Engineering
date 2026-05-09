#!/usr/bin/env bash
# ------------------------------------------------------------------
# Run one review persona against the current PR diff.
#
# 约定:
#   usage:  scripts/run_review_persona.sh <persona-name>
#   in-env:
#     PERSONA_FILE   - path to templates/review-personas/<persona>.md
#     DIFF_PATH      - path to a unified diff of the PR
#     REVIEW_RUNNER  - adapter id: abstain | codex | claude-code | custom
#     REVIEW_MODEL   - (optional) model id to pass to the adapter
#
#   out:   YAML on stdout, matching review-personas/README.md § 3 schema.
#
# 设计动机:
#   本仓库不绑定具体模型 runtime。不同 fork 可以把 REVIEW_RUNNER
#   换成自己的 agent 平台,而不用改本工作流。
#
# 默认行为 (REVIEW_RUNNER=abstain):
#   产出一个合法的 'abstain' YAML, 表示 "未启用真正的 reviewer"。
#   这样 CI pipeline 在裸仓库也能跑通,不会 red。
# ------------------------------------------------------------------
set -euo pipefail

persona="${1:-}"
if [[ -z "$persona" ]]; then
  echo "usage: $0 <persona>" >&2
  exit 2
fi

persona_file="${PERSONA_FILE:-templates/review-personas/${persona}.md}"
diff_path="${DIFF_PATH:-pr.diff}"
runner="${REVIEW_RUNNER:-abstain}"
model="${REVIEW_MODEL:-}"

if [[ ! -f "$persona_file" ]]; then
  echo "persona file not found: $persona_file" >&2
  exit 2
fi

case "$runner" in
  abstain)
    cat <<EOF
persona: "$persona"
verdict: "approve"
summary: "REVIEW_RUNNER is 'abstain' (default). No real reviewer was invoked; see .github/workflows/review.yml to wire up an agent."
findings: []
followups:
  - "Set repository variable REVIEW_RUNNER to 'codex' / 'claude-code' / 'custom' to enable actual review."
escalate_to_human:
  required: false
  reason: ""
EOF
    ;;

  codex)
    # Wire up OpenAI Codex CLI. Placeholder invocation; adjust to your deployment.
    #
    # Expected env (set as GitHub Actions secrets):
    #   OPENAI_API_KEY
    #
    # codex exec <<"END-INPUT-STREAMED-BELOW"
    # System prompt: (contents of $persona_file)
    # User message:  Please review this PR. Diff follows:
    # <diff contents>
    # END-INPUT-STREAMED-BELOW
    #
    # The adapter must emit YAML matching README.md § 3 on stdout.
    if ! command -v codex >/dev/null 2>&1; then
      echo "REVIEW_RUNNER=codex but codex CLI not installed" >&2
      exit 3
    fi
    model_arg=""
    [[ -n "$model" ]] && model_arg="--model $model"
    # shellcheck disable=SC2086
    codex review $model_arg \
      --system-prompt-file "$persona_file" \
      --input-file "$diff_path" \
      --format yaml
    ;;

  claude-code)
    if ! command -v claude-code >/dev/null 2>&1; then
      echo "REVIEW_RUNNER=claude-code but claude-code CLI not installed" >&2
      exit 3
    fi
    # claude-code 的实际 CLI 形态以官方为准;下面是一个示例。
    claude-code review \
      --system "$persona_file" \
      --input  "$diff_path" \
      --yaml
    ;;

  custom)
    if [[ -z "${CUSTOM_REVIEW_CMD:-}" ]]; then
      echo "REVIEW_RUNNER=custom requires env CUSTOM_REVIEW_CMD" >&2
      exit 3
    fi
    # 约定:CUSTOM_REVIEW_CMD 接 $persona_file 与 $diff_path 两个参数,
    # 输出合法 YAML 到 stdout
    # shellcheck disable=SC2086
    $CUSTOM_REVIEW_CMD "$persona_file" "$diff_path"
    ;;

  *)
    echo "unknown REVIEW_RUNNER=$runner (expected: abstain|codex|claude-code|custom)" >&2
    exit 4
    ;;
esac
