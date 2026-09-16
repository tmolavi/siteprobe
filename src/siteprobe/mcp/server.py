import asyncio
import uuid
from typing import Any, Dict, List, Optional
import httpx

try:
    from mcp.server.fastmcp import FastMCP
except (ImportError, ModuleNotFoundError):
    try:
        from mcp.server.mcpserver import MCPServer as FastMCP
    except Exception:
        FastMCP = None

from siteprobe.checks.technical.ssr import analyze_ssr
from siteprobe.core.config import SiteProbeConfig
from siteprobe.core.engine import AuditEngine, AuditResult
from siteprobe.models.config import CrawlConfig, SiteConfig
from siteprobe.models.finding import FindingCategory, Severity
from siteprobe.remediation.executor import RemediationExecutor
from siteprobe.remediation.planner import RemediationPlanner
from siteprobe.reporting.html_reporter import HtmlReporter
from siteprobe.reporting.json_reporter import JsonReporter
from siteprobe.reporting.markdown_reporter import MarkdownReporter
from siteprobe.verification.verifier import FixVerifier


mcp = FastMCP("siteprobe")

# In-memory background jobs repository
_JOBS: Dict[str, Dict[str, Any]] = {}


@mcp.tool()
async def start_audit(url: str, max_pages: int = 50, language: str = "en") -> str:
    """Start an asynchronous website audit and return a unique job_id."""
    job_id = str(uuid.uuid4())[:8]
    _JOBS[job_id] = {
        "status": "running",
        "url": url,
        "language": language,
        "result": None,
        "error": None,
    }

    async def _runner():
        try:
            cfg = SiteProbeConfig(
                site=SiteConfig(url=url, language=language),
                crawl=CrawlConfig(max_pages=max_pages),
            )
            engine = AuditEngine(config=cfg, language=language)
            result = await engine.run_audit(url)
            _JOBS[job_id]["result"] = result
            _JOBS[job_id]["status"] = "completed"
        except Exception as e:
            _JOBS[job_id]["status"] = "failed"
            _JOBS[job_id]["error"] = str(e)

    asyncio.create_task(_runner())
    return f"Audit job started with ID: {job_id}. Use get_audit_status('{job_id}') to track progress."


@mcp.tool()
def get_audit_status(job_id: str) -> Dict[str, Any]:
    """Check the status of an ongoing or completed audit job."""
    job = _JOBS.get(job_id)
    if not job:
        return {"error": f"Job {job_id} not found."}
    return {
        "job_id": job_id,
        "status": job["status"],
        "url": job["url"],
        "error": job["error"],
        "has_result": job["result"] is not None,
    }


@mcp.tool()
async def check_ssr(url: str) -> Dict[str, Any]:
    """Inspect a URL to check whether it uses Server-Side Rendering (SSR) vs Client-Side (CSR/SPA)."""
    try:
        async with httpx.AsyncClient(
            headers={"User-Agent": "SiteProbe/0.1.1 MCP-SSR"},
            follow_redirects=True,
            timeout=15.0
        ) as client:
            resp = await client.get(url)
            analysis = analyze_ssr(resp.text)
            return {
                "url": url,
                "status_code": resp.status_code,
                "rendering_mode": analysis.rendering_mode,
                "framework": analysis.framework,
                "has_hydration_payload": analysis.has_hydration_payload,
                "hydration_payload_size_bytes": analysis.hydration_payload_size_bytes,
                "raw_word_count": analysis.raw_word_count,
                "has_empty_root_container": analysis.has_empty_root_container,
                "raw_seo_tags": analysis.raw_seo_tags,
                "diagnostic_signals": analysis.details,
            }
    except Exception as e:
        return {"error": str(e), "url": url}


