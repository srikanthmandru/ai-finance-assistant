
from typing import Literal

from src.workflow.state import FinanceAssistantState


AgentType = Literal["qa", "portfolio", "market", "goal", "news", "tax"]


def classify_query(query: str) -> AgentType:
    q = query.lower()

    if any(word in q for word in ["portfolio", "allocation", "diversified", "rebalance", "holdings"]):
        return "portfolio"

    if any(word in q for word in ["stock", "market", "price", "ticker", "trend", "share"]):
        return "market"

    if any(word in q for word in ["goal", "save", "retirement", "plan", "future value"]):
        return "goal"

    if any(word in q for word in ["tax", "401k", "ira", "capital gains", "deduction"]):
        return "tax"

    if any(word in q for word in ["news", "headline", "update", "recent market news"]):
        return "news"

    return "qa"


def router_node(state: FinanceAssistantState) -> FinanceAssistantState:
    query = state.get("user_query", "").strip()

    if not query:
        return {
            **state,
            "query_type": "qa",
            "selected_agent": "qa",
            "error": "Empty query received.",
        }

    agent_type = classify_query(query)

    return {
        **state,
        "query_type": agent_type,
        "selected_agent": agent_type,
        "error": None,
    }


def route_to_agent(state: FinanceAssistantState) -> str:
    if state.get("error"):
        return "fallback"

    return state.get("selected_agent", "qa")