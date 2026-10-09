# September 2026 Google Spam Update: Impact Triage Methodology

## Executive Summary

On **September 24, 2026**, Google began rolling out a global Spam Update, officially concluding rollout on **October 8, 2026**.

Website operators observing traffic fluctuations during this period face a critical diagnostic challenge: distinguishing genuine algorithmic shifts from internal technical site malfunctions, seasonal macro-shifts, tracking failures, and manual actions.

SiteProbe provides an evidence-based, reproducible triage utility designed to evaluate Search Console performance without over-interpreting data or making unsupported causal claims.

> [!NOTE]
> **Permitted Public Claim**:
> *"SiteProbe provides a reproducible workflow for examining Search Console changes around Google's September 2026 spam update."*
>
> **Forbidden Public Claims**:
> - ❌ *"SiteProbe detects Google penalties."*
> - ❌ *"SiteProbe identifies SpamBrain violations."*
> - ❌ *"SiteProbe proves the update caused a traffic loss."*

---

## 1. Official Rollout Timeline & Frozen Comparison Windows

To conduct sound statistical comparisons, timelines must control for day-of-week traffic variance. Comparing arbitrary date ranges introduces weekend vs. weekday bias.

SiteProbe establishes **four frozen windows**:

```
 2026-09-10                2026-09-24          2026-10-08  2026-10-09                2026-10-22
[------- PRE (14d) -------][-- ROLLOUT (14d) --][COMPL(1d)][------- POST (14d) ------]
  Thu Sep 10 - Wed Sep 23    Thu Sep 24 - Wed Oct 7   Thu Oct 8   Thu Oct 9 - Wed Oct 22 (Incomplete)
```

1. **PRE Window (`2026-09-10` to `2026-09-23`)**:
   - Exactly **14 days**.
   - Runs Thursday through Wednesday.
   - Represents the unperturbed baseline period immediately preceding the rollout.
2. **ROLLOUT Window (`2026-09-24` to `2026-10-07`)**:
   - Exactly **14 days**.
   - Runs Thursday through Wednesday.
   - Perfectly matched weekday composition with the PRE window (2 Thursdays, 2 Fridays, 2 Saturdays, etc.).
3. **COMPLETION Day (`2026-10-08`)**:
   - Exactly **1 day** (Thursday).
   - Google announced the completion of the rollout on this date.
   - Evaluated as an independent milestone rather than bundled into the 14-day comparison to preserve day-of-week symmetry.
4. **POST Window (`2026-10-09` to `2026-10-22`)**:
   - Exactly **14 days** scheduled.
   - **Current status: Incomplete**. As of October 9, 2026, the post-rollout observation period has only begun.
   - **Methodological constraint**: Incomplete windows are never compared against 14-day complete baselines. Missing future observations are never synthesized or extrapolated.

---

## 2. Data Requirements & Validation

SiteProbe accepts an optional Google Search Console CSV export or connects to the Search Console API when configured.

### Required CSV Columns
- `date`: Chronological date in `YYYY-MM-DD` format.
- `clicks`: Non-negative integer (`>= 0`).
- `impressions`: Non-negative integer (`>= 0`).

### Optional Dimensions
- `query`: Keyword query string.
- `page`: Landing page URL.
- `device`: Device category (`desktop`, `mobile`, `tablet`).
- `country`: Country identifier.
- `position`: Average position rank (`>= 1.0`).
- `ctr`: Click-through rate (`0.0 <= ctr <= 1.0` or `0%` to `100%`).

### Integrity & Validation Rules
1. **Zero Fake Data**: SiteProbe never generates simulated or synthetic Search Console rows when live data is missing. If neither credentials nor a user-provided CSV is supplied, it returns `status="DATA_UNAVAILABLE"`.
2. **Duplicate Detection**: Duplicate rows across dimension composite keys are flagged as validation errors.
3. **Mathematical Consistency**: Clicks cannot exceed impressions. Rows where `clicks > impressions` or `impressions == 0 and clicks > 0` fail validation.
4. **Aggregate CTR Calculation**: SiteProbe calculates CTR as:
   $$\text{CTR}_{\text{window}} = \frac{\sum \text{Clicks}}{\sum \text{Impressions}}$$
   SiteProbe **never averages individual daily CTR percentages**, which would introduce significant weighting errors.
