import uuid
from django.db import models
from base.models import BaseLLMineModel
from core.utils.llm_service import LLM_CHOICES

from core.utils.prompting import EXTRACTER_PROMPT_RETURN_TYPES
from datasources.models import Datasource


class ContentPool(BaseLLMineModel):
    pool_name = models.CharField(max_length=255, unique=True)
    llm_name = models.CharField(max_length=255, choices=LLM_CHOICES)

    def __str__(self) -> str:
        return self.pool_name


class InjestedTextContent(BaseLLMineModel):
    content_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    content_pool = models.ForeignKey(ContentPool, on_delete=models.CASCADE)
    text_content = models.TextField()
    metadata_json = models.JSONField(null=True, blank=True)
    datasource = models.ForeignKey(Datasource, on_delete=models.CASCADE)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.text_content

class ExtracterChain(BaseLLMineModel):
    chain_name = models.CharField(max_length=100, unique=True)
    content_pool = models.ForeignKey(ContentPool, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.chain_name

class ExtracterPrompt(BaseLLMineModel):
    prompt_name = models.CharField(max_length=100, unique=True)
    prompt_text = models.TextField()
    return_type = models.CharField(
        max_length=255, choices=EXTRACTER_PROMPT_RETURN_TYPES
    )
    jsonschema = models.TextField(
        null=True, blank=True, help_text="Only used when return type is json"
    )

    labels_config_json = models.JSONField(
        null=True, blank=True, help_text="Only used when return type is label"
    )

    extracter_chain = models.ForeignKey(ExtracterChain, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.prompt_name