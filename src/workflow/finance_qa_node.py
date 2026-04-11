from langchain_core.messages import ToolMessage
from core.finance_qa_agent_llm import FinanceQAAgentLLM
from prompts.finance_qa_prompt import finance_qa_prompt
from state.finance_workflow_state import FinanceWorkflowState
import json
from tools.tavily_search import TavilySearchTool
from langchain.agents import create_agent


finance_qa_agent_llm = FinanceQAAgentLLM().llm
tools = [TavilySearchTool().tool]

# One-way to bind tools to the agent is to create a new agent chain with the tools included, but this can lead to issues with tool calls not being properly handled in the workflow. Instead, we will create the agent with tools from the start and handle tool calls in the agent node function.
finance_qa_llm_with_tools = finance_qa_agent_llm.bind_tools(tools)
finance_qa_agent = finance_qa_prompt | finance_qa_llm_with_tools

# Create agent with memory
# finance_qa_agent = create_agent(
#     model=finance_qa_agent_llm,
#     tools=tools,
#     system_prompt=finance_qa_prompt
# )

# Agent node functions
def finance_qa_agent_node(state: FinanceWorkflowState):
    """Finance QA agent node"""
    messages = state["messages"]
    response = finance_qa_agent.invoke({"messages": messages})

    # Handle tool calls if present
    if hasattr(response, 'tool_calls') and response.tool_calls:
        tool_messages = []
        for tool_call in response.tool_calls:
            if tool_call['name'] == 'tavily_search_results_json':
                try:
                    tool_result = tools[0].search(query=tool_call['args']['query'], max_results=2)
                    tool_result = json.dumps(tool_result, indent=2)
                except Exception as e:
                    tool_result = f"Search failed: {str(e)}"

                tool_messages.append(ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call['id']
                ))

        if tool_messages:
            all_messages = messages + [response] + tool_messages
            final_response = finance_qa_agent.invoke({"messages": all_messages})
            return {"messages": [response] + tool_messages + [final_response]}

    return {"messages": [response]}