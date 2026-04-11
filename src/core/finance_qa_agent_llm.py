from langchain_community.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from constants import Constants

class FinanceQAAgentLLM:
    def __init__(self):
        # Initialize LLM
        self._llm = ChatGoogleGenerativeAI(api_key=Constants.GEMINI_API_KEY, temperature=Constants.TEMPERATURE, model=Constants.AGENT_LLM_MAP["finance_qa_agent"])
    
    @property
    def llm(self):
        return self._llm
    
    @llm.setter
    def set_llm(self, new_llm):
        if self._llm is not None:
            print(f"LLM already set to {type(self._llm).__name__}. Overwriting with {type(new_llm).__name__}.")

        if isinstance(new_llm, ChatOpenAI) or isinstance(new_llm, ChatGoogleGenerativeAI):
            self._llm = new_llm
        else:
            raise ValueError("Invalid LLM type. Must be an instance of ChatOpenAI or ChatGoogleGenerativeAI.")

        return
