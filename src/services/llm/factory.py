from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import SecretStr

from src.config import settings
from src.exceptions import LLMProviderError


def create_llm() -> BaseChatModel:
    """Create LangChain ChatModel based on configuration."""
    provider = settings.llm_provider.lower()
    model = settings.llm_model
    api_key = settings.llm_api_key
    base_url = settings.llm_base_url
    timeout = settings.llm_timeout

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        api_key_secret = SecretStr(api_key) if api_key else None
        return ChatOpenAI(
            model=model,
            api_key=api_key_secret,
            base_url=base_url,
            timeout=timeout,
        )
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        # If using anthropic, api_key must be provided
        assert api_key is not None, "llm_api_key must be set for anthropic provider"
        api_key_secret = SecretStr(api_key)
        return ChatAnthropic(
            model_name=model,
            api_key=api_key_secret,
            base_url=base_url,
            timeout=timeout,
        )
    elif provider == "azure":
        from langchain_openai import AzureChatOpenAI
        # If using azure, api_key must be provided
        assert api_key is not None, "llm_api_key must be set for azure provider"
        assert base_url is not None, "llm_base_url must be set for azure provider"
        api_key_secret = SecretStr(api_key)
        return AzureChatOpenAI(
            azure_deployment=model,
            api_key=api_key_secret,
            azure_endpoint=base_url,
            timeout=timeout,
        )
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
    elif provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        base_url_str = base_url if base_url else "http://localhost:11434"
        return ChatOllama(
            model=model,
            base_url=base_url_str,
            timeout=timeout,
        )
    else:
        raise LLMProviderError(
            f"Unsupported LLM provider: {provider}. "
            "Supported providers: openai, anthropic, azure, gemini, ollama"
        )
