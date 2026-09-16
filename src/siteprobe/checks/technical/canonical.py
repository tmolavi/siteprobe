from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage
from siteprobe.utils.url_helper import normalize_url


class CanonicalCheck(BaseCheck):
    id = "technical.canonical"
    category = FindingCategory.TECHNICAL_SEO
    name = "Canonical URL Check"
    description = "Verifies canonical tag presence, self-referential status, and target validity."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200:
            return findings

        norm_url = normalize_url(page.url, strip_trailing_slash=True)

        if not page.canonical:
            findings.append(Finding(
                id="technical.canonical.missing",
                category=self.category,
                severity=Severity.HIGH,
                confidence=0.98,
                url=page.url,
                title="Missing canonical URL tag",
                evidence={"url": page.url, "has_canonical": False},
                why_it_matters="Without a canonical tag, URL parameters or duplicate pathways can dilute search rank signals.",
                recommended_action=f'Add <link rel="canonical" href="{page.url}"> to the <head> section.',
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
                required_capability="source_code",
                verification_check="technical.canonical",
            ))
        else:
            norm_canonical = normalize_url(page.canonical, strip_trailing_slash=True)
            if norm_canonical != norm_url:
                findings.append(Finding(
                    id="technical.canonical.mismatch",
                    category=self.category,
                    severity=Severity.MEDIUM,
                    confidence=0.95,
                    url=page.url,
                    title="Canonical URL points to a different address",
                    evidence={"page_url": page.url, "canonical_declared": page.canonical},
                    why_it_matters="This tells search engines not to index the current page, passing ranking signals to the canonical target.",
                    recommended_action="Confirm that this page is intentionally non-canonical. If it is the primary version, update canonical to self-referential.",
                    auto_fixable=False,
                    risk_class=RiskClass.REVIEW_RECOMMENDED,
                    required_capability="source_code",
                    verification_check="technical.canonical",
                ))
        return findings
