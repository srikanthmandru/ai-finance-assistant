
from langgraph.graph import END, START, StateGraph

from src.workflow.fallback import fallback_node
from src.workflow.nodes import make_agent_node, response_node
from src.workflow.router import route_to_agent, router_node
from src.workflow.state import FinanceAssistantState


def build_graph(agents):
    graph = StateGraph(FinanceAssistantState)

    # Core nodes
    graph.add_node("router", router_node)
    graph.add_node("qa", make_agent_node("qa", agents))
    graph.add_node("portfolio", make_agent_node("portfolio", agents))
    graph.add_node("market", make_agent_node("market", agents))
    graph.add_node("goal", make_agent_node("goal", agents))
    graph.add_node("news", make_agent_node("news", agents))
    graph.add_node("tax", make_agent_node("tax", agents))
    graph.add_node("fallback", fallback_node)
    graph.add_node("response", response_node)

    # Start
    graph.add_edge(START, "router")

    # Conditional routing
    graph.add_conditional_edges(
        "router",
        route_to_agent,
        {
            "qa": "qa",
            "portfolio": "portfolio",
            "market": "market",
            "goal": "goal",
            "news": "news",
            "tax": "tax",
            "fallback": "fallback",
        },
    )

    # Success path
    graph.add_edge("qa", "response")
    graph.add_edge("portfolio", "response")
    graph.add_edge("market", "response")
    graph.add_edge("goal", "response")
    graph.add_edge("news", "response")
    graph.add_edge("tax", "response")

    # Error path
    graph.add_edge("fallback", "response")

    # End
    graph.add_edge("response", END)

    return graph.compile()