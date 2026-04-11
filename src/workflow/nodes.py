
from typing import Any, Callable, Dict

from src.workflow.state import FinanceAssistantState


def make_agent_node(agent_name: str, agents: Dict[str, Any]) -> Callable[[FinanceAssistantState], FinanceAssistantState]:
    def agent_node(state: FinanceAssistantState) -> FinanceAssistantState:
        try:
            agent = agents[agent_name]
            return agent.run(state)
        except Exception as exc:
            return {
                **state,
                "error": f"{agent_name} agent failed: {str(exc)}",
            }

    return agent_node


def response_node(state: FinanceAssistantState) -> FinanceAssistantState:
    response = state.get("response", "").strip()

    if not response:
        response = (
            "I could not generate a complete response. "
            "Please refine your question and try again."
        )

    if state.get("retrieved_docs"):
        response += "\n\nSources: available from retrieved knowledge base documents."

    response += "\n\nDisclaimer: This is for educational purposes only and not financial advice."

    return {
        **state,
        "response": response,
    }