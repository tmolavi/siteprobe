from typer.testing import CliRunner
from siteprobe.checks.technical.ssr import SsrCheck, analyze_ssr
from siteprobe.cli.main import app
from siteprobe.models.crawl import CrawlPage


runner = CliRunner()


def test_ssr_nextjs():
    html = """
    <!DOCTYPE html>
    <html>
      <head><title>Next.js Page</title></head>
      <body>
        <div id="__next"><h1>Next App</h1><p>Server rendered content.</p></div>
        <script id="__NEXT_DATA__" type="application/json">{"props":{"pageProps":{}}}</script>
      </body>
    </html>
    """
    res = analyze_ssr(html)
    assert res.rendering_mode == "HYDRATED_SSR"
    assert res.framework == "Next.js"
    assert res.has_hydration_payload is True
    assert res.raw_seo_tags["title"] is True
    assert res.raw_seo_tags["h1"] is True


def test_ssr_nuxt():
    html = """
    <!DOCTYPE html>
    <html data-server-rendered="true">
      <head><title>Nuxt Page</title></head>
      <body>
        <div id="__nuxt"><h1>Nuxt App</h1></div>
        <script id="__NUXT_DATA__" type="application/json">[{"state":{}}]</script>
      </body>
    </html>
    """
    res = analyze_ssr(html)
    assert res.rendering_mode == "HYDRATED_SSR"
    assert "Nuxt" in res.framework
    assert res.has_hydration_payload is True


def test_ssr_astro():
    html = """
    <!DOCTYPE html>
    <html>
      <head><title>Astro Page</title></head>
      <body>
        <h1>Astro Site</h1>
        <astro-island component-url="/island.js"></astro-island>
      </body>
    </html>
    """
    res = analyze_ssr(html)
    assert res.rendering_mode == "ISLANDS_SSR"
    assert "Astro" in res.framework


def test_ssr_client_side_spa():
    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <!-- No title, no description, pure blank shell -->
      </head>
      <body>
        <div id="root"></div>
        <script src="/static/js/main.chunk.js"></script>
      </body>
    </html>
    """
    res = analyze_ssr(html)
    assert res.rendering_mode == "CLIENT_SIDE_SPA"
    assert res.has_empty_root_container is True
    assert res.empty_container_id == "root"
    assert res.raw_seo_tags["title"] is False
    assert res.raw_seo_tags["h1"] is False

    # Check finding generation
    check = SsrCheck()
    page = CrawlPage(url="https://example.com/spa", status_code=200, html=html, depth=0)
    findings = check.run(page, [page], {})
    finding_ids = [f.id for f in findings]
    assert "technical.ssr.client_only_rendering" in finding_ids
    assert "technical.ssr.missing_raw_seo_tags" in finding_ids


def test_ssr_static_html():
    html = """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <title>Static Page</title>
        <meta name="description" content="A comprehensive static HTML article.">
        <link rel="canonical" href="https://example.com/static">
      </head>
      <body>
        <h1>Full Server Rendered Article</h1>
        <p>This is a rich article that has plenty of textual words rendered directly by the server without any need for client side javascript execution.</p>
      </body>
    </html>
    """
    res = analyze_ssr(html)
    assert res.rendering_mode == "STATIC_HTML"
    assert res.raw_seo_tags["title"] is True
    assert res.raw_seo_tags["description"] is True
    assert res.raw_seo_tags["canonical"] is True


def test_cli_ssr_command(mock_server):
    result = runner.invoke(app, ["ssr", f"{mock_server}/destination.html"])
    assert result.exit_code == 0
    assert "Detected Rendering Mode:" in result.output
    assert "Critical SEO Tag" in result.output
