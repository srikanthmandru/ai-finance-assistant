from src.tools.portfolio_calculator import PortfolioCalculator

portfolio_data = {
    "holdings": [
        {"symbol": "VTI", "quantity": 10, "price": 250.0, "asset_type": "ETF", "expense_ratio": 0.03},
        {"symbol": "AAPL", "quantity": 5, "price": 190.0, "asset_type": "Stock", "expense_ratio": 0.0},
        {"symbol": "BND", "quantity": 8, "price": 72.0, "asset_type": "Bond ETF", "expense_ratio": 0.04},
    ]
}

calculator = PortfolioCalculator()
result = calculator.analyze(portfolio_data)

print(result["summary"])
print(result["allocations"])
print(result["asset_mix"])