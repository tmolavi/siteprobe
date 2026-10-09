"""Constants and frozen windows for Google Algorithm Update Impact Triage."""

EVENT_NAME = "September 2026 Google Spam Update"

# Official rollout window declared by Google
ROLLOUT_START = "2026-09-24"
ROLLOUT_END = "2026-10-08"

# Frozen comparison windows
# PRE: 14 days (Thursday 2026-09-10 to Wednesday 2026-09-23)
PRE_WINDOW_START = "2026-09-10"
PRE_WINDOW_END = "2026-09-23"
PRE_WINDOW_DAYS = 14

# ROLLOUT: 14 days (Thursday 2026-09-24 to Wednesday 2026-10-07)
# Matched 14 days with identical weekday distribution to PRE window
ROLLOUT_WINDOW_START = "2026-09-24"
ROLLOUT_WINDOW_END = "2026-10-07"
ROLLOUT_WINDOW_DAYS = 14

# COMPLETION DAY: Recorded separately to avoid distorting matched 14-day cycles
COMPLETION_DATE = "2026-10-08"

# POST WINDOW: 14 days following completion (Thursday 2026-10-09 to Wednesday 2026-10-22)
# Note: As of 2026-10-09, this window is incomplete. Future observations must not be invented.
POST_WINDOW_START = "2026-10-09"
POST_WINDOW_END = "2026-10-22"
POST_WINDOW_DAYS = 14

# Diagnostic Classifications
DIAGNOSTIC_NO_CLEAR_CHANGE = "NO_CLEAR_CHANGE_OBSERVED"
DIAGNOSTIC_NO_CHANGE = DIAGNOSTIC_NO_CLEAR_CHANGE  # Canonical reference
DIAGNOSTIC_NO_MEANINGFUL_CHANGE = DIAGNOSTIC_NO_CLEAR_CHANGE  # Backward-compatible alias
DIAGNOSTIC_PERFORMANCE_CHANGE = "PERFORMANCE_CHANGE_OBSERVED"
DIAGNOSTIC_TECHNICAL_ISSUE = "TECHNICAL_ISSUE_OBSERVED"
DIAGNOSTIC_MANUAL_ACTION = "MANUAL_ACTION_REPORTED"
DIAGNOSTIC_INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

ALL_DIAGNOSTICS = [
    DIAGNOSTIC_NO_CLEAR_CHANGE,
    DIAGNOSTIC_PERFORMANCE_CHANGE,
    DIAGNOSTIC_TECHNICAL_ISSUE,
    DIAGNOSTIC_MANUAL_ACTION,
    DIAGNOSTIC_INSUFFICIENT_DATA,
]

STATUS_DATA_UNAVAILABLE = "DATA_UNAVAILABLE"

# Required and optional CSV columns
REQUIRED_COLUMNS = ["date", "clicks", "impressions"]
OPTIONAL_DIMENSIONS = ["query", "page", "country", "device", "position", "ctr"]

# Strict public claims guidance
DISCLAIMER_TEXT = (
    "SiteProbe provides a reproducible workflow for examining Search Console changes "
    "around Google's September 2026 spam update. Correlation does not prove causation. "
    "SiteProbe does not detect private Google spam classifiers or SpamBrain penalties, "
    "and does not label any site as spam."
)
