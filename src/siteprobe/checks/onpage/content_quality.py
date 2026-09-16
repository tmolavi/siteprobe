import re
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class ContentQualityCheck(BaseCheck):
    id = "onpage.content"
    category = FindingCategory.CONTENT_QUALITY
    name = "Content Depth & Thin Content Check"
    description = "Analyzes word count heuristics and soft 404 indicators."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200 or not page.html:
            return findings

        soup = BeautifulSoup(page.html, "html.parser")
        # Remove scripts, styles, navigations, footers
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        words = re.findall(r"\b\w+\b", text)
        word_count = len(words)

        if word_count < 100 and page.depth > 0:
            findings.append(Finding(
                id="content.quality.thin_content",
                category=self.category,
                severity=Severity.MEDIUM,
                confidence=0.85,
                url=page.url,
                title=f"Thin content detected ({word_count} words)",
                evidence={"word_count": word_count},
                why_it_matters="Pages with little substantive content struggle to rank and risk being classified as low-quality by search algorithms.",
                recommended_action="Enrich the page with comprehensive, helpful content addressing user intent.",
                auto_fixable=False,
                risk_class=RiskClass.MANUAL_ONLY,
                required_capability="source_code",
                verification_check="onpage.content",
            ))

        # Check soft-404 patterns in text
        lower_text = text.lower()
        if any(term in lower_text for term in ["page not found", "item not found", "404 not found", "does not exist"]) and page.status_code == 200:
            findings.append(Finding(
                id="content.quality.soft_404",
                category=FindingCategory.TECHNICAL_SEO,
                severity=Severity.HIGH,
                confidence=0.90,
                url=page.url,
                title="Possible Soft-404 error page returning HTTP 200",
                evidence={"detected_phrases": [p for p in ["page not found", "404 not found"] if p in lower_text]},
                why_it_matters="Returning 200 OK for missing content tricks crawlers into indexing empty pages, wasting index budget.",
                recommended_action="Ensure non-existent pages return an actual HTTP 404 or 410 status code.",
                auto_fixable=False,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="server_ssh",
                verification_check="onpage.content",
            ))

        return findings
