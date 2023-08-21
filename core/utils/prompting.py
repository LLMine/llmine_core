# Extracters
import json
from typing import List

EXTRACTER_PROMPT_RETURN_TYPES = (("text", "text"), ("label", "label"), ("json", "json"))


def label_return_prompt(llm_name, labels: List[str]):
    """ Labels should be valid json """
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

def get_return_type_prompt(llm_name: str, return_type: str, labels_config_json: str, jsonschema: str) -> str:
    if return_type == "json":
        return json_return_prompt(llm_name, jsonschema)
    elif return_type == "label":
        return label_return_prompt(llm_name, labels_config_json)
    else:
        return "Respond with a text output."

def get_user_prompt(prompt, llm_name: str):
    return_type_prompt = get_return_type_prompt(llm_name, prompt.return_type, prompt.labels_config_json, prompt.jsonschema)
    user_content = f"""
    ######
    Question: 
    {prompt.prompt_text}

    ########
    {return_type_prompt}
    """
    return {"role" : "user", "content" : user_content}

def get_assistant_prompt(prompt, llm_name: str):
    return {"role": "assitant", "content": prompt}
