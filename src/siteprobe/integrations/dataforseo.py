import os
from typing import Any, Dict, Optional
from siteprobe.integrations.base import BaseIntegration


class DataForSEOIntegration(BaseIntegration):
    name = "DataForSEO"

    def __init__(self, login: Optional[str] = None, password: Optional[str] = None):
        self.login = login or os.environ.get("DATAFORSEO_LOGIN")
        self.password = password or os.environ.get("DATAFORSEO_PASSWORD")

    def is_available(self) -> bool:
        return bool(self.login and self.password)

    def get_status_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "available": self.is_available(),
            "description": "Enables off-page SERP rankings, backlink analysis, and search volume estimation.",
            "setup_guide": "Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD environment variables.",
        }
