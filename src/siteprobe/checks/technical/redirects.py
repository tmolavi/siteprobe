from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class RedirectCheck(BaseCheck):
    id = "technical.redirects"
    category = FindingCategory.TECHNICAL_SEO
    name = "Redirect Chain & Loop Check"
    description = "Detects multiple redirect hops or redirect loops."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        chain = page.redirect_chain
        if len(chain) > 2:
            hops = [f"{h.status_code}: {h.url}" for h in chain]
            findings.append(Finding(
                id="technical.redirect.chain",
                category=self.category,
                severity=Severity.MEDIUM,
                confidence=1.0,
                url=page.url,
                title=f"Redirect chain detected ({len(chain) - 1} hops)",
                evidence={"hops": hops},
                why_it_matters="Chained redirects increase page load latency and dilute link authority.",
                recommended_action=f"Update internal references to link directly to final destination: {chain[-1].url}",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
                required_capability="source_code",
                verification_check="technical.redirects",
            ))
        return findings
