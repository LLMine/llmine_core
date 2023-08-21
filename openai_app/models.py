from django.db import models
from base.models import BaseLLMineModel


# Create your models here.
class OpenAICallLog(BaseLLMineModel):
    usage_type = models.CharField(max_length=255, null=True, blank=True)
    used_in_module = models.CharField(max_length=255, null=True, blank=True)
    prompt_token = models.IntegerField(null=True, blank=True)
    total_token = models.IntegerField(null=True, blank=True)
    openai_resp = models.TextField(null=True, blank=True)
