.PHONY: install test lint format run tunnel build up down logs

install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

run:
	poetry run uvicorn ai_bug_investigator.api.main:app --reload --port 8000

tunnel:
	cloudflared tunnel --url http://localhost:8000

build:
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f agent