import tempfile
from pathlib import Path
from siteprobe.core.engine import AuditResult
from siteprobe.core.score import ScoreReport
from siteprobe.models.crawl import CrawlSummary
from siteprobe.models.finding import Finding, FindingCategory, Severity
from siteprobe.reporting.html_reporter import HtmlReporter
from siteprobe.reporting.json_reporter import JsonReporter
from siteprobe.reporting.markdown_reporter import MarkdownReporter


def test_reporters():
    summary = CrawlSummary(start_url="https://example.com", total_crawled=2, crawl_duration_seconds=1.2)
    scores = ScoreReport(overall_score=88, geo_score=75)
    findings = [
        Finding(
            id="technical.canonical.missing",
            category=FindingCategory.TECHNICAL_SEO,
            severity=Severity.HIGH,
            url="https://example.com",
            title="Missing canonical URL",
            why_it_matters="Dilutes signals",
            recommended_action="Add tag",
            auto_fixable=True,
        )
    ]
    res = AuditResult(
        site_url="https://example.com",
        crawl_summary=summary,
        scores=scores,
        findings=findings,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir)
        json_path = JsonReporter.save(res, out / "audit.json")
        md_path = MarkdownReporter.save(res, out / "audit.md")
        html_path = HtmlReporter.save(res, out / "audit.html")

        assert json_path.exists() and len(json_path.read_text(encoding="utf-8")) > 50
        assert md_path.exists() and "# SiteProbe Audit Report" in md_path.read_text(encoding="utf-8")
        assert html_path.exists() and "<!DOCTYPE html>" in html_path.read_text(encoding="utf-8")
