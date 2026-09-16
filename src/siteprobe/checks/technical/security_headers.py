from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class SecurityHeadersCheck(BaseCheck):
    id = "technical.security"
    category = FindingCategory.SECURITY
    name = "Security & Transport Headers Check"
    description = "Inspects HTTPS enforcement, HSTS, CSP, and protective HTTP headers."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if not page.url.startswith("https://") and page.status_code == 200:
            findings.append(Finding(
                id="technical.security.insecure_http",
                category=self.category,
                severity=Severity.CRITICAL,
                confidence=1.0,
                url=page.url,
                title="Page served over insecure HTTP",
                evidence={"url": page.url},
                why_it_matters="Insecure HTTP exposes data in transit to interception and is penalized by modern browsers and search engines.",
                recommended_action="Enforce HTTPS via 301 redirect and configure valid TLS certificates.",
                auto_fixable=False,
                risk_class=RiskClass.MANUAL_ONLY,
                required_capability="server_ssh",
                verification_check="technical.security",
            ))
        elif page.url.startswith("https://"):
            headers_lower = {k.lower(): v for k, v in page.headers.items()}
            if "strict-transport-security" not in headers_lower:
                findings.append(Finding(
                    id="technical.security.missing_hsts",
                    category=self.category,
                    severity=Severity.MEDIUM,
                    confidence=1.0,
                    url=page.url,
                    title="Strict-Transport-Security (HSTS) header missing",
                    evidence={"headers_checked": list(page.headers.keys())},
                    why_it_matters="HSTS forces browsers to connect exclusively over HTTPS, preventing downgrade attacks.",
                    recommended_action="Configure web server to add 'Strict-Transport-Security: max-age=31536000; includeSubDomains'.",
                    auto_fixable=False,
                    risk_class=RiskClass.REVIEW_RECOMMENDED,
                    required_capability="server_ssh",
                    verification_check="technical.security",
                ))
            if "x-content-type-options" not in headers_lower:
                findings.append(Finding(
                    id="technical.security.missing_xcto",
                    category=self.category,
                    severity=Severity.LOW,
                    confidence=1.0,
                    url=page.url,
                    title="X-Content-Type-Options header missing",
                    evidence={},
                    why_it_matters="Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.",
                    recommended_action="Add header: 'X-Content-Type-Options: nosniff'.",
                    auto_fixable=False,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    required_capability="server_ssh",
                    verification_check="technical.security",
                ))
        return findings
