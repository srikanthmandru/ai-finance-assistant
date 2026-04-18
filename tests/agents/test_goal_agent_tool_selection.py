from src.agents.goal_agent import GoalAgent


class MockLLM:
    def __init__(self):
        self.calls = 0

    def invoke(self, prompt: str) -> str:
        self.calls += 1
        if self.calls == 1:
            return '{"tool_name": "calculate_future_value", "arguments": {"monthly_contribution": 500, "years": 10, "expected_return": 0.07}}'
        return "With $500 invested monthly for 10 years, the projected value grows over time."


class MockPlanner:
    def create_plan(self, goal_data):
        return {"summary": "Required monthly plan"}

    def calculate_future_value(self, goal_data):
        return {"summary": "Future value plan", "future_value": 86000}


def test_goal_agent_llm_selects_tool():
    agent = GoalAgent(llm=MockLLM(), planner=MockPlanner())

    state = {
        "user_query": "How much will I have if I invest 500 per month for 10 years?",
        "goal_data": {},
        "messages": [],
    }

    result = agent.run(state)

    assert result["goal_selected_tool"] == "calculate_future_value"
    assert result["response"].startswith("With $500")