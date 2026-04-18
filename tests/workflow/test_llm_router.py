from src.workflow.llm_router import LLMRouter


class MockLLM:
    def invoke(self, prompt: str) -> str:
        return '{"agents": ["portfolio", "market"]}'


def test_llm_router_returns_agent_chain():
    router = LLMRouter(llm=MockLLM())
    result = router.classify("Analyze my portfolio and compare market trends")

    assert result == ["portfolio", "market"]