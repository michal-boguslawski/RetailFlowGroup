from pyspark.sql import SparkSession

from infrastructure.config.settings import SparkSettings


def create_spark_session(
    app_name: str,
    spark_settings: SparkSettings | None = None,
    shuffle_partitions: int = 2,
    packages: list[str] | None = None,
) -> SparkSession:
    spark_settings = spark_settings or SparkSettings()
    builder = SparkSession.builder

    if not isinstance(builder, SparkSession.Builder):
        raise TypeError(
            "Unexpected type of `builder`. "
            f"Expected `SparkSession.Builder`, found `{type(builder)}`."
        )

    builder = (
        builder
        .appName(app_name)
        .master(spark_settings.master_url)
        .config(
            "spark.sql.shuffle.partitions",
            shuffle_partitions,
        )
    )

    if packages:
        builder = builder.config(
            "spark.jars.packages",
            ",".join(packages),
        )

    return builder.getOrCreate()
