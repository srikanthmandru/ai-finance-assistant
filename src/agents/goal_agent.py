from typing import Any, Dict, List

from src.agents.llm_tool_agent import LLMToolAgent
from src.workflow.state import FinanceAssistantState
from src.utils.input_parser import parse_goal_from_query


class GoalAgent(LLMToolAgent):
    def __init__(self, llm, planner):
        super().__init__("goal", llm)
        self.planner = planner

    def get_available_tools(self, state: FinanceAssistantState) -> List[Dict[str, Any]]:
        return [
            {
                "name": "create_plan",
                "description": "Calculate required monthly investment to reach a target amount",
                "arguments_schema": {
                    "target_amount": "float",
                    "years": "int",
                    "expected_return": "float",
                },
            },
            {
                "name": "calculate_future_value",
                "description": "Calculate future value from monthly contribution and time horizon",
                "arguments_schema": {
                    "monthly_contribution": "float",
                    "years": "int",
                    "expected_return": "float",
                    "current_amount": "float",
                },
            },
        ]

    def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        state: FinanceAssistantState,
    ) -> Dict[str, Any]:
        goal_data = dict(state.get("goal_data", {}))
        portfolio_analysis = state.get("portfolio_analysis", {})
        user_profile = state.get("user_profile", {})

        if portfolio_analysis:
            goal_data["current_portfolio_value"] = portfolio_analysis.get("total_value", 0)

        if user_profile.get("risk_tolerance"):
            goal_data["risk_tolerance"] = user_profile["risk_tolerance"]

        merged = {**parse_goal_from_query(state.get("user_query", "")), **goal_data, **arguments}

        if tool_name == "create_plan":
            return {
                "goal_data": merged,
                "goal_plan": self.planner.create_plan(merged),
            }

        if tool_name == "calculate_future_value":
            return {
                "goal_data": merged,
                "goal_plan": self.planner.calculate_future_value(merged),
            }

        raise ValueError(f"Unsupported goal tool: {tool_name}")

    def build_explanation_prompt(
        self,
        state: FinanceAssistantState,
        tool_name: str,
        tool_result: Dict[str, Any],
    ) -> str:
        query = state.get("user_query", "")
        history = self._format_messages(state.get("messages", []))

        return f"""
You are the Goal Planning Agent.

Recent conversation:
{history}

User query:
{query}

Selected tool:
{tool_name}

Tool result:
{tool_result}

Explain the result clearly and practically.
Do not provide personalized financial advice.
Keep it concise.
Include a short educational disclaimer.
""".strip()