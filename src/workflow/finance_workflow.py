from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, StateGraph

from agents.router_agent import router_agent_node
from src.agents.qa_agent import finance_qa_agent_node
from src.agents.goal_agent import goal_planner_agent_node
from src.agents.market_agent import market_analyzer_agent_node
from src.agents.news_agent import news_synthesizer_agent_node
from src.agents.portfolio_agent import portfolio_analyzer_agent_node
from src.agents.tax_agent import tax_educator_agent_node
from state.finance_workflow_state import FinanceWorkflowState


# Conditional routing function

def route_to_agent(state: FinanceWorkflowState) -> str:
    """Conditional edge function - routes to appropriate agent based on router decision"""

    next_agent = state.get("next_agent")

    valid_agents = {
        "finance_qa_agent",
        "goal_planner",
        "market_analyzer",
        "news_synthesizer",
        "portfolio_analyzer",
        "tax_educator",
    }

    if next_agent in valid_agents:
        return next_agent

    # Default fallback
    return "finance_qa_agent"
    
class FinanceWorkflow:
    def __init__(self) -> None:
        self.financial_assistant = self.build_workflow()

    def build_workflow(self):
        workflow_builder = StateGraph(FinanceWorkflowState)

        workflow_builder.add_node("router_agent", router_agent_node)
        workflow_builder.add_node("finance_qa_agent", finance_qa_agent_node)
        # workflow_builder.add_node("goal_planner", goal_planner_agent_node)
        # workflow_builder.add_node("market_analyzer", market_analyzer_agent_node)
        # workflow_builder.add_node("news_synthesizer", news_synthesizer_agent_node)
        # workflow_builder.add_node("portfolio_analyzer", portfolio_analyzer_agent_node)
        # workflow_builder.add_node("tax_educator", tax_educator_agent_node)

        workflow_builder.set_entry_point("router_agent")
        workflow_builder.add_conditional_edges(
            "router_agent",
            route_to_agent,
            {
                "finance_qa_agent": "finance_qa_agent",
                # "goal_planner": "goal_planner",
                # "market_analyzer": "market_analyzer",
                # "news_synthesizer": "news_synthesizer",
                # "portfolio_analyzer": "portfolio_analyzer",
                # "tax_educator": "tax_educator",
            },
        )

        for node_name in [
            "finance_qa_agent",
            # "goal_planner",
            # "market_analyzer",
            # "news_synthesizer",
            # "portfolio_analyzer",
            # "tax_educator",
        ]:
            workflow_builder.add_edge(node_name, END)

        return workflow_builder.compile(checkpointer=InMemorySaver())

    # def run_workflow(self, user_query: str, session_id: str = "default") -> dict:
    #     initial_state: FinanceWorkflowState = {
    #         "user_query": user_query,
    #         "session_id": session_id,
    #         "messages": [HumanMessage(content=user_query)],
    #     }
    #     config = {"configurable": {"thread_id": session_id}}
    #     return self.financial_assistant.invoke(initial_state, config=config)
