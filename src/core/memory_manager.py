from src.utils.conversation_memory import should_summarize, summarize_messages


class MemoryManager:
    def __init__(self, llm, threshold: int = 12, keep_recent: int = 6):
        self.llm = llm
        self.threshold = threshold
        self.keep_recent = keep_recent

    def update_memory(self, state: dict) -> dict:
        messages = state.get("messages", [])
        existing_summary = state.get("conversation_summary", "")

        if not should_summarize(messages, self.threshold):
            return state

        old_messages = messages[:-self.keep_recent]
        recent_messages = messages[-self.keep_recent:]

        if not old_messages:
            return state

        new_summary = summarize_messages(
            llm=self.llm,
            messages=old_messages,
            existing_summary=existing_summary,
        )

        return {
            **state,
            "conversation_summary": new_summary,
            "summary_message_count": len(old_messages),
            "messages": recent_messages,
        }