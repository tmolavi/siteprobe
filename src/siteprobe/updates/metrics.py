import datetime
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

from siteprobe.updates.constants import (
    COMPLETION_DATE,
    POST_WINDOW_DAYS,
    POST_WINDOW_END,
    POST_WINDOW_START,
    PRE_WINDOW_DAYS,
    PRE_WINDOW_END,
    PRE_WINDOW_START,
    ROLLOUT_WINDOW_DAYS,
    ROLLOUT_WINDOW_END,
    ROLLOUT_WINDOW_START,
)
from siteprobe.updates.models import DimensionDelta, GscDataRow, WindowMetrics


def generate_date_range(start_str: str, end_str: str) -> List[datetime.date]:
    """Generates all calendar dates between start and end inclusive."""
    start = datetime.date.fromisoformat(start_str)
    end = datetime.date.fromisoformat(end_str)
    curr = start
    dates = []
    while curr <= end:
        dates.append(curr)
        curr += datetime.timedelta(days=1)
    return dates


def compute_window_metrics(
    window_name: str,
    start_str: str,
    end_str: str,
    expected_days: int,
    rows: List[GscDataRow],
) -> WindowMetrics:
    """
    Computes aggregated performance metrics for a specific time window.
    Strictly calculates CTR as sum(clicks) / sum(impressions) without averaging CTRs.
    """
    start_dt = datetime.date.fromisoformat(start_str)
    end_dt = datetime.date.fromisoformat(end_str)

    window_rows = [r for r in rows if start_dt <= r.date <= end_dt]
    distinct_dates = set(r.date for r in window_rows)

    total_clicks = sum(r.clicks for r in window_rows)
    total_impressions = sum(r.impressions for r in window_rows)

    # Calculate CTR strictly from totals
    ctr = (total_clicks / total_impressions) if total_impressions > 0 else 0.0

    # Impression-weighted position calculation if available
    pos_rows = [r for r in window_rows if r.position is not None and r.impressions > 0]
    total_pos_imp = sum(r.impressions for r in pos_rows)
    if total_pos_imp > 0:
        weighted_pos = sum(r.position * r.impressions for r in pos_rows) / total_pos_imp  # type: ignore[operator]
        avg_position = round(weighted_pos, 2)
    else:
        avg_position = None

    # Daily breakdown
    daily_groups: Dict[str, Dict[str, int]] = defaultdict(lambda: {"clicks": 0, "impressions": 0})
    for r in window_rows:
        d_str = r.date.isoformat()
        daily_groups[d_str]["clicks"] += r.clicks
        daily_groups[d_str]["impressions"] += r.impressions

    daily_breakdown = []
    for d_str in sorted(daily_groups.keys()):
        d_imp = daily_groups[d_str]["impressions"]
        d_clk = daily_groups[d_str]["clicks"]
        d_ctr = (d_clk / d_imp) if d_imp > 0 else 0.0
        daily_breakdown.append({
            "date": d_str,
            "clicks": d_clk,
            "impressions": d_imp,
            "ctr": round(d_ctr, 4),
        })

    is_complete = len(distinct_dates) == expected_days

    return WindowMetrics(
        window_name=window_name,
        start_date=start_str,
        end_date=end_str,
        days_expected=expected_days,
        days_present=len(distinct_dates),
        is_complete=is_complete,
        total_clicks=total_clicks,
        total_impressions=total_impressions,
        ctr=round(ctr, 6),
        avg_position=avg_position,
        daily_breakdown=daily_breakdown,
    )


def compute_dimension_deltas(
    pre_rows: List[GscDataRow],
    rollout_rows: List[GscDataRow],
    dimension: str,
    top_limit: int = 15,
) -> List[DimensionDelta]:
    """Computes pre vs rollout changes for dimensions (query or page)."""
    pre_map: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"clicks": 0, "impressions": 0, "pos_imp": 0, "pos_sum": 0.0})
    rollout_map: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"clicks": 0, "impressions": 0, "pos_imp": 0, "pos_sum": 0.0})

    for r in pre_rows:
        val = getattr(r, dimension, None)
        if val:
            pre_map[val]["clicks"] += r.clicks
            pre_map[val]["impressions"] += r.impressions
            if r.position and r.impressions > 0:
                pre_map[val]["pos_imp"] += r.impressions
                pre_map[val]["pos_sum"] += r.position * r.impressions

    for r in rollout_rows:
        val = getattr(r, dimension, None)
        if val:
            rollout_map[val]["clicks"] += r.clicks
            rollout_map[val]["impressions"] += r.impressions
            if r.position and r.impressions > 0:
                rollout_map[val]["pos_imp"] += r.impressions
                rollout_map[val]["pos_sum"] += r.position * r.impressions

    all_keys = set(pre_map.keys()) | set(rollout_map.keys())
    deltas: List[DimensionDelta] = []

    for k in all_keys:
        pre_c = pre_map[k]["clicks"]
        roll_c = rollout_map[k]["clicks"]
        pre_i = pre_map[k]["impressions"]
        roll_i = rollout_map[k]["impressions"]

        pre_pos = (pre_map[k]["pos_sum"] / pre_map[k]["pos_imp"]) if pre_map[k]["pos_imp"] > 0 else None
        roll_pos = (rollout_map[k]["pos_sum"] / rollout_map[k]["pos_imp"]) if rollout_map[k]["pos_imp"] > 0 else None

        deltas.append(DimensionDelta(
            dimension=dimension,
            value=k,
            pre_clicks=pre_c,
            rollout_clicks=roll_c,
            click_change=roll_c - pre_c,
            pre_impressions=pre_i,
            rollout_impressions=roll_i,
            impression_change=roll_i - pre_i,
            pre_position=round(pre_pos, 2) if pre_pos else None,
            rollout_position=round(roll_pos, 2) if roll_pos else None,
        ))

    # Sort by absolute click change or total pre impressions
    deltas.sort(key=lambda x: (abs(x.click_change), x.pre_impressions), reverse=True)
    return deltas[:top_limit]


