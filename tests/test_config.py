from ai_bug_investigator.config import Settings


def test_secret_is_hidden_in_repr():
    settings = Settings(github_token="my-secret-123")

    assert "my-secret-123" not in repr(settings)
    assert settings.github_token.get_secret_value() == "my-secret-123"


def test_empty_env_value_becomes_none(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "")
    settings = Settings(_env_file=None)
    assert settings.github_token is None
