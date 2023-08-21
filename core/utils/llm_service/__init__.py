from .base_llm_service import BaseLLMService
from .openai_llm_service import OpenAILLMService

LLM_CHOICES = [
    ("gpt-3.5-turbo", "gpt-3.5-turbo"),
    ("gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k"),
    ("gpt-4", "gpt-4"),
]

LLM_SERVICE_MAPPING = {
    "gpt-3.5-turbo" : get_openai_llm_service,
    "gpt-3.5-turbo-16k": get_openai_llm_service,
    "gpt-4": get_openai_llm_service
}

def get_openai_llm_service(model_name, llm_config):
    '''Returns the OpenAI LLM Service based on the llm_name and llm_config'''

    return OpenAILLMService(model_name, llm_config)

def get_llm_service(llm_name : str = "gpt-3.5-turbo", llm_config: dict = None) -> BaseLLMService :
    '''Returns the LLM service based on the llm_name and llm_config'''

    llm_service = LLM_SERVICE_MAPPING.get(llm_name, None)

    if not llm_service:
        raise Exception("LLM service not configured")

    return llm_service(llm_name, llm_config)
