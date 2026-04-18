from src.workflow.router import classify_query


def test_router_portfolio_query():
    assert classify_query("Analyze my portfolio") == "portfolio"


def test_router_market_query():
    assert classify_query("What is the price of AAPL?") == "market"


def test_router_goal_query():
    assert classify_query("Help me save for retirement") == "goal"


def test_router_tax_query():
    assert classify_query("Explain capital gains tax") == "tax"


# def test_router_news_query():
#     assert classify_query("Summarize market news") == "news"


def test_router_default_query():
    assert classify_query("What is diversification?") == "qa"