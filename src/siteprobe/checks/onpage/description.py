from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class DescriptionCheck(BaseCheck):
    id = "onpage.description"
    category = FindingCategory.ONPAGE_SEO
    name = "Meta Description Check"
    description = "Inspects meta description presence, length boundaries (70-160 chars), and uniqueness."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200:
            return findings

        if not page.meta_description:
            findings.append(Finding(
                id="onpage.description.missing",
                category=self.category,
                severity=Severity.HIGH,
                confidence=1.0,
                url=page.url,
                title="Missing meta description",
                evidence={},
                why_it_matters="Meta descriptions provide the promotional snippet in search results and strongly influence user click-through rate.",
                recommended_action="Add a compelling <meta name=\"description\" content=\"...\"> tag between 70 and 160 characters.",
                auto_fixable=True,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="onpage.description",
            ))
            return findings

        d_len = len(page.meta_description)
        if d_len > 165:
            findings.append(Finding(
                id="onpage.description.too_long",
                category=self.category,
                severity=Severity.LOW,
                confidence=0.90,
                url=page.url,
                title=f"Meta description too long ({d_len} characters)",
                evidence={"meta_description": page.meta_description, "length": d_len},
                why_it_matters="Descriptions longer than 160 characters get truncated in search result snippets.",
                recommended_action="Condense the description to 140-160 characters.",
                auto_fixable=False,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="onpage.description",
            ))
        elif d_len < 50:
            findings.append(Finding(
                id="onpage.description.too_short",
                category=self.category,
                severity=Severity.LOW,
                confidence=0.90,
                url=page.url,
                title=f"Meta description too short ({d_len} characters)",
                evidence={"meta_description": page.meta_description, "length": d_len},
                why_it_matters="Very short meta descriptions may be replaced by search engines with uncurated page snippets.",
                recommended_action="Expand the description to at least 70-120 characters.",
                auto_fixable=False,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="onpage.description",
            ))
        return findings
