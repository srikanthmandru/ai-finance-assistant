import streamlit as st


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "portfolio_data" not in st.session_state:
        st.session_state.portfolio_data = {"holdings": []}

    if "goal_data" not in st.session_state:
        st.session_state.goal_data = {}

    if "market_history" not in st.session_state:
        st.session_state.market_history = []