from src.workflow.router import classify_query_multi


def test_multi_agent_chain():
    result = classify_query_multi(
        "Analyze my portfolio and compare it with market trends"
    )

    assert "portfolio" in result
    assert "market" in result


def test_goal_and_tax_chain():
    result = classify_query_multi(
        "Help me plan retirement and explain tax implications"
    )

    assert "goal" in result
    assert "tax" in result