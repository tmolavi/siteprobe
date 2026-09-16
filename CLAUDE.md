# Claude Code & Antigravity Instructions for SiteProbe

Refer to `skills/siteprobe/SKILL.md` for complete trigger and phase definitions.

## Key CLI Commands
- `siteprobe audit <url>`: Run deep public website crawl and multi-category audit.
- `siteprobe fix <audit.json> --repo <path>`: Apply safe automated fixes with rollback snapshots.
- `siteprobe verify <audit.json> --repo <path>`: Verify resolution of detected issues.
- `siteprobe doctor`: Inspect local tools (Python, Lighthouse, Playwright, GSC/GA4 keys).
- `siteprobe serve-mcp`: Run MCP server over stdio for agent tool calling.

## Operational Discipline
- **Audit → Evidence → Plan → Fix → Verify → Report**.
- Never claim an issue is fixed unless `siteprobe verify` passes.
