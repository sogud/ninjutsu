# Source Gate: {Topic}

## 1. Gate Result

PASS / FAIL

## 2. Blocking Items

| Blocking item | Missing source/tool | Why it blocks final report | Required action |
|---|---|---|---|
| Missing original URL / stable locator |  | Final citations cannot be clicked or audited | Fetch/open original source |
| Local artifact used as proof |  | Local files are process artifacts, not external evidence | Replace with original source URL |
| Web-search-only evidence |  | Search snippets are discovery, not proof | Open real page / filing / PDF / data endpoint / original post |
| Financial baseline missing |  | Company ranking / valuation / liquidity cannot be supported | Use yfinance / a-stock-data / Funda / TradingView / official/manual equivalent |
| Anti-hype narrative capture missing |  | Narrative origin/crowding path is not auditable | Use OpenCLI / browser / social reader / manual original URL |
| Data figure lacks source ids |  | Chart may look authoritative without proof | Add source ids in caption or remove figure |

## 3. Acquisition Plan

| Missing evidence | Preferred tool / source | Canonical install/source URL | User action needed | Fallback |
|---|---|---|---|---|
| Financial baseline | yfinance / a-stock-data / Funda / TradingView / official filing |  | API key / install approval / subscription / manual source | Manual official filing/exchange data with date and field names |
| Social narrative origin | OpenCLI / browser / social reader / original URL |  | login / browser session / install approval / manual source | Mark narrative origin unknown and remove origin claim |
| Original filing / IR source | SEC / HKEX / CNINFO / exchange / company IR |  | manual source / browser access | Remove company Fact or mark unknown |
| Technical source | paper / patent / standard / official technical doc |  | subscription / manual source | Remove technical feasibility claim |
| Clickable final citation | original URL / stable locator |  | manual source | Block final HTML |

## 4. Permission Prompts

Ask these before running commands or accessing login/API/subscription sources:

1. May I run a read-only financial-data query or setup check for `{tool}` in this environment?
2. May I use OpenCLI/browser automation with your logged-in session to read `{site}`? I will use read-only actions only.
3. Do you have access to `{paid/subscription source}` or should I use a manual/public fallback?

## 5. Stage Result

- Recommended next stage:
- Why:
- Handoff input:
- Stop / continue recommendation:
