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


# 11. No clear change observed (within site-specific baseline variability)
def test_no_clear_change_within_baseline():
    # Only 1% fluctuation (100 clicks -> 99 clicks)
    csv_data = build_synthetic_csv(
        pre_days=14, rollout_days=14, pre_clicks=100, rollout_clicks=99, pre_imp=2000, rollout_imp=1980
    )
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data))
    result = triage.run()

    assert result.diagnostic in (DIAGNOSTIC_NO_CHANGE, "NO_CLEAR_CHANGE_OBSERVED")
    assert result.diagnostic_classification == result.diagnostic
    assert result.metrics.change_significance == "UNKNOWN"
    assert "falls within the site's heuristic baseline daily variability envelope" in result.metrics.change_significance_details


# 12. Baseline variability calculation
def test_baseline_variability_model():
    csv_data = build_synthetic_csv(
        pre_days=14, rollout_days=14, pre_clicks=100, rollout_clicks=50, pre_imp=2000, rollout_imp=1000
    )
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data))
    result = triage.run()

    assert result.metrics.baseline_variability is not None
    assert result.metrics.baseline_variability.daily_clicks_mean == 100.0
    assert result.metrics.change_significance == "UNKNOWN"
    assert "exceeds the site's heuristic baseline daily variability envelope" in result.metrics.change_significance_details


# ==============================================================================
# REGRESSION SUITE: Scientific Integrity & Methodology Verification (TASK 8)
# ==============================================================================

# 1. Documentation / classification consistency
def test_regression_documentation_classification_consistency():
    from pathlib import Path
    doc_path = Path("docs/research/google-spam-update-september-2026.md")
    readme_path = Path("examples/update-impact/README.md")

    assert doc_path.exists()
    assert readme_path.exists()

    doc_text = doc_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")

    # Outdated universal ±15% claims must be absent
    assert "normal variance (±15%)" not in doc_text
    assert "standard variance (±15%)" not in readme_text

    # Consistent diagnostic terms and heuristic envelope documentation
    assert "NO_CLEAR_CHANGE_OBSERVED" in doc_text
    assert "PERFORMANCE_CHANGE_OBSERVED" in doc_text
    assert "heuristic variability envelope" in doc_text.lower()


# 2. No universal ±15% threshold
def test_regression_no_universal_15_percent_threshold():
    # Scenario A: 8% drop (less than 15%), but baseline daily CV is 0.0 (envelope = 5.0%)
    # Exceeds the 5% envelope -> PERFORMANCE_CHANGE_OBSERVED (would fail under universal 15%)
    csv_data_8pct = build_synthetic_csv(
        pre_days=14, rollout_days=14, pre_clicks=100, rollout_clicks=92, pre_imp=2000, rollout_imp=1840
    )
    triage_a = UpdateImpactTriage(csv_source=io.StringIO(csv_data_8pct))
    res_a = triage_a.run()
    assert res_a.click_change_percent == -8.0
    assert res_a.diagnostic == DIAGNOSTIC_PERFORMANCE_CHANGE

    # Scenario B: 12% drop, but high daily variance makes CV = 0.15 (envelope = 30.0%)
    # Falls within 30% envelope -> NO_CLEAR_CHANGE_OBSERVED
    lines = ["date,clicks,impressions"]
    # Varying pre-window clicks to create high variance
    pre_vals = [50, 150, 60, 140, 70, 130, 80, 120, 50, 150, 60, 140, 70, 130]  # mean 100
    for idx, c in enumerate(pre_vals):
        day = 10 + idx
        lines.append(f"2026-09-{day:02d},{c},{c * 20}")
    # Rollout clicks = constant 88 (12% drop from mean 100)
    for idx in range(14):
        if idx < 7:
            day = 24 + idx
            lines.append(f"2026-09-{day:02d},88,1760")
        else:
            day = idx - 6
            lines.append(f"2026-10-{day:02d},88,1760")
    triage_b = UpdateImpactTriage(csv_source=io.StringIO("\n".join(lines)))
    res_b = triage_b.run()
    assert res_b.click_change_percent == -12.0
    assert res_b.diagnostic in (DIAGNOSTIC_NO_CHANGE, "NO_CLEAR_CHANGE_OBSERVED")


# 3. No false statistical significance
def test_regression_no_false_statistical_significance():
    # Massive 70% decline
    csv_data = build_synthetic_csv(
        pre_days=14, rollout_days=14, pre_clicks=100, rollout_clicks=30, pre_imp=2000, rollout_imp=600
    )
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data))
    result = triage.run()

    # Statistical significance must remain UNKNOWN (heuristic envelope is not a validated significance test)
    assert result.metrics.change_significance == "UNKNOWN"
    assert "informal heuristic" in result.metrics.change_significance_details.lower()
    assert "statistical significance is unknown" in result.metrics.change_significance_details.lower()


# 4. Fractional click count rejection
def test_regression_fractional_click_count_rejection():
    from siteprobe.updates.validator import parse_non_negative_int

    # Direct unit test
    with pytest.raises(ValueError, match="must be an integer, got fractional value"):
        parse_non_negative_int("12.5", "clicks", 2)

    with pytest.raises(ValueError, match="must be an integer, got fractional value"):
        parse_non_negative_int("0.2", "clicks", 5)

    # CSV integration test
    csv_data = "date,clicks,impressions\n2026-09-10,12.5,200\n"
    with pytest.raises(ValueError, match="must be an integer, got fractional value '12.5'"):
        validate_and_parse_gsc_csv(csv_data)


# 5. Fractional impression count rejection
def test_regression_fractional_impression_count_rejection():
    from siteprobe.updates.validator import parse_non_negative_int

    # Direct unit test
    with pytest.raises(ValueError, match="must be an integer, got fractional value"):
        parse_non_negative_int("100.8", "impressions", 3)

    # CSV integration test
    csv_data = "date,clicks,impressions\n2026-09-10,12,200.7\n"
    with pytest.raises(ValueError, match="must be an integer, got fractional value '200.7'"):
        validate_and_parse_gsc_csv(csv_data)


# 6. --json and --output flags work together
def test_regression_json_and_output_flags_together(tmp_path):
    import json
    csv_content = build_synthetic_csv()
    csv_file = tmp_path / "input.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    out_file = tmp_path / "combined_report.json"

    res = runner.invoke(app, [
        "update-triage",
        "--csv", str(csv_file),
        "--json",
        "--output", str(out_file),
    ])

    assert res.exit_code == 0
    # Stdout must be valid JSON parseable directly
    stdout_json = json.loads(res.output)
    assert stdout_json["event"]["name"] == "September 2026 Google Spam Update"

    # Requested output file must exist and match stdout
    assert out_file.exists()
    file_json = json.loads(out_file.read_text(encoding="utf-8"))
    assert file_json["event"]["name"] == "September 2026 Google Spam Update"
    assert file_json["diagnostic"] == stdout_json["diagnostic"]


# 7. Missing GSC API access clarity
def test_regression_missing_gsc_api_access():
    triage = UpdateImpactTriage(csv_source=None)
    result = triage.run()

    assert result.status == STATUS_DATA_UNAVAILABLE
    assert result.diagnostic == DIAGNOSTIC_INSUFFICIENT_DATA
    # Diagnostic reason must not claim automated API retrieval
    assert "Search Console performance data is unavailable" in result.diagnostic_reason
    assert "CSV export was provided" in result.diagnostic_reason


# 8. Incomplete POST window handling
def test_regression_incomplete_post_window():
    csv_data = build_synthetic_csv(pre_days=14, rollout_days=14, include_completion=True, include_post=True)
    triage = UpdateImpactTriage(csv_source=io.StringIO(csv_data))
    result = triage.run()

    assert result.post_metrics is not None
    assert result.post_metrics.is_complete is False
    assert result.post_metrics.status == "INCOMPLETE"
    assert result.post_metrics.days_present == 1
    assert result.post_metrics.days_expected == 14
    assert any("Post-update recovery cannot be reliably evaluated" in w for w in result.validation_warnings)


# 9. Synthetic data disclosure
def test_regression_synthetic_data_disclosure(tmp_path):
    csv_file = tmp_path / "synthetic_test.csv"
    csv_content = (
        "# SYNTHETIC DATASET FOR BENCHMARK TESTING\n"
        + build_synthetic_csv()
    )
    csv_file.write_text(csv_content, encoding="utf-8")

    triage = UpdateImpactTriage(csv_source=csv_file)
    result = triage.run()

    assert result.data_quality.data_type == "SYNTHETIC"
    assert any("SYNTHETIC benchmark data" in w for w in result.data_quality.validation_warnings)


# 10. Existing CLI backward compatibility
def test_regression_cli_backward_compatibility():
    # Help flag
    res_help = runner.invoke(app, ["update-triage", "--help"])
    assert res_help.exit_code == 0
    assert "--csv" in res_help.output
    assert "--audit-file" in res_help.output
    assert "--manual-action" in res_help.output
    assert "--output" in res_help.output
    assert "--json" in res_help.output

