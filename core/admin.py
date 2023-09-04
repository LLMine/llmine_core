from typing import Optional, Type
from django.contrib import admin, messages
from django.contrib.admin.sites import AdminSite
from core.models import *
from datasources.models import *
from django.db.models.query import QuerySet
from core.tasks import process_data_export


class CustomModelAdmin(admin.ModelAdmin):
    exclude = ("is_deleted",)

    def has_delete_permission(self, request, obj=None):
        return False

    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)

    soft_delete.short_description = "Soft delete selected items"
    actions = [soft_delete]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


# ContentPoolAdmin
@admin.register(ContentPool)
class ContentPoolAdmin(CustomModelAdmin):
    list_display = ("pool_name", "created_at", "updated_at")

    list_filter = ("pool_name", "created_at", "updated_at")

    list_filter = list_display


# InjestedTextContentAdmin
@admin.register(InjestedTextContent)
class InjestedTextContentAdmin(CustomModelAdmin):
    list_display = (
        "content_uuid",
        "content_pool",
        "datasource",
        "processed_at",
        "process_completed_successfully",
        "created_at",
        "updated_at",
    )
    list_filter = list_display
    exclude = ("is_deleted",)

    def __init__(self, model: type, admin_site: AdminSite | None) -> None:
        super().__init__(model, admin_site)
        self.actions += [self.export_data]

    def export_data(self, request, queryset: QuerySet[InjestedTextContent]):
        pools = queryset.distinct("content_pool_id").order_by("content_pool_id")
        print(pools)
        if len(pools) < 1:
            raise Exception("This shouldn't have happened")

        if len(pools) > 1:
            messages.error(
                request, "Please select data from a single content pool only"
            )
        else:
            ids = list(queryset.values_list("id", flat=True))
            process_data_export.delay(ids, pools[0].content_pool_id)


# ExtracterChainAdmin
class ExtracterPromptInline(admin.StackedInline):
    model = ExtracterPrompt
    extra = 1
    fields = (
        "prompt_name",
        "prompt_text",
        "return_type",
        "jsonschema",
        "labels_config_json",
        "order_index",
        "run_if_expr",
        "is_deleted",
    )
    can_delete = False


@admin.register(ExtracterChain)
class ExtracterChainAdmin(CustomModelAdmin):
    list_display = (
        "chain_name",
        "content_pool",
        "llm_name",
        "created_at",
        "updated_at",
    )

    exclude = ("is_deleted",)
    list_filter = list_display

    inlines = [ExtracterPromptInline]


# ExtracterPromptAdmin
# @admin.register(ExtracterPrompt)
# class ExtracterPromptAdmin(admin.ModelAdmin):
#     list_display = (
#         "prompt_name",
#         "extracter_chain",
#         "return_type",
#         "order_index",
#         "created_at",
#         "updated_at",
#     )
#     exclude = ("is_deleted",)


# ProcessedDataAdmin
@admin.register(ProcessedData)
class ProcessedDataAdmin(CustomModelAdmin):
    list_display = (
        "content_pool",
        "injested_text_content",
        "chain",
        "prompt",
        "prompt_result",
        "created_at",
        "updated_at",
    )
    exclude = ("is_deleted",)
    list_filter = (
        "content_pool",
        "injested_text_content",
        "chain",
        "created_at",
        "updated_at",
    )


# DatasourceAdmin
@admin.register(Datasource)
class DatasourceAdmin(CustomModelAdmin):
    list_display = (
        "datasource_name",
        "datasource_type_name",
        "created_at",
        "updated_at",
    )
    exclude = ("is_deleted",)
    list_filter = list_display


@admin.register(DataExport)
class DataExportAdmin(CustomModelAdmin):
    list_display = (
        "export_uuid",
        "export_type",
        "data_file",
        "created_at",
        "updated_at",
    )
