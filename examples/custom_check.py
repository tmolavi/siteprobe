"""Example: Creating a custom check in SiteProbe."""
from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class CustomCopyrightCheck(BaseCheck):
    id = "content.copyright.outdated"
    category = FindingCategory.CONTENT_QUALITY
    name = "Outdated Copyright Year Check"
    description = "Checks whether footer copyright mentions an outdated year."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if "© 2018" in page.html or "© 2019" in page.html:
            findings.append(Finding(
                id=self.id,
                category=self.category,
                severity=Severity.LOW,
                url=page.url,
                title="Outdated copyright year detected in footer",
                why_it_matters="Stale copyright dates give users the impression that the business or site is inactive.",
                recommended_action="Update copyright year dynamically or advance to the current year.",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
            ))
        return findings
