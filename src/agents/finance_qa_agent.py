
from typing import List

from src.agents.base_agent import BaseAgent
from src.workflow.state import FinanceAssistantState
from src.rag.citation_formatter import format_sources


class QAAgent(BaseAgent):
    def __init__(self, retriever, llm):
        super().__init__("qa")
        self.retriever = retriever
        self.llm = llm

    def _build_prompt(self, query: str, docs: List[dict]) -> str:
        context = "\n\n".join(
            f"Source: {doc.get('source', 'unknown')}\nContent: {doc.get('content', '')}"
            for doc in docs
        )

        return f"""
            You are an AI Finance Assistant for educational purposes only.
            Answer clearly and simply.
            Do not give personalized financial advice.
            Use only the provided context when relevant.

            User question:
            {query}

            Retrieved context:
            {context}

            Return:
            1. A concise educational answer
            2. Key points if useful
            3. Mention that the answer is educational, not financial advice
            """.strip()


    def run(self, state: FinanceAssistantState) -> FinanceAssistantState:
        query = state.get("user_query", "")
        docs = self.retriever.retrieve(query, top_k=4)

        context = "\n\n".join(doc["content"] for doc in docs)

        prompt = f"""
            You are a finance education assistant.
            Answer clearly using the context below.
            Do not provide direct financial advice.

            Question: {query}

            Context:
            {context}
            """.strip()

        answer = self.llm.invoke(prompt)
        # Normalize LLM output to plain string
        if hasattr(answer, "content"):
            answer_text = answer.content
        elif isinstance(answer, dict) and "content" in answer:
            answer_text = answer["content"]
        else:
            answer_text = str(answer)
        sources = format_sources(docs)

        return {
            **state,
            "retrieved_docs": docs,
            "response": f"{answer_text}\n\n{sources}",
            "error": None,
        }
        


