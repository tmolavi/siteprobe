from siteprobe.checks.base import BaseCheck
from siteprobe.checks.registry import CheckRegistry, default_registry
from siteprobe.checks.technical import (
    HttpStatusCheck,
    CanonicalCheck,
    RedirectCheck,
    BrokenLinkCheck,
    RobotsSitemapCheck,
    SecurityHeadersCheck,
    UrlStructureCheck,
)
from siteprobe.checks.onpage import (
    TitleCheck,
    DescriptionCheck,
    HeadingsCheck,
    ImagesCheck,
    HreflangCheck,
    ContentQualityCheck,
)
from siteprobe.checks.schema import StructuredDataCheck
from siteprobe.checks.geo import GeoAeoCheck
from siteprobe.checks.performance import PerformanceHeuristicsCheck
from siteprobe.checks.accessibility import WcagDeterministicCheck
from siteprobe.checks.ux import ViewportCheck


def register_default_checks(registry: CheckRegistry) -> None:
    # Technical
    registry.register(HttpStatusCheck())
    registry.register(CanonicalCheck())
    registry.register(RedirectCheck())
    registry.register(BrokenLinkCheck())
    registry.register(RobotsSitemapCheck())
    registry.register(SecurityHeadersCheck())
    registry.register(UrlStructureCheck())

    # On-Page
    registry.register(TitleCheck())
    registry.register(DescriptionCheck())
    registry.register(HeadingsCheck())
    registry.register(ImagesCheck())
    registry.register(HreflangCheck())
    registry.register(ContentQualityCheck())

    # Schema
    registry.register(StructuredDataCheck())

    # GEO / AEO
    registry.register(GeoAeoCheck())

    # Performance
    registry.register(PerformanceHeuristicsCheck())

    # Accessibility
    registry.register(WcagDeterministicCheck())

    # UX
    registry.register(ViewportCheck())


# Initialize default checks
register_default_checks(default_registry)

__all__ = [
    "BaseCheck",
    "CheckRegistry",
    "default_registry",
    "register_default_checks",
]
