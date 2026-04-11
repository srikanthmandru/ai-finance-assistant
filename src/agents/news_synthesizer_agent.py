
from src.agents.base_agent import BaseAgent
from src.workflow.state import FinanceAssistantState


class NewsAgent(BaseAgent):
    def __init__(self, news_tool, llm):
        super().__init__("news")
        self.news_tool = news_tool
        self.llm = llm

    def run(self, state: FinanceAssistantState) -> FinanceAssistantState:
        try:
            articles = self.news_tool.get_latest_news(limit=5)
        except Exception as exc:
            return {
                **state,
                "error": f"News fetch failed: {str(exc)}",
            }

        article_text = "\n".join(
            f"- {article.get('title', '')}: {article.get('summary', '')}"
            for article in articles
        )

        prompt = f"""
Summarize the following financial news for a beginner investor.
Keep it short, clear, and educational.

News:
{article_text}
""".strip()

        summary = self.llm.invoke(prompt)

        return {
            **state,
            "news_data": articles,
            "response": summary,
            "error": None,
        }