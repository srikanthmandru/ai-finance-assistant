import streamlit as st

import os


from src.agents import build_agents
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

    llm = DummyLLM()
    calculator = PortfolioCalculator()
    market_tool = MarketDataTool()
    planner = GoalPlanner()
    news_tool = DummyNewsTool()

    agents = build_agents(
        retriever=retriever,
        llm=llm,
        calculator=calculator,
        market_tool=market_tool,
        planner=planner,
        news_tool=news_tool,
    )

    app_graph = build_graph(agents)
    return app_graph, market_tool, calculator, planner


def main():
    st.set_page_config(page_title="Finnie AI", layout="wide")
    st.title("Finnie AI - Your Personal Finance Assistant")

    init_session_state()
    app_graph, market_tool, calculator, planner = setup_app()

    tab1, tab2, tab3, tab4 = st.tabs(["Chat", "Portfolio", "Market", "Goals"])

    with tab1:
        st.subheader("Finance Chat")
        render_chat_messages(st.session_state.messages)

        user_input = st.chat_input("Ask a finance question")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            state = {
                "user_query": user_input,
                "messages": st.session_state.messages,
                "portfolio_data": st.session_state.portfolio_data,
                "goal_data": st.session_state.goal_data,
            }

            result = app_graph.invoke(state)
            assistant_reply = result.get("response", "No response generated.")

            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
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
        if st.button("Get Market Data"):
            market_data = market_tool.get_quote(ticker)
            history = market_tool.get_history(ticker, period="1mo")
            st.session_state.market_history = history

            render_market_summary(market_data)

            fig = market_line_chart(history)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

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