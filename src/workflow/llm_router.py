import json
from typing import List


ALLOWED_AGENTS = {"qa", "portfolio", "market", "goal", "news", "tax"}


class LLMRouter:
    def __init__(self, llm):
        self.llm = llm

    def classify(self, query: str) -> List[str]:
        prompt = f"""
You are routing user queries for an AI Finance Assistant.

Available agents:
- qa: general finance education
- portfolio: portfolio analysis
- market: live market data and market trends
- goal: goal planning and projections
- news: financial news summarization
- tax: tax education

Return ONLY valid JSON in this format:
{{"agents": ["qa"]}}

Rules:
- Return 1 or more agents
- Use only these agent names: qa, portfolio, market, goal, news, tax
- If unsure, return ["qa"]

User query:
{query}
""".strip()

        raw = self.llm.invoke(prompt)

        try:
            parsed = json.loads(raw)
            agents = parsed.get("agents", ["qa"])
            agents = [a for a in agents if a in ALLOWED_AGENTS]
            return agents or ["qa"]
        except Exception:
            return ["qa"]