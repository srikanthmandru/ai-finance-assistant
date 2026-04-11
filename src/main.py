from urllib import response

import gradio as gr
from langchain.messages import HumanMessage

# example_workflow_run.py
from src.agents import build_agents
from src.workflow.graph import build_graph

from src.tools.goal_planner import GoalPlanner
from src.tools.market_data_tool import MarketDataTool
from src.tools.portfolio_calculator import PortfolioCalculator

# Stub dependencies for now
retriever = ...
llm = ...
calculator = PortfolioCalculator()
market_tool = MarketDataTool()
planner = GoalPlanner()
news_tool = ...

agents = build_agents(
    retriever=retriever,
    llm=llm,
    calculator=calculator,
    market_tool=market_tool,
    planner=planner,
    news_tool=news_tool,
)

workflow = build_graph(agents)



def chat_with_agent(user_query, session_id="default"):
    """Multi-turn conversation with checkpoint memory.
    Processes user input and maintains session-based chat history.
    
    Args:
        user_query: The user's question or message
        session_id: Unique identifier for the conversation session
        
    Returns:
        str: The agent's response
    """
    try:
        # Configure session
        config = {"configurable": {"thread_id": session_id}}

        # initial_state: FinanceWorkflowState = {
        #     "user_query": user_query,
        #     "session_id": session_id,   
        #     "messages": [HumanMessage(content=user_query)],
        # }
        
        # # Invoke agent
        # response = finance_workflow.financial_assistant.invoke(
        #     initial_state,
        #     config=config
        # )


        initial_state = {
            "user_query": user_query,
            "messages": [],
            "portfolio_data": {
                "holdings": [
                    {"symbol": "VTI", "weight": 50},
                    {"symbol": "AAPL", "weight": 30},
                    {"symbol": "TSLA", "weight": 20},
                ]
            },
        }

        result = workflow.invoke(initial_state, config=config)
        response = result.get("response", "No response generated")

        # Extract response
        if response and "messages" in response:
            return response["messages"][-1].content
        else:
            return "Error: Unexpected response format"                      
                
    except Exception as e:
        return f"Error: {str(e)}"


with gr.Blocks() as app:
    gr.Markdown("# Finnie AI")
    gr.Markdown("A finance assistant MVP with routing, specialist agents, and session memory.")

    with gr.Row():
        input_box = gr.Textbox(
            label="Ask a finance question",
            placeholder="Example: How much should I save monthly to reach $100000 in 8 years?",
            lines=3,
        )

    with gr.Row():
        session_input = gr.Textbox(
            label="Session ID",
            placeholder="default",
            value="default",
        )

    output_box = gr.Textbox(label="Assistant Response", lines=14)
    submit_button = gr.Button("Submit")

    submit_button.click(
        chat_with_agent,
        inputs=[input_box, session_input],
        outputs=output_box,
    )


if __name__ == "__main__":
    app.launch(debug=True)
