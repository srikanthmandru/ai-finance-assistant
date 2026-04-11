
from typing import Dict


class GoalPlanner:
    def create_plan(self, goal_data: Dict) -> Dict:
        target_amount = float(goal_data.get("target_amount", 0))
        years = int(goal_data.get("years", 1))
        expected_return = float(goal_data.get("expected_return", 0.07))

        months = years * 12
        monthly_rate = expected_return / 12

        if monthly_rate == 0:
            monthly_investment = target_amount / months
        else:
            monthly_investment = target_amount * monthly_rate / ((1 + monthly_rate) ** months - 1)

        summary = (
            f"To target ${target_amount:,.2f} in {years} years, "
            f"you may need to invest about ${monthly_investment:,.2f} per month "
            f"at an assumed annual return of {expected_return * 100:.1f}%."
        )

        return {
            "target_amount": target_amount,
            "years": years,
            "monthly_investment": round(monthly_investment, 2),
            "summary": summary,
        }