import streamlit as st
import json

holdings = []

with open('src/data/sample_portfolios/holdings.json', 'r') as f:
    holdings = json.load(f)

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "portfolio_data" not in st.session_state:
        st.session_state.portfolio_data = {"holdings": holdings["holdings"]}

    if "goal_data" not in st.session_state:
        st.session_state.goal_data = {}

    if "market_history" not in st.session_state:
        st.session_state.market_history = []

    if "conversation_summary" not in st.session_state:
        st.session_state.conversation_summary = ""

    if "summary_message_count" not in st.session_state:
        st.session_state.summary_message_count = 0