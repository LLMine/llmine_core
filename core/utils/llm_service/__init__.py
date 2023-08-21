from .base_llm_service import BaseLLMService
from .openai_llm_service import OpenAILLMService

LLM_CHOICES = [
    ("gpt-3.5-turbo", "gpt-3.5-turbo"),
    ("gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k"),
    ("gpt-4", "gpt-4"),
]

LLM_SERVICE_CLASS_MAPPING = {
    "gpt-3.5-turbo": OpenAILLMService,
    "gpt-3.5-turbo-16k": OpenAILLMService,
    "gpt-4": OpenAILLMService,
}


def get_llm_service(llm_name: str = "gpt-3.5-turbo") -> BaseLLMService:
    """Returns the LLM service based on the llm_name and llm_config"""

    llm_service_klass = LLM_SERVICE_CLASS_MAPPING[llm_name]
    return llm_service_klass(llm_name)
