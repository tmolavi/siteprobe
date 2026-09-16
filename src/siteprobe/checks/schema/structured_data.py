from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class StructuredDataCheck(BaseCheck):
    id = "schema.structured_data"
    category = FindingCategory.SCHEMA_ORG
    name = "Structured Data & Schema.org Validator"
    description = "Inspects JSON-LD and Microdata for syntax errors, required entities, and sameAs links."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200:
            return findings

        # 1. Check for syntax parse errors in JSON-LD
        for raw in page.schema_raw:
            if raw.get("_parse_error"):
                findings.append(Finding(
                    id="schema.jsonld.syntax_error",
                    category=self.category,
                    severity=Severity.HIGH,
                    confidence=1.0,
                    url=page.url,
                    title="Invalid JSON-LD syntax error in script tag",
                    evidence={"snippet": raw.get("raw", "")},
                    why_it_matters="Malformed JSON-LD cannot be parsed by search engines or AI crawlers, invalidating rich snippets.",
                    recommended_action="Validate and fix JSON syntax errors (e.g. unescaped quotes or trailing commas).",
                    auto_fixable=True,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    required_capability="source_code",
                    verification_check="schema.structured_data",
                ))

        # 2. Check homepage entity representation (Organization or WebSite)
        if page.depth == 0:
            types_lower = [t.lower() for t in page.schema_types]
            if not any(t in types_lower for t in ["organization", "website", "corporation", "localbusiness"]):
                findings.append(Finding(
                    id="schema.entity.missing_organization",
                    category=self.category,
                    severity=Severity.MEDIUM,
                    confidence=0.95,
                    url=page.url,
                    title="Missing Organization or WebSite schema on homepage",
                    evidence={"schema_types_found": page.schema_types},
                    why_it_matters="Organization schema establishes authoritative brand identity, official logos, and social proof in Google Knowledge Graph.",
                    recommended_action="Inject an 'Organization' schema.org JSON-LD snippet with name, url, logo, and sameAs links.",
                    auto_fixable=True,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    required_capability="source_code",
                    verification_check="schema.structured_data",
                ))

        # 3. Check BreadcrumbList on deep pages
        if page.depth >= 2:
            types_lower = [t.lower() for t in page.schema_types]
            if "breadcrumblist" not in types_lower:
                findings.append(Finding(
                    id="schema.breadcrumbs.missing",
                    category=self.category,
                    severity=Severity.LOW,
                    confidence=0.85,
                    url=page.url,
                    title="Missing BreadcrumbList schema on subpage",
                    evidence={"depth": page.depth},
                    why_it_matters="Breadcrumb schema enables enhanced breadcrumb navigation trails in Google search results.",
                    recommended_action="Add BreadcrumbList JSON-LD representing the hierarchy from home to current page.",
                    auto_fixable=True,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    required_capability="source_code",
                    verification_check="schema.structured_data",
                ))

        return findings
