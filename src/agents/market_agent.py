from typing import Any, Dict, List

from src.agents.llm_tool_agent import LLMToolAgent
from src.workflow.state import FinanceAssistantState
from src.utils.input_parser import parse_ticker_from_query


class MarketAgent(LLMToolAgent):
    def __init__(self, llm, market_tool):
        super().__init__("market", llm)
        self.market_tool = market_tool

    def get_available_tools(self, state: FinanceAssistantState) -> List[Dict[str, Any]]:
        return [
            {
                "name": "get_quote",
                "description": "Get current market quote for a ticker",
                "arguments_schema": {"ticker": "str"},
            },
            {
                "name": "get_trend_summary",
                "description": "Get recent market trend summary for a ticker and period",
                "arguments_schema": {"ticker": "str", "period": "str"},
            },
            {
                "name": "get_portfolio_market_summary",
                "description": "Get market snapshot for portfolio holdings",
                "arguments_schema": {"tickers": ["str"]},
            },
        ]

    def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        state: FinanceAssistantState,
    ) -> Dict[str, Any]:
        if tool_name == "get_quote":
            ticker = arguments.get("ticker") or parse_ticker_from_query(state["user_query"]) or self.market_tool._extract_ticker(state["user_query"])
            return {"market_data": self.market_tool.get_quote(ticker)}

        if tool_name == "get_trend_summary":
            ticker = arguments.get("ticker") or parse_ticker_from_query(state["user_query"]) or self.market_tool._extract_ticker(state["user_query"])
            period = arguments.get("period", "1mo")
            trend = self.market_tool.get_trend_summary(ticker, period=period)
            return {
                "market_data": {"ticker": ticker},
                "market_trend": trend,
                "market_history": trend.get("history", []),
            }

        if tool_name == "get_portfolio_market_summary":
            tickers = arguments.get("tickers")
            if not tickers:
                tickers = [
                    h.get("symbol")
                    for h in state.get("portfolio_data", {}).get("holdings", [])
                    if h.get("symbol")
                ]
            return {"market_data": self.market_tool.get_portfolio_market_summary(tickers[:5])}

        raise ValueError(f"Unsupported market tool: {tool_name}")

    def build_explanation_prompt(
        self,
        state: FinanceAssistantState,
        tool_name: str,
        tool_result: Dict[str, Any],
    ) -> str:
        query = state.get("user_query", "")
        history = self._format_messages(state.get("messages", []))

        return f"""
You are the Market Analysis Agent.

Strict rule:
- You only assist with finance-related educational questions.
- If the request is not finance-related, refuse briefly.

Recent conversation:
{history}

User query:
{query}

Selected tool:
{tool_name}

Tool result:
{tool_result}

Explain the result clearly for a beginner.
Do not provide buy/sell advice.
Keep it concise.
Include a short educational disclaimer.
""".strip()