# Remediation & Autofix Guide

SiteProbe partitions all remediations into three safety categories:
1. `SAFE_AUTOFIX`: Executed automatically when running `siteprobe fix`.
2. `REVIEW_RECOMMENDED`: Structural suggestions requiring developer review before merging.
3. `MANUAL_ONLY`: Architectural or editorial decisions.
