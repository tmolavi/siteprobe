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
[Agent Skill](#-agent-skill-installation--exact-instructions) &bull;
[MCP Server](#-model-context-protocol-mcp) &bull;
[Honesty & Status Table](#-feature-status--honesty-table) &bull;
[Architecture](#-architecture)

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
* **Zero Hallucination**: No simulated rankings or fabricated Search Console numbers. If an external credential is missing, SiteProbe clearly marks it as optional/unavailable and explains how to connect it.
* **Deterministic Quality Scoring**: Transparent, explainable weights across Technical, On-Page, Schema, GEO, Accessibility, and Security.
* **Realistic GEO Metrics**: The GEO score is strictly a technical readiness index evaluating observable signals (AI crawler permissions in robots.txt, `/llms.txt` presence, structured entities, and question-answer semantics). It is **not** a guarantee or predictor of AI citations or rankings.
* **Safety First**: Every automated fix creates an in-memory file snapshot before applying changes and rolls back automatically if verification fails.
* **Multilingual from Day 1**: Native localized audits in English (`en`), Persian (`fa`), and Turkish (`tr`).

---

## 📋 Feature Status & Honesty Table

| Component / Feature | Implementation Status | Test Coverage | Description |
| :--- | :---: | :---: | :--- |
| **AsyncIO Crawler** | **WORKING** | Verified (Unit & Live) | Polite queue, adaptive backoff, SQLite storage, robots & sitemap parsing. |
| **Technical SEO Checks** | **WORKING** | Verified (Unit & Live) | HTTP status codes, broken links, redirect chains, canonicals, robots/sitemap. |
| **SSR & Hydration Audit** | **WORKING** | Verified (Unit & Live) | Framework signatures, client-only SPA empty shells, and raw server SEO tag parity. |
| **On-Page SEO Checks** | **WORKING** | Verified (Unit & Live) | Title/description lengths, duplicates, H1 hierarchy, alt tags, hreflangs. |
| **Schema.org Validator** | **WORKING** | Verified (Unit & Live) | JSON-LD syntax errors, Organization, Article, Breadcrumb, and FAQ schemas. |
| **GEO / AEO Readiness** | **WORKING** | Verified (Unit & Live) | Bot directives (OAI-SearchBot, PerplexityBot, ClaudeBot), `/llms.txt`, QA markup. |
| **Deterministic Scoring** | **WORKING** | Verified (Unit & Live) | 100% transparent formula with itemized deductions and pillar breakdowns. |
| **Safe Autofix Engine** | **WORKING** | Verified (Unit & Live) | Local file modifier for meta tags, canonicals, alt attributes, robots.txt, llms.txt. |
| **Verification Engine** | **WORKING** | Verified (Unit & Live) | Re-evaluates before/after states; assigns FIXED, IMPROVED, UNCHANGED, SKIPPED. |
| **Multi-format Reporting** | **WORKING** | Verified (Unit & Live) | Single-file zero-CDN HTML dashboard, structured JSON (`audit.json`), Markdown. |
| **Multilingual (i18n)** | **WORKING** | Verified (Unit & Live) | Native translations for English (`en`), Persian (`fa`), and Turkish (`tr`). |
| **MCP Server** | **WORKING** | Verified (Unit & Live) | FastMCP server exposing 14 tools (`start_audit`, `get_findings`, `apply_safe_fixes`). |
| **Lighthouse CLI** | **OPTIONAL** | Tested | Lab Core Web Vitals runner via local Node.js / `lighthouse` or `npx`. |
| **Playwright Automation** | **OPTIONAL** | Tested | Headless browser for SPA rendering (requires `pip install siteprobe[browser]`). |
| **Google Search Console** | **OPTIONAL** | Scaffolded | Adapter ready; requires `GOOGLE_APPLICATION_CREDENTIALS` (never simulated). |
| **Google Analytics 4** | **OPTIONAL** | Scaffolded | Adapter ready; requires `GA4_PROPERTY_ID` (never simulated). |
| **DataForSEO API** | **OPTIONAL** | Scaffolded | Adapter ready; requires `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`. |
| **AI LLM Reasoning** | **OPTIONAL** | Scaffolded | LiteLLM wrapper for deeper semantics (requires OpenAI/Anthropic/Gemini keys). |
| **SSH Server Fixer** | **ROADMAP** | Planned | Direct atomic remote patching over SSH key authentication. |
| **WordPress / CMS Plugins**| **ROADMAP** | Planned | Native CMS plugins for direct headless database and API remediation. |

---

## 🎯 From Measurement To Action: The Remediation Loop

SiteProbe serves as the **Autonomous Remediation & Verification Engine** for the [Molavi AI Visibility Stack](docs/BENCHMARK_ECOSYSTEM.md), turning empirical findings from [GEO-Scope Benchmarks](https://github.com/tmolavi/geo-scope/tree/main/benchmarks/geo-seo-digital-agency-iran-2026.1) into verified code remediations:

```text
┌─────────────────────────────────┐
│     1. BENCHMARK FINDING        │  Empirical visibility baseline measured via GEO-Scope
│   (e.g., Low AI Recommendation) │  (e.g., missing citations, unquoted brand entities)
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│        2. DEEP AUDIT            │  SiteProbe / SAGE analyzes DOM, headers, AI crawlers,
│  (Technical, Entity, Semantic)  │  passage chunk boundaries, and schema structures
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│     3. RECOMMENDATION PLAN      │  Deterministic, risk-stratified actionable fixes:
│  (SAFE_AUTOFIX / MANUAL_REVIEW) │  robots.txt bot policies, JSON-LD graphs, llms.txt
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│    4. SAFE IMPLEMENTATION       │  SiteProbe safely modifies source code repository
│   (Atomic Snapshot & Patch)     │  with automatic rollback on syntax or rule failure
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│    5. EMPIRICAL RE-MEASURE      │  GEO-Scope re-executes standardized prompt test suite
│  (Measure Δ SoM & Citations)    │  to measure verified lift in observed AI visibility
└─────────────────────────────────┘
```

See the [Benchmark Ecosystem Map](docs/BENCHMARK_ECOSYSTEM.md) for full architectural contracts.

## 🏛️ Ecosystem

SiteProbe operates as the autonomous remediation component of the **Molavi AI Visibility Stack**:

- **Discovery**: [AnswerPath GEO](https://github.com/tmolavi/answerpath-geo)
- **Measurement**: [GEO-Scope](https://github.com/tmolavi/geo-scope)
- **Diagnostics**: [SAGE Audit](https://github.com/tmolavi/sage-audit)
- **Action**: [SiteProbe](https://github.com/tmolavi/siteprobe)
- **Protocol**: [MCP GEO Server](https://github.com/tmolavi/mcp-geo-server)

## 📖 Sample Audit & Remediation Evidence

- Audit Findings Payload: [`examples/audit_example.json`](examples/audit_example.json)
- Verified Fix & Delta Payload: [`examples/fix_example.json`](examples/fix_example.json)

---

## 📊 Report Preview

SiteProbe generates a single-file, interactive HTML report with zero external CDN dependencies:
* **Interactive Scorecard**: Overall score and individual category health gauges.
* **GEO & AI Search Pillar Breakdown**: Transparent scoring for bot access, `llms.txt`, entity clarity, and QA markup.
* **Filterable Finding Cards**: Browse issues by severity (Critical, High, Medium, Low) and category.
* **Diff Viewer**: See unified code diffs of all remediations applied.

---

## 📦 Installation

### From Source (Clean Environment)

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
    print(f"GEO Readiness Score: {result.scores.geo_score}/100")
    print(f"Discovered {len(result.findings)} findings across {result.crawl_summary.total_crawled} pages.")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 💻 CLI Usage

### SSR & Rendering Inspection
Inspect initial raw server HTML for SSR vs. client-only SPA rendering, framework hydration payloads (Next.js, Nuxt, Remix, Astro), and missing raw SEO tags:
```bash
siteprobe ssr https://example.com
```

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

## 🤖 Agent Skill Installation & Exact Instructions

SiteProbe provides a canonical Agent Skill at:
[`skills/siteprobe/SKILL.md`](https://github.com/tmolavi/siteprobe/blob/main/skills/siteprobe/SKILL.md)

### 1. Claude Code
To equip Claude Code with SiteProbe, point to the skill folder or copy it into your local skill directory:
```bash
# Copy to local skills directory
mkdir -p ~/.claude/skills
cp -r skills/siteprobe ~/.claude/skills/
```
**Tested Invocation**:
```bash
claude "Read skills/siteprobe/SKILL.md and audit https://example.com, then fix safe issues in this project."
```

### 2. OpenAI Codex / CLI Agents
Codex reads repository guidelines from `AGENTS.md` in the project root:
```bash
codex "Audit https://example.com using the siteprobe CLI and verify all changes."
```

### 3. Google Gemini / Antigravity
In Antigravity or Gemini CLI, link the skill location in your configuration:
```json
{
  "skills": [
    "/path/to/siteprobe/skills/siteprobe/SKILL.md"
  ]
}
```
**Tested Invocation**:
> "Audit this website and fix all safe issues you can verify following the siteprobe skill workflow."

### 4. Cursor
In Cursor, reference the skill file in `.cursorrules` or mention the file directly in the chat prompt:
```text
@skills/siteprobe/SKILL.md Audit https://example.com and apply verified fixes.
```

---

## 🔌 Model Context Protocol (MCP)

Launch SiteProbe's MCP server over stdio:

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
- [ ] v0.2.0: Deep JS rendering via distributed Playwright cluster
- [ ] v0.2.0: Automated GitHub Pull Request creation CLI command (`siteprobe pr`)
- [ ] v0.3.0: Native headless CMS plugins for WordPress and Shopify API-based auto-remediation

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

---

## 💡 Related Projects & Inspiration

SiteProbe's SSR and rendering analysis draws architectural inspiration from prominent technical web tooling:
* **`is-ssr` & regex/ast hydration analyzers**: Inspecting hydration state payloads (`__NEXT_DATA__`, `__NUXT_DATA__`, `window.__remixContext`, `astro-island`).
* **`puppeteer-ssr-checker` & Rendertron**: Comparing initial raw server markup against rendered client DOM.
* **Model Context Protocol (`@modelcontextprotocol/server-puppeteer` & `server-fetch`)**: Standardizing browser inspection primitives and raw HTTP fetching for AI agents.

---
## 📄 License

SiteProbe is licensed under the [MIT License](LICENSE).
Copyright &copy; 2026 Taqi Molavi.
