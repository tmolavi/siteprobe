import re
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from siteprobe.checks.base import BaseCheck
from siteprobe.models.crawl import CrawlPage
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity


class SsrAnalysisResult(BaseModel):
    rendering_mode: str = "STATIC_HTML"  # FULL_SSR, HYDRATED_SSR, ISLANDS_SSR, STATIC_HTML, CLIENT_SIDE_SPA
    framework: str = "None / Static"
    has_hydration_payload: bool = False
    hydration_payload_size_bytes: int = 0
    raw_word_count: int = 0
    has_empty_root_container: bool = False
    empty_container_id: Optional[str] = None
    raw_seo_tags: Dict[str, bool] = Field(default_factory=dict)
    details: List[str] = Field(default_factory=list)


def analyze_ssr(html: str) -> SsrAnalysisResult:
    """Analyze raw HTML for SSR indicators, client hydration payloads, and empty SPA root shells."""
    result = SsrAnalysisResult()
    if not html:
        result.rendering_mode = "CLIENT_SIDE_SPA"
        result.details.append("Initial HTML response is empty.")
        return result

    soup = BeautifulSoup(html, "html.parser")

    # 1. Inspect raw SEO tags
    title = soup.find("title")
    meta_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    h1 = soup.find("h1")
    canonical = soup.find("link", rel=lambda x: x and "canonical" in (x if isinstance(x, list) else [x]))

    result.raw_seo_tags = {
        "title": bool(title and title.get_text(strip=True)),
        "description": bool(meta_desc and meta_desc.get("content", "").strip()),
        "h1": bool(h1 and h1.get_text(strip=True)),
        "canonical": bool(canonical and canonical.get("href", "").strip()),
    }

    # 2. Inspect body text volume (ignoring scripts/styles)
    body = soup.find("body")
    text_content = ""
    if body:
        soup_copy = BeautifulSoup(str(body), "html.parser")
        for s in soup_copy(["script", "style", "noscript"]):
            s.decompose()
        text_content = soup_copy.get_text(separator=" ", strip=True)
    words = re.findall(r"\b\w+\b", text_content)
    result.raw_word_count = len(words)

    # 3. Detect framework hydration payloads
    hydration_size = 0
    detected_framework = None

    # Next.js
    next_script = soup.find("script", id="__NEXT_DATA__")
    if next_script and next_script.string:
        detected_framework = "Next.js"
        hydration_size += len(next_script.string)
        result.details.append("Detected Next.js hydration payload (__NEXT_DATA__).")
    elif "self.__next_f" in html or "/_next/static/" in html:
        detected_framework = "Next.js (App Router)"
        result.details.append("Detected Next.js App Router streaming markers.")

    # Nuxt.js
    nuxt_script = soup.find("script", id="__NUXT_DATA__") or soup.find(string=re.compile(r"window\.__NUXT__"))
    if nuxt_script:
        detected_framework = "Nuxt.js"
        hydration_size += len(str(nuxt_script))
        result.details.append("Detected Nuxt.js hydration payload.")
    elif 'data-server-rendered="true"' in html:
        detected_framework = "Nuxt.js / Vue SSR"
        result.details.append("Detected Vue server-rendered attribute.")

    # Remix
    if "window.__remixContext" in html or "__remixManifest" in html:
        detected_framework = "Remix"
        result.details.append("Detected Remix context hydration payload.")

    # SvelteKit
    if "__sveltekit" in html or "data-sveltekit-hydrate" in html:
        detected_framework = "SvelteKit"
        result.details.append("Detected SvelteKit hydration payload.")

    # Astro Islands
    if soup.find("astro-island") or "astro-island" in html:
        detected_framework = "Astro (Islands Architecture)"
        result.details.append("Detected Astro partial hydration islands.")

    # Angular Universal
    if soup.find(attrs={"ng-version": True}) or "ng-server-context" in html:
        detected_framework = "Angular Universal"
        result.details.append("Detected Angular server-side rendering markers.")

    # Gatsby
    if soup.find("div", id="___gatsby") or "___gatsby" in html:
        detected_framework = "Gatsby"
        result.details.append("Detected Gatsby static hydration markers.")

    if detected_framework:
        result.framework = detected_framework
        result.has_hydration_payload = True
        result.hydration_payload_size_bytes = hydration_size

    # 4. Detect empty SPA root shells (e.g. <div id="root"></div> or <div id="app"></div>)
    common_spa_roots = ["root", "app", "__next", "main-app"]
    for root_id in common_spa_roots:
        root_elem = soup.find("div", id=root_id)
        if root_elem:
            inner_text = root_elem.get_text(strip=True)
            if len(inner_text) < 30 and result.raw_word_count < 35:
                result.has_empty_root_container = True
                result.empty_container_id = root_id
                result.details.append(f"Found near-empty container <div id='{root_id}'> without server-rendered content.")
                break

    # 5. Classify rendering architecture
    has_scripts = bool(soup.find_all("script", src=True))
    if result.has_empty_root_container and has_scripts:
        result.rendering_mode = "CLIENT_SIDE_SPA"
    elif detected_framework and "Astro" in detected_framework:
        result.rendering_mode = "ISLANDS_SSR"
    elif detected_framework:
        result.rendering_mode = "HYDRATED_SSR"
    elif result.raw_word_count > 60:
        result.rendering_mode = "STATIC_HTML"
    else:
        result.rendering_mode = "CLIENT_SIDE_SPA" if has_scripts else "STATIC_HTML"

    return result


