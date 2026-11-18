"""HTTP-слой агента (Ingestion Layer из архитектуры).

Здесь живут только HTTP-эндпоинты. Логики агента тут не будет:
эндпоинты принимают запросы и передают работу дальше.
"""

from fastapi import FastAPI

from ai_bug_investigator.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}
