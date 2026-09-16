import re
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from siteprobe.checks.base import BaseCheck
from siteprobe.models.finding import Finding, FindingCategory, RiskClass, Severity
from siteprobe.models.crawl import CrawlPage


class GeoAeoCheck(BaseCheck):
    id = "geo.ai_search"
    category = FindingCategory.GEO_AEO
    name = "Generative Engine Optimization (GEO/AEO) & AI Readiness"
    description = "Evaluates AI search crawler permissions, /llms.txt availability, QA structures, entity clarity, and citations."

    def run(self, page: CrawlPage, all_pages: List[CrawlPage], context: Dict[str, Any]) -> List[Finding]:
        findings = []

        # Run site-level checks on the homepage
        if page.depth == 0:
            robots = context.get("robots")
            if robots:
                ai_status = robots.get_ai_crawler_status()
                blocked_search_bots = []
                for bot_name in ["OAI-SearchBot", "PerplexityBot", "ClaudeBot"]:
                    if bot_name in ai_status and not ai_status[bot_name]["allowed"]:
                        blocked_search_bots.append(bot_name)

                if blocked_search_bots:
                    findings.append(Finding(
                        id="geo.ai_bots.blocked",
                        category=self.category,
                        severity=Severity.HIGH,
                        confidence=1.0,
                        url=page.url,
                        title=f"AI search retrieval crawlers blocked: {', '.join(blocked_search_bots)}",
                        evidence={"blocked_bots": blocked_search_bots, "status": ai_status},
                        why_it_matters="Blocking AI retrieval bots prevents your site from being cited as an authoritative source in ChatGPT, Perplexity, or Claude answers.",
                        recommended_action="Allow OAI-SearchBot and PerplexityBot in robots.txt while optionally disallowing general scraping bots (e.g. CCBot).",
                        auto_fixable=True,
                        risk_class=RiskClass.SAFE_AUTOFIX,
                        required_capability="source_code",
                        verification_check="geo.ai_search",
                    ))

            # Check llms.txt
            has_llms_txt = context.get("has_llms_txt", False)
            if not has_llms_txt:
                findings.append(Finding(
                    id="geo.llms_txt.missing",
                    category=self.category,
                    severity=Severity.MEDIUM,
                    confidence=0.95,
                    url=page.url,
                    title="Missing /llms.txt file for AI agent navigation",
                    evidence={"path_checked": "/llms.txt"},
                    why_it_matters="/llms.txt is an emerging web standard that provides LLM crawlers with a clean markdown index of high-value documentation and site capabilities.",
                    recommended_action="Generate a /llms.txt markdown file at the root domain listing key pages and summaries.",
                    auto_fixable=True,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    required_capability="source_code",
                    verification_check="geo.ai_search",
                ))

        # Page-level semantic readiness
        if page.status_code == 200 and page.html:
            soup = BeautifulSoup(page.html, "html.parser")
            h2_texts = [h["text"] for h in page.headings if h["level"] in ("h2", "h3")]
            question_headings = [t for t in h2_texts if any(q in t.lower() for q in ["what", "how", "why", "when", "where", "who", "چیست", "چگونه", "nedir", "nasıl", "?"])]

            # Check FAQ schema vs question headings
            if len(question_headings) >= 2 and "faqpage" not in [t.lower() for t in page.schema_types]:
                findings.append(Finding(
                    id="geo.structure.missing_faq_schema",
                    category=self.category,
                    severity=Severity.LOW,
                    confidence=0.88,
                    url=page.url,
                    title="Question-based content found without FAQPage schema",
                    evidence={"question_headings": question_headings[:4]},
                    why_it_matters="Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.",
                    recommended_action="Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.",
                    auto_fixable=True,
                    risk_class=RiskClass.SAFE_AUTOFIX,
                    required_capability="source_code",
                    verification_check="geo.ai_search",
                ))

            # Entity and author attribution check for content pages
            text_len = len(soup.get_text())
            if text_len > 1200 and page.depth > 0:
                has_author = bool(soup.find(attrs={"rel": re.compile(r"^author$", re.I)})) or bool(soup.find(class_=re.compile(r"author|byline", re.I))) or any("person" in t.lower() for t in page.schema_types)
                if not has_author:
                    findings.append(Finding(
                        id="geo.entity.missing_author",
                        category=self.category,
                        severity=Severity.LOW,
                        confidence=0.80,
                        url=page.url,
                        title="Long-form content lacking author attribution or Person schema",
                        evidence={"url": page.url},
                        why_it_matters="AI ranking models prioritize verifiable authoritative sources with clear human or organizational authorship.",
                        recommended_action="Add author byline markup and Person/Author structured data.",
                        auto_fixable=False,
                        risk_class=RiskClass.REVIEW_RECOMMENDED,
                        required_capability="source_code",
                        verification_check="geo.ai_search",
                    ))

        return findings
