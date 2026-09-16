from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RedirectHop(BaseModel):
    url: str
    status_code: int


class ImageItem(BaseModel):
    src: str
    alt: Optional[str] = None
    loading: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None


class CrawlPage(BaseModel):
    url: str
    status_code: int
    content_type: str = ""
    headers: Dict[str, str] = Field(default_factory=dict)
    html: str = ""
    title: str = ""
    meta_description: str = ""
    h1s: List[str] = Field(default_factory=list)
    headings: List[Dict[str, str]] = Field(default_factory=list)  # {"level": "h2", "text": "..."}
    canonical: Optional[str] = None
    robots_meta: Optional[str] = None
    lang: Optional[str] = None
    hreflangs: List[Dict[str, str]] = Field(default_factory=list)  # {"lang": "en", "href": "..."}
    links: List[Dict[str, Any]] = Field(default_factory=list)  # {"href": "...", "text": "...", "internal": True, "rel": "..."}
    images: List[ImageItem] = Field(default_factory=list)
    scripts: List[str] = Field(default_factory=list)
    stylesheets: List[str] = Field(default_factory=list)
    schema_types: List[str] = Field(default_factory=list)
    schema_raw: List[Dict[str, Any]] = Field(default_factory=list)
    open_graph: Dict[str, str] = Field(default_factory=dict)
    twitter_card: Dict[str, str] = Field(default_factory=dict)
    response_time_ms: float = 0.0
    body_size_bytes: int = 0
    depth: int = 0
    is_indexable: bool = True
    redirect_chain: List[RedirectHop] = Field(default_factory=list)


class CrawlSummary(BaseModel):
    start_url: str
    total_crawled: int = 0
    total_internal_discovered: int = 0
    total_external_discovered: int = 0
    broken_links_count: int = 0
    crawl_duration_seconds: float = 0.0
    status_codes_distribution: Dict[str, int] = Field(default_factory=dict)
