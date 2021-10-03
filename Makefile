run:
	uvicorn app.main:app --reload

run_db:
	docker-compose up -d

stop_db:
	docker-compose stop

migrate:
	alembic upgrade head

generate_migration:
	alembic revision --autogenerate -m "$$message"

isort:
	isort .
