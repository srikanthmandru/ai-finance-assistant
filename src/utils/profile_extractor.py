import re
from typing import Dict


def update_user_profile(profile: Dict, query: str) -> Dict:
    updated = dict(profile or {})
    q = query.lower()

    if "low risk" in q or "conservative" in q:
        updated["risk_tolerance"] = "low"
    elif "moderate risk" in q or "moderate" in q:
        updated["risk_tolerance"] = "moderate"
    elif "high risk" in q or "aggressive" in q:
        updated["risk_tolerance"] = "high"

    years_match = re.search(r"(\d+)\s+years?", q)
    if years_match:
        updated["time_horizon_years"] = int(years_match.group(1))

    if "retirement" in q:
        updated["goal_type"] = "retirement"
    elif "house" in q or "home" in q:
        updated["goal_type"] = "house"
    elif "education" in q:
        updated["goal_type"] = "education"

    return updated