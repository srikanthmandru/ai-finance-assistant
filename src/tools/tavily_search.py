from langchain_tavily import TavilySearch
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

class TavilySearchTool:
    def __init__(self):
        self.tool = TavilySearch(max_results=2)
    

# # Define Tavily search tool
# @tool
# def search_tavily(query: str) -> str:
#     """Executes a web search using Tavily for current information.
    
#     Args:
#         query: The search query entered by the user
        
#     Returns:
#         str: Search results with answers and content
#     """
#     search_tool = TavilySearchResults(
#         max_results=5,
#         include_answer=True,
#         include_raw_content=True,
#         include_images=True,
#     )
#     results = search_tool.invoke(query)
    
#     # Format results as string
#     if isinstance(results, list):
#         return "\n\n".join([str(r) for r in results])
#     return str(results)
