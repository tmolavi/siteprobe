# Molavi AI Visibility Stack — Benchmark Ecosystem & Evidence Map

This document defines the architectural boundaries, data flow, and reproducible evidence contracts between the 5 components of the Molavi AI Visibility Stack.

```
       ┌────────────────────────────────────────────────────────┐
       │                    AnswerPath GEO                      │
       │     (Question Discovery, Intent Mining & Provenance)   │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   │  30 Prompts (15 Observed + 15 Generated)
                                   │  Schema: source_type, intent, cluster
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                       GEO-Scope                        │
       │     (Execution Engine, Multi-Provider Measurement)     │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   │  Empirical L5 Observations (N=120)
                                   │  Mentions, Recommendations, Citations, CIs
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                       SAGE                             │
       │    (Static Technical & Semantic Passage Diagnostics)   │
       │   L1: Technical · L2: Extractable · L3: Entity · L4: CSP│
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   │  Diagnostic Diagnostic Scores (0–100)
                                   │  LLMS.txt & Clean RAG Chunks
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                         MAVI                           │
       │        (Molavi AI Visibility Index Aggregation)        │
       │          Composite Index = L1 + L2 + L3 + L4 + L5       │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   │  Identified Gaps & Low-Score Signals
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                      SiteProbe                         │
       │      (Autonomous Remediation: Audit → Fix → Verify)     │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   │  Applied Remediation & Post-Fix Validation
                                   ▼
                       [ Re-measurement via GEO-Scope ]
```

---

## Ecosystem Roles & Contract Boundaries

### 1. AnswerPath GEO — Question Discovery & Demand Stratification
* **Repository**: [`tmolavi/answerpath-geo`](https://github.com/tmolavi/answerpath-geo)
* **Role**: Mines owned conversations, search logs, and exploratory templates to construct structured question banks.
* **Strict Boundary**: AnswerPath **never** calculates visibility scores, rankings, or provider responses. It only discovers and categorizes questions.
* **Evidence Schema**:
  ```json
  {
    "id": "PRM-IR-001",
    "prompt": "بهترین آژانس دیجیتال مارکتینگ و سئو در ایران کدام است؟",
    "intent": "commercial",
    "source_type": "observed",
    "source_reference": "answerpath",
    "cluster": "general_recommendation"
  }
  ```

### 2. GEO-Scope — Benchmark Execution & Multi-Model Observation
* **Repository**: [`tmolavi/geo-scope`](https://github.com/tmolavi/geo-scope)
* **Role**: Executes multi-model benchmarks, collects full raw provider completions, records routing provenance (native vs fallback), extracts entity mentions and citations, and computes statistical visibility metrics with 95% bootstrap confidence intervals.
* **Strict Boundary**: GEO-Scope measures **empirical observations**, not internal AI ranking algorithms.
* **Release Artifact**: `benchmark/releases/geo-seo-digital-agency-iran-2026.1/`

### 3. SAGE — 4-Layer Diagnostic Audit Engine
* **Repository**: [`tmolavi/sage-audit`](https://github.com/tmolavi/sage-audit)
* **Role**: Provides deterministic pre-retrieval diagnostics across 4 distinct layers:
  * **L1 Technical Accessibility**: AI crawler permissions (GPTBot, PerplexityBot, ClaudeBot), HTTP headers, clean DOM extraction.
  * **L2 Semantic Extractability**: Boilerplate stripping, text-to-code ratio, 60–120 token chunk boundaries.
  * **L3 Entity Clarity**: JSON-LD graph validation (`Organization`, `FAQPage`, `sameAs` Wikidata/Crunchbase).
  * **L4 Citation Readiness**: Cosine distance, semantic entropy, and Citation Survival Proxy (CSP).

### 4. MAVI — Molavi AI Visibility Index
* **Package**: `geo_scope.mavi`
* **Role**: Synthesizes the 4 diagnostic layers (SAGE L1–L4) with empirical multi-model observations (GEO-Scope L5) into a unified, balanced 0–100 visibility index.
* **Formula**:
  $$\text{MAVI} = w_1 L_1 + w_2 L_2 + w_3 L_3 + w_4 L_4 + w_5 L_5$$
* **Integrity Guarantee**: If L5 is unmeasured (e.g. static audit only), MAVI marks L5 as `NOT_MEASURED` rather than fabricating synthetic observation data.

### 5. SiteProbe — Autonomous Remediation & Verification
* **Repository**: [`tmolavi/siteprobe`](https://github.com/tmolavi/siteprobe)
* **Role**: Closes the loop from observation to action. Turns diagnostic findings into atomic code fixes:
  * Generates missing `/llms.txt` and semantic chunks.
  * Fixes unindexed bot directives in `robots.txt`.
  * Injects missing Schema.org JSON-LD entity structures.
  * Verifies post-remediation changes before scheduling re-measurement in GEO-Scope.

---

## The Closed-Loop AI Visibility Lifecycle

1. **Discovery (AnswerPath)**: Extract real user questions across commercial, comparative, and problem-solving intents.
2. **Measurement (GEO-Scope)**: Run multi-provider benchmarks across Google Gemini, OpenAI GPT, Anthropic Claude, and Perplexity Sonar.
3. **Diagnosis (SAGE)**: Inspect low-visibility entities for technical, semantic, or entity-graph deficiencies.
4. **Scoring (MAVI)**: Establish an overall baseline index.
5. **Remediation (SiteProbe)**: Safely patch code, inject structured data, and publish clean `/llms.txt`.
6. **Re-measurement (GEO-Scope)**: Re-run benchmark to measure observed delta in mentions, recommendations, and grounding citations.
