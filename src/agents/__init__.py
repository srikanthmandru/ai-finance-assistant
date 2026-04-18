from src.agents.goal_agent import GoalAgent
from src.agents.market_agent import MarketAgent
from src.agents.news_agent import NewsAgent
from src.agents.portfolio_agent import PortfolioAgent
from src.agents.qa_agent import QAAgent
from src.agents.tax_agent import TaxAgent

from src.tools.portfolio_advisor import PortfolioAdvisor


def build_agents(retriever, llm, calculator, market_tool, planner, news_tool):
    advisor = PortfolioAdvisor()

    return {
        "qa": QAAgent(retriever, llm),

        "portfolio": PortfolioAgent(
            llm=llm,
            calculator=calculator,
            advisor=advisor,
        ),

        "market": MarketAgent(
            llm=llm,
            market_tool=market_tool,
        ),

        "goal": GoalAgent(
            llm=llm,
            planner=planner,
        ),

        "news": NewsAgent(news_tool, llm),
        "tax": TaxAgent(retriever, llm),
    }