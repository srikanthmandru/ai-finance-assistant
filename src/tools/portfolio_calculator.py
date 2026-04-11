from collections import defaultdict
from typing import Dict, List


class PortfolioCalculator:
    def calculate_total_value(self, holdings: List[Dict]) -> float:
        return round(sum(h["quantity"] * h["price"] for h in holdings), 2)

    def calculate_allocation_percentages(self, holdings: List[Dict], total_value: float) -> List[Dict]:
        allocations = []

        for h in holdings:
            value = h["quantity"] * h["price"]
            allocation_pct = round((value / total_value) * 100, 2) if total_value else 0.0

            allocations.append({
                "symbol": h["symbol"],
                "value": round(value, 2),
                "allocation_pct": allocation_pct,
                "asset_type": h.get("asset_type", "Unknown"),
                "expense_ratio": h.get("expense_ratio", 0.0),
            })

        return allocations

    def calculate_weighted_expense_ratio(self, allocations: List[Dict]) -> float:
        weighted = sum(
            item["allocation_pct"] * item.get("expense_ratio", 0.0)
            for item in allocations
        )
        return round(weighted / 100, 4)

    def calculate_asset_type_mix(self, allocations: List[Dict]) -> Dict[str, float]:
        mix = defaultdict(float)

        for item in allocations:
            mix[item["asset_type"]] += item["allocation_pct"]

        return {k: round(v, 2) for k, v in mix.items()}

    def calculate_diversification_score(self, allocations: List[Dict]) -> int:
        unique_symbols = len({item["symbol"] for item in allocations})
        unique_asset_types = len({item["asset_type"] for item in allocations})

        score = min(100, unique_symbols * 10 + unique_asset_types * 15)
        return score

    def assess_risk(self, asset_mix: Dict[str, float]) -> str:
        stock_pct = asset_mix.get("Stock", 0) + asset_mix.get("ETF", 0)
        bond_pct = asset_mix.get("Bond ETF", 0) + asset_mix.get("Bond", 0)

        if stock_pct >= 80:
            return "High"
        if stock_pct >= 60:
            return "Moderately High"
        if bond_pct >= 40:
            return "Moderate"
        return "Balanced"

    def build_summary(
        self,
        total_value: float,
        diversification_score: int,
        risk_level: str,
        weighted_expense_ratio: float,
    ) -> str:
        return (
            f"Portfolio value is ${total_value:,.2f}. "
            f"Diversification score is {diversification_score}/100. "
            f"Estimated risk level is {risk_level}. "
            f"Weighted expense ratio is {weighted_expense_ratio:.2f}%."
        )

    def analyze(self, portfolio_data: Dict) -> Dict:
        holdings = portfolio_data.get("holdings", [])
        if not holdings:
            raise ValueError("Portfolio holdings are missing.")

        total_value = self.calculate_total_value(holdings)
        allocations = self.calculate_allocation_percentages(holdings, total_value)
        asset_mix = self.calculate_asset_type_mix(allocations)
        diversification_score = self.calculate_diversification_score(allocations)
        risk_level = self.assess_risk(asset_mix)
        weighted_expense_ratio = self.calculate_weighted_expense_ratio(allocations)

        summary = self.build_summary(
            total_value=total_value,
            diversification_score=diversification_score,
            risk_level=risk_level,
            weighted_expense_ratio=weighted_expense_ratio,
        )

        return {
            "total_value": total_value,
            "allocations": allocations,
            "asset_mix": asset_mix,
            "diversification_score": diversification_score,
            "risk_level": risk_level,
            "weighted_expense_ratio": weighted_expense_ratio,
            "summary": summary,
        }