from rest_framework import serializers
from datasources.models import Datasource
from core.models import (
    ContentPool,
    InjestedTextContent,
    ExtracterChain,
    ExtracterPrompt,
    ProcessedData,
)

# Datasources


class DatasourceSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Datasource
        fields = [
            "id",
            "datasource_name",
            "datasource_type_name",
            "created_at",
            "updated_at",
        ]


# Core


class ContentPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentPool
        fields = ("id", "created_at", "updated_at", "pool_name")


class InjestedTextContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InjestedTextContent
        fields = (
            "id",
            "created_at",
            "updated_at",
            "content_uuid",
            "content_pool",
            "text_content",
            "metadata_json",
            "datasource",
            "processed_at",
            "process_completed_successfully",
        )


class ExtracterChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtracterChain
        fields = (
            "id",
            "created_at",
            "updated_at",
            "chain_name",
            "content_pool",
            "llm_name",
        )


class ExtracterPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtracterPrompt
        fields = (
            "id",
            "created_at",
            "updated_at",
            "prompt_name",
            "prompt_text",
            "return_type",
            "jsonschema",
            "labels_config_json",
            "extracter_chain",
            "run_if_expr",
            "order_index",
        )


class ProcessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedData
        fields = (
            "id",
            "created_at",
            "updated_at",
            "content_pool",
            "injested_text_content",
            "chain",
            "prompt",
            "prompt_result",
        )
