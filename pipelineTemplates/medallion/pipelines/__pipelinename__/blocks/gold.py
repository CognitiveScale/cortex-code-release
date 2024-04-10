import os
from pyspark.sql.streaming import StreamingQuery

from sensa_data_pipelines.executors.pyspark.mixins.profiles_sdk_mixins import (
    ProfilesSdkMixin,
    DataEndpointProfilesSdkMixin,
)
from sensa_data_pipelines.executors.pyspark.mixins.pyspark_mixins import (
    PySparkMixin,
)
from sensa_data_pipelines.pipeline_model import (
    SensaDataModelConfig,
    SensaProfileSchemaConfig,
)
from sensa_data_pipelines.executors.pyspark.streaming import StreamingBlock

INPUT_NAME = "from_profile_schema"
OUTPUT_NAME = "to_gold_checkpoint"

# Collection of fields to aggregate as their own DeltaTable
sub_tables = [
    "contactMedium",
    "customer",
    "customer360",
    "individual",
    "loyalty",
    "partyInteraction",
    "resource",
    "usage",
]


class GoldBlock(StreamingBlock, PySparkMixin, ProfilesSdkMixin, DataEndpointProfilesSdkMixin):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def write_delta(self, batch, epoch):
        """Writes the given batch to separate Delta tables."""
        batch.persist()
        format_ = "delta"
        gold_destination = self.ods_conn.paths.location
        gold_checkpoint = self.ods_conn.paths.checkpoint_path
        # Collect dedicated tables
        for f in sub_tables:
            selection = f"{f}.*"  # using wildcard
            # Resolve the paths to the destination & checkpoint files for the subtable by appending
            # the subtable name
            destination = os.path.dirname(gold_checkpoint) + "-" + f
            checkpoint = os.path.join(destination, os.path.basename(gold_checkpoint))
            batch.select(selection).write.format(format_).mode("append").option(
                "checkpointLocation", checkpoint
            ).option("delta.enableChangeDataFeed", "false").save(destination)
            self.logger.info(
                "Appended batch '%s' to table '%s' to '%s' (checkpoint: %s)",
                epoch,
                selection,
                destination,
                checkpoint,
            )
        # Write the entire batch to its own DeltaTable ("gold")
        (
            batch.write.format(format_)
            .mode("append")
            .option("checkpointLocation", gold_checkpoint)
            .option("delta.enableChangeDataFeed", "false")
            .save(gold_destination)
        )
        self.logger.info(
            "Appended batch '%s' to aggregate DeltTable '%s' (checkpoint: %s)",
            epoch,
            gold_destination,
            gold_checkpoint,
        )
        batch.unpersist()

    def write_mongo(self, batch, epoch):
        """Writes the given batch to separate tables in MongoDB"""
        # Write to "external" Mongo (i.e. not a Cortex Connection)
        batch.persist()
        format_ = "mongo"
        mongo_base_uri = "mongodb://localhost:27017/gold"
        # Collect dedicated tables
        for f in sub_tables:
            selection = f"{f}.*"  # using wildcard
            table_uri = f"{mongo_base_uri}.f"
            batch.select(selection).write.format(format_).mode("append").option(
                "spark.mongodb.output.uri", table_uri
            ).save()
            self.logger.info("Wrote subset of batch '%s' to table '%s'", epoch, f)
        # Write the entire batch to its own table (All)
        batch.write.format(format_).mode("append").option("spark.mongodb.output.uri", f"{mongo_base_uri}.All").save()
        self.logger.info("Wrote batch '%s' to table All", epoch)
        batch.unpersist()

    def execute_stream(self, **kwargs) -> StreamingQuery:
        profile_schema = self.get_input_config(INPUT_NAME, SensaProfileSchemaConfig)
        readStream = (
            self.spark.readStream.format("delta")
            .option("readChangeFeed", "true")
            .option("startingVersion", 0)
            .load(profile_schema.paths.location)
        )
        # Store a reference to the Output as a property of self (make it usable across methods)
        self.ods_conn = self.get_output_config(OUTPUT_NAME, SensaDataModelConfig)
        return (
            readStream.writeStream.queryName(self.ods_conn.paths.segment)
            .option("checkpointLocation", self.ods_conn.paths.checkpoint_path)
            .outputMode("append")
            .foreachBatch(self.write_delta)
            .start()
        )
