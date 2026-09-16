import re
import xml.etree.ElementTree as ET
from typing import List, Optional
import httpx


class SitemapParser:
    """Discovers and parses standard XML sitemaps and sitemap indexes."""

    @staticmethod
    def parse_xml_content(xml_text: str) -> List[str]:
        urls: List[str] = []
        if not xml_text:
            return urls

        # Remove XML namespaces for easier traversal
        clean_xml = re.sub(r'\sxmlns="[^"]+"', '', xml_text, count=1)
        try:
            root = ET.fromstring(clean_xml)
        except Exception:
            # Fallback regex extraction if XML is slightly malformed
            return re.findall(r'<loc>\s*(https?://[^\s<]+)\s*</loc>', xml_text, re.IGNORECASE)

        # Standard urlset
        for loc in root.findall(".//url/loc"):
            if loc.text and loc.text.strip():
                urls.append(loc.text.strip())

        # Sitemapindex references
        for loc in root.findall(".//sitemap/loc"):
            if loc.text and loc.text.strip():
                urls.append(loc.text.strip())

        return urls

    @classmethod
    async def fetch_sitemap_urls(cls, sitemap_url: str, client: httpx.AsyncClient, max_sub_sitemaps: int = 5) -> List[str]:
        discovered_urls: List[str] = []
        try:
            resp = await client.get(sitemap_url, follow_redirects=True, timeout=10.0)
            if resp.status_code != 200:
                return discovered_urls

            locs = cls.parse_xml_content(resp.text)
            sub_sitemaps = [l for l in locs if l.endswith(".xml") or "sitemap" in l]
            page_urls = [l for l in locs if l not in sub_sitemaps]

            discovered_urls.extend(page_urls)

            # Recurse for sub-sitemaps up to limit
            for sub in sub_sitemaps[:max_sub_sitemaps]:
                if sub != sitemap_url:
                    try:
                        sub_resp = await client.get(sub, follow_redirects=True, timeout=10.0)
                        if sub_resp.status_code == 200:
                            sub_locs = cls.parse_xml_content(sub_resp.text)
                            discovered_urls.extend([l for l in sub_locs if not (l.endswith(".xml") or "sitemap" in l)])
                    except Exception:
                        continue
        except Exception:
            pass

        return list(dict.fromkeys(discovered_urls))
