import shutil
from typing import Any, Dict
from siteprobe.integrations.base import BaseIntegration


class LighthouseIntegration(BaseIntegration):
    name = "Lighthouse CLI"

    def is_available(self) -> bool:
        return bool(shutil.which("lighthouse") or shutil.which("npx"))

    def get_status_info(self) -> Dict[str, Any]:
        has_cli = bool(shutil.which("lighthouse"))
        has_npx = bool(shutil.which("npx"))
        return {
            "name": self.name,
            "available": has_cli or has_npx,
            "lighthouse_binary": has_cli,
            "npx_binary": has_npx,
            "description": "Calculates Core Web Vitals (LCP, CLS, TBT) and lab performance metrics.",
            "setup_guide": "Install Node.js and run 'npm install -g lighthouse' or use npx.",
        }
