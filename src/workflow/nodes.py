# src/workflow/nodes.py
from typing import Any, Callable, Dict

from src.workflow.state import FinanceAssistantState


def make_agent_node(agent_name: str, agents: Dict[str, Any]) -> Callable[[FinanceAssistantState], FinanceAssistantState]:
    def agent_node(state: FinanceAssistantState) -> FinanceAssistantState:
        try:
            agent = agents[agent_name]
            result = agent.run(state)

            outputs = dict(state.get("agent_outputs", {}))
            outputs[agent_name] = result.get("response", "")

            current_index = state.get("current_agent_index", 0)
            next_index = current_index + 1

            return {
                **result,
                "agent_outputs": outputs,
                "current_agent_index": next_index,
            }
        except Exception as exc:
            return {
                **state,
                "error": f"{agent_name} agent failed: {str(exc)}",
            }

    return agent_node


def response_node(state: FinanceAssistantState) -> FinanceAssistantState:
    outputs = state.get("agent_outputs", {})

    if outputs:
        sections = []
        ordered_agents = state.get("agent_chain", [])

        for agent_name in ordered_agents:
            if agent_name in outputs:
                title = agent_name.replace("_", " ").title()
                sections.append(f"### {title}\n{outputs[agent_name]}")

        final_response = "\n\n".join(sections)
    else:
        final_response = state.get("response", "").strip()

    if not final_response:
        final_response = "I could not generate a complete response."

    final_response += (
        "\n\nDisclaimer: This assistant is for educational purposes only and does not provide financial advice."
    )

    return {
        **state,
        "response": final_response,
    }