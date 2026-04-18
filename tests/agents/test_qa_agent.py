from src.agents.qa_agent import QAAgent


class MockRetriever:
    def retrieve(self, query, top_k=4):
        return [
            {
                "title": "What Is Diversification?",
                "source": "Investopedia",
                "content": "Diversification spreads investments across assets.",
            }
        ]


class MockLLM:
    def invoke(self, prompt):
        return "Diversification means spreading investments across assets."


def test_qa_agent_run():
    agent = QAAgent(retriever=MockRetriever(), llm=MockLLM())

    state = {"user_query": "What is diversification?"}
    result = agent.run(state)

    assert len(result["retrieved_docs"]) == 1
    assert "Diversification" in result["response"]
    assert result["error"] is None