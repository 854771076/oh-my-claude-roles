from src.config import Settings
from pydantic_settings import SettingsConfigDict


def test_default_settings():
    settings = Settings()
    assert settings.llm_provider == "openai"
    assert settings.llm_model == "gpt-4o"
    assert settings.llm_timeout == 120
    assert len(settings.default_components) == 6
