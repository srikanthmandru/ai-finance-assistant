from typing import Dict, List


def format_recent_messages(messages: List[Dict[str, str]], limit: int = 6) -> str:
    recent = messages[-limit:] if messages else []
    return "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in recent
    )


def should_summarize(messages: List[Dict[str, str]], threshold: int = 12) -> bool:
    return len(messages) >= threshold


def summarize_messages(llm, messages: List[Dict[str, str]], existing_summary: str = "") -> str:
    raw_history = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in messages
    )

    prompt = f"""
You are summarizing a finance assistant conversation.

Existing summary:
{existing_summary}

New conversation turns:
{raw_history}

Create a short summary capturing:
1. User goals
2. Risk tolerance
3. Portfolio details
4. Important follow-up context
5. Open questions

Keep it concise.
""".strip()

    return llm.invoke(prompt)