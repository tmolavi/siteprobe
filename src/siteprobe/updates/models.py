import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from siteprobe.updates.constants import (
    DISCLAIMER_TEXT,
    EVENT_NAME,
    ROLLOUT_END,
    ROLLOUT_START,
)


class GscDataRow(BaseModel):
    """Represents a validated row of Google Search Console performance data."""
    date: datetime.date
    clicks: int = Field(..., ge=0, description="Non-negative total clicks")
    impressions: int = Field(..., ge=0, description="Non-negative total impressions")
    query: Optional[str] = None
    page: Optional[str] = None
    country: Optional[str] = None
    device: Optional[str] = None
    position: Optional[float] = Field(default=None, ge=1.0, description="Average rank position (>= 1.0)")
    ctr: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Click-through rate (0.0 to 1.0)")


class WindowMetrics(BaseModel):
    """Metrics calculated strictly across a frozen calendar window."""
    window_name: str
    start_date: str
    end_date: str
    days_expected: int
    days_present: int
    is_complete: bool
    status: str = "COMPLETE"  # "COMPLETE" or "INCOMPLETE"
    total_clicks: int = 0
    total_impressions: int = 0
    ctr: float = 0.0  # Computed strictly as total_clicks / total_impressions
    avg_position: Optional[float] = None
    daily_breakdown: List[Dict[str, Any]] = Field(default_factory=list)


class DimensionDelta(BaseModel):
    """Change analysis for an optional dimension like query or page."""
    dimension: str
    value: str
    pre_clicks: int = 0
    rollout_clicks: int = 0
    click_change: int = 0
    pre_impressions: int = 0
    rollout_impressions: int = 0
    impression_change: int = 0
    pre_position: Optional[float] = None
    rollout_position: Optional[float] = None


class TechnicalAuditSummary(BaseModel):
    """Summary of deterministic technical checks relevant to indexation & traffic drops."""
    has_blocking_issues: bool = False
    http_errors_count: int = 0
    robots_disallowed: bool = False
    noindex_detected: bool = False
    canonical_issues_count: int = 0
    redirect_issues_count: int = 0
    ssr_issues_count: int = 0
    sitemap_issues_count: int = 0
    critical_findings: List[Dict[str, Any]] = Field(default_factory=list)


class BaselineVariability(BaseModel):
    """Site-specific daily performance variance computed from pre-update historical data."""
    daily_clicks_mean: Optional[float] = None
    daily_clicks_std: Optional[float] = None
    daily_clicks_cv: Optional[float] = None  # Coefficient of variation (std / mean)
    daily_impressions_mean: Optional[float] = None
    daily_impressions_std: Optional[float] = None
    daily_impressions_cv: Optional[float] = None
    baseline_period_days: int = 14


class DataQualityReport(BaseModel):
    """Integrity and origin assessment of input Search Console data."""
    status: str = "OK"  # "OK", "DATA_UNAVAILABLE", "INCOMPLETE_PERIODS", "VALIDATION_FAILED"
    data_type: str = "REAL"  # "REAL" or "SYNTHETIC"
    missing_dates: List[str] = Field(default_factory=list)
    duplicate_rows: int = 0
    validation_warnings: List[str] = Field(default_factory=list)


class EventInfo(BaseModel):
    """Declared Google algorithm rollout event metadata."""
    name: str = EVENT_NAME
    rollout_start: str = ROLLOUT_START
    completion: str = ROLLOUT_END


class WindowsContainer(BaseModel):
    """Frozen sequential calendar windows."""
    pre: Optional[WindowMetrics] = None
    rollout: Optional[WindowMetrics] = None
    completion: Optional[WindowMetrics] = None
    post: Optional[WindowMetrics] = None


class MetricsContainer(BaseModel):
    """Descriptive change measurements and site-specific variability context."""
    click_change_percent: Optional[float] = None
    impression_change_percent: Optional[float] = None
    ctr_change: Optional[float] = None
    baseline_variability: Optional[BaselineVariability] = None
    change_significance: str = "UNKNOWN"  # Statistical significance: "UNKNOWN" (heuristic envelope is not a formal significance test)
    change_significance_details: Optional[str] = None
    position_interpretation_note: Optional[str] = None


