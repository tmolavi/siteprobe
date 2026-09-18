# SiteProbe Audit Report: https://molavi.pro
> **Audit Date**: 2026-09-16T16:45:39.445553+00:00 | **Language**: `fa`

## 📊 Executive Summary

- **Overall Quality Score**: **68 / 100**
- **GEO / AI Search Readiness**: **50 / 100**
- **Total Pages Crawled**: 50
- **Crawl Duration**: 97.76s
- **Broken Links**: 0

### Category Breakdown
| Category | Score | Critical | High | Medium | Low |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Technical Seo | 100 | 0 | 0 | 0 | 0 |
| Onpage Seo | 78 | 0 | 2 | 0 | 1 |
| Schema Org | 95 | 0 | 0 | 1 | 0 |
| Geo Aeo | 50 | 0 | 0 | 1 | 30 |
| Performance | 0 | 0 | 45 | 2 | 0 |
| Accessibility | 40 | 0 | 6 | 0 | 0 |
| Security | 0 | 0 | 0 | 50 | 50 |
| Content Quality | 95 | 0 | 0 | 1 | 0 |
| Ux | 100 | 0 | 0 | 0 | 0 |

### 🤖 GEO / AI-Search Readiness Pillars
- **AI Crawler Access**: 40 / 40
- **/llms.txt Availability**: 0 / 20
- **Entity & Authorship Clarity**: 10 / 20
- **QA & Semantic Structures**: 0 / 20

---
## 🚨 Prioritized Findings

### **[HIGH]** Slow Time to First Byte (9346 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 9346}`

### **[HIGH]** Slow Time to First Byte (8962 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/digital-pr-ai-elecomp-1405`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 8962}`

### **[HIGH]** فیلد فرم فاقد برچسب (Label) مرتبط است (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/digital-pr-ai-elecomp-1405`
- **Rule ID**: `accessibility.form.unlabeled_input`
- **Why It Matters**: کاربران ابزارهای کمکی نمی‌توانند کاربرد فیلدهای بدون برچسب را تشخیص دهند.
- **Recommended Fix**: تگ <label for="..."> مرتبط یا ویژگی aria-label را به فیلد ورودی اضافه کنید.
- **Evidence**: `{'snippets': ['<input autocomplete="off" name="company" tabindex="-1"/>', '<input aria-hidden="true" class="hidden" name="phone" tabindex="-1"/>', '<input aria-hidden="true" class="hidden" name="website" tabindex="-1"/>'], 'count': 3}`

### **[HIGH]** Missing reciprocal hreflang return link on https://molavi.pro/tr/proof (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/proof`
- **Rule ID**: `onpage.hreflang.missing_return_link`
- **Why It Matters**: Google ignores hreflang annotations if the target page does not link back with a matching hreflang tag.
- **Recommended Fix**: Add reciprocal hreflang annotation on https://molavi.pro/tr/proof referencing https://molavi.pro/proof.
- **Evidence**: `{'source': 'https://molavi.pro/proof', 'target': 'https://molavi.pro/tr/proof', 'declared_lang': 'tr'}`

### **[HIGH]** Slow Time to First Byte (22629 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/proof`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 22629}`

### **[HIGH]** Slow Time to First Byte (22817 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/contact`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 22817}`

### **[HIGH]** Missing reciprocal hreflang return link on https://molavi.pro/tr/research (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/research`
- **Rule ID**: `onpage.hreflang.missing_return_link`
- **Why It Matters**: Google ignores hreflang annotations if the target page does not link back with a matching hreflang tag.
- **Recommended Fix**: Add reciprocal hreflang annotation on https://molavi.pro/tr/research referencing https://molavi.pro/research.
- **Evidence**: `{'source': 'https://molavi.pro/research', 'target': 'https://molavi.pro/tr/research', 'declared_lang': 'tr'}`

### **[HIGH]** Slow Time to First Byte (22836 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 22836}`

### **[HIGH]** Slow Time to First Byte (4289 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/first-websites-to-ai-visibility`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 4289}`

