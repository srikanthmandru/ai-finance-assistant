
from typing import List

from src.agents.base_agent import BaseAgent
from src.workflow.state import FinanceAssistantState


class TaxAgent(BaseAgent):
    def __init__(self, retriever, llm):
        super().__init__("tax")
        self.retriever = retriever
        self.llm = llm

    def _build_prompt(self, query: str, docs: List[dict]) -> str:
        context = "\n\n".join(
            f"Source: {doc.get('source', 'unknown')}\nContent: {doc.get('content', '')}"
            for doc in docs
        )

        return f"""
            You are an educational tax concepts assistant.
            Explain clearly for beginners.
            Do not provide legal or tax filing advice.

            Strict rule:
            - You only assist with finance-related educational questions.
            - If the request is not finance-related, refuse briefly.

            Question:
            {query}

            Context:
            {context}
            """.strip()

    def run(self, state: FinanceAssistantState) -> FinanceAssistantState:
        query = state.get("user_query", "")
        docs = self.retriever.retrieve(query, top_k=4)
        prompt = self._build_prompt(query, docs)
        answer = self.llm.invoke(prompt)
        # Normalize LLM output to plain string
        if hasattr(answer, "content"):
            answer_text = answer.content
        elif isinstance(answer, dict) and "content" in answer:
            answer_text = answer["content"]
        else:
            answer_text = str(answer)

        return {
            **state,
            "retrieved_docs": docs,
            "response": answer_text,
            "error": None,
        }