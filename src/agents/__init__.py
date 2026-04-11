
from src.agents.goal_planner_agent import GoalAgent
from src.agents.market_analyzer_agent import MarketAgent
from src.agents.news_synthesizer_agent import NewsAgent
from src.agents.portfolio_analyzer_agent import PortfolioAgent
from src.agents.finance_qa_agent import QAAgent
from src.agents.tax_educator_agent import TaxAgent


def build_agents(retriever, llm, calculator, market_tool, planner, news_tool):
    return {
        "qa": QAAgent(retriever, llm),
        "portfolio": PortfolioAgent(calculator),
        "market": MarketAgent(market_tool),
        "goal": GoalAgent(planner),
        "news": NewsAgent(news_tool, llm),
        "tax": TaxAgent(retriever, llm),
    }