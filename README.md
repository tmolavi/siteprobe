<div align="center">

# SiteProbe

**Open-source autonomous website auditor & fixer for SEO, GEO, performance, accessibility and technical web quality.**

[![CI](https://github.com/tmolavi/siteprobe/actions/workflows/ci.yml/badge.svg)](https://github.com/tmolavi/siteprobe/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![MCP Server](https://img.shields.io/badge/MCP-Ready-green.svg)](https://modelcontextprotocol.io)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-orange.svg)](https://github.com/tmolavi/siteprobe/blob/main/skills/siteprobe/SKILL.md)

<p align="center">
  <strong>SiteProbe audits a website, tells you what is wrong, and—when authorized access is available—helps your AI coding agent fix and verify it.</strong>
</p>

[Quick Start](#-60-second-quick-start) &bull;
[Workflow](#-audit--fix--verify-workflow) &bull;
[Agent Skill](#-agent-skill-installation) &bull;
[MCP Server](#-model-context-protocol-mcp) &bull;
[Architecture](#-architecture) &bull;
[Documentation](https://github.com/tmolavi/siteprobe/tree/main/docs)

</div>

---

## ⚡ Short Demo

```bash
# 1. Run deep public website audit
siteprobe audit https://example.com --lang en --output ./siteprobe-report

# 2. Automatically apply safe code remediations to local project
siteprobe fix ./siteprobe-report/audit.json --repo /path/to/project

# 3. Verify that changes resolved the issues without regressions
siteprobe verify ./siteprobe-report/audit.json --repo /path/to/project
```

---

## 💡 Why SiteProbe?

Most auditing tools are passive checklists. They hand you a 40-page PDF of problems and leave the engineering team with all the toil. 

**SiteProbe connects diagnosis with remediation.**

It doesn't just find a missing canonical tag, an unlabelled accessibility input, or an absent `/llms.txt` file for AI agents—it constructs an atomic, risk-categorized remediation plan, modifies local source code safely, and runs post-change verification to prove the problem is resolved.

### Core Guarantees:
* **Zero Hallucination**: No simulated rankings or fabricated Search Console numbers. If an external credential is missing, SiteProbe clearly marks it as optional and explains how to connect it.
* **Deterministic Scoring**: Transparent, explainable weights across Technical, On-Page, Schema, GEO, Accessibility, and Security.
* **Safety First**: Every automated fix creates a snapshot before applying changes and rolls back automatically if verification fails.
* **Multilingual from Day 1**: Native localized audits in English (`en`), Persian (`fa`), and Turkish (`tr`).

---

## 🚀 Capabilities

| Capability Category | What SiteProbe Audits | Safe Auto-Fix Capability |
| :--- | :--- | :---: |
| **Technical SEO** | Status codes (4xx/5xx), broken internal links, redirect chains & loops, canonical mismatches, robots.txt, XML sitemap validation, HTTPS & trailing slash consistency. | ✅ |
| **On-Page SEO** | Title tags (length & duplicate detection), meta descriptions, H1 hierarchy & duplicates, image alt attributes, hreflang reciprocal links, thin content. | ✅ |
| **GEO / AEO (AI-Search)** | AI search crawler access (`OAI-SearchBot`, `PerplexityBot`, `ClaudeBot`), `/llms.txt` validation, conversational QA structures, entity clarity & authorship. | ✅ |
| **Structured Data** | JSON-LD syntax verification, Organization, WebSite, Breadcrumbs, Article, and FAQPage schema presence. | ✅ |
| **Accessibility (WCAG 2.1)**| Missing `lang` on `<html>`, unlabelled form inputs, empty buttons without accessible text, landmark coverage. | ✅ |
| **Security & Headers** | HTTPS enforcement, HSTS (`Strict-Transport-Security`), CSP, and `X-Content-Type-Options`. | 🛠️ Server Config |
| **Performance Heuristics**| Server TTFB latency, oversized HTML document payloads, external script bloat, optional Google Lighthouse integration. | 🛠️ Advisory |
| **Mobile UX** | Meta viewport presence and responsive `width=device-width` parameters. | ✅ |

---

## 🔄 Audit → Fix → Verify Workflow

```text
┌────────────────┐     ┌───────────────┐     ┌──────────────────┐
│  PUBLIC AUDIT  │ ──> │   EVIDENCE    │ ──> │ REMEDIATION PLAN │
└────────────────┘     └───────────────┘     └──────────────────┘
                                                       │
┌────────────────┐     ┌───────────────┐               ▼
│  FINAL REPORT  │ <── │  VERIFICATION │ <── ┌──────────────────┐
└────────────────┘     └───────────────┘     │    APPLY FIX     │
                                             └──────────────────┘
```

1. **Audit**: Polite, asynchronous crawler parses the site graph, extracts HTML metadata, and catalogs all assets in SQLite.
2. **Evidence**: Every finding captures the exact HTTP headers, HTML DOM selector, and response timings.
3. **Plan**: Findings are classified into `SAFE_AUTOFIX`, `REVIEW_RECOMMENDED`, or `MANUAL_ONLY`.
4. **Fix**: Safe modifications (e.g. inserting canonical tags, creating `robots.txt` / `llms.txt`, setting viewport, fixing alt text) are applied with in-memory snapshots.
5. **Verify**: The verification engine re-evaluates the rules against the target and produces before/after proof.
6. **Report**: Comprehensive results rendered in standalone HTML, structured JSON, or Markdown.

---

## 📊 Report Preview

SiteProbe generates a single-file, interactive HTML report with zero external CDN dependencies:
* **Interactive Scorecard**: Overall score and individual category health gauges.
* **GEO & AI Search Pillar Breakdown**: Transparent scoring for bot access, `llms.txt`, entity clarity, and QA markup.
* **Filterable Finding Cards**: Browse issues by severity (Critical, High, Medium, Low) and category.
* **Diff Viewer**: See unified code diffs of all remediations applied.

---

## 📦 Installation

### From Source (Recommended for Developers)

```bash
git clone https://github.com/tmolavi/siteprobe.git
cd siteprobe
pip install -e .
```

### Optional Dependency Extras

```bash
# Headless browser automation (Playwright)
pip install "siteprobe[browser]"
playwright install chromium

# Google Search Console & GA4 APIs
pip install "siteprobe[google]"

# LLM Providers (LiteLLM)
pip install "siteprobe[ai]"

# All optional integrations
pip install "siteprobe[all]"
```

---

## ⏱️ 60-Second Quick Start

```bash
# Check installed tools and environment
siteprobe doctor

# Run an audit on a website
siteprobe audit https://example.com

# Inspect generated reports
open ./siteprobe-report/audit.html
```

---

## 🐍 Python Usage

```python
import asyncio
from siteprobe.core.engine import AuditEngine
from siteprobe.core.config import SiteProbeConfig, SiteConfig, CrawlConfig

async def main():
    config = SiteProbeConfig(
        site=SiteConfig(url="https://example.com", language="en"),
        crawl=CrawlConfig(max_pages=25, concurrency=3),
    )
    engine = AuditEngine(config=config)
    result = await engine.run_audit("https://example.com")
    
    print(f"Overall Quality Score: {result.scores.overall_score}/100")
    print(f"GEO Score: {result.scores.geo_score}/100")
    print(f"Discovered {len(result.findings)} findings across {result.crawl_summary.total_crawled} pages.")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 💻 CLI Usage

### Audit Command
```bash
# Standard audit
siteprobe audit https://example.com

# Specify crawl cap and output folder
siteprobe audit https://example.com --max-pages 100 --output ./my-audit

# Multilingual audit in Persian or Turkish
siteprobe audit https://example.com --lang fa
siteprobe audit https://example.com --lang tr

# Include Lighthouse performance lab data (requires Node.js)
siteprobe audit https://example.com --lighthouse
```

### Fix Command
```bash
# Apply safe autofixes to a local project repository
siteprobe fix ./my-audit/audit.json --repo /path/to/my-project
```

### Verify Command
```bash
# Verify applied changes against the audit report
siteprobe verify ./my-audit/audit.json --repo /path/to/my-project
```

### System Diagnostics
```bash
# Inspect environment and optional integration status
siteprobe doctor

# List configured providers
siteprobe integrations
```

---

## 🤖 Agent Skill Installation

SiteProbe includes a first-class Agent Skill adhering to standard agentic specifications:

`skills/siteprobe/SKILL.md`

### Using with OpenAI Codex / CLI
Codex automatically detects repository instructions from `skills/siteprobe/SKILL.md` and `AGENTS.md`.

### Using with Claude Code
Invoke Claude Code and reference the skill:
```bash
claude "Audit https://example.com and fix all safe issues in this repository"
```
Claude will follow the phased intake, audit, plan, fix, verify, and report lifecycle defined in `CLAUDE.md` and `skills/siteprobe/SKILL.md`.

### Using with Google Gemini / Antigravity
The skill is located at `skills/siteprobe/SKILL.md`. Gemini and Antigravity agents can invoke the CLI or MCP tools directly during coding workflows.

### Using with Cursor
Point Cursor Rules or `@agent` to `skills/siteprobe/SKILL.md` to enable autonomous website auditing and file remediation.

---

## 🔌 Model Context Protocol (MCP)

SiteProbe exposes an asynchronous, non-blocking MCP server:

```bash
siteprobe serve-mcp
```

### Adding to Claude Desktop or Agent MCP Configuration
Add to your `claude_desktop_config.json` or agent settings:

```json
{
  "mcpServers": {
    "siteprobe": {
      "command": "siteprobe",
      "args": ["serve-mcp"]
    }
  }
}
```

### Exposed MCP Tools:
* `start_audit(url, max_pages, language)`: Initiates background audit job.
* `get_audit_status(job_id)`: Checks job status.
* `get_findings(job_id, category, severity)`: Returns filtered audit findings.
* `get_geo_findings(job_id)`: Returns GEO score and AI crawler accessibility.
* `create_remediation_plan(job_id)`: Generates actionable fix plan.
* `apply_safe_fixes(job_id, repo_path)`: Applies safe code modifications.
* `verify_fixes(job_id, repo_path)`: Verifies fix results.
* `generate_report(job_id, format)`: Exports report in HTML, JSON, or Markdown.

---

## 🔗 External Integrations

All external integrations are strictly optional and degrade gracefully:

* **Google Search Console**: Set `GOOGLE_APPLICATION_CREDENTIALS` to correlate audit findings with impressions, CTR, and search queries.
* **Google Analytics 4**: Set `GA4_PROPERTY_ID` to connect technical defects with conversion drop-offs.
* **DataForSEO**: Set `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` for SERP volume and backlink data.
* **Lighthouse / Chrome**: Available automatically when Node.js and Chrome are detected.
* **Playwright**: Installed via `pip install "siteprobe[browser]"`.

---

## 🐳 Docker

Run SiteProbe via Docker with zero host dependencies:

```bash
docker build -t siteprobe .
docker run --rm -v $(pwd)/reports:/app/reports siteprobe audit https://example.com --output /app/reports
```

Or with `docker-compose`:
```bash
docker-compose up
```

---

## 🏗️ Architecture

```text
siteprobe/
├── src/siteprobe/
│   ├── cli/          # Typer CLI commands
│   ├── core/         # Audit orchestrator, scoring model, YAML loader
│   ├── crawler/      # AsyncIO polite crawler, SQLite storage, robots/sitemaps
│   ├── checks/       # 9 check categories (Technical, Onpage, Schema, GEO, etc.)
│   ├── integrations/ # Modular adapters (GSC, GA4, DataForSEO, Lighthouse, Playwright)
│   ├── remediation/  # Risk-classified planner, atomic file handlers, snapshot/rollback
│   ├── verification/ # Post-fix verification engine
│   ├── reporting/    # Interactive HTML dashboard, JSON, and Markdown reporters
│   ├── i18n/         # Locales (English, Persian, Turkish) and translation engine
│   ├── models/       # Pydantic data schemas
│   └── mcp/          # FastMCP / Standard MCP server
├── skills/
│   └── siteprobe/    # Canonical Agent Skill (SKILL.md, references, scripts)
├── tests/            # Automated test suite + mock website fixture
└── docs/             # Technical architecture and user guides
```

---

## 🛡️ Remediation Safety & Rollback

SiteProbe is engineered with defensive patterns:
* **Pre-Flight Snapshot**: Every file about to be edited is captured in an in-memory snapshot.
* **Format Preservation**: HTML changes use semantic tag injection preserving surrounding structure.
* **Automatic Rollback**: If a verification check fails after editing, SiteProbe can immediately restore files to their exact pre-fix state.
* **Clean Diffs**: Unified diffs are printed to the console and saved in remediation reports.

---

## 🗺️ Roadmap

- [x] v0.1.0: Core async crawler with SQLite storage
- [x] v0.1.0: 24 deterministic checks across 9 categories
- [x] v0.1.0: GEO / AI-search readiness scoring
- [x] v0.1.0: Remediation framework with safe autofixes
- [x] v0.1.0: Before/after verification engine
- [x] v0.1.0: Standalone interactive HTML reporting
- [x] v0.1.0: Multilingual support (en, fa, tr)
- [x] v0.1.0: FastMCP server & Agent Skill specification
- [ ] v0.2.0: Deep JS rendering via Playwright cluster
- [ ] v0.2.0: Automated GitHub Pull Request creator (`siteprobe pr`)
- [ ] v0.3.0: WordPress & Shopify headless API remediation plugins

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

```bash
# Run test suite
pytest -v
```

---

## 🔒 Security

For security vulnerability disclosures, please review [SECURITY.md](SECURITY.md) and contact [taqimolavi@gmail.com](mailto:taqimolavi@gmail.com).

---

## 📄 License

SiteProbe is licensed under the [MIT License](LICENSE).
Copyright &copy; 2026 Taqi Molavi.
