from typing import Dict, List
from pydantic import BaseModel, Field
from siteprobe.models.finding import Finding, FindingCategory, Severity


class CategoryScore(BaseModel):
    category: str
    score: int = 100
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    info_count: int = 0
    deductions: List[str] = Field(default_factory=list)


class ScoreReport(BaseModel):
    overall_score: int = 100
    category_scores: Dict[str, CategoryScore] = Field(default_factory=dict)
    geo_score: int = 100
    geo_score_breakdown: Dict[str, int] = Field(default_factory=dict)
    methodology: str = (
        "Overall score is a deterministic weighted composite: Technical (25%), On-Page (20%), "
        "Schema (15%), GEO/AEO (15%), Accessibility (15%), Security (10%). Deductions per category "
        "are: Critical (-25), High (-10), Medium (-5), Low (-2), bounded between 0 and 100. "
        "GEO score is evaluated directly on 4 transparent pillars: AI crawler access (40 pts), "
        "llms.txt availability (20 pts), Entity & authorship structure (20 pts), and QA semantic markup (20 pts)."
    )


def compute_scores(findings: List[Finding]) -> ScoreReport:
    """Compute deterministic scores and explainable breakdowns from audit findings."""
    cats = [c.value for c in FindingCategory]
    cat_scores: Dict[str, CategoryScore] = {c: CategoryScore(category=c, score=100) for c in cats}

    # Track severity counts and deductions
    for f in findings:
        cs = cat_scores.get(f.category.value)
        if not cs:
            continue

        if f.severity == Severity.CRITICAL:
            cs.critical_count += 1
            deduct = 25
        elif f.severity == Severity.HIGH:
            cs.high_count += 1
            deduct = 10
        elif f.severity == Severity.MEDIUM:
            cs.medium_count += 1
            deduct = 5
        elif f.severity == Severity.LOW:
            cs.low_count += 1
            deduct = 2
        else:
            cs.info_count += 1
            deduct = 0

        cs.score = max(0, cs.score - deduct)
        if deduct > 0:
            cs.deductions.append(f"[-{deduct}] {f.title}")

    # Specific GEO pillar calculation
    geo_pillars = {
        "ai_crawler_access": 40,
        "llms_txt_presence": 20,
        "entity_authorship": 20,
        "qa_semantic_structure": 20,
    }
    for f in findings:
        if f.id == "geo.ai_bots.blocked":
            geo_pillars["ai_crawler_access"] = 0
        elif f.id == "geo.llms_txt.missing":
            geo_pillars["llms_txt_presence"] = 0
        elif f.id in ("geo.entity.missing_author", "schema.entity.missing_organization"):
            geo_pillars["entity_authorship"] = max(0, geo_pillars["entity_authorship"] - 10)
        elif f.id == "geo.structure.missing_faq_schema":
            geo_pillars["qa_semantic_structure"] = max(0, geo_pillars["qa_semantic_structure"] - 10)

    calculated_geo_score = sum(geo_pillars.values())
    cat_scores[FindingCategory.GEO_AEO.value].score = calculated_geo_score

    # Weighted overall score
    weights = {
        FindingCategory.TECHNICAL_SEO.value: 0.25,
        FindingCategory.ONPAGE_SEO.value: 0.20,
        FindingCategory.SCHEMA_ORG.value: 0.15,
        FindingCategory.GEO_AEO.value: 0.15,
        FindingCategory.ACCESSIBILITY.value: 0.15,
        FindingCategory.SECURITY.value: 0.10,
    }

    weighted_sum = 0.0
    for cat_name, w in weights.items():
        score_val = cat_scores.get(cat_name, CategoryScore(category=cat_name, score=100)).score
        weighted_sum += score_val * w

    overall = int(round(weighted_sum))

    return ScoreReport(
        overall_score=max(0, min(100, overall)),
        category_scores=cat_scores,
        geo_score=calculated_geo_score,
        geo_score_breakdown=geo_pillars,
    )
