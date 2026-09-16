import pytest
from siteprobe.core.engine import AuditEngine
from siteprobe.models.config import SiteProbeConfig, SiteConfig, CrawlConfig


@pytest.mark.asyncio
async def test_full_audit_on_mock_server(mock_server):
    cfg = SiteProbeConfig(
        site=SiteConfig(url=mock_server, language="en"),
        crawl=CrawlConfig(max_pages=10, timeout_seconds=5.0),
    )
    engine = AuditEngine(config=cfg, language="en")
    result = await engine.run_audit(mock_server)

    assert result.site_url == mock_server
    assert result.crawl_summary.total_crawled >= 2
    assert len(result.findings) > 0

    # Ensure deliberate defects in mock_server/index.html were detected!
    finding_ids = [f.id for f in result.findings]
    assert "technical.robots.missing" in finding_ids
    assert "geo.llms_txt.missing" in finding_ids
    assert "technical.canonical.missing" in finding_ids
    assert "onpage.images.missing_alt" in finding_ids
    assert "accessibility.html.missing_lang" in finding_ids
    assert "accessibility.form.unlabeled_input" in finding_ids
    assert "ux.viewport.missing" in finding_ids
    assert "technical.redirect.chain" in finding_ids
    assert "technical.links.broken_internal" in finding_ids
