import pytest
from siteprobe.integrations.dataforseo import DataForSEOIntegration
from siteprobe.mcp.server import (
    audit_competitor_gap,
    get_backlink_intelligence,
    get_ai_search_visibility,
    generate_agent_remediation_tasks,
    _JOBS,
)
from siteprobe.core.engine import AuditResult
from siteprobe.models.crawl import CrawlSummary
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.core.score import ScoreReport


@pytest.mark.asyncio
async def test_dataforseo_free_heuristics():
    integration = DataForSEOIntegration()
    assert integration.name == "DataForSEO"
    status = integration.get_status_info()
    assert status["mode"] in ("live_api", "free_agentic_heuristics")

    gap = await integration.get_keyword_gap("example.com", "competitor.com")
    assert gap["target_domain"] == "example.com"
    assert len(gap["high_opportunity_gaps"]) > 0

    backlinks = await integration.get_backlink_profile("example.com")
    assert backlinks["domain"] == "example.com"
    assert "citation_balance" in backlinks

    ai_vis = await integration.get_ai_search_visibility("example.com", "ExampleBrand")
    assert ai_vis["brand_name"] == "ExampleBrand"
    assert "chatgpt_search" in ai_vis["engine_status"]


@pytest.mark.asyncio
async def test_mcp_agent_tools():
    gap = await audit_competitor_gap("mysite.com", "rival.com")
    assert gap["target_domain"] == "mysite.com"

    backlinks = await get_backlink_intelligence("mysite.com")
    assert backlinks["domain"] == "mysite.com"

    ai_vis = await get_ai_search_visibility("mysite.com")
    assert "ai_visibility_index" in ai_vis


def test_generate_agent_remediation_tasks():
    job_id = "test_job_123"
    dummy_finding = Finding(
        id="technical.canonical.missing",
        rule_id="RULE-CANONICAL",
        title="Missing Canonical Tag",
        description="Page lacks canonical link tag",
        category=FindingCategory.TECHNICAL_SEO,
        severity=Severity.HIGH,
        risk_class=RiskClass.SAFE_AUTOFIX,
        url="https://example.com",
        why_it_matters="Prevents duplicate content issues",
        recommended_action="Add canonical tag to head",
        remediation_guidance="Add canonical tag to head",
        auto_fixable=True,
    )
    res = AuditResult(
        site_url="https://example.com",
        crawl_summary=CrawlSummary(start_url="https://example.com", total_pages_crawled=1),
        scores=ScoreReport(overall_score=85),
        findings=[dummy_finding],
        start_time=1.0,
        end_time=2.0,
    )
    _JOBS[job_id] = {"result": res, "status": "completed"}

    tasks = generate_agent_remediation_tasks(job_id)
    assert len(tasks) == 1
    assert tasks[0]["task_id"] == "TASK-001"
    assert tasks[0]["finding_id"] == "technical.canonical.missing"
    assert "Add canonical tag" in tasks[0]["agent_instruction"]
