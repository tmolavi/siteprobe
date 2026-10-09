# Google Algorithm Update Impact Triage — Example & Reproduction Guide

This directory provides a self-contained, reproducible example of SiteProbe's **Google Update Impact Triage** pipeline for the **September 2026 Google Spam Update**.

> [!IMPORTANT]
> **SYNTHETIC BENCHMARK DATASET NOTICE**  
> `sample-input.csv` contains purely **SYNTHETIC** benchmark Search Console metrics generated to demonstrate and verify the triage calculation engine. No proprietary Google data or private website analytics are included.

---

## 📅 Official Event & Frozen Windows

Google declared the September 2026 Spam Update rollout between **2026-09-24** and **2026-10-08**. To ensure sound statistical analysis, SiteProbe freezes four sequential calendar periods:

| Window | Date Range | Duration | Weekday Alignment | Status |
| :--- | :--- | :---: | :--- | :--- |
| **PRE** | `2026-09-10` to `2026-09-23` | 14 days | Thursday to Wednesday | Complete baseline |
| **ROLLOUT** | `2026-09-24` to `2026-10-07` | 14 days | Thursday to Wednesday | Complete rollout window |
| **COMPLETION** | `2026-10-08` | 1 day | Thursday | Recorded separately |
| **POST** | `2026-10-09` to `2026-10-22` | 14 days | In progress | Incomplete (no forward extrapolation) |

### Key Methodological Rules
1. **Matched Weekdays**: Both PRE and ROLLOUT cover exactly 14 days and share identical weekday representations (2 Thursdays, 2 Fridays, etc.) to cancel out weekend vs. weekday traffic seasonality.
2. **Separated Completion Day**: The final official day of rollout (2026-10-08) is isolated so it does not distort the 14-day matched-window symmetry.
3. **Incomplete POST Window**: As of October 9, 2026, the POST window has just begun. SiteProbe **never compares incomplete periods against complete periods** and **never invents missing future observations**.

---

## 🛠️ Reproduction Command

To reproduce the analysis from the root of the SiteProbe repository:

```bash
siteprobe update-triage \
  --csv examples/update-impact/sample-input.csv \
  --output examples/update-impact/sample-output.json
```

Or to inspect raw JSON output directly on standard output:

```bash
siteprobe update-triage \
  --csv examples/update-impact/sample-input.csv \
  --json
```

---

## 🔬 Diagnostic Classifications

SiteProbe classifies audit outcomes into one of five mutually exclusive empirical categories:

1. `NO_MEANINGFUL_CHANGE_OBSERVED`: Performance metrics stayed within standard variance (±15%).
2. `PERFORMANCE_CHANGE_OBSERVED`: Statistically significant performance decline or shift observed during rollout, with no manual action or technical errors detected.
3. `TECHNICAL_ISSUE_OBSERVED`: Technical website errors (HTTP 5xx, sitewide noindex, robots.txt blocks, SSR empty shell, canonical loops) explain traffic declines independently of algorithm changes.
4. `MANUAL_ACTION_REPORTED`: Search Console explicitly documented a human-reviewed manual action on the property.
5. `INSUFFICIENT_DATA`: Comparison windows have missing dates, zero impressions, or no Search Console export was provided.

---

## ⚠️ Scientific Integrity & Public Claims

- **Allowed Claim**:
  > *"SiteProbe provides a reproducible workflow for examining Search Console changes around Google's September 2026 spam update."*
- **Forbidden Claims**:
  - *"SiteProbe detects Google penalties."*
  - *"SiteProbe identifies SpamBrain violations."*
  - *"SiteProbe proves the update caused a traffic loss."*

Correlation with update rollout dates does not prove causation. External factors such as seasonal demand shifts, tracking tag misconfigurations, competitor launches, or SERP layout modifications frequently mimic algorithm impacts.
