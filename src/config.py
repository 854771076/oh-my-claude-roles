from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    # Generation defaults
    default_components: list[str] = Field(
        default=["claude_md", "hooks", "commands", "agents", "rules", "skills"],
        description="Default components to generate"
    )

    model_config = SettingsConfigDict(
        env_prefix="OH_ROLES_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
