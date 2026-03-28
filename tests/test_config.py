import os
import importlib
from pathlib import Path


def test_default_settings():
    # Clear any existing env vars that might interfere
    original = dict(os.environ)
    for k in list(os.environ.keys()):
        if k.startswith("OH_ROLES_"):
            del os.environ[k]

    # Temporarily rename .env file if it exists
    env_path = Path(".env")
    env_backup = Path(".env.temp")
    env_exists = env_path.exists()
    if env_exists:
        env_path.rename(env_backup)

    try:
        # Import after clearing environment so defaults are picked up correctly
        from src.config import Settings

        # Create a fresh settings instance without loading from .env
        class TempSettings(Settings):
            model_config = Settings.model_config.copy()
            model_config["env_file"] = None

        settings = TempSettings()
        assert settings.llm_provider == "openai"
        assert settings.llm_model == "gpt-4o"
        assert settings.llm_timeout == 120
        assert len(settings.default_components) == 6
    finally:
        # Restore .env file if it existed
        if env_exists and env_backup.exists():
            env_backup.rename(env_path)

        # Restore original environment
        os.environ.clear()
        os.environ.update(original)