### **[HIGH]** فیلد فرم فاقد برچسب (Label) مرتبط است (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/first-websites-to-ai-visibility`
- **Rule ID**: `accessibility.form.unlabeled_input`
- **Why It Matters**: کاربران ابزارهای کمکی نمی‌توانند کاربرد فیلدهای بدون برچسب را تشخیص دهند.
- **Recommended Fix**: تگ <label for="..."> مرتبط یا ویژگی aria-label را به فیلد ورودی اضافه کنید.
- **Evidence**: `{'snippets': ['<input aria-hidden="true" autocomplete="off" class="sr-only" name="website" tabindex="-1" value=""/>', '<input class="rounded-md border border-white/10 bg-[#02090f] px-3 py-3 text-sm text-white outline-no', '<input class="rounded-md border border-white/10 bg-[#02090f] px-3 py-3 text-sm text-white outline-no'], 'count': 3}`

### **[HIGH]** Slow Time to First Byte (27555 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 27555}`

### **[HIGH]** Slow Time to First Byte (5173 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-seo`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 5173}`

### **[HIGH]** Slow Time to First Byte (4945 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-geo`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 4945}`

### **[HIGH]** Slow Time to First Byte (5017 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-aeo`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 5017}`

### **[HIGH]** Slow Time to First Byte (7447 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/healthcare-ai-visibility-digital-trust`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 7447}`

### **[HIGH]** Slow Time to First Byte (2878 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/next-layer`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 2878}`

### **[HIGH]** Slow Time to First Byte (2930 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-project-roi`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 2930}`

### **[HIGH]** Slow Time to First Byte (3343 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-ai-visibility`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 3343}`

### **[HIGH]** Slow Time to First Byte (3031 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/ai-visibility-services`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 3031}`

### **[HIGH]** Slow Time to First Byte (2490 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/network-civilization`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 2490}`

### **[HIGH]** Slow Time to First Byte (2424 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-is-not-the-new-seo`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 2424}`

### **[HIGH]** Slow Time to First Byte (3419 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/founder-personality-seo-ai-visibility`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 3419}`

### **[HIGH]** Slow Time to First Byte (3480 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/search-engineering-semantic-seo-ai`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 3480}`

### **[HIGH]** Slow Time to First Byte (2861 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/default-answer-search-visibility`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 2861}`

### **[HIGH]** Slow Time to First Byte (2752 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/ai-seo-brand-visibility`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 2752}`

### **[HIGH]** Slow Time to First Byte (2937 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/measuring-ai-visibility`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 2937}`

### **[HIGH]** Slow Time to First Byte (4743 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/simplify-before-you-automate`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 4743}`

### **[HIGH]** فیلد فرم فاقد برچسب (Label) مرتبط است (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/simplify-before-you-automate`
- **Rule ID**: `accessibility.form.unlabeled_input`
- **Why It Matters**: کاربران ابزارهای کمکی نمی‌توانند کاربرد فیلدهای بدون برچسب را تشخیص دهند.
- **Recommended Fix**: تگ <label for="..."> مرتبط یا ویژگی aria-label را به فیلد ورودی اضافه کنید.
- **Evidence**: `{'snippets': ['<input aria-hidden="true" autocomplete="off" class="sr-only" name="website" tabindex="-1" value=""/>', '<input class="rounded-md border border-white/10 bg-[#02090f] px-3 py-3 text-sm text-white outline-no', '<input class="rounded-md border border-white/10 bg-[#02090f] px-3 py-3 text-sm text-white outline-no'], 'count': 3}`

### **[HIGH]** Slow Time to First Byte (2071 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-scope-ai-visibility-benchmark`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 2071}`

### **[HIGH]** فیلد فرم فاقد برچسب (Label) مرتبط است (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/geo-scope-ai-visibility-benchmark`
- **Rule ID**: `accessibility.form.unlabeled_input`
- **Why It Matters**: کاربران ابزارهای کمکی نمی‌توانند کاربرد فیلدهای بدون برچسب را تشخیص دهند.
- **Recommended Fix**: تگ <label for="..."> مرتبط یا ویژگی aria-label را به فیلد ورودی اضافه کنید.
- **Evidence**: `{'snippets': ['<input aria-hidden="true" autocomplete="off" class="sr-only" name="website" tabindex="-1" value=""/>', '<input class="rounded-md border border-white/10 bg-[#02090f] px-3 py-3 text-sm text-white outline-no', '<input class="rounded-md border border-white/10 bg-[#02090f] px-3 py-3 text-sm text-white outline-no'], 'count': 3}`

### **[HIGH]** Slow Time to First Byte (2093 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/why-brands-ignored-in-ai-answers`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 2093}`

