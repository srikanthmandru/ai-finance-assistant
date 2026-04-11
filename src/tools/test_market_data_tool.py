from src.tools.market_data_tool import MarketDataTool

tool = MarketDataTool(ttl_seconds=1800)

quote = tool.get_market_summary("What is the price of AAPL?")
print(quote["summary"])

history = tool.get_history("AAPL", period="1mo")
print(history[:3])