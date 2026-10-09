import io
import pytest
from typer.testing import CliRunner

from siteprobe.cli.main import app
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.updates.constants import (
    DIAGNOSTIC_INSUFFICIENT_DATA,
    DIAGNOSTIC_MANUAL_ACTION,
    DIAGNOSTIC_NO_CHANGE,
    DIAGNOSTIC_PERFORMANCE_CHANGE,
    DIAGNOSTIC_TECHNICAL_ISSUE,
    STATUS_DATA_UNAVAILABLE,
)
from siteprobe.updates.triage import UpdateImpactTriage
from siteprobe.updates.validator import validate_and_parse_gsc_csv

runner = CliRunner()


def build_synthetic_csv(
    pre_days: int = 14,
    rollout_days: int = 14,
    pre_clicks: int = 100,
    rollout_clicks: int = 60,
    pre_imp: int = 2000,
    rollout_imp: int = 1500,
    include_completion: bool = True,
    include_post: bool = True,
) -> str:
    """Helper to generate well-formed synthetic CSV data."""
    lines = ["date,clicks,impressions,ctr,position,query,page,device,country"]

    # PRE: 2026-09-10 to 2026-09-23
    for i in range(pre_days):
        day = 10 + i
        lines.append(
            f"2026-09-{day:02d},{pre_clicks},{pre_imp},0.05,4.0,test query,https://example.com/,desktop,usa"
        )

    # ROLLOUT: 2026-09-24 to 2026-10-07
    for i in range(rollout_days):
        if i < 7:
            # Sep 24 to Sep 30
            day = 24 + i
            lines.append(
                f"2026-09-{day:02d},{rollout_clicks},{rollout_imp},0.04,5.5,test query,https://example.com/,desktop,usa"
            )
        else:
            # Oct 01 to Oct 07
            day = i - 6
            lines.append(
                f"2026-10-{day:02d},{rollout_clicks},{rollout_imp},0.04,5.5,test query,https://example.com/,desktop,usa"
            )

    if include_completion:
        lines.append(
            f"2026-10-08,{rollout_clicks},{rollout_imp},0.04,5.5,test query,https://example.com/,desktop,usa"
        )

    if include_post:
        lines.append(
            f"2026-10-09,{rollout_clicks},{rollout_imp},0.04,5.5,test query,https://example.com/,desktop,usa"
        )

    return "\n".join(lines)


# 1. Missing dates in comparison window
def test_missing_dates():
    # Only 13 days in PRE window instead of 14
    csv_data = build_synthetic_csv(pre_days=13, rollout_days=14)
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data))
    result = triage.run()

    assert result.diagnostic == DIAGNOSTIC_INSUFFICIENT_DATA
    assert result.pre_metrics is not None
    assert result.pre_metrics.is_complete is False
    assert result.pre_metrics.days_present == 13
    assert any("PRE window is incomplete" in w for w in result.validation_warnings)


# 2. Duplicate rows validation
def test_duplicate_rows():
    csv_data = (
        "date,clicks,impressions\n"
        "2026-09-10,10,200\n"
        "2026-09-10,10,200\n"  # Duplicate date without dimensions
    )
    with pytest.raises(ValueError, match="Duplicate row detected"):
        validate_and_parse_gsc_csv(csv_data)


# 3. Zero impressions
def test_zero_impressions_baseline():
    # All 14 days PRE and ROLLOUT present, but impressions = 0
    csv_data = build_synthetic_csv(pre_clicks=0, rollout_clicks=0, pre_imp=0, rollout_imp=0)
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data))
    result = triage.run()

    assert result.diagnostic == DIAGNOSTIC_INSUFFICIENT_DATA
    assert "Zero impressions" in result.diagnostic_reason


def test_zero_impressions_single_day_valid_ctr():
    # Single valid row with zero clicks and zero impressions: CTR must be 0.0
    csv_data = "date,clicks,impressions\n2026-09-10,0,0\n"
    rows, _ = validate_and_parse_gsc_csv(csv_data)
    assert len(rows) == 1
    assert rows[0].clicks == 0
    assert rows[0].impressions == 0
    assert rows[0].ctr == 0.0


# 4. Invalid CTR validation
def test_invalid_ctr_out_of_bounds():
    # CTR > 1.0 (e.g. 1.25)
    csv_data = "date,clicks,impressions,ctr\n2026-09-10,10,200,1.25\n"
    with pytest.raises(ValueError, match="Invalid CTR value"):
        validate_and_parse_gsc_csv(csv_data)

    # Clicks > impressions
    csv_data_impossible = "date,clicks,impressions\n2026-09-10,300,100\n"
    with pytest.raises(ValueError, match="Clicks .* cannot exceed impressions"):
        validate_and_parse_gsc_csv(csv_data_impossible)


