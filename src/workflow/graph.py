# src/workflow/graph.py
from langgraph.graph import END, START, StateGraph

from src.workflow.fallback import fallback_node
from src.workflow.nodes import make_agent_node, response_node
from src.workflow.router import route_after_agent, route_after_router, router_node
from src.workflow.state import FinanceAssistantState


def build_graph(agents):
    graph = StateGraph(FinanceAssistantState)

    graph.add_node("router", router_node)
    graph.add_node("qa", make_agent_node("qa", agents))
    graph.add_node("portfolio", make_agent_node("portfolio", agents))
    graph.add_node("market", make_agent_node("market", agents))
    graph.add_node("goal", make_agent_node("goal", agents))
    graph.add_node("news", make_agent_node("news", agents))
    graph.add_node("tax", make_agent_node("tax", agents))
    graph.add_node("fallback", fallback_node)
    graph.add_node("response", response_node)

    graph.add_edge(START, "router")

    graph.add_conditional_edges(
        "router",
        route_after_router,
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

    for node_name in ["qa", "portfolio", "market", "goal", "news", "tax"]:
        graph.add_conditional_edges(
            node_name,
            route_after_agent,
            {
                "qa": "qa",
                "portfolio": "portfolio",
                "market": "market",
                "goal": "goal",
                "news": "news",
                "tax": "tax",
                "response": "response",
                "fallback": "fallback",
            },
        )

    graph.add_edge("fallback", "response")
    graph.add_edge("response", END)

    return graph.compile()