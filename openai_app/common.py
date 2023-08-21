from typing import List
import openai
from openai_app.utils import log_usage
from django.conf import settings


class OpenAIChatAPIClient:
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        temperature: float = 1,
        app_module: str = "",
    ) -> None:
        openai.api_key = settings.OPENAI_API_KEY
        self.model = model
        self.temperature = temperature
        self.app_module = app_module

    def process(self, messages, request_timeout: int = 250) -> str:
        messages = messages

        system_response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            request_timeout=request_timeout,
        )
        usage_data = system_response["usage"]

        log_usage(
            "chat_completion",
            self.app_module,
            usage_data["prompt_tokens"],
            usage_data["total_tokens"],
            "",
        )

        return next(
            map(
                lambda message: message.get("content", ""),
                map(
                    lambda choice: choice.get("message", {}),
                    system_response.get("choices", []),
                ),
            )
        )