### **[HIGH]** فیلد فرم فاقد برچسب (Label) مرتبط است (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/why-brands-ignored-in-ai-answers`
- **Rule ID**: `accessibility.form.unlabeled_input`
- **Why It Matters**: کاربران ابزارهای کمکی نمی‌توانند کاربرد فیلدهای بدون برچسب را تشخیص دهند.
- **Recommended Fix**: تگ <label for="..."> مرتبط یا ویژگی aria-label را به فیلد ورودی اضافه کنید.
- **Evidence**: `{'snippets': ['<input aria-hidden="true" autocomplete="off" class="sr-only" name="website" tabindex="-1" value=""/>', '<input class="rounded-md border border-white/10 bg-[#02090f] px-3 py-3 text-sm text-white outline-no', '<input class="rounded-md border border-white/10 bg-[#02090f] px-3 py-3 text-sm text-white outline-no'], 'count': 3}`

### **[HIGH]** Slow Time to First Byte (9309 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/media-age-ai`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 9309}`

### **[HIGH]** Slow Time to First Byte (8583 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/n8n-agent-skills-verifiable-automation`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 8583}`

### **[HIGH]** Slow Time to First Byte (8675 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/enterprise-seo-geo-architecture`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 8675}`

### **[HIGH]** Slow Time to First Byte (12315 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/mcp-agent-skills-hub-curation`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 12315}`

### **[HIGH]** Slow Time to First Byte (3882 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/mcp-geo-server-rag-readiness`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 3882}`

### **[HIGH]** Slow Time to First Byte (3908 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-scope-reproducible-benchmark`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 3908}`

### **[HIGH]** Slow Time to First Byte (18471 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/local-geo-iran-complete-guide`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 18471}`

### **[HIGH]** Slow Time to First Byte (20528 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/seo-ai-search-news-august-2026`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 20528}`

### **[HIGH]** فیلد فرم فاقد برچسب (Label) مرتبط است (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/seo-ai-search-news-august-2026`
- **Rule ID**: `accessibility.form.unlabeled_input`
- **Why It Matters**: کاربران ابزارهای کمکی نمی‌توانند کاربرد فیلدهای بدون برچسب را تشخیص دهند.
- **Recommended Fix**: تگ <label for="..."> مرتبط یا ویژگی aria-label را به فیلد ورودی اضافه کنید.
- **Evidence**: `{'snippets': ['<input aria-hidden="true" autocomplete="off" class="sr-only" name="website" tabindex="-1" value=""/>', '<input class="rounded-md border border-white/10 bg-[#02090f] px-3 py-3 text-sm text-white outline-no', '<input class="rounded-md border border-white/10 bg-[#02090f] px-3 py-3 text-sm text-white outline-no'], 'count': 3}`

### **[HIGH]** Slow Time to First Byte (5834 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/laravel-ai-summary-provider-architecture`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 5834}`

### **[HIGH]** Slow Time to First Byte (6137 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/sage-audit-three-pillars`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 6137}`

### **[HIGH]** Slow Time to First Byte (5883 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/agent-project-discovery-before-editing`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 5883}`

### **[HIGH]** Slow Time to First Byte (3737 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/sage-audit-open-source-engine`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 3737}`

### **[HIGH]** Slow Time to First Byte (3808 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/vpa-rag-semantic-entropy`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 3808}`

### **[HIGH]** Slow Time to First Byte (3821 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/answerpath-geo-question-mining`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 3821}`

### **[HIGH]** Slow Time to First Byte (4117 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/awesome-skills-directory-evaluation`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 4117}`

### **[HIGH]** Slow Time to First Byte (4150 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/lean-agent-skills-context-efficiency`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 4150}`

### **[HIGH]** Slow Time to First Byte (11865 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/digital-twin-what-is`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 11865}`

### **[HIGH]** Slow Time to First Byte (11893 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/tr`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 11893}`

### **[HIGH]** Slow Time to First Byte (12024 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/geo-pyramid`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 12024}`

### **[HIGH]** Slow Time to First Byte (12013 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/tr/notes`
- **Rule ID**: `performance.ttfb.slow`
- **Why It Matters**: High TTFB directly harms Core Web Vitals (LCP) and causes user abandonment on mobile connections.
- **Recommended Fix**: Enable server-side page caching, use a CDN, or optimize backend database queries.
- **Evidence**: `{'response_time_ms': 12013}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** Missing Organization or WebSite schema on homepage (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/`
- **Rule ID**: `schema.entity.missing_organization`
- **Why It Matters**: Organization schema establishes authoritative brand identity, official logos, and social proof in Google Knowledge Graph.
- **Recommended Fix**: Inject an 'Organization' schema.org JSON-LD snippet with name, url, logo, and sameAs links.
- **Evidence**: `{'schema_types_found': []}`

