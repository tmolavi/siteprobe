from typing import Any, Dict, List
from bs4 import BeautifulSoup
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class WcagDeterministicCheck(BaseCheck):
    id = "accessibility.wcag"
    category = FindingCategory.ACCESSIBILITY
    name = "Deterministic WCAG Accessibility Check"
    description = "Checks html lang attribute, unassociated form inputs, and empty buttons."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []
        if page.status_code != 200 or not page.html:
            return findings

        soup = BeautifulSoup(page.html, "html.parser")

        # 1. Missing html lang
        if not page.lang:
            findings.append(Finding(
                id="accessibility.html.missing_lang",
                category=self.category,
                severity=Severity.HIGH,
                confidence=1.0,
                url=page.url,
                title="Missing or empty lang attribute on <html> element",
                evidence={},
                why_it_matters="WCAG 2.1 Criterion 3.1.1: Screen readers need the document language to select appropriate voice synthesis and pronunciation.",
                recommended_action="Add lang attribute to <html> tag, e.g. <html lang=\"en\">.",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
                required_capability="source_code",
                verification_check="accessibility.wcag",
            ))

        # 2. Form inputs without label
        unlabeled_inputs = []
        for inp in soup.find_all("input"):
            inp_type = inp.get("type", "text").lower()
            if inp_type in ("hidden", "submit", "button", "image", "reset"):
                continue
            inp_id = inp.get("id")
            has_label = False
            if inp_id and soup.find("label", attrs={"for": inp_id}):
                has_label = True
            elif inp.find_parent("label"):
                has_label = True
            elif inp.get("aria-label") or inp.get("aria-labelledby") or inp.get("title"):
                has_label = True

            if not has_label:
                unlabeled_inputs.append(str(inp)[:100])

        if unlabeled_inputs:
            findings.append(Finding(
                id="accessibility.form.unlabeled_input",
                category=self.category,
                severity=Severity.HIGH,
                confidence=0.98,
                url=page.url,
                title=f"{len(unlabeled_inputs)} form input(s) missing associated label",
                evidence={"snippets": unlabeled_inputs[:3], "count": len(unlabeled_inputs)},
                why_it_matters="WCAG 2.1 Criterion 1.3.1 & 4.1.2: Users with visual impairments cannot determine what information is requested in unlabeled fields.",
                recommended_action="Associate a <label for=\"inputId\"> with the input or provide an explicit aria-label.",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
                required_capability="source_code",
                verification_check="accessibility.wcag",
            ))

        # 3. Empty buttons
        empty_buttons = []
        for btn in soup.find_all("button"):
            txt = btn.get_text(strip=True)
            if not txt and not btn.get("aria-label") and not btn.find("img", alt=True):
                empty_buttons.append(str(btn)[:100])

        if empty_buttons:
            findings.append(Finding(
                id="accessibility.buttons.empty",
                category=self.category,
                severity=Severity.MEDIUM,
                confidence=0.95,
                url=page.url,
                title=f"{len(empty_buttons)} button(s) lack text content or accessible name",
                evidence={"snippets": empty_buttons[:3]},
                why_it_matters="Screen reader users cannot understand the action performed by a button without an accessible name.",
                recommended_action="Provide visible descriptive text or an aria-label attribute inside the button.",
                auto_fixable=True,
                risk_class=RiskClass.SAFE_AUTOFIX,
                required_capability="source_code",
                verification_check="accessibility.wcag",
            ))

        return findings
