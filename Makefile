load-products:
	python -m bootstrap.seed --store alpha --csv data/seed/alpha_products.csv
	python -m bootstrap.seed --store beta --csv data/seed/beta_products.csv

init-kafka-topics:
	python -m bootstrap.kafka store --store-id alpha
	python -m bootstrap.kafka store --store-id beta
	python -m bootstrap.kafka infrastructure

reset-postgres-schema:
	python -m bootstrap.postgres --mode schema

truncate-postgres-tables:
	python -m bootstrap.postgres --mode truncate

bootstrap-users:
	python -m bootstrap.users alpha --users 100
	python -m bootstrap.users beta --users 100

initialize-buckets:
	python -m bootstrap.minio

init-landing-notifications: init-kafka-topics init-buckets
	python -m bootstrap.notifications

run-generator:
	python -m generator.runner alpha
	python -m generator.runner beta
	python -m generator.runner gamma