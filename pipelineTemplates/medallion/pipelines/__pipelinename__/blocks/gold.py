from pyspark.sql.streaming import StreamingQuery

from sensa_data_pipelines.executors.pyspark.mixins.profiles_sdk_mixins import (
    ProfilesSdkMixin,
    DataEndpointProfilesSdkMixin,
)
from sensa_data_pipelines.executors.pyspark.mixins.pyspark_mixins import PySparkMixin
from sensa_data_pipelines.pipeline_model import (
    SensaDataModelConfig,
    SensaProfileSchemaConfig,
)
from sensa_data_pipelines.executors.pyspark.streaming import StreamingBlock

INPUT_NAME = "from_profile_schema"
OUTPUT_NAME = "to_gold_checkpoint"

class GoldBlock(
    StreamingBlock, PySparkMixin, ProfilesSdkMixin, DataEndpointProfilesSdkMixin
):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def execute_stream(self, **kwargs) -> StreamingQuery:
        profile_schema = self.get_input_config(
            INPUT_NAME, SensaProfileSchemaConfig
        )

        readStream = (
            self.spark.readStream.format("delta")
            .option("readChangeFeed", "true")
            .option("startingVersion", 0)
            .load(profile_schema.paths.location)
        )

        def writeMongo(batch, epoch):
            batch.persist()

            # TODO(LA): Need to remove references to Mongo, the final table reference is
            format_ = "mongo"
            common_options = ["spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.ContactMedium"]

            batch.select("contactMedium.*").write.format(format_).mode("append").option(**common_options).save()
            batch.select("customer.*").write.format(format_).mode("append").option(**common_options).save()
            batch.select("customer360.*").write.format(format_).mode("append").option().save()
            batch.select("individual.*").write.format(format_).mode("append").option().save()
            batch.select("loyalty.*").write.format(format_).mode("append").option().save()
            batch.select("partyInteraction.*").write.format(format_).mode("append").option().save()
            batch.select("resource.*").write.format("format_").mode("append").option().save()
            batch.select("usage.*").write.format("mongo").mode("append").option().save()
            batch.write.format("mongo").mode("append").option().save()

            #batch.select("contactMedium.*").write.format("mongo").mode("append").option(
            #    "spark.mongodb.output.uri",
            #    "mongodb://localhost:27017/mctest.ContactMedium",
            #).save()
            #batch.select("customer.*").write.format("mongo").mode("append").option(
            #    "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.Customer"
            #).save()
            #batch.select("customer360.*").write.format("mongo").mode("append").option(
            #    "spark.mongodb.output.uri",
            #    "mongodb://localhost:27017/mctest.Customer360",
            #).save()
            #batch.select("individual.*").write.format("mongo").mode("append").option(
            #    "spark.mongodb.output.uri",
            #    "mongodb://localhost:27017/mctest.Individual",
            #).save()
            #batch.select("loyalty.*").write.format("mongo").mode("append").option(
            #    "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.Loyalty"
            #).save()
            #batch.select("partyInteraction.*").write.format("mongo").mode(
            #    "append"
            #).option(
            #    "spark.mongodb.output.uri",
            #    "mongodb://localhost:27017/mctest.PartyInteraction",
            #).save()
            #batch.select("resource.*").write.format("mongo").mode("append").option(
            #    "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.Resource"
            #).save()
            #batch.select("usage.*").write.format("mongo").mode("append").option(
            #    "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.Usage"
            #).save()
            #batch.write.format("mongo").mode("append").option(
            #    "spark.mongodb.output.uri", "mongodb://localhost:27017/mctest.All"
            #).save()

            batch.unpersist()

        output_connection = self.get_output_config(
            OUTPUT_NAME, SensaDataModelConfig
        )

        print("Done!")
        if True:
            return 0 # TODO: Short-circuit prior to actually writing data - need to decide final format

        return (
            readStream.writeStream.queryName(output_connection.paths.segment)
            .option("checkpointLocation", output_connection.paths.checkpoint_path)
            .outputMode("append")
            .foreachBatch(writeMongo)
            .start()
        )
