"""Code related with dealing with legacy / change management"""
from typing import Any, Dict


def update_time_range(form_data: Dict[str, Any]) -> None:
    """Move since and until to time_range."""
    if "since" in form_data or "until" in form_data:
        form_data["time_range"] = "{} : {}".format(
            form_data.pop("since", "") or "", form_data.pop("until", "") or ""
        )
