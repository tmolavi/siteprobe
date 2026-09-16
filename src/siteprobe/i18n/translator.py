import json
from pathlib import Path
from typing import Any, Dict, Optional
from siteprobe.models.finding import Finding


LOCALES_DIR = Path(__file__).parent / "locales"


class Translator:
    """Translation manager supporting en, fa, and tr locales."""

    def __init__(self, lang: str = "en"):
        self.lang = lang.lower() if lang else "en"
        self._catalogs: Dict[str, Dict[str, Any]] = {}
        self._load_catalogs()

    def _load_catalogs(self) -> None:
        for file in LOCALES_DIR.glob("*.json"):
            code = file.stem.lower()
            try:
                with open(file, "r", encoding="utf-8") as f:
                    self._catalogs[code] = json.load(f)
            except Exception:
                self._catalogs[code] = {}

    def get_category_label(self, category: str) -> str:
        cat = str(category).lower()
        active = self._catalogs.get(self.lang, {})
        if "categories" in active and cat in active["categories"]:
            return active["categories"][cat]
        fallback = self._catalogs.get("en", {})
        return fallback.get("categories", {}).get(cat, category)

    def get_severity_label(self, severity: str) -> str:
        sev = str(severity).lower()
        active = self._catalogs.get(self.lang, {})
        if "severities" in active and sev in active["severities"]:
            return active["severities"][sev]
        fallback = self._catalogs.get("en", {})
        return fallback.get("severities", {}).get(sev, severity)

    def translate_finding(self, finding: Finding) -> Finding:
        """Return a copy of finding with title, why_it_matters, and recommended_action translated if available."""
        if self.lang == "en":
            return finding

        active = self._catalogs.get(self.lang, {})
        entry = active.get("findings", {}).get(finding.id)
        if not entry:
            return finding

        translated = finding.model_copy()
        if "title" in entry:
            translated.title = entry["title"]
        if "why_it_matters" in entry:
            translated.why_it_matters = entry["why_it_matters"]
        if "recommended_action" in entry:
            translated.recommended_action = entry["recommended_action"]
        return translated


_default_translator: Optional[Translator] = None


def get_translator(lang: str = "en") -> Translator:
    global _default_translator
    if _default_translator is None or _default_translator.lang != lang:
        _default_translator = Translator(lang)
    return _default_translator
