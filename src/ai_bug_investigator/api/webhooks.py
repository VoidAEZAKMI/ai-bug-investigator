"""Приём вебхуков от Sentry.

Шаг 2.2: ничего не разбираем и не проверяем, только сохраняем запрос как есть.
Эти файлы станут фикстурами: на них мы разработаем парсинг (2.3) без Sentry.
"""

import json
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, Request

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

# Папка в .gitignore: сырые запросы не коммитим, сначала просматриваем глазами
RAW_DIR = Path("var/webhooks/sentry")


@router.post("/sentry")
async def sentry_webhook(request: Request) -> dict[str, str]:
    # Берём тело как СЫРЫЕ БАЙТЫ, без разбора JSON.
    # Подпись Sentry (шаг 2.3) считается ровно по этим байтам:
    # если распарсить и сохранить заново, байты изменятся и подпись не сойдётся.
    body = await request.body()

    # Какой тип события пришёл (event_alert, issue и т.д.) — из заголовка
    resource = request.headers.get("sentry-hook-resource", "unknown")

    # Сохраняем только заголовки Sentry: среди них подпись и время отправки
    sentry_headers = {
        k: v for k, v in request.headers.items() if k.lower().startswith("sentry-")
    }

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f")
    (RAW_DIR / f"{stamp}-{resource}.body.json").write_bytes(body)
    (RAW_DIR / f"{stamp}-{resource}.headers.json").write_text(
        json.dumps(sentry_headers, indent=2), encoding="utf-8"
    )

    # Отвечаем сразу: Sentry ждёт ответа недолго, а при ошибке может повторить отправку
    return {"status": "received"}