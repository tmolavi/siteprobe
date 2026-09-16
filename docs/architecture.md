# SiteProbe Architectural Design

SiteProbe operates on an explicit 6-stage lifecycle:
**Audit → Evidence → Plan → Fix → Verify → Report**

### Design Principles
1. **Zero Hallucination**: No fake Search Console data, no simulated rankings, no fabricated metrics. If a capability or credential is missing, SiteProbe marks it as `OPTIONAL / UNAVAILABLE` and explains how to enable it.
2. **Deterministic Quality Scoring**: Scores are calculated with explicit, documented deduction weights across 6 categories.
3. **Transparent GEO Scoring**: The GEO score isolates AI search crawlability, structured knowledge (/llms.txt), entity attribution, and conversational question-and-answer semantic markup.
4. **Safe Remediation with Snapshot & Rollback**: Safe autofixes preserve code formatting, record file snapshots, and automatically rollback if verification fails.
