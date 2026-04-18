# src/agents/tool_selection.py
import json
from typing import Any, Dict, List


class ToolSelector:
    def __init__(self, llm):
        self.llm = llm

    def select_tool(
        self,
        agent_name: str,
        user_query: str,
        available_tools: List[Dict[str, Any]],
        extra_context: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        prompt = f"""
You are selecting the best tool for the {agent_name} agent.

User query:
{user_query}

Available tools:
{json.dumps(available_tools, indent=2)}

Extra context:
{json.dumps(extra_context or {}, indent=2)}

Return ONLY valid JSON in this format:
{{
  "tool_name": "tool_name_here",
  "arguments": {{}}
}}

Rules:
- Use only one tool
- Use only listed tool names
- Arguments must match the tool purpose
- If unsure, choose the safest most relevant tool
""".strip()

        raw = self.llm.invoke(prompt)

        try:
            parsed = json.loads(raw)
            return {
                "tool_name": parsed["tool_name"],
                "arguments": parsed.get("arguments", {}),
            }
        except Exception:
            return {
                "tool_name": available_tools[0]["name"],
                "arguments": {},
            }