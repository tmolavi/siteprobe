from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    FIXED = "FIXED"
    IMPROVED = "IMPROVED"
    UNCHANGED = "UNCHANGED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    NEEDS_ACCESS = "NEEDS_ACCESS"
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"


class VerificationResult(BaseModel):
    finding_id: str
    url: str
    status: VerificationStatus
    message: str
    before_evidence: Dict[str, Any] = Field(default_factory=dict)
    after_evidence: Dict[str, Any] = Field(default_factory=dict)
