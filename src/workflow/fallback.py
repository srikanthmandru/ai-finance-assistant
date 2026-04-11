
from src.workflow.state import FinanceAssistantState


def fallback_node(state: FinanceAssistantState) -> FinanceAssistantState:
    error = state.get("error") or "Unknown error"

    safe_response = (
        "I could not fully process that request. "
        "Please try again with a clearer finance question, portfolio input, or ticker symbol. "
        "This assistant provides educational guidance only, not financial advice."
    )

    return {
        **state,
        "response": safe_response,
        "error": error,
    }