from fastapi.testclient import TestClient

from ai_bug_investigator.api import webhooks
from ai_bug_investigator.api.main import app

client = TestClient(app)


def test_sentry_webhook_saves_raw_body(tmp_path, monkeypatch):
    # tmp_path — временная папка от pytest: тест не мусорит в настоящей var/
    monkeypatch.setattr(webhooks, "RAW_DIR", tmp_path)
    raw = b'{"action": "triggered"}'

    response = client.post(
        "/webhooks/sentry",
        content=raw,
        headers={"Sentry-Hook-Resource": "event_alert"},
    )

    assert response.status_code == 200
    saved = list(tmp_path.glob("*-event_alert.body.json"))
    assert len(saved) == 1
    # Байты сохранены в точности такими, какими пришли
    assert saved[0].read_bytes() == raw