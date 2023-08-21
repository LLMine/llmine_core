import PyPDF2

import tiktoken
import openai
from openai.datalib import numpy as np

from django.conf import settings

from .models import OpenAICallLog

# from presidio_analyzer import AnalyzerEngine
# from presidio_anonymizer import AnonymizerEngine

openai.api_key = settings.OPENAI_API_KEY

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

encoding = tiktoken.get_encoding(embedding_encoding)


# def get_anonymized_text(text):
#     entities_to_anonymize = [
#         "EMAIL_ADDRESS",
#         "PERSON",
#         "PHONE_NUMBER",
#         "US_SSN",
#         "US_PASSPORT",
#         "US_DRIVER_LICENSE",
#         "URL",
#     ]

#     analyzer = AnalyzerEngine()
#     analyzer_results = analyzer.analyze(
#         text=text,
#         language="en",
#         entities=entities_to_anonymize,
#         score_threshold=0.3,
#         allow_list=allowed_keywords,
#     )

#     engine = AnonymizerEngine()
#     result = engine.anonymize(text=text, analyzer_results=analyzer_results)

#     return result.text


def log_usage(usage_type, used_in_module, prompt_token, total_token, openai_resp):
    call_log = OpenAICallLog.objects.create(
        usage_type=usage_type,
        used_in_module=used_in_module,
        prompt_token=prompt_token,
        total_token=total_token,
        openai_resp=openai_resp,
    )

    call_log.save()


def get_token_length(text):
    return len(encoding.encode(text))


def get_embedding_vector(text, module="Generic", reason="Unknown"):
    text = text.replace("\n", " ")

    openai_resp = openai.Embedding.create(input=[text], model=embedding_model)
    usage_data = openai_resp["usage"]
    try:
        log_usage(
            "embedding",
            module,
            usage_data["prompt_tokens"],
            usage_data["total_tokens"],
            openai_resp,
        )
    except Exception as e:
        print(e)
        print("Couldn't log usage")

    return openai_resp["data"][0]["embedding"]


def get_text_from_pdf(fileobj):
    pdfreader = PyPDF2.PdfReader(fileobj)

    text = ""
    for page in pdfreader.pages:
        text += "\n" + page.extract_text()

    return text


def scale_transform(x, min_x, max_x, min_y, max_y):
    return (x - min_x) / (max_x - min_x) * (max_y - min_y) + min_y


def get_cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_cosine_distance_transformed(a, b):
    return scale_transform(get_cosine_similarity(a, b), 0.5, 1, 0, 1)
