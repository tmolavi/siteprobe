# SiteProbe Public Demo

`[STANDALONE_DEMO_FIXTURE]` — **Autonomous Closed-Loop Audit & Remediation Engine**

This demo shows SiteProbe's end-to-end remediation workflow:
1. **Audit Phase**: Identifies technical SEO, Schema markup, and GEO readiness gaps.
2. **Remediation Phase**: Proposes classified, deterministic autofixes (`llms.txt`, robots.txt rules, schema markup).
3. **Verification Phase**: Measures verified score deltas before and after remediation.

---

## Files

| File | Description |
|------|-------------|
| `audit_before.json` | Initial diagnostic state with identified deficiencies |
| `recommended_changes.json` | Generated safe autofixes and target file patches |
| `audit_after.json` | Post-remediation verification report showing score improvement |
| `run_demo.py` | Executable script walking through the closed-loop workflow |

---

## 🚀 How to Run (Under 10 Seconds)

```bash
python examples/public_demo/run_demo.py
```

### Expected Output
```text
======================================================================
SiteProbe: Closed-Loop Autonomous Remediation Demo
======================================================================
• Target Site         : https://example.local
• Initial Health Score: 71.5/100 (NEEDS_REMEDIATION)
----------------------------------------------------------------------
Phase 1: Diagnostic Deficiency Detection
  • Technical      :  85.0/100 — Issues: (missing_canonical_link, weak_cache_headers)
  • Schema         :  50.0/100 — Issues: (missing_organization_schema, missing_faq_schema)
  • Geo_readiness  :  60.0/100 — Issues: (missing_llms_txt, unstructured_passage_bounds)
  • Accessibility  :  91.0/100 — Issues: None

Phase 2: Generating Deterministic Remediation Patches
  ✓ [SAFE_AUTOFIX] FIX-001 -> create_llms_txt (public/llms.txt)
  ✓ [SAFE_AUTOFIX] FIX-002 -> inject_schema_markup (index.html)
  ✓ [SAFE_AUTOFIX] FIX-003 -> allow_ai_crawlers_robots_txt (public/robots.txt)

Phase 3: Automated Verification & Quantifiable Impact
  • New Health Score    : 94.2/100 (VERIFIED_OPTIMIZED)
  • Score Improvement   : +22.7 points
  • Issues Fixed        : 6 issues resolved safely
======================================================================
✓ Closed-loop remediation successfully demonstrated offline.
======================================================================
```
