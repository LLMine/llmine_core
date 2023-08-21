import json
from typing import List
import openai
from .base_llm_service import BaseLLMService
from django.conf import settings
from enum import Enum
from openai_app.common import OpenAIChatAPIClient


class ChatRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class OpenAILLMService(BaseLLMService):
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
    ):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = model
        self.llm_config = settings.LLM_CONFIG
        self.temperature = self.llm_config.get("temperature")

    def _get_openai_message(self, chat_role: ChatRole, content_str):
        return {"role": chat_role.value, "content": content_str}

    def _add_message(self, message):
        self.message_chain.append(message)

    def _label_return_prompt(self, label_config: List[str]):
        lables_json = json.dumps(label_config)
        return f"Respond with one of the following choices.\n{lables_json}"

    def _json_return_prompt(self, jsonschema_text):
        return f"Respond strictly with a JSON conforming to the following JSONSchema text\n{jsonschema_text}"

    def _get_return_type_prompt(
        self, return_type, jsonschema=None, label_config_json=None
    ):
        if return_type == "json":
            return self._json_return_prompt(jsonschema)
        elif return_type == "label":
            return self._label_return_prompt(label_config_json)
        else:
            return "Respond with a text output."

    def init_chain(self):
        system_prompt = """
        You are an AI Assistant that can answer questions or perform tasks related to a given text content in specified manner.
        """
        self.message_chain = [
            self._get_openai_message(ChatRole.SYSTEM, system_prompt.replace("\t", ""))
        ]

    def process_prompt(
        self,
        ingested_text_str: str,
        extracter_prompt_str,
        return_type,
        jsonschema=None,
        label_config_json=None,
    ) -> str:
        return_type_prompt = self._get_return_type_prompt(
            return_type, jsonschema, label_config_json
        )
        content = f"""
        {extracter_prompt_str}

        Text Content: ###
        {ingested_text_str}
        ###

        {return_type_prompt}        
        """
        self.message_chain.append(self._get_openai_message(ChatRole.USER, content))

        chat_client = OpenAIChatAPIClient(
            self.model, self.temperature, "Extracter Prompt Run"
        )

        step_output = chat_client.process(self.message_chain)
        self.message_chain.append(
            self._get_openai_message(ChatRole.ASSISTANT, step_output)
        )

        return step_output
