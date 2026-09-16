from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class TitleCheck(BaseCheck):
    id = "onpage.title"
    category = FindingCategory.ONPAGE_SEO
    name = "Page Title Tag Check"
    description = "Inspects title presence, length boundaries (30-60 chars), and duplicate titles."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200:
            return findings

        if not page.title or not page.title.strip():
            findings.append(Finding(
                id="onpage.title.missing",
                category=self.category,
                severity=Severity.CRITICAL,
                confidence=1.0,
                url=page.url,
                title="Missing <title> tag",
                evidence={"title": page.title},
                why_it_matters="Title tags are among the strongest ranking factors and serve as the headline in search engine result pages.",
                recommended_action="Add a concise, keyword-rich <title> tag between 30 and 60 characters.",
                auto_fixable=True,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="onpage.title",
            ))
            return findings

        t_len = len(page.title)
        if t_len > 60:
            findings.append(Finding(
                id="onpage.title.too_long",
                category=self.category,
                severity=Severity.MEDIUM,
                confidence=0.95,
                url=page.url,
                title=f"Title tag too long ({t_len} characters)",
                evidence={"title": page.title, "length": t_len},
                why_it_matters="Titles exceeding 60 characters are truncated by search engines, hiding important call-to-actions.",
                recommended_action="Shorten title to under 60 characters while preserving primary keywords.",
                auto_fixable=False,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="onpage.title",
            ))
        elif t_len < 20:
            findings.append(Finding(
                id="onpage.title.too_short",
                category=self.category,
                severity=Severity.LOW,
                confidence=0.90,
                url=page.url,
                title=f"Title tag too short ({t_len} characters)",
                evidence={"title": page.title, "length": t_len},
                why_it_matters="Short titles miss valuable opportunities to rank for relevant search terms and clarify topic focus.",
                recommended_action="Expand the title tag to at least 30 characters with descriptive details.",
                auto_fixable=False,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="onpage.title",
            ))

        # Check duplicates
        same_title_pages = [p.url for p in all_pages if p.url != page.url and p.title.strip().lower() == page.title.strip().lower()]
        if same_title_pages:
            findings.append(Finding(
                id="onpage.title.duplicate",
                category=self.category,
                severity=Severity.HIGH,
                confidence=0.98,
                url=page.url,
                title="Duplicate page title detected across pages",
                evidence={"title": page.title, "conflicting_urls": same_title_pages[:3]},
                why_it_matters="Identical titles create keyword cannibalization and make it harder for search engines to determine which page to rank.",
                recommended_action="Ensure each indexable page has a distinct and unique title tag.",
                auto_fixable=False,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="onpage.title",
            ))

        return findings
