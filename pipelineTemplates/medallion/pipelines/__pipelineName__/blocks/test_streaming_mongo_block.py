from pyspark.sql.streaming import StreamingQuery

from sensa_data_pipelines.executors.pyspark.mixins.profiles_sdk_mixins import (
    ProfilesSdkMixin,
    DataEndpointProfilesSdkMixin,
)
from sensa_data_pipelines.executors.pyspark.mixins.pyspark_mixins import PySparkMixin
from sensa_data_pipelines.pipeline_model import SensaDataModelConfig, SensaProfileSchemaConfig
from sensa_data_pipelines.executors.pyspark.streaming import StreamingBlock


class Test_Streaming_Mongo_Block(StreamingBlock, PySparkMixin, ProfilesSdkMixin, DataEndpointProfilesSdkMixin):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def execute_stream(self, **kwargs) -> StreamingQuery:
        profile_schema = self.get_input_config("from_profile_schema", SensaProfileSchemaConfig)

        readStream = (
            self.spark.readStream.format("delta")
            .option("readChangeFeed", "true")
            .option("startingVersion", 0)
            .load(profile_schema.paths.location)
        )

        def writeMongo(batch, epoch):
            batch.persist()
            batch.select("contactMedium.*").write.format("mongo").mode("append").option(
                "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.ContactMedium"
            ).save()
            batch.select("customer.*").write.format("mongo").mode("append").option(
                "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.Customer"
            ).save()
            batch.select("customer360.*").write.format("mongo").mode("append").option(
                "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.Customer360"
            ).save()
            batch.select("individual.*").write.format("mongo").mode("append").option(
                "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.Individual"
            ).save()
            batch.select("loyalty.*").write.format("mongo").mode("append").option(
                "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.Loyalty"
            ).save()
            batch.select("partyInteraction.*").write.format("mongo").mode("append").option(
                "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.PartyInteraction"
            ).save()
            batch.select("resource.*").write.format("mongo").mode("append").option(
                "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.Resource"
            ).save()
            batch.select("usage.*").write.format("mongo").mode("append").option(
                "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.Usage"
            ).save()
            batch.write.format("mongo").mode("append").option(
                "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.All"
            ).save()
            batch.unpersist()

        mongo_connection = self.get_output_config("to_mongo_checkpoint", SensaDataModelConfig)

        return (
            readStream.writeStream.queryName(mongo_connection.paths.segment)
            .option("checkpointLocation", mongo_connection.paths.checkpoint_path)
            .outputMode("append")
            .foreachBatch(writeMongo)
            .start()
        )
