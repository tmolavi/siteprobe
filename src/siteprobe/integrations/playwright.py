import importlib.util
from typing import Any, Dict
from siteprobe.integrations.base import BaseIntegration


class PlaywrightIntegration(BaseIntegration):
    name = "Playwright Headless Browser"

    def is_available(self) -> bool:
        return importlib.util.find_spec("playwright") is not None

    def get_status_info(self) -> Dict[str, Any]:
        available = self.is_available()
        return {
            "name": self.name,
            "available": available,
            "description": "Enables client-side JavaScript rendering, automated screenshots, and axe-core accessibility auditing.",
            "setup_guide": "Run 'pip install siteprobe[browser] && playwright install chromium'.",
        }
