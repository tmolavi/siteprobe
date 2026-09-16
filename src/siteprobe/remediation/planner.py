import datetime
from typing import List, Optional
from siteprobe.models.finding import Finding, RiskClass
from siteprobe.models.remediation import RemediationAction, RemediationActionType, RemediationPlan


class RemediationPlanner:
    """Generates a structured, risk-classified remediation plan from audit findings."""

    @classmethod
    def create_plan(cls, site_url: str, findings: List[Finding]) -> RemediationPlan:
        actions: List[RemediationAction] = []
        action_idx = 1

        for f in findings:
            if not f.auto_fixable and f.risk_class == RiskClass.MANUAL_ONLY:
                # Still include manual guidance in the plan
                actions.append(RemediationAction(
                    id=f"act-{action_idx:03d}",
                    finding_id=f.id,
                    target_url=f.url,
                    action_type=RemediationActionType.MANUAL_TASK,
                    risk_class=RiskClass.MANUAL_ONLY,
                    title=f.title,
                    description=f.recommended_action,
                ))
                action_idx += 1
                continue

            # Map specific auto-fixable finding rules
            if f.id == "technical.robots.missing":
                actions.append(RemediationAction(
                    id=f"act-{action_idx:03d}",
                    finding_id=f.id,
                    target_url=f.url,
                    file_path="robots.txt",
                    action_type=RemediationActionType.FILE_CREATE,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    title="Generate standard robots.txt with AI search bot access",
                    description="Create a compliant robots.txt file allowing search engines and AI retrieval bots while referencing sitemap.",
                    proposed_snippet=(
                        "User-agent: *\nAllow: /\n\n"
                        "User-agent: OAI-SearchBot\nAllow: /\n\n"
                        "User-agent: PerplexityBot\nAllow: /\n\n"
                        "User-agent: ClaudeBot\nAllow: /\n\n"
                        f"Sitemap: {site_url.rstrip('/')}/sitemap.xml\n"
                    ),
                ))
                action_idx += 1

            elif f.id == "geo.llms_txt.missing":
                actions.append(RemediationAction(
                    id=f"act-{action_idx:03d}",
                    finding_id=f.id,
                    target_url=f.url,
                    file_path="llms.txt",
                    action_type=RemediationActionType.FILE_CREATE,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    title="Generate standardized /llms.txt markdown index",
                    description="Create an /llms.txt file to help AI agents navigate high-value site documentation.",
                    proposed_snippet=(
                        f"# {site_url}\n\n"
                        "> Autonomous summary of site capabilities and structured resources.\n\n"
                        "## Core Pages\n"
                        f"- [{site_url}]({site_url}): Primary home page.\n"
                    ),
                ))
                action_idx += 1

            elif f.id == "technical.canonical.missing":
                actions.append(RemediationAction(
                    id=f"act-{action_idx:03d}",
                    finding_id=f.id,
                    target_url=f.url,
                    action_type=RemediationActionType.FILE_MODIFY,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    title=f"Insert self-referential canonical tag for {f.url}",
                    description=f"Add <link rel=\"canonical\" href=\"{f.url}\"> into HTML <head> section.",
                    proposed_snippet=f'<link rel="canonical" href="{f.url}">',
                ))
                action_idx += 1

            elif f.id == "accessibility.html.missing_lang":
                actions.append(RemediationAction(
                    id=f"act-{action_idx:03d}",
                    finding_id=f.id,
                    target_url=f.url,
                    action_type=RemediationActionType.FILE_MODIFY,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    title="Add lang attribute to <html> tag",
                    description="Set <html lang=\"en\"> to ensure screen readers use correct pronunciation rules.",
                    proposed_snippet='<html lang="en">',
                ))
                action_idx += 1

            elif f.id == "ux.viewport.missing":
                actions.append(RemediationAction(
                    id=f"act-{action_idx:03d}",
                    finding_id=f.id,
                    target_url=f.url,
                    action_type=RemediationActionType.FILE_MODIFY,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    title="Add meta viewport tag for responsive rendering",
                    description="Inject <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"> into <head>.",
                    proposed_snippet='<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                ))
                action_idx += 1

            elif f.id == "onpage.images.missing_alt":
                actions.append(RemediationAction(
                    id=f"act-{action_idx:03d}",
                    finding_id=f.id,
                    target_url=f.url,
                    action_type=RemediationActionType.FILE_MODIFY,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    title="Add alt attribute to image tags",
                    description="Ensure all img tags have an explicit alt attribute for accessibility.",
                    proposed_snippet='alt=""',
                ))
                action_idx += 1

        safe = sum(1 for a in actions if a.risk_class == RiskClass.SAFE_AUTOFIX)
        review = sum(1 for a in actions if a.risk_class == RiskClass.REVIEW_RECOMMENDED)
        manual = sum(1 for a in actions if a.risk_class == RiskClass.MANUAL_ONLY)

        return RemediationPlan(
            site_url=site_url,
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            actions=actions,
            safe_count=safe,
            review_count=review,
            manual_count=manual,
        )