@mcp.tool()
def get_findings(job_id: str, category: Optional[str] = None, severity: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all findings from a completed audit job, with optional filtering."""
    job = _JOBS.get(job_id)
    if not job or not job.get("result"):
        return []
    res: AuditResult = job["result"]
    findings = res.findings
    if category:
        findings = [f for f in findings if f.category.value == category]
    if severity:
        findings = [f for f in findings if f.severity.value == severity]
    return [f.to_dict() for f in findings]


@mcp.tool()
def get_finding(job_id: str, finding_id: str) -> Dict[str, Any]:
    """Retrieve detailed data and evidence for a specific finding ID."""
    job = _JOBS.get(job_id)
    if not job or not job.get("result"):
        return {"error": "Audit result not ready"}
    res: AuditResult = job["result"]
    for f in res.findings:
        if f.id == finding_id:
            return f.to_dict()
    return {"error": f"Finding {finding_id} not found"}


@mcp.tool()
def get_crawl_summary(job_id: str) -> Dict[str, Any]:
    """Retrieve crawl summary and status code statistics."""
    job = _JOBS.get(job_id)
    if not job or not job.get("result"):
        return {"error": "Audit result not ready"}
    res: AuditResult = job["result"]
    return res.crawl_summary.model_dump()


@mcp.tool()
def get_geo_findings(job_id: str) -> Dict[str, Any]:
    """Get GEO / AI-search specific readiness score and findings."""
    job = _JOBS.get(job_id)
    if not job or not job.get("result"):
        return {"error": "Audit result not ready"}
    res: AuditResult = job["result"]
    geo_findings = [f.to_dict() for f in res.findings if f.category == FindingCategory.GEO_AEO]
    return {
        "geo_score": res.scores.geo_score,
        "pillars": res.scores.geo_score_breakdown,
        "findings": geo_findings,
    }


@mcp.tool()
def get_performance_findings(job_id: str) -> Dict[str, Any]:
    """Get performance and server latency findings."""
    job = _JOBS.get(job_id)
    if not job or not job.get("result"):
        return {"error": "Audit result not ready"}
    res: AuditResult = job["result"]
    return {
        "score": res.scores.category_scores.get(FindingCategory.PERFORMANCE.value, {}).score if hasattr(res.scores.category_scores.get(FindingCategory.PERFORMANCE.value), 'score') else 100,
        "findings": [f.to_dict() for f in res.findings if f.category == FindingCategory.PERFORMANCE],
    }


@mcp.tool()
def get_accessibility_findings(job_id: str) -> Dict[str, Any]:
    """Get accessibility WCAG findings."""
    job = _JOBS.get(job_id)
    if not job or not job.get("result"):
        return {"error": "Audit result not ready"}
    res: AuditResult = job["result"]
    return {
        "score": res.scores.category_scores.get(FindingCategory.ACCESSIBILITY.value, {}).score if hasattr(res.scores.category_scores.get(FindingCategory.ACCESSIBILITY.value), 'score') else 100,
        "findings": [f.to_dict() for f in res.findings if f.category == FindingCategory.ACCESSIBILITY],
    }


@mcp.tool()
def create_remediation_plan(job_id: str) -> Dict[str, Any]:
    """Generate a risk-categorized remediation plan from audit findings."""
    job = _JOBS.get(job_id)
    if not job or not job.get("result"):
        return {"error": "Audit result not ready"}
    res: AuditResult = job["result"]
    plan = RemediationPlanner.create_plan(res.site_url, res.findings)
    res.remediation_plan = plan
    return plan.model_dump()


@mcp.tool()
def apply_safe_fixes(job_id: str, repo_path: str) -> Dict[str, Any]:
    """Apply safe, non-destructive automated fixes to a local repository."""
    job = _JOBS.get(job_id)
    if not job or not job.get("result"):
        return {"error": "Audit result not ready"}
    res: AuditResult = job["result"]
    plan = res.remediation_plan or RemediationPlanner.create_plan(res.site_url, res.findings)
    executor = RemediationExecutor(repo_path)
    report = executor.apply_safe_fixes(plan)
    return report.model_dump()


@mcp.tool()
def verify_fixes(job_id: str, repo_path: str) -> List[Dict[str, Any]]:
    """Verify before-and-after fix state for audit findings."""
    job = _JOBS.get(job_id)
    if not job or not job.get("result"):
        return [{"error": "Audit result not ready"}]
    res: AuditResult = job["result"]
    results = FixVerifier.verify_local_changes(res.findings, repo_path)
    return [r.model_dump() for r in results]


@mcp.tool()
def generate_report(job_id: str, format: str = "markdown") -> str:
    """Generate audit report in 'markdown', 'json', or 'html' format."""
    job = _JOBS.get(job_id)
    if not job or not job.get("result"):
        return "Error: Audit result not ready."
    res: AuditResult = job["result"]
    fmt = format.lower()
    if fmt == "json":
        return JsonReporter.render(res)
    elif fmt == "html":
        return HtmlReporter.render(res)
    return MarkdownReporter.render(res)


def run_mcp():
    """Run FastMCP server over standard stdio."""
    if mcp is None:
        raise RuntimeError("MCP library not available.")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run_mcp()
