# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
