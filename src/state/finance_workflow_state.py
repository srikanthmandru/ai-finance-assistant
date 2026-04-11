from typing import Annotated, List, Literal, Optional, TypedDict
import operator

from langchain_core.messages import BaseMessage

AgentName = Literal[
    "finance_qa_agent",
    "goal_planner",
    "market_analyzer",
    "news_synthesizer",
    "portfolio_analyzer",
    "tax_educator",
]


class FinanceWorkflowState(TypedDict, total=False):
    user_query: str # current input
    query_type: str # classified intent
    session_id: str # user session for memory
    messages: Annotated[List[BaseMessage], operator.add] # conversation history
    next_agent: AgentName # routing decision
    route_reason: Optional[str] # optional explanation for routing
    portfolio_data: dict # user portfolio info
    market_data: dict # relevant market info
    goal_data: dict # user financial goals
    retrieved_docs: list # retrieved knowledge base documents
    response: str # final agent response
    error: str # error message if any step fails