class SsrCheck(BaseCheck):
    id = "technical.ssr"
    category = FindingCategory.TECHNICAL_SEO
    name = "Server-Side Rendering & Hydration Audit"
    description = "Inspects raw HTTP responses for client-side empty shells and unrendered SEO tags."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200 or not page.html:
            return findings

        analysis = analyze_ssr(page.html)

        # Flag Client-Side Rendered SPAs with empty DOM shell
        if analysis.rendering_mode == "CLIENT_SIDE_SPA":
            findings.append(Finding(
                id="technical.ssr.client_only_rendering",
                category=self.category,
                severity=Severity.HIGH,
                confidence=0.92,
                url=page.url,
                title="Client-Side Only Rendering (SPA) detected with empty initial HTML shell",
                evidence={
                    "rendering_mode": analysis.rendering_mode,
                    "raw_word_count": analysis.raw_word_count,
                    "empty_container": analysis.empty_container_id,
                    "framework": analysis.framework,
                },
                why_it_matters="Search engines and AI retrieval bots crawl raw HTML first. If main content is rendered solely in the client browser, search bots face rendering delays or may fail to index the page content entirely.",
                recommended_action="Implement Server-Side Rendering (SSR) or Static Site Generation (SSG) using frameworks like Next.js, Nuxt, or Astro.",
                auto_fixable=False,
                risk_class=RiskClass.MANUAL_ONLY,
                required_capability="source_code",
                verification_check="technical.ssr",
            ))

        # Flag missing critical SEO tags in raw HTML
        missing_tags = [k for k, v in analysis.raw_seo_tags.items() if not v]
        if missing_tags and page.depth == 0:
            findings.append(Finding(
                id="technical.ssr.missing_raw_seo_tags",
                category=self.category,
                severity=Severity.HIGH,
                confidence=0.95,
                url=page.url,
                title=f"Critical SEO tag(s) missing from raw server HTML: {', '.join(missing_tags)}",
                evidence={
                    "missing_raw_tags": missing_tags,
                    "raw_tags_status": analysis.raw_seo_tags,
                },
                why_it_matters="Crawlers that do not execute JavaScript (or execute it with low render budgets) will not detect client-injected metadata like titles or descriptions.",
                recommended_action="Ensure title, description, and canonical tags are rendered directly in the initial server HTML response.",
                auto_fixable=True,
                risk_class=RiskClass.REVIEW_RECOMMENDED,
                required_capability="source_code",
                verification_check="technical.ssr",
            ))

        return findings
