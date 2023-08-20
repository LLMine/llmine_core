from django.db import models
from .managers import NonDeletedManager, StandardManager


# Create your models here.
class BaseLLMineModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    objects = NonDeletedManager()
    standard_objects = StandardManager()

    class Meta:
        abstract = True
