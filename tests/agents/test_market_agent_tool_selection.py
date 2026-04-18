from src.agents.market_agent import MarketAgent


class MockLLM:
    def __init__(self):
        self.calls = 0

    def invoke(self, prompt: str) -> str:
        self.calls += 1
        if self.calls == 1:
            return '{"tool_name": "get_trend_summary", "arguments": {"ticker": "AAPL", "period": "1mo"}}'
        return "AAPL has shown a recent upward trend over the past month."


class MockMarketTool:
    def get_quote(self, ticker):
        return {"ticker": ticker, "current_price": 200}

    def get_trend_summary(self, ticker, period="1mo"):
        return {"ticker": ticker, "period": period, "trend_summary": "Up 5%", "history": []}

    def get_portfolio_market_summary(self, tickers):
        return {"summary": "Portfolio snapshot"}


def test_market_agent_llm_selects_trend_tool():
    agent = MarketAgent(llm=MockLLM(), market_tool=MockMarketTool())

    state = {
        "user_query": "Show me the trend for AAPL over the last month",
        "messages": [],
    }

    result = agent.run(state)

    assert result["market_selected_tool"] == "get_trend_summary"
    assert "upward trend" in result["response"].lower()