from src.agents.market_agent import MarketAgent


class MockMarketTool:
    def get_portfolio_market_summary(self, tickers):
        return {
            "summary": "Portfolio market snapshot:\nAAPL: $200.00 (1.50%)",
            "quotes": [{"ticker": "AAPL", "current_price": 200.0, "change_percent": 1.5}],
        }

    def get_market_summary(self, query):
        return {
            "summary": "AAPL price is $200.00",
            "ticker": "AAPL",
            "current_price": 200.0,
            "change_percent": 1.5,
        }


def test_market_agent_uses_portfolio_holdings():
    agent = MarketAgent(market_tool=MockMarketTool())

    state = {
        "user_query": "How is my portfolio doing?",
        "portfolio_data": {
            "holdings": [
                {"symbol": "AAPL", "quantity": 5, "price": 190.0}
            ]
        },
    }

    result = agent.run(state)

    assert "Portfolio market snapshot" in result["response"]
    assert result["error"] is None