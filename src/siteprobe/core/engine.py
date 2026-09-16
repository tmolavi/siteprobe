import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
import httpx
from pydantic import BaseModel, Field

from siteprobe.checks.registry import default_registry
from siteprobe.core.config import load_config
from siteprobe.core.score import ScoreReport, compute_scores
from siteprobe.crawler.engine import AsyncCrawler
from siteprobe.crawler.storage import CrawlStorage
from siteprobe.i18n.translator import get_translator
from siteprobe.models.config import SiteProbeConfig
from siteprobe.models.crawl import CrawlPage, CrawlSummary
from siteprobe.models.finding import Finding
from siteprobe.models.remediation import RemediationPlan


class MissingCapability(BaseModel):
    name: str
    description: str
    why_it_improves_audit: str
    how_to_enable: str


class AuditResult(BaseModel):
    site_url: str
    language: str = "en"
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    crawl_summary: CrawlSummary
    scores: ScoreReport
    findings: List[Finding] = Field(default_factory=list)
    remediation_plan: Optional[RemediationPlan] = None
    missing_capabilities: List[MissingCapability] = Field(default_factory=list)
    pages: List[Dict[str, Any]] = Field(default_factory=list)


class AuditEngine:
    """Core orchestrator connecting crawler, checks registry, scoring, and remediation planner."""

    def __init__(self, config: Optional[SiteProbeConfig] = None, language: str = "en"):
        self.config = config or load_config()
        self.language = language or self.config.site.language

    async def run_audit(self, target_url: Optional[str] = None) -> AuditResult:
        url = target_url or self.config.site.url
        storage = CrawlStorage()
        crawler = AsyncCrawler(url, config=self.config.crawl, storage=storage)

        # Execute crawl
        crawl_summary = await crawler.crawl()
        pages = await storage.get_all_pages()

        # Check for /llms.txt at root domain
        has_llms_txt = False
        parsed = urlparse(url)
        llms_url = f"{parsed.scheme}://{parsed.netloc}/llms.txt"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(llms_url)
                if r.status_code == 200 and len(r.text.strip()) > 20:
                    has_llms_txt = True
        except Exception:
            has_llms_txt = False

        # Run checks registry
        context = {
            "start_url": url,
            "robots": crawler.robots,
            "sitemap_urls": crawler.sitemap_urls,
            "has_llms_txt": has_llms_txt,
        }
        raw_findings = default_registry.run_all(pages, context)

        # Translate findings if required
        translator = get_translator(self.language)
        translated_findings = [translator.translate_finding(f) for f in raw_findings]

        # Compute deterministic scores
        scores = compute_scores(translated_findings)

        # Identify missing capabilities
        missing = self._detect_missing_capabilities()

        # Minimal page representations for report
        page_summaries = [
            {
                "url": p.url,
                "status_code": p.status_code,
                "title": p.title,
                "depth": p.depth,
                "response_time_ms": round(p.response_time_ms, 1),
                "is_indexable": p.is_indexable,
            }
            for p in pages
        ]

        await storage.close()

        return AuditResult(
            site_url=url,
            language=self.language,
            crawl_summary=crawl_summary,
            scores=scores,
            findings=translated_findings,
            missing_capabilities=missing,
            pages=page_summaries,
        )

    def _detect_missing_capabilities(self) -> List[MissingCapability]:
        caps = []
        if not self.config.integrations.search_console:
            caps.append(MissingCapability(
                name="Google Search Console",
                description="Organic search performance metrics (clicks, impressions, average positions, keyword queries).",
                why_it_improves_audit="Identifies high-impression queries with weak CTR, tracks ranking drops, and validates Google indexing coverage.",
                how_to_enable="Set GOOGLE_APPLICATION_CREDENTIALS or ask user to authenticate via browser session.",
            ))
        if not self.config.integrations.ga4:
            caps.append(MissingCapability(
                name="Google Analytics 4 (GA4)",
                description="Real-world user behavioral and organic landing page conversion metrics.",
                why_it_improves_audit="Connects technical crawl defects directly to user drop-offs and lost conversions.",
                how_to_enable="Configure GA4_PROPERTY_ID and OAuth service account credentials.",
            ))
        if not self.config.integrations.lighthouse:
            caps.append(MissingCapability(
                name="Google Lighthouse / Chrome",
                description="Lab-tested Core Web Vitals (LCP, CLS, INP/TBT) and synthetic visual rendering metrics.",
                why_it_improves_audit="Provides granular rendering waterfall insights beyond server TTFB.",
                how_to_enable="Install Node.js and Chrome, or pass --lighthouse CLI flag.",
            ))
        if not self.config.integrations.playwright:
            caps.append(MissingCapability(
                name="Playwright Browser Session",
                description="Headless browser automation for client-side rendered SPAs and visual viewport screenshots.",
                why_it_improves_audit="Enables auditing JavaScript-only single page apps (React/Vue/Angular) and visual overflow verification.",
                how_to_enable="Run 'pip install siteprobe[browser] && playwright install chromium'.",
            ))
        return caps
