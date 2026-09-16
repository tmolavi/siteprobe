# SiteProbe Checks Catalog

| Check ID | Category | Default Severity | Auto-Fixable | Description |
| :--- | :--- | :--- | :---: | :--- |
| `technical.status.http_4xx` | Technical SEO | High | No | Client error HTTP status (400-499) |
| `technical.status.http_5xx` | Technical SEO | Critical | No | Server error HTTP status (500-599) |
| `technical.canonical.missing` | Technical SEO | High | Yes | Missing `<link rel="canonical">` |
| `technical.canonical.mismatch` | Technical SEO | Medium | No | Canonical points away from current URL |
| `technical.redirect.chain` | Technical SEO | Medium | Yes | Chained redirects (> 1 hop) |
| `technical.links.broken_internal`| Technical SEO | High | Yes | Hyperlink pointing to internal 4xx page |
| `technical.robots.missing` | Technical SEO | High | Yes | Root robots.txt missing |
| `technical.sitemap.missing` | Technical SEO | High | Yes | XML sitemap missing or undeclared |
| `technical.security.insecure_http`| Security | Critical | No | Page served over plain HTTP |
| `technical.security.missing_hsts` | Security | Medium | No | Missing Strict-Transport-Security header |
| `onpage.title.missing` | On-Page SEO | Critical | Yes | Missing `<title>` tag |
| `onpage.title.too_long` | On-Page SEO | Medium | No | Title exceeds 60 characters |
| `onpage.title.duplicate` | On-Page SEO | High | No | Identical title found across multiple pages |
| `onpage.description.missing` | On-Page SEO | High | Yes | Missing meta description |
| `onpage.h1.missing` | On-Page SEO | High | Yes | Missing `<h1>` heading tag |
| `onpage.h1.multiple` | On-Page SEO | Medium | No | More than one `<h1>` heading tag |
| `onpage.images.missing_alt` | On-Page SEO | High | Yes | Missing image `alt` attribute |
| `geo.ai_bots.blocked` | GEO / AEO | High | Yes | OAI-SearchBot or PerplexityBot blocked in robots.txt |
| `geo.llms_txt.missing` | GEO / AEO | Medium | Yes | Root `/llms.txt` missing |
| `geo.structure.missing_faq_schema`| GEO / AEO | Low | Yes | Question headings present without FAQPage schema |
| `schema.jsonld.syntax_error` | Schema.org | High | Yes | Malformed JSON-LD script |
| `accessibility.html.missing_lang`| Accessibility | High | Yes | Missing or empty `lang` attribute on `<html>` |
| `accessibility.form.unlabeled_input`| Accessibility | High | Yes | Form input without label or aria-label |
| `ux.viewport.missing` | Mobile UX | High | Yes | Missing `<meta name="viewport">` |
