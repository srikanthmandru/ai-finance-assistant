from routers.finance_qa_router import create_router
from state.finance_workflow_state import FinanceWorkflowState

router = create_router()

def router_agent_node(state: FinanceWorkflowState) -> FinanceWorkflowState:
    """Router node - determines which agent should handle the query"""
    user_query = state["messages"][-1].content
    query_type, next_agent = router(state)

    return {
        "user_query": user_query,
        "query_type": query_type,
        "session_id": state["session_id"],
        "next_agent": next_agent,
        "messages": state["messages"],
    }
