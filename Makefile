make_migrations: ## create migrations for root
	alembic --config alembic.ini revision --autogenerate -m "$(msg)"

make_migrate: ## migrate root
	alembic --config alembic.ini upgrade head

run_server:
	uvicorn cost_wiz.main:app --host 0.0.0.0 --reload

