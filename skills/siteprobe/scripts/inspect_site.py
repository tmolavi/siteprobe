#!/usr/bin/env python3
"""SiteProbe Agent Helper Script: Quickly inspect a website and print raw summary."""
import asyncio
import sys
from siteprobe.core.engine import AuditEngine
from siteprobe.models.config import CrawlConfig, SiteConfig, SiteProbeConfig


async def main():
    if len(sys.argv) < 2:
        print("Usage: python inspect_site.py <url> [lang]")
        sys.exit(1)

    url = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "en"

    cfg = SiteProbeConfig(
        site=SiteConfig(url=url, language=lang),
        crawl=CrawlConfig(max_pages=20),
    )
    engine = AuditEngine(config=cfg, language=lang)
    res = await engine.run_audit(url)

    print(f"Audit Complete: {res.site_url}")
    print(f"Overall Quality Score: {res.scores.overall_score}/100")
    print(f"GEO Score: {res.scores.geo_score}/100")
    print(f"Total Findings: {len(res.findings)}")
    for f in res.findings[:5]:
        print(f" - [{f.severity.value.upper()}] {f.title} ({f.url})")


if __name__ == "__main__":
    asyncio.run(main())
