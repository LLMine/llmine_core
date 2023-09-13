import uuid
from django.db import models
from base.models import BaseLLMineModel
from core.utils.llm_service import LLM_CHOICES

from core.utils.prompting import EXTRACTER_PROMPT_RETURN_TYPES
from datasources.models import Datasource


class ContentPool(BaseLLMineModel):
    pool_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.pool_name


class InjestedTextContent(BaseLLMineModel):
    content_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    content_pool = models.ForeignKey(ContentPool, on_delete=models.CASCADE)
    text_content = models.TextField()
    metadata_json = models.JSONField(null=True, blank=True)
    datasource = models.ForeignKey(Datasource, on_delete=models.CASCADE)
    processed_at = models.DateTimeField(null=True, blank=True)
    process_completed_successfully = models.BooleanField(null=True, blank=True)

    def __str__(self) -> str:
        return self.text_content

    class Meta:
        verbose_name = "Ingested Text Content"
        verbose_name_plural = "Ingested Text Data"


class ExtracterChain(BaseLLMineModel):
    chain_name = models.CharField(max_length=100, unique=True)
    content_pool = models.ForeignKey(
        ContentPool, on_delete=models.CASCADE, related_name="extracter_chains"
    )
    llm_name = models.CharField(
        max_length=255, choices=LLM_CHOICES, default="gpt-3.5-turbo"
    )

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
    run_if_expr = models.TextField(
        null=True, blank=True, help_text="Blank means always run"
    )
    order_index = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.prompt_name

    class Meta:
        unique_together = ("extracter_chain", "order_index")


class ProcessedData(BaseLLMineModel):
    content_pool = models.ForeignKey(ContentPool, on_delete=models.CASCADE)
    injested_text_content = models.ForeignKey(
        InjestedTextContent, on_delete=models.CASCADE
    )
    chain = models.ForeignKey(ExtracterChain, on_delete=models.CASCADE)
    prompt = models.ForeignKey(ExtracterPrompt, on_delete=models.CASCADE)
    prompt_result = models.TextField()

    def __str__(self) -> str:
        return f"{self.content_pool.pool_name} - {self.injested_text_content_id}"


class DataExport(BaseLLMineModel):
    export_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    export_type = models.CharField(max_length=255)
    data_file = models.FileField()

    def __str__(self) -> str:
        return self.export_uuid
