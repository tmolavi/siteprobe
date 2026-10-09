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


class UpdateTriageResult(BaseModel):
    """Comprehensive diagnostic result for algorithm update impact triage."""
    event: str = EVENT_NAME
    rollout_dates: Dict[str, str] = Field(
        default_factory=lambda: {"start": ROLLOUT_START, "end": ROLLOUT_END}
    )
    status: str
    diagnostic: str
    diagnostic_reason: str
    pre_metrics: Optional[WindowMetrics] = None
    rollout_metrics: Optional[WindowMetrics] = None
    completion_day_metrics: Optional[WindowMetrics] = None
    post_metrics: Optional[WindowMetrics] = None
    click_change_percent: Optional[float] = None
    impression_change_percent: Optional[float] = None
    ctr_change_points: Optional[float] = None
    position_interpretation_note: Optional[str] = None
    query_level_changes: List[DimensionDelta] = Field(default_factory=list)
    page_level_changes: List[DimensionDelta] = Field(default_factory=list)
    device_breakdown: Dict[str, Any] = Field(default_factory=dict)
    country_breakdown: Dict[str, Any] = Field(default_factory=dict)
    technical_audit: Optional[TechnicalAuditSummary] = None
    manual_action_reported: Optional[bool] = None
    validation_warnings: List[str] = Field(default_factory=list)
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
