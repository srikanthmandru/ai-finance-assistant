# src/utils/reference_resolver.py
from typing import Dict, List


def get_last_user_and_assistant_messages(messages: List[Dict[str, str]]) -> Dict[str, str]:
    last_user = ""
    last_assistant = ""

    for msg in reversed(messages):
        if msg["role"] == "assistant" and not last_assistant:
            last_assistant = msg["content"]
        elif msg["role"] == "user" and not last_user:
            last_user = msg["content"]

        if last_user and last_assistant:
            break

    return {
        "last_user_message": last_user,
        "last_assistant_message": last_assistant,
    }


def build_followup_context(state: Dict) -> str:
    messages = state.get("messages", [])
    conversation_summary = state.get("conversation_summary", "")
    portfolio_analysis = state.get("portfolio_analysis", {})
    goal_plan = state.get("goal_plan", {})
    market_data = state.get("market_data", {})
    user_profile = state.get("user_profile", {})

    recent_refs = get_last_user_and_assistant_messages(messages)

    sections = []

    if conversation_summary:
        sections.append(f"Conversation summary:\n{conversation_summary}")

    if recent_refs["last_user_message"]:
        sections.append(f"Last user message:\n{recent_refs['last_user_message']}")

    if recent_refs["last_assistant_message"]:
        sections.append(f"Last assistant message:\n{recent_refs['last_assistant_message']}")

    if portfolio_analysis:
        sections.append(f"Portfolio analysis:\n{portfolio_analysis.get('summary', '')}")

    if goal_plan:
        sections.append(f"Goal plan:\n{goal_plan.get('summary', '')}")

    if market_data:
        sections.append(f"Market context:\n{market_data.get('summary', '')}")

    if user_profile:
        sections.append(f"User profile:\n{user_profile}")

    return "\n\n".join(sections).strip()