from langchain_core.output_parsers import StrOutputParser
from src.core.router_agent_llm import RouterAgentLLM
from src.prompts.router_prompt import router_prompt

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
                "qa": "qa",
                "goal": "goal",
                "market": "market",
                "news": "news",
                "portfolio": "portfolio",
                "tax": "tax",
            }

            next_agent = agent_mapping.get(decision, "finance_qa_agent")
            print(f"🎯 Router decision: {decision} → {next_agent}")

            return next_agent

        except Exception as e:
            print(f"⚠️ Router error, defaulting to finance_qa_agent: {e}")
            return "qa"

    return route_query


