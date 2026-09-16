# SiteProbe Architecture Reference

SiteProbe is constructed with modular Python boundaries:

```
src/siteprobe/
├── cli/              # Typer CLI commands (audit, fix, verify, doctor, integrations, serve-mcp)
├── core/             # Engine orchestration, YAML/env config loader, deterministic scoring
├── crawler/          # AsyncIO crawler, polite rate limiting, SQLite storage, robots/sitemap parsers
├── checks/           # Audit check modules:
│   ├── technical/    # 4xx/5xx, redirect chains, canonicals, robots, sitemaps, HTTPS, security headers
│   ├── onpage/       # Titles, descriptions, H1 hierarchy, images alt, hreflangs, thin content
│   ├── schema/       # JSON-LD syntax, Organization, Breadcrumbs, Article, FAQPage
│   ├── geo/          # AI search bot directives, /llms.txt discovery, QA structure, entity clarity
│   ├── performance/  # Server TTFB, payload size, asset count, optional Lighthouse
│   ├── accessibility/# Deterministic WCAG 2.1 checks (lang, form labels, empty buttons)
│   ├── security/     # HSTS, CSP, X-Content-Type-Options, HTTPS enforcement
│   ├── content/      # Word count heuristics, boilerplate ratio, soft-404 detection
│   └── ux/           # Viewport presence and responsive configuration
├── remediation/      # Risk-classified planner, atomic file handlers, snapshot/rollback executor
├── verification/     # Before-and-after re-auditor and diff verifier
├── reporting/        # JSON, GitHub Markdown, and standalone responsive HTML dashboard
├── i18n/             # Locale catalogs (en, fa, tr) and translator engine
├── models/           # Pydantic data contracts (Finding, CrawlPage, RemediationPlan, etc.)
└── mcp/              # FastMCP / Standard MCP server for AI agent tool calling
```
