from siteprobe.checks.technical.canonical import CanonicalCheck
from siteprobe.checks.technical.status import HttpStatusCheck
from siteprobe.checks.onpage.title import TitleCheck
from siteprobe.checks.onpage.headings import HeadingsCheck
from siteprobe.checks.onpage.images import ImagesCheck
from siteprobe.checks.accessibility.wcag_deterministic import WcagDeterministicCheck
from siteprobe.checks.ux.viewport import ViewportCheck
from siteprobe.models.crawl import CrawlPage, ImageItem


def test_http_status_check():
    check = HttpStatusCheck()
    p_404 = CrawlPage(url="https://example.com/404", status_code=404)
    findings = check.run(p_404, [p_404], {})
    assert len(findings) == 1
    assert findings[0].id == "technical.status.http_4xx"

    p_500 = CrawlPage(url="https://example.com/500", status_code=500)
    findings5 = check.run(p_500, [p_500], {})
    assert len(findings5) == 1
    assert findings5[0].id == "technical.status.http_5xx"


def test_canonical_check():
    check = CanonicalCheck()
    p_no_canon = CrawlPage(url="https://example.com/page", status_code=200)
    findings = check.run(p_no_canon, [p_no_canon], {})
    assert any(f.id == "technical.canonical.missing" for f in findings)

    p_mismatch = CrawlPage(url="https://example.com/page", canonical="https://example.com/other", status_code=200)
    findings2 = check.run(p_mismatch, [p_mismatch], {})
    assert any(f.id == "technical.canonical.mismatch" for f in findings2)


def test_title_check():
    check = TitleCheck()
    p_empty = CrawlPage(url="https://example.com/page", title="", status_code=200)
    findings = check.run(p_empty, [p_empty], {})
    assert any(f.id == "onpage.title.missing" for f in findings)

    p_long = CrawlPage(url="https://example.com/page", title="A" * 70, status_code=200)
    findings_long = check.run(p_long, [p_long], {})
    assert any(f.id == "onpage.title.too_long" for f in findings_long)


def test_headings_check():
    check = HeadingsCheck()
    p_no_h1 = CrawlPage(url="https://example.com/page", h1s=[], status_code=200)
    findings = check.run(p_no_h1, [p_no_h1], {})
    assert any(f.id == "onpage.h1.missing" for f in findings)

    p_multi_h1 = CrawlPage(url="https://example.com/page", h1s=["H1 First", "H1 Second"], status_code=200)
    findings_multi = check.run(p_multi_h1, [p_multi_h1], {})
    assert any(f.id == "onpage.h1.multiple" for f in findings_multi)


def test_images_check():
    check = ImagesCheck()
    p_img = CrawlPage(url="https://example.com/page", images=[ImageItem(src="test.png", alt=None)], status_code=200)
    findings = check.run(p_img, [p_img], {})
    assert any(f.id == "onpage.images.missing_alt" for f in findings)


def test_accessibility_check():
    check = WcagDeterministicCheck()
    html = '<html><head></head><body><form><input type="text" name="foo"></form></body></html>'
    p = CrawlPage(url="https://example.com/page", html=html, status_code=200)
    findings = check.run(p, [p], {})
    assert any(f.id == "accessibility.html.missing_lang" for f in findings)
    assert any(f.id == "accessibility.form.unlabeled_input" for f in findings)


def test_viewport_check():
    check = ViewportCheck()
    html = '<html><head><title>Test</title></head><body></body></html>'
    p = CrawlPage(url="https://example.com/page", html=html, status_code=200)
    findings = check.run(p, [p], {})
    assert any(f.id == "ux.viewport.missing" for f in findings)
