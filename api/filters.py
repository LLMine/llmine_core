from django_filters import rest_framework as filters
from core.models import (
    ContentPool,
    InjestedTextContent,
    ExtracterChain,
    ExtracterPrompt,
    ProcessedData,
)


class ContentPoolFilter(filters.FilterSet):
    class Meta:
        model = ContentPool
        fields = {
            "pool_name": ["exact", "icontains"],
        }


class InjestedTextContentFilter(filters.FilterSet):
    class Meta:
        model = InjestedTextContent
        fields = {
            "content_uuid": ["exact"],
            "content_pool__pool_name": [
                "exact",
                "icontains",
            ],  # Assuming pool_name is unique
            "datasource__datasource_name": [
                "exact",
                "icontains",
            ],  # Replace with 'name' if it's unique
            "processed_at": ["exact", "gte", "lte"],
            "process_completed_successfully": ["exact"],
        }


class ExtracterChainFilter(filters.FilterSet):
    class Meta:
        model = ExtracterChain
        fields = {
            "chain_name": ["exact", "icontains"],
            "content_pool__pool_name": ["exact", "icontains"],
            "llm_name": ["exact"],
        }


class ExtracterPromptFilter(filters.FilterSet):
    class Meta:
        model = ExtracterPrompt
        fields = {
            "prompt_name": ["exact", "icontains"],
            "return_type": ["exact"],
            "extracter_chain__chain_name": ["exact", "icontains"],
            "order_index": ["exact", "gte", "lte"],
        }


class ProcessedDataFilter(filters.FilterSet):
    class Meta:
        model = ProcessedData
        fields = {
            "content_pool__pool_name": ["exact", "icontains"],
            "injested_text_content__content_uuid": ["exact"],
            "chain__chain_name": ["exact", "icontains"],
            "prompt__prompt_name": ["exact", "icontains"],
        }
