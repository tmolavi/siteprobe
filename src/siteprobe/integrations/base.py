from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseIntegration(ABC):
    """Abstract adapter for external services and browser runtimes."""

    name: str = ""

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if credentials, libraries, or binaries are present."""
        pass

    @abstractmethod
    def get_status_info(self) -> Dict[str, Any]:
        """Return human-readable configuration status and capabilities."""
        pass
