from src.core.memory_manager import MemoryManager


class MockLLM:
    def invoke(self, prompt: str) -> str:
        return "User wants a retirement plan, moderate risk, and asked about ETFs."


def test_memory_manager_summarizes_long_chat():
    manager = MemoryManager(llm=MockLLM(), threshold=4, keep_recent=2)

    state = {
        "messages": [
            {"role": "user", "content": "I want to invest for retirement."},
            {"role": "assistant", "content": "What is your risk tolerance?"},
            {"role": "user", "content": "Moderate risk."},
            {"role": "assistant", "content": "Do you prefer ETFs?"},
            {"role": "user", "content": "Yes, mostly ETFs."},
        ],
        "conversation_summary": "",
    }

    result = manager.update_memory(state)

    assert result["conversation_summary"] != ""
    assert len(result["messages"]) == 2