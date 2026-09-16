import re
from urllib.parse import urljoin, urlparse, urlunparse, parse_qsl, urlencode


def normalize_url(url: str, remove_fragments: bool = True, strip_trailing_slash: bool = False) -> str:
    """Normalize URL by lowering scheme and netloc, sorting query params, and stripping fragments."""
    if not url:
        return ""
    url = url.strip()
    parsed = urlparse(url)
    scheme = parsed.scheme.lower() if parsed.scheme else "http"
    netloc = parsed.netloc.lower()
    # Default ports removal
    if (scheme == "http" and netloc.endswith(":80")) or (scheme == "https" and netloc.endswith(":443")):
        netloc = netloc.rsplit(":", 1)[0]
        
    path = parsed.path or "/"
    if strip_trailing_slash and len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")

    # Sort query parameters
    query_tuples = parse_qsl(parsed.query, keep_blank_values=True)
    query_tuples.sort(key=lambda x: x[0])
    query = urlencode(query_tuples)

    fragment = "" if remove_fragments else parsed.fragment
    return urlunparse((scheme, netloc, path, parsed.params, query, fragment))


def is_same_domain(url1: str, url2: str) -> bool:
    """Check if two URLs share the exact domain or subdomain."""
    p1 = urlparse(url1).netloc.lower().split(":")[0]
    p2 = urlparse(url2).netloc.lower().split(":")[0]
    # Remove leading www. for comparison
    clean_p1 = p1[4:] if p1.startswith("www.") else p1
    clean_p2 = p2[4:] if p2.startswith("www.") else p2
    return clean_p1 == clean_p2


def resolve_link(base_url: str, link: str) -> str:
    """Resolve relative or protocol-relative link against base URL."""
    if not link:
        return ""
    link = link.strip()
    # Ignore mailto, tel, javascript, data
    if re.match(r"^(mailto|tel|javascript|data|sms):", link, re.IGNORECASE):
        return ""
    joined = urljoin(base_url, link)
    return normalize_url(joined, remove_fragments=True)


def is_valid_http_url(url: str) -> bool:
    """Check whether string is a valid HTTP/HTTPS URL."""
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False
