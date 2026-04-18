# src/agents/llm_tool_agent.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.agents.base_agent import BaseAgent
from src.agents.tool_selection import ToolSelector
from src.workflow.state import FinanceAssistantState


class LLMToolAgent(BaseAgent, ABC):
    def __init__(self, name: str, llm):
        super().__init__(name)
        self.llm = llm
        self.tool_selector = ToolSelector(llm)

    def _format_messages(self, messages: List[Dict[str, str]], limit: int = 6) -> str:
        recent = messages[-limit:] if messages else []
        return "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in recent
        )

    @abstractmethod
    def get_available_tools(self, state: FinanceAssistantState) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        state: FinanceAssistantState,
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def build_explanation_prompt(
        self,
        state: FinanceAssistantState,
        tool_name: str,
        tool_result: Dict[str, Any],
    ) -> str:
        pass

    def run(self, state: FinanceAssistantState) -> FinanceAssistantState:
        try:
            tools = self.get_available_tools(state)

            selection = self.tool_selector.select_tool(
                agent_name=self.name,
                user_query=state.get("user_query", ""),
                available_tools=tools,
                extra_context={
                    "user_profile": state.get("user_profile", {}),
                    "portfolio_data": state.get("portfolio_data", {}),
                    "goal_data": state.get("goal_data", {}),
                },
            )

            tool_name = selection["tool_name"]
            arguments = selection.get("arguments", {})

            tool_result = self.execute_tool(tool_name, arguments, state)
            prompt = self.build_explanation_prompt(state, tool_name, tool_result)
            answer = self.llm.invoke(prompt)

            return {
                **state,
                **tool_result,
                f"{self.name}_selected_tool": tool_name,
                "response": answer,
                "error": None,
            }
        except Exception as exc:
            return {
                **state,
                "response": f"{self.name} agent failed: {str(exc)}",
                "error": None,
            }