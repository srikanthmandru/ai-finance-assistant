from src.agents.goal_agent import GoalAgent
from src.tools.goal_planner import GoalPlanner


class MockPlanner:
    def create_plan(self, goal_data):
        return {
            "target_amount": 50000,
            "years": 5,
            "monthly_investment": 700,
            "summary": "Mock goal summary",
        }


def test_goal_agent_run():
    agent = GoalAgent(planner=MockPlanner())

    state = {
        "goal_data": {
            "target_amount": 50000,
            "years": 5,
            "expected_return": 0.07,
        }
    }

    result = agent.run(state)

    assert result["goal_plan"]["monthly_investment"] == 700
    assert result["response"] == "Mock goal summary"
    assert result["error"] is None

from src.agents.goal_agent import GoalAgent
from src.tools.goal_planner import GoalPlanner


def test_goal_agent_with_data():
    agent = GoalAgent(planner=GoalPlanner())

    state = {
        "goal_data": {
            "target_amount": 50000,
            "years": 5,
            "expected_return": 0.07,
        }
    }

    result = agent.run(state)
    assert "To target $50,000.00 in 5 years" in result["response"]