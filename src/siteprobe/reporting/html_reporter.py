import json
from pathlib import Path
from typing import Union
from siteprobe.core.engine import AuditResult
from siteprobe.models.finding import Severity


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{{ language }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SiteProbe Audit Report &mdash; {{ site_url }}</title>
  <style>
    :root {
      --bg: #0d1117;
      --card-bg: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --text-dim: #8b949e;
      --heading: #f0f6fc;
      --accent: #58a6ff;
      --critical: #f85149;
      --high: #d29922;
      --medium: #e3b341;
      --low: #3fb950;
      --info: #8b949e;
      --score-high: #3fb950;
      --score-mid: #d29922;
      --score-low: #f85149;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
    body { background: var(--bg); color: var(--text); padding: 2rem 1rem; line-height: 1.6; }
    .container { max-width: 1200px; margin: 0 auto; }
    header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem; }
    h1 { color: var(--heading); font-size: 1.8rem; display: flex; align-items: center; gap: 0.5rem; }
    .badge { display: inline-block; padding: 0.2rem 0.6rem; font-size: 0.75rem; font-weight: bold; border-radius: 999px; text-transform: uppercase; }
    .badge-critical { background: rgba(248, 81, 73, 0.2); color: var(--critical); border: 1px solid var(--critical); }
    .badge-high { background: rgba(210, 153, 34, 0.2); color: var(--high); border: 1px solid var(--high); }
    .badge-medium { background: rgba(227, 179, 65, 0.2); color: var(--medium); border: 1px solid var(--medium); }
    .badge-low { background: rgba(63, 185, 80, 0.2); color: var(--low); border: 1px solid var(--low); }
    .badge-fix { background: rgba(88, 166, 255, 0.2); color: var(--accent); border: 1px solid var(--accent); }
    .hero-grid { display: grid; grid-template-columns: 280px 1fr; gap: 1.5rem; margin-bottom: 2rem; }
    @media (max-width: 850px) { .hero-grid { grid-template-columns: 1fr; } }
    .score-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 2rem; text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .score-circle { width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: 800; margin-bottom: 1rem; border: 8px solid; }
    .score-green { border-color: var(--score-high); color: var(--score-high); }
    .score-yellow { border-color: var(--score-mid); color: var(--score-mid); }
    .score-red { border-color: var(--score-low); color: var(--score-low); }
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
    .stat-box { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 1.2rem; }
    .stat-label { font-size: 0.85rem; color: var(--text-dim); text-transform: uppercase; margin-bottom: 0.3rem; }
    .stat-val { font-size: 1.4rem; font-weight: 700; color: var(--heading); }
    .section-title { font-size: 1.3rem; color: var(--heading); margin: 2rem 0 1rem 0; border-left: 4px solid var(--accent); padding-left: 0.75rem; }
    .cards-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
    .cat-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; }
    .cat-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
    .cat-name { font-weight: 600; color: var(--heading); }
    .cat-score { font-size: 1.2rem; font-weight: bold; }
    .finding-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem; transition: border-color 0.2s; }
    .finding-card:hover { border-color: var(--accent); }
    .finding-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: 0.75rem; flex-wrap: wrap; }
    .finding-title { font-size: 1.1rem; color: var(--heading); font-weight: 600; }
    .finding-body { font-size: 0.95rem; margin-bottom: 0.5rem; }
    .finding-evidence { background: #000; padding: 0.75rem; border-radius: 6px; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 0.85rem; overflow-x: auto; margin-top: 0.5rem; border: 1px solid #222; }
    .tab-bar { display: flex; gap: 0.5rem; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem; overflow-x: auto; padding-bottom: 0.5rem; }
    .tab-btn { background: none; border: 1px solid transparent; color: var(--text-dim); padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; font-size: 0.9rem; font-weight: 600; }
    .tab-btn.active { background: var(--card-bg); border-color: var(--border); color: var(--accent); }
    footer { margin-top: 4rem; text-align: center; font-size: 0.85rem; color: var(--text-dim); border-top: 1px solid var(--border); padding-top: 1.5rem; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div>
        <h1>SiteProbe Audit Report</h1>
        <p style="color: var(--text-dim); font-size: 0.9rem;">Target: <strong style="color: var(--heading);">{{ site_url }}</strong> | Scanned at {{ timestamp }}</p>
      </div>
      <div>
        <span class="badge badge-fix">Engine v0.1.0</span>
        <span class="badge badge-low">Audit Mode</span>
      </div>
    </header>

    <div class="hero-grid">
      <div class="score-card">
        <div class="score-circle {{ score_color_class }}">
          {{ scores.overall_score }}
        </div>
        <div style="font-size: 1.1rem; font-weight: bold; color: var(--heading);">Overall Quality Score</div>
        <p style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0.5rem;">Weighted across Technical, On-Page, Schema, GEO, A11y, and Security.</p>
      </div>

      <div class="stats-grid">
        <div class="stat-box">
          <div class="stat-label">GEO & AI-Search Score</div>
          <div class="stat-val" style="color: var(--accent);">{{ scores.geo_score }} / 100</div>
          <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0.4rem;">Pillars: Bots ({{ scores.geo_score_breakdown.ai_crawler_access }}/40), llms.txt ({{ scores.geo_score_breakdown.llms_txt_presence }}/20)</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Pages Crawled</div>
          <div class="stat-val">{{ crawl_summary.total_crawled }}</div>
          <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0.4rem;">Duration: {{ crawl_summary.crawl_duration_seconds }}s</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Total Findings</div>
          <div class="stat-val" style="color: var(--critical);">{{ findings|length }}</div>
          <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0.4rem;">Auto-Fixable: {{ auto_fixable_count }}</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Broken Links</div>
          <div class="stat-val" style="color: {{ 'var(--critical)' if crawl_summary.broken_links_count > 0 else 'var(--low)' }};">{{ crawl_summary.broken_links_count }}</div>
          <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0.4rem;">HTTP 4xx / 5xx links</div>
        </div>
      </div>
    </div>

    <div class="section-title">Category Health Breakdown</div>
    <div class="cards-row">
      {% for cat_id, cs in scores.category_scores.items() %}
      <div class="cat-card">
        <div class="cat-card-header">
          <span class="cat-name">{{ cat_id|replace('_', ' ')|title }}</span>
          <span class="cat-score" style="color: {{ 'var(--low)' if cs.score >= 85 else ('var(--high)' if cs.score >= 60 else 'var(--critical)') }};">{{ cs.score }}</span>
        </div>
        <div style="font-size: 0.8rem; color: var(--text-dim);">
          Critical: {{ cs.critical_count }} &bull; High: {{ cs.high_count }} &bull; Med: {{ cs.medium_count }}
        </div>
      </div>
      {% endfor %}
    </div>

    <div class="section-title">Audit Findings & Remediation Steps</div>
    {% if not findings %}
      <div class="stat-box" style="text-align: center; padding: 2rem;">
        <h3 style="color: var(--low);">All Checks Passed!</h3>
        <p style="color: var(--text-dim);">No defects detected on crawled pages.</p>
      </div>
    {% else %}
      {% for f in findings %}
      <div class="finding-card">
        <div class="finding-header">
          <div class="finding-title">
            <span class="badge badge-{{ f.severity.value }}">{{ f.severity.value }}</span>
            {% if f.auto_fixable %}
              <span class="badge badge-fix">Auto-Fixable</span>
            {% endif %}
            {{ f.title }}
          </div>
          <span style="font-size: 0.8rem; color: var(--text-dim); font-family: monospace;">{{ f.id }}</span>
        </div>
        <div class="finding-body">
          <div style="color: var(--accent); font-size: 0.85rem; margin-bottom: 0.3rem;">URL: {{ f.url }}</div>
          <p><strong>Why it matters:</strong> {{ f.why_it_matters }}</p>
          <p style="margin-top: 0.3rem;"><strong>Recommended Action:</strong> {{ f.recommended_action }}</p>
          {% if f.evidence %}
          <div class="finding-evidence">{{ f.evidence|tojson(indent=2) }}</div>
          {% endif %}
        </div>
      </div>
      {% endfor %}
    {% endif %}

    {% if missing_capabilities %}
    <div class="section-title">Missing Capabilities & Enriched Audit Options</div>
    <div class="cards-row">
      {% for cap in missing_capabilities %}
      <div class="cat-card">
        <div style="font-weight: 600; color: var(--heading); margin-bottom: 0.4rem;">{{ cap.name }}</div>
        <p style="font-size: 0.85rem; color: var(--text-dim); margin-bottom: 0.5rem;">{{ cap.why_it_improves_audit }}</p>
        <div style="font-size: 0.8rem; color: var(--accent);">How to enable: {{ cap.how_to_enable }}</div>
      </div>
      {% endfor %}
    </div>
    {% endif %}

    <footer>
      Generated autonomously by <a href="https://github.com/tmolavi/siteprobe" style="color: var(--accent); text-decoration: none;">SiteProbe</a> &mdash; Autonomous Website Auditor & Fixer.
    </footer>
  </div>
</body>
</html>
"""


class HtmlReporter:
    """Generates polished, responsive, standalone HTML audit dashboards."""

    @classmethod
    def render(cls, res: AuditResult) -> str:
        from jinja2 import Template

        score = res.scores.overall_score
        score_class = "score-green" if score >= 80 else ("score-yellow" if score >= 55 else "score-red")
        auto_count = sum(1 for f in res.findings if f.auto_fixable)

        tmpl = Template(HTML_TEMPLATE)
        return tmpl.render(
            site_url=res.site_url,
            language=res.language,
            timestamp=res.timestamp,
            scores=res.scores,
            crawl_summary=res.crawl_summary,
            findings=res.findings,
            missing_capabilities=res.missing_capabilities,
            score_color_class=score_class,
            auto_fixable_count=auto_count,
        )

    @classmethod
    def save(cls, audit_result: AuditResult, output_path: Union[str, Path]) -> Path:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        content = cls.render(audit_result)
        p.write_text(content, encoding="utf-8")
        return p
