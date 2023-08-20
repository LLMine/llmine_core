from django.db import models


class StandardManager(models.Manager):
    pass


class NonDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
