from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class HeadingsCheck(BaseCheck):
    id = "onpage.headings"
    category = FindingCategory.ONPAGE_SEO
    name = "Heading Hierarchy Check"
    description = "Verifies H1 presence, uniqueness, and structural progression."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200:
            return findings

        if not page.h1s:
            findings.append(Finding(
                id="onpage.h1.missing",
                category=self.category,
                severity=Severity.HIGH,
                confidence=1.0,
                url=page.url,
                title="Missing <h1> heading",
                evidence={"headings_found": [h["level"] for h in page.headings]},
                why_it_matters="The H1 heading identifies the central topic of the page for search algorithms and assistive screen readers.",
                recommended_action="Add exactly one descriptive <h1> element that captures the main topic.",
                auto_fixable=True,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="onpage.headings",
            ))
        elif len(page.h1s) > 1:
            findings.append(Finding(
                id="onpage.h1.multiple",
                category=self.category,
                severity=Severity.MEDIUM,
                confidence=1.0,
                url=page.url,
                title=f"Multiple <h1> headings found ({len(page.h1s)} H1s)",
                evidence={"h1_texts": page.h1s},
                why_it_matters="Having multiple H1 headings weakens topical clarity and creates ambiguity in document outline structure.",
                recommended_action="Keep one primary <h1> and convert secondary headings into <h2> tags.",
                auto_fixable=False,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="onpage.headings",
            ))

        # Check skipped levels e.g. h1 to h3
        levels = [int(h["level"][1]) for h in page.headings if len(h["level"]) == 2 and h["level"][1].isdigit()]
        for i in range(len(levels) - 1):
            if levels[i + 1] > levels[i] + 1:
                findings.append(Finding(
                    id="onpage.headings.skipped_level",
                    category=self.category,
                    severity=Severity.LOW,
                    confidence=0.90,
                    url=page.url,
                    title=f"Heading level skipped from H{levels[i]} directly to H{levels[i+1]}",
                    evidence={"previous_level": f"H{levels[i]}", "next_level": f"H{levels[i+1]}"},
                    why_it_matters="Skipping heading levels violates semantic document outlines and degrades accessibility.",
                    recommended_action="Restructure heading tags to follow an incremental hierarchical order without skipping levels.",
                    auto_fixable=False,
                    risk_class=RiskClass.REVIEW_RECOMMENDED,
                    required_capability="source_code",
                    verification_check="onpage.headings",
                ))
                break
        return findings
