.PHONY: install test lint format build up down logs

install:
	poetry install
test:
	poetry run pytest
lint:
	poetry run ruff check .
format:
	poetry run ruff format .


build:
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f agent