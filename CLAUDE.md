# Claude Code & Anthropic Assistant Guidelines for SiteProbe

SiteProbe is an autonomous website auditor, code remediator, and Google Algorithm Update impact triage engine.

---

## ⚡ First-Use Intake & Agent Checklist

When Claude Code or any Anthropic agent is prompted to use SiteProbe:

1. **Verify Environment**:
   - Check if CLI is available: `siteprobe --version`
   - If not installed, run: `pip install -e .`
   - Run diagnostic: `siteprobe doctor`
2. **Obtain Missing User Inputs**:
   - **Website Audit**: Prompt for target URL (`https://...`) and language (`en`, `fa`, `tr`).
   - **Google Update Triage**: Prompt for Google Search Console CSV (`--csv <path>` with `date`, `clicks`, `impressions`). If none exists, inform user or run synthetic sample (`examples/update-impact/sample-input.csv`).
   - **Remediation**: Prompt for local repository path (`--repo <path>`).
3. **Safety & Policy**:
   - Never fabricate GSC / GA4 observations.
   - Never infer manual actions from traffic drop.
   - Never claim an issue is resolved without passing `siteprobe verify`.

---

## 🛠️ CLI Cheat-Sheet

```bash
# Diagnostic & Capability Check
siteprobe doctor

# Full Autonomous Website Audit
siteprobe audit https://example.com --lang en --output ./siteprobe-report

# SSR vs Client-Side SPA Inspection
siteprobe check-ssr https://example.com

# September 2026 Google Spam Update Impact Triage
siteprobe update-triage --csv ./gsc_performance.csv --output ./triage-report.json

# Safe Automated Fixes & Verification Cycle
siteprobe fix ./siteprobe-report/audit.json --repo /path/to/project
siteprobe verify ./siteprobe-report/audit.json --repo /path/to/project

# Launch FastMCP Server (stdio)
siteprobe serve-mcp
```

---

## 🔌 FastMCP Configuration (Claude Desktop)

To configure SiteProbe as an MCP tool in Claude Desktop, add to `claude_desktop_config.json`:

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

---

## 🧪 Testing & Validation

```bash
# Run pytest suite
pytest -v

# Run type checks and linting
ruff check .
```
