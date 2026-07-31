load-products:
	python -m bootstrap.seed --store alpha --csv data/seed/alpha_products.csv
	python -m bootstrap.seed --store beta --csv data/seed/beta_products.csv

init-kafka-topics:
	python -m bootstrap.kafka store --store-id alpha
	python -m bootstrap.kafka store --store-id beta
	python -m bootstrap.kafka infrastructure

reset-postgres-schema:
	python -m bootstrap.postgres --mode schema --store alpha
	python -m bootstrap.postgres --mode schema --store metadata

truncate-postgres-tables:
	python -m bootstrap.postgres --mode truncate --store alpha
	python -m bootstrap.postgres --mode truncate --store metadata

bootstrap-users:
	python -m bootstrap.users alpha --users 100
	python -m bootstrap.users beta --users 100

initialize-buckets:
	python -m bootstrap.minio

init-landing-notifications: init-kafka-topics init-buckets
	python -m bootstrap.notifications

generate-orders:
	python -m bootstrap.generate gamma --event_type orders --num 10000

run-generator:
	python -m generator.runner alpha
	python -m generator.runner beta
	python -m generator.runner gamma

alpha-bronze-ingestion:
	python -m ingestion.runner --contract alpha_kafka_orders --mode batch
	python -m ingestion.runner --contract alpha_kafka_clickstreams --mode batch
	python -m ingestion.runner --contract alpha_db_users --mode batch
	python -m ingestion.runner --contract alpha_db_products --mode batch
	python -m ingestion.runner --contract alpha_db_orders --mode batch
	python -m ingestion.runner --contract alpha_db_order_items --mode batch

beta-bronze-ingestion:
	python -m ingestion.runner --contract beta_kafka_orders --mode batch
	python -m ingestion.runner --contract beta_kafka_clickstreams --mode batch
	python -m ingestion.runner --contract beta_db_user_profiles --mode batch
	python -m ingestion.runner --contract beta_db_products --mode batch

bronze-ingestion: alpha-bronze-ingestion beta-bronze-ingestion
