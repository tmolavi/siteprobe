# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-10-09

### Added
- **Google Algorithm Update Impact Triage (`update-triage`)**: Deterministic triage utility to evaluate Google Search Console performance shifts around algorithm updates (specifically the September 2026 Google Spam Update).
- **Frozen Comparison Windows**: Strict 14-day matched-weekday comparison methodology (`PRE`: 2026-09-10 to 2026-09-23, `ROLLOUT`: 2026-09-24 to 2026-10-07) with isolated completion day (2026-10-08) and guarded incomplete `POST` window.
- **Defensive GSC Data Validation**: Validates date formats, types, prevents impossible data (clicks > impressions), composite duplicate row detection, and never generates fake observations.
- **5 Empirical Diagnostic Classifications**: `NO_CLEAR_CHANGE_OBSERVED`, `PERFORMANCE_CHANGE_OBSERVED`, `TECHNICAL_ISSUE_OBSERVED`, `MANUAL_ACTION_REPORTED`, and `INSUFFICIENT_DATA`.
- **Methodological Research Guide**: Documented in `docs/research/google-spam-update-september-2026.md`.
- **Synthetic Benchmark Dataset & Reproduction**: Complete reproducible example in `examples/update-impact/`.
- **Agent Skill Update**: Upgraded canonical agent skill `siteprobe` to v0.2.0 with update notification requirement.

### Fixed
- **Scientific Integrity & Methodology Alignment**:
  - Removed outdated claims of universal ±15% normal variance; documented site-specific heuristic baseline daily variability envelope ($\max(5\%, 2 \times \text{CV})$).
  - Explicitly labeled CV envelope as an informal heuristic rather than a validated significance test; set statistical significance to `UNKNOWN`.
  - Avoided classifying performance differences as "normal" or "abnormal" solely based on heuristic thresholds.
  - Enforced integer count validation in CSV parser: fractional click/impression values are rejected rather than silently rounded.
  - Fixed CLI `--json` and `--output` flags to reliably write report file and output clean JSON simultaneously.
  - Clarified that update triage requires CSV exports, removing unsupported claims of automated GSC API retrieval.
  - Added 10-point regression test suite for update triage methodology and CLI behavior.

## [0.1.1] - 2026-09-16

### Added
- **SSR & Hydration Inspector**: Comprehensive Server-Side Rendering (SSR) vs. Client-Side Rendering (CSR/SPA) detection engine.
- **Hydration Payloads & Framework Detection**: Detects Next.js (`__NEXT_DATA__`, `self.__next_f`), Nuxt (`__NUXT_DATA__`), Remix, SvelteKit, Astro islands, Gatsby, and Angular Universal.
- **Raw Server HTML Parity**: Checks whether critical SEO tags (`<title>`, `<meta description>`, `<h1>`, `<link rel="canonical">`) exist directly in initial server response or require client JS execution.
- **Empty Shell SPA Detection**: Identifies `<div id="root"></div>` / `<div id="app"></div>` empty shells that cause indexing degradation on low-render-budget search bots.
- **CLI Command**: `siteprobe ssr <url>` for instant terminal inspection with rich formatted diagnostic tables.
- **MCP Tool**: `check_ssr(url)` enabling AI agents to inspect rendering status on demand.
- **Unit & Integration Tests**: 6 dedicated SSR tests covering major modern frameworks and CLI rendering.

## [0.1.0] - 2026-09-16

### Added
- **Core Engine**: AsyncIO polite crawler with SQLite storage, per-host adaptive rate limiting, and backoff handling.
- **Audit Checks Suite**: 9 check modules covering Technical SEO, On-Page SEO, Schema.org, GEO/AEO (AI Search readiness), Performance heuristics, WCAG accessibility, Security headers, Content quality, and Mobile UX.
- **GEO / AI Search Readiness**: Dedicated scoring module measuring AI bot crawl access (OAI-SearchBot, PerplexityBot, ClaudeBot), `/llms.txt` validation, and conversational QA structures.
- **Remediation Framework**: Risk-classified plan generator (`SAFE_AUTOFIX`, `REVIEW_RECOMMENDED`, `MANUAL_ONLY`) and local code executor with snapshot/rollback.
- **Verification Engine**: Before/after verification validating whether detected issues were genuinely fixed.
- **Multi-format Reporting**: Single-file interactive HTML dashboard, structured JSON (`audit.json`), and GitHub Markdown.
- **Internationalization (i18n)**: Full multilingual support for English (`en`), Persian (`fa`), and Turkish (`tr`).
- **MCP Server**: FastMCP server exposing tools for seamless AI agent integration (`start_audit`, `get_findings`, `apply_safe_fixes`, etc.).
- **Agent Skill**: Production-grade `skills/siteprobe/SKILL.md` for Codex, Claude Code, Gemini CLI, and Cursor.
- **CLI**: Command-line interface with `audit`, `fix`, `verify`, `doctor`, and `integrations` subcommands.