class UpdateTriageResult(BaseModel):
    """Comprehensive diagnostic result for algorithm update impact triage."""
    event: EventInfo = Field(default_factory=EventInfo)
    data_quality: DataQualityReport = Field(default_factory=DataQualityReport)
    windows: WindowsContainer = Field(default_factory=WindowsContainer)
    metrics: MetricsContainer = Field(default_factory=MetricsContainer)
    technical_findings: List[Dict[str, Any]] = Field(default_factory=list)
    manual_action: str = "UNKNOWN"  # "REPORTED", "CLEAN", "UNKNOWN"
    classification: str = "INSUFFICIENT_DATA"
    diagnostic_classification: str = "INSUFFICIENT_DATA"
    diagnostic: str = "INSUFFICIENT_DATA"
    diagnostic_reason: str = ""
    status: str = "OK"
    
    # Backward compatibility fields (direct access)
    pre_metrics: Optional[WindowMetrics] = None
    rollout_metrics: Optional[WindowMetrics] = None
    completion_day_metrics: Optional[WindowMetrics] = None
    post_metrics: Optional[WindowMetrics] = None
    click_change_percent: Optional[float] = None
    impression_change_percent: Optional[float] = None
    ctr_change_points: Optional[float] = None
    position_interpretation_note: Optional[str] = None
    technical_audit: Optional[TechnicalAuditSummary] = None
    manual_action_reported: Optional[bool] = None
    validation_warnings: List[str] = Field(default_factory=list)

    # Dimensional breakdowns
    query_level_changes: List[DimensionDelta] = Field(default_factory=list)
    page_level_changes: List[DimensionDelta] = Field(default_factory=list)
    device_breakdown: Dict[str, Any] = Field(default_factory=dict)
    country_breakdown: Dict[str, Any] = Field(default_factory=dict)

    limitations: List[str] = Field(
        default_factory=lambda: [
            "Search Console data has an inherent 48-72 hour reporting delay.",
            "Average position shifts must not be interpreted without query composition context.",
            "Correlation with update rollout dates does not prove algorithm causation.",
            "The POST-update window is incomplete as of 2026-10-09; no future observations are inferred.",
            "SiteProbe cannot inspect Google's internal SpamBrain algorithms or manual review queues.",
        ]
    )
    disclaimer: str = DISCLAIMER_TEXT

    def sync_nested_and_flat(self) -> None:
        """Syncs nested containers with flat backward-compatible fields."""
        if self.windows.pre:
            self.pre_metrics = self.windows.pre
        elif self.pre_metrics:
            self.windows.pre = self.pre_metrics

        if self.windows.rollout:
            self.rollout_metrics = self.windows.rollout
        elif self.rollout_metrics:
            self.windows.rollout = self.rollout_metrics

        if self.windows.completion:
            self.completion_day_metrics = self.windows.completion
        elif self.completion_day_metrics:
            self.windows.completion = self.completion_day_metrics

        if self.windows.post:
            self.post_metrics = self.windows.post
        elif self.post_metrics:
            self.windows.post = self.post_metrics

        if self.metrics.click_change_percent is not None:
            self.click_change_percent = self.metrics.click_change_percent
        elif self.click_change_percent is not None:
            self.metrics.click_change_percent = self.click_change_percent

        if self.metrics.impression_change_percent is not None:
            self.impression_change_percent = self.metrics.impression_change_percent
        elif self.impression_change_percent is not None:
            self.metrics.impression_change_percent = self.impression_change_percent

        if self.metrics.ctr_change is not None:
            self.ctr_change_points = self.metrics.ctr_change
        elif self.ctr_change_points is not None:
            self.metrics.ctr_change = self.ctr_change_points

        if self.validation_warnings and not self.data_quality.validation_warnings:
            self.data_quality.validation_warnings = self.validation_warnings
        elif self.data_quality.validation_warnings and not self.validation_warnings:
            self.validation_warnings = self.data_quality.validation_warnings

        self.classification = self.diagnostic
        self.diagnostic_classification = self.diagnostic
