from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_user_config_dir() -> Path:
    """Get user configuration directory (~/.oh-my-claude-roles)"""
    home = Path.home()
    return home / ".oh-my-claude-roles"


def get_env_files() -> list[str]:
    """Get environment file paths in order of precedence"""
    user_config_dir = get_user_config_dir()
    return [str(user_config_dir / ".env"), ".env"]


class Settings(BaseSettings):
    # LLM configuration
    llm_provider: str = Field(
        default="openai",
        description="LLM provider: openai, anthropic, azure, gemini, ollama"
    )
    llm_api_key: str | None = Field(
        default=None,
        description="LLM API Key"
    )
    llm_model: str = Field(
        default="gpt-4o",
        description="Model name"
    )
    llm_base_url: str | None = Field(
        default=None,
        description="API Base URL (for local models or proxy)"
    )
    llm_timeout: int = Field(
        default=120,
        description="LLM API call timeout in seconds"
    )
    llm_max_retries: int = Field(
        default=3,
        description="Maximum retry attempts for LLM calls"
    )
    llm_concurrency: int = Field(
        default=3,
        description="Concurrent LLM requests limit"
    )

    # Path configuration
    roles_dir: str = Field(
        default="roles",
        description="Roles directory path (relative to project root)"
    )
    packages_dir: str = Field(
        default="packages",
        description="Package cache directory path"
    )

    # User configuration directory
    user_config_dir: Path = Field(
        default_factory=get_user_config_dir,
        description="User configuration directory"
    )

    @property
    def user_roles_dir(self) -> Path:
        """User roles directory (~/.oh-my-claude-roles/roles)"""
        return self.user_config_dir / "roles"

    @property
    def user_packages_dir(self) -> Path:
        """User packages directory (~/.oh-my-claude-roles/packages)"""
        return self.user_config_dir / "packages"

    # Generation defaults
    default_components: list[str] = Field(
        default=["hooks", "commands", "agents", "rules", "skills", "claude_md"],
        description=(
            "Default components to generate "
            "(claude_md last to include all tool indexes)"
        )
    )

    model_config = SettingsConfigDict(
        env_prefix="OH_ROLES_",
        env_file=get_env_files(),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
