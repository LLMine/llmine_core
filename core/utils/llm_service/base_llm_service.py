from abc import ABC, abstractmethod

class BaseLLMService(ABC):
    @abstractmethod
    def fetch_response(self, prompts) -> str:
        raise NotImplementedError()
    
