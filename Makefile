load_products:
    python -m bootstrap.seed

reset_kafka_topics:
    python -m bootstrap.kafka --store-id alpha

reset_postgres_schema:
    python -m bootstrap.postgres --mode schema

truncate_postgres_tables:
    python -m bootstrap.postgres --mode truncate

bootstrap_users:
    python -m bootstrap.users --users 100

run_generator:
    python -m generator.runner