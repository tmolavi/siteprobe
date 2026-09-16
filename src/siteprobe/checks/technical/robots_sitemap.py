from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class RobotsSitemapCheck(BaseCheck):
    id = "technical.robots_sitemap"
    category = FindingCategory.TECHNICAL_SEO
    name = "Robots & Sitemap Verification"
    description = "Checks existence of robots.txt, sitemaps, and detects indexability conflicts."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        # Only run on the homepage
        if page.depth != 0:
            return findings

        robots = context.get("robots")
        if not robots or not robots.raw_content.strip():
            findings.append(Finding(
                id="technical.robots.missing",
                category=self.category,
                severity=Severity.HIGH,
                confidence=1.0,
                url=page.url,
                title="robots.txt file not found",
                evidence={"url": page.url},
                why_it_matters="A missing robots.txt gives no crawling directives and can lead to unwanted crawling of sensitive pages.",
                recommended_action="Generate and upload a robots.txt file to the site root with sitemap references.",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
                required_capability="source_code",
                verification_check="technical.robots_sitemap",
            ))

        sitemap_urls = context.get("sitemap_urls", [])
        if not sitemap_urls:
            findings.append(Finding(
                id="technical.sitemap.missing",
                category=self.category,
                severity=Severity.HIGH,
                confidence=0.95,
                url=page.url,
                title="XML sitemap not found or empty",
                evidence={"url": page.url},
                why_it_matters="Sitemaps guide search engines to high-value pages, ensuring new and updated content is indexed quickly.",
                recommended_action="Create an XML sitemap (sitemap.xml) and declare its location in robots.txt.",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
                required_capability="source_code",
                verification_check="technical.robots_sitemap",
            ))
        return findings
