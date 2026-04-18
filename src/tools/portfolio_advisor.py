# src/tools/portfolio_advisor.py
from typing import Dict, List


class PortfolioAdvisor:
    def suggest_educational_improvements(self, analysis: Dict) -> Dict:
        allocations: List[Dict] = analysis.get("allocations", [])
        top_holding = analysis.get("top_holding")
        risk_level = analysis.get("risk_level", "Unknown")
        asset_mix = analysis.get("asset_mix", {})

        suggestions = []

        if top_holding and top_holding.get("allocation_pct", 0) > 40:
            suggestions.append(
                f"The portfolio is concentrated in {top_holding['symbol']} at {top_holding['allocation_pct']:.2f}%."
            )

        if len(allocations) < 3:
            suggestions.append("The portfolio has limited diversification across holdings.")

        stock_like = asset_mix.get("Stock", 0) + asset_mix.get("ETF", 0)
        bond_like = asset_mix.get("Bond", 0) + asset_mix.get("Bond ETF", 0)

        if stock_like > 85:
            suggestions.append("The portfolio is heavily tilted toward equities, which may increase volatility.")

        if bond_like == 0:
            suggestions.append("There is no bond exposure, so the portfolio may be less defensive.")

        if not suggestions:
            suggestions.append("The portfolio appears reasonably balanced at a high level.")

        return {
            "risk_level": risk_level,
            "suggestions": suggestions,
            "summary": " ".join(suggestions),
        }