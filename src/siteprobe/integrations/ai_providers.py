import os
from typing import Any, Dict, Optional
from siteprobe.integrations.base import BaseIntegration


class AIProviderIntegration(BaseIntegration):
    name = "Optional AI Provider"

    def is_available(self) -> bool:
        return any(k in os.environ for k in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY"))

    def get_status_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "available": self.is_available(),
            "configured_keys": [
                k for k in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY") if k in os.environ
            ],
            "description": "Optional semantic reasoning for deeper content clarity and semantic entity analysis.",
            "setup_guide": "Export OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY.",
        }
