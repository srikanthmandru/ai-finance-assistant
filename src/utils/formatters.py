from typing import List, Dict


def format_price_trend(history: List[Dict]) -> str:
    if not history:
        return "No historical data available."

    start = history[0]["close"]
    end = history[-1]["close"]
    change_pct = ((end - start) / start * 100) if start else 0.0

    return (
        f"Over the selected period, price moved from ${start:.2f} "
        f"to ${end:.2f}, a change of {change_pct:.2f}%."
    )