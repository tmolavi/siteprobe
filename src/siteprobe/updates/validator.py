import csv
import datetime
import io
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from siteprobe.updates.constants import REQUIRED_COLUMNS
from siteprobe.updates.models import GscDataRow


def parse_date(val: str, row_idx: int) -> datetime.date:
    """Parses and validates a date string strictly in YYYY-MM-DD format."""
    val = val.strip()
    if not val:
        raise ValueError(f"Row {row_idx}: Missing required 'date' value.")
    try:
        dt = datetime.date.fromisoformat(val)
        return dt
    except Exception as e:
        raise ValueError(f"Row {row_idx}: Invalid date '{val}'. Expected YYYY-MM-DD. Error: {e}")


def parse_non_negative_int(val: str, field_name: str, row_idx: int) -> int:
    """Parses and validates a non-negative integer."""
    val = val.strip()
    if val == "":
        raise ValueError(f"Row {row_idx}: Missing required '{field_name}' value.")
    try:
        # Support string floats representing ints like '10.0'
        num = float(val)
        if not num.is_integer() and field_name in ("clicks", "impressions"):
            # Some platforms export floats for impressions/clicks, round or check
            pass
        int_val = int(round(num))
        if int_val < 0:
            raise ValueError(f"Row {row_idx}: '{field_name}' cannot be negative ({val}).")
        return int_val
    except Exception as e:
        if "cannot be negative" in str(e):
            raise
        raise ValueError(f"Row {row_idx}: Invalid integer for '{field_name}': '{val}'.")


def parse_ctr(val: Optional[str], row_idx: int) -> Optional[float]:
    """Parses and validates a CTR value, accepting decimal (0.05) or percentage (5%)."""
    if val is None or val.strip() == "":
        return None
    val = val.strip()
    is_percent = val.endswith("%")
    clean_val = val[:-1].strip() if is_percent else val
    try:
        num = float(clean_val)
        if is_percent:
            num = num / 100.0
        if num < 0.0 or num > 1.0:
            raise ValueError(
                f"Row {row_idx}: Invalid CTR value '{val}'. CTR must be between 0.0 and 1.0 (or 0% to 100%)."
            )
        return num
    except Exception as e:
        if "CTR must be between" in str(e):
            raise
        raise ValueError(f"Row {row_idx}: Invalid CTR numeric value: '{val}'.")


def parse_position(val: Optional[str], row_idx: int) -> Optional[float]:
    """Parses and validates average ranking position (>= 1.0)."""
    if val is None or val.strip() == "":
        return None
    val = val.strip()
    try:
        pos = float(val)
        if pos < 1.0:
            raise ValueError(f"Row {row_idx}: Average position must be >= 1.0, got '{val}'.")
        return pos
    except Exception as e:
        if "must be >= 1.0" in str(e):
            raise
        raise ValueError(f"Row {row_idx}: Invalid numeric position: '{val}'.")


