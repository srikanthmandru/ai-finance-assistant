from src.utils.profile_extractor import update_user_profile
from src.workflow.state import FinanceAssistantState


def router_node(state: FinanceAssistantState) -> FinanceAssistantState:
    query = state.get("user_query", "").strip()
    profile = state.get("user_profile", {})
    llm_router = state.get("llm_router")
    llm_guardrail = state.get("llm_guardrail")

    if not query:
        return {
            **state,
            "query_type": "qa",
            "selected_agent": "qa",
            "agent_chain": ["qa"],
            "current_agent_index": 0,
            "agent_outputs": {},
            "error": "Empty query received.",
        }

    if llm_guardrail:
        guardrail_result = llm_guardrail.evaluate(query)

        if not guardrail_result["allowed"]:
            return {
                **state,
                "guardrail_result": guardrail_result,
                "guardrail_blocked": True,
                "response": llm_guardrail.rejection_message(guardrail_result["reason"]),
                "agent_chain": [],
                "agent_outputs": {},
                "error": None,
            }
    else:
        guardrail_result = {
            "allowed": True,
            "reason": "finance_related",
            "confidence": 1.0,
        }

    if llm_router:
        agent_chain = llm_router.classify(query)
    else:
        agent_chain = ["qa"]

    updated_profile = update_user_profile(profile, query)

    return {
        **state,
        "query_type": agent_chain[0],
        "selected_agent": agent_chain[0],
        "agent_chain": agent_chain,
        "current_agent_index": 0,
        "agent_outputs": {},
        "user_profile": updated_profile,
        "guardrail_result": guardrail_result,
        "guardrail_blocked": False,
        "error": None,
    }


def route_after_router(state: FinanceAssistantState) -> str:
    if state.get("guardrail_blocked"):
        return "response"

    if state.get("error"):
        return "fallback"

    return state.get("selected_agent", "qa")


def route_after_agent(state: FinanceAssistantState) -> str:
    if state.get("error"):
        return "fallback"

    chain = state.get("agent_chain", [])
    next_index = state.get("current_agent_index", 0)

    if next_index < len(chain):
        return chain[next_index]

    return "response"