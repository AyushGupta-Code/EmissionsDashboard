.PHONY: up down logs api web psql seed

up:
	docker compose --env-file .env up -d --build
	docker compose logs -f --tail=50

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=100

api:
	@echo "Open http://localhost:8000/docs"

web:
	@echo "Open http://localhost:5173"

psql:
	docker exec -it emissions_db psql -U $$POSTGRES_USER -d $$POSTGRES_DB

seed:
	docker exec -it emissions_db psql -U $$POSTGRES_USER -d $$POSTGRES_DB -f /docker-entrypoint-initdb.d/seeds/seed_demo.sql