def validate_and_parse_gsc_csv(
    source: Union[str, Path, io.StringIO, io.TextIOBase]
) -> Tuple[List[GscDataRow], List[str]]:
    """
    Validates and parses a Search Console CSV export.
    
    Required columns: date, clicks, impressions
    Optional dimensions: query, page, country, device, position, ctr
    
    Validates:
    - Missing required headers
    - Empty file
    - Missing row values
    - Date syntax and calendar validity
    - Negative or malformed numbers
    - Logical integrity (clicks <= impressions)
    - CTR bounds (0 <= CTR <= 1.0)
    - Position validity (>= 1.0)
    - Duplicate rows across dimension composite keys
    """
    warnings: List[str] = []

    if isinstance(source, (str, Path)) and Path(str(source)).exists():
        with open(source, "r", encoding="utf-8-sig") as f:
            content = f.read()
    elif isinstance(source, str):
        content = source
    elif isinstance(source, (io.StringIO, io.TextIOBase)):
        content = source.read()
    else:
        raise ValueError(f"Invalid input source for GSC data: {source}")

    if not content.strip():
        raise ValueError("CSV source is empty.")

    # Strip comment lines (e.g. # SYNTHETIC DATASET NOTICE)
    clean_lines = [line for line in content.splitlines() if not line.strip().startswith("#")]
    if not clean_lines or not any(l.strip() for l in clean_lines):
        raise ValueError("CSV source contains only comments or empty lines.")

    reader = csv.reader(clean_lines)
    try:
        raw_headers = next(reader)
    except StopIteration:
        raise ValueError("CSV source has no header row.")

    # Normalize headers
    header_map: Dict[str, int] = {}
    for idx, h in enumerate(raw_headers):
        norm = h.strip().lower()
        # Handle common BOM or formatting quirks
        norm = norm.replace("\ufeff", "")
        if norm:
            header_map[norm] = idx

    # Check required columns
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in header_map]
    if missing_cols:
        raise ValueError(
            f"Missing required columns in CSV: {missing_cols}. Found: {list(header_map.keys())}"
        )

    date_idx = header_map["date"]
    clicks_idx = header_map["clicks"]
    imp_idx = header_map["impressions"]

    query_idx = header_map.get("query")
    page_idx = header_map.get("page")
    country_idx = header_map.get("country")
    device_idx = header_map.get("device")
    pos_idx = header_map.get("position")
    ctr_idx = header_map.get("ctr")

    parsed_rows: List[GscDataRow] = []
    seen_keys: Set[Tuple[Any, ...]] = set()

    has_dimensions = any(idx is not None for idx in [query_idx, page_idx, country_idx, device_idx])

    for row_idx, row in enumerate(reader, start=2):
        if not row or all(c.strip() == "" for c in row):
            continue  # skip completely blank rows

        if len(row) <= max(date_idx, clicks_idx, imp_idx):
            raise ValueError(f"Row {row_idx}: Row has fewer columns than required headers.")

        # Parse required fields
        dt = parse_date(row[date_idx], row_idx)
        clicks = parse_non_negative_int(row[clicks_idx], "clicks", row_idx)
        impressions = parse_non_negative_int(row[imp_idx], "impressions", row_idx)

        # Logical consistency
        if clicks > impressions:
            raise ValueError(
                f"Row {row_idx}: Clicks ({clicks}) cannot exceed impressions ({impressions})."
            )

        # Optional fields
        query = row[query_idx].strip() if query_idx is not None and len(row) > query_idx else None
        page = row[page_idx].strip() if page_idx is not None and len(row) > page_idx else None
        country = row[country_idx].strip() if country_idx is not None and len(row) > country_idx else None
        device = row[device_idx].strip() if device_idx is not None and len(row) > device_idx else None

        pos = None
        if pos_idx is not None and len(row) > pos_idx:
            pos = parse_position(row[pos_idx], row_idx)

        ctr = None
        if ctr_idx is not None and len(row) > ctr_idx:
            ctr = parse_ctr(row[ctr_idx], row_idx)
        elif impressions > 0:
            ctr = clicks / impressions
        else:
            ctr = 0.0

        # Duplicate checking
        if has_dimensions:
            dup_key = (
                dt,
                query.lower() if query else "",
                page.lower() if page else "",
                country.lower() if country else "",
                device.lower() if device else "",
            )
        else:
            dup_key = (dt,)

        if dup_key in seen_keys:
            raise ValueError(
                f"Duplicate row detected at line {row_idx} for key: {dup_key}."
            )
        seen_keys.add(dup_key)

        data_row = GscDataRow(
            date=dt,
            clicks=clicks,
            impressions=impressions,
            query=query or None,
            page=page or None,
            country=country or None,
            device=device or None,
            position=pos,
            ctr=ctr,
        )
        parsed_rows.append(data_row)

    if not parsed_rows:
        raise ValueError("CSV contains header but no valid data rows.")

    return parsed_rows, warnings
