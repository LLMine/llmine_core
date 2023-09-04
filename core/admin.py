from django.contrib import admin
from core.models import *
from datasources.models import *


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
