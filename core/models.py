from django.db import models
from base.models import BaseLLMineModel
import uuid
from core.utils.prompting import EXTRACTER_PROMPT_RETURN_TYPES

from datasources.datasource_types import DATASOURCE_TYPE_MAP


class ContentPool(BaseLLMineModel):
    pool_name = models.CharField(max_length=255, unique=True)


class InjestedTextContent(BaseLLMineModel):
    content_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    content_pool = models.ForeignKey(ContentPool, on_delete=models.CASCADE)
    text_content = models.TextField()
    metadata_json = models.JSONField(null=True, blank=True)
    datasource_type_name = models.CharField(
        max_length=255, choices=DATASOURCE_TYPE_MAP.keys()
    )
    processed_at = models.DateTimeField(null=True, blank=True)


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

    content_pool = models.ForeignKey(ContentPool, on_delete=models.CASCADE)
