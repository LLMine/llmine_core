from abc import ABC, abstractmethod


class BaseLLMService(ABC):
    def __init__(
        self,
        model,
    ):
        pass

    @abstractmethod
    def init_chain(self):
        raise NotImplementedError()

    @abstractmethod
    def process_prompt(
        self,
        ingested_text_str: str,
        extracter_prompt_str,
        return_type,
        jsonschema=None,
        label_config_json=None,
    ) -> str:
        raise NotImplementedError()
