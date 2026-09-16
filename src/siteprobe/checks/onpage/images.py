from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class ImagesCheck(BaseCheck):
    id = "onpage.images"
    category = FindingCategory.ONPAGE_SEO
    name = "Image Alt Text & Optimization Check"
    description = "Checks for missing alt attributes and accessibility image metadata."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200:
            return findings

        missing_alt = [img.src for img in page.images if img.alt is None]
        if missing_alt:
            findings.append(Finding(
                id="onpage.images.missing_alt",
                category=self.category,
                severity=Severity.HIGH,
                confidence=1.0,
                url=page.url,
                title=f"{len(missing_alt)} image(s) missing alt attribute",
                evidence={"affected_images": missing_alt[:5], "total_missing": len(missing_alt)},
                why_it_matters="Alt text is required by WCAG accessibility guidelines for screen readers and allows search engines to index image context.",
                recommended_action="Add descriptive alt text to informative images, or alt=\"\" to purely decorative images.",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
                required_capability="source_code",
                verification_check="onpage.images",
            ))
        return findings
