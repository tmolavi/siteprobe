from typing import Optional, Tuple

from siteprobe.updates.constants import (
    DIAGNOSTIC_INSUFFICIENT_DATA,
    DIAGNOSTIC_MANUAL_ACTION,
    DIAGNOSTIC_NO_CLEAR_CHANGE,
    DIAGNOSTIC_PERFORMANCE_CHANGE,
    DIAGNOSTIC_TECHNICAL_ISSUE,
    STATUS_DATA_UNAVAILABLE,
)
from siteprobe.updates.models import TechnicalAuditSummary, WindowMetrics


def classify_update_impact(
    pre_metrics: Optional[WindowMetrics],
    rollout_metrics: Optional[WindowMetrics],
    click_change_pct: Optional[float],
    imp_change_pct: Optional[float],
    technical_summary: Optional[TechnicalAuditSummary],
    manual_action_reported: Optional[bool] = None,
    change_significance: str = "UNKNOWN",
    change_significance_details: Optional[str] = None,
    data_unavailable: bool = False,
) -> Tuple[str, str, str]:
    """
    Determines diagnostic classification based strictly on empirical evidence.
    
    Returns:
        (status, diagnostic, reason)
        
    Strict Rules:
    - Never infer a manual action from falling traffic. Must come from Search Console evidence.
    - Keep technical findings separate from algorithmic-update correlation.
    - Never claim to detect Google's private spam classifier or prove causality.
    - Does NOT use an arbitrary universal +/-15% threshold; relies on site baseline variability.
    """
    if data_unavailable or pre_metrics is None or rollout_metrics is None:
        return (
            STATUS_DATA_UNAVAILABLE,
            DIAGNOSTIC_INSUFFICIENT_DATA,
            "Search Console performance data is unavailable. Neither active GSC API credentials "
            "nor a valid user-supplied CSV export was provided.",
        )

    # Check comparison period completeness
    if not pre_metrics.is_complete or not rollout_metrics.is_complete:
        missing_parts = []
        if not pre_metrics.is_complete:
            missing_parts.append(f"PRE window ({pre_metrics.days_present}/{pre_metrics.days_expected} days)")
        if not rollout_metrics.is_complete:
            missing_parts.append(f"ROLLOUT window ({rollout_metrics.days_present}/{rollout_metrics.days_expected} days)")
        return (
            DIAGNOSTIC_INSUFFICIENT_DATA,
            DIAGNOSTIC_INSUFFICIENT_DATA,
            f"Comparison periods are incomplete: {', '.join(missing_parts)}. "
            "PRE and ROLLOUT must each contain 14 complete days with matched weekdays.",
        )

    # Check zero impressions baseline
    if pre_metrics.total_impressions == 0 and rollout_metrics.total_impressions == 0:
        return (
            DIAGNOSTIC_INSUFFICIENT_DATA,
            DIAGNOSTIC_INSUFFICIENT_DATA,
            "Zero impressions recorded across both the PRE and ROLLOUT comparison windows. "
            "Cannot establish a baseline for performance triage.",
        )

    # Priority 1: Verified Manual Action in Search Console
    if manual_action_reported is True:
        return (
            DIAGNOSTIC_MANUAL_ACTION,
            DIAGNOSTIC_MANUAL_ACTION,
            "Verified Google Search Console manual action reported on this property. "
            "Manual actions represent direct human-reviewer penalties and supersede algorithmic fluctuations.",
        )

    # Priority 2: Technical website issues detected by SiteProbe
    if technical_summary and technical_summary.has_blocking_issues:
        reasons = []
        if technical_summary.http_errors_count > 0:
            reasons.append(f"{technical_summary.http_errors_count} HTTP client/server errors")
        if technical_summary.noindex_detected:
            reasons.append("unintended noindex directive(s)")
        if technical_summary.robots_disallowed:
            reasons.append("crawler-blocking robots.txt directive(s)")
        if technical_summary.canonical_issues_count > 0:
            reasons.append("canonical tag conflict(s)")
        if technical_summary.redirect_issues_count > 0:
            reasons.append("redirect chain or loop issue(s)")
        if technical_summary.ssr_issues_count > 0:
            reasons.append("empty SPA root shell / unrendered server HTML")

        reason_str = ", ".join(reasons) if reasons else "critical technical SEO anomalies"
        return (
            DIAGNOSTIC_TECHNICAL_ISSUE,
            DIAGNOSTIC_TECHNICAL_ISSUE,
            f"Technical audit revealed blocking site issues ({reason_str}) that impair crawling, "
            "indexation, or rendering independently of any search engine algorithm update.",
        )

    # Priority 3: Statistically evaluated Performance Change
    c_pct_str = f"{click_change_pct:+.1f}%" if click_change_pct is not None else "0.0%"
    i_pct_str = f"{imp_change_pct:+.1f}%" if imp_change_pct is not None else "0.0%"

    if change_significance == "SIGNIFICANT_RELATIVE_TO_BASELINE":
        details = f" ({change_significance_details})" if change_significance_details else ""
        if click_change_pct is not None and click_change_pct < 0:
            return (
                DIAGNOSTIC_PERFORMANCE_CHANGE,
                DIAGNOSTIC_PERFORMANCE_CHANGE,
                f"Observed Search Console performance decline (clicks: {c_pct_str}, impressions: {i_pct_str}) "
                f"during rollout with no manual actions or blocking technical errors detected{details}. "
                "Possible algorithm-update correlation. Causality is explicitly not claimed.",
            )
        else:
            return (
                DIAGNOSTIC_PERFORMANCE_CHANGE,
                DIAGNOSTIC_PERFORMANCE_CHANGE,
                f"Observed Search Console performance gain (clicks: {c_pct_str}, impressions: {i_pct_str}) "
                f"during rollout with no manual actions or blocking technical errors detected{details}.",
            )
    elif change_significance == "WITHIN_BASELINE_VARIABILITY":
        details = f" ({change_significance_details})" if change_significance_details else ""
        return (
            DIAGNOSTIC_NO_CLEAR_CHANGE,
            DIAGNOSTIC_NO_CLEAR_CHANGE,
            f"Search Console performance fluctuations (clicks: {c_pct_str}, impressions: {i_pct_str}) "
            f"remain within the site's own pre-update baseline daily variability envelope{details}.",
        )

    # Priority 4: Fallback when baseline variability is UNKNOWN
    # If a clear non-zero change exists, report observed change descriptively without claiming universal threshold
    if click_change_pct is not None and abs(click_change_pct) > 0.0:
        return (
            DIAGNOSTIC_PERFORMANCE_CHANGE,
            DIAGNOSTIC_PERFORMANCE_CHANGE,
            f"A measurable performance change was observed during the defined comparison period "
            f"(clicks: {c_pct_str}, impressions: {i_pct_str}). Baseline historical variability could not "
            "be fully calculated. Possible update correlation; causality is not claimed.",
        )

    return (
        DIAGNOSTIC_NO_CLEAR_CHANGE,
        DIAGNOSTIC_NO_CLEAR_CHANGE,
        f"Search Console performance remained unchanged between PRE and ROLLOUT windows "
        f"(clicks: {c_pct_str}, impressions: {i_pct_str}).",
    )
