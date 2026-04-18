from typing import Any, Dict, List

from src.agents.llm_tool_agent import LLMToolAgent
from src.workflow.state import FinanceAssistantState


class PortfolioAgent(LLMToolAgent):
    def __init__(self, llm, calculator, advisor):
        super().__init__("portfolio", llm)
        self.calculator = calculator
        self.advisor = advisor

    def get_available_tools(self, state: FinanceAssistantState) -> List[Dict[str, Any]]:
        return [
            {
                "name": "analyze_portfolio",
                "description": "Calculate allocations, diversification, and risk for the portfolio",
                "arguments_schema": {},
            },
            {
                "name": "suggest_improvements",
                "description": "Provide educational portfolio improvement guidance",
                "arguments_schema": {},
            },
        ]

    def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        state: FinanceAssistantState,
    ) -> Dict[str, Any]:
        portfolio_data = state.get("portfolio_data", {})
        holdings = portfolio_data.get("holdings", [])

        if not holdings:
            raise ValueError("No portfolio holdings found.")

        analysis = self.calculator.analyze(portfolio_data)

        if tool_name == "analyze_portfolio":
            return {"portfolio_analysis": analysis}

        if tool_name == "suggest_improvements":
            guidance = self.advisor.suggest_educational_improvements(analysis)
            return {
                "portfolio_analysis": analysis,
                "portfolio_guidance": guidance,
            }

        raise ValueError(f"Unsupported portfolio tool: {tool_name}")

    def build_explanation_prompt(
        self,
        state: FinanceAssistantState,
        tool_name: str,
        tool_result: Dict[str, Any],
    ) -> str:
        query = state.get("user_query", "")
        history = self._format_messages(state.get("messages", []))
        user_profile = state.get("user_profile", {})

        return f"""
You are the Portfolio Analysis Agent.

Recent conversation:
{history}

User query:
{query}

User profile:
{user_profile}

Selected tool:
{tool_name}

Tool result:
{tool_result}

Explain the portfolio clearly.
Mention diversification, concentration, and risk.
If guidance is present, explain it educationally.
Do not provide personalized financial advice.
Keep it concise.
""".strip()