### **[MEDIUM]** فایل llms.txt موجود نیست (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/`
- **Rule ID**: `geo.llms_txt.missing`
- **Why It Matters**: فایل llms.txt خلاصه‌ای بهینه برای خزنده‌ها و مدل‌های هوش مصنوعی فراهم می‌سازد.
- **Recommended Fix**: یک فایل استاندارد /llms.txt حاوی معرفی هویت و اسناد کلیدی سایت ایجاد کنید.
- **Evidence**: `{'path_checked': '/llms.txt'}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/digital-pr-ai-elecomp-1405`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/proof`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/contact`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** Thin content detected (89 words) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/contact`
- **Rule ID**: `content.quality.thin_content`
- **Why It Matters**: Pages with little substantive content struggle to rank and risk being classified as low-quality by search algorithms.
- **Recommended Fix**: Enrich the page with comprehensive, helpful content addressing user intent.
- **Evidence**: `{'word_count': 89}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/first-websites-to-ai-visibility`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-seo`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-geo`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-aeo`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/healthcare-ai-visibility-digital-trust`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/next-layer`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-project-roi`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-ai-visibility`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/ai-visibility-services`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/network-civilization`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-is-not-the-new-seo`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/founder-personality-seo-ai-visibility`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/search-engineering-semantic-seo-ai`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/evidence-architecture-for-ai`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** Moderate server response latency (1027 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/evidence-architecture-for-ai`
- **Rule ID**: `performance.ttfb.moderate`
- **Why It Matters**: Google recommends server response times under 200ms for optimal Core Web Vitals.
- **Recommended Fix**: Review caching layers and edge delivery configurations.
- **Evidence**: `{'response_time_ms': 1027}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/ai-experts-research`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** Moderate server response latency (1084 ms) (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/ai-experts-research`
- **Rule ID**: `performance.ttfb.moderate`
- **Why It Matters**: Google recommends server response times under 200ms for optimal Core Web Vitals.
- **Recommended Fix**: Review caching layers and edge delivery configurations.
- **Evidence**: `{'response_time_ms': 1084}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/default-answer-search-visibility`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/ai-seo-brand-visibility`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/measuring-ai-visibility`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/simplify-before-you-automate`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-scope-ai-visibility-benchmark`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/why-brands-ignored-in-ai-answers`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/media-age-ai`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/n8n-agent-skills-verifiable-automation`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/enterprise-seo-geo-architecture`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/mcp-agent-skills-hub-curation`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/mcp-geo-server-rag-readiness`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-scope-reproducible-benchmark`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/local-geo-iran-complete-guide`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/seo-ai-search-news-august-2026`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/laravel-ai-summary-provider-architecture`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/sage-audit-three-pillars`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/agent-project-discovery-before-editing`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/sage-audit-open-source-engine`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/vpa-rag-semantic-entropy`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/answerpath-geo-question-mining`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/awesome-skills-directory-evaluation`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/lean-agent-skills-context-efficiency`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/digital-twin-what-is`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/tr`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/geo-pyramid`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'x-middleware-rewrite', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/tr/notes`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': ['server', 'date', 'content-type', 'transfer-encoding', 'connection', 'content-language', 'vary', 'link', 'x-powered-by', 'cache-control', 'content-encoding']}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/geo-methods-and-techniques`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': []}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/tr/research`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': []}`

### **[MEDIUM]** هدر Strict-Transport-Security (HSTS) موجود نیست (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/tr/proof`
- **Rule ID**: `technical.security.missing_hsts`
- **Why It Matters**: پروتکل HSTS ارتباط امن HTTPS را اجباری کرده و از حملات مرد میانی محافظت می‌کند.
- **Recommended Fix**: وب‌سرور را برای ارسال هدر HSTS با max-age معتبر پیکربندی کنید.
- **Evidence**: `{'headers_checked': []}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['What Is a Digital Twin? Architecture and Uses', 'How to Curate MCP Agent Skills for Reliable AI Work']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/digital-pr-ai-elecomp-1405`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/proof`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/proof`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['What this page is for', 'Why this matters to a business', 'Why open source?', 'If you do not know how your brand appears in AI answers, start here.']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/contact`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Heading level skipped from H1 directly to H4 (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/contact`
- **Rule ID**: `onpage.headings.skipped_level`
- **Why It Matters**: Skipping heading levels violates semantic document outlines and degrades accessibility.
- **Recommended Fix**: Restructure heading tags to follow an incremental hierarchical order without skipping levels.
- **Evidence**: `{'previous_level': 'H1', 'next_level': 'H4'}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/first-websites-to-ai-visibility`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/first-websites-to-ai-visibility`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why Good Brands Still Disappear', 'What I Focus On Today']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['How to Curate MCP Agent Skills for Reliable AI Work', 'Why Coding Agents Need Project Discovery Before They Edit', 'How to Evaluate an AI Coding-Agent Skills Directory', 'Why Are Some Brands Missing from AI Answers?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-seo`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-geo`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/what-is-geo`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Can GEO Work Without a Website?', 'Why SEO Is the Prerequisite']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-aeo`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/what-is-aeo`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['What AEO Actually Means', 'Why SEO Comes Before AEO']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/healthcare-ai-visibility-digital-trust`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/healthcare-ai-visibility-digital-trust`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Is SEO becoming obsolete?', 'Should healthcare organizations stop investing in content marketing?', 'Does AI replace Google Search?', 'What is the biggest competitive advantage in the AI era?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/next-layer`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-project-roi`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/what-is-ai-visibility`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/what-is-ai-visibility`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why SEO, AEO, and GEO Work Together', 'Why One Strategist Can Own This']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/ai-visibility-services`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/ai-visibility-services`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['What AI Visibility Really Means', 'Why This Is Not Separate From SEO and GEO']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/network-civilization`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-is-not-the-new-seo`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/geo-is-not-the-new-seo`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['What to build', 'Is GEO an official Google ranking factor?', 'Can a brand have GEO visibility without a website?', 'What should be measured first?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/founder-personality-seo-ai-visibility`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/founder-personality-seo-ai-visibility`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['When a strength becomes authority', 'How the same strength creates SEO problems', 'A personal brand is what the web infers', 'Does this page add experience or only repeat a definition?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/search-engineering-semantic-seo-ai`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/search-engineering-semantic-seo-ai`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why raw mass content is dangerous', 'Where SEO meets software engineering', 'Why agile teams can outperform large organizations']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/evidence-architecture-for-ai`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/ai-experts-research`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/ai-experts-research`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['What to record', 'What the study can—and cannot—show']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/default-answer-search-visibility`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/ai-seo-brand-visibility`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/ai-seo-brand-visibility`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why do some brands appear more often?', 'What can we learn from familiar brands?', 'Zara: people have a clear idea of what it is', 'What should your brand do?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/measuring-ai-visibility`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/simplify-before-you-automate`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-scope-ai-visibility-benchmark`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/geo-scope-ai-visibility-benchmark`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['What is GEO-Scope, in plain English?', 'What does it measure?', 'Why should a business care?', 'How do you try it?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/why-brands-ignored-in-ai-answers`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/why-brands-ignored-in-ai-answers`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['What the six research charts suggest', '6. A five-layer funnel for testing where a brand disappears', 'How to read the numbers in this research', 'How to test whether your brand is actually overlooked']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/media-age-ai`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/n8n-agent-skills-verifiable-automation`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/n8n-agent-skills-verifiable-automation`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['2. Real experience: why I built n8n Agent Skills', 'Does n8n Agent Skills make an AI agent reliable by itself?', 'Why is a green n8n execution insufficient?', 'What should builders measure first?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/enterprise-seo-geo-architecture`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/mcp-agent-skills-hub-curation`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/mcp-agent-skills-hub-curation`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why does this matter to the industry?', 'Why the problem exists', 'What problem does this project solve?', 'Is its output a performance guarantee?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/mcp-geo-server-rag-readiness`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/mcp-geo-server-rag-readiness`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why does this matter to the industry?', 'Why the problem exists', 'What problem does this project solve?', 'Is its output a performance guarantee?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/geo-scope-reproducible-benchmark`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/geo-scope-reproducible-benchmark`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why does this matter to the industry?', 'Why the problem exists', 'What problem does this project solve?', 'Is its output a performance guarantee?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/local-geo-iran-complete-guide`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/local-geo-iran-complete-guide`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['What is Local GEO?', 'Why every market needs a localized playbook', 'What not to do', 'Does Local GEO replace SEO?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/seo-ai-search-news-august-2026`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/seo-ai-search-news-august-2026`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['What is confirmed, and what is still a report?', 'What the August numbers can and cannot tell us', 'Does an AI impression mean that my site received a visitor?', 'Should I rewrite every article for AI Overviews?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/laravel-ai-summary-provider-architecture`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/laravel-ai-summary-provider-architecture`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why does this matter to the industry?', 'Why the problem exists', 'What problem does this project solve?', 'Is its output a performance guarantee?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/sage-audit-three-pillars`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/sage-audit-three-pillars`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why does this matter to the industry?', 'Why the problem exists', 'What problem does this project solve?', 'Is its output a performance guarantee?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/agent-project-discovery-before-editing`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/agent-project-discovery-before-editing`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why does this matter to the industry?', 'Why the problem exists', 'What problem does this project solve?', 'Is its output a performance guarantee?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/sage-audit-open-source-engine`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/vpa-rag-semantic-entropy`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/answerpath-geo-question-mining`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/answerpath-geo-question-mining`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why does this matter to the industry?', 'Why the problem exists', 'Does AnswerPath reveal what everyone asks?', 'Is it a keyword tool?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/awesome-skills-directory-evaluation`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/awesome-skills-directory-evaluation`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why does this matter to the industry?', 'Why the problem exists', 'What problem does this project solve?', 'Is its output a performance guarantee?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/notes/lean-agent-skills-context-efficiency`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/notes/lean-agent-skills-context-efficiency`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Why does this matter to the industry?', 'Why the problem exists', 'What problem does this project solve?', 'Is its output a performance guarantee?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/digital-twin-what-is`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/research/digital-twin-what-is`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['How a digital twin works', 'What I learned while building Hamzad', 'Does a digital twin need sensors?', 'Is a 3D model a digital twin?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/tr`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/geo-pyramid`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/tr/notes`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** Question-based content found without FAQPage schema (⚡ `AUTO-FIXABLE`)
- **URL**: `https://molavi.pro/tr/notes`
- **Rule ID**: `geo.structure.missing_faq_schema`
- **Why It Matters**: Structuring conversational question-and-answer sections with FAQPage schema boosts eligibility for AI answer snippets.
- **Recommended Fix**: Add FAQPage schema.org JSON-LD to clearly demarcate Questions and Answers.
- **Evidence**: `{'question_headings': ['Kodlama Ajanları Düzenlemeden Önce Projeyi Neden Keşfetmeli?', 'AI Coding Agent Skill Dizini Nasıl Değerlendirilir?', 'Bazı Markalar Yapay Zeka Yanıtlarında Neden Yer Almaz?', 'Kurucu Kişiliği SEO ve Yapay Zekayı Nasıl Etkiler?']}`

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/research/geo-methods-and-techniques`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/tr/research`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

### **[LOW]** X-Content-Type-Options header missing (🛠️ `MANUAL`)
- **URL**: `https://molavi.pro/tr/proof`
- **Rule ID**: `technical.security.missing_xcto`
- **Why It Matters**: Prevents MIME-sniffing vulnerabilities where browsers interpret non-executable files as executable.
- **Recommended Fix**: Add header: 'X-Content-Type-Options: nosniff'.

---
## 🔌 Enriched Audit Capabilities (Missing Integrations)

### Google Search Console
- **Impact**: Identifies high-impression queries with weak CTR, tracks ranking drops, and validates Google indexing coverage.
- **How to Enable**: Set GOOGLE_APPLICATION_CREDENTIALS or ask user to authenticate via browser session.

### Google Analytics 4 (GA4)
- **Impact**: Connects technical crawl defects directly to user drop-offs and lost conversions.
- **How to Enable**: Configure GA4_PROPERTY_ID and OAuth service account credentials.

### Google Lighthouse / Chrome
- **Impact**: Provides granular rendering waterfall insights beyond server TTFB.
- **How to Enable**: Install Node.js and Chrome, or pass --lighthouse CLI flag.

### Playwright Browser Session
- **Impact**: Enables auditing JavaScript-only single page apps (React/Vue/Angular) and visual overflow verification.
- **How to Enable**: Run 'pip install siteprobe[browser] && playwright install chromium'.

---
*Generated autonomously by [SiteProbe](https://github.com/tmolavi/siteprobe).*