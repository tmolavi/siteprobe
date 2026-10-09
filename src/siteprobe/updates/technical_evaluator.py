from typing import Any, Dict, List, Optional
from siteprobe.core.engine import AuditResult
from siteprobe.models.finding import Finding, FindingCategory, Severity
from siteprobe.updates.models import TechnicalAuditSummary


def evaluate_findings(findings: List[Finding]) -> TechnicalAuditSummary:
    """
    Evaluates findings from a SiteProbe audit specifically for technical indexability
    and rendering barriers that can trigger severe ranking/traffic losses.
    """
    summary = TechnicalAuditSummary()
    critical_items = []

    for f in findings:
        fid = f.id.lower()
        cat = f.category

        # 1. HTTP Errors (4xx, 5xx)
        if "technical.status.http_5xx" in fid or (f.severity == Severity.CRITICAL and "5xx" in f.title):
            summary.http_errors_count += 1
            summary.has_blocking_issues = True
            critical_items.append(f.to_dict())
        elif "technical.status.http_4xx" in fid:
            summary.http_errors_count += 1
            if f.severity in (Severity.HIGH, Severity.CRITICAL):
                summary.has_blocking_issues = True
                critical_items.append(f.to_dict())

        # 2. Robots.txt issues
        if "robots" in fid and ("missing" in fid or "block" in fid or "disallow" in fid):
            summary.robots_disallowed = True
            if f.severity in (Severity.HIGH, Severity.CRITICAL):
                summary.has_blocking_issues = True
                critical_items.append(f.to_dict())

        # 3. Noindex detection
        if "noindex" in fid or "noindex" in f.title.lower() or "not_indexable" in fid:
            summary.noindex_detected = True
            summary.has_blocking_issues = True
            critical_items.append(f.to_dict())

        # 4. Canonical issues
        if "canonical" in fid:
            summary.canonical_issues_count += 1
            if "mismatch" in fid or f.severity == Severity.HIGH:
                summary.has_blocking_issues = True
                critical_items.append(f.to_dict())

        # 5. Redirect loops / long chains
        if "redirect" in fid:
            summary.redirect_issues_count += 1
            if "loop" in fid or f.severity in (Severity.HIGH, Severity.CRITICAL):
                summary.has_blocking_issues = True
                critical_items.append(f.to_dict())

        # 6. SSR visibility & empty SPA shells
        if "ssr" in fid:
            summary.ssr_issues_count += 1
            if "client_only_rendering" in fid or "missing_raw_seo_tags" in fid:
                summary.has_blocking_issues = True
                critical_items.append(f.to_dict())

        # 7. Sitemap availability
        if "sitemap" in fid:
            summary.sitemap_issues_count += 1
            if "missing" in fid and f.severity in (Severity.HIGH, Severity.CRITICAL):
                critical_items.append(f.to_dict())

    summary.critical_findings = critical_items
    return summary


def evaluate_audit_result(audit_result: Optional[AuditResult]) -> Optional[TechnicalAuditSummary]:
    """Extracts technical health summary from an existing AuditResult."""
    if not audit_result:
        return None
    return evaluate_findings(audit_result.findings)
