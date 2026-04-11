from src.agents.base_agent import BaseAgent
from src.workflow.state import FinanceAssistantState


class PortfolioAgent(BaseAgent):
    def __init__(self, calculator):
        super().__init__("portfolio")
        self.calculator = calculator

    def run(self, state: FinanceAssistantState) -> FinanceAssistantState:
        portfolio_data = state.get("portfolio_data", {})

        try:
            analysis = self.calculator.analyze(portfolio_data)
        except Exception as exc:
            return {
                **state,
                "error": f"Portfolio analysis failed: {str(exc)}",
            }

        return {
            **state,
            "portfolio_analysis": analysis,
            "response": analysis["summary"],
            "error": None,
        }