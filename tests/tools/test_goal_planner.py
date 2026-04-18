from src.tools.goal_planner import GoalPlanner


def test_goal_planner_create_plan():
    planner = GoalPlanner()

    goal_data = {
        "target_amount": 50000,
        "years": 5,
        "expected_return": 0.07,
    }

    result = planner.create_plan(goal_data)

    assert result["target_amount"] == 50000
    assert result["years"] == 5
    assert result["monthly_investment"] > 0
    assert "summary" in result