from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SiteConfig(BaseModel):
    url: str
    language: str = "en"


class CrawlConfig(BaseModel):
    max_pages: int = 100
    max_depth: int = 4
    concurrency: int = 5
    crawl_delay_ms: int = 100
    respect_robots: bool = True
    timeout_seconds: float = 15.0
    user_agent: str = "SiteProbe/0.1.0 (+https://github.com/tmolavi/siteprobe)"


class ChecksConfig(BaseModel):
    technical: bool = True
    onpage: bool = True
    schema_org: bool = True
    geo: bool = True
    performance: bool = True
    accessibility: bool = True
    security: bool = True
    content: bool = True
    ux: bool = True


class IntegrationsConfig(BaseModel):
    search_console: bool = False
    ga4: bool = False
    dataforseo: bool = False
    lighthouse: bool = False
    playwright: bool = False


class SiteProbeConfig(BaseModel):
    site: SiteConfig
    crawl: CrawlConfig = Field(default_factory=CrawlConfig)
    checks: ChecksConfig = Field(default_factory=ChecksConfig)
    integrations: IntegrationsConfig = Field(default_factory=IntegrationsConfig)
