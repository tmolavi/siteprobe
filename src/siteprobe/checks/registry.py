from typing import Any, Dict, List
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding
from siteprobe.models.crawl import CrawlPage


class CheckRegistry:
    """Registry maintaining active audit checks across all categories."""

    def __init__(self):
        self._checks: List[BaseCheck] = []

    def register(self, check: BaseCheck) -> None:
        self._checks.append(check)

    def get_all_checks(self) -> List[BaseCheck]:
        return list(self._checks)

    def run_all(self, pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings: List[Finding] = []
        for page in pages:
            for check in self._checks:
                try:
                    results = check.run(page, pages, context)
                    if results:
                        findings.extend(results)
                except Exception as e:
                    # Log or record check failure without crashing the whole audit
                    continue
        return findings


default_registry = CheckRegistry()
