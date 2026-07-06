load_products:
	python -m bootstrap.seed --store alpha --csv data/seed/alpha_products.csv
	python -m bootstrap.seed --store beta --csv data/seed/beta_products.csv

reset_kafka_topics:
	python -m bootstrap.kafka --store-id alpha
	python -m bootstrap.kafka --store-id beta

reset_postgres_schema:
	python -m bootstrap.postgres --mode schema

truncate_postgres_tables:
	python -m bootstrap.postgres --mode truncate

bootstrap_users:
	python -m bootstrap.users alpha --users 100
	python -m bootstrap.users beta --users 100

initialize_buckets:
	python -m bootstrap.minio --store-id gamma

run_generator:
	python -m generator.runner alpha
	python -m generator.runner beta