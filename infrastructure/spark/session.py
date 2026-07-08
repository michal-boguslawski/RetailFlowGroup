from pyspark.sql import SparkSession
from infrastructure.spark.config import spark_config


def create_spark_session():

    return (
        SparkSession.builder
        .appName(spark_config.app_name)
        .config(
            "spark.sql.shuffle.partitions",
            spark_config.shuffle_partitions
        )
        .getOrCreate()
    )
