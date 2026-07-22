from datetime import datetime

from domain.enums import StoreId, EntityType
from infrastructure.kafka.topics import load_store_topics
from infrastructure.spark.config import load_spark_config
from infrastructure.spark.session import create_spark_session
from ingestion.connectors.kafka import KafkaConnector
from ingestion.connectors.avro import AvroConnector
from infrastructure.lake import LAKE_PATHS_RESOLVERS


if __name__ == "__main__":
    spark_config = load_spark_config("alpha_orders")
    store_id = StoreId(spark_config.job.store)
    topics = load_store_topics(store_id)
    entity = EntityType(spark_config.job.entity)
    topic = topics[entity]
    
    spark = create_spark_session(
        spark_config.job.app_name,
        shuffle_partitions=spark_config.job.shuffle_partitions,
        packages=[
            "org.apache.kafka:kafka-clients:4.0.0",
            "org.apache.spark:spark-avro_2.13:4.2.0",
            "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0",
        ],
    )
    
    kafka_connector = KafkaConnector()
    avro_connector = AvroConnector("http://schema-registry:8081")
    df = kafka_connector.read_batch(spark, topic.name)
    df = avro_connector.decode(df)
    print(df.show())
    
    
    lake_path_resolver = LAKE_PATHS_RESOLVERS[spark_config.job.target]
    path = lake_path_resolver(
        store=store_id.value,
        entity=entity.value,
        dt=datetime.now().date()
    )
    
    checkpoint_path_resolver = LAKE_PATHS_RESOLVERS["checkpoint"]
    checkpoint_path = checkpoint_path_resolver(
        store=store_id.value,
        entity=entity.value,
    )
    print(path, checkpoint_path)
    
    # print(topics[entity])
    spark.stop()
    