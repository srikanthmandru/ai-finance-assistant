import streamlit as st


def render_chat_messages(messages):
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def render_portfolio_summary(analysis: dict):
    st.subheader("Portfolio Summary")
    st.write(f"Total Value: ${analysis.get('total_value', 0):,.2f}")
    st.write(f"Diversification Score: {analysis.get('diversification_score', 0)}")
    st.write(f"Risk Level: {analysis.get('risk_level', 'N/A')}")
    st.write(f"Weighted Expense Ratio: {analysis.get('weighted_expense_ratio', 0):.2f}%")
    st.write(analysis.get("summary", ""))


def render_market_summary(market_data: dict):
    st.subheader("Market Summary")
    st.write(f"Ticker: {market_data.get('ticker', 'N/A')}")
    st.write(f"Current Price: ${market_data.get('current_price', 0):.2f}")
    st.write(f"Change: {market_data.get('change_percent', 0):.2f}%")
    st.write(f"From Cache: {market_data.get('from_cache', False)}")
    st.write(market_data.get("summary", ""))


def render_goal_summary(goal_plan: dict):
    st.subheader("Goal Plan")
    st.write(f"Target Amount: ${goal_plan.get('target_amount', 0):,.2f}")
    st.write(f"Years: {goal_plan.get('years', 0)}")
    st.write(f"Monthly Investment Needed: ${goal_plan.get('monthly_investment', 0):,.2f}")
    st.write(goal_plan.get("summary", ""))