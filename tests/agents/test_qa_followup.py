from src.agents.qa_agent import QAAgent


class MockRetriever:
    def retrieve(self, query, top_k=4):
        return [
            {
                "title": "ETF Basics",
                "source": "Investopedia",
                "content": "ETFs are diversified funds that trade like stocks.",
            },
            {
                "title": "Bond Basics",
                "source": "Investor.gov",
                "content": "Bonds are generally lower risk than stocks but may offer lower returns.",
            },
        ]


class MockLLM:
    def invoke(self, prompt):
        assert "Last assistant message" in prompt
        assert "Compare it with bonds" in prompt
        return "Compared with bonds, ETFs can offer broader equity exposure and usually higher growth potential, but often with higher volatility."


def test_qa_agent_followup_uses_context():
    agent = QAAgent(retriever=MockRetriever(), llm=MockLLM())

    state = {
        "user_query": "Compare it with bonds",
        "messages": [
            {"role": "user", "content": "What is an ETF?"},
            {"role": "assistant", "content": "An ETF is a fund that holds a basket of assets and trades like a stock."},
            {"role": "user", "content": "Compare it with bonds"},
        ],
        "conversation_summary": "User asked about ETFs.",
    }

    result = agent.run(state)

    assert "Compared with bonds" in result["response"]
    assert result["error"] is None