import difflib
from pathlib import Path
from typing import Dict, List, Optional
from siteprobe.models.finding import RiskClass
from siteprobe.models.remediation import RemediationAction, RemediationPlan
from siteprobe.remediation.handlers import SafeAutofixHandler


class RemediationReport(RemediationPlan):
    applied_count: int = 0
    diffs: Dict[str, str] = {}


class RemediationExecutor:
    """Executes safe auto-fixes on local repository or source folder with snapshot & rollback."""

    def __init__(self, repo_dir: str):
        self.repo_path = Path(repo_dir).resolve()
        self.snapshots: Dict[str, str] = {}
        self.diffs: Dict[str, str] = {}

    def apply_safe_fixes(self, plan: RemediationPlan) -> RemediationReport:
        applied_count = 0

        for action in plan.actions:
            if action.risk_class != RiskClass.SAFE_AUTOFIX:
                continue

            # 1. File creation (robots.txt, llms.txt)
            if action.file_path and action.proposed_snippet:
                target_file = self.repo_path / action.file_path
                if not target_file.exists():
                    target_file.write_text(action.proposed_snippet, encoding="utf-8")
                    action.applied = True
                    applied_count += 1
                    self.diffs[str(action.file_path)] = f"+ Created {action.file_path}\n" + action.proposed_snippet
                    continue

            # 2. File modification on HTML files
            html_candidates = list(self.repo_path.glob("*.html")) + list(self.repo_path.glob("**/*.html"))
            for html_file in html_candidates:
                # Avoid venv or hidden folders
                if any(part.startswith(".") or part in ("venv", ".venv", "node_modules") for part in html_file.parts):
                    continue

                try:
                    orig_content = html_file.read_text(encoding="utf-8")
                except Exception:
                    continue

                # Snapshot for potential rollback
                if str(html_file) not in self.snapshots:
                    self.snapshots[str(html_file)] = orig_content

                new_content, changed = SafeAutofixHandler.fix_html_content(orig_content, action.title, action.target_url)
                if changed:
                    html_file.write_text(new_content, encoding="utf-8")
                    action.applied = True
                    applied_count += 1

                    # Compute diff
                    diff = "\n".join(difflib.unified_diff(
                        orig_content.splitlines(),
                        new_content.splitlines(),
                        fromfile=f"a/{html_file.relative_to(self.repo_path)}",
                        tofile=f"b/{html_file.relative_to(self.repo_path)}",
                        lineterm="",
                    ))
                    self.diffs[str(html_file.relative_to(self.repo_path))] = diff
                    break

        return RemediationReport(
            site_url=plan.site_url,
            created_at=plan.created_at,
            actions=plan.actions,
            safe_count=plan.safe_count,
            review_count=plan.review_count,
            manual_count=plan.manual_count,
            applied_count=applied_count,
            diffs=self.diffs,
        )

    def rollback(self) -> None:
        """Rollback all modified files from in-memory snapshot."""
        for file_str, orig_content in self.snapshots.items():
            Path(file_str).write_text(orig_content, encoding="utf-8")
        self.snapshots.clear()
        self.diffs.clear()
