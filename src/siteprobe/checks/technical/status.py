from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class HttpStatusCheck(BaseCheck):
    id = "technical.status"
    category = FindingCategory.TECHNICAL_SEO
    name = "HTTP Response Status Check"
    description = "Flags pages returning 4xx client errors or 5xx server errors."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if 400 <= page.status_code < 500:
            findings.append(Finding(
                id="technical.status.http_4xx",
                category=self.category,
                severity=Severity.HIGH,
                confidence=1.0,
                url=page.url,
                title=f"Client error (HTTP {page.status_code})",
                evidence={"status_code": page.status_code},
                why_it_matters="Broken pages degrade user experience, waste search engine crawl budget, and stop link equity transmission.",
                recommended_action="Fix internal links pointing to this page or configure a 301 redirect if the page was permanently moved.",
                auto_fixable=False,
                risk_class=RiskClass.MANUAL_ONLY,
                required_capability="source_code",
                verification_check="technical.status",
            ))
        elif page.status_code >= 500:
            findings.append(Finding(
                id="technical.status.http_5xx",
                category=self.category,
                severity=Severity.CRITICAL,
                confidence=1.0,
                url=page.url,
                title=f"Server error (HTTP {page.status_code})",
                evidence={"status_code": page.status_code},
                why_it_matters="Server errors prevent search engines from crawling or indexing content and cause immediate user abandonment.",
                recommended_action="Inspect backend logs to identify server crashes, timeout issues, or uncaught exceptions.",
                auto_fixable=False,
                risk_class=RiskClass.MANUAL_ONLY,
                required_capability="server_ssh",
                verification_check="technical.status",
            ))
        return findings
