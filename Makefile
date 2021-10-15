run:
	@uvicorn app.main:app --reload

run_db:
	@docker-compose up -d postgres

stop_db:
	@docker-compose stop postgres

migrate:
	@alembic upgrade head

generate_migration:
	@alembic revision --autogenerate -m "$$message"

clean:
	@docker-compose down && sudo rm -rf postgres-data

format:
	@autoflake -r -i --remove-all-unused-imports .
	@isort .
	@black app tests migrations

test:
	@docker-compose rm -s -f -v postgres_test
	@docker-compose up -d postgres_test
	@sleep 1
	@pytest tests -sv --pdb
	@# @pytest tests -sv --pdb --cov-report term-missing:skip-covered --cov=app tests/
