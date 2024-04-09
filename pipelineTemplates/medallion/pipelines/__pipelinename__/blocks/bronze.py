from pyspark.sql.streaming import StreamingQuery
from sensa_data_pipelines.executors.pyspark.mixins.profiles_sdk_mixins import (
    ProfilesSdkMixin,
    DataEndpointProfilesSdkMixin,
)
from sensa_data_pipelines.pipeline_model import (
    SensaDataModelConfig,
    SensaConnectionConfig,
)
from sensa_data_pipelines.executors.pyspark.streaming import StreamingBlock

INPUT_NAME = "bronze_input"
OUTPUT_NAME = "to_bronze"
USE_STREAMING = True


class BronzeBlock(StreamingBlock, ProfilesSdkMixin, DataEndpointProfilesSdkMixin):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def execute_stream(self, **kwargs) -> StreamingQuery:
        # NOTE: This requires streaming input (S3FileStream, GCPFileStream, KafkaStream, etc.).
        #  Need to include instructions for this, or add the ability to use the local-csv file.
        connection = self.get_input_config(INPUT_NAME, SensaConnectionConfig)
        bronze_model = self.get_output_config(OUTPUT_NAME, SensaDataModelConfig)
        stream_pair = (
            self.sensa.readStream().readConnection(connection.endpoint.project, connection.endpoint.name).load()
        )
        # write the starting data to the checkpoint, then write the streaming data
        static_df = stream_pair.getStaticDf()
        (
            static_df.write.format("delta")
            .mode("overwrite")
            .option("checkpointLocation", bronze_model.paths.checkpoint_path)
            .save(bronze_model.paths.location)
        )
        return (
            stream_pair.getStreamDf()
            .writeStream.format("delta")
            .queryName(bronze_model.paths.segment)
            .outputMode("append")
            .option("checkpointLocation", bronze_model.paths.checkpoint_path)
            .trigger(processingTime="5 seconds")
            .start(bronze_model.paths.location)
        )
