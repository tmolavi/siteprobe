import os
from typing import Any, Dict, Optional
from siteprobe.integrations.base import BaseIntegration


class GA4Integration(BaseIntegration):
    name = "Google Analytics 4"

    def __init__(self, property_id: Optional[str] = None):
        self.property_id = property_id or os.environ.get("GA4_PROPERTY_ID")

    def is_available(self) -> bool:
        return bool(self.property_id and os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

    def get_status_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "available": self.is_available(),
            "property_configured": bool(self.property_id),
            "description": "Correlates technical findings with user bounce rate and conversion drops.",
            "setup_guide": "Set GA4_PROPERTY_ID and GOOGLE_APPLICATION_CREDENTIALS environment variables.",
        }
