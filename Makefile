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

clean:
	docker-compose down && sudo rm -rf postgres-data

format:
	autoflake -r -i --remove-all-unused-imports . &&\
	isort . &&\
	black app &&\
	black migrations
