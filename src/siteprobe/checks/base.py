from abc import ABC, abstractmethod
from typing import Any, Dict, List
from siteprobe.models.finding import Finding, FindingCategory
from siteprobe.models.crawl import CrawlPage


class BaseCheck(ABC):
    """Abstract base class for all SiteProbe audit checks."""

    id: str = ""
    category: FindingCategory = FindingCategory.TECHNICAL_SEO
    name: str = ""
    description: str = ""

    @abstractmethod
    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        """Execute check against a specific crawled page and overall site context."""
        pass
