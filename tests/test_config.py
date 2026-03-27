import os
import importlib


def test_default_settings():
    # Clear any existing env vars that might interfere
    original = dict(os.environ)
    for k in list(os.environ.keys()):
        if k.startswith("OH_ROLES_"):
            del os.environ[k]

    # Import after clearing environment so defaults are picked up correctly
    from src.config import Settings

    settings = Settings()
    assert settings.llm_provider == "openai"
    assert settings.llm_model == "gpt-4o"
    assert settings.llm_timeout == 120
    assert len(settings.default_components) == 6

    # Restore original environment
    os.environ.clear()
    os.environ.update(original)
