from src.agents.market_agent import MarketAgent


class MockMarketTool:
    def get_market_summary(self, query):
        return {
            "ticker": "AAPL",
            "current_price": 200.0,
            "change_percent": 1.5,
            "summary": "AAPL price is $200.00",
        }


def test_market_agent_run():
    agent = MarketAgent(market_tool=MockMarketTool())

    state = {"user_query": "What is the price of AAPL?"}
    result = agent.run(state)

    assert result["market_data"]["ticker"] == "AAPL"
    assert result["response"] == "AAPL price is $200.00"
    assert result["error"] is None