from typing import Dict, List

from src.agents.base_agent import BaseAgent
from src.rag.citation_formatter import format_sources
from src.utils.reference_resolver import build_followup_context
from src.workflow.state import FinanceAssistantState


class QAAgent(BaseAgent):
    def __init__(self, retriever, llm):
        super().__init__("qa")
        self.retriever = retriever
        self.llm = llm

    def _format_history(self, messages: List[Dict[str, str]], limit: int = 6) -> str:
        recent = messages[-limit:] if messages else []
        return "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in recent
        )

    def _build_prompt(
        self,
        query: str,
        docs: List[dict],
        messages: List[Dict[str, str]],
        conversation_summary: str,
        followup_context: str,
    ) -> str:
        history = self._format_history(messages)
        context = "\n\n".join(
            f"Source: {doc.get('source', 'unknown')}\nTitle: {doc.get('title', 'unknown')}\nContent: {doc.get('content', '')}"
            for doc in docs
        )

        return f"""
You are an AI Finance Assistant for educational purposes only.

Instructions:
- Answer clearly and concisely.
- Use recent conversation and follow-up context to resolve references like "that", "it", "those", or "earlier".
- If the question is a follow-up, connect it to the prior discussion naturally.
- Do not provide personalized financial advice.

Conversation summary:
{conversation_summary}

Recent conversation:
{history}

Follow-up context:
{followup_context}

User question:
{query}

Retrieved knowledge:
{context}

Return:
1. A direct answer
2. Short comparison or explanation if helpful
3. Sources section
""".strip()

    def run(self, state: FinanceAssistantState) -> FinanceAssistantState:
        query = state.get("user_query", "")
        messages = state.get("messages", [])
        conversation_summary = state.get("conversation_summary", "")
        followup_context = build_followup_context(state)

        retrieval_query = f"{query}\n\n{followup_context}" if followup_context else query
        docs = self.retriever.retrieve(retrieval_query, top_k=4)

        prompt = self._build_prompt(
            query=query,
            docs=docs,
            messages=messages,
            conversation_summary=conversation_summary,
            followup_context=followup_context,
        )

        answer = self.llm.invoke(prompt)
        sources = format_sources(docs)

        return {
            **state,
            "retrieved_docs": docs,
            "response": f"{answer}\n\n{sources}",
            "error": None,
        }