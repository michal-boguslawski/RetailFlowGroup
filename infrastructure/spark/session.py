from pyspark.sql import SparkSession

from infrastructure.spark.config import SparkConfig
from infrastructure.minio.config import S3Config


def create_spark_session(
    app_name: str,
    spark_settings: SparkConfig | None = None,
    s3_settings: S3Config | None = None,
    shuffle_partitions: int = 2,
    packages: list[str] | None = None,
) -> SparkSession:
    spark_settings = spark_settings or SparkConfig()
    s3_settings = s3_settings or S3Config()
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
        .config("spark.hadoop.fs.s3a.endpoint", s3_settings.endpoint_docker or s3_settings.endpoint_url)
        .config("spark.hadoop.fs.s3a.access.key", s3_settings.access_key)
        .config("spark.hadoop.fs.s3a.secret.key", s3_settings.secret_key)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", str(s3_settings.secure).lower())
        .config("spark.hadoop.fs.s3a.aws.credentials.provider",
                "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
    )

    if packages:
        builder = builder.config(
            "spark.jars.packages",
            ",".join(packages),
        )

    return builder.getOrCreate()
