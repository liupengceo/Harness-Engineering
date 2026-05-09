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
#     SKIP_VALIDATE  - set to "1" to skip the output validator
#                      (only use for local debugging; CI must not set this)
#
#   out:   YAML on stdout, matching review-personas/README.md § 3 schema.
#          Every code path pipes its output through
#          scripts/validate_persona_output.py so the aggregator never
#          sees a malformed report.
#
# 设计动机:
#   本仓库不绑定具体模型 runtime。不同 fork 可以把 REVIEW_RUNNER
#   换成自己的 agent 平台,而不用改本工作流。
#
# 默认行为 (REVIEW_RUNNER=abstain):
#   产出一个合法的 'abstain' YAML, 表示 "没有任何 reviewer 实际评审过"。
#   aggregate_reviews.py 看到 abstain 会在聚合 markdown 顶部打显眼
#   banner,阻止"bot 绿 = 万事大吉"的懒惰反射。
#   这条规则见 templates/review-personas/README.md § 3.1。
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

# ------------------------------------------------------------------
# Output the persona YAML into $out, then validate it before streaming
# to stdout. We route through a temp file so we can validate atomically
# without double-invoking the adapter.
# ------------------------------------------------------------------
out="$(mktemp)"
# shellcheck disable=SC2064
trap "rm -f '$out'" EXIT

case "$runner" in
  abstain)
    cat > "$out" <<EOF
persona: "$persona"
verdict: "abstain"
summary: "No actual review performed: REVIEW_RUNNER='abstain' (the default). Set repo variable REVIEW_RUNNER to 'codex' / 'claude-code' / 'custom' to enable a real reviewer. Do NOT treat this as approval."
findings: []
followups:
  - "Set repository variable REVIEW_RUNNER to 'codex' / 'claude-code' / 'custom' to wire up an agent."
escalate_to_human:
  required: false
  reason: ""
EOF
    ;;

  codex)
    # Wire up OpenAI Codex CLI. Placeholder invocation; adjust to your
    # deployment. Expected env (set as GitHub Actions secrets):
    #   OPENAI_API_KEY
    #
    # The adapter MUST emit *raw* YAML matching README.md § 3 on stdout
    # (no markdown code fences, no natural-language preamble).
    # See templates/review-personas/README.md § 3.2.
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
      --format yaml > "$out"
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
      --yaml > "$out"
    ;;

  custom)
    if [[ -z "${CUSTOM_REVIEW_CMD:-}" ]]; then
      echo "REVIEW_RUNNER=custom requires env CUSTOM_REVIEW_CMD" >&2
      exit 3
    fi
    # 约定:CUSTOM_REVIEW_CMD 接 $persona_file 与 $diff_path 两个参数,
    # 输出合法 YAML 到 stdout(不得 code fence,不得前后带自然语言)。
    # shellcheck disable=SC2086
    $CUSTOM_REVIEW_CMD "$persona_file" "$diff_path" > "$out"
    ;;

  *)
    echo "unknown REVIEW_RUNNER=$runner (expected: abstain|codex|claude-code|custom)" >&2
    exit 4
    ;;
esac

# ------------------------------------------------------------------
# Validate before streaming to stdout.
# ------------------------------------------------------------------
if [[ "${SKIP_VALIDATE:-0}" != "1" ]]; then
  if ! python3 scripts/validate_persona_output.py \
         --persona "$persona" \
         --input "$out" >&2; then
    echo "run_review_persona: adapter output for '$persona' failed validation (runner=$runner)" >&2
    exit 3
  fi
fi

cat "$out"
