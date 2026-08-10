# OpenCLI Reader Playbook

## Best for

Read-only extraction from dynamic websites, logged-in pages, social feeds, financial portals, and research sites when normal web search or static fetch is insufficient.

Use it as a transport layer for sources such as Yahoo Finance, Bloomberg, Reuters, Eastmoney, Xueqiu, Reddit, HackerNews, Substack, arXiv, Google Scholar, Weibo, Xiaohongshu, Zhihu, Weixin, YouTube, government policy sites, and other OpenCLI-supported adapters.

Reference pattern: finance-skills `opencli-reader` and `twitter-reader`.

## Canonical install source

Use `../tool-install-sources.md` before setup.

| Field | Value |
|---|---|
| Canonical source | `https://github.com/jackwener/opencli` |
| Package / connector | `@jackwener/opencli` |
| Setup Mode | Local install; Browser login session for many adapters |
| Verify | `opencli doctor`, `opencli list -f json` |
| Output preference | `-f json`, `-f yaml`, `-f csv`, or limited markdown |

Run install, doctor, adapter discovery, or browser-session checks only after user approval.

## Detection flow

1. Check `command -v opencli`.
2. Run `opencli doctor` if user approves.
3. Run `opencli list -f json` to discover supported adapters and strategies.
4. For the target source, inspect `opencli <site> --help` and command-level help.
5. Check adapter strategy:
   - `PUBLIC` / `LOCAL`: may work without login.
   - `COOKIE` / `HEADER` / `INTERCEPT` / `UI`: requires browser login/session and user approval.
6. If missing, ask for install approval using canonical source.

Do not guess adapter names or flags.

## Read-only guardrails

Never invoke write actions, including:

- post, like, retweet, reply, comment, follow;
- save, subscribe, upvote, bookmark if it changes account state;
- create/delete alerts;
- edit watchlists;
- place trades or modify accounts;
- upload files or change profile/account settings.

If the adapter exposes both read and write commands, use only read commands.

## Source Tier

Tier depends entirely on the underlying source:

| Underlying source | Tier | Evidence role |
|---|---:|---|
| Government / exchange / regulator page | 1 | Strong Fact if original URL and excerpt are preserved. |
| Company page / IR / press release | 2 | Company primary context. |
| Financial data portal | 3 | Numeric baseline. |
| News or trade media | 4 | Event clue / context. |
| Social, forum, influencer, comment feed | 5 | Rumor / narrative clue. |

OpenCLI is not an evidence source. Do not cite “OpenCLI” as proof.

## Structured acquisition recipe

1. Define the exact source and claim.
2. Prefer dedicated source resources first: SEC EDGAR, HKEXnews, CNINFO, Company IR, yfinance, a-stock-data, TradingView, China policy sources.
3. Use OpenCLI if:
   - page is dynamic;
   - login session is needed;
   - adapter provides structured output;
   - static fetch failed.
4. Use `-f json` or `-f yaml` where available.
5. Limit results; start with 10–20 records unless the user asks for more.
6. Preserve original URLs and timestamps.
7. Feed only relevant extracted records into Source Registry.

## Common finance/research acquisition patterns

| Need | OpenCLI role | Evidence classification |
|---|---|---|
| X / Twitter narrative | read tweets/search/thread | Tier 5 narrative clue. |
| Reddit / forum narrative | read posts/comments/search | Tier 5 narrative clue. |
| Eastmoney / Xueqiu A-share narrative | read stock page/hot/comments if adapter exists | Tier 5 narrative / Tier 3 market data depending on underlying field. |
| Bloomberg/Reuters headlines | read/search headlines | Tier 4 event clue, verify original article. |
| Government policy page | dynamic page extraction | Tier 1 if official URL preserved. |
| Weixin/article/social | read-only extraction | Usually Tier 4/5 unless official account is primary source. |

## Required provenance

Record:

- Underlying platform/source.
- OpenCLI adapter and command category.
- URL or stable locator.
- Author/handle for social sources.
- Timestamp and timezone.
- Query/filter/search terms.
- Extracted text or screenshot locator.
- Adapter strategy and login/access caveat.
- Whether command was read-only.

## What it can support

- Dynamic page access when static fetch fails.
- Social narrative capture for anti-hype mode.
- A-share / China narrative sources such as 东方财富、雪球、同花顺社区 if supported.
- Government/policy/law pages when adapter support exists.
- Screenshots or structured extracts with provenance.
- Source Gate recovery when a source is blocked by static fetch.

## What it cannot support

- Bypassing access controls or paywalls.
- Turning social/forum content into Strong Fact.
- Trading execution, account changes, or write operations.
- Reliable extraction when an adapter is stale or the site layout changed.
- Final evidence without original source details.

## Source Gate rules

Hard gate fails if:

- OpenCLI output is cited without the underlying source URL/locator;
- social/forum output is used as Strong Fact;
- the command could have modified account state;
- adapter/source access is required but user did not approve login/session use.

## Fallbacks

- Native web search and fetch.
- Browser automation.
- Manual browser extraction.
- Dedicated provider resource.
- Official source pages.
