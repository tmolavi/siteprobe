import pytest
from siteprobe.crawler.extractors import extract_page_data
from siteprobe.crawler.robots import RobotsParser
from siteprobe.crawler.sitemap import SitemapParser
from siteprobe.crawler.storage import CrawlStorage
from siteprobe.models.crawl import CrawlPage


def test_robots_parser():
    content = """
User-agent: *
Disallow: /admin/
Allow: /admin/public/

User-agent: OAI-SearchBot
Allow: /

User-agent: CCBot
Disallow: /

Sitemap: https://example.com/sitemap.xml
"""
    parser = RobotsParser(content)
    assert "https://example.com/sitemap.xml" in parser.sitemaps
    assert parser.is_allowed("Googlebot", "/") is True
    assert parser.is_allowed("Googlebot", "/admin/secret") is False
    assert parser.is_allowed("Googlebot", "/admin/public/page") is True

    ai_status = parser.get_ai_crawler_status()
    assert ai_status["OAI-SearchBot"]["allowed"] is True
    assert ai_status["CCBot"]["allowed"] is False


def test_sitemap_parser():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://example.com/page1</loc></url>
      <url><loc>https://example.com/page2</loc></url>
    </urlset>
    """
    urls = SitemapParser.parse_xml_content(xml)
    assert "https://example.com/page1" in urls
    assert "https://example.com/page2" in urls


def test_page_extractor():
    html = """
    <html lang="en">
      <head>
        <title>Sample Test Page</title>
        <meta name="description" content="Sample description here.">
        <link rel="canonical" href="https://example.com/canonical">
      </head>
      <body>
        <h1>Main Heading</h1>
        <h2>Subheading</h2>
        <a href="/internal" rel="nofollow">Internal Link</a>
        <img src="pic.jpg" alt="A photo">
        <script type="application/ld+json">
          {"@context": "https://schema.org", "@type": "Organization", "name": "Acme Corp"}
        </script>
      </body>
    </html>
    """
    page = extract_page_data("https://example.com/page", html, 200, {"content-type": "text/html"}, 120.0)
    assert page.title == "Sample Test Page"
    assert page.meta_description == "Sample description here."
    assert page.canonical == "https://example.com/canonical"
    assert page.lang == "en"
    assert len(page.h1s) == 1
    assert page.h1s[0] == "Main Heading"
    assert len(page.images) == 1
    assert page.images[0].alt == "A photo"
    assert "Organization" in page.schema_types


@pytest.mark.asyncio
async def test_crawl_storage():
    storage = CrawlStorage(":memory:")
    await storage.initialize()
    page = CrawlPage(url="https://example.com/test", status_code=200, title="Test")
    await storage.save_page(page)

    retrieved = await storage.get_page("https://example.com/test")
    assert retrieved is not None
    assert retrieved.title == "Test"
    assert await storage.count_pages() == 1
    await storage.close()
