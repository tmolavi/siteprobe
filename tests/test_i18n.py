from siteprobe.i18n.translator import Translator
from siteprobe.models.finding import Finding, FindingCategory, Severity


def test_translations():
    f_orig = Finding(
        id="technical.canonical.missing",
        category=FindingCategory.TECHNICAL_SEO,
        severity=Severity.HIGH,
        url="https://example.com",
        title="Missing canonical URL tag",
        why_it_matters="Without a canonical tag...",
        recommended_action="Add canonical...",
    )

    # Persian
    fa_trans = Translator("fa")
    f_fa = fa_trans.translate_finding(f_orig)
    assert "کنونیکال" in f_fa.title
    assert fa_trans.get_category_label("technical_seo") == "سئو فنی (تکنیکال)"

    # Turkish
    tr_trans = Translator("tr")
    f_tr = tr_trans.translate_finding(f_orig)
    assert "Kanonik" in f_tr.title
    assert tr_trans.get_category_label("technical_seo") == "Teknik SEO"
