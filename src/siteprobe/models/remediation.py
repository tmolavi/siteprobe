from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from siteprobe.models.finding import RiskClass


class RemediationActionType(str, Enum):
    FILE_MODIFY = "file_modify"
    FILE_CREATE = "file_create"
    SERVER_CONFIG = "server_config"
    CMS_ACTION = "cms_action"
    MANUAL_TASK = "manual_task"


class RemediationAction(BaseModel):
    id: str
    finding_id: str
    target_url: str
    file_path: Optional[str] = None
    action_type: RemediationActionType = RemediationActionType.FILE_MODIFY
    risk_class: RiskClass = RiskClass.SAFE_AUTOFIX
    title: str
    description: str
    original_snippet: Optional[str] = None
    proposed_snippet: Optional[str] = None
    applied: bool = False
    rollback_data: Optional[Dict[str, Any]] = None


class RemediationPlan(BaseModel):
    site_url: str
    created_at: str
    actions: List[RemediationAction] = Field(default_factory=list)
    safe_count: int = 0
    review_count: int = 0
    manual_count: int = 0
