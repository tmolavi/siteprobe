import re
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class ViewportCheck(BaseCheck):
    id = "ux.viewport"
    category = FindingCategory.UX
    name = "Mobile Viewport Configuration Check"
    description = "Checks presence and responsive parameters of meta viewport tag."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200 or not page.html:
            return findings

        soup = BeautifulSoup(page.html, "html.parser")
        viewport = soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)})

        if not viewport or not viewport.get("content"):
            findings.append(Finding(
                id="ux.viewport.missing",
                category=self.category,
                severity=Severity.HIGH,
                confidence=1.0,
                url=page.url,
                title="Missing meta viewport tag",
                evidence={},
                why_it_matters="Without a viewport tag, mobile devices render pages at desktop scale, leading to microscopic fonts and poor mobile usability.",
                recommended_action='Add <meta name="viewport" content="width=device-width, initial-scale=1.0"> inside <head>.',
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
                required_capability="source_code",
                verification_check="ux.viewport",
            ))
        else:
            content = viewport.get("content", "").lower()
            if "width=device-width" not in content:
                findings.append(Finding(
                    id="ux.viewport.improper_configuration",
                    category=self.category,
                    severity=Severity.MEDIUM,
                    confidence=0.95,
                    url=page.url,
                    title="Meta viewport missing width=device-width configuration",
                    evidence={"content": viewport.get("content")},
                    why_it_matters="Failing to set width=device-width may cause incorrect responsive rendering across varying mobile screen resolutions.",
                    recommended_action='Ensure content includes "width=device-width, initial-scale=1.0".',
                    auto_fixable=True,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    required_capability="source_code",
                    verification_check="ux.viewport",
                ))
        return findings
