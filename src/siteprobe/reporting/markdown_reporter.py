from pathlib import Path
from typing import Union
from siteprobe.core.engine import AuditResult
from siteprobe.models.finding import Severity


class MarkdownReporter:
    """Generates structured Markdown reports for terminal rendering, PR comments, and docs."""

    @staticmethod
    def render(res: AuditResult) -> str:
        lines = [
            f"# SiteProbe Audit Report: {res.site_url}",
            f"> **Audit Date**: {res.timestamp} | **Language**: `{res.language}`",
            "",
            "## 📊 Executive Summary",
            "",
            f"- **Overall Quality Score**: **{res.scores.overall_score} / 100**",
            f"- **GEO / AI Search Readiness**: **{res.scores.geo_score} / 100**",
            f"- **Total Pages Crawled**: {res.crawl_summary.total_crawled}",
            f"- **Crawl Duration**: {res.crawl_summary.crawl_duration_seconds}s",
            f"- **Broken Links**: {res.crawl_summary.broken_links_count}",
            "",
            "### Category Breakdown",
            "| Category | Score | Critical | High | Medium | Low |",
            "| :--- | :---: | :---: | :---: | :---: | :---: |",
        ]

        for cat, cs in res.scores.category_scores.items():
            clean_name = cat.replace("_", " ").title()
            lines.append(f"| {clean_name} | {cs.score} | {cs.critical_count} | {cs.high_count} | {cs.medium_count} | {cs.low_count} |")

        lines.extend([
            "",
            "### 🤖 GEO / AI-Search Readiness Pillars",
            f"- **AI Crawler Access**: {res.scores.geo_score_breakdown.get('ai_crawler_access', 0)} / 40",
            f"- **/llms.txt Availability**: {res.scores.geo_score_breakdown.get('llms_txt_presence', 0)} / 20",
            f"- **Entity & Authorship Clarity**: {res.scores.geo_score_breakdown.get('entity_authorship', 0)} / 20",
            f"- **QA & Semantic Structures**: {res.scores.geo_score_breakdown.get('qa_semantic_structure', 0)} / 20",
            "",
            "---",
            "## 🚨 Prioritized Findings",
            "",
        ])

        if not res.findings:
            lines.append("✅ *No issues detected across all active audit checks.*")
        else:
            sorted_findings = sorted(res.findings, key=lambda f: (
                0 if f.severity == Severity.CRITICAL else
                1 if f.severity == Severity.HIGH else
                2 if f.severity == Severity.MEDIUM else
                3 if f.severity == Severity.LOW else 4
            ))

            for f in sorted_findings:
                sev_badge = f"**[{f.severity.value.upper()}]**"
                fix_badge = "⚡ `AUTO-FIXABLE`" if f.auto_fixable else "🛠️ `MANUAL`"
                lines.extend([
                    f"### {sev_badge} {f.title} ({fix_badge})",
                    f"- **URL**: `{f.url}`",
                    f"- **Rule ID**: `{f.id}`",
                    f"- **Why It Matters**: {f.why_it_matters}",
                    f"- **Recommended Fix**: {f.recommended_action}",
                ])
                if f.evidence:
                    lines.append(f"- **Evidence**: `{f.evidence}`")
                lines.append("")

        if res.missing_capabilities:
            lines.extend([
                "---",
                "## 🔌 Enriched Audit Capabilities (Missing Integrations)",
                "",
            ])
            for cap in res.missing_capabilities:
                lines.extend([
                    f"### {cap.name}",
                    f"- **Impact**: {cap.why_it_improves_audit}",
                    f"- **How to Enable**: {cap.how_to_enable}",
                    "",
                ])

        lines.extend([
            "---",
            "*Generated autonomously by [SiteProbe](https://github.com/tmolavi/siteprobe).*",
        ])
        return "\n".join(lines)

    @classmethod
    def save(cls, audit_result: AuditResult, output_path: Union[str, Path]) -> Path:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        content = cls.render(audit_result)
        p.write_text(content, encoding="utf-8")
        return p
