from typing import Dict
from datasources.datasource_types.base_datasource_type import IngestableData
from .base_datasource_type import BaseDataSourceType, IngestableData


class StandardDataSourceType(BaseDataSourceType):
    def transform(data_sent_from_source: Dict) -> IngestableData:
        ingestable_data = IngestableData(
            content_pool=data_sent_from_source["content_type"],
            text_content=data_sent_from_source["text_content"],
        )

        if "metadata_json" in data_sent_from_source["metadata_json"]:
            ingestable_data.metadata_json = data_sent_from_source.get(
                "metadata_json", None
            )

        return ingestable_data
