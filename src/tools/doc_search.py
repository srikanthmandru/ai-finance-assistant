from langchain.tools import tool

# # Load the vectorstore
# embeddings = OpenAIEmbeddings()
# vector = FAISS.load_local(
#     "./faiss_index", embeddings, allow_dangerous_deserialization=True
# )



# # Creating a retriever
# retriever = vector.as_retriever()

# # Define Amazon product search tool
# @tool
# def amazon_product_search(query: str) -> str:
#     """Search for information about Amazon products.
#     For any questions related to Amazon products, this tool must be used.
    
#     Args:
#         query: The search query for Amazon products
        
#     Returns:
#         str: Relevant Amazon product information
#     """
#     docs = retriever.invoke(query)
#     return "\n\n".join([doc.page_content for doc in docs])
