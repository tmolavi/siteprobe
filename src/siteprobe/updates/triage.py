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
    compute_baseline_variability,
    compute_categorical_breakdown,
    compute_dimension_deltas,
    evaluate_change_significance,
)
from siteprobe.updates.models import (
    DataQualityReport,
    EventInfo,
    GscDataRow,
    MetricsContainer,
    TechnicalAuditSummary,
    UpdateTriageResult,
    WindowMetrics,
    WindowsContainer,
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
        data_type = "REAL"

        # 1. Resolve Search Console Data
        if self.csv_source is not None:
            # Check for synthetic benchmark indicator
            if isinstance(self.csv_source, (str, Path)):
                try:
                    s_str = str(self.csv_source)
                    if Path(s_str).exists():
                        raw_preview = Path(s_str).read_text(encoding="utf-8-sig", errors="ignore")[:500]
                        if "SYNTHETIC" in raw_preview.upper():
                            data_type = "SYNTHETIC"
                    elif "SYNTHETIC" in s_str.upper():
                        data_type = "SYNTHETIC"
                except Exception:
                    pass

            parsed_rows, parse_warns = validate_and_parse_gsc_csv(self.csv_source)
            rows = parsed_rows
            warnings.extend(parse_warns)
            if any("SYNTHETIC" in w for w in parse_warns):
                data_type = "SYNTHETIC"
        elif self.gsc_integration.is_available():
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
            dq = DataQualityReport(
                status=STATUS_DATA_UNAVAILABLE,
                data_type=data_type,
                missing_dates=[],
                duplicate_rows=0,
                validation_warnings=["No Search Console data source provided."],
            )
            res = UpdateTriageResult(
                event=EventInfo(),
                data_quality=dq,
                status=status,
                classification=diagnostic,
                diagnostic_classification=diagnostic,
                diagnostic=diagnostic,
                diagnostic_reason=reason,
                manual_action="UNKNOWN",
                manual_action_reported=self.manual_action_reported,
                validation_warnings=["No Search Console data source provided."],
            )
            res.sync_nested_and_flat()
            return res

        # 2. Compute Frozen Comparison Windows
        pre, rollout, completion, post, click_pct, imp_pct, ctr_pts, win_warns = analyze_windows(rows)
        warnings.extend(win_warns)

        # 3. Compute Site-Specific Baseline Variability (PRE window)
        baseline_var = compute_baseline_variability(pre)
        significance, sig_details = evaluate_change_significance(click_pct, imp_pct, baseline_var)

        # 4. Dimensional Analysis (Optional dimensions)
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

        # 5. Technical Audit Evaluation
        technical_summary = evaluate_findings(self.audit_findings) if self.audit_findings else None

        # 6. Diagnostic Classification
        status, diagnostic, reason = classify_update_impact(
            pre_metrics=pre,
            rollout_metrics=rollout,
            click_change_pct=click_pct,
            imp_change_pct=imp_pct,
            technical_summary=technical_summary,
            manual_action_reported=self.manual_action_reported,
            change_significance=significance,
            change_significance_details=sig_details,
        )

        missing_dates = []
        if not pre.is_complete:
            missing_dates.append(f"PRE: missing {pre.days_expected - pre.days_present} days")
        if not rollout.is_complete:
            missing_dates.append(f"ROLLOUT: missing {rollout.days_expected - rollout.days_present} days")

        dq_status = "OK" if (pre.is_complete and rollout.is_complete) else "INCOMPLETE_PERIODS"
        dq = DataQualityReport(
            status=dq_status,
            data_type=data_type,
            missing_dates=missing_dates,
            duplicate_rows=0,
            validation_warnings=warnings,
        )

        windows = WindowsContainer(
            pre=pre,
            rollout=rollout,
            completion=completion,
            post=post,
        )

        metrics = MetricsContainer(
            click_change_percent=click_pct,
            impression_change_percent=imp_pct,
            ctr_change=ctr_pts,
            baseline_variability=baseline_var,
            change_significance=significance,
            change_significance_details=sig_details,
            position_interpretation_note=position_note,
        )

        manual_act_str = "REPORTED" if self.manual_action_reported is True else (
            "CLEAN" if self.manual_action_reported is False else "UNKNOWN"
        )

        res = UpdateTriageResult(
            event=EventInfo(),
            data_quality=dq,
            windows=windows,
            metrics=metrics,
            technical_findings=technical_summary.critical_findings if technical_summary else [],
            manual_action=manual_act_str,
            status=status,
            classification=diagnostic,
            diagnostic_classification=diagnostic,
            diagnostic=diagnostic,
            diagnostic_reason=reason,
            query_level_changes=query_deltas,
            page_level_changes=page_deltas,
            device_breakdown=device_breakdown,
            country_breakdown=country_breakdown,
            technical_audit=technical_summary,
            manual_action_reported=self.manual_action_reported,
            validation_warnings=warnings,
        )
        res.sync_nested_and_flat()
        return res
