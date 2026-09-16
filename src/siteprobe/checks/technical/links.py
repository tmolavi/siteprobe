from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage
from siteprobe.utils.url_helper import normalize_url


class BrokenLinkCheck(BaseCheck):
    id = "technical.links"
    category = FindingCategory.TECHNICAL_SEO
    name = "Broken Internal Links Check"
    description = "Identifies hyperlinks leading to 4xx client errors within crawled pages."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        # Build lookup of dead pages
        dead_lookup = {normalize_url(p.url): p.status_code for p in all_pages if p.status_code >= 400}

        for link in page.links:
            if link.get("internal"):
                target = normalize_url(link.get("href", ""))
                if target in dead_lookup:
                    findings.append(Finding(
                        id="technical.links.broken_internal",
                        category=self.category,
                        severity=Severity.HIGH,
                        confidence=0.99,
                        url=page.url,
                        title=f"Broken internal link to {target} (HTTP {dead_lookup[target]})",
                        evidence={"source_page": page.url, "broken_link": target, "anchor_text": link.get("text", ""), "status_code": dead_lookup[target]},
                        why_it_matters="Dead links trap users, interrupt conversion funnels, and waste crawler bandwidth.",
                        recommended_action=f"Update link target '{target}' on page '{page.url}' to a valid active URL.",
                        auto_fixable=True,
                        risk_class=RiskClass.SAFE_AUTOFIX,
                        required_capability="source_code",
                        verification_check="technical.links",
                    ))
        return findings
