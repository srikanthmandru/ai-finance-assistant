
from src.agents.base_agent import BaseAgent
from src.workflow.state import FinanceAssistantState


class GoalAgent(BaseAgent):
    def __init__(self, planner):
        super().__init__("goal")
        self.planner = planner

    def run(self, state: FinanceAssistantState) -> FinanceAssistantState:
        goal_data = state.get("goal_data", {})

        if not goal_data:
            return {
                **state,
                "error": "Goal data is missing.",
            }

        plan = self.planner.create_plan(goal_data)

        return {
            **state,
            "goal_plan": plan,
            "response": plan["summary"],
            "error": None,
        }