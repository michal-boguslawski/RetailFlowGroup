import argparse

from infrastructure.kafka.config import KafkaConfig
from infrastructure.postgres.factory import build_control_db_service
from infrastructure.spark.session import create_spark_session
from ingestion.connectors.kafka import KafkaConnector
from ingestion.connectors.avro import AvroConnector
from ingestion.contracts.loader import load_contract
from ingestion.writers.lake import LakeWriter
from ingestion.jobs.kafka_to_bronze import KafkaAvroBronzeIngestionJob
from ingestion.jobs.factory import build_job



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bronze ingestion job")
    parser.add_argument(
        "--contract",
        required=True,
        help="Contract name to load, e.g. 'alpha_orders'",
    )
    parser.add_argument(
        "--mode",
        choices=["batch", "streaming"],
        required=True,
        help="Ingestion mode",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    ingestion_contract = load_contract(args.contract)

    if ingestion_contract.target.layer == "bronze":
        writer = LakeWriter(
            format = ingestion_contract.target.format,
            mode=ingestion_contract.target.mode,
        )
    else:
        raise ValueError(f"Unsupported target layer: {ingestion_contract.target.layer}")

    control_db_service = build_control_db_service()

    spark = create_spark_session(
        ingestion_contract.job.app_name,
        shuffle_partitions=ingestion_contract.job.shuffle_partitions,
    )
    
    job = build_job(
        ingestion_contract=ingestion_contract,
        control_db_service=control_db_service,
        writer=writer,
    )

    query = None
    try:
        if args.mode == "batch":
            job.run_batch(spark)
        else:
            query = job.run_streaming(spark)
            query.awaitTermination()
            
    except KeyboardInterrupt:
        if query is not None:
            query.stop()

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
