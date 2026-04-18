from src.tools.portfolio_calculator import PortfolioCalculator


def test_portfolio_calculator_analyze():
    calculator = PortfolioCalculator()

    portfolio_data = {
        "holdings": [
            {"symbol": "VTI", "quantity": 10, "price": 250.0, "asset_type": "ETF", "expense_ratio": 0.03},
            {"symbol": "AAPL", "quantity": 5, "price": 190.0, "asset_type": "Stock", "expense_ratio": 0.0},
            {"symbol": "BND", "quantity": 8, "price": 72.0, "asset_type": "Bond ETF", "expense_ratio": 0.04},
        ]
    }

    result = calculator.analyze(portfolio_data)

    assert result["total_value"] > 0
    assert "allocations" in result
    assert "risk_level" in result
    assert "summary" in result