import json
import re
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup
from siteprobe.models.crawl import CrawlPage, ImageItem
from siteprobe.utils.url_helper import is_same_domain, resolve_link


def extract_page_data(url: str, html: str, status_code: int, headers: Dict[str, str], response_time_ms: float, depth: int = 0) -> CrawlPage:
    """Extract metadata, headings, links, images, and schema data from HTML string."""
    soup = BeautifulSoup(html, "html.parser")
    page = CrawlPage(
        url=url,
        status_code=status_code,
        headers=headers,
        html=html,
        response_time_ms=response_time_ms,
        body_size_bytes=len(html.encode("utf-8")),
        depth=depth,
    )

    # Content-Type
    content_type = headers.get("content-type", "")
    page.content_type = content_type

    # Lang attribute
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        page.lang = html_tag.get("lang").strip()

    # Title
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        page.title = title_tag.string.strip()

    # Meta Description
    meta_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    if meta_desc and meta_desc.get("content"):
        page.meta_description = meta_desc.get("content").strip()

    # Canonical Link
    canonical_tag = soup.find("link", attrs={"rel": lambda x: x and "canonical" in [v.lower() for v in (x if isinstance(x, list) else [x])]})
    if canonical_tag and canonical_tag.get("href"):
        page.canonical = resolve_link(url, canonical_tag.get("href"))

    # Robots meta tag
    robots_meta = soup.find("meta", attrs={"name": re.compile(r"^robots$", re.I)})
    if robots_meta and robots_meta.get("content"):
        page.robots_meta = robots_meta.get("content").strip()
        if "noindex" in page.robots_meta.lower():
            page.is_indexable = False

    # Check X-Robots-Tag header
    x_robots = headers.get("x-robots-tag", "")
    if "noindex" in x_robots.lower():
        page.is_indexable = False

    # Headings
    for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        level = h.name.lower()
        text = h.get_text(strip=True)
        if text:
            page.headings.append({"level": level, "text": text})
            if level == "h1":
                page.h1s.append(text)

    # Hreflangs
    for link_tag in soup.find_all("link", attrs={"rel": lambda x: x and "alternate" in (x if isinstance(x, list) else [x])}):
        hreflang = link_tag.get("hreflang")
        href = link_tag.get("href")
        if hreflang and href:
            page.hreflangs.append({"lang": hreflang.strip(), "href": resolve_link(url, href)})

    # Links
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        resolved = resolve_link(url, href)
        if resolved:
            internal = is_same_domain(url, resolved)
            rel = a.get("rel", "")
            if isinstance(rel, list):
                rel = " ".join(rel)
            page.links.append({
                "href": resolved,
                "text": a.get_text(strip=True),
                "internal": internal,
                "rel": rel,
            })

    # Images
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if src:
            resolved_src = resolve_link(url, src)
            alt = img.get("alt")
            loading = img.get("loading")
            width = img.get("width")
            height = img.get("height")
            page.images.append(ImageItem(
                src=resolved_src,
                alt=alt.strip() if alt is not None else None,
                loading=loading.strip() if loading else None,
                width=str(width) if width else None,
                height=str(height) if height else None,
            ))

    # Scripts & Stylesheets
    for s in soup.find_all("script", src=True):
        page.scripts.append(resolve_link(url, s.get("src")))
    for l in soup.find_all("link", rel=lambda x: x and "stylesheet" in (x if isinstance(x, list) else [x])):
        if l.get("href"):
            page.stylesheets.append(resolve_link(url, l.get("href")))

    # OpenGraph & Twitter Card
    for meta in soup.find_all("meta"):
        prop = meta.get("property") or meta.get("name") or ""
        cont = meta.get("content") or ""
        if prop.startswith("og:"):
            page.open_graph[prop] = cont
        elif prop.startswith("twitter:"):
            page.twitter_card[prop] = cont

    # Schema.org JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        if script.string:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    page.schema_raw.append(data)
                    stype = data.get("@type")
                    if stype:
                        page.schema_types.append(stype if isinstance(stype, str) else str(stype))
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            page.schema_raw.append(item)
                            stype = item.get("@type")
                            if stype:
                                page.schema_types.append(stype if isinstance(stype, str) else str(stype))
            except Exception:
                page.schema_raw.append({"_parse_error": True, "raw": script.string[:200]})

    return page
