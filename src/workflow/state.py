
from typing import Any, Dict, List, Optional, TypedDict


class FinanceAssistantState(TypedDict, total=False):
    user_query: str
    query_type: str
    selected_agent: str
    messages: List[Dict[str, str]]

    portfolio_data: Dict[str, Any]
    portfolio_analysis: Dict[str, Any]

    market_data: Dict[str, Any]
    goal_data: Dict[str, Any]
    goal_plan: Dict[str, Any]

    news_data: List[Dict[str, Any]]
    retrieved_docs: List[Dict[str, Any]]

    response: str
    error: Optional[str]