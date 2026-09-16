from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class PerformanceHeuristicsCheck(BaseCheck):
    id = "performance.heuristics"
    category = FindingCategory.PERFORMANCE
    name = "Performance & Payload Heuristics Check"
    description = "Analyzes server TTFB, HTML weight, and external asset density."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200:
            return findings

        # TTFB / Response time
        if page.response_time_ms > 1200:
            findings.append(Finding(
                id="performance.ttfb.slow",
                category=self.category,
                severity=Severity.HIGH,
                confidence=0.95,
                url=page.url,
                title=f"Slow Time to First Byte ({round(page.response_time_ms)} ms)",
                evidence={"response_time_ms": round(page.response_time_ms)},
                why_it_matters="High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.",
                recommended_action="Enable server-side page caching, use a CDN, or optimize backend database queries.",
                auto_fixable=False,
                risk_class=RiskClass.MANUAL_ONLY,
                required_capability="server_ssh",
                verification_check="performance.heuristics",
            ))
        elif page.response_time_ms > 600:
            findings.append(Finding(
                id="performance.ttfb.moderate",
                category=self.category,
                severity=Severity.MEDIUM,
                confidence=0.90,
                url=page.url,
                title=f"Moderate server response latency ({round(page.response_time_ms)} ms)",
                evidence={"response_time_ms": round(page.response_time_ms)},
                why_it_matters="Google recommends server response times under 200ms for optimal Core Web Vitals.",
                recommended_action="Review caching layers and edge delivery configurations.",
                auto_fixable=False,
                risk_class=RiskClass.MANUAL_ONLY,
                required_capability="server_ssh",
                verification_check="performance.heuristics",
            ))

        # Payload weight
        if page.body_size_bytes > 1_500_000:
            kb = round(page.body_size_bytes / 1024)
            findings.append(Finding(
                id="performance.payload.oversized",
                category=self.category,
                severity=Severity.HIGH,
                confidence=0.95,
                url=page.url,
                title=f"Oversized HTML document payload ({kb} KB)",
                evidence={"body_size_bytes": page.body_size_bytes, "size_kb": kb},
                why_it_matters="Excessive document size delays DOM parsing, inflates memory consumption, and drains mobile bandwidth.",
                recommended_action="Minify HTML, purge unused inline base64 images or bloated JSON blobs.",
                auto_fixable=False,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="performance.heuristics",
            ))

        # External asset bloat
        if len(page.scripts) > 25:
            findings.append(Finding(
                id="performance.assets.excessive_scripts",
                category=self.category,
                severity=Severity.MEDIUM,
                confidence=0.90,
                url=page.url,
                title=f"High external script count ({len(page.scripts)} script tags)",
                evidence={"script_count": len(page.scripts)},
                why_it_matters="Numerous external scripts increase HTTP requests and block rendering, worsening Total Blocking Time (TBT).",
                recommended_action="Bundle scripts, defer non-critical JavaScript, or remove redundant third-party trackers.",
                auto_fixable=False,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="performance.heuristics",
            ))

        return findings
