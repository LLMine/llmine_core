from django.db import models

from base.models import BaseLLMineModel
from .datasource_types import DATASOURCE_TYPE_MAP


# Create your models here.
class Datasource(BaseLLMineModel):
    datasource_name = models.CharField(max_length=255, unique=True)
    datasource_type_name = models.CharField(
        max_length=255,
        choices=tuple((item, item) for item in DATASOURCE_TYPE_MAP.keys()),
    )

    def __str__(self) -> str:
        return self.datasource_name
