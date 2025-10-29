makemigrations:
	alembic revision --autogenerate
migrate:
	alembic upgrade head
init_databse:
	python3 -m db_manip.db_init.init_database
start-app:
	make migrate && make init_databse && python3 -m main