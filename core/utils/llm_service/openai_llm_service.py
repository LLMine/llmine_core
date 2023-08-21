import openai
from .base_llm_service import BaseLLMService
from django.conf import settings

class OpenAILLMService(BaseLLMService):
    def __init__(self, model: str = "gpt-3.5-turbo", llm_config: dict = {"temperature" : 1, "app_module" : ""} ) -> None:
        openai.api_key = settings.OPENAI_API_KEY
        self.model = model
        self.llm_config = llm_config
        self.temperature = llm_config.get("temperature")

        self.message_chain = []
    
    def fetch_response(self, messages):
        pass

    def system_prompt(self) -> str :
        message = """You're an AI assistant who's job is to derive insights based on the data 
                feeded to you below, you might recieve a chain of questions to which you honour and answer the question given below :
                """
        return {"role" : "system", "content" : message}