def compute_categorical_breakdown(
    pre_rows: List[GscDataRow],
    rollout_rows: List[GscDataRow],
    dimension: str,
) -> Dict[str, Any]:
    """Computes breakdown by categorical dimension (e.g. device or country)."""
    categories = set(
        getattr(r, dimension) for r in (pre_rows + rollout_rows) if getattr(r, dimension)
    )
    result = {}
    for cat in sorted(categories):
        p_c = sum(r.clicks for r in pre_rows if getattr(r, dimension) == cat)
        r_c = sum(r.clicks for r in rollout_rows if getattr(r, dimension) == cat)
        p_i = sum(r.impressions for r in pre_rows if getattr(r, dimension) == cat)
        r_i = sum(r.impressions for r in rollout_rows if getattr(r, dimension) == cat)
        p_ctr = (p_c / p_i) if p_i > 0 else 0.0
        r_ctr = (r_c / r_i) if r_i > 0 else 0.0
        c_change_pct = (((r_c - p_c) / p_c) * 100.0) if p_c > 0 else None

        result[cat] = {
            "pre_clicks": p_c,
            "rollout_clicks": r_c,
            "click_change_percent": round(c_change_pct, 2) if c_change_pct is not None else None,
            "pre_impressions": p_i,
            "rollout_impressions": r_i,
            "pre_ctr": round(p_ctr, 4),
            "rollout_ctr": round(r_ctr, 4),
        }
    return result


def analyze_windows(
    rows: List[GscDataRow],
) -> Tuple[WindowMetrics, WindowMetrics, WindowMetrics, WindowMetrics, Optional[float], Optional[float], Optional[float], List[str]]:
    """
    Computes all frozen windows: PRE, ROLLOUT, COMPLETION, and POST.
    Ensures incomplete periods are flagged and not compared against complete periods.
    """
    warnings: List[str] = []

    pre = compute_window_metrics(
        "PRE", PRE_WINDOW_START, PRE_WINDOW_END, PRE_WINDOW_DAYS, rows
    )
    rollout = compute_window_metrics(
        "ROLLOUT", ROLLOUT_WINDOW_START, ROLLOUT_WINDOW_END, ROLLOUT_WINDOW_DAYS, rows
    )
    completion = compute_window_metrics(
        "COMPLETION", COMPLETION_DATE, COMPLETION_DATE, 1, rows
    )
    post = compute_window_metrics(
        "POST", POST_WINDOW_START, POST_WINDOW_END, POST_WINDOW_DAYS, rows
    )

    if not pre.is_complete:
        warnings.append(
            f"PRE window is incomplete ({pre.days_present}/{PRE_WINDOW_DAYS} days present)."
        )

    if not rollout.is_complete:
        warnings.append(
            f"ROLLOUT window is incomplete ({rollout.days_present}/{ROLLOUT_WINDOW_DAYS} days present)."
        )

    if not post.is_complete:
        warnings.append(
            f"POST window is currently incomplete ({post.days_present}/{POST_WINDOW_DAYS} days present). "
            f"Post-update recovery cannot be reliably evaluated until all 14 days are recorded."
        )

    # Comparisons are ONLY calculated if both PRE and ROLLOUT are complete
    click_change_pct = None
    imp_change_pct = None
    ctr_change_pts = None

    if pre.is_complete and rollout.is_complete:
        if pre.total_clicks > 0:
            click_change_pct = round(
                ((rollout.total_clicks - pre.total_clicks) / pre.total_clicks) * 100.0, 2
            )
        elif rollout.total_clicks == 0:
            click_change_pct = 0.0

        if pre.total_impressions > 0:
            imp_change_pct = round(
                ((rollout.total_impressions - pre.total_impressions) / pre.total_impressions) * 100.0, 2
            )
        elif rollout.total_impressions == 0:
            imp_change_pct = 0.0

        ctr_change_pts = round((rollout.ctr - pre.ctr) * 100.0, 4)

    return pre, rollout, completion, post, click_change_pct, imp_change_pct, ctr_change_pts, warnings
