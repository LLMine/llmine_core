# Extracters
import json
from typing import List

EXTRACTER_PROMPT_RETURN_TYPES = ("text", "label", "json")


def label_return_prompt(llm_name, labels: List[str]):
    if llm_name in ["gpt-3.5", "gpt-4"]:
        lables_json = json.dumps(labels)
        return f"Respond with one of the following choices.\n{lables_json}"
    else:
        return f"Respond with one of the following choices.\n{lables_json}"


def json_return_prompt(llm_name, jsonschema_text):
    # TODO: Validate if jsonschema_text is a valid jsonschema itself
    if llm_name in ["gpt-3.5", "gpt-4"]:
        return f"Respond strictly with a JSON conforming to the following JSONSchema text\n{jsonschema_text}"
    else:
        return f"Respond strictly with a JSON conforming to the following JSONSchema text\n{jsonschema_text}"