# 5. Incomplete comparison periods
def test_incomplete_comparison_periods():
    # Incomplete rollout window (only 7 days)
    csv_data = build_synthetic_csv(pre_days=14, rollout_days=7)
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data))
    result = triage.run()

    assert result.diagnostic == DIAGNOSTIC_INSUFFICIENT_DATA
    assert result.click_change_percent is None  # Never compares incomplete periods!
    assert result.rollout_metrics.is_complete is False


def test_post_window_incomplete_handling():
    # Complete PRE and ROLLOUT, but POST has only 1 day
    csv_data = build_synthetic_csv(pre_days=14, rollout_days=14, include_post=True)
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data))
    result = triage.run()

    assert result.post_metrics is not None
    assert result.post_metrics.is_complete is False
    assert result.post_metrics.days_present == 1
    assert any("POST window is currently incomplete" in w for w in result.validation_warnings)


# 6. Missing GSC access
def test_missing_gsc_access():
    triage = UpdateImpactTriage(csv_source=None)
    result = triage.run()

    assert result.status == STATUS_DATA_UNAVAILABLE
    assert result.diagnostic == DIAGNOSTIC_INSUFFICIENT_DATA
    assert "Search Console performance data is unavailable" in result.diagnostic_reason


# 7. Manual-action status unknown / False (Never infer manual action from falling traffic)
def test_manual_action_status_unknown_with_falling_traffic():
    csv_data = build_synthetic_csv(
        pre_days=14, rollout_days=14, pre_clicks=100, rollout_clicks=30, pre_imp=2000, rollout_imp=800
    )
    # Traffic dropped by 70%, but manual action is UNKNOWN (None)
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data), manual_action_reported=None)
    result = triage.run()

    # Must NEVER infer manual action from traffic drop!
    assert result.diagnostic == DIAGNOSTIC_PERFORMANCE_CHANGE
    assert result.diagnostic != DIAGNOSTIC_MANUAL_ACTION


def test_manual_action_explicitly_reported():
    csv_data = build_synthetic_csv(pre_days=14, rollout_days=14)
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data), manual_action_reported=True)
    result = triage.run()

    assert result.diagnostic == DIAGNOSTIC_MANUAL_ACTION


# 8. Technical issue without ranking loss
def test_technical_issue_without_ranking_loss():
    # Traffic did not drop (pre clicks == rollout clicks)
    csv_data = build_synthetic_csv(pre_days=14, rollout_days=14, pre_clicks=100, rollout_clicks=100)
    tech_finding = Finding(
        id="technical.status.http_5xx",
        category=FindingCategory.TECHNICAL_SEO,
        severity=Severity.CRITICAL,
        confidence=1.0,
        url="https://example.com/",
        title="Server error (HTTP 500)",
        why_it_matters="Critical server failure.",
        recommended_action="Fix backend.",
        auto_fixable=False,
        risk_class=RiskClass.MANUAL_ONLY,
    )
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data), audit_findings=[tech_finding])
    result = triage.run()

    # Classified as technical issue because blocking errors exist
    assert result.diagnostic == DIAGNOSTIC_TECHNICAL_ISSUE
    assert result.technical_audit is not None
    assert result.technical_audit.has_blocking_issues is True


# 9. Ranking / performance loss without technical issue
def test_ranking_loss_without_technical_issue():
    # 40% click decline, no technical findings
    csv_data = build_synthetic_csv(
        pre_days=14, rollout_days=14, pre_clicks=100, rollout_clicks=60, pre_imp=2000, rollout_imp=1400
    )
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data), audit_findings=[])
    result = triage.run()

    assert result.diagnostic == DIAGNOSTIC_PERFORMANCE_CHANGE
    assert result.click_change_percent == -40.0
    assert result.technical_audit is None or not result.technical_audit.has_blocking_issues
    assert "Possible algorithm-update correlation" in result.diagnostic_reason


# 10. CLI command execution
def test_cli_update_triage_command(tmp_path):
    csv_content = build_synthetic_csv()
    csv_file = tmp_path / "test_gsc.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    out_file = tmp_path / "output.json"

    res = runner.invoke(app, [
        "update-triage",
        "--csv", str(csv_file),
        "--output", str(out_file),
    ])
    assert res.exit_code == 0
    assert "September 2026 Google Spam Update" in res.output
    assert out_file.exists()


def test_cli_update_triage_no_data():
    res = runner.invoke(app, ["update-triage", "--json"])
    assert res.exit_code == 0
    assert "DATA_UNAVAILABLE" in res.output
