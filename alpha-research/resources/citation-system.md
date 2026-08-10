# Citation System

Use this resource when producing `report-source.md` and final `report.html`.

The final report must be readable and click-verifiable. A source hidden at the bottom without clickable inline citations is not acceptable.

## Core rules

- Cite the **original source of the data or claim**, not the local research artifact that repeated it.
- Local files may be cited only as internal prior work, never as proof for external Facts.
- Every key Fact, numeric baseline, figure, and company recommendation must have clickable inline citations.
- Every reference entry must include a clickable URL or stable locator.
- Do not use a generic anchor text like “链接” alone. Use the source title or publisher + title.
- If a URL is unavailable, mark the citation as `MISSING URL` and block final report generation for key Facts.
- Search-result snippets, synthesized web-search answers, and wrapper summaries are discovery only.

## HTML citation pattern

Use clickable superscripts inline:

```html
<span class="claim">AI capex guidance increased across hyperscalers</span><sup class="cite"><a href="#S6">S6</a><a href="#S7">S7</a></sup>
```

In the bibliography:

```html
<li id="S6">
  <a href="https://www.microsoft.com/en-us/investor/earnings/fy-2026-q1/" target="_blank" rel="noopener noreferrer">
    Microsoft FY2026 Q1 earnings release
  </a>
  <span class="source-meta">Microsoft Investor Relations · 2026-04-29 · Tier 2 · Company primary source</span>
  <a class="backref" href="#claim-capex">↩</a>
</li>
```

Requirements:

- `href="#S#"` for inline citation links.
- `id="S#"` for bibliography entries.
- External links use `target="_blank" rel="noopener noreferrer"`.
- Use stable source URLs whenever possible.
- If multiple claims cite the same source, the backref may point to the most important claim or be omitted.

## Markdown source artifact pattern

Use Markdown footnotes:

```markdown
AI capex guidance increased across hyperscalers.[^S6]

[^S6]: Microsoft FY2026 Q1 earnings release, Microsoft Investor Relations, 2026-04-29, https://...
```

## Source Registry fields required for final report

Each reference must include:

| Field | Required? | Notes |
|---|---|---|
| Citation id | yes | `[S1]`, `[S2]`, etc. |
| Source title | yes | Actual title, not “web search result”. |
| Publisher / owner | yes | Company, regulator, exchange, media, social platform, data provider. |
| URL / stable locator | yes | Required for key Facts. |
| Date / period | yes | Filing date, publication date, report period, query date, or post timestamp. |
| Access date | yes | Especially for dynamic pages and market data. |
| Source tier | yes | From `research-tool-stack.md`. |
| Evidence role | yes | Strong Fact, Numeric baseline, Technical basis, Rumor clue, etc. |
| Retrieval method | yes | filing fetch, URL fetch, yfinance, OpenCLI, manual browser, etc. |
| Original provenance | yes for wrappers | Original filing/page/API/URL behind the wrapper output. |
| Excerpt / page / table | key Facts | Quote or stable section/table/page where possible. |

## Social and tweet/X citations

For X/Twitter and similar platforms:

- Preserve author handle, timestamp, post URL, and exact claim.
- Link the handle and the post separately when available.
- Treat social sources as Tier 5 narrative clues unless confirmed by primary sources.

Pattern:

```html
<li id="S14">
  <a href="https://x.com/handle/status/123" target="_blank" rel="noopener noreferrer">
    @handle post on AI infrastructure capex
  </a>
  <span class="source-meta">X/Twitter · 2026-05-01 10:32 UTC · Tier 5 · Rumor / narrative clue</span>
</li>
```

If only the user id is known and the post URL is missing, link the profile but mark the source incomplete:

```html
<a href="https://x.com/handle" target="_blank" rel="noopener noreferrer">@handle</a>
<span class="source-warning">post URL missing — cannot support a key Fact</span>
```

## Local-file rule

Local files such as `../other-topic/prior-draft.md` or `alpha-research-output/.../source-map.md` are process artifacts.

Allowed:

- “Prior internal Alpha Research draft” for context.
- “Internal source map says this claim still needs verification.”

Not allowed:

- Using a local report as the final citation for CoWoS capacity, HBM share, capex, valuation, or other external Facts.
- Linking local Markdown as if readers can verify the original data.

If prior work contains useful claims, copy its original Source Registry entries into the current Source Registry and cite those original URLs.

## Wrapper and data-provider rule

Do not cite the wrapper alone.

Examples:

- yfinance can support a numeric baseline only if ticker, field, query time, and Yahoo/source URL are recorded.
- Funda can surface filings/transcripts, but final source should identify the original filing/transcript URL or locator.
- OpenCLI is transport. Final citation must be the underlying platform URL, author/handle, timestamp, and extracted claim.
- TradingView chart data must include instrument, exchange, timeframe, query date, and source URL/locator.

## Citation quality gate

Block final `report.html` if any of these are true:

- Key Facts have non-clickable citations.
- Bibliography entries have no URL or stable locator.
- A key citation points to a local file instead of the original source.
- A figure uses data but has no source ids in its caption.
- A social claim lacks handle/timestamp/post URL and is used beyond narrative context.
- A search snippet or synthesized answer is treated as a final source.
