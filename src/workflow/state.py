from typing import Any, Dict, List, Optional, TypedDict


class FinanceAssistantState(TypedDict, total=False):
    user_query: str
    query_type: str
    selected_agent: str
    messages: List[Dict[str, str]]

    user_profile: Dict[str, Any]

    agent_chain: List[str]
    current_agent_index: int
    agent_outputs: Dict[str, str]

    portfolio_data: Dict[str, Any]
    portfolio_analysis: Dict[str, Any]

    market_data: Dict[str, Any]
    goal_data: Dict[str, Any]
    goal_plan: Dict[str, Any]

    news_data: List[Dict[str, Any]]
    retrieved_docs: List[Dict[str, Any]]

    conversation_summary: str
    summary_message_count: int

    llm_router: Any
    llm_guardrail: Any
    guardrail_result: Dict[str, Any]
    guardrail_blocked: bool

    response: str
    error: Optional[str]