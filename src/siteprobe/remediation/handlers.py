import re
from pathlib import Path
from typing import Optional, Tuple
from bs4 import BeautifulSoup


class SafeAutofixHandler:
    """Safe handlers that perform deterministic file edits with preservation of formatting."""

    @staticmethod
    def fix_html_content(html: str, action_title: str, url: str) -> Tuple[str, bool]:
        """Apply safe deterministic fixes to HTML string."""
        modified = False
        soup = BeautifulSoup(html, "html.parser")

        # 1. Missing lang attribute
        if "lang attribute" in action_title.lower():
            html_tag = soup.find("html")
            if html_tag and not html_tag.get("lang"):
                html_tag["lang"] = "en"
                modified = True

        # 2. Missing viewport
        if "viewport" in action_title.lower():
            head = soup.find("head")
            if head and not soup.find("meta", attrs={"name": re.compile(r"^viewport$", re.I)}):
                vp_tag = soup.new_tag("meta", attrs={"name": "viewport", "content": "width=device-width, initial-scale=1.0"})
                head.insert(0, vp_tag)
                modified = True

        # 3. Missing canonical
        if "canonical tag" in action_title.lower():
            head = soup.find("head")
            if head and not soup.find("link", rel=lambda x: x and "canonical" in (x if isinstance(x, list) else [x])):
                canon_tag = soup.new_tag("link", attrs={"rel": "canonical", "href": url})
                head.append(canon_tag)
                modified = True

        # 4. Missing image alt
        if "alt attribute" in action_title.lower():
            for img in soup.find_all("img"):
                if img.get("alt") is None:
                    img["alt"] = ""
                    modified = True

        if modified:
            return str(soup), True
        return html, False

    @staticmethod
    def create_root_file(repo_path: Path, filename: str, content: str) -> bool:
        """Create a file (e.g. robots.txt, llms.txt) in the project root."""
        target = repo_path / filename
        if not target.exists():
            target.write_text(content, encoding="utf-8")
            return True
        return False
