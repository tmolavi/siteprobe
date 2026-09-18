#!/usr/bin/env python3
"""
SiteProbe Public Demo
[STANDALONE_DEMO_FIXTURE] — Closed-Loop Autonomous Remediation Demo

Demonstrates SiteProbe's complete 3-step closed-loop lifecycle:
1. Audit Target Website (Extract diagnostic deficiencies across SEO, AEO, and GEO).
2. Generate Safe Remediation Patches (Schema injection, llms.txt generation, robot directives).
3. Verify Remediation & Quantify Delta (Re-audit proving measurable score improvement).
"""

import json
from pathlib import Path

DEMO_DIR = Path(__file__).parent

def run():
    before_file = DEMO_DIR / "audit_before.json"
    patches_file = DEMO_DIR / "recommended_changes.json"
    after_file = DEMO_DIR / "audit_after.json"

    with open(before_file, "r", encoding="utf-8") as f:
        before_data = json.load(f)
    with open(patches_file, "r", encoding="utf-8") as f:
        patches_data = json.load(f)
    with open(after_file, "r", encoding="utf-8") as f:
        after_data = json.load(f)

    print("=" * 70)
    print("SiteProbe: Closed-Loop Autonomous Remediation Demo")
    print("=" * 70)
    print(f"• Target Site         : {before_data['url']}")
    print(f"• Initial Health Score: {before_data['composite_score']}/100 ({before_data['status']})")
    print("-" * 70)

    print("Phase 1: Diagnostic Deficiency Detection")
    for cat, info in before_data["categories"].items():
        issues_str = f"({', '.join(info['issues'])})" if info['issues'] else "None"
        print(f"  • {cat.capitalize():15}: {info['score']:5.1f}/100 — Issues: {issues_str}")

    print("\nPhase 2: Generating Deterministic Remediation Patches")
    for patch in patches_data["patches"]:
        print(f"  ✓ [{patch['classification']}] {patch['id']} -> {patch['rule']} ({patch['target_file']})")

    print("\nPhase 3: Automated Verification & Quantifiable Impact")
    delta = after_data["delta"]
    print(f"  • New Health Score    : {after_data['composite_score']}/100 ({after_data['status']})")
    print(f"  • Score Improvement   : {delta['score_improvement']}")
    print(f"  • Issues Fixed        : {delta['fixed_issues']} issues resolved safely")
    print("=" * 70)
    print("✓ Closed-loop remediation successfully demonstrated offline.")
    print("=" * 70)

if __name__ == "__main__":
    run()
