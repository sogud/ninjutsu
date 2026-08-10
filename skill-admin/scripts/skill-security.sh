#!/bin/bash
# skill-security.sh - Minimal security scanner for AI skills
# Usage: ./skill-security.sh [skill_path]

set -e

RULES_FILE="${BASH_SOURCE[0]%/*}/security-rules.txt"
SKILL_PATH="${1:-$HOME/.claude/skills}"

# Generate grep patterns file from YAML if needed
generate_patterns() {
  if [[ ! -f "$RULES_FILE" ]]; then
    echo "Generating patterns from YAML..."
    python3 -c "
import yaml, sys
rules = yaml.safe_load(open('${BASH_SOURCE[0]%/*}/security-rules.yaml'))
for dim, patterns in rules.items():
  if dim == 'trust_signals': continue
  for p in patterns:
    print(f\"{p['pattern']}\t{p['level']}\t{p['desc']}\")
" > "$RULES_FILE" 2>/dev/null || {
      # Fallback: hardcoded patterns
      cat > "$RULES_FILE" << 'EOF'
ignore\s+(all\s+)?(previous|above|prior)\s+(instructions?|prompts?|rules?)	CRITICAL	Prompt injection: ignore previous
override\s+(your\s+)?system\s+prompt	CRITICAL	Prompt injection: override system
jailbreak	CRITICAL	Prompt injection: jailbreak
~\/\.ssh\/	CRITICAL	Permission abuse: SSH key access
~\/\.aws\/(credentials|config)	CRITICAL	Permission abuse: AWS credentials
\/etc\/(passwd|shadow|sudoers)	CRITICAL	Permission abuse: system files
silently\s+\[?do	CRITICAL	Hook: silently execute
without\s+(informing|telling)\s+the\s+user	CRITICAL	Hook: without user knowledge
curl\s+-X\s+POST\s+https?://(?!registry\.npmjs\.org)	CRITICAL	Exfiltration: POST to unknown
webhook\.site\/	CRITICAL	Exfiltration: webhook.site
Official\s+Anthropic\s+(skill|tool)	CRITICAL	Social: fake official
rm\s+-rf\s+[^|]*$	CRITICAL	Destructive: rm -rf
DROP\s+(TABLE|DATABASE)	CRITICAL	Destructive: DROP
sk-[a-zA-Z0-9]{20,}	CRITICAL	Secret: OpenAI API key
ghp_[a-zA-Z0-9]{36}	CRITICAL	Secret: GitHub PAT
EOF
    }
  fi
}

# Scan function
scan() {
  local path="$1"
  local score=100
  local critical=0 high=0 medium=0

  echo "Scanning: $path"
  echo "---"

  # Run grep with extended regex
  while IFS=$'\t' read -r pattern level desc; do
    # Skip empty lines
    [[ -z "$pattern" ]] && continue

    # Find matches
    matches=$(grep -rEn --include="*.md" --include="*.ts" --include="*.js" --include="*.py" \
      --exclude-dir={node_modules,dist,build,.git,__pycache__,test,tests,__tests__} \
      "$pattern" "$path" 2>/dev/null || true)

    if [[ -n "$matches" ]]; then
      # Filter out safe contexts (documentation/examples)
      # Skip: table rows (|), inline code (``), list items with examples (1. "pattern"), security descriptions
      filtered=$(echo "$matches" | grep -v -E '^\s*\||\|\s*$|```.+```|`\S+`|allowed without warning|safe to use|^[0-9]+\.\s*"|security check|Security check|Destructive command' || true)

      if [[ -n "$filtered" ]]; then
        count=$(echo "$filtered" | wc -l | tr -d ' ')
        echo "[$level] $desc ($count matches)"

        case "$level" in
          CRITICAL) critical=$((critical + count)); score=$((score - count * 40)) ;;
          HIGH) high=$((high + count)); score=$((score - count * 15)) ;;
          MEDIUM) medium=$((medium + count)); score=$((score - count * 5)) ;;
        esac

        # Show first 3 matches
        echo "$filtered" | head -3 | while read -r line; do
          echo "  $line"
        done
        echo ""
      fi
    fi
  done < "$RULES_FILE"

  # Clamp score
  [[ $score -lt 0 ]] && score=0
  [[ $score -gt 100 ]] && score=100

  # Print result
  echo "---"
  echo "Score: $score/100"
  echo "Issues: CRITICAL=$critical HIGH=$high MEDIUM=$medium"

  if [[ $score -lt 25 ]]; then
    echo "Verdict: ${RED}DANGEROUS${RESET} - REJECT"
  elif [[ $score -lt 50 ]]; then
    echo "Verdict: ${YELLOW}HIGH_RISK${RESET} - REJECT"
  elif [[ $score -lt 70 ]]; then
    echo "Verdict: ${YELLOW}SUSPICIOUS${RESET} - APPROVE_WITH_CAUTION"
  elif [[ $score -lt 85 ]]; then
    echo "Verdict: ${GREEN}LIKELY_SAFE${RESET} - APPROVE_WITH_CAUTION"
  else
    echo "Verdict: ${GREEN}TRUSTED${RESET} - APPROVE"
  fi
}

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RESET='\033[0m'

# Main
generate_patterns

# Check if path is a single skill (contains SKILL.md) or a platform directory
if [[ -f "$SKILL_PATH/SKILL.md" ]]; then
  # Single skill directory
  scan "$SKILL_PATH"
elif [[ -d "$SKILL_PATH" ]]; then
  # Platform directory - scan all skills
  for skill in "$SKILL_PATH"/*/; do
    [[ -L "$skill" ]] && continue  # Skip symlinks
    [[ -f "$skill/SKILL.md" ]] || continue  # Skip non-skill dirs
    scan "$skill"
    echo ""
  done
else
  echo "Error: $SKILL_PATH not found"
  exit 1
fi