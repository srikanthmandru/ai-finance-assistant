import os

class Constants:
    TEMPERATURE = 0.2
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    AGENT_LLM_MAP = {
        "router_agent": "gpt-4o-mini",
        "finance_qa_agent": "gemini-2.0-flash",
        "goal_planner": "gpt-4o-mini",
        "market_analyzer": "gpt-4o-mini",
        "news_synthesizer": "gpt-4o-mini",
        "portfolio_analyzer": "gpt-4o-mini",
        "tax_educator": "gpt-4o-mini",
    }

