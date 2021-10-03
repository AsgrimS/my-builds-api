run_dev:
	uvicorn app.main:app --reload

run_db:
	docker-compose up -d

stop_db:
	docker-compose stop

migrate:
	alembic upgrade head

make_migration:
	alembic revision -m "$$message"