5. **Position Shifts & Query Composition**: Average position cannot be evaluated in isolation. A loss of low-ranking long-tail impressions can paradoxically *improve* average position, while acquiring high impressions on positions 8–10 can *depress* average position without any ranking loss.

---

## 3. Diagnostic Classifications

SiteProbe outputs one of five empirical observations:

| Diagnostic | Trigger Criteria |
| :--- | :--- |
| `NO_MEANINGFUL_CHANGE_OBSERVED` | Comparison windows complete; performance shift within normal variance (±15%); no blocking technical or manual issues. |
| `PERFORMANCE_CHANGE_OBSERVED` | Significant decline or gain (≥15% clicks or impressions) during rollout window; no manual action and no blocking technical errors found. Represents potential update correlation. |
| `TECHNICAL_ISSUE_OBSERVED` | Deterministic site errors identified (HTTP 5xx/4xx, sitewide noindex, robots.txt crawl blocks, canonical conflicts, redirect loops, empty SPA client shells). |
| `MANUAL_ACTION_REPORTED` | Google Search Console explicitly confirms a manual penalty issued by human webspam reviewers. Never inferred from traffic changes. |
| `INSUFFICIENT_DATA` | Search Console data missing, PRE or ROLLOUT windows missing dates (<14 days), or zero total impressions recorded. |

---

## 4. Technical Audit Integration

Before attributing traffic declines to an algorithm update, SiteProbe leverages its existing crawler and deterministic checks:

- **HTTP Status (`technical.status`)**: Identifies 5xx server downtime or 4xx client errors.
- **Robots Directives (`technical.robots_sitemap`)**: Flags unintended `Disallow` rules blocking search engine bots.
- **Indexability (`extract_page_data`)**: Flags meta robots `noindex` or `X-Robots-Tag: noindex`.
- **Canonical Health (`technical.canonical`)**: Detects missing canonicals or accidental canonical loops pointing off-site.
- **Redirects (`technical.redirects`)**: Identifies broken redirect hops or cyclic chains.
- **Server-Side Rendering (`technical.ssr`)**: Detects empty client-side SPA root shells where search crawlers without JavaScript execution cannot retrieve text.
- **Sitemap Availability (`technical.robots_sitemap`)**: Verifies XML sitemaps are reachable and valid.

Technical findings are kept completely separate from algorithm update correlations. SiteProbe **never labels a website as spam**.

---

## 5. Why Correlation Does Not Prove Causation

Observing a Search Console traffic decline concurrently with an algorithm rollout does **not** prove the algorithm caused the decline. Confounding variables include:

1. **Seasonal Demand**: Macro consumer interest for products or topics shifts naturally across calendar weeks.
2. **Technical Regressions**: CMS updates, CDN caching issues, or firewall false positives blocking Googlebot.
3. **SERP Feature Expansion**: Google expanding AI Overviews, featured snippets, or local packs above organic listings can reduce click-through rates while rankings remain constant.
4. **Competitor Enhancements**: Competing sites publishing superior content or earning authoritative links can displace rankings without any update penalty.
5. **Data Reporting Delays**: Google Search Console has a 48–72 hour data aggregation delay.

---

## 6. How to Reproduce

Run the triage workflow using the synthetic benchmark dataset:

```bash
# Terminal summary
siteprobe update-triage --csv examples/update-impact/sample-input.csv

# Output machine-readable JSON
siteprobe update-triage --csv examples/update-impact/sample-input.csv --output report.json

# Incorporate existing SiteProbe audit findings
siteprobe update-triage --csv examples/update-impact/sample-input.csv --audit-file ./siteprobe-report/audit.json
```
