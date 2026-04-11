from langchain_core.output_parsers import StrOutputParser
from core.router_agent_llm import RouterAgentLLM
from prompts.router_prompt import router_prompt

def create_router():
    """Creates a router for the finance assistant specialist agents."""

    # prompt_value = router_prompt.invoke({"query": user_message})
    # llm_output = llm.invoke(prompt_value)
    # decision = StrOutputParser().invoke(llm_output)
    router_chain = router_prompt | RouterAgentLLM().llm | StrOutputParser()

    def route_query(state):
        """Router function for LangGraph - decides which agent to call next"""

        # Get the latest user message
        user_message = state["messages"][-1].content

        print(f"🧭 Router analyzing: '{user_message[:50]}...'")

        try:
            # Get LLM routing decision
            decision = router_chain.invoke({"query": user_message}).strip().upper()
            # Map to our agent node names
            agent_mapping = {
                "FINANCE_QA": "finance_qa_agent",
                "GOAL_PLANNER": "goal_planner",
                "MARKET_ANALYZER": "market_analyzer",
                "NEWS_SYNTHESIZER": "news_synthesizer",
                "PORTFOLIO_ANALYZER": "portfolio_analyzer",
                "TAX_EDUCATOR": "tax_educator",
            }

            next_agent = agent_mapping.get(decision, "finance_qa_agent")
            print(f"🎯 Router decision: {decision} → {next_agent}")

            return decision, next_agent

        except Exception as e:
            print(f"⚠️ Router error, defaulting to finance_qa_agent: {e}")
            return "FINANCE_QA","finance_qa_agent"

    return route_query


