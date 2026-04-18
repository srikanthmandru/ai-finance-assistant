from langchain.messages import AIMessage
from langchain_openai import ChatOpenAI
import streamlit as st
from src.core.memory_manager import MemoryManager
from src.core.llm import OpenAILLM
from src.workflow import llm_router
from src.workflow.llm_router import LLMRouter
import os


from src.agents import build_agents
from src.constants import Constants
from src.rag.build_index import build_faiss_index
from src.rag.embeddings import EmbeddingService
from src.rag.retriever import FinanceRetriever
from src.tools.goal_planner import GoalPlanner
from src.tools.market_data_tool import MarketDataTool
from src.tools.portfolio_calculator import PortfolioCalculator
from src.web_app.charts import market_line_chart, portfolio_pie_chart
from src.web_app.components import (
    render_chat_messages,
    render_goal_summary,
    render_market_summary,
    render_portfolio_summary,
)
from src.web_app.session import init_session_state
from src.workflow.graph import build_graph
from src.utils.input_parser import parse_goal_from_query, parse_portfolio_from_query


class DummyLLM:
    def invoke(self, prompt: str) -> str:
        return "Sample response from LLM."


class DummyNewsTool:
    def get_latest_news(self, limit=5):
        return [{"title": "Market update", "summary": "Stocks moved higher today."}]


class DummyEmbeddingModel:
    def embed_documents(self, texts):
        return [[0.1] * 8 for _ in texts]

    def embed_query(self, query):
        return [0.1] * 8

def setup_app():
    embedding_model = DummyEmbeddingModel()
    vector_store = build_faiss_index("src/data/knowledge_base", embedding_model)
    embedding_service = EmbeddingService(embedding_model)
    retriever = FinanceRetriever(embedding_service, vector_store)

    llm = OpenAILLM(model="gpt-4.1-mini")
    llm_router = LLMRouter(llm=llm)
    calculator = PortfolioCalculator()
    market_tool = MarketDataTool()
    planner = GoalPlanner()
    news_tool = DummyNewsTool()
    memory_manager = MemoryManager(llm=llm, threshold=12, keep_recent=6)

    agents = build_agents(
        retriever=retriever,
        llm=llm,
        calculator=calculator,
        market_tool=market_tool,
        planner=planner,
        news_tool=news_tool,
    )

    app_graph = build_graph(agents)
    return app_graph, market_tool, calculator, planner, memory_manager, llm_router


def main():
    st.set_page_config(page_title="AI Finance Assistant", layout="wide")
    st.title("AI Finance Assistant")

    init_session_state()
    app_graph, market_tool, calculator, planner, memory_manager, llm_router = setup_app()

    tab1, tab2, tab3, tab4 = st.tabs(["Chat", "Portfolio", "Market", "Goals"])

    with tab1:
        st.subheader("Finance Chat")
        render_chat_messages(st.session_state.messages)

        user_input = st.chat_input("Ask a finance question")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            parsed_portfolio = parse_portfolio_from_query(user_input)
            parsed_goal = parse_goal_from_query(user_input)

            current_portfolio_data = (
                parsed_portfolio
                if parsed_portfolio.get("holdings")
                else st.session_state.portfolio_data
            )

            current_goal_data = (
                parsed_goal
                if parsed_goal.get("target_amount")
                else st.session_state.goal_data
            )

            state = {
                "user_query": user_input,
                "messages": st.session_state.messages,
                "portfolio_data": current_portfolio_data,
                "goal_data": current_goal_data,
                "conversation_summary": st.session_state.conversation_summary,
                "summary_message_count": st.session_state.summary_message_count,
                "user_profile": st.session_state.get("user_profile", {}),
                "portfolio_analysis": st.session_state.get("portfolio_analysis", {}),
                "goal_plan": st.session_state.get("goal_plan", {}),
                "market_data": st.session_state.get("market_data", {}),
                "llm_router": llm_router,
            }

            state = memory_manager.update_memory(state)

            result = app_graph.invoke(state)
            assistant_reply = result.get("response", "No response generated.")

            st.session_state.user_profile = result.get("user_profile", st.session_state.get("user_profile", {}))
            st.session_state.portfolio_analysis = result.get("portfolio_analysis", st.session_state.get("portfolio_analysis", {}))
            st.session_state.goal_plan = result.get("goal_plan", st.session_state.get("goal_plan", {}))
            
            if parsed_portfolio.get("holdings"):
                st.session_state.portfolio_data = parsed_portfolio

            if parsed_goal.get("target_amount"):
                st.session_state.goal_data = parsed_goal

            st.session_state.market_data = result.get("market_data", st.session_state.get("market_data", {}))

            st.session_state.messages = result.get("messages", state["messages"])
            st.session_state.conversation_summary = result.get(
                "conversation_summary",
                state.get("conversation_summary", ""),
            )
            st.session_state.summary_message_count = result.get(
                "summary_message_count",
                state.get("summary_message_count", 0),
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_reply}
            )
            st.rerun()

    with tab2:
        st.subheader("Portfolio Analysis")

        symbol = st.text_input("Symbol", value="VTI")
        quantity = st.number_input("Quantity", min_value=0.0, value=10.0)
        price = st.number_input("Price", min_value=0.0, value=250.0)
        asset_type = st.selectbox("Asset Type", ["ETF", "Stock", "Bond ETF", "Bond"])
        expense_ratio = st.number_input("Expense Ratio", min_value=0.0, value=0.03)

        if st.button("Add Holding"):
            st.session_state.portfolio_data["holdings"].append(
                {
                    "symbol": symbol,
                    "quantity": quantity,
                    "price": price,
                    "asset_type": asset_type,
                    "expense_ratio": expense_ratio,
                }
            )
            st.success("Holding added.")

        if st.button("Analyze Portfolio"):
            result = calculator.analyze(st.session_state.portfolio_data)
            render_portfolio_summary(result)

            fig = portfolio_pie_chart(result["allocations"])
            if fig:
                st.plotly_chart(fig, use_container_width=True)

            st.json(st.session_state.portfolio_data)

    with tab3:
        st.subheader("Market Overview")

        ticker = st.text_input("Ticker Symbol", value="AAPL")
        provider_note = st.caption("Uses Alpha Vantage first, then yfinance fallback.")

        if st.button("Get Market Data"):
            try:
                market_data = market_tool.get_quote(ticker.upper())
                history = market_tool.get_history(ticker.upper(), period="1mo")
                st.session_state.market_history = history

                render_market_summary(market_data)

                fig = market_line_chart(history)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as exc:
                st.error(f"Failed to fetch market data: {exc}")

    with tab4:
        st.subheader("Goal Planning")

        target_amount = st.number_input("Target Amount", min_value=0.0, value=50000.0)
        years = st.number_input("Years", min_value=1, value=5)
        expected_return = st.number_input("Expected Annual Return", min_value=0.0, value=0.07)

        if st.button("Create Goal Plan"):
            st.session_state.goal_data = {
                "target_amount": target_amount,
                "years": years,
                "expected_return": expected_return,
            }

            plan = planner.create_plan(st.session_state.goal_data)
            render_goal_summary(plan)


if __name__ == "__main__":
    main()