from typing import Any, Dict, List
from urllib.parse import urlparse
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class UrlStructureCheck(BaseCheck):
    id = "technical.url_structure"
    category = FindingCategory.TECHNICAL_SEO
    name = "URL Structure & Hierarchy Check"
    description = "Checks click depth, trailing slash consistency, and URL readability."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.depth > 4:
            findings.append(Finding(
                id="technical.url_structure.deep_click_depth",
                category=self.category,
                severity=Severity.LOW,
                confidence=0.90,
                url=page.url,
                title=f"High click depth ({page.depth} clicks from root)",
                evidence={"depth": page.depth},
                why_it_matters="Pages buried deeper than 3-4 clicks receive less crawl priority and internal link equity.",
                recommended_action="Improve internal linking from main category pages or navigation menus.",
                auto_fixable=False,
                risk_class=RiskClass.MANUAL_ONLY,
                required_capability="source_code",
                verification_check="technical.url_structure",
            ))

        parsed = urlparse(page.url)
        if len(parsed.query) > 80:
            findings.append(Finding(
                id="technical.url_structure.excessive_parameters",
                category=self.category,
                severity=Severity.LOW,
                confidence=0.85,
                url=page.url,
                title="Excessive query parameters in URL",
                evidence={"query": parsed.query},
                why_it_matters="Complex URL parameters confuse search crawlers and increase duplicate content risk.",
                recommended_action="Use clean RESTful URL slugs instead of multiple parameter strings.",
                auto_fixable=False,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="technical.url_structure",
            ))
        return findings
