from src.agents.portfolio_agent import PortfolioAgent
from src.tools.portfolio_calculator import PortfolioCalculator


class MockCalculator:
    def analyze(self, portfolio_data):
        return {
            "total_value": 1000,
            "allocations": [],
            "risk_level": "Moderate",
            "summary": "Mock portfolio summary",
        }


def test_portfolio_agent_run():
    agent = PortfolioAgent(calculator=MockCalculator())

    state = {
        "portfolio_data": {
            "holdings": [
                {"symbol": "VTI", "quantity": 1, "price": 100, "asset_type": "ETF", "expense_ratio": 0.03}
            ]
        }
    }

    result = agent.run(state)

    assert result["portfolio_analysis"]["total_value"] == 1000
    assert result["response"] == "Mock portfolio summary"
    assert result["error"] is None

from src.agents.portfolio_agent import PortfolioAgent
from src.tools.portfolio_calculator import PortfolioCalculator


def test_portfolio_agent_with_holdings():
    agent = PortfolioAgent(calculator=PortfolioCalculator())

    state = {
        "portfolio_data": {
            "holdings": [
                {"symbol": "VTI", "quantity": 10, "price": 250.0, "asset_type": "ETF", "expense_ratio": 0.03},
                {"symbol": "AAPL", "quantity": 5, "price": 190.0, "asset_type": "Stock", "expense_ratio": 0.0},
            ]
        }
    }

    result = agent.run(state)
    assert "Portfolio value is" in result["response"]