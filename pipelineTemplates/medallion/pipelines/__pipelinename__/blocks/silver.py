from sensa_data_pipelines.executors.pyspark.mixins.profiles_sdk_mixins import (
    ProfilesSdkMixin,
    DataEndpointProfilesSdkMixin,
    OpenMetadataProfilesSdkMixin,
)
from sensa_data_pipelines.executors.pyspark.mixins.pyspark_mixins import (
    PySparkMixin,
    DbtPySparkMixin,
)
from sensa_data_pipelines.integrations.open_metadata.open_metadata_mixin import (
    OpenMetadataJobConfig,
    OpenMetadataJobTypes,
)
from sensa_data_pipelines.pipeline_model import (
    SensaDataModelConfig,
    SensaDataSourceConfig,
    SensaProfileSchemaConfig,
)
from sensa_data_pipelines.executors.pyspark.streaming import StreamingBlock

INPUT_NAME = "from_bronze"
OUTPUT_NAME = "to_data_source"

class SilverBlock(
    StreamingBlock,
    DbtPySparkMixin,
    PySparkMixin,
    ProfilesSdkMixin,
    DataEndpointProfilesSdkMixin,
    OpenMetadataProfilesSdkMixin,
):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def execute(self, **kwargs) -> str:
        bronze_model = self.get_input_config(INPUT_NAME, SensaDataModelConfig)
        data_source = self.get_output_config(OUTPUT_NAME, SensaDataSourceConfig)
        profile_schema = self.get_output_config(
            "to_profile_schema", SensaProfileSchemaConfig
        )

        # TODO infer?
        dbt_vars = dict(
            {
                "bronze-location": bronze_model.paths.location,
                "path-silver": data_source.paths.location_root,
                "alias-silver": data_source.paths.segment,
                "path-gold": profile_schema.paths.location_root,
                "alias-gold": profile_schema.paths.segment,
            }
        )
        run_results = self.run_dbt(dbt_vars=dbt_vars)
        self.logger.info("Completed dbt Job")
        self.logger.info("Running OpenMetadata Job")
        self.run_open_metadata_job(
            [
                OpenMetadataJobConfig(OpenMetadataJobTypes.DELTA_LAKE_INGEST, None),
                OpenMetadataJobConfig(OpenMetadataJobTypes.DELTA_LAKE_PROFILE, None),
                OpenMetadataJobConfig(OpenMetadataJobTypes.DBT, None),
            ]
        )

        if not run_results.success:
            self.logger.error(
                "DBT run failed, results have been uploaded to MC and ingested by OM"
            )

        return "ran"
