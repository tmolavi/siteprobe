# Security Policy

## Reporting Security Vulnerabilities

If you discover a potential security vulnerability in SiteProbe, please do not file a public issue. Instead, report it privately to:

**Taqi Molavi**  
Email: [taqimolavi@gmail.com](mailto:taqimolavi@gmail.com)

We will acknowledge receipt of your vulnerability report within 48 hours and provide a timeline for remediation.

## Untrusted Input & Prompt Injection Defense

SiteProbe crawls external and potentially hostile websites. All crawled HTML, HTTP headers, and URL query strings are treated as **untrusted data**. SiteProbe implements:
1. Automated credential and authorization header redaction in all exported reports.
2. Sanitization filters to protect AI agents against prompt-injection directives hidden in crawled HTML text.
3. No execution of arbitrary JavaScript or executable binaries fetched during audits.
