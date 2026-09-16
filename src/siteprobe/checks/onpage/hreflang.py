from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage
from siteprobe.utils.url_helper import normalize_url


class HreflangCheck(BaseCheck):
    id = "onpage.hreflang"
    category = FindingCategory.ONPAGE_SEO
    name = "International Hreflang Check"
    description = "Inspects hreflang declarations and verifies reciprocal return links."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if not page.hreflangs:
            return findings

        # Check reciprocal return links
        lookup = {normalize_url(p.url): p for p in all_pages}
        for hl in page.hreflangs:
            target_url = normalize_url(hl["href"])
            target_page = lookup.get(target_url)
            if target_page:
                target_return_hrefs = [normalize_url(h["href"]) for h in target_page.hreflangs]
                current_norm = normalize_url(page.url)
                if current_norm not in target_return_hrefs:
                    findings.append(Finding(
                        id="onpage.hreflang.missing_return_link",
                        category=self.category,
                        severity=Severity.HIGH,
                        confidence=0.95,
                        url=page.url,
                        title=f"Missing reciprocal hreflang return link on {hl['href']}",
                        evidence={"source": page.url, "target": hl["href"], "declared_lang": hl["lang"]},
                        why_it_matters="Google ignores hreflang annotations if the target page does not link back with a matching hreflang tag.",
                        recommended_action=f"Add reciprocal hreflang annotation on {hl['href']} referencing {page.url}.",
                        auto_fixable=True,
                        risk_class=RiskClass.REVIEW_RECOMMENDED,
                        required_capability="source_code",
                        verification_check="onpage.hreflang",
                    ))
        return findings
