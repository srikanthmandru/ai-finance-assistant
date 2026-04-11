from src.agents.base_agent import BaseAgent
from src.workflow.state import FinanceAssistantState


class MarketAgent(BaseAgent):
    def __init__(self, market_tool):
        super().__init__("market")
        self.market_tool = market_tool

    def run(self, state: FinanceAssistantState) -> FinanceAssistantState:
        query = state.get("user_query", "")

        try:
            market_data = self.market_tool.get_market_summary(query)
        except Exception as exc:
            return {
                **state,
                "error": f"Market agent failed: {str(exc)}",
            }

        return {
            **state,
            "market_data": market_data,
            "response": market_data["summary"],
            "error": None,
        }