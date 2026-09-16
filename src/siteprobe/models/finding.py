from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingCategory(str, Enum):
    TECHNICAL_SEO = "technical_seo"
    ONPAGE_SEO = "onpage_seo"
    SCHEMA_ORG = "schema_org"
    GEO_AEO = "geo_aeo"
    PERFORMANCE = "performance"
    ACCESSIBILITY = "accessibility"
    SECURITY = "security"
    CONTENT_QUALITY = "content_quality"
    UX = "ux"


class RiskClass(str, Enum):
    SAFE_AUTOFIX = "SAFE_AUTOFIX"
    REVIEW_RECOMMENDED = "REVIEW_RECOMMENDED"
    MANUAL_ONLY = "MANUAL_ONLY"


class Finding(BaseModel):
    id: str = Field(..., description="Stable dot-separated identifier, e.g. technical.canonical.missing")
    category: FindingCategory
    severity: Severity
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    url: str
    title: str
    evidence: Dict[str, Any] = Field(default_factory=dict)
    why_it_matters: str
    recommended_action: str
    auto_fixable: bool = False
    risk_class: RiskClass = RiskClass.MANUAL_ONLY
    required_capability: str = "source_code"
    verification_check: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode="json")
