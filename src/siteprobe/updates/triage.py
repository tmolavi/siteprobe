import io
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from siteprobe.core.engine import AuditResult
from siteprobe.integrations.search_console import SearchConsoleIntegration
from siteprobe.models.finding import Finding
from siteprobe.updates.classifier import classify_update_impact
from siteprobe.updates.constants import (
    DIAGNOSTIC_INSUFFICIENT_DATA,
    EVENT_NAME,
    POST_WINDOW_DAYS,
    POST_WINDOW_END,
    POST_WINDOW_START,
    STATUS_DATA_UNAVAILABLE,
)
from siteprobe.updates.metrics import (
    analyze_windows,
    compute_categorical_breakdown,
    compute_dimension_deltas,
)
from siteprobe.updates.models import (
    GscDataRow,
    TechnicalAuditSummary,
    UpdateTriageResult,
    WindowMetrics,
)
from siteprobe.updates.technical_evaluator import evaluate_findings
from siteprobe.updates.validator import validate_and_parse_gsc_csv


class UpdateImpactTriage:
    """
    Orchestrates evidence-based Google Spam Update impact triage.
    Distinguishes observed GSC performance shifts, technical site errors,
    manual actions, and potential update correlations without over-claiming.
    """

    def __init__(
        self,
        csv_source: Optional[Union[str, Path, io.StringIO]] = None,
        site_url: Optional[str] = None,
        manual_action_reported: Optional[bool] = None,
        audit_findings: Optional[List[Finding]] = None,
        gsc_integration: Optional[SearchConsoleIntegration] = None,
    ):
        self.csv_source = csv_source
        self.site_url = site_url
        self.manual_action_reported = manual_action_reported
        self.audit_findings = audit_findings or []
        self.gsc_integration = gsc_integration or SearchConsoleIntegration()

    def run(self) -> UpdateTriageResult:
        warnings: List[str] = []
        rows: Optional[List[GscDataRow]] = None

        # 1. Resolve Search Console Data
        if self.csv_source is not None:
            parsed_rows, parse_warns = validate_and_parse_gsc_csv(self.csv_source)
            rows = parsed_rows
            warnings.extend(parse_warns)
        elif self.gsc_integration.is_available():
            # In live production with credentials configured
            # For triage, requires historical CSV or full query export
            warnings.append("GSC API credentials configured, but historical window CSV is preferred for freeze analysis.")
            rows = None
        else:
            rows = None

        # If data is completely unavailable
        if rows is None:
            status, diagnostic, reason = classify_update_impact(
                pre_metrics=None,
                rollout_metrics=None,
                click_change_pct=None,
                imp_change_pct=None,
                technical_summary=None,
                manual_action_reported=self.manual_action_reported,
                data_unavailable=True,
            )
            return UpdateTriageResult(
                status=status,
                diagnostic=diagnostic,
                diagnostic_reason=reason,
                manual_action_reported=self.manual_action_reported,
                validation_warnings=["No Search Console data source provided."],
            )

        # 2. Compute Frozen Comparison Windows
        pre, rollout, completion, post, click_pct, imp_pct, ctr_pts, win_warns = analyze_windows(rows)
        warnings.extend(win_warns)

        # 3. Dimensional Analysis (Optional dimensions)
        has_queries = any(r.query for r in rows)
        has_pages = any(r.page for r in rows)
        has_devices = any(r.device for r in rows)
        has_countries = any(r.country for r in rows)
        has_positions = any(r.position is not None for r in rows)

        pre_rows = [r for r in rows if pre.start_date <= r.date.isoformat() <= pre.end_date]
        rollout_rows = [r for r in rows if rollout.start_date <= r.date.isoformat() <= rollout.end_date]

        query_deltas = compute_dimension_deltas(pre_rows, rollout_rows, "query") if has_queries else []
        page_deltas = compute_dimension_deltas(pre_rows, rollout_rows, "page") if has_pages else []
        device_breakdown = compute_categorical_breakdown(pre_rows, rollout_rows, "device") if has_devices else {}
        country_breakdown = compute_categorical_breakdown(pre_rows, rollout_rows, "country") if has_countries else {}

        position_note = None
        if has_positions:
            position_note = (
                "Average position changes must be evaluated alongside query impression composition. "
                "Shifts in query mix or lost long-tail impressions can artificially change average position "
                "even without algorithmic ranking demotions."
            )

        # 4. Technical Audit Evaluation
        technical_summary = evaluate_findings(self.audit_findings) if self.audit_findings else None

        # 5. Diagnostic Classification
        status, diagnostic, reason = classify_update_impact(
            pre_metrics=pre,
            rollout_metrics=rollout,
            click_change_pct=click_pct,
            imp_change_pct=imp_pct,
            technical_summary=technical_summary,
            manual_action_reported=self.manual_action_reported,
        )

        return UpdateTriageResult(
            status=status,
            diagnostic=diagnostic,
            diagnostic_reason=reason,
            pre_metrics=pre,
            rollout_metrics=rollout,
            completion_day_metrics=completion,
            post_metrics=post,
            click_change_percent=click_pct,
            impression_change_percent=imp_pct,
            ctr_change_points=ctr_pts,
            position_interpretation_note=position_note,
            query_level_changes=query_deltas,
            page_level_changes=page_deltas,
            device_breakdown=device_breakdown,
            country_breakdown=country_breakdown,
            technical_audit=technical_summary,
            manual_action_reported=self.manual_action_reported,
            validation_warnings=warnings,
        )
