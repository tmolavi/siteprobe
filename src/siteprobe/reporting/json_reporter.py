import json
from pathlib import Path
from typing import Union
from siteprobe.core.engine import AuditResult


class JsonReporter:
    """Generates machine-readable JSON reports."""

    @staticmethod
    def render(audit_result: AuditResult, indent: int = 2) -> str:
        return audit_result.model_dump_json(indent=indent)

    @classmethod
    def save(cls, audit_result: AuditResult, output_path: Union[str, Path]) -> Path:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        content = cls.render(audit_result)
        p.write_text(content, encoding="utf-8")
        return